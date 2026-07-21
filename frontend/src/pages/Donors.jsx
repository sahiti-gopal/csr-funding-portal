import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import DonorOverview from "../components/donors/DonorOverview";
import DonorCharts from "../components/donors/DonorCharts";
import DonorCard from "../components/donors/DonorCard";

import DocumentsTab from "../components/donors/documents/DocumentsTab";
import PaymentsTab from "../components/donors/payments/PaymentsTab";
import PaymentHeader from "../components/donors/payments/PaymentHeader";

import "../styles/dashboard.css";
import "../styles/donors.css";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/api";

const getColor = (score) => {
  if (score >= 85) return "#16A34A";
  if (score >= 70) return "#F59E0B";
  return "#2563EB";
};

export default function Donors() {
  const navigate = useNavigate();

  const [activeTab, setActiveTab] =
    useState("overview");

  const [donors, setDonors] = useState([]);
  const [loading, setLoading] =
    useState(true);

  const [search, setSearch] =
    useState("");

  const [focusArea, setFocusArea] =
    useState("All");

  const [likelihood, setLikelihood] =
    useState("All");

  const [selectedPaymentDonor, setSelectedPaymentDonor] =
    useState(null);

  useEffect(() => {
    if (!selectedPaymentDonor && donors.length > 0) {
      setSelectedPaymentDonor(donors[0]);
    }
  }, [donors, selectedPaymentDonor]);

  const loadDonors = async () => {
    try {
      setLoading(true);

      const res = await axios.get(
        `${API}/donors`
      );

      setDonors(res.data ?? []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDonors();
  }, []);

  const filteredDonors = useMemo(() => {
    return donors.filter((d) => {
      const matchSearch =
        d.name
          ?.toLowerCase()
          .includes(search.toLowerCase());

      const matchFocus =
        focusArea === "All"
          ? true
          : d.focus_area === focusArea;

      const matchLikelihood =
        likelihood === "All"
          ? true
          : likelihood === "High"
          ? d.likelihood >= 85
          : likelihood === "Medium"
          ? d.likelihood >= 70 &&
            d.likelihood < 85
          : d.likelihood < 70;

      return (
        matchSearch &&
        matchFocus &&
        matchLikelihood
      );
    });
  }, [
    donors,
    search,
    focusArea,
    likelihood,
  ]);

  const summary = {
    atRisk: donors.filter(
      (d) => d.likelihood < 70
    ).length,

    attention: donors.filter(
      (d) =>
        d.likelihood >= 70 &&
        d.likelihood < 85
    ).length,

    healthy: donors.filter(
      (d) => d.likelihood >= 85
    ).length,

    atRiskAmount: "₹2.0 Cr",

    attentionAmount: "₹5.0 Cr",

    healthyAmount: "₹14.2 Cr",
  };

  return (
    <div className="donors-page">

      <div className="dashboard-head">

        <div className="dashboard-title">

          <span className="eyebrow">Relationships</span>

          <h4 className="section-heading">Donors</h4>

        </div>

      </div>

      <div className="donor-tabs-row">

        <div className="donor-tabs">

          <button
            className={
              activeTab === "overview"
                ? "active"
                : ""
            }
            onClick={() =>
              setActiveTab("overview")
            }
          >
            Donor Overview
          </button>

          <button
            className={
              activeTab === "documents"
                ? "active"
                : ""
            }
            onClick={() =>
              setActiveTab("documents")
            }
          >
            Documents
          </button>

          <button
            className={
              activeTab === "payments"
                ? "active"
                : ""
            }
            onClick={() =>
              setActiveTab("payments")
            }
          >
            Payments
          </button>

        </div>

        {activeTab === "payments" && (

          <PaymentHeader
            donor={selectedPaymentDonor}
            donors={donors}
            onChange={(id) => {
              const donor = donors.find(
                (d) => d.id === Number(id)
              );

              setSelectedPaymentDonor(donor);
            }}
          />

        )}

      </div>

      <div className="donors-scroll">

      {activeTab === "overview" && (
        <>

          <DonorOverview summary={summary} />

          <div className="donors-chart-wrapper">

            <DonorCharts donors={donors} />

          </div>

          <div className="donor-toolbar">

            <div className="toolbar-left">

              <input
                className="donor-search"
                type="text"
                placeholder="Search donors..."
                value={search}
                onChange={(e) =>
                  setSearch(e.target.value)
                }
              />

            </div>

            <div className="toolbar-right">

              <select
                value={focusArea}
                onChange={(e) =>
                  setFocusArea(e.target.value)
                }
              >

                <option value="All">
                  All Focus Areas
                </option>

                {[
                  ...new Set(
                    donors.map(
                      (d) => d.focus_area
                    )
                  ),
                ].map((area) => (

                  <option
                    key={area}
                    value={area}
                  >
                    {area}
                  </option>

                ))}

              </select>

              <select
                value={likelihood}
                onChange={(e) =>
                  setLikelihood(
                    e.target.value
                  )
                }
              >

                <option value="All">
                  All Scores
                </option>

                <option value="High">
                  High (85%+)
                </option>

                <option value="Medium">
                  Medium (70–84%)
                </option>

                <option value="Low">
                  Low (&lt;70%)
                </option>

              </select>

            </div>

          </div>

          <div className="donors-list">

            {loading ? (

              <div className="loading-card">

                Loading donors...

              </div>

            ) : filteredDonors.length === 0 ? (

              <div className="loading-card">

                No donors found.

              </div>

            ) : (

              filteredDonors.map((donor) => (

                <DonorCard
                  key={donor.id}
                  donor={donor.name}
                  category={
                    donor.focus_area
                  }
                  likelihood={
                    donor.likelihood
                  }
                  lastContact={
                    donor.last_contact
                  }
                  color={getColor(
                    donor.likelihood
                  )}
                  onClick={() =>
                    navigate(`/donors/${donor.id}`)
                  }
                />

              ))

            )}

          </div>

          <div className="donors-bottom">

            <div className="summary-card">

              <h3>
                Pipeline Summary
              </h3>

              <div className="summary-row">

                <span>
                  Total Donors
                </span>

                <strong>
                  {donors.length}
                </strong>

              </div>

              <div className="summary-row">

                <span>
                  Healthy
                </span>

                <strong>

                  {
                    donors.filter(
                      (d) =>
                        d.likelihood >=
                        85
                    ).length
                  }

                </strong>

              </div>

              <div className="summary-row">

                <span>
                  Needs Attention
                </span>

                <strong>

                  {
                    donors.filter(
                      (d) =>
                        d.likelihood >=
                          70 &&
                        d.likelihood <
                          85
                    ).length
                  }

                </strong>

              </div>

              <div className="summary-row">

                <span>
                  At Risk
                </span>

                <strong>

                  {
                    donors.filter(
                      (d) =>
                        d.likelihood <
                        70
                    ).length
                  }

                </strong>

              </div>

            </div>
                        <div className="summary-card">

              <h3>Quick Insights</h3>

              <div className="insight-item">

                <span>Highest Match</span>

                <strong>

                  {Math.max(
                    ...donors.map(
                      (d) => d.likelihood
                    ),
                    0
                  )}
                  %

                </strong>

              </div>

              <div className="insight-item">

                <span>Average Match</span>

                <strong>

                  {donors.length
                    ? Math.round(
                        donors.reduce(
                          (sum, d) =>
                            sum +
                            d.likelihood,
                          0
                        ) / donors.length
                      )
                    : 0}
                  %

                </strong>

              </div>

              <div className="insight-item">

                <span>Focus Areas</span>

                <strong>

                  {
                    new Set(
                      donors.map(
                        (d) =>
                          d.focus_area
                      )
                    ).size
                  }

                </strong>

              </div>

              <div className="insight-item">

                <span>
                  Ready to Contact
                </span>

                <strong>

                  {
                    donors.filter(
                      (d) =>
                        d.status ===
                        "Ready"
                    ).length
                  }

                </strong>

              </div>

            </div>

          </div>

        </>

      )}

      {activeTab === "documents" && (

        <DocumentsTab />

      )}

      {activeTab === "payments" && (

        <PaymentsTab donor={selectedPaymentDonor} />

      )}

      </div>

    </div>
  );
}