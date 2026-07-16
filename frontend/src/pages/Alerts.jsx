import { useEffect, useState } from "react";
import axios from "axios";
import {
  RefreshCcw,
  Download,
} from "lucide-react";

import AlertStats from "../components/alerts/AlertStats";
import AlertFilters from "../components/alerts/AlertFilters";
import AlertCard from "../components/alerts/AlertCard";

import "../styles/alerts.css";

const API = "http://127.0.0.1:5000/api";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);

  const [summary, setSummary] = useState({
    total: 0,
    unread: 0,
    high: 0,
    resolved: 0,
  });

  const [loading, setLoading] = useState(true);

  const [category, setCategory] = useState("All");
  const [priority, setPriority] = useState("All");

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

      const res = await axios.get(`${API}/alerts`, {
        params: {
          category,
          priority,
        },
      });

      console.log("ALERTS API:", res.data);

      const mapped = res.data.map((a) => ({
        id: a.id,
        type: a.category,
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
  }, [category, priority]);

  const exportAlerts = () => {
    window.open(`${API}/alerts/export`, "_blank");
  };

  return (
    <div className="alerts-page">

      <div className="alerts-header">

  <div>
    <h4>Alerts</h4>
  </div>

</div>
      <AlertStats summary={summary} />

      <AlertFilters
        category={category}
        priority={priority}
        onCategoryChange={setCategory}
        onPriorityChange={setPriority}
      />

      <div className="alerts-list">

        {loading ? (
          <div className="loading-card">
            Loading alerts...
          </div>
        ) : alerts.length === 0 ? (
          <div className="loading-card">
            No alerts found.
          </div>
        ) : (
          alerts.map((alert) => (
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