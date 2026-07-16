import {
  LayoutGrid,
  AlertTriangle,
  FolderKanban,
  Users,
  FileText,
  Settings,
  Leaf,
  BadgeCheck,
} from "lucide-react";
import { NavLink } from "react-router-dom";
import "../../styles/layout.css";

const NAV = [
  { to: "/", label: "Overview", icon: LayoutGrid, end: true },
  { to: "/alerts", label: "Alerts", icon: AlertTriangle },
  { to: "/projects", label: "Projects", icon: FolderKanban },
  { to: "/donors", label: "Donors", icon: Users },
  { to: "/reports", label: "Reports", icon: FileText },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="logo">
        <div className="logo-circle">
          <Leaf size={22} />
        </div>
        <div>
          <h2>CSR Portal</h2>
          <p>Prayas Foundation</p>
        </div>
      </div>

      <nav>
        {NAV.map(({ to, label, icon: Icon, end }) => (
          <NavLink key={to} to={to} end={end} className="nav-item">
            <Icon size={19} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-user">
        <img
  src="/images/Profilepic.jpg"
  alt="Sahiti"
  className="sidebar-user-avatar-img"
/>
        <div>
          <p className="sidebar-user-name">Sahiti</p>
          <p className="sidebar-user-role">
            <BadgeCheck size={13} />
            CSR Admin
          </p>
        </div>
      </div>
    </aside>
  );
}
