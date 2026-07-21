const TABS = [
  { key: "overview", label: "Overview" },
  { key: "gallery", label: "Gallery" },
];

export default function ProjectHeader({ activeTab, onTabChange }) {
  return (
    <div className="pd-header">
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
