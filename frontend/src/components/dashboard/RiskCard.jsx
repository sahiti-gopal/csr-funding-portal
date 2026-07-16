import { useRef, useState } from "react";
import { createPortal } from "react-dom";
import { ChevronRight, FileText, Paperclip, X } from "lucide-react";

const TONE_LABEL = {
  high: "Critical action required",
  medium: "Action required",
  low: "For your attention",
};

export default function RiskCard({
  icon: Icon,
  title,
  description,
  level,
  timeLeft,
  action,
}) {
  const tone = level.toLowerCase();

  const [open, setOpen] = useState(false);
  const [file, setFile] = useState(null);
  const [uploaded, setUploaded] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const acceptFile = (selected) => {
    if (!selected) return;
    setFile(selected);
    setUploaded(false);
  };

  const handleFileChange = (e) => acceptFile(e.target.files?.[0] ?? null);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    acceptFile(e.dataTransfer.files?.[0] ?? null);
  };

  const handleUpload = () => {
    if (!file) return;
    // No backend endpoint for MOU uploads yet; acknowledge locally.
    setUploaded(true);
  };

  const closePanel = () => setOpen(false);

  return (
    <div className={`risk-card risk-card-${tone}`}>
      <div className="risk-top">
        <span className={`risk-icon risk-icon-${tone}`}>
          {Icon && <Icon size={18} />}
        </span>

        <div className="risk-body">
          <h4>{title}</h4>
          <p>{description}</p>
        </div>

        <div className="risk-meta">
          <span className={`badge ${tone}`}>{level}</span>
          <span className="risk-time-label">Time left</span>
          <span className={`risk-time ${tone}`}>{timeLeft}</span>
        </div>
      </div>

      <button
        className="risk-action"
        onClick={() => setOpen(true)}
      >
        <span>{action}</span>
        <ChevronRight size={14} />
      </button>

      {open &&
        createPortal(
          <div className="risk-modal-overlay" onClick={closePanel}>
            <div
              className={`risk-modal risk-modal-${tone}`}
              role="dialog"
              aria-modal="true"
              aria-labelledby="risk-modal-title"
              onClick={(e) => e.stopPropagation()}
            >
              <button
                type="button"
                className="risk-modal-close"
                onClick={closePanel}
                aria-label="Close"
              >
                <X size={16} />
              </button>

              <div className="risk-modal-header">
                <span className={`risk-modal-eyebrow risk-modal-eyebrow-${tone}`}>
                  {TONE_LABEL[tone] ?? "Action required"}
                </span>
                <h3 id="risk-modal-title">{title}</h3>
              </div>

              <div className="risk-modal-stats">
                <div className="risk-modal-stat">
                  <span className="risk-modal-stat-label">Severity</span>
                  <span className={`badge ${tone}`}>{level}</span>
                </div>
                <div className="risk-modal-stat-divider" />
                <div className="risk-modal-stat">
                  <span className="risk-modal-stat-label">Time left</span>
                  <span className={`risk-modal-stat-value ${tone}`}>
                    {timeLeft}
                  </span>
                </div>
              </div>

              <p className="risk-modal-description">{description}</p>

              <div className="risk-modal-divider" />

              <div className="risk-modal-upload-label">
                <FileText size={14} />
                <span>Supporting document</span>
              </div>

              <div
                className={`risk-dropzone ${dragOver ? "risk-dropzone-active" : ""} ${
                  file ? "risk-dropzone-filled" : ""
                }`}
                onClick={() => fileInputRef.current?.click()}
                onDragOver={(e) => {
                  e.preventDefault();
                  setDragOver(true);
                }}
                onDragLeave={() => setDragOver(false)}
                onDrop={handleDrop}
              >
                {!file && (
                  <>
                    <span className="risk-dropzone-icon">
                      <Paperclip size={18} />
                    </span>
                    <span className="risk-dropzone-title">
                      Drop your file here, or click to browse
                    </span>
                    <span className="risk-dropzone-hint">PDF, DOC or DOCX up to 10 MB</span>
                  </>
                )}

                {file && (
                  <div className="risk-dropzone-file">
                    <span className="risk-dropzone-file-icon">
                      <FileText size={16} />
                    </span>
                    <div className="risk-dropzone-file-info">
                      <span className="risk-dropzone-filename">{file.name}</span>
                      <span className="risk-dropzone-filesize">
                        {(file.size / 1024).toFixed(0)} KB
                      </span>
                    </div>
                    <button
                      type="button"
                      className="risk-dropzone-remove"
                      onClick={(e) => {
                        e.stopPropagation();
                        setFile(null);
                        setUploaded(false);
                      }}
                      aria-label="Remove selected file"
                    >
                      <X size={14} />
                    </button>
                  </div>
                )}
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.doc,.docx"
                className="risk-upload-input"
                onChange={handleFileChange}
              />

              <div className="risk-modal-actions">
                <button type="button" className="risk-modal-cancel" onClick={closePanel}>
                  Cancel
                </button>
                <button
                  type="button"
                  className={`risk-modal-submit risk-modal-submit-${tone}`}
                  disabled={!file}
                  onClick={handleUpload}
                >
                  {uploaded ? "Uploaded ✓" : "Upload document"}
                </button>
              </div>
            </div>
          </div>,
          document.body
        )}
    </div>
  );
}
