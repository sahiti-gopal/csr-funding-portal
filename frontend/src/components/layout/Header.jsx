import { useEffect, useRef, useState } from "react";
import {
  Link,
  useLocation,
  useMatch,
  useNavigate,
  useSearchParams,
} from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import {
  Bell,
  BadgeCheck,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  LogOut,
} from "lucide-react";

import NotificationDropdown from "./NotificationDropdown";
import { getGreeting } from "../../utils/greeting";
import { getProject } from "../../services/projectService";

import "../../styles/layout.css";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/api";

export default function Header({
  userName = "Sahiti",
}) {
  const location = useLocation();
  const navigate = useNavigate();
  const isMainPage = location.pathname === "/";

  const handleLogout = () => {
    localStorage.removeItem("seva-user-email");
    navigate("/login");
  };

  const projectMatch = useMatch("/projects/:id");
  const projectId = projectMatch?.params?.id;

  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => getProject(projectId),
    enabled: Boolean(projectId),
  });

  const [searchParams, setSearchParams] = useSearchParams();
  const region = searchParams.get("region") || "all";
  const fy = searchParams.get("fy") || "all";

  const handleFilterChange = (key, value) => {
    const next = new URLSearchParams(searchParams);
    next.set(key, value);
    setSearchParams(next);
  };

  const [alerts, setAlerts] = useState([]);

  const [showNotifications, setShowNotifications] =
    useState(false);

  const [showUserMenu, setShowUserMenu] = useState(false);

  const notificationRef = useRef(null);
  const userMenuRef = useRef(null);

  const loadAlerts = async () => {
    try {
      const res = await axios.get(`${API}/alerts`);

      setAlerts(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadAlerts();
  }, []);

  useEffect(() => {
    function handleClickOutside(event) {
      if (
        notificationRef.current &&
        !notificationRef.current.contains(event.target)
      ) {
        setShowNotifications(false);
      }

      if (
        userMenuRef.current &&
        !userMenuRef.current.contains(event.target)
      ) {
        setShowUserMenu(false);
      }
    }

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () =>
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );
  }, []);

  const unreadCount = alerts.filter(
    (a) => !a.is_read
  ).length;

  const openNotifications = async () => {
    setShowNotifications((prev) => !prev);

    try {
      await axios.post(
        `${API}/alerts/mark-all-read`
      );

      setAlerts((prev) =>
        prev.map((alert) => ({
          ...alert,
          is_read: true,
        }))
      );
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <header className="header">

      {isMainPage && (
        <h1 className="header-greeting">
          {getGreeting()}, {userName}!
        </h1>
      )}

      {projectMatch && (
        <nav className="header-breadcrumb">
          <Link to="/projects" className="header-crumb-link">
            <ChevronLeft size={16} />
            Projects
          </Link>
          <ChevronRight size={14} className="header-crumb-sep" />
          <span className="header-crumb-current">
            {project?.project_name ?? "…"}
          </span>
        </nav>
      )}

      <div className="header-right">

        {isMainPage && (
          <div className="header-filters">
            <select
              value={region}
              onChange={(e) =>
                handleFilterChange("region", e.target.value)
              }
            >
              <option value="all">All Regions</option>
              <option value="South">South</option>
              <option value="West">West</option>
              <option value="North">North</option>
              <option value="East">East</option>
            </select>

            <select
              value={fy}
              onChange={(e) =>
                handleFilterChange("fy", e.target.value)
              }
            >
              <option value="all">All Years</option>
              <option value="2023-24">FY 2023-24</option>
              <option value="2024-25">FY 2024-25</option>
              <option value="2025-26">FY 2025-26</option>
              <option value="2026-27">FY 2026-27</option>
            </select>
          </div>
        )}

        <div
          className="notification-wrapper"
          ref={notificationRef}
        >

          <button
            className="header-bell"
            aria-label="Notifications"
            onClick={openNotifications}
          >
            <Bell size={17} />

            {unreadCount > 0 && (
              <span className="header-bell-badge">
                {unreadCount}
              </span>
            )}
          </button>

          {showNotifications && (
            <NotificationDropdown
              alerts={alerts}
              onClose={() =>
                setShowNotifications(false)
              }
            />
          )}

        </div>

        <div className="header-user" ref={userMenuRef}>
          <button
            className="header-user-trigger"
            onClick={() => setShowUserMenu((prev) => !prev)}
            aria-label="Account menu"
          >
            <img
              src="/images/team/Woman-3.png"
              alt={userName}
              className="header-user-avatar-img"
            />
            <div className="header-user-info">
              <p className="header-user-name">{userName}</p>
              <p className="header-user-role">
                <BadgeCheck size={13} />
                CSR Admin
              </p>
            </div>
            <ChevronDown size={14} className="header-user-caret" />
          </button>

          {showUserMenu && (
            <div className="header-user-menu">
              <button
                className="header-user-menu-item"
                onClick={handleLogout}
              >
                <LogOut size={14} />
                Sign out
              </button>
            </div>
          )}
        </div>

      </div>

    </header>
  );
}
