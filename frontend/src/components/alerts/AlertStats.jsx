import {
  Bell,
  MailOpen,
  TriangleAlert,
  CircleCheck,
} from "lucide-react";

const cards = [
  {
    key: "total",
    title: "All Alerts",
    icon: Bell,
  },
  {
    key: "unread",
    title: "Unread",
    icon: MailOpen,
  },
  {
    key: "high",
    title: "High Priority",
    icon: TriangleAlert,
  },
  {
    key: "resolved",
    title: "Resolved",
    icon: CircleCheck,
  },
];

export default function AlertStats({ summary }) {
  return (
    <div className="alert-stats">
      {cards.map((card) => {
        const Icon = card.icon;

        return (
          <div
            key={card.key}
            className="summary-card"
          >
            {Icon && (
              <span className="summary-icon">
                <Icon size={15} />
              </span>
            )}

            <div className="summary-title">
              {card.title}
            </div>

            <div className="summary-number">
              {summary[card.key]}
            </div>
          </div>
        );
      })}
    </div>
  );
}