import { Button } from "@/components/ui/button";
import { MessageSquare } from "lucide-react"; // Using a generic message icon for now

const WhatsAppButton = () => {
  const phoneNumber = "201117552174";
  const whatsappLink = `https://wa.me/${phoneNumber}`;

  return (
    <a
      href={whatsappLink}
      target="_blank"
      rel="noopener noreferrer"
      className="fixed bottom-6 right-6 z-50"
    >
      <Button
        size="icon"
        className="rounded-full bg-green-500 hover:bg-green-600 text-white w-14 h-14"
      >
        <MessageSquare className="h-7 w-7" />
        <span className="sr-only">Contact us on WhatsApp</span>
      </Button>
    </a>
  );
};

export default WhatsAppButton;
