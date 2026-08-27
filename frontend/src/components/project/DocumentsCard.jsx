import { useState } from "react";
import { createPortal } from "react-dom";
import { FileText, FileSpreadsheet, Download, X } from "lucide-react";

import Collapsible from "./Collapsible";
import { resolveApiFileUrl } from "../../api/axios";

const isPdf = (name = "") => name.toLowerCase().endsWith(".pdf");

function DocumentPreviewModal({ document: doc, onClose }) {
  const fileUrl = resolveApiFileUrl(doc.url);

  return createPortal(
    <div className="document-preview-overlay" onClick={onClose}>
      <div
        className="document-preview-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="document-preview-title"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="document-preview-header">
          <h3 id="document-preview-title">{doc.name}</h3>
          <button
            type="button"
            className="document-preview-close"
            onClick={onClose}
            aria-label="Close preview"
          >
            <X size={16} />
          </button>
        </div>

        {fileUrl && isPdf(doc.name) ? (
          <iframe
            src={fileUrl}
            title={doc.name}
            className="document-preview-frame"
          />
        ) : (
          <div className="document-preview-fallback">
            {isPdf(doc.name) ? <FileText size={32} /> : <FileSpreadsheet size={32} />}
            <p>
              {fileUrl
                ? "This file type can't be previewed inline — download it to view."
                : "No file is available for this document."}
            </p>
            {fileUrl && (
              <a
                className="document-preview-download"
                href={fileUrl}
                download={doc.name}
              >
                <Download size={14} />
                Download
              </a>
            )}
          </div>
        )}
      </div>
    </div>,
    window.document.body
  );
}

export default function DocumentsCard({ documents = [] }) {
  const [previewDoc, setPreviewDoc] = useState(null);

  return (
    <Collapsible title="Recent Files" wrapperClassName="card">
      {documents.length === 0 ? (
        <p className="pd-empty-note">
          No files uploaded yet.
        </p>
      ) : (
        <ul className="recent-files">
          {documents.slice(0,3).map((doc)=>(
            <li key={doc.name} className="recent-file">

              <button
                type="button"
                className="recent-file-btn"
                onClick={() => setPreviewDoc(doc)}
              >
                {isPdf(doc.name) ? <FileText size={18}/> : <FileSpreadsheet size={18} />}

                <span>{doc.name}</span>
              </button>

            </li>
          ))}
        </ul>
      )}

      {documents.length>3 && (
        <a href="#" className="view-files">
          View {documents.length-3} more files →
        </a>
      )}

      {previewDoc && (
        <DocumentPreviewModal
          document={previewDoc}
          onClose={() => setPreviewDoc(null)}
        />
      )}
    </Collapsible>
  );
}
