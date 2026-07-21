import { forwardRef } from "react";

const AlertCard = forwardRef(function AlertCard({ alert, highlighted }, ref) {
  return (
    <div
      ref={ref}
      className={`alert-card priority-${alert.priority.toLowerCase()}${
        highlighted ? " alert-card-highlighted" : ""
      }`}
    >
      <div className="alert-left-bar" />

      <div className="alert-content">

        <div className="alert-row">

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
});

export default AlertCard;
