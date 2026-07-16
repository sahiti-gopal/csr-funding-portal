import {
  Sparkles,
  TrendingUp,
  TriangleAlert,
  Lightbulb,
} from "lucide-react";

export default function AIInsights({
  insights = [],
}) {

  const icon = (priority) => {

    if (priority === "High")
      return TriangleAlert;

    if (priority === "Medium")
      return TrendingUp;

    return Lightbulb;

  };

  const color = (priority) => {

    if (priority === "High")
      return "#EF4444";

    if (priority === "Medium")
      return "#F59E0B";

    return "#2563EB";

  };

  if (!insights.length) {

    return (

      <div className="ai-insights-card">

        <div className="section-header">

          <div>

            <h3>

              <Sparkles size={18}/>

              AI Insights

            </h3>

            <p>No insights available.</p>

          </div>

        </div>

      </div>

    );

  }

  return (

    <div className="ai-insights-card">

      <div className="section-header">

        <div>

          <h3>

            <Sparkles
              size={18}
            />

            AI Insights

          </h3>

          <p>

            AI-generated payment recommendations

          </p>

        </div>

      </div>

      <div className="ai-insights-list">

        {insights.map((item) => {

          const Icon =
            icon(item.priority);

          return (

            <div
              key={item.id}
              className="ai-insight-row"
            >

              <div
                className="ai-icon"
                style={{
                  color: color(item.priority),
                }}
              >

                <Icon size={20}/>

              </div>

              <div
                className="ai-content"
              >

                <h4>

                  {item.title}

                </h4>

                <p>

                  {item.description}

                </p>

                <small>

                  {item.priority} Priority

                </small>

              </div>

            </div>

          );

        })}

      </div>

    </div>

  );

}