import {
  TriangleAlert,
  CircleAlert,
  CircleCheck,
} from "lucide-react";

export default function DonorOverview({
  summary = {},
}) {
  const cards = [
    {
      title: "At Risk",
      value: summary.atRisk ?? 0,
      amount: summary.atRiskAmount ?? "₹0",
      color: "#EF4444",
      bg: "#FEE2E2",
      icon: TriangleAlert,
    },
    {
      title: "Needs Attention",
      value: summary.attention ?? 0,
      amount: summary.attentionAmount ?? "₹0",
      color: "#F59E0B",
      bg: "#FEF3C7",
      icon: CircleAlert,
    },
    {
      title: "Healthy",
      value: summary.healthy ?? 0,
      amount: summary.healthyAmount ?? "₹0",
      color: "#22C55E",
      bg: "#DCFCE7",
      icon: CircleCheck,
    },
  ];

  const total =
    (summary.atRisk ?? 0) +
    (summary.attention ?? 0) +
    (summary.healthy ?? 0);

  const red =
    total === 0
      ? 0
      : ((summary.atRisk ?? 0) / total) * 100;

  const orange =
    total === 0
      ? 0
      : ((summary.attention ?? 0) / total) * 100;

  const green =
    total === 0
      ? 0
      : ((summary.healthy ?? 0) / total) * 100;

  return (
    <div className="health-card">

      <h3>Donor Health Overview</h3>

      <div className="health-grid">

        {cards.map((card) => {
          const Icon = card.icon;

          return (
            <div
              key={card.title}
              className="health-item"
            >
              <div className="health-top">

                <div>

                  <div
                    className="health-value"
                    style={{
                      color: card.color,
                    }}
                  >
                    {card.value}
                  </div>

                  <div
                    className="health-title"
                    style={{
                      color: card.color,
                    }}
                  >
                    {card.title}
                  </div>

                </div>

                <div
                  className="health-icon"
                  style={{
                    background: card.bg,
                    color: card.color,
                  }}
                >
                  <Icon size={15} />
                </div>

              </div>

              <h4>{card.amount}</h4>

              <span>Committed</span>

            </div>
          );
        })}

      </div>

      <div className="distribution">

        <div className="distribution-bar">

          <div
            className="red"
            style={{
              width: `${red}%`,
            }}
          />

          <div
            className="orange"
            style={{
              width: `${orange}%`,
            }}
          />

          <div
            className="green"
            style={{
              width: `${green}%`,
            }}
          />

        </div>

        <div className="distribution-footer">

          <strong>
            {total} Total Donors
          </strong>

          <span>Distribution</span>

        </div>

      </div>

    </div>
  );
}