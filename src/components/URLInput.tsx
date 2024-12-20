import React from 'react';
import { Input } from "@/components/ui/input";

interface URLInputProps {
  value: string;
  onChange: (value: string) => void;
  error?: string;
}

const URLInput = ({ value, onChange, error }: URLInputProps) => {
  return (
    <div className="w-full space-y-2">
      <Input
        type="url"
        placeholder="أدخل الرابط هنا..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full p-4 text-lg border rounded-lg focus:ring-2 focus:ring-qr-primary"
        dir="rtl"
      />
      {error && <p className="text-red-500 text-sm">{error}</p>}
    </div>
  );
};

export default URLInput;