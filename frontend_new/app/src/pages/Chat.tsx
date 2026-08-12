import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import { Send } from "lucide-react";
import api from "../api/axios";
import type { Message } from "../types/chat";
import ChatMessage from "../components/ChatMessage";

function Chat() {
  const { id } = useParams();
  const [conversation, setConversation] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    initializeChat();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const initializeChat = async () => {
    try {
      const start = await api.post("chat/start/", { document_id: id });
      setConversation(start.data.conversation_id);

      const history = await api.get(`chat/history/${id}/`);
      if (history.data.length > 0) {
        setMessages(history.data[0].messages || []);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || !conversation) return;

    const question = input;
    setInput("");

    setMessages((prev) => [
      ...prev,
      { id: Date.now(), role: "user", content: question },
    ]);

    try {
      setLoading(true);
      const response = await api.post("chat/message/", {
        conversation_id: conversation,
        question,
      });

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: "assistant",
          content: response.data.answer,
          citations: response.data.sources,
        },
      ]);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-72px-72px)]">
      {messages.length === 0 && !loading ? (
        <div className="flex-1 flex flex-col items-center justify-center text-center px-6">
          <div className="w-12 h-12 rounded-full bg-spine flex items-center justify-center mb-5">
            <svg width="20" height="20" viewBox="0 0 48 48" fill="none">
              <line x1="15" y1="31" x2="33" y2="17" stroke="#4338ca" strokeWidth="4" strokeLinecap="round" />
              <circle cx="15" cy="31" r="8" fill="#4338ca" />
              <circle cx="33" cy="17" r="5" fill="#0e8e82" />
            </svg>
          </div>
          <h3 className="font-display text-xl font-semibold text-ink">Ask this document anything</h3>
          <p className="text-ink-soft mt-2 max-w-sm">
            Answers are grounded in the PDF's own pages, with the source page cited next to each one.
          </p>
        </div>
      ) : (
        <div className="flex-1 overflow-y-auto space-y-5 pr-2">
          {messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-ink-soft text-sm pl-11">
              <span className="flex gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-ink-faint animate-bounce [animation-delay:-0.3s]" />
                <span className="w-1.5 h-1.5 rounded-full bg-ink-faint animate-bounce [animation-delay:-0.15s]" />
                <span className="w-1.5 h-1.5 rounded-full bg-ink-faint animate-bounce" />
              </span>
              reading the document
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      )}

      <div className="mt-5 bg-surface border border-line rounded-2xl p-2.5 flex gap-2.5">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
          placeholder="Ask anything about your document…"
          className="flex-1 outline-none px-3.5 bg-transparent text-[15px] placeholder:text-ink-faint"
        />
        <button
          onClick={sendMessage}
          disabled={!input.trim()}
          className="bg-accent hover:bg-accent-hover disabled:bg-ink-faint text-white px-4 rounded-xl transition-colors"
          aria-label="Send message"
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}

export default Chat;
