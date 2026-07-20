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
    icon: FileText,
  },
  {
    key: "submitted",
    title: "Submitted",
    icon: CheckCircle2,
  },
  {
    key: "pending",
    title: "Pending review",
    icon: Clock3,
  },
  {
    key: "missing",
    title: "Missing / expired",
    icon: TriangleAlert,
  },
  {
    key: "compliance",
    title: "Compliance score",
    suffix: "%",
    icon: ShieldCheck,
  },
];

export default function DocumentStats({ stats }) {
  return (
    <div className="overview-grid document-stats">

      {cards.map((card) => {
        const Icon = card.icon;

        return (
          <div
            key={card.key}
            className="overview-card stat-card"
          >

            <span className="stat-icon">
              <Icon size={15} />
            </span>

            <span className="eyebrow">
              {card.title}
            </span>

            <div className="overview-value">
              {stats[card.key]}
              {card.suffix ?? ""}
            </div>

          </div>
        );
      })}

    </div>
  );
}