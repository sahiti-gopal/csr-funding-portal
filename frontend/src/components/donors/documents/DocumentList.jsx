import { useRef } from "react";
import {
  FileText,
  AlertTriangle,
  Eye,
  Upload,
} from "lucide-react";

export default function DocumentList({
  documents,
  onUpload,
  onReview,
}) {
  const fileInputRef = useRef(null);
  const pendingDocId = useRef(null);

  const triggerUpload = (docId) => {
    pendingDocId.current = docId;
    fileInputRef.current?.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    if (file && pendingDocId.current != null) {
      onUpload?.(pendingDocId.current, file);
    }
    event.target.value = "";
  };

  const criticalMissing = documents.find(
    (doc) => !doc.fileUrl && doc.severity === "Critical"
  );

  return (
    <div className="document-list">

      <input
        ref={fileInputRef}
        type="file"
        style={{ display: "none" }}
        onChange={handleFileChange}
      />

      {documents.map((doc) => {

        const missing = !doc.fileUrl;

        return (
          <div
            key={doc.id}
            className={`document-card ${
              missing
                ? "missing-document"
                : ""
            }`}
          >

            <div className="document-left">

              <div
                className={`document-file-icon ${
                  missing
                    ? "danger"
                    : ""
                }`}
              >
                {missing ? (
                  <AlertTriangle
                    size={16}
                  />
                ) : (
                  <FileText
                    size={16}
                  />
                )}
              </div>

              <div>

                <div className="document-title-row">

                  <h3>{doc.title}</h3>

                  <span
                    className={`severity-pill ${
                      doc.severity.toLowerCase()
                    }`}
                  >
                    {doc.severity}
                  </span>

                </div>

                <p>
                  Due: {doc.due ?? "Required"}

                  {doc.updated &&
                    ` • Updated ${doc.updated}`}

                  {doc.owner &&
                    ` by ${doc.owner}`}
                </p>

              </div>

            </div>

            <div className="document-right">

              <span
                className={`status-pill ${
                  missing
                    ? "missing"
                    : "pending"
                }`}
              >
                ● {doc.status}
              </span>

              {missing ? (

                <button
                  className="doc-upload-btn"
                  onClick={() => triggerUpload(doc.id)}
                >

                  <Upload size={16} />

                  Upload

                </button>

              ) : (

                <button
                  className="review-btn"
                  onClick={() => onReview?.(doc.id)}
                  disabled={doc.status === "Verified"}
                >

                  <Eye size={16} />

                  {doc.status === "Verified" ? "Reviewed" : "Review"}

                </button>

              )}

            </div>

          </div>
        );
      })}

      {criticalMissing && (

        <div className="risk-banner">

          <AlertTriangle
            size={18}
          />

          <span>

            <strong>High risk</strong>

            {` — ${criticalMissing.title} is a mandatory filing. Missing it may delay donor approval.`}

          </span>

        </div>

      )}

    </div>
  );
}
