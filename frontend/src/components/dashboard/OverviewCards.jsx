export default function OverviewCards({
  stats,
  activeCard,
  onCardClick,
}) {
  return (
    <div className="overview-grid">
      {stats.map((card) => {
        const Icon = card.icon;

        return (
          <div
            key={card.title}
            className={`overview-card ${
              activeCard === card.title ? "active" : ""
            }`}
            onClick={() => onCardClick(card.title)}
          >
            {Icon && (
              <span className="overview-icon">
                <Icon size={15} />
              </span>
            )}

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
        );
      })}
    </div>
  );
}