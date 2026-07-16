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
    color: "#2563EB",
  },
  {
    key: "unread",
    title: "Unread",
    icon: MailOpen,
    color: "#2563EB",
  },
  {
    key: "high",
    title: "High Priority",
    icon: TriangleAlert,
    color: "#EF4444",
  },
  {
    key: "resolved",
    title: "Resolved",
    icon: CircleCheck,
    color: "#2563EB",
  },
];

export default function AlertStats({ summary }) {
  return (
    <div className="alert-stats">
      {cards.map((card) => {
        return (
          <div
            key={card.key}
            className="summary-card"
          >
            <div
              className="summary-number"
              style={{ color: card.color }}
            >
              {summary[card.key]}
            </div>

            <div className="summary-title">
              {card.title}
            </div>
          </div>
        );
      })}
    </div>
  );
}