import { FileBarChart2 } from "lucide-react";

import "../styles/dashboard.css";

export default function Reports() {
  return (
    <div className="dashboard">

      <div className="dashboard-head">
        <div className="dashboard-title">
          <span className="section-label">Reporting</span>
          <h4 className="section-heading">Reports</h4>
          <p className="dashboard-subtitle">
            Compliance and impact reports for your CSR portfolio.
          </p>
        </div>
      </div>

      <div className="empty-state-panel">
        <FileBarChart2 size={28} className="empty-state-icon" />
        <h3>Reports are on the way</h3>
        <p>This section is under construction. Check back soon.</p>
      </div>

    </div>
  );
}
