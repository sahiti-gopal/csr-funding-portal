export default function OverviewCards({
  stats,
  activeCard,
  onCardClick,
}) {
  return (
    <div className="overview-grid">
      {stats.map((card) => (
        <div
          key={card.title}
          className={`overview-card ${
            activeCard === card.title ? "active" : ""
          }`}
          onClick={() => onCardClick(card.title)}
        >
          <span className="eyebrow">{card.title}</span>

          <div className="overview-value">{card.value}</div>

          <div className="overview-delta">
            {typeof card.percent === "number"
              ? `${card.percent}% · ${card.status}`
              : card.subtitle}
          </div>
        </div>
      ))}
    </div>
  );
}
