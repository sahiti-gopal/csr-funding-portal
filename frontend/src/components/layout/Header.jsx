import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Bell } from "lucide-react";

import NotificationDropdown from "./NotificationDropdown";

import "../../styles/layout.css";

const API = "http://127.0.0.1:5000/api";

const greeting = () => {
  const hour = new Date().getHours();

  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";

  return "Good evening";
};

export default function Header({
  userName = "Sahiti",
  filters,
  onFilterChange,
}) {
  const navigate = useNavigate();

  const [alerts, setAlerts] = useState([]);

  const [showNotifications, setShowNotifications] =
    useState(false);

  const notificationRef = useRef(null);

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

  const loadAlerts = async () => {
    try {
      const res = await axios.get(`${API}/alerts`);

      setAlerts(res.data);
    } catch (err) {
      console.error(err);
    }
  };

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

      <h1 className="header-greeting">
        {greeting()}, {userName}! ☀️
      </h1>

      <div className="header-right">

        {filters && (
          <div className="header-filters">

            <select
              value={filters.region}
              onChange={(e) =>
                onFilterChange(
                  "region",
                  e.target.value
                )
              }
            >
              <option value="all">
                All Regions
              </option>
              <option value="South">
                South
              </option>
              <option value="West">
                West
              </option>
              <option value="North">
                North
              </option>
              <option value="East">
                East
              </option>
            </select>

            <select
              value={filters.fy}
              onChange={(e) =>
                onFilterChange(
                  "fy",
                  e.target.value
                )
              }
            >
              <option value="all">
                All Years
              </option>
              <option value="2023-24">
                FY 2023-24
              </option>
              <option value="2024-25">
                FY 2024-25
              </option>
              <option value="2025-26">
                FY 2025-26
              </option>
              <option value="2026-27">
                FY 2026-27
              </option>
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
            <Bell size={20} />

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

      </div>

    </header>
  );
}