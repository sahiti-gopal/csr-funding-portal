import {
  HeartHandshake,
  Calendar,
  ArrowUpRight,
} from "lucide-react";

export default function DonorCard({
  donor,
  category,
  likelihood,
  lastContact,
  color = "#2563EB",
}) {
  return (
    <div className="donor-card">

      <div className="donor-left">

        <div
          className="donor-avatar"
          style={{
            background: `${color}15`,
            color,
          }}
        >
          <HeartHandshake size={22} />
        </div>

        <div className="donor-details">

          <div className="donor-name">
            {donor}
          </div>

          <div className="donor-category">
            {category}
          </div>

          <div className="donor-progress">

            <div className="progress-track">

              <div
                className="progress-fill"
                style={{
                  width: `${likelihood}%`,
                  background: color,
                }}
              />

            </div>

          </div>

        </div>

      </div>

      <div className="donor-right">

        <div
          className="likelihood-pill"
          style={{
            color,
            background: `${color}15`,
          }}
        >
          {likelihood}% Match
        </div>

        <div className="contact-row">

          <Calendar size={14} />

          <span>{lastContact}</span>

        </div>

        <button className="view-btn">

          View

          <ArrowUpRight size={15} />

        </button>

      </div>

    </div>
  );
}