import { FileText } from "lucide-react";
import type { Message } from "../types/chat";

interface Props {
  message: Message;
}

function ChatMessage({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-spine flex items-center justify-center shrink-0 mt-1">
          <svg width="14" height="14" viewBox="0 0 48 48" fill="none">
            <line x1="15" y1="31" x2="33" y2="17" stroke="#4338ca" strokeWidth="4" strokeLinecap="round" />
            <circle cx="15" cy="31" r="8" fill="#4338ca" />
            <circle cx="33" cy="17" r="5" fill="#0e8e82" />
          </svg>
        </div>
      )}

      <div
        className={`max-w-2xl rounded-2xl px-5 py-3.5 ${
          isUser
            ? "bg-accent text-white rounded-tr-sm"
            : "bg-surface border border-line text-ink rounded-tl-sm"
        }`}
      >
        <p className="whitespace-pre-wrap leading-relaxed text-[15px]">{message.content}</p>

        {message.citations && message.citations.length > 0 && (
          <div className="mt-3.5 pt-3 border-t border-line/70 flex flex-wrap gap-2">
            {message.citations.map((citation, index) => (
              <span
                key={index}
                className="inline-flex items-center gap-1.5 text-xs font-mono text-ink-soft bg-paper-dim px-2 py-1 rounded-md"
              >
                <FileText size={12} />
                p. {citation.page + 1}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatMessage;
