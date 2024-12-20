import React from 'react';

interface ColorPickerProps {
  value: string;
  onChange: (color: string) => void;
}

const ColorPicker = ({ value, onChange }: ColorPickerProps) => {
  const colors = ['#000000', '#0EA5E9', '#8B5CF6', '#EC4899', '#EF4444'];

  return (
    <div className="flex items-center gap-4 justify-center" dir="rtl">
      <span className="text-qr-text">لون الباركود:</span>
      <div className="flex gap-2">
        {colors.map((color) => (
          <button
            key={color}
            className={`w-8 h-8 rounded-full border-2 ${
              color === value ? 'border-qr-primary' : 'border-transparent'
            }`}
            style={{ backgroundColor: color }}
            onClick={() => onChange(color)}
          />
        ))}
      </div>
    </div>
  );
};

export default ColorPicker;