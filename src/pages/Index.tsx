import QRGenerator from "@/components/QRGenerator";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-qr-secondary py-12">
      <div className="container">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-qr-text mb-4">مولد الباركود</h1>
          <p className="text-gray-600">قم بإنشاء باركود خاص بك في ثوانٍ معدودة</p>
        </div>
        <QRGenerator />
      </div>
    </div>
  );
};

export default Index;