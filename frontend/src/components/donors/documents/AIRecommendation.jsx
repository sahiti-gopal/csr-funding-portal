import { Sparkles } from "lucide-react";

export default function AIRecommendation({
  recommendation,
  onGenerateRequest,
}) {
  return (
    <div className="docai-card">

      <div className="docai-icon">
        <Sparkles size={16} />
      </div>

      <div className="docai-content">

        <h3>AI Recommendation</h3>

        <p>
          {recommendation}
        </p>

      </div>

      <button className="docai-btn" onClick={onGenerateRequest}>
        Generate Request
      </button>

    </div>
  );
}
