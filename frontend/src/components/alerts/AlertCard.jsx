export default function AlertCard({ alert }) {
  return (
    <div
      className={`alert-card priority-${alert.priority.toLowerCase()}`}
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
}
