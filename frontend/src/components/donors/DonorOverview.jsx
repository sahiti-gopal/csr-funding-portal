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
      icon: TriangleAlert,
    },
    {
      title: "Needs Attention",
      value: summary.attention ?? 0,
      amount: summary.attentionAmount ?? "₹0",
      icon: CircleAlert,
    },
    {
      title: "Healthy",
      value: summary.healthy ?? 0,
      amount: summary.healthyAmount ?? "₹0",
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
    <>
      <div className="overview-grid donor-kpi-grid">

        {cards.map((card) => {
          const Icon = card.icon;

          return (
            <div
              key={card.title}
              className="overview-card stat-card"
            >
              <span className="stat-icon">
                <Icon size={15} />
              </span>

              <span className="eyebrow">
                {card.title}
              </span>

              <div className="overview-value">
                {card.value}
              </div>

              <div className="overview-delta">
                {card.amount} · Committed
              </div>

            </div>
          );
        })}

      </div>

      <div className="distribution-band">

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
    </>
  );
}
