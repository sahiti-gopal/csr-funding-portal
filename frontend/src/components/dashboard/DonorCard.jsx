export default function DonorCard({
  donor,
  category,
  likelihood,
  lastContact,
  color,
}) {
  return (
    <div
      className="donor-bullet"
      style={{ borderLeftColor: color }}
    >

      <div className="donor-content">

        <div className="donor-row">

          <h4>{donor}</h4>

          <span className="donor-score">
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