import { useEffect, useState } from "react";

import { getDonors } from "../../../services/donorService";
import {
  getDonorDocuments,
  uploadDonorDocument,
  reviewDonorDocument,
  generateDocumentRequest,
} from "../../../services/documentService";

import DocumentStats from "./DocumentStats";
import DocumentList from "./DocumentList";
import AIRecommendation from "./AIRecommendation";
import UploadBanner from "./UploadBanner";
import DocumentCategory from "./DocumentCategory";

import "../../../styles/donorDocuments.css";

export default function DocumentsTab() {
  const [donors, setDonors] = useState([]);
  const [selectedDonorId, setSelectedDonorId] = useState(null);

  const [stats, setStats] = useState({
    required: 0,
    submitted: 0,
    pending: 0,
    missing: 0,
    compliance: 0,
  });
  const [documents, setDocuments] = useState([]);
  const [categories, setCategories] = useState([]);
  const [recommendation, setRecommendation] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDonors().then((data) => {
      setDonors(data ?? []);
      if (data?.length) {
        setSelectedDonorId(data[0].id);
      }
    });
  }, []);

  const loadDocuments = async (donorId) => {
    setLoading(true);
    try {
      const data = await getDonorDocuments(donorId);
      setStats(data.stats);
      setDocuments(data.documents);
      setCategories(data.categories);
      setRecommendation(data.recommendation);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedDonorId) {
      loadDocuments(selectedDonorId);
    }
  }, [selectedDonorId]);

  const refresh = () => loadDocuments(selectedDonorId);

  const handleUpload = async (docId, file) => {
    await uploadDonorDocument(selectedDonorId, docId, file);
    refresh();
  };

  const handleReview = async (docId) => {
    await reviewDonorDocument(selectedDonorId, docId);
    refresh();
  };

  const handleGenerateRequest = async () => {
    await generateDocumentRequest(selectedDonorId);
    refresh();
  };

  const attentionDocuments = documents.filter(
    (doc) => doc.status !== "Verified"
  );

  const missingDocument = documents.find((doc) => !doc.fileUrl);

  return (
    <div className="documents-page donor-tab-content">

      <DocumentStats stats={stats} />

      <div className="document-toolbar">

        <div className="doc-toolbar-left">

          <span>
            Showing documents for
          </span>

          <select
            value={selectedDonorId ?? ""}
            onChange={(e) =>
              setSelectedDonorId(Number(e.target.value))
            }
          >
            {donors.map((donor) => (
              <option key={donor.id} value={donor.id}>
                {donor.name}
              </option>
            ))}
          </select>

        </div>

      </div>

      {loading ? (
        <div className="loading-card">Loading documents...</div>
      ) : (
        <>
          <DocumentList
            documents={attentionDocuments}
            onUpload={handleUpload}
            onReview={handleReview}
          />

          <AIRecommendation
            recommendation={recommendation}
            onGenerateRequest={handleGenerateRequest}
          />

          <UploadBanner
            document={missingDocument}
            onUpload={handleUpload}
          />

          {categories.map((category) => (
            <DocumentCategory
              key={category.title}
              {...category}
              documents={documents.filter(
                (doc) => doc.category === category.title
              )}
              onUpload={handleUpload}
              onReview={handleReview}
            />
          ))}
        </>
      )}

    </div>
  );
}
