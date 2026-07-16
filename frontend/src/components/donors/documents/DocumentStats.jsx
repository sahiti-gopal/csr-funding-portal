import {
  FileText,
  CheckCircle2,
  Clock3,
  TriangleAlert,
  ShieldCheck,
} from "lucide-react";

const cards = [
  {
    key: "required",
    title: "Required documents",
    color: "#2563EB",
    icon: FileText,
  },
  {
    key: "submitted",
    title: "Submitted",
    color: "#16A34A",
    icon: CheckCircle2,
  },
  {
    key: "pending",
    title: "Pending review",
    color: "#F59E0B",
    icon: Clock3,
  },
  {
    key: "missing",
    title: "Missing / expired",
    color: "#EF4444",
    icon: TriangleAlert,
  },
  {
    key: "compliance",
    title: "Compliance score",
    color: "#7C3AED",
    suffix: "%",
    icon: ShieldCheck,
  },
];

export default function DocumentStats({ stats }) {
  return (
    <div className="document-stats">

      {cards.map((card) => (

        <div
          key={card.key}
          className="document-stat-card"
        >

          <div className="stat-title">
            {card.title}
          </div>

          <div
            className="stat-number"
            style={{
              color: card.color,
            }}
          >
            {stats[card.key]}
            {card.suffix ?? ""}
          </div>

        </div>

      ))}

    </div>
  );
}