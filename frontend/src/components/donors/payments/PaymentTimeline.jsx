import {
  CheckCircle2,
  Circle,
} from "lucide-react";

export default function PaymentTimeline({
  data,
}) {
  return (
    <div className="payment-timeline-card">

      <div className="section-header">

        <div>

          <h3>Funding Timeline</h3>

          <p>
            Approval to final
            disbursement milestones
          </p>

        </div>

      </div>

      <div className="timeline-wrapper">

        <div className="timeline-line" />

        {data.map((step, index) => (

          <div
            key={step.title}
            className="timeline-step"
          >

            <div
              className={`timeline-circle ${
                step.completed
                  ? "completed"
                  : "pending"
              }`}
            >

              {step.completed ? (

                <CheckCircle2
                  size={22}
                />

              ) : (

                <Circle
                  size={22}
                />

              )}

            </div>

            <div className="timeline-content">

              <h4>
                {step.title}
              </h4>

              <span className="timeline-date">
                {step.date}
              </span>

              <strong>
                {step.amount}
              </strong>

            </div>

            {index <
              data.length - 1 && (
              <div className="timeline-connector" />
            )}

          </div>

        ))}

      </div>

    </div>
  );
}