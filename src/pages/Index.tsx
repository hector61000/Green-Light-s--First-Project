import WhatsAppButton from "@/components/WhatsAppButton";

const Index = () => {
  return (
    <div dir="rtl" className="flex flex-col min-h-screen bg-brand-secondary font-sans text-brand-text">
      <WhatsAppButton />
      {/* Header */}
      <header className="py-10 bg-white border-b border-gray-200">
        <div className="container mx-auto text-center px-4">
          <h1 className="text-5xl md:text-6xl font-serif font-bold tracking-tight text-brand-text">
            ابو البنات
          </h1>
          <p className="mt-3 text-lg text-gray-500">
            أسعار مميزة، جودة عالية
          </p>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-grow container mx-auto py-16 text-center px-4">
        <div className="text-center">
          <h2 className="text-3xl font-semibold text-gray-800 font-serif">المنتجات ستضاف قريباً</h2>
          <p className="mt-4 text-gray-600 max-w-xl mx-auto">
            نحن نعمل حالياً على تجهيز تشكيلة فريدة من الملابس والإكسسوارات. تابعونا لمعرفة كل جديد!
          </p>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200">
        <div className="container mx-auto py-6 text-center text-sm text-gray-500 px-4">
          <p>&copy; {new Date().getFullYear()} ابو البنات. جميع الحقوق محفوظة.</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;