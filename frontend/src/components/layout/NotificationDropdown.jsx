
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import {
  Bell,
  TriangleAlert,
  CircleAlert,
  CircleCheck,
} from "lucide-react";

const API = "http://127.0.0.1:5000/api";

export default function NotificationDropdown({ onClose }) {
  const navigate = useNavigate();

  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    try {
      const res = await axios.get(`${API}/alerts`);

      setAlerts(res.data.slice(0, 5));
    } catch (err) {
      console.error(err);
    }
  };

  const getIcon = (priority) => {
    switch (priority?.toLowerCase()) {
      case "high":
        return <TriangleAlert size={18} color="#EF4444" />;

      case "medium":
        return <CircleAlert size={18} color="#F59E0B" />;

      default:
        return <CircleCheck size={18} color="#22C55E" />;
    }
  };

  return (
    <div className="notification-dropdown">

      <div className="notification-header">

        <div className="notification-title">

          <Bell size={18} />

          Notifications

        </div>

        <span
  className="view-all-link"
  onClick={() => {
    navigate("/alerts");
    onClose?.();
  }}
>
  View all →
</span>
      </div>

      <div className="notification-list">

        {alerts.length === 0 ? (

          <div className="notification-empty">

            No notifications

          </div>

        ) : (

          alerts.map((alert) => (

  <div
    key={alert.id}
    className="notification-row"
    onClick={() => {
      navigate("/alerts");
      onClose?.();
    }}
  >

    <div className="notification-icon">
      {getIcon(alert.priority)}
    </div>

    <div className="notification-text">

      <h4>{alert.title}</h4>

      <span>{alert.category}</span>

    </div>

    <div
      className={`priority-dot ${alert.priority.toLowerCase()}`}
    />

  </div>

))

        )}

      </div>

    </div>
  );
}