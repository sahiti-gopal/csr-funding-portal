import { useEffect, useRef, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Bot, MessageSquarePlus, Send, Sparkles, Trash2, User } from "lucide-react";

import {
  createConversation,
  deleteConversation,
  getConversation,
  listConversations,
  sendMessage,
} from "../services/chatService";

import "../styles/chat.css";

const FAQ_QUESTIONS = [
  "Which donors have the highest likelihood?",
  "List active projects by region",
  "Show projects with low fund utilization",
  "Which donor funded the most projects?",
];

function formatRelativeTime(dateString) {
  if (!dateString) return "";
  const date = new Date(dateString);
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
  if (seconds < 60) return "Just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 30) return `${days}d ago`;
  return date.toLocaleDateString();
}

export default function Chat() {
  const queryClient = useQueryClient();
  const [activeId, setActiveId] = useState(null);
  const [input, setInput] = useState("");
  const listRef = useRef(null);

  const { data: conversations = [] } = useQuery({
    queryKey: ["conversations"],
    queryFn: listConversations,
  });

  const { data: activeConversation } = useQuery({
    queryKey: ["conversation", activeId],
    queryFn: () => getConversation(activeId),
    enabled: !!activeId,
    staleTime: 30000,
  });

  const createMutation = useMutation({
    mutationFn: createConversation,
    onSuccess: (conversation) => {
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
      setActiveId(conversation.id);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteConversation,
    onSuccess: (_data, deletedId) => {
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
      if (activeId === deletedId) setActiveId(null);
    },
  });

  const sendMutation = useMutation({
    mutationFn: ({ conversationId, message }) => sendMessage(conversationId, message),
    onSuccess: (_data, { conversationId }) => {
      queryClient.invalidateQueries({ queryKey: ["conversation", conversationId] });
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
    onError: (error, { conversationId }) => {
      const text =
        error?.response?.data?.error ||
        "Something went wrong reaching the AI assistant.";
      queryClient.setQueryData(["conversation", conversationId], (prev) => ({
        ...prev,
        messages: [
          ...(prev?.messages || []),
          { id: `error-${Date.now()}`, role: "assistant", content: text, isError: true },
        ],
      }));
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
  });

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [activeConversation?.messages, sendMutation.isPending]);

  const handleNewChat = () => {
    createMutation.mutate();
  };

  const handleSend = async (text) => {
    const trimmed = (text ?? input).trim();
    if (!trimmed || sendMutation.isPending) return;

    let conversationId = activeId;
    if (!conversationId) {
      const conversation = await createConversation();
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
      setActiveId(conversation.id);
      conversationId = conversation.id;
    }

    setInput("");
    queryClient.setQueryData(["conversation", conversationId], (prev) => ({
      ...prev,
      messages: [
        ...(prev?.messages || []),
        { id: `local-${Date.now()}`, role: "user", content: trimmed },
      ],
    }));
    sendMutation.mutate({ conversationId, message: trimmed });
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const messages = activeConversation?.messages || [];

  return (
    <div className="chat-page">
      <aside className="chat-history-rail">
        <button className="chat-new-btn" onClick={handleNewChat}>
          <MessageSquarePlus size={16} />
          New chat
        </button>

        <div className="chat-history-list">
          {conversations.length === 0 ? (
            <p className="chat-history-empty">No conversations yet.</p>
          ) : (
            conversations.map((conversation) => (
              <div
                key={conversation.id}
                className={`chat-history-item${
                  conversation.id === activeId ? " active" : ""
                }`}
                onClick={() => setActiveId(conversation.id)}
              >
                <div className="chat-history-item-text">
                  <span className="chat-history-title">{conversation.title}</span>
                  <span className="chat-history-time">
                    {formatRelativeTime(conversation.updated_at)}
                  </span>
                </div>
                <button
                  className="chat-history-delete"
                  aria-label="Delete conversation"
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteMutation.mutate(conversation.id);
                  }}
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))
          )}
        </div>
      </aside>

      <section className="chat-main">
        <header className="chat-main-header">
          <span className="chat-main-header-icon">
            <Sparkles size={16} />
          </span>
          <span>AI Assistant</span>
        </header>

        <div className="chat-messages" ref={listRef}>
          {messages.length === 0 ? (
            <div className="chat-empty-state">
              <span className="chat-empty-icon">
                <Sparkles size={26} />
              </span>
              <h4>How can I help?</h4>
              <p>Ask me anything about your projects and donors.</p>
            </div>
          ) : (
            messages.map((m) => (
              <div key={m.id} className={`chat-row chat-row-${m.role}`}>
                <span className={`chat-avatar chat-avatar-${m.role}`}>
                  {m.role === "user" ? <User size={14} /> : <Bot size={14} />}
                </span>
                <div
                  className={`chat-bubble chat-bubble-${m.role}${
                    m.isError ? " chat-bubble-error" : ""
                  }`}
                >
                  {m.content}
                </div>
              </div>
            ))
          )}
          {sendMutation.isPending && (
            <div className="chat-row chat-row-assistant">
              <span className="chat-avatar chat-avatar-assistant">
                <Bot size={14} />
              </span>
              <div className="chat-bubble chat-bubble-assistant chat-bubble-typing">
                <span className="chat-typing-dot" />
                <span className="chat-typing-dot" />
                <span className="chat-typing-dot" />
              </div>
            </div>
          )}
        </div>

        {messages.length === 0 && (
          <div className="chat-faq-row">
            {FAQ_QUESTIONS.map((question) => (
              <button
                key={question}
                className="chat-faq-chip"
                onClick={() => handleSend(question)}
              >
                {question}
              </button>
            ))}
          </div>
        )}

        <div className="chat-input-row">
          <textarea
            className="chat-input"
            placeholder="Ask about your projects, donors…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
          />
          <button
            className="chat-send"
            aria-label="Send message"
            onClick={() => handleSend()}
            disabled={sendMutation.isPending || !input.trim()}
          >
            <Send size={16} />
          </button>
        </div>
      </section>
    </div>
  );
}
