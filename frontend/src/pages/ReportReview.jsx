import { useParams, useNavigate } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
} from "recharts";
import {
  ArrowLeft,
  Leaf,
  CheckCircle2,
  Send,
  Download,
  RotateCw,
  AlertTriangle,
  Sparkles,
} from "lucide-react";

import { getReport, approveReport, deliverReport, retryReport } from "../services/reportService";

import "../styles/dashboard.css";
import "../styles/reports.css";

const DONOR_COLORS = [
  "#0f1f3d", "#2563eb", "#7c3aed", "#0d9488", "#dc2626",
  "#ea580c", "#0891b2", "#4d7c0f", "#9333ea", "#be123c",
];

const FOCUS_AREA_COLORS = ["#0f1f3d", "#16a34a", "#f59e0b", "#2563eb", "#7c3aed", "#dc2626"];

const initials = (name = "") =>
  name.split(" ").filter(Boolean).slice(0, 2).map((w) => w[0]).join("").toUpperCase();

const colorFor = (name = "") => {
  let hash = 0;
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);
  return DONOR_COLORS[Math.abs(hash) % DONOR_COLORS.length];
};

const formatCr = (value) => {
  const n = Number(value || 0);
  if (n >= 1e7) return `₹${(n / 1e7).toFixed(2)} Cr`;
  if (n >= 1e5) return `₹${(n / 1e5).toFixed(1)} L`;
  return `₹${n.toLocaleString("en-IN")}`;
};

const formatCompact = (value) => {
  const n = Number(value || 0);
  if (n >= 1e5) return `${(n / 1e5).toFixed(2)} Lakh`;
  return n.toLocaleString("en-IN");
};

