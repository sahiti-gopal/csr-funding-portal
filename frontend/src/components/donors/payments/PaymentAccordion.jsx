import { useState } from "react";

import {
  ChevronDown,
  ChevronUp,
  Landmark,
  CalendarDays,
} from "lucide-react";

import PaymentDocumentRow from "./PaymentDocumentRow";

export default function PaymentAccordion({
  proof,
}) {
  const [open, setOpen] = useState(
    proof.id === 1
  );

  return (
    <div className="proof-card">

      <div
        className="proof-header"
        onClick={() => setOpen(!open)}
      >

        <div>

          <h3>{proof.title}</h3>

          <div className="proof-meta">

            <span>

              <Landmark size={15} />

              {proof.amount}

            </span>

            <span>

              <CalendarDays size={15} />

              {proof.received}

            </span>

          </div>

        </div>

        <button className="proof-toggle">

          {open ? (
            <ChevronUp size={20}/>
          ) : (
            <ChevronDown size={20}/>
          )}

        </button>

      </div>

      {open && (

        <>

          <div className="utr-box">

            <span>
              UTR Number
            </span>

            <strong>
              {proof.utr}
            </strong>

          </div>

          <div className="documents-list">

            {proof.documents.map(
              (doc, index) => (

                <PaymentDocumentRow
                  key={index}
                  document={doc}
                />

              )
            )}

          </div>

        </>

      )}

    </div>
  );
}