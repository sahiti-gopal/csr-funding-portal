import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import {
  RefreshCcw,
  Download,
} from "lucide-react";

import AlertStats from "../components/alerts/AlertStats";
import AlertCard from "../components/alerts/AlertCard";

import "../styles/dashboard.css";
import "../styles/alerts.css";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/api";

const CARD_FILTERS = {
  total: () => true,
  unread: (a) => !a.is_read,
  high: (a) => a.priority === "HIGH",
  resolved: (a) => a.is_resolved,
};

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);

  const [summary, setSummary] = useState({
    total: 0,
    unread: 0,
    high: 0,
    resolved: 0,
  });

  const [loading, setLoading] = useState(true);

  const [activeCard, setActiveCard] = useState("total");

  const loadSummary = async () => {
    try {
      const res = await axios.get(`${API}/alerts/summary`);

      console.log("SUMMARY API:", res.data);

      setSummary(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadAlerts = async () => {
    try {
      setLoading(true);

      const res = await axios.get(`${API}/alerts`);

      console.log("ALERTS API:", res.data);

      const mapped = res.data.map((a) => ({
        id: a.id,
        title: a.title,
        description: a.description,
        meta: a.meta ?? "",
        date: a.due_date,
        priority: a.priority,
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

  const exportAlerts = () => {
    window.open(`${API}/alerts/export`, "_blank");
  };

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
            />
          ))
        )}

      </div>

    </div>
  );
}