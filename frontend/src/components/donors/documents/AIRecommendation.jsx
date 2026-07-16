import { Sparkles } from "lucide-react";

export default function AIRecommendation() {
  return (
    <div className="docai-card">

      <div className="docai-icon">
        <Sparkles size={16} />
      </div>

      <div className="docai-content">

        <h3>AI Recommendation</h3>

        <p>
          Request the donor's latest audited financial statements.
          This will improve compliance from <strong>63%</strong> to approximately
          <strong> 81%</strong>.
        </p>

      </div>

      <button className="docai-btn">
        Generate Request
      </button>

    </div>
  );
}