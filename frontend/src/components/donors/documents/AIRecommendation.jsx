import { Sparkles } from "lucide-react";

export default function AIRecommendation() {
  return (
    <div className="ai-card">

      <div className="ai-icon">
        <Sparkles size={22} />
      </div>

      <div className="ai-content">

        <h3>AI Recommendation</h3>

        <p>
          Request the donor's latest audited financial statements.
          This will improve compliance from <strong>63%</strong> to approximately
          <strong> 81%</strong>.
        </p>

      </div>

      <button className="ai-btn">
        Generate Request
      </button>

    </div>
  );
}