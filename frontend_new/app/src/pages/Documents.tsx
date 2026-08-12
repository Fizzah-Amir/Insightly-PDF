import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FileText, UploadCloud } from "lucide-react";
import api from "../api/axios";
import type { Document } from "../types/document";
import DocumentCard from "../components/DocumentCard";

function Documents() {
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

  return (
    <div>
      <div className="mb-8 flex items-end justify-between">
        <div>
          <h1 className="font-display text-3xl font-semibold text-ink">Documents</h1>
          <p className="text-ink-soft mt-2">Manage and chat with your AI-powered documents.</p>
        </div>
        <button
          onClick={() => navigate("/upload")}
          className="hidden sm:flex items-center gap-2 bg-accent hover:bg-accent-hover text-white text-sm font-medium px-4 py-2.5 rounded-xl transition-colors"
        >
          <UploadCloud size={16} />
          Upload
        </button>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-56 rounded-2xl bg-surface border border-line animate-pulse" />
          ))}
        </div>
      ) : documents.length === 0 ? (
        <div className="bg-surface rounded-2xl border border-line p-14 text-center">
          <div className="w-12 h-12 rounded-xl bg-accent-soft text-accent flex items-center justify-center mx-auto mb-4">
            <FileText size={22} />
          </div>
          <h3 className="font-display text-lg font-semibold text-ink">No documents yet</h3>
          <p className="text-ink-soft mt-2 max-w-sm mx-auto">
            Upload a PDF and it'll show up here, ready to chat with and map.
          </p>
          <button
            onClick={() => navigate("/upload")}
            className="mt-5 bg-accent hover:bg-accent-hover text-white text-sm font-medium px-5 py-2.5 rounded-xl transition-colors"
          >
            Upload your first PDF
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {documents.map((doc) => (
            <DocumentCard key={doc.id} document={doc} />
          ))}
        </div>
      )}
    </div>
  );
}

export default Documents;
