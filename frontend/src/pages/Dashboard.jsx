import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import axios from "axios";
import {
  Sparkles,
  TriangleAlert,
  FileText,
  Shield,
  CheckCircle,
  Target,
} from "lucide-react";

import OverviewCards from "../components/dashboard/OverviewCards";
import RiskCard from "../components/dashboard/RiskCard";
import SDGImpact from "../components/dashboard/SDGImpact";

import { getDonor, getDonorAiSummary } from "../services/donorService";
import { formatCurrency, formatCount } from "../utils/format";

import "../styles/dashboard.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

const utilizationStatus = (pct) => {
  if (pct >= 85) return "Excellent";
  if (pct >= 65) return "On Track";
  if (pct >= 40) return "In Progress";
  return "Needs Attention";
};

const formatFunds = formatCurrency;

const RISK_ICONS = {
  file: FileText,
  shield: Shield,
  check: CheckCircle,
};

const decorateRisk = (risk) => ({
  ...risk,
  icon:
    RISK_ICONS[risk.icon] ??
    FileText,
  timeLeft: risk.time_left,
});

export default function Dashboard() {
  const navigate = useNavigate();

  const [searchParams] = useSearchParams();

  const filters = {
    region: searchParams.get("region") || "all",
    fy: searchParams.get("fy") || "all",
  };

  const [globalStats, setGlobalStats] =
    useState([]);

  const [fundedSdgIds, setFundedSdgIds] =
    useState([]);

  const [sdgImpactDetails, setSdgImpactDetails] =
    useState({});

  const [aiSummary, setAiSummary] = useState(null);
  const [loadingAiSummary, setLoadingAiSummary] = useState(true);

  const [donorsList, setDonorsList] = useState([]);
  const [selectedDonorId, setSelectedDonorId] = useState("");
  const [donorDetail, setDonorDetail] = useState(null);
  const [donorAiSummary, setDonorAiSummary] = useState(null);
  const [loadingDonorAi, setLoadingDonorAi] = useState(false);

  const selectedDonorName = donorDetail?.name ?? "";

  const [risks, setRisks] =
    useState([]);

  useEffect(() => {
    axios
      .get(
        `${API}/dashboard/summary`,
        {
          params: {
            region: filters.region,
            fy: filters.fy,
          },
        }
      )
      .then((res) => {
        const d = res.data;

        setFundedSdgIds(d.funded_sdg_ids ?? []);
        setSdgImpactDetails(d.sdg_impact_details ?? {});

        setGlobalStats([
          {
            title: "Raised",
            value: formatFunds(d.raised_amount),
            subtitle: `${d.sponsors} sponsors`,
          },
          {
            title: "Utilized",
            value: formatFunds(d.utilized_amount),
            subtitle: "of funds raised",
            percent: d.utilization_pct,
            status: utilizationStatus(d.utilization_pct),
          },
          {
            title: "Projects",
            value: d.funded,
            subtitle: "funded",
          },
          {
            title: "Beneficiaries",
            value: formatCount(d.beneficiaries),
            subtitle: "reached",
          },
        ]);
      })
      .catch(console.error);
  }, [filters.region, filters.fy]);

  useEffect(() => {
    axios
      .get(`${API}/donors`, {
        params: { region: filters.region },
      })
      .then((res) => setDonorsList(res.data ?? []))
      .catch(console.error);
  }, [filters.region]);

  useEffect(() => {
    // Clear the selection if the donor drops out of the list (e.g. after a
    // region change) so the KPI cards/AI summary don't get stuck on stale data.
    if (
      selectedDonorId &&
      donorsList.length &&
      !donorsList.some((d) => String(d.id) === String(selectedDonorId))
    ) {
      setSelectedDonorId("");
    }
  }, [donorsList, selectedDonorId]);

  useEffect(() => {
    if (!selectedDonorId) {
      setDonorDetail(null);
      setDonorAiSummary(null);
      return;
    }

    setLoadingDonorAi(true);

    Promise.all([
      getDonor(selectedDonorId),
      getDonorAiSummary(selectedDonorId),
    ])
      .then(([detail, ai]) => {
        setDonorDetail(detail);
        setDonorAiSummary(ai);
      })
      .catch(console.error)
      .finally(() => setLoadingDonorAi(false));
  }, [selectedDonorId]);

  const stats = selectedDonorId && donorDetail
    ? [
        {
          title: "Raised",
          value: formatFunds(donorDetail.raised_total),
          subtitle: donorDetail.focus_area,
        },
        {
          title: "Utilized",
          value: formatFunds(donorDetail.utilized_total),
          subtitle: "of funds raised",
          percent: donorDetail.utilization_pct,
          status: utilizationStatus(donorDetail.utilization_pct),
        },
        {
          title: "Projects",
          value: donorDetail.projects_total,
          subtitle: "total",
        },
        {
          title: "Beneficiaries",
          value: formatCount(donorDetail.beneficiaries_total),
          subtitle: "reached",
        },
      ]
    : globalStats;

  useEffect(() => {
    setLoadingAiSummary(true);

    axios
      .get(
        `${API}/dashboard/ai-summary`,
        {
          params: {
            region: filters.region,
            fy: filters.fy,
          },
        }
      )
      .then((res) => {
        setAiSummary(res.data);
      })
      .catch(console.error)
      .finally(() => setLoadingAiSummary(false));
  }, [filters.region, filters.fy]);

  useEffect(() => {
    axios
      .get(
        `${API}/risks`
      )
      .then((res) => {
        setRisks(
          res.data.map(
            decorateRisk
          )
        );
      })
      .catch(console.error);
  }, [filters.region]);

  return (
  <div className="dashboard">

    <div className="dashboard-head">
      <div className="dashboard-title">
        <span className="eyebrow">Funding &amp; impact</span>
        <h4 className="section-heading">Portfolio overview</h4>
      </div>
    </div>

    {/* ---------------- SDG Impact (full width) ---------------- */}

    <div className="sdg-band">

      <div className="sdg-band-head">
        <h3 className="dash-heading">
          <Target size={20} className="panel-title-icon icon-green" />
          SDG impact
        </h3>

        <span className="sdg-band-count">
          {fundedSdgIds.length} of 17 goals actively funded this FY
        </span>
      </div>

      <SDGImpact fundedIds={fundedSdgIds} impactByGoal={sdgImpactDetails} />

    </div>

    {/* ---------------- KPI Cards ---------------- */}

    <OverviewCards
      stats={stats}
      activeCard={null}
      onCardClick={() => navigate("/projects")}
    />

    {/* ---------------- Donor + Risks ---------------- */}

    <div className="dashboard-content">

      <div className="overview-row2">

        <div className="panel ai-summary-panel">

          <h3 className="panel-title">

            <Sparkles
              size={20}
              className="panel-title-icon icon-blue"
            />

            AI Summary

            <select
              className="ai-summary-donor-select"
              value={selectedDonorId}
              onChange={(e) => setSelectedDonorId(e.target.value)}
            >
              <option value="">All Companies</option>
              {donorsList.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name}
                </option>
              ))}
            </select>

          </h3>

          <div className="panel-body ai-summary-body">

            {selectedDonorId ? (

              loadingDonorAi ? (
                <div className="ai-summary-skeleton" />
              ) : (
                <>
                  <div className="ai-summary-section">
                    <span className="ai-summary-section-title">Engagement</span>
                    <p>{donorAiSummary?.engagement_summary}</p>
                  </div>

                  <div className="ai-summary-section">
                    <span className="ai-summary-section-title">Key Risks</span>
                    <ul className="ai-summary-risk-list">
                      {donorAiSummary?.key_risks?.map((risk, i) => (
                        <li key={i}>{risk}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="ai-summary-section">
                    <span className="ai-summary-section-title">Project Health</span>
                    <p>{donorAiSummary?.project_health_summary}</p>
                  </div>

                  <div className="ai-summary-attribution">
                    <Sparkles size={12} />
                    {donorAiSummary?.ai_generated
                      ? `Generated by AI from ${selectedDonorName}'s data.`
                      : "Computed summary (AI generation unavailable)."}
                  </div>
                </>
              )

            ) : loadingAiSummary ? (
              <div className="ai-summary-skeleton" />
            ) : (
              <>
                <p>{aiSummary?.summary}</p>

                <div className="ai-summary-attribution">
                  <Sparkles size={12} />
                  {aiSummary?.ai_generated
                    ? "Generated by AI from the current portfolio data."
                    : "Computed summary (AI generation unavailable)."}
                </div>
              </>
            )}

          </div>

        </div>

        <div className="panel risk-panel">

          <h3 className="panel-title">

            <TriangleAlert
              size={20}
              className="panel-title-icon icon-amber"
            />

            Upcoming Risks

            <span className="panel-count">{risks.length}</span>

          </h3>

          <div className="panel-scroll risk-list">

            {risks.map((risk) => (
              <RiskCard key={risk.id} {...risk} />
            ))}

          </div>

        </div>

      </div>

    </div>

  </div>
);
}
