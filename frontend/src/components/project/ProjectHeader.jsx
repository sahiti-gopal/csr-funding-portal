import { ChevronLeft, ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";

const TABS = [
  { key: "overview", label: "Overview" },
  { key: "gallery", label: "Gallery" },
];

export default function ProjectHeader({ name, activeTab, onTabChange }) {
  return (
    <div className="pd-header">
      <nav className="pd-breadcrumb">
        <Link to="/projects" className="pd-crumb-link">
          <ChevronLeft size={16} />
          Projects
        </Link>
        <ChevronRight size={16} className="pd-crumb-sep" />
        <span className="pd-crumb-current">{name}</span>
      </nav>

      <div className="pd-tabs" role="tablist">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            role="tab"
            aria-selected={activeTab === tab.key}
            className={`pd-tab ${activeTab === tab.key ? "active" : ""}`}
            onClick={() => onTabChange(tab.key)}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </div>
  );
}
