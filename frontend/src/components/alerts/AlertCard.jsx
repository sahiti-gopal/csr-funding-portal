import {
  HeartHandshake,
  FileText,
  FileBarChart2,
  Settings2,
} from "lucide-react";

const CATEGORY = {
  "DONOR RISK": {
    icon: HeartHandshake,
    className: "risk",
    label: "DONOR RISK",
  },
  DOCUMENTS: {
    icon: FileText,
    className: "documents",
    label: "DOCUMENTS",
  },
  REPORTS: {
    icon: FileBarChart2,
    className: "reports",
    label: "REPORTS",
  },
  SYSTEM: {
    icon: Settings2,
    className: "system",
    label: "SYSTEM",
  },
};

export default function AlertCard({ alert }) {
  const item =
    CATEGORY[alert.type?.toUpperCase()] ??
    CATEGORY.SYSTEM;

  const Icon = item.icon;

  return (
    <div
      className={`alert-card priority-${alert.priority.toLowerCase()}`}
    >
      <div className="alert-left-bar" />

      <div className="alert-content">

        <div className="alert-row">

          <span
            className={`alert-pill ${item.className}`}
          >
            {item.label}
          </span>

          <div className="alert-title">
            {alert.title}
          </div>

          <div className="alert-date">
            {alert.date}
          </div>

          <span
            className={`priority-pill ${alert.priority.toLowerCase()}`}
          >
            {alert.priority}
          </span>

        </div>

        <div className="alert-meta">
          {alert.description}
        </div>

      </div>

    </div>
  );
}