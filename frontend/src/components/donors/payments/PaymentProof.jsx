import { useState } from "react";
import {
  ChevronDown,
  ChevronUp,
  Download,
  FileText,
  Upload,
  CheckCircle2,
  Clock3,
  XCircle,
} from "lucide-react";

export default function PaymentProof({
  proofs = [],
}) {
  const [open, setOpen] = useState({});

  const toggle = (id) => {
    setOpen((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  const statusIcon = (status) => {
    switch (status) {
      case "Verified":
        return (
          <CheckCircle2
            size={16}
            color="#16A34A"
          />
        );

      case "Rejected":
        return (
          <XCircle
            size={16}
            color="#DC2626"
          />
        );

      default:
        return (
          <Clock3
            size={16}
            color="#F59E0B"
          />
        );
    }
  };

  return (
    <div className="payment-proof-card">

      <div className="section-header">

        <div>

          <h3>
            Payment Proof & Documents
          </h3>

          <p>
            Supporting documents uploaded
            for every installment
          </p>

        </div>

      </div>

      <div className="proof-list">

        {proofs.map((proof) => (

          <div
            key={proof.paymentId}
            className="proof-card"
          >

            <div
              className="proof-header"
              onClick={() =>
                toggle(proof.paymentId)
              }
            >

              <div>

                <h4>

                  {proof.installment}

                </h4>

                <span>

                  {proof.receivedDate ||
                    "Pending"}

                </span>

              </div>

              <div className="proof-right">

                <strong>

                  ₹
                  {Number(
                    proof.amount
                  ).toLocaleString(
                    "en-IN"
                  )}

                </strong>

                {open[
                  proof.paymentId
                ] ? (
                  <ChevronUp />
                ) : (
                  <ChevronDown />
                )}

              </div>

            </div>

            {open[
              proof.paymentId
            ] && (

              <div className="proof-body">

                <div className="proof-meta">

                  <div>

                    <span>
                      Transaction ID
                    </span>

                    <strong>

                      {proof.utr ||
                        "-"}

                    </strong>

                  </div>

                  <button className="upload-btn">

                    <Upload
                      size={16}
                    />

                    Upload

                  </button>

                </div>

                <table className="proof-table">

                  <thead>

                    <tr>

                      <th>
                        Document
                      </th>

                      <th>
                        Size
                      </th>

                      <th>
                        Status
                      </th>

                      <th>
                        Uploaded By
                      </th>

                      <th>
                        Actions
                      </th>

                    </tr>

                  </thead>

                  <tbody>

                    {proof.documents
                      ?.length ? (

                      proof.documents.map(
                        (
                          doc
                        ) => (

                          <tr
                            key={
                              doc.id
                            }
                          >

                            <td>

                              <div className="doc-name">

                                <FileText
                                  size={
                                    16
                                  }
                                />

                                {
                                  doc.name
                                }

                              </div>

                            </td>

                            <td>

                              {doc.size ||
                                "-"}

                            </td>

                            <td>

                              <div className="doc-status">

                                {statusIcon(
                                  doc.status
                                )}

                                <span>

                                  {
                                    doc.status
                                  }

                                </span>

                              </div>

                            </td>

                            <td>

                              {doc.uploadedBy ||
                                "-"}

                            </td>

                            <td>

                              <button className="table-action">

                                <Download
                                  size={
                                    15
                                  }
                                />

                              </button>

                            </td>

                          </tr>

                        )
                      )

                    ) : (

                      <tr>

                        <td
                          colSpan={5}
                          style={{
                            textAlign:
                              "center",
                            padding:
                              "25px",
                          }}
                        >

                          No documents
                          uploaded

                        </td>

                      </tr>

                    )}

                  </tbody>

                </table>

              </div>

            )}

          </div>

        ))}

      </div>

    </div>
  );
}