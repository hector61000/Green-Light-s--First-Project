from flask import Flask, render_template, request, send_from_directory
import os
from doc_processor import extract_structured_content
import re 
import unicodedata
from weasyprint import HTML, CSS
import logging # For logging

app = Flask(__name__)
# Basic logging configuration
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO) # Ensure Flask's logger also respects this level
# Define base directories relative to the app's root path (where app.py is)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
COVER_UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output') # For generated PDF and HTML

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COVER_UPLOAD_FOLDER'] = COVER_UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    # Ensure all necessary directories exist
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['COVER_UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    except OSError as e:
        app.logger.error(f"Error creating directories: {e}")
        return render_template('results.html', error_message=f"Server error: Could not create necessary storage locations. Please contact support. Details: {str(e)}")
    
    word_file = request.files.get('word_file')
    cover_image = request.files.get('cover_image')
    
    word_file_path = None
    word_file_name = None 
    cover_image_filename = None
    
    # Process Word file
    if word_file and word_file.filename: # Ensure filename is not empty
        word_file_name = word_file.filename # Use werkzeug.utils.secure_filename in production
        try:
            word_file_path = os.path.join(app.config['UPLOAD_FOLDER'], word_file_name)
            word_file.save(word_file_path)
            app.logger.info(f"Uploaded Word file: {word_file_name}")
        except Exception as e:
            app.logger.error(f"Error saving uploaded Word file {word_file_name}: {e}")
            return render_template('results.html', error_message=f"Error saving uploaded Word file: {str(e)}", word_file_name=word_file_name)
    else: # No word file or empty filename
        return render_template('results.html', error_message="No Word document was uploaded or filename is empty. Please upload a valid .docx file.", word_file_name=None)
        
    # Process Cover image
    if cover_image and cover_image.filename: # Ensure filename is not empty
        cover_image_filename = cover_image.filename # Use secure_filename
        try:
            cover_image_save_path = os.path.join(app.config['COVER_UPLOAD_FOLDER'], cover_image_filename)
            cover_image.save(cover_image_save_path)
            app.logger.info(f"Uploaded Cover image: {cover_image_filename}")
        except Exception as e:
            app.logger.error(f"Error saving cover image {cover_image_filename}: {e}")
            # Non-fatal for cover image, proceed with Word file processing but log error.
            # User will see no cover image.
            cover_image_filename = None # Ensure it's None if save failed

    # At this point, word_file_path should be valid if we haven't returned an error
    if not word_file_path or not os.path.exists(word_file_path):
         # This case should ideally be caught by earlier checks, but as a safeguard:
        app.logger.error(f"Word file path not valid or file does not exist: {word_file_path}")
        return render_template('results.html', error_message="Critical error: Word file was not properly saved or found.", word_file_name=word_file_name)

    try:
        app.logger.info(f"Starting content extraction for: {word_file_name}")
        chapters_data, images_to_save = extract_structured_content(word_file_path)
        app.logger.info(f"Content extraction complete. Found {len(images_to_save)} images.")
        
        # Save extracted content images
        if images_to_save:
            app.logger.info(f"Saving {len(images_to_save)} content images...")
            for image_data in images_to_save:
                try:
                    img_filepath = os.path.join(app.config['COVER_UPLOAD_FOLDER'], image_data['unique_filename'])
                    with open(img_filepath, 'wb') as img_f:
                        img_f.write(image_data['blob'])
                    app.logger.info(f"Saved content image: {image_data['unique_filename']}")
                except IOError as e: # More specific for file write errors
                    app.logger.error(f"IOError saving content image {image_data.get('unique_filename', 'unknown')}: {e}")
                    # Non-fatal for individual image save, but log it.
                except Exception as e: # Catch any other unexpected errors
                    app.logger.error(f"Unexpected error saving content image {image_data.get('unique_filename', 'unknown')}: {e}")
        
    except (ValueError, RuntimeError) as e: # Catch errors from extract_structured_content
        app.logger.error(f"Error during content extraction from {word_file_name}: {e}")
        return render_template('results.html', error_message=str(e), word_file_name=word_file_name, cover_image_filename=cover_image_filename)
    except Exception as e: # Catch any other unexpected error during extraction phase
        app.logger.error(f"Unexpected critical error during processing of {word_file_name}: {e}")
        return render_template('results.html', error_message=f"An unexpected server error occurred during document processing. Details: {str(e)}", word_file_name=word_file_name, cover_image_filename=cover_image_filename)

    # Generate toc_items from chapters_data (assuming chapters_data is always defined)
        toc_items = []
        def generate_toc_recursive(items, current_level_data, id_prefix=""):
            counter = 1
            for item in current_level_data:
                # Create a unique ID (slugify)
                text_slug = item['title'].lower()
                text_slug = unicodedata.normalize('NFKD', text_slug).encode('ascii', 'ignore').decode('ascii') # Remove accents
                text_slug = re.sub(r'[^\w\s-]', '', text_slug).strip() # Remove non-alphanumeric
                text_slug = re.sub(r'[-\s]+', '-', text_slug) # Replace spaces/hyphens with single hyphen
                
                unique_id = f"{id_prefix}{text_slug}-{counter}"
                
                toc_items.append({'level': item['level'], 'text': item['title'], 'id': unique_id, 'style': item['style']})
                item['id'] = unique_id # Add id to chapters_data as well for rendering chapter anchors
                counter +=1
                if item.get('children'):
                    generate_toc_recursive(items, item['children'], id_prefix=f"sub-{counter-1}-") # Pass items list for modification
        
        generate_toc_recursive(toc_items, chapters_data) # toc_items list is modified in place

        # Note: full_text is not explicitly generated here anymore unless needed.
        # The content is now within chapters_data.
        # If a simple full_text is still required for some reason, it would need separate extraction.
        
        # --- Step 1: Render the full HTML content ---
        # Note: request.base_url is crucial for WeasyPrint to find static assets (CSS, images)
        # if they are linked relatively or via url_for in the template.
        rendered_html = render_template('book_template.html',
                                        cover_image_filename=cover_image_filename,
                                        toc_items=toc_items,
                                        chapters_data=chapters_data,
                                        word_file_name=word_file_name,
                                        # Pass base_url for absolute URLs if needed by template, though url_for should handle it
                                        # base_url_for_static=request.url_root + "static/" 
                                        )

        # --- Step 2: Generate PDF and Save HTML ---
        safe_original_filename = "".join(c if c.isalnum() else "_" for c in os.path.splitext(word_file_name)[0])
        pdf_filename = f"{safe_original_filename}.pdf"
        html_filename = f"{safe_original_filename}.html"

        pdf_filepath = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)
        html_filepath = os.path.join(app.config['OUTPUT_FOLDER'], html_filename)

        try:
            # Generate PDF
            # Using request.url_root as base_url to help WeasyPrint find static files
            html_doc = HTML(string=rendered_html, base_url=request.url_root)
            html_doc.write_pdf(pdf_filepath)
            app.logger.info(f"Generated PDF: {pdf_filename}")
            
            # Save the rendered HTML
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
            app.logger.info(f"Saved HTML: {html_filename}")

        except Exception as e:
            app.logger.error(f"Error during PDF/HTML file generation for {word_file_name}: {e}")
            # Pass existing data to results page, but show error for file gen
            return render_template('results.html',
                                   pdf_filename=None, # Indicate PDF failed
                                   html_filename=None, # Indicate HTML failed
                                   error_message=f"Error generating output files: {str(e)}",
                                   word_file_name=word_file_name,
                                   cover_image_filename=cover_image_filename) # Keep cover image if it was processed

        # --- Step 3: Return download links via results.html ---
        return render_template('results.html', 
                               pdf_filename=pdf_filename, 
                               html_filename=html_filename,
                               word_file_name=word_file_name,
                               cover_image_filename=cover_image_filename) # Pass cover image to results if needed for display/context
                               
    # This part of the original logic (elif word_file_name, else) is now handled by earlier checks.
    # If word_file_name is None or empty, it's caught at the beginning.
    # If word_file_path is not valid after attempting to save, it's also caught.
    # This ensures that processing only proceeds if a Word file has been successfully saved.
    # A final fallback, though theoretically unreachable if logic above is sound:
    app.logger.error("Reached an unexpected state in /upload. Word file may not have been processed correctly.")
    return render_template('results.html', error_message="An unknown error occurred. Word file might not have been processed.", word_file_name=word_file_name or "Unknown")


@app.route('/download/<file_type>/<filename>')
def download_file(file_type, filename):
    # Basic security: werkzeug.utils.secure_filename is good for input,
    # but for generated filenames, ensure they don't allow traversal.
    # os.path.basename can also help ensure it's just a filename.
    filename = os.path.basename(filename) # Ensure it's just the filename part
    if ".." in filename or filename.startswith("/"): 
        app.logger.warning(f"Invalid filename access attempt: {filename}")
        return "Invalid filename.", 400

    directory = app.config['OUTPUT_FOLDER']
    app.logger.info(f"Download request for type '{file_type}', filename '{filename}' from directory '{directory}'")

    try:
        return send_from_directory(directory, filename, as_attachment=True)
    except FileNotFoundError:
        app.logger.error(f"File not found for download: {os.path.join(directory, filename)}")
        return f"Error: File '{filename}' not found. It might not have been generated correctly.", 404
    except Exception as e:
        app.logger.error(f"Error during file download of {filename}: {e}")
        return "Error serving file.", 500


if __name__ == '__main__':
    app.run(debug=True)
