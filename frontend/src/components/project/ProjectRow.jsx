import { Eye, MapPin } from "lucide-react";
import { useNavigate } from "react-router-dom";

const formatCr = (value) =>
  `₹${(Number(value ?? 0) / 10000000).toFixed(1)} Cr`;

export default function ProjectRow({ project }) {
  const navigate = useNavigate();

  const statusClass = () => {
    switch (project.status) {
      case "Completed":
        return "completed";

      case "Delayed":
        return "delayed";

      case "On Hold":
        return "on-hold";

      case "Planning":
        return "planning";

      case "Registered":
        return "registered";

      default:
        return "active";
    }
  };

  const budget = Number(project.budget ?? 0);
  const utilized = Number(project.utilized_amount ?? 0);
  const usedPct = budget > 0 ? Math.round((utilized / budget) * 100) : 0;

  return (
    <tr className="project-row">
      <td>
        <strong>{project.project_name}</strong>
        <div className="project-row-sub">{project.project_type}</div>
      </td>

      <td>{project.sponsor_name || "—"}</td>

      <td>
        <span className="project-row-region">
          <MapPin size={14} />
          {project.region || project.location}
        </span>
      </td>

      <td>
        <strong>{formatCr(budget)}</strong>
        <div className="project-row-sub">{usedPct}% used</div>
      </td>

      <td>
        <div className="progress-cell">
          <span className="progress-pct">{usedPct}%</span>
          <div className="progress-track">
            <div
              className="progress-fill"
              style={{ width: `${Math.min(usedPct, 100)}%` }}
            />
          </div>
        </div>
      </td>

      <td>
        <span className={`status ${statusClass()}`}>
          {project.status}
        </span>
      </td>

      <td>{project.end_date}</td>

      <td>
        <button
          className="view-btn"
          onClick={() => navigate(`/projects/${project.id}`)}
        >
          <Eye size={18} />
          View
        </button>
      </td>
    </tr>
  );
}