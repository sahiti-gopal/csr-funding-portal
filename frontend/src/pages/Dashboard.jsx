import { useEffect, useState } from "react";
import { useNavigate, useOutletContext } from "react-router-dom";
import axios from "axios";
import {
  HeartHandshake,
  TriangleAlert,
  FileText,
  Shield,
  CheckCircle,
} from "lucide-react";

import OverviewCards from "../components/dashboard/OverviewCards";
import DonorCard from "../components/dashboard/DonorCard";
import RiskCard from "../components/dashboard/RiskCard";
import SDGImpact from "../components/dashboard/SDGImpact";

import "../styles/dashboard.css";

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

  const { filters } = useOutletContext();

  const [stats, setStats] =
    useState([]);

  const [donors, setDonors] =
    useState([]);

  const [risks, setRisks] =
    useState([]);

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
          },
          {
            title: "Utilized",
            value: `₹${(
              d.utilized_amount /
              10000000
            ).toFixed(1)} Cr`,
            subtitle: `${d.utilization_pct}% utilization`,
          },
          {
            title: "Projects",
            value: d.funded,
            subtitle: "funded",
          },
          {
            title: "Beneficiaries",
            value: (
              d.beneficiaries ?? 0
            ).toLocaleString(),
            subtitle: "reached",
          },
          {
            title: "Registered",
            value: d.registered,
            subtitle: "projects",
          },
          {
            title: "Completed",
            value: d.completed,
            subtitle: "projects",
          },
          {
            title:
              "Needs Attention",
            value:
              d.needs_attention,
            subtitle: "projects",
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

            </h3>

            <div className="panel-body">

              <SDGImpact />

            </div>

          </div>

        </div>

        {/* ================= RIGHT COLUMN ================= */}

        <div className="dashboard-right">

          <div className="panel risk-panel">

            <h3 className="panel-title">

              <TriangleAlert
                size={20}
                className="panel-title-icon icon-amber"
              />

              Upcoming Risks

            </h3>

            <div className="panel-scroll">

              {risks.map((risk) => (

                <RiskCard
                  key={risk.title}
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