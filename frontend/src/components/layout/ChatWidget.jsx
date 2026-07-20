import { useNavigate, useLocation } from "react-router-dom";
import { Bot } from "lucide-react";

export default function ChatWidget() {
  const navigate = useNavigate();
  const location = useLocation();

  if (location.pathname === "/chat") return null;

  return (
    <button
      className="ai-fab"
      aria-label="Open AI assistant"
      onClick={() => navigate("/chat")}
    >
      <Bot size={22} />
    </button>
  );
}
