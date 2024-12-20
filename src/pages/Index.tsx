import QRGenerator from "@/components/QRGenerator";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-[#F2FCE2] to-[#E2FFD3] relative">
      <div className="container">
        <div className="text-center py-8">
          <h1 className="text-2xl md:text-3xl font-bold text-[#2E7D32] mb-2">
            شركة جرين لايت لتكنولوجيا والتطوير
          </h1>
          <div className="text-center mb-12">
            <h2 className="text-xl md:text-2xl font-bold text-[#388E3C] mb-4">مولد الباركود</h2>
            <p className="text-[#4CAF50]">قم بإنشاء باركود خاص بك في ثوانٍ معدودة</p>
          </div>
        </div>
        <QRGenerator />
      </div>
      
      {/* Footer Section */}
      <div className="absolute bottom-0 left-0 right-0 p-4 bg-[#F2FCE2] border-t border-[#2E7D32]/20">
        <div className="container mx-auto flex justify-between items-center text-[#2E7D32]">
          <div className="text-sm">
            Gm.محمد مصطفي
          </div>
          <div className="text-sm">
            جميع الحقوق محفوظة &copy; {new Date().getFullYear()} Green Light
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;