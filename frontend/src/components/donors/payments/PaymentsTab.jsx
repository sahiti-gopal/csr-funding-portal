import { useEffect, useMemo, useState } from "react";
import axios from "axios";

import PaymentKPIs from "./PaymentKPIs";
import PaymentTimeline from "./PaymentTimeline";
import PaymentSchedule from "./PaymentSchedule";
import PaymentProof from "./PaymentProof";
import FundUtilization from "./FundUtilization";
import LinkedProjects from "./LinkedProjects";
import AIInsights from "./AIInsights";
import RecentActivity from "./RecentActivity";
import { formatCurrency } from "../../../utils/format";

import "../../../styles/payments.css";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/api";

export default function PaymentsTab({ donor }) {

  const [loading, setLoading] = useState(true);

  const [paymentData, setPaymentData] = useState(null);

  //----------------------------------
  // Load Payments
  //----------------------------------

  const loadPayments = async (donorId) => {

  try {

    setLoading(true);

    const url =
      `${API}/donors/${donorId}/payments`;

    const res = await axios.get(url);

    setPaymentData(res.data);

  } catch (err) {

    console.error(err);

  } finally {

    setLoading(false);

  }

};

  //----------------------------------
  // Donor Changed
  //----------------------------------

  useEffect(() => {

  if (!donor) return;

  loadPayments(donor.id);

}, [donor]);

  //----------------------------------
  // KPI Cards
  //----------------------------------

  const kpis = useMemo(() => {

    if (!paymentData)
      return [];

    const d =
      paymentData.kpis;

    return [

      {
        title: "Total Committed",
        value: formatCurrency(d.totalCommitted),
      },

      {
        title: "Funds Received",
        value: formatCurrency(d.totalReceived),
      },

      {
        title: "Pending",
        value: formatCurrency(d.pendingDisbursement),
      },

      {
        title: "Current FY",
        value: formatCurrency(d.currentFYContribution),
      },

      {
        title: "Utilized",
        value: formatCurrency(d.totalUtilized),
      },

      {
        title: "Balance",
        value: formatCurrency(d.remainingBalance),
      },

    ];

  }, [

    paymentData,

  ]);

  //----------------------------------
  // Loading
  //----------------------------------

  if (loading) {
    return (
      <div className="payments-loading">
        Loading payment information...
      </div>
    );
  }

  //----------------------------------
  // Empty
  //----------------------------------

  if (!paymentData) {
    return (
      <div className="payments-error">
        No payment information available.
      </div>
    );
  }

  //----------------------------------
  // Render
  //----------------------------------

  return (

    <div className="payments-page">

      <PaymentKPIs
        data={kpis}
      />

      <PaymentTimeline
        data={paymentData.timeline}
      />

      <PaymentSchedule
        rows={paymentData.schedule}
      />

      <PaymentProof
        proofs={paymentData.documents}
        onRefresh={() => loadPayments(donor.id)}
      />

      <FundUtilization
        projects={paymentData.projects}
      />

      <LinkedProjects
        projects={paymentData.projects}
      />

      <AIInsights
        insights={paymentData.aiInsights}
      />

      <RecentActivity
        data={paymentData.activity}
      />

    </div>

  );

}
