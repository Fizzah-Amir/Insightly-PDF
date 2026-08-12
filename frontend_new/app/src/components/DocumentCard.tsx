import { FileText, MessageCircle, Share2, Trash2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import type { Document } from "../types/document";

interface Props {
  document: Document;
}

function statusTone(status: string) {
  const s = status.toUpperCase();
  if (s === "READY") return { dot: "text-link bg-link", label: "text-link" };
  if (s === "FAILED" || s === "ERROR") return { dot: "text-danger bg-danger", label: "text-danger" };
  return { dot: "text-warn bg-warn", label: "text-warn" };
}

function DocumentCard({ document }: Props) {
  const navigate = useNavigate();
  const tone = statusTone(document.status);

  return (
    <div className="group bg-surface border border-line rounded-2xl p-6 hover:border-ink-faint hover:shadow-[0_1px_0_0_rgba(0,0,0,0.02)] transition-colors duration-200">
      <div className="flex justify-between items-start">
        <div className="w-11 h-11 rounded-xl bg-accent-soft text-accent flex items-center justify-center">
          <FileText size={22} strokeWidth={2} />
        </div>
        <button
          aria-label="Delete document"
          className="text-ink-faint hover:text-danger transition-colors opacity-0 group-hover:opacity-100"
        >
          <Trash2 size={17} />
        </button>
      </div>

      <h2 className="font-display text-lg font-semibold text-ink mt-5 truncate" title={document.title}>
        {document.title}
      </h2>

      <p className="text-xs font-mono text-ink-faint mt-2">
        {new Date(document.created_at).toLocaleDateString(undefined, {
          year: "numeric",
          month: "short",
          day: "numeric",
        })}
      </p>

      <div className="flex items-center gap-1.5 mt-4">
        <span className={`relative status-dot ${tone.dot}`} />
        <span className={`text-xs font-mono uppercase tracking-wide ${tone.label}`}>
          {document.status}
        </span>
      </div>

      <div className="flex gap-2.5 mt-6">
        <button
          onClick={() => navigate(`/chat/${document.id}`)}
          className="flex-1 flex items-center justify-center gap-2 bg-accent hover:bg-accent-hover text-white text-sm font-medium py-2.5 rounded-xl transition-colors"
        >
          <MessageCircle size={16} />
          Chat
        </button>
        <button
          onClick={() => navigate(`/mindmap/${document.id}`)}
          className="flex-1 flex items-center justify-center gap-2 border border-line hover:bg-paper-dim text-ink text-sm font-medium py-2.5 rounded-xl transition-colors"
        >
          <Share2 size={16} />
          Mind map
        </button>
      </div>
    </div>
  );
}

export default DocumentCard;
