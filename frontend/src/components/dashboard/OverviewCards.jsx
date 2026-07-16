export default function OverviewCards({
  stats,
  activeCard,
  onCardClick,
}) {
  return (
    <div className="overview-grid">
      {stats.map((card) => {
        const accent = card.accent ?? "raised";

        return (
          <div
            key={card.title}
            className={`overview-card overview-card-photo accent-${accent} ${
              activeCard === card.title ? "active" : ""
            }`}
            onClick={() => onCardClick(card.title)}
          >
            <div className="overview-card-top">
              {typeof card.percent === "number" && (
                <span className="overview-percent-badge">
                  {card.percent}%
                </span>
              )}
            </div>

            <div className="overview-title">
              {card.title}
            </div>

            <div className="overview-value">
              {card.value}
            </div>

            {typeof card.percent === "number" ? (
              <>
                <div className="overview-progress-track">
                  <div
                    className="overview-progress-fill"
                    style={{ width: `${Math.min(card.percent, 100)}%` }}
                  />
                </div>

                <span className="overview-status-pill">
                  {card.status}
                </span>
              </>
            ) : (
              <span className="overview-status-pill overview-subtitle-pill">
                {card.subtitle}
              </span>
            )}
          </div>
        );
      })}
    </div>
  );
}
