import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  FileBarChart2,
  Plus,
  Eye,
  Download,
  RotateCw,
  FileText,
  Clock,
  CheckCircle2,
  Send,
} from "lucide-react";

import { listReports, retryReport } from "../services/reportService";
import { formatCurrency, formatCount } from "../utils/format";

import "../styles/dashboard.css";
import "../styles/reports.css";

const DONOR_COLORS = [
  "#0f1f3d", "#2563eb", "#7c3aed", "#0d9488", "#dc2626",
  "#ea580c", "#0891b2", "#4d7c0f", "#9333ea", "#be123c",
];

const initials = (name = "") =>
  name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0])
    .join("")
    .toUpperCase();

const colorFor = (name = "") => {
  let hash = 0;
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);
  return DONOR_COLORS[Math.abs(hash) % DONOR_COLORS.length];
};

const formatDate = (iso) =>
  iso
    ? new Date(iso).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" })
    : "—";

const formatFunds = (value) => formatCurrency(value, { fallback: "—" });

const REVIEW_CLASS = {
  Approved: "approved",
  "Pending review": "pending",
  Failed: "failed",
};

const DELIVERY_CLASS = {
  Delivered: "delivered",
  Awaiting: "awaiting",
};

const CARD_FILTERS = {
  total: () => true,
  pending: (r) => r.review_status === "Pending review",
  approved: (r) => r.review_status === "Approved",
  delivered: (r) => r.delivery_status === "Delivered",
};

export default function Reports() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [activeCard, setActiveCard] = useState("total");

  const { data: reports = [], isLoading } = useQuery({
    queryKey: ["reports"],
    queryFn: listReports,
  });

  const retryMutation = useMutation({
    mutationFn: retryReport,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["reports"] }),
  });

  const stats = useMemo(() => {
    const pending = reports.filter((r) => r.review_status === "Pending review").length;
    const approved = reports.filter((r) => r.review_status === "Approved").length;
    const delivered = reports.filter((r) => r.delivery_status === "Delivered").length;

    return [
      { key: "total", title: "Total Reports", value: reports.length, icon: FileText },
      { key: "pending", title: "Pending Review", value: pending, icon: Clock },
      { key: "approved", title: "Approved", value: approved, icon: CheckCircle2 },
      { key: "delivered", title: "Delivered", value: delivered, icon: Send },
    ];
  }, [reports]);

  const filteredReports = useMemo(() => {
    const matches = CARD_FILTERS[activeCard] ?? CARD_FILTERS.total;
    return reports.filter(matches);
  }, [reports, activeCard]);

  return (
    <div className="dashboard reports-page">
      <div className="dashboard-head">
        <div className="dashboard-title">
          <span className="eyebrow">Reporting</span>
          <h4 className="section-heading">Reports</h4>
          <p className="dashboard-subtitle">
            AI-generated annual reports, one per donor per financial year.
          </p>
        </div>

        <button className="reports-generate-btn" onClick={() => navigate("/reports/generate")}>
          <Plus size={16} />
          Generate Report
        </button>
      </div>

      <div className="overview-grid reports-stats-grid">
        {stats.map((card) => {
          const Icon = card.icon;
          return (
            <div
              key={card.key}
              className={`overview-card stat-card ${activeCard === card.key ? "active" : ""}`}
              onClick={() => setActiveCard(card.key)}
            >
              <span className="stat-icon">
                <Icon size={15} />
              </span>
              <span className="eyebrow">{card.title}</span>
              <div className="overview-value">{card.value}</div>
            </div>
          );
        })}
      </div>

      <div className="reports-table-panel">
        {isLoading ? (
          <div className="empty-state-panel">
            <FileBarChart2 size={28} className="empty-state-icon" />
            <h3>Loading reports…</h3>
          </div>
        ) : reports.length === 0 ? (
          <div className="empty-state-panel">
            <FileBarChart2 size={28} className="empty-state-icon" />
            <h3>No reports yet</h3>
            <p>Generate your first AI report to see it here.</p>
          </div>
        ) : filteredReports.length === 0 ? (
          <div className="empty-state-panel">
            <FileBarChart2 size={28} className="empty-state-icon" />
            <h3>No reports match this filter</h3>
            <p>Try a different card, or clear the filter to see all reports.</p>
          </div>
        ) : (
          <table className="reports-table">
            <thead>
              <tr>
                <th>Report Name</th>
                <th>Donor</th>
                <th>FY</th>
                <th>Projects</th>
                <th>Beneficiaries</th>
                <th>Committed</th>
                <th>Utilization</th>
                <th>Generated</th>
                <th>Review</th>
                <th>Delivery</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredReports.map((r) => (
                <tr key={r.id}>
                  <td className="reports-name-cell">{r.title}</td>
                  <td>
                    <div className="reports-donor-cell">
                      <span
                        className="reports-donor-avatar"
                        style={{ background: colorFor(r.donor?.name) }}
                      >
                        {initials(r.donor?.name)}
                      </span>
                      <div>
                        <div>{r.donor?.name}</div>
                        {r.donor?.focus_area && (
                          <div className="reports-donor-focus">{r.donor.focus_area}</div>
                        )}
                      </div>
                    </div>
                  </td>
                  <td>{r.financial_year}</td>
                  <td>{r.project_count ?? "—"}</td>
                  <td>{formatCount(r.beneficiaries_total, { fallback: "—" })}</td>
                  <td>{formatFunds(r.committed)}</td>
                  <td>
                    {r.utilization_pct != null ? (
                      <div className="reports-util-cell">
                        <div className="reports-progress-track">
                          <div
                            className="reports-progress-fill"
                            style={{
                              width: `${Math.min(r.utilization_pct, 100)}%`,
                              background: r.utilization_pct >= 75 ? "#16a34a" : "#f59e0b",
                            }}
                          />
                        </div>
                        <span className="reports-progress-label">{r.utilization_pct}%</span>
                      </div>
                    ) : (
                      "—"
                    )}
                  </td>
                  <td>{formatDate(r.generated_at)}</td>
                  <td>
                    <span className={`reports-pill ${REVIEW_CLASS[r.review_status] || ""}`}>
                      {r.review_status}
                    </span>
                  </td>
                  <td>
                    <span className={`reports-pill ${DELIVERY_CLASS[r.delivery_status] || ""}`}>
                      {r.delivery_status}
                    </span>
                  </td>
                  <td>
                    <div className="reports-actions">
                      <button onClick={() => navigate(`/reports/${r.id}`)}>
                        <Eye size={14} />
                        View
                      </button>
                      {r.review_status !== "Failed" && (
                        <button onClick={() => navigate(`/reports/${r.id}`)}>
                          <Download size={14} />
                          Download
                        </button>
                      )}
                      {r.review_status === "Failed" && (
                        <button
                          className="reports-retry-btn"
                          disabled={retryMutation.isPending}
                          onClick={() => retryMutation.mutate(r.id)}
                        >
                          <RotateCw size={14} />
                          Retry
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
