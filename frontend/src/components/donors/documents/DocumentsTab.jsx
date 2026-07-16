import { useState } from "react";

import DocumentStats from "./DocumentStats";
import DocumentList from "./DocumentList";
import AIRecommendation from "./AIRecommendation";
import UploadBanner from "./UploadBanner";
import DocumentCategory from "./DocumentCategory";

import "../../../styles/donorDocuments.css";

export default function DocumentsTab() {
  const [selectedDonor, setSelectedDonor] =
    useState("Wipro Cares");

  const stats = {
    required: 16,
    submitted: 10,
    pending: 2,
    missing: 3,
    compliance: 63,
  };

  const documents = [
    {
      id: 1,
      title: "Annual Report",
      due: "15 Jul",
      updated: "1 day ago",
      owner: "Meera",
      status: "Pending Review",
      severity: "Medium",
    },
    {
      id: 2,
      title: "CSR-1 Registration",
      due: "Required",
      updated: "Not Uploaded",
      owner: "",
      status: "Missing",
      severity: "Critical",
    },
  ];

  const categories = [
    {
      title: "Financial Documents",
      subtitle:
        "Tax certificates and audit filings",
      progress: 75,
      completed: "3/4",
      color: "#F97316",
    },
    {
      title: "Compliance Documents",
      subtitle:
        "Mandatory regulatory filings",
      progress: 25,
      completed: "1/4",
      color: "#7C3AED",
    },
    {
      title: "Legal Documents",
      subtitle:
        "Agreements and registrations",
      progress: 60,
      completed: "3/5",
      color: "#2563EB",
    },
    {
      title: "Impact Reports",
      subtitle:
        "Quarterly and annual impact reports",
      progress: 80,
      completed: "4/5",
      color: "#16A34A",
    },
  ];

  return (
    <div className="documents-page donor-tab-content">

     

      <DocumentStats stats={stats} />

      <div className="document-toolbar">

        <div className="toolbar-left">

          <span>
            Showing documents for
          </span>

          <select
            value={selectedDonor}
            onChange={(e) =>
              setSelectedDonor(
                e.target.value
              )
            }
          >
            <option>
              Wipro Cares
            </option>

            <option>
              Tata Trusts
            </option>

            <option>
              Infosys Foundation
            </option>

          </select>

        </div>

      </div>

      <DocumentList
        documents={documents}
      />

      <AIRecommendation />

      <UploadBanner />

      {categories.map((category) => (
        <DocumentCategory
          key={category.title}
          {...category}
        />
      ))}

    </div>
  );
}