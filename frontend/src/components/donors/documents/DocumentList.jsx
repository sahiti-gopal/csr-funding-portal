import {
  FileText,
  AlertTriangle,
  Eye,
  Upload,
} from "lucide-react";

export default function DocumentList({
  documents,
}) {
  return (
    <div className="document-list">

      {documents.map((doc) => {

        const missing =
          doc.status === "Missing";

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
                    size={20}
                  />
                ) : (
                  <FileText
                    size={20}
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
                  Due: {doc.due}

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

                <button className="upload-btn">

                  <Upload size={16} />

                  Upload

                </button>

              ) : (

                <button className="review-btn">

                  <Eye size={16} />

                  Review

                </button>

              )}

            </div>

          </div>
        );
      })}

      <div className="risk-banner">

        <AlertTriangle
          size={18}
        />

        <span>

          <strong>High risk</strong>

          {" — CSR-1 registration is a mandatory filing. Missing it may delay donor approval."}

        </span>

      </div>

    </div>
  );
}