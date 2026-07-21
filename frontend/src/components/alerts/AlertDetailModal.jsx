import { useEffect } from "react";
import { createPortal } from "react-dom";
import { X, CalendarDays, FolderKanban, Tag } from "lucide-react";

export default function AlertDetailModal({ alert, onClose }) {
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === "Escape") onClose?.();
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  if (!alert) return null;

  return createPortal(
    <div className="alert-modal-overlay" onClick={onClose}>
      <div
        className="alert-modal"
        role="dialog"
        aria-modal="true"
        onClick={(event) => event.stopPropagation()}
      >
        <button
          type="button"
          className="alert-modal-close"
          aria-label="Close"
          onClick={onClose}
        >
          <X size={16} />
        </button>

        <div className={`alert-modal-bar priority-${alert.priority.toLowerCase()}`} />

        <div className="alert-modal-body">
          <span className={`priority-pill ${alert.priority.toLowerCase()}`}>
            {alert.priority}
          </span>

          <h3 className="alert-modal-title">{alert.title}</h3>

          <p className="alert-modal-description">{alert.description}</p>

          <dl className="alert-modal-meta">
            {alert.date && (
              <div>
                <dt>
                  <CalendarDays size={13} />
                  Due date
                </dt>
                <dd>{alert.date}</dd>
              </div>
            )}

            {alert.category && (
              <div>
                <dt>
                  <Tag size={13} />
                  Category
                </dt>
                <dd>{alert.category}</dd>
              </div>
            )}

            {alert.projectName && (
              <div>
                <dt>
                  <FolderKanban size={13} />
                  Project
                </dt>
                <dd>{alert.projectName}</dd>
              </div>
            )}
          </dl>

          <div className="alert-modal-status">
            <span className={`alert-modal-status-pill ${alert.is_read ? "read" : "unread"}`}>
              {alert.is_read ? "Read" : "Unread"}
            </span>
            <span
              className={`alert-modal-status-pill ${alert.is_resolved ? "resolved" : "open"}`}
            >
              {alert.is_resolved ? "Resolved" : "Open"}
            </span>
          </div>
        </div>
      </div>
    </div>,
    document.body
  );
}
