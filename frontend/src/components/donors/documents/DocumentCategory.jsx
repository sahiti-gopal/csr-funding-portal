import { useState } from "react";
import {
  ChevronDown,
  ChevronUp,
  FolderOpen,
} from "lucide-react";

import DocumentList from "./DocumentList";

export default function DocumentCategory({
  title,
  subtitle,
  progress,
  completed,
  color,
  documents = [],
  onUpload,
  onReview,
}) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="document-category">

      <div
        className="category-header"
        onClick={() => setExpanded((prev) => !prev)}
        style={{ cursor: "pointer" }}
      >

        <div className="category-left">

          <div
            className="category-icon"
            style={{
              background: `${color}15`,
              color,
            }}
          >
            <FolderOpen size={16} />
          </div>

          <div>

            <h3>{title}</h3>

            <p>{subtitle}</p>

          </div>

        </div>

        <div className="category-right">

          <strong>{completed}</strong>

          {expanded ? (
            <ChevronUp size={20} />
          ) : (
            <ChevronDown size={20} />
          )}

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

      {expanded && (
        <DocumentList
          documents={documents}
          onUpload={onUpload}
          onReview={onReview}
        />
      )}

    </div>
  );
}
