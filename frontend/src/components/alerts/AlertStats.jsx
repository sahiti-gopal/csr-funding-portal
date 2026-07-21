import {
  Bell,
  TriangleAlert,
  CircleAlert,
  CircleCheck,
} from "lucide-react";

const cards = [
  {
    key: "total",
    title: "All Alerts",
    icon: Bell,
  },
  {
    key: "high",
    title: "High",
    icon: TriangleAlert,
  },
  {
    key: "medium",
    title: "Medium",
    icon: CircleAlert,
  },
  {
    key: "low",
    title: "Low",
    icon: CircleCheck,
  },
];

export default function AlertStats({ summary, activeCard, onCardClick }) {
  return (
    <div className="alert-stats overview-grid">
      {cards.map((card) => {
        const Icon = card.icon;

        return (
          <div
            key={card.key}
            className={`overview-card stat-card ${
              activeCard === card.key ? "active" : ""
            }`}
            onClick={() => onCardClick?.(card.key)}
          >
            {Icon && (
              <span className="stat-icon">
                <Icon size={15} />
              </span>
            )}

            <span className="eyebrow">
              {card.title}
            </span>

            <div className="overview-value">
              {summary[card.key]}
            </div>
          </div>
        );
      })}
    </div>
  );
}