import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import { ArrowLeft, Sparkles, Loader2 } from "lucide-react";

import { getDonors } from "../services/donorService";
import { previewReport, generateReport } from "../services/reportService";

import "../styles/dashboard.css";
import "../styles/reports.css";

const FINANCIAL_YEARS = ["2023-24", "2024-25", "2025-26", "2026-27"];

const formatCr = (value) => {
  const n = Number(value || 0);
  if (n >= 1e7) return `₹${(n / 1e7).toFixed(2)} Cr`;
  if (n >= 1e5) return `₹${(n / 1e5).toFixed(1)} L`;
  return `₹${n.toLocaleString("en-IN")}`;
};

export default function GenerateReport() {
  const navigate = useNavigate();
  const [donorId, setDonorId] = useState("");
  const [financialYear, setFinancialYear] = useState("");

  const { data: donors = [] } = useQuery({
    queryKey: ["donors"],
    queryFn: getDonors,
  });

  const { data: preview, isFetching: previewLoading } = useQuery({
    queryKey: ["report-preview", donorId, financialYear],
    queryFn: () => previewReport(donorId, financialYear),
    enabled: !!donorId && !!financialYear,
  });

  const generateMutation = useMutation({
    mutationFn: () => generateReport(donorId, financialYear),
    onSuccess: (report) => navigate(`/reports/${report.id}`),
  });

  const selectedDonor = donors.find((d) => String(d.id) === String(donorId));

  return (
    <div className="dashboard reports-page">
      <button className="reports-back-link" onClick={() => navigate("/reports")}>
        <ArrowLeft size={15} />
        Back to reports
      </button>

      <div className="reports-generate-banner">
        <span className="reports-generate-banner-label">
          <Sparkles size={13} />
          NEW ANNUAL REPORT
        </span>
        <h4>Generate a report with AI</h4>
      </div>

      <p className="reports-generate-hint">
        Pick a donor and financial year — the AI engine pulls every linked project automatically.
      </p>

      <div className="reports-generate-form">
        <div className="reports-field">
          <label>Donor</label>
          <select value={donorId} onChange={(e) => setDonorId(e.target.value)}>
            <option value="">Select a donor…</option>
            {donors.map((d) => (
              <option key={d.id} value={d.id}>
                {d.name}
              </option>
            ))}
          </select>
        </div>

        <div className="reports-field">
          <label>Financial year</label>
          <select value={financialYear} onChange={(e) => setFinancialYear(e.target.value)}>
            <option value="">Select a year…</option>
            {FINANCIAL_YEARS.map((fy) => (
              <option key={fy} value={fy}>
                FY {fy}
              </option>
            ))}
          </select>
        </div>
      </div>

      {donorId && financialYear && (
        <div className="reports-preview-card">
          {previewLoading ? (
            <p className="reports-preview-loading">
              <Loader2 size={14} className="reports-spin" />
              Checking linked projects…
            </p>
          ) : (
            <>
              <div className="reports-preview-header">
                <strong>{selectedDonor?.name}</strong>
              </div>
              <p>
                {preview?.linked_projects ?? 0} linked project
                {preview?.linked_projects === 1 ? "" : "s"} ·{" "}
                <strong>{formatCr(preview?.committed)}</strong> committed for FY {financialYear}
              </p>
            </>
          )}

          <button
            className="reports-generate-submit"
            disabled={generateMutation.isPending}
            onClick={() => generateMutation.mutate()}
          >
            {generateMutation.isPending ? (
              <>
                <Loader2 size={15} className="reports-spin" />
                Generating…
              </>
            ) : (
              <>
                <Sparkles size={15} />
                Generate Report
              </>
            )}
          </button>

          {generateMutation.isError && (
            <p className="reports-generate-error">
              Something went wrong generating the report. Please try again.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
