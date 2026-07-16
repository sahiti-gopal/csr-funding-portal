import {
  FileText,
  Eye,
  Download,
  Upload,
  BadgeCheck,
  CircleAlert,
} from "lucide-react";

export default function PaymentDocumentRow({
  document,
}) {
  const verified =
    document.status === "Verified";

  return (
    <div className="payment-document">

      <div className="payment-document-left">

        <div className="payment-pdf">

          <FileText size={22}/>

        </div>

        <div>

          <h4>
            {document.name}
          </h4>

          <div className="payment-document-meta">

            <span>
              PDF
            </span>

            <span>
              {document.size}
            </span>

            {verified ? (

              <span className="verified">

                <BadgeCheck size={14}/>

                Verified

              </span>

            ) : (

              <span className="pending">

                <CircleAlert size={14}/>

                Pending

              </span>

            )}

          </div>

        </div>

      </div>

      <div className="payment-actions">

        <button className="view-btn">

          <Eye size={16}/>

          View

        </button>

        {verified ? (

          <button className="download-btn">

            <Download size={16}/>

            Download

          </button>

        ) : (

          <button className="replace-btn">

            <Upload size={16}/>

            Replace

          </button>

        )}

      </div>

    </div>
  );
}