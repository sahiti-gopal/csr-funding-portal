import { ChevronRight } from "lucide-react";

export default function RiskCard({
  icon: Icon,
  title,
  description,
  level,
  timeLeft,
  action,
}) {
  const tone = level.toLowerCase();

  return (
    <div className="risk-card">
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

      <button className={`risk-action risk-action-${tone}`}>
        <span>{action}</span>
        <ChevronRight size={16} />
      </button>
    </div>
  );
}