export default function ReportReview() {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: report, isLoading } = useQuery({
    queryKey: ["report", id],
    queryFn: () => getReport(id),
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["report", id] });

  const approveMutation = useMutation({ mutationFn: () => approveReport(id), onSuccess: invalidate });
  const deliverMutation = useMutation({ mutationFn: () => deliverReport(id), onSuccess: invalidate });
  const retryMutation = useMutation({
    mutationFn: () => retryReport(id),
    onSuccess: () => {
      invalidate();
      queryClient.invalidateQueries({ queryKey: ["reports"] });
    },
  });

  if (isLoading) {
    return (
      <div className="dashboard reports-page">
        <p>Loading report…</p>
      </div>
    );
  }

  if (!report) return null;

  const c = report.content;

  return (
    <div className="dashboard reports-page">
      <button className="reports-back-link" onClick={() => navigate("/reports")}>
        <ArrowLeft size={15} />
        Back
      </button>

      <div className="reports-head-row">
        <div className="dashboard-title">
          <span className="eyebrow">Admin review</span>
          <h4 className="section-heading">Verify generated report data</h4>
        </div>

        <div className="reports-review-actions">
          {report.review_status === "Failed" && (
            <button
              className="reports-action-btn primary"
              disabled={retryMutation.isPending}
              onClick={() => retryMutation.mutate()}
            >
              <RotateCw size={14} />
              Retry Generation
            </button>
          )}
          {report.review_status === "Pending review" && (
            <button
              className="reports-action-btn primary"
              disabled={approveMutation.isPending}
              onClick={() => approveMutation.mutate()}
            >
              <CheckCircle2 size={14} />
              Approve
            </button>
          )}
          {report.review_status === "Approved" && report.delivery_status !== "Delivered" && (
            <button
              className="reports-action-btn primary"
              disabled={deliverMutation.isPending}
              onClick={() => deliverMutation.mutate()}
            >
              <Send size={14} />
              Mark Delivered
            </button>
          )}
          {report.review_status !== "Failed" && (
            <button className="reports-action-btn" onClick={() => window.print()}>
              <Download size={14} />
              Download
            </button>
          )}
        </div>
      </div>

      {report.review_status === "Failed" ? (
        <div className="reports-failed-panel">
          <AlertTriangle size={26} />
          <h3>Generation failed</h3>
          <p>{report.error_message || "An unknown error occurred while generating this report."}</p>
        </div>
      ) : (
        <div className="reports-doc" id="report-print-area">
          <div className="reports-doc-header">
            <div className="reports-doc-brand">
              <Leaf size={20} />
              <span>CSR</span>
            </div>
            <div className="reports-doc-title">
              <h2>IMPACT REPORT {report.financial_year}</h2>
              <p>Driving Meaningful Change, Together.</p>
            </div>
            <div
              className="reports-doc-donor-badge"
              style={{ background: colorFor(c?.donor?.name) }}
            >
              {initials(c?.donor?.name)}
            </div>
          </div>

          {c?.ai_narrative && (
            <div className="reports-doc-section reports-ai-blurb">
              <Sparkles size={14} />
              <p>{c.ai_narrative}</p>
            </div>
          )}

          <div className="reports-doc-section">
            <h5>Outcome Progress</h5>
            <table className="reports-outcome-table">
              <thead>
                <tr>
                  <th>Programme</th>
                  <th>Target</th>
                  <th>Achieved</th>
                  <th>Progress</th>
                </tr>
              </thead>
              <tbody>
                {(c?.outcome_progress || []).map((row) => (
                  <tr key={row.programme}>
                    <td>
                      <strong>{row.programme}</strong>
                      <span className="reports-outcome-meta">
                        {row.location} · {formatCr(row.budget)}
                      </span>
                    </td>
                    <td>{row.target.toLocaleString("en-IN")}</td>
                    <td>{row.achieved.toLocaleString("en-IN")}</td>
                    <td>
                      <div className="reports-progress-track">
                        <div
                          className="reports-progress-fill"
                          style={{
                            width: `${Math.min(row.progress_pct, 100)}%`,
                            background: row.progress_pct >= 75 ? "#16a34a" : "#f59e0b",
                          }}
                        />
                      </div>
                      <span className="reports-progress-label">{row.progress_pct}%</span>
                    </td>
                  </tr>
                ))}
                {(!c?.outcome_progress || c.outcome_progress.length === 0) && (
                  <tr>
                    <td colSpan={4} className="reports-outcome-empty">
                      No linked projects for this donor and financial year.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          <div className="reports-doc-section">
            <h5>Our Impact Highlights</h5>
            <div className="reports-highlight-tiles">
              <div className="reports-highlight-tile">
                <strong>{formatCompact(c?.impact_highlights?.beneficiaries_total)}</strong>
                <span>Beneficiaries</span>
              </div>
              <div className="reports-highlight-tile">
                <strong>{c?.impact_highlights?.project_count ?? 0}</strong>
                <span>Projects</span>
              </div>
              <div className="reports-highlight-tile">
                <strong>{c?.impact_highlights?.spend_efficiency_pct ?? 0}%</strong>
                <span>Spend Efficiency</span>
              </div>
              <div className="reports-highlight-tile">
                <strong>{c?.impact_highlights?.locations_covered ?? 0}</strong>
                <span>Locations Covered</span>
              </div>
            </div>
          </div>

          <div className="reports-doc-section reports-doc-columns">
            <div>
              <h5>Funds Summary</h5>
              <div className="reports-funds-summary">
                <div className="reports-donut-wrapper">
                  <ResponsiveContainer width={140} height={140}>
                    <PieChart>
                      <Pie
                        data={[
                          { name: "Utilized", value: c?.funds_summary?.utilized || 0, color: "#16a34a" },
                          { name: "Balance", value: c?.funds_summary?.balance || 0, color: "#a7f3d0" },
                          { name: "Pending receipt", value: c?.funds_summary?.pending_receipt || 0, color: "#e2e8f0" },
                        ]}
                        innerRadius={42}
                        outerRadius={62}
                        dataKey="value"
                      >
                        {["Utilized", "Balance", "Pending receipt"].map((name, i) => (
                          <Cell key={name} fill={["#16a34a", "#a7f3d0", "#e2e8f0"][i]} />
                        ))}
                      </Pie>
                    </PieChart>
                  </ResponsiveContainer>
                  <div className="reports-donut-center">
                    <strong>{c?.funds_summary?.utilization_pct ?? 0}%</strong>
                    <span>Utilised</span>
                  </div>
                </div>
                <div className="reports-funds-details">
                  <p className="reports-funds-total">
                    Total Received
                    <strong>{formatCr(c?.funds_summary?.received)}</strong>
                  </p>
                  <div className="reports-funds-row">
                    <span className="reports-legend-dot" style={{ background: "#16a34a" }} />
                    Utilized <strong>{formatCr(c?.funds_summary?.utilized)}</strong>
                  </div>
                  <div className="reports-funds-row">
                    <span className="reports-legend-dot" style={{ background: "#a7f3d0" }} />
                    Balance <strong>{formatCr(c?.funds_summary?.balance)}</strong>
                  </div>
                  <div className="reports-funds-row">
                    <span className="reports-legend-dot" style={{ background: "#e2e8f0" }} />
                    Pending receipt <strong>{formatCr(c?.funds_summary?.pending_receipt)}</strong>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h5>Impact Across Focus Areas</h5>
              <div className="reports-funds-summary">
                <div className="reports-donut-wrapper">
                  <ResponsiveContainer width={140} height={140}>
                    <PieChart>
                      <Pie
                        data={c?.impact_by_focus_area || []}
                        innerRadius={42}
                        outerRadius={62}
                        dataKey="beneficiaries"
                      >
                        {(c?.impact_by_focus_area || []).map((item, i) => (
                          <Cell key={item.name} fill={FOCUS_AREA_COLORS[i % FOCUS_AREA_COLORS.length]} />
                        ))}
                      </Pie>
                    </PieChart>
                  </ResponsiveContainer>
                  <div className="reports-donut-center">
                    <strong>{formatCompact(c?.impact_highlights?.beneficiaries_total)}</strong>
                    <span>Total Impacted</span>
                  </div>
                </div>
                <div className="reports-funds-details">
                  {(c?.impact_by_focus_area || []).map((item, i) => (
                    <div className="reports-funds-row" key={item.name}>
                      <span
                        className="reports-legend-dot"
                        style={{ background: FOCUS_AREA_COLORS[i % FOCUS_AREA_COLORS.length] }}
                      />
                      {item.name}
                      <strong>
                        {item.pct}% ({item.beneficiaries.toLocaleString("en-IN")})
                      </strong>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
