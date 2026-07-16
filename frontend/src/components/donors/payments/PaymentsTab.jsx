import { useEffect, useMemo, useState } from "react";
import axios from "axios";

import PaymentHeader from "./PaymentHeader";
import PaymentToolbar from "./PaymentToolbar";
import PaymentKPIs from "./PaymentKPIs";
import PaymentTimeline from "./PaymentTimeline";
import PaymentSchedule from "./PaymentSchedule";
import PaymentProof from "./PaymentProof";
import FundUtilization from "./FundUtilization";
import LinkedProjects from "./LinkedProjects";
import AIInsights from "./AIInsights";
import RecentActivity from "./RecentActivity";

import "../../../styles/payments.css";

const API = "http://127.0.0.1:5000/api";

export default function PaymentsTab() {

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const [donors, setDonors] = useState([]);

  const [selectedDonor, setSelectedDonor] = useState(null);

  const [paymentData, setPaymentData] = useState(null);

  const [search, setSearch] = useState("");

  const [statusFilter, setStatusFilter] = useState("All");

  const [fyFilter, setFyFilter] = useState("All");

  //----------------------------------
  // Currency Formatter
  //----------------------------------

  const formatCurrency = (value) => {

    const amount = Number(value || 0);

    return new Intl.NumberFormat(
      "en-IN",
      {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0,
      }
    ).format(amount);

  };

  //----------------------------------
  // Load Donors
  //----------------------------------

  const loadDonors = async () => {

  try {

    const res = await axios.get(`${API}/donors`);

    setDonors(res.data);

    if (res.data.length > 0) {

      console.log("Loaded donors", res.data);

      setSelectedDonor(res.data[0]);

    }

  } catch (err) {

    console.error(err);

  }

};
  //----------------------------------
  // Load Payments
  //----------------------------------

  const loadPayments = async (donorId) => {

  console.log("Loading donor id:", donorId);

  try {

    setLoading(true);

    const url =
      `${API}/donors/${donorId}/payments`;

    console.log(url);

    const res = await axios.get(url);

    setPaymentData(res.data);

  } catch (err) {

    console.error(err);

  } finally {

    setLoading(false);

  }

};

  //----------------------------------
  // Initial Load
  //----------------------------------

  useEffect(() => {

    loadDonors();

  }, []);

  //----------------------------------
  // Donor Changed
  //----------------------------------

  useEffect(() => {

  if (!selectedDonor) return;

  console.log(
    "Selected donor:",
    selectedDonor.id,
    selectedDonor.name
  );

  loadPayments(selectedDonor.id);

}, [selectedDonor]);
    //----------------------------------
  // Filter Schedule
  //----------------------------------

  const filteredSchedule = useMemo(() => {

    if (!paymentData)
      return [];

    return paymentData.schedule.filter((row) => {

      const searchText =
        search.trim().toLowerCase();

      const installment =
        (row.installment || "").toLowerCase();

      const transaction =
        (row.transactionId || "").toLowerCase();

      const paymentMode =
        (row.paymentMode || "").toLowerCase();

      const status =
        (row.status || "").trim().toLowerCase();

      const dueDate =
        row.due || "";

      const year =
        dueDate
          ? new Date(dueDate)
              .getFullYear()
              .toString()
          : "";

      const matchesSearch =

        !search ||

        installment.includes(searchText) ||

        transaction.includes(searchText) ||

        paymentMode.includes(searchText) ||

        status.includes(searchText);

      const matchesStatus =

        statusFilter === "All" ||

        status ===
          statusFilter.toLowerCase();

      const matchesFY =

        fyFilter === "All" ||

        year === fyFilter;

      return (

        matchesSearch &&

        matchesStatus &&

        matchesFY

      );

    });

  }, [

    paymentData,

    search,

    statusFilter,

    fyFilter,

  ]);

  //----------------------------------
  // Timeline
  //----------------------------------

  const filteredTimeline = useMemo(() => {

    if (!paymentData)
      return [];

    return paymentData.timeline.filter(
      (item) => {

        if (!search)
          return true;

        return item.title
          ?.toLowerCase()
          .includes(
            search.toLowerCase()
          );

      }
    );

  }, [

    paymentData,

    search,

  ]);

  //----------------------------------
  // Documents
  //----------------------------------

  const filteredDocuments = useMemo(() => {

    if (!paymentData)
      return [];

    return paymentData.documents.filter(
      (payment) => {

        if (!search)
          return true;

        return (

          payment.installment
            ?.toLowerCase()
            .includes(
              search.toLowerCase()
            ) ||

          payment.documents.some(
            (doc) =>

              doc.name
                ?.toLowerCase()
                .includes(
                  search.toLowerCase()
                )
          )

        );

      }
    );

  }, [

    paymentData,

    search,

  ]);

  //----------------------------------
  // Projects
  //----------------------------------

  const filteredProjects = useMemo(() => {

    if (!paymentData)
      return [];

    return paymentData.projects.filter(
      (project) => {

        if (!search)
          return true;

        return (

          project.name
            ?.toLowerCase()
            .includes(
              search.toLowerCase()
            ) ||

          (project.location || "")
            .toLowerCase()
            .includes(
              search.toLowerCase()
            )

        );

      }
    );

  }, [

    paymentData,

    search,

  ]);

  //----------------------------------
  // AI Insights
  //----------------------------------

  const filteredInsights = useMemo(() => {

    if (!paymentData)
      return [];

    return paymentData.aiInsights.filter(
      (item) => {

        if (!search)
          return true;

        return (

          item.title
            ?.toLowerCase()
            .includes(search.toLowerCase()) ||

          item.description
            ?.toLowerCase()
            .includes(search.toLowerCase())

        );

      }
    );

  }, [

    paymentData,

    search,

  ]);

  //----------------------------------
  // Activity
  //----------------------------------

  const filteredActivity = useMemo(() => {

    if (!paymentData)
      return [];

    return paymentData.activity.filter(
      (item) => {

        if (!search)
          return true;

        return item.title
          ?.toLowerCase()
          .includes(
            search.toLowerCase()
          );

      }
    );

  }, [

    paymentData,

    search,

  ]);

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
        color: "#111827",
      },

      {
        title: "Funds Received",
        value: formatCurrency(d.totalReceived),
        color: "#16A34A",
      },

      {
        title: "Pending",
        value: formatCurrency(d.pendingDisbursement),
        color: "#F59E0B",
      },

      {
        title: "Current FY",
        value: formatCurrency(d.currentFYContribution),
        color: "#2563EB",
      },

      {
        title: "Utilized",
        value: formatCurrency(d.totalUtilized),
        color: "#0EA5E9",
      },

      {
        title: "Balance",
        value: formatCurrency(d.remainingBalance),
        color: "#7C3AED",
      },

    ];

  }, [

    paymentData,

  ]);

  //----------------------------------
  // Refresh
  //----------------------------------

  const refresh = () => {

    if (!selectedDonor)
      return;

    loadPayments(
      selectedDonor.id
    );

  };

  //----------------------------------
  // Download CSV
  //----------------------------------

  const downloadStatement = () => {

    if (!filteredSchedule.length)
      return;

    const csv = [

      [
        "Installment",
        "Amount",
        "Due Date",
        "Received",
        "Status",
      ],

      ...filteredSchedule.map(
        (row) => [

          row.installment,

          row.amount,

          row.due,

          row.received,

          row.status,

        ]
      ),

    ];

    const blob = new Blob(

      [
        csv
          .map(
            (r) => r.join(",")
          )
          .join("\n"),
      ],

      {
        type: "text/csv",
      }

    );

    const link =
      document.createElement("a");

    link.href =
      URL.createObjectURL(blob);

    link.download =
      `${selectedDonor.name}_Payments.csv`;

    link.click();

  };
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
  // Error
  //----------------------------------

  if (error) {
    return (
      <div className="payments-error">
        {error}
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

      <PaymentHeader
  donor={selectedDonor}
  donors={donors}
  onChange={(id) => {

    const donor = donors.find(
      (d) => d.id === Number(id)
    );

    console.log("Changed donor:", donor);

    setSelectedDonor(donor);

  }}
/>

      <PaymentToolbar

        search={search}
        onSearch={setSearch}

        statusFilter={statusFilter}
        setStatusFilter={setStatusFilter}

        fyFilter={fyFilter}
        setFyFilter={setFyFilter}

        onRefresh={refresh}

        onDownload={downloadStatement}

      />

      <PaymentKPIs
        data={kpis}
      />

      <PaymentTimeline
        data={filteredTimeline}
      />

      <PaymentSchedule
        rows={filteredSchedule}
      />

      <PaymentProof
        proofs={filteredDocuments}
      />

      <FundUtilization
        projects={filteredProjects}
      />

      <LinkedProjects
        projects={filteredProjects}
      />

      <AIInsights
        insights={filteredInsights}
      />

      <RecentActivity
        data={filteredActivity}
      />

    </div>

  );

}