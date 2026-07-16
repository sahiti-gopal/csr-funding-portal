import { Settings2 } from "lucide-react";

import "../styles/dashboard.css";

export default function Settings() {
  return (
    <div className="dashboard">

      <div className="dashboard-head">
        <div className="dashboard-title">
          <span className="section-label">Preferences</span>
          <h4 className="section-heading">Settings</h4>
          <p className="dashboard-subtitle">
            Manage your account, roles and portal preferences.
          </p>
        </div>
      </div>

      <div className="empty-state-panel">
        <Settings2 size={28} className="empty-state-icon" />
        <h3>Settings are on the way</h3>
        <p>This section is under construction. Check back soon.</p>
      </div>

    </div>
  );
}
