import {
  UploadCloud,
  ArrowRight,
} from "lucide-react";

export default function UploadBanner() {
  return (
    <div className="upload-banner">

      <div className="upload-left">

        <div className="upload-icon">

          <UploadCloud size={18} />

        </div>

        <div>

          <h3>Upload Missing Documents</h3>

          <p>
            Drag & drop PDFs or browse your computer to upload
            required compliance documents.
          </p>

        </div>

      </div>

      <button className="upload-banner-btn">

        Upload Documents

        <ArrowRight size={18} />

      </button>

    </div>
  );
}