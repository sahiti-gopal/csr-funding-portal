import {
  LayoutGrid,
  AlertTriangle,
  FolderKanban,
  Users,
  FileText,
  Settings,
  Leaf,
  BadgeCheck,
  MessageSquare,
  LogOut,
} from "lucide-react";
import { NavLink, Link, useNavigate } from "react-router-dom";
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
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("seva-user-email");
    navigate("/login");
  };

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

      <div className="sidebar-user">
        <img
  src="/images/team/Woman-3.png"
  alt="Sahiti"
  className="sidebar-user-avatar-img"
/>
        <div className="sidebar-user-info">
          <p className="sidebar-user-name">Sahiti</p>
          <p className="sidebar-user-role">
            <BadgeCheck size={13} />
            CSR Admin
          </p>
        </div>
        <button
          className="sidebar-logout"
          onClick={handleLogout}
          aria-label="Sign out"
          title="Sign out"
        >
          <LogOut size={16} />
        </button>
      </div>
    </aside>
  );
}
