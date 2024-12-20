import QRGenerator from "@/components/QRGenerator";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-[#F6F6F7] to-[#E6E9F0]">
      <div className="container">
        <div className="text-center py-8">
          <h1 className="text-2xl md:text-3xl font-bold text-[#1A1F2C] mb-2">
            شركة جرين لايت لتكنولوجيا والتطوير
          </h1>
          <div className="text-center mb-12">
            <h2 className="text-xl md:text-2xl font-bold text-[#403E43] mb-4">مولد الباركود</h2>
            <p className="text-[#8E9196]">قم بإنشاء باركود خاص بك في ثوانٍ معدودة</p>
          </div>
        </div>
        <QRGenerator />
      </div>
    </div>
  );
};

export default Index;