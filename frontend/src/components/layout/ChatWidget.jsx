import { useState, useRef, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Bot, Send, X } from "lucide-react";
import { useMutation } from "@tanstack/react-query";

import { sendChatMessage } from "../../services/chatService";

const PAGE_LABELS = {
  "/": "Dashboard",
  "/projects": "Projects",
  "/alerts": "Alerts",
  "/donors": "Donors",
  "/reports": "Reports",
  "/analytics": "Analytics",
  "/settings": "Settings",
};

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hi! Ask me anything about your projects, donors, alerts, or risks.",
    },
  ]);
  const location = useLocation();
  const listRef = useRef(null);

  const mutation = useMutation({
    mutationFn: (message) => sendChatMessage(message, location.pathname),
    onSuccess: (data) => {
      setMessages((prev) => [...prev, { role: "assistant", text: data.reply }]);
    },
    onError: (error) => {
      const text =
        error?.response?.data?.error ||
        "Something went wrong reaching the AI assistant.";
      setMessages((prev) => [...prev, { role: "assistant", text, isError: true }]);
    },
  });

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [messages, mutation.isPending]);

  const handleSend = () => {
    const trimmed = input.trim();
    if (!trimmed || mutation.isPending) return;

    setMessages((prev) => [...prev, { role: "user", text: trimmed }]);
    setInput("");
    mutation.mutate(trimmed);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const pageLabel = PAGE_LABELS[location.pathname] || "this page";

  return (
    <>
      <button
        className="ai-fab"
        aria-label={open ? "Close AI assistant" : "Open AI assistant"}
        onClick={() => setOpen((v) => !v)}
      >
        {open ? <X size={22} /> : <Bot size={22} />}
      </button>

      {open && (
        <div className="ai-chat-panel">
          <div className="ai-chat-header">
            <div className="ai-chat-header-title">
              <Bot size={18} />
              <span>AI Assistant</span>
            </div>
            <span className="ai-chat-header-page">Viewing: {pageLabel}</span>
          </div>

          <div className="ai-chat-messages" ref={listRef}>
            {messages.map((m, i) => (
              <div
                key={i}
                className={`ai-chat-bubble ai-chat-bubble-${m.role}${
                  m.isError ? " ai-chat-bubble-error" : ""
                }`}
              >
                {m.text}
              </div>
            ))}
            {mutation.isPending && (
              <div className="ai-chat-bubble ai-chat-bubble-assistant ai-chat-bubble-typing">
                Thinking…
              </div>
            )}
          </div>

          <div className="ai-chat-input-row">
            <textarea
              className="ai-chat-input"
              placeholder="Ask about your projects, donors, alerts…"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
            />
            <button
              className="ai-chat-send"
              aria-label="Send message"
              onClick={handleSend}
              disabled={mutation.isPending || !input.trim()}
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      )}
    </>
  );
}
