import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FileText, CheckCircle2, Share2, Clock, ArrowRight } from "lucide-react";
import api from "../api/axios";
import type { Document } from "../types/document";
import StatsCard from "../components/StatsCard";

function timeAgo(dateStr: string) {
  const diffMs = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diffMs / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  return `${days}d ago`;
}

function Dashboard() {
  const navigate = useNavigate();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("")
      .then((response) => setDocuments(response.data))
      .catch((error) => console.log(error))
      .finally(() => setLoading(false));
  }, []);

  const stats = useMemo(() => {
    const ready = documents.filter((d) => d.status?.toUpperCase() === "READY").length;
    const mapped = documents.filter((d) => (d.mindmap_status ?? "NOT_STARTED").toUpperCase() !== "NOT_STARTED").length;
    return { total: documents.length, ready, mapped };
  }, [documents]);

  const recent = useMemo(
    () =>
      [...documents]
        .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        .slice(0, 5),
    [documents]
  );

  return (
    <div>
      <div className="mb-9">
        <h1 className="font-display text-3xl font-semibold text-ink">Welcome back</h1>
        <p className="text-ink-soft mt-2">Here's what's happening across your documents.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <StatsCard title="Total documents" value={loading ? "—" : stats.total} icon={FileText} accent="accent" />
        <StatsCard title="Ready to query" value={loading ? "—" : stats.ready} icon={CheckCircle2} accent="link" />
        <StatsCard title="Mind maps generated" value={loading ? "—" : stats.mapped} icon={Share2} accent="warn" />
      </div>

      <div className="mt-8 grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2 bg-surface rounded-2xl border border-line p-6">
          <div className="flex justify-between items-center mb-5">
            <h2 className="font-display text-lg font-semibold text-ink">Recent documents</h2>
            <button
              onClick={() => navigate("/documents")}
              className="text-accent text-sm font-medium flex items-center gap-1 hover:gap-1.5 transition-all"
            >
              View all <ArrowRight size={14} />
            </button>
          </div>

          {loading ? (
            <p className="text-ink-soft text-sm py-8 text-center">Loading documents…</p>
          ) : recent.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-ink-soft">No documents yet.</p>
              <button
                onClick={() => navigate("/upload")}
                className="mt-3 text-accent text-sm font-medium"
              >
                Upload your first PDF →
              </button>
            </div>
          ) : (
            <div className="space-y-2.5">
              {recent.map((doc) => {
                 const ready = doc.status?.toUpperCase() === "READY";
                return (
                  <button
                    key={doc.id}
                    onClick={() => navigate(`/chat/${doc.id}`)}
                    className="w-full flex items-center justify-between p-4 rounded-xl bg-paper hover:bg-paper-dim transition-colors text-left"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <FileText size={18} className="text-ink-faint shrink-0" />
                      <div className="min-w-0">
                        <p className="font-medium text-ink truncate">{doc.title}</p>
                        <p className="text-xs text-ink-soft mt-0.5 flex items-center gap-1">
                          <Clock size={11} /> {timeAgo(doc.created_at)}
                        </p>
                      </div>
                    </div>
                    <span
                      className={`shrink-0 ml-3 px-2.5 py-1 rounded-full text-xs font-mono uppercase ${
                        ready ? "bg-link-soft text-link" : "bg-warn-soft text-warn"
                      }`}
                    >
                      {doc.status}
                    </span>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        <div className="bg-spine rounded-2xl p-6 text-white flex flex-col">
          <h2 className="font-display text-lg font-semibold mb-3">AI Assistant</h2>
          <p className="text-spine-text-dim leading-relaxed text-sm flex-1">
            Upload a PDF, ask it questions in plain language, and see how its ideas connect as a mind map.
          </p>
          <button
            onClick={() => navigate("/upload")}
            className="mt-6 bg-accent hover:bg-accent-hover text-white px-5 py-3 rounded-xl font-medium text-sm transition-colors"
          >
            Upload a document
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
