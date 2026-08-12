import { useState, useRef } from "react";
import type { DragEvent } from "react";
import { UploadCloud, FileText, CheckCircle2, X, AlertCircle } from "lucide-react";
import api from "../api/axios";

function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      setStatus("idle");
      await api.post("upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus("success");
      setFile(null);
    } catch (error) {
      console.log(error);
      setStatus("error");
    } finally {
      setUploading(false);
    }
  };

  const handleDrag = (e: DragEvent<HTMLDivElement>, active: boolean) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(active);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped) setFile(dropped);
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="font-display text-3xl font-semibold text-ink">Upload a document</h1>
        <p className="text-ink-soft mt-2">Drop in a PDF and the assistant will read it end to end.</p>
      </div>

      <div className="max-w-2xl bg-surface border border-line rounded-2xl p-8">
        <div
          onDragEnter={(e) => handleDrag(e, true)}
          onDragOver={(e) => handleDrag(e, true)}
          onDragLeave={(e) => handleDrag(e, false)}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-colors ${
            dragActive ? "border-accent bg-accent-soft" : "border-line hover:border-ink-faint"
          }`}
        >
          <UploadCloud
            size={44}
            className={`mx-auto mb-4 transition-colors ${dragActive ? "text-accent" : "text-ink-faint"}`}
          />
          <h2 className="text-lg font-medium text-ink">
            {dragActive ? "Drop it here" : "Drag a PDF here, or click to browse"}
          </h2>
          <p className="text-ink-soft text-sm mt-2">Supported format: PDF</p>

          <input
            ref={inputRef}
            type="file"
            accept="application/pdf"
            className="hidden"
            onChange={(e) => {
              if (e.target.files) setFile(e.target.files[0]);
            }}
          />

          {file && (
            <div
              className="mt-6 inline-flex items-center gap-2 text-ink bg-paper px-4 py-2 rounded-lg text-sm"
              onClick={(e) => e.stopPropagation()}
            >
              <FileText size={16} className="text-accent" />
              {file.name}
              <button
                onClick={() => setFile(null)}
                aria-label="Remove file"
                className="text-ink-faint hover:text-danger ml-1"
              >
                <X size={14} />
              </button>
            </div>
          )}
        </div>

        <button
          disabled={!file || uploading}
          onClick={handleUpload}
          className="mt-6 w-full bg-accent hover:bg-accent-hover disabled:bg-ink-faint text-white py-3 rounded-xl font-medium transition-colors"
        >
          {uploading ? "Processing…" : "Upload & analyze"}
        </button>

        {status === "success" && (
          <div className="mt-5 flex items-center gap-2 bg-link-soft text-link p-4 rounded-xl text-sm">
            <CheckCircle2 size={18} />
            Document uploaded. It'll be ready to chat with shortly.
          </div>
        )}
        {status === "error" && (
          <div className="mt-5 flex items-center gap-2 bg-danger-soft text-danger p-4 rounded-xl text-sm">
            <AlertCircle size={18} />
            Upload failed. Check your connection and try again.
          </div>
        )}
      </div>
    </div>
  );
}

export default Upload;
