import { useRef } from "react";
import {
  UploadCloud,
  ArrowRight,
} from "lucide-react";

export default function UploadBanner({ document, onUpload }) {
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    if (file && document) {
      onUpload?.(document.id, file);
    }
    event.target.value = "";
  };

  return (
    <div className="upload-banner">

      <input
        ref={fileInputRef}
        type="file"
        style={{ display: "none" }}
        onChange={handleFileChange}
      />

      <div className="upload-left">

        <div className="upload-icon">

          <UploadCloud size={18} />

        </div>

        <div>

          <h3>Upload Missing Documents</h3>

          <p>
            {document
              ? `Upload "${document.title}" — drag & drop or browse your computer.`
              : "Drag & drop PDFs or browse your computer to upload required compliance documents."}
          </p>

        </div>

      </div>

      <button
        className="upload-banner-btn"
        onClick={() => fileInputRef.current?.click()}
        disabled={!document}
      >

        Upload Documents

        <ArrowRight size={18} />

      </button>

    </div>
  );
}
