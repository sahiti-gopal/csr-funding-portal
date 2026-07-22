import { useEffect, useMemo, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

import AlertStats from "../components/alerts/AlertStats";
import AlertCard from "../components/alerts/AlertCard";
import AlertDetailModal from "../components/alerts/AlertDetailModal";

import "../styles/dashboard.css";
import "../styles/alerts.css";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/api";

const CARD_FILTERS = {
  total: () => true,
  high: (a) => a.priority === "HIGH",
  medium: (a) => a.priority === "MEDIUM",
  low: (a) => a.priority === "LOW",
};

export default function Alerts() {
  const location = useLocation();
  const navigate = useNavigate();

  const [alerts, setAlerts] = useState([]);

  const [summary, setSummary] = useState({
    total: 0,
    high: 0,
    medium: 0,
    low: 0,
  });

  const [loading, setLoading] = useState(true);

  const [activeCard, setActiveCard] = useState("total");

  const [selectedAlert, setSelectedAlert] = useState(null);

  const [highlightAlertId, setHighlightAlertId] = useState(
    location.state?.highlightAlertId ?? null
  );

  const alertRefs = useRef({});

  useEffect(() => {
    if (!location.state?.highlightAlertId) return;

    setActiveCard("total");

    // clear the router state so a refresh/back-nav doesn't re-highlight
    navigate(location.pathname, { replace: true, state: {} });
  }, [location.state]);

  useEffect(() => {
    if (!highlightAlertId) return;

    const timer = setTimeout(() => setHighlightAlertId(null), 3000);
    return () => clearTimeout(timer);
  }, [highlightAlertId]);

  useEffect(() => {
    if (!highlightAlertId) return;

    alertRefs.current[highlightAlertId]?.scrollIntoView({
      behavior: "smooth",
      block: "center",
    });
  }, [highlightAlertId, alerts]);

  const loadSummary = async () => {
    try {
      const res = await axios.get(`${API}/alerts/summary`);

      setSummary(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadAlerts = async () => {
    try {
      setLoading(true);

      const res = await axios.get(`${API}/alerts`);

      const mapped = res.data.map((a) => ({
        id: a.id,
        title: a.title,
        description: a.description,
        category: a.category,
        projectName: a.project_name,
        meta: a.meta ?? "",
        date: a.due_date,
        priority: a.priority,
        status: a.status,
        is_read: a.is_read,
        is_resolved: a.is_resolved,
      }));

      setAlerts(mapped);

      await loadSummary();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAlerts();
  }, []);

  const filteredAlerts = useMemo(() => {
    const matches = CARD_FILTERS[activeCard] ?? CARD_FILTERS.total;
    return alerts.filter(matches);
  }, [alerts, activeCard]);

  return (
    <div className="alerts-page">

      <div className="alerts-header">
        <div className="dashboard-title">
          <span className="eyebrow">Compliance &amp; risk</span>
          <h4 className="section-heading">Alerts</h4>
        </div>
      </div>

      <AlertStats
        summary={summary}
        activeCard={activeCard}
        onCardClick={setActiveCard}
      />

      <div className="alerts-list">

        {loading ? (
          <div className="loading-card">
            Loading alerts...
          </div>
        ) : filteredAlerts.length === 0 ? (
          <div className="loading-card">
            No alerts found.
          </div>
        ) : (
          filteredAlerts.map((alert) => (
            <AlertCard
              key={alert.id}
              alert={alert}
              ref={(el) => {
                if (el) alertRefs.current[alert.id] = el;
                else delete alertRefs.current[alert.id];
              }}
              highlighted={alert.id === highlightAlertId}
              onClick={() => setSelectedAlert(alert)}
            />
          ))
        )}

      </div>

      {selectedAlert && (
        <AlertDetailModal
          alert={selectedAlert}
          onClose={() => setSelectedAlert(null)}
        />
      )}

    </div>
  );
}