import { forwardRef } from "react";

const AlertCard = forwardRef(function AlertCard(
  { alert, highlighted, onClick },
  ref
) {
  return (
    <div
      ref={ref}
      className={`alert-card priority-${alert.priority.toLowerCase()}${
        highlighted ? " alert-card-highlighted" : ""
      }`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onClick?.();
        }
      }}
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
