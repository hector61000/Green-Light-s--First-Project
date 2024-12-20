import React, { useState } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { Button } from "@/components/ui/button";
import URLInput from './URLInput';
import ColorPicker from './ColorPicker';
import { toast } from 'sonner';

const QRGenerator = () => {
  const [url, setUrl] = useState('');
  const [color, setColor] = useState('#2E7D32');
  const [error, setError] = useState('');

  const validateURL = (value: string) => {
    try {
      new URL(value);
      setError('');
      return true;
    } catch {
      setError('الرجاء إدخال رابط صحيح');
      return false;
    }
  };

  const handleURLChange = (value: string) => {
    setUrl(value);
    if (value) validateURL(value);
  };

  const downloadQR = () => {
    if (!url || !validateURL(url)) return;

    const svg = document.getElementById('qr-code');
    if (!svg) return;

    const svgData = new XMLSerializer().serializeToString(svg);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx?.drawImage(img, 0, 0);
      const pngFile = canvas.toDataURL('image/png');
      
      const downloadLink = document.createElement('a');
      downloadLink.download = 'qr-code.png';
      downloadLink.href = pngFile;
      downloadLink.click();
      
      toast.success('تم تحميل الباركود بنجاح');
    };
    
    img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
  };

  return (
    <div className="w-full max-w-xl mx-auto space-y-8 p-6 bg-white rounded-xl shadow-lg">
      <URLInput value={url} onChange={handleURLChange} error={error} />
      
      <ColorPicker value={color} onChange={setColor} />
      
      <div className="flex justify-center">
        {url && !error && (
          <div className="p-6 bg-[#F2FCE2] rounded-lg shadow-md">
            <QRCodeSVG
              id="qr-code"
              value={url}
              size={200}
              fgColor={color}
              level="H"
              includeMargin
            />
          </div>
        )}
      </div>

      <Button
        onClick={downloadQR}
        disabled={!url || !!error}
        className="w-full bg-[#2E7D32] hover:bg-[#1B5E20] text-white transition-colors"
      >
        تحميل الباركود
      </Button>
    </div>
  );
};

export default QRGenerator;