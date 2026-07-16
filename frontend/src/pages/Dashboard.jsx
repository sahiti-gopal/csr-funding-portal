import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import {
  HeartHandshake,
  TriangleAlert,
  FileText,
  Shield,
  CheckCircle,
  IndianRupee,
  Wallet,
  FolderKanban,
  Users2,
} from "lucide-react";

import OverviewCards from "../components/dashboard/OverviewCards";
import DonorCard from "../components/dashboard/DonorCard";
import RiskCard from "../components/dashboard/RiskCard";
import SDGImpact from "../components/dashboard/SDGImpact";

import "../styles/dashboard.css";

const utilizationStatus = (pct) => {
  if (pct >= 85) return "Excellent";
  if (pct >= 65) return "On Track";
  if (pct >= 40) return "In Progress";
  return "Needs Attention";
};

const LIKELIHOOD_COLOR = (value) => {
  if (value >= 85) return "#16A34A";
  if (value >= 70) return "#D97706";
  return "#DC2626";
};

const CATEGORY_CLASSES = [
  "tag-blue",
  "tag-purple",
  "tag-green",
];

const categoryClass = (focusArea) => {
  let hash = 0;

  for (const char of focusArea ?? "") {
    hash =
      (hash + char.charCodeAt(0)) %
      CATEGORY_CLASSES.length;
  }

  return CATEGORY_CLASSES[hash];
};

const RISK_ICONS = {
  file: FileText,
  shield: Shield,
  check: CheckCircle,
};

const initials = (name = "") =>
  name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0])
    .join("")
    .toUpperCase();

const relativeTime = (dateStr) => {
  if (!dateStr) return "—";

  const days = Math.floor(
    (Date.now() -
      new Date(dateStr).getTime()) /
      (1000 * 60 * 60 * 24)
  );

  if (days <= 0) return "today";
  if (days === 1) return "1 day ago";
  if (days < 14) return `${days} days ago`;
  if (days < 60)
    return `${Math.floor(days / 7)} wks ago`;

  return `${Math.floor(days / 30)} mo ago`;
};

const decorateDonor = (donor) => ({
  donor: donor.name,
  initials: initials(donor.name),
  category: donor.focus_area,
  categoryClass: categoryClass(
    donor.focus_area
  ),
  likelihood: donor.likelihood,
  lastContact: relativeTime(
    donor.last_contact
  ),
  color: LIKELIHOOD_COLOR(
    donor.likelihood
  ),
});

const decorateRisk = (risk) => ({
  ...risk,
  icon:
    RISK_ICONS[risk.icon] ??
    FileText,
  timeLeft: risk.time_left,
});

export default function Dashboard() {
  const navigate = useNavigate();

  const [filters, setFilters] = useState({
    region: "all",
    fy: "all",
  });

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const [stats, setStats] =
    useState([]);

  const [donors, setDonors] =
    useState([]);

  const [risks, setRisks] =
    useState([]);

  // ---------- Risk panel scroll-linked fade ----------
  const riskScrollRef = useRef(null);
  const [riskAtBottom, setRiskAtBottom] = useState(false);

  const handleRiskScroll = () => {
    const el = riskScrollRef.current;
    if (!el) return;

    // Also treat "nothing to scroll" (content shorter than the panel) as at-bottom,
    // so the fade never shows over a fully-visible list.
    const atBottom =
      el.scrollHeight - el.scrollTop - el.clientHeight < 4;

    setRiskAtBottom(atBottom);
  };

  useEffect(() => {
    // Re-check once risks load / change, in case the list is short enough
    // to not need scrolling at all.
    handleRiskScroll();
  }, [risks]);

  useEffect(() => {
    axios
      .get(
        "http://localhost:5000/api/dashboard/summary",
        {
          params: {
            region: filters.region,
            fy: filters.fy,
          },
        }
      )
      .then((res) => {
        const d = res.data;

        setStats([
          {
            title: "Raised",
            value: `₹${(
              d.raised_amount /
              10000000
            ).toFixed(1)} Cr`,
            subtitle: `${d.sponsors} sponsors`,
            icon: IndianRupee,
            accent: "raised",
          },
          {
            title: "Utilized",
            value: `₹${(
              d.utilized_amount /
              10000000
            ).toFixed(1)} Cr`,
            subtitle: "of funds raised",
            icon: Wallet,
            accent: "utilized",
            percent: d.utilization_pct,
            status: utilizationStatus(d.utilization_pct),
          },
          {
            title: "Projects",
            value: d.funded,
            subtitle: "funded",
            icon: FolderKanban,
            accent: "projects",
          },
          {
            title: "Beneficiaries",
            value: (
              d.beneficiaries ?? 0
            ).toLocaleString(),
            subtitle: "reached",
            icon: Users2,
            accent: "beneficiaries",
          },
        ]);
      })
      .catch(console.error);
  }, [filters]);

  useEffect(() => {
    axios
      .get(
        "http://localhost:5000/api/donors",
        {
          params: {
            region:
              filters.region,
          },
        }
      )
      .then((res) => {
        setDonors(
          res.data.map(
            decorateDonor
          )
        );
      })
      .catch(console.error);

    axios
      .get(
        "http://localhost:5000/api/risks"
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
        <h4 className="section-heading">Portfolio overview</h4>
      </div>

      <div className="dashboard-filters">

        <select
          value={filters.region}
          onChange={(e) =>
            handleFilterChange(
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
            handleFilterChange(
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
    </div>

    {/* ---------------- KPI Cards ---------------- */}

    <OverviewCards
      stats={stats}
      activeCard={null}
      onCardClick={() => navigate("/projects")}
    />

    {/* ---------------- Main Dashboard ---------------- */}

    <div className="dashboard-content">

      <div className="dashboard-grid">

        {/* ================= LEFT COLUMN ================= */}

        <div className="dashboard-left">

          {/* ---------- Donor Outreach ---------- */}

          <div className="panel donor-panel">

            <h3 className="panel-title">

              <HeartHandshake
                size={20}
                className="panel-title-icon icon-blue"
              />

              Donor Outreach Readiness

              <span className="panel-count">{donors.length}</span>

            </h3>

            <div className="panel-scroll">

              {donors.map((donor) => (

                <DonorCard
                  key={donor.donor}
                  {...donor}
                />

              ))}

            </div>

          </div>

          {/* ---------- SDG Impact ---------- */}

          <div className="panel sdg-panel">

            <h3 className="panel-title">

              🌍 SDG Impact

              <span className="panel-count">17</span>

            </h3>

            <div className="panel-body">

              <SDGImpact />

            </div>

          </div>

        </div>

        {/* ================= RIGHT COLUMN ================= */}

        <div className="dashboard-right">

          <div className={`panel risk-panel ${riskAtBottom ? "at-bottom" : ""}`}>

            <h3 className="panel-title">

              <TriangleAlert
                size={20}
                className="panel-title-icon icon-amber"
              />

              Upcoming Risks

              <span className="panel-count">{risks.length}</span>

            </h3>

            <div
              className="panel-scroll"
              ref={riskScrollRef}
              onScroll={handleRiskScroll}
            >

              {risks.map((risk) => (

                <RiskCard
                  key={risk.id}
                  {...risk}
                />

              ))}

            </div>

          </div>

        </div>

      </div>

    </div>

  </div>
);
}
