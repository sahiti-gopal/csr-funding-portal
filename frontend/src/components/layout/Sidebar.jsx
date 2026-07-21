import {
  LayoutGrid,
  AlertTriangle,
  FolderKanban,
  Users,
  FileText,
  Settings,
  Leaf,
  MessageSquare,
} from "lucide-react";
import { NavLink, Link } from "react-router-dom";
import "../../styles/layout.css";

const NAV = [
  { to: "/", label: "Overview", icon: LayoutGrid, end: true },
  { to: "/alerts", label: "Alerts", icon: AlertTriangle },
  { to: "/projects", label: "Projects", icon: FolderKanban },
  { to: "/donors", label: "Donors", icon: Users },
  { to: "/chat", label: "Chat", icon: MessageSquare },
  { to: "/reports", label: "Reports", icon: FileText },
  { to: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <Link to="/" className="logo">
        <div className="logo-circle">
          <Leaf size={22} />
        </div>
        <div>
          <h2>CSR Portal</h2>
          <p>Prayas Foundation</p>
        </div>
      </Link>

      <nav>
        {NAV.map(({ to, label, icon: Icon, end }) => (
          <NavLink key={to} to={to} end={end} className="nav-item">
            <Icon size={19} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
