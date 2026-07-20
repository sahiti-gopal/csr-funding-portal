import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Sparkles,
  TriangleAlert,
  HeartPulse,
  HeartHandshake,
} from "lucide-react";

import { getDonor, getDonorAiSummary } from "../services/donorService";

import "../styles/donors.css";
import "../styles/donorDetail.css";

const initials = (name = "") =>
  name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0])
    .join("")
    .toUpperCase();

const formatAmount = (amount) => {
  if (!amount) return "₹0";
  if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(1)} Cr`;
  if (amount >= 100000) return `₹${(amount / 100000).toFixed(1)} L`;
  return `₹${amount.toLocaleString()}`;
};

const PROJECT_STATUS_CLASS = {
  Active: "status-pill-active",
  Completed: "status-pill-completed",
  Planning: "status-pill-attention",
  Pending: "status-pill-attention",
  "On Hold": "status-pill-attention",
};

export default function DonorDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [donor, setDonor] = useState(null);
  const [loadingDonor, setLoadingDonor] = useState(true);

  const [aiSummary, setAiSummary] = useState(null);
  const [loadingAi, setLoadingAi] = useState(true);

  useEffect(() => {
    setLoadingDonor(true);
    getDonor(id)
      .then(setDonor)
      .catch(console.error)
      .finally(() => setLoadingDonor(false));
  }, [id]);

  useEffect(() => {
    setLoadingAi(true);
    getDonorAiSummary(id)
      .then(setAiSummary)
      .catch(console.error)
      .finally(() => setLoadingAi(false));
  }, [id]);

  if (loadingDonor) {
    return <div className="donor-detail-loading">Loading donor…</div>;
  }

  if (!donor) {
    return <div className="donor-detail-loading">Donor not found.</div>;
  }

  return (
    <div className="donor-detail-page">
      <button
        type="button"
        className="donor-detail-back"
        onClick={() => navigate("/donors")}
      >
        <ArrowLeft size={16} />
        Back to Donors
      </button>

      <div className="donor-detail-header">
        {donor.logo_url ? (
          <img
            src={donor.logo_url}
            alt={donor.name}
            className="donor-detail-logo"
            onError={(e) => {
              e.currentTarget.style.display = "none";
            }}
          />
        ) : (
          <div className="donor-detail-logo donor-detail-logo-fallback">
            {initials(donor.name)}
          </div>
        )}

        <div className="donor-detail-title">
          <h1>{donor.name}</h1>
          <div className="donor-detail-meta">
            <span>{donor.focus_area}</span>
            <span className="donor-detail-dot">•</span>
            <span>{donor.likelihood}% likelihood</span>
            <span className="donor-detail-dot">•</span>
            <span>Last contact: {donor.last_contact ?? "Never"}</span>
          </div>
        </div>

        <span className="donor-detail-status-pill">{donor.status}</span>
      </div>

      <div className="donor-detail-stats-row">
        <div className="donor-detail-stat">
          <span>Projects</span>
          <strong>{donor.projects_total}</strong>
        </div>
        <div className="donor-detail-stat">
          <span>Utilization</span>
          <strong>{donor.utilization_pct}%</strong>
        </div>
        <div className="donor-detail-stat">
          <span>Raised</span>
          <strong>{formatAmount(donor.raised_total)}</strong>
        </div>
        <div className="donor-detail-stat">
          <span>Beneficiaries</span>
          <strong>{donor.beneficiaries_total.toLocaleString()}</strong>
        </div>
        <div className="donor-detail-stat">
          <span>Overdue payments</span>
          <strong>{donor.payments_overdue}</strong>
        </div>
      </div>

      <div className="donor-detail-ai-grid">
        <div className="donor-ai-card">
          <h3>
            <HeartHandshake size={18} className="icon-blue" />
            Engagement Summary
          </h3>
          {loadingAi ? (
            <div className="donor-ai-skeleton" />
          ) : (
            <p>{aiSummary?.engagement_summary}</p>
          )}
        </div>

        <div className="donor-ai-card">
          <h3>
            <TriangleAlert size={18} className="icon-amber" />
            Key Risks
          </h3>
          {loadingAi ? (
            <div className="donor-ai-skeleton" />
          ) : (
            <ul className="donor-ai-risk-list">
              {aiSummary?.key_risks?.map((risk, i) => (
                <li key={i}>{risk}</li>
              ))}
            </ul>
          )}
        </div>

        <div className="donor-ai-card">
          <h3>
            <HeartPulse size={18} className="icon-green" />
            Project Health
          </h3>
          {loadingAi ? (
            <div className="donor-ai-skeleton" />
          ) : (
            <p>{aiSummary?.project_health_summary}</p>
          )}
        </div>
      </div>

      {!loadingAi && (
        <div className="donor-ai-attribution">
          <Sparkles size={13} />
          {aiSummary?.ai_generated
            ? "Generated by AI from this donor's project and payment data."
            : "Computed summary (AI generation unavailable)."}
        </div>
      )}

      <div className="donor-detail-projects">
        <h3>Funded Projects</h3>

        {donor.projects.length === 0 ? (
          <div className="donor-detail-empty">No projects yet.</div>
        ) : (
          <table className="donor-detail-projects-table">
            <thead>
              <tr>
                <th>Project</th>
                <th>Status</th>
                <th>Budget</th>
                <th>Raised</th>
                <th>Utilized</th>
                <th>Beneficiaries</th>
              </tr>
            </thead>
            <tbody>
              {donor.projects.map((p) => (
                <tr key={p.id}>
                  <td>{p.name}</td>
                  <td>
                    <span
                      className={`donor-detail-status-badge ${
                        PROJECT_STATUS_CLASS[p.status] ?? ""
                      }`}
                    >
                      {p.status}
                    </span>
                  </td>
                  <td>{formatAmount(p.budget)}</td>
                  <td>{formatAmount(p.raised_amount)}</td>
                  <td>{formatAmount(p.utilized_amount)}</td>
                  <td>{p.beneficiaries_reached.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
