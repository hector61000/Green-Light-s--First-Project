# DOCX to PDF/HTML Converter

This Flask application converts uploaded DOCX (Microsoft Word) files into styled PDF and HTML documents. It also allows for an optional cover image to be included in the generated output.

The application extracts headings (H1, H2, H3) to generate a table of contents and attempts to extract inline images from the DOCX file to include in the output.

## Features

-   Upload DOCX files.
-   Upload an optional cover image (JPG, PNG).
-   Extracts H1, H2, H3 headings for a Table of Contents.
-   Attempts to extract inline images from the DOCX content.
-   Generates a PDF file with the cover image, TOC, and structured content.
-   Generates an HTML file with the same content and structure.
-   Uses WeasyPrint for PDF generation, allowing for CSS styling.
-   Uses Tailwind CSS for styling the HTML preview and base for PDF.
-   Arabic language support (RTL text direction, Arabic font for text).

## Project Structure

```
docx_to_pdf_converter/
├── app.py                  # Main Flask application
├── doc_processor.py        # Handles DOCX parsing and content extraction
├── requirements.txt        # Python dependencies
├── static/                 # Static files (CSS, JS, uploaded images)
│   └── uploads/            # Stores uploaded cover images and content images
├── templates/              # HTML templates for Flask
│   ├── index.html          # Main upload page
│   ├── book_template.html  # Template for generating the HTML version of the book (used for PDF and HTML output)
│   └── results.html        # Page to display download links for generated files
├── uploads/                # Temporary storage for uploaded DOCX files
└── output/                 # Storage for generated PDF and HTML files
└── README.md               # This file
```

## Installation

1.  **Clone the repository (or download the files).**
2.  **Navigate to the project directory:**
    ```bash
    cd path/to/docx_to_pdf_converter
    ```
3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    Note: WeasyPrint has external dependencies (like Pango, Cairo, GDK-PixBuf) that might need to be installed separately depending on your OS. Please refer to the [WeasyPrint documentation](https://doc.weasyprint.org/stable/first_steps.html#installation) for OS-specific instructions.

## How to Run

1.  **Ensure all dependencies are installed.**
2.  **Run the Flask application:**
    ```bash
    flask run
    ```
    Alternatively, you can run:
    ```bash
    python app.py
    ```
3.  **Open your web browser and go to:** `http://127.0.0.1:5000/` (or the address shown in your terminal).

## Usage

1.  On the main page, use the form to select a `.docx` file.
2.  Optionally, select a cover image (`.jpg`, `.jpeg`, `.png`).
3.  Click "Upload".
4.  The application will process the file and redirect you to a results page.
5.  On the results page, you will find download links for the generated PDF and HTML files.
6.  If any errors occur during processing, an error message will be displayed.

## Key Libraries Used

-   **Flask**: Web framework.
-   **python-docx**: For reading and parsing DOCX files.
-   **WeasyPrint**: For generating PDF documents from HTML/CSS.
-   **BeautifulSoup4**: (Included in requirements, though direct usage might have been superseded by internal parsing logic or was for an earlier iteration - good to keep if there's any residual utility or for future HTML parsing tasks).
-   **Tailwind CSS**: For UI styling (via CDN in templates).
-   **Google Fonts (Cairo)**: For Arabic text rendering.

---
This project provides a foundation for DOCX to structured HTML/PDF conversion. Further enhancements could include more sophisticated image placement, handling of various DOCX elements (tables, lists, footnotes), and more customizable styling options.
