export default function DonorCard({
  donor,
  category,
  likelihood,
  lastContact,
  color,
}) {
  return (
    <div className="donor-bullet">

      <div className="donor-status">
        <span
          className="status-dot"
          style={{ background: color }}
        />
      </div>

      <div className="donor-content">

        <div className="donor-row">

          <h4>{donor}</h4>

          <span
            className="donor-score"
            style={{ color }}
          >
            {likelihood}%
          </span>

        </div>

        <div className="donor-meta">
          {category} • Last contact {lastContact}
        </div>

      </div>

    </div>
  );
}