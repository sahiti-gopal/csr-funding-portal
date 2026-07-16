export default function ProjectOwnerCard({ members = [] }) {
  const owner = members[0];

  if (!owner) return null;

  return (
    <div className="card project-owner-card">

      <h3 className="pd-section-title">
        Project Owner
      </h3>

      <div className="owner-profile">

        <div className="owner-avatar">

          <img
            src={owner.image}
            alt={owner.name}
            className="owner-avatar-img"
          />

        </div>

        <div>

          <h4>{owner.name}</h4>

          <p>{owner.role}</p>

        </div>

      </div>

      <div className="owner-divider" />

      <div className="owner-row">

        <span>Business Unit</span>

        <strong>BU2</strong>

      </div>

      <div className="owner-row">

        <span>Team Size</span>

        <strong>{members.length} Members</strong>

      </div>

    </div>
  );
}