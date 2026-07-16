import Collapsible from "./Collapsible";

export default function ProjectOwnerCard({ members = [] }) {
  const owner = members[0];

  if (!owner) {
    return (
      <Collapsible
        title="Project Owner"
        wrapperClassName="card project-owner-card"
      >
        <p className="pd-empty-note">
          No project owner assigned yet.
        </p>
      </Collapsible>
    );
  }

  return (
    <Collapsible
      title="Project Owner"
      wrapperClassName="card project-owner-card"
    >

      <div className="owner-profile">

        <div
          className="owner-avatar"
          style={!owner.image ? { background: owner.color } : undefined}
        >

          {owner.image ? (
            <img
              src={owner.image}
              alt={owner.name}
              className="owner-avatar-img"
            />
          ) : (
            <span className="pd-avatar-fallback">
              {owner.initials}
            </span>
          )}

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

    </Collapsible>
  );
}