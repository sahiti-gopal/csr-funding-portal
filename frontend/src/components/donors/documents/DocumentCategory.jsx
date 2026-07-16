import {
  ChevronDown,
  FolderOpen,
} from "lucide-react";

export default function DocumentCategory({
  title,
  subtitle,
  progress,
  completed,
  color,
}) {
  return (
    <div className="document-category">

      <div className="category-header">

        <div className="category-left">

          <div
            className="category-icon"
            style={{
              background: `${color}15`,
              color,
            }}
          >
            <FolderOpen size={20} />
          </div>

          <div>

            <h3>{title}</h3>

            <p>{subtitle}</p>

          </div>

        </div>

        <div className="category-right">

          <strong>{completed}</strong>

          <ChevronDown size={20} />

        </div>

      </div>

      <div className="category-progress">

        <div className="category-track">

          <div
            className="category-fill"
            style={{
              width: `${progress}%`,
              background: color,
            }}
          />

        </div>

        <span>{progress}% Complete</span>

      </div>

    </div>
  );
}   