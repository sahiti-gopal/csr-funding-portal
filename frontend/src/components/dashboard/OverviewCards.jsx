

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
          <div className="overview-title">
            {card.title}
          </div>

          <div className="overview-value">
            {card.value}
          </div>

          <div className="overview-subtitle">
            {card.subtitle}
          </div>
        </div>
      ))}
    </div>
  );
}