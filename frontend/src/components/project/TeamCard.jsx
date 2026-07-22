import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

const BADGE_CLASS = {
  Lead: "pd-badge-green",
  Ops: "pd-badge-blue",
  Training: "pd-badge-purple",
  Partner: "pd-badge-outline",
};

export default function TeamCard({ members = [] }) {
  const [open, setOpen] = useState(false);
  return (
  <div className="pd-panel">

    <div
      className="pd-collapse-header"
      onClick={() => setOpen(!open)}
    >
      <h4 className="pd-panel-title">
        Team & Ownership
      </h4>

      <div className="pd-collapse-right">
        <span>{members.length} Members</span>

        {open ? (
          <ChevronDown size={18} />
        ) : (
          <ChevronRight size={18} />
        )}
      </div>
    </div>

    {open && (
      <ul className="pd-team-list">
        {members.map((member) => (
          <li className="pd-team-row" key={member.name}>
            <span
              className="pd-avatar"
              style={{ background: member.color }}
            >
              {member.image ? (
                <img
                  src={member.image}
                  alt={member.name}
                  className="pd-avatar-img"
                />
              ) : (
                member.initials
              )}
            </span>

            <div className="pd-team-info">
              <p className="pd-team-name">{member.name}</p>
              <p className="pd-team-role">{member.role}</p>
            </div>

            <span
              className={`pd-badge ${
                BADGE_CLASS[member.tag] ?? "pd-badge-blue"
              }`}
            >
              {member.tag}
            </span>
          </li>
        ))}
      </ul>
    )}
  </div>
);
}