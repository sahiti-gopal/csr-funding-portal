const MAX_PARTNER_LOGOS = 4;

const GOALS = [
  {
    id: 1,
    title: "No Poverty",
    color: "#E5243B",
    paths: ["M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"],
  },
  {
    id: 2,
    title: "Zero Hunger",
    color: "#DDA63A",
    paths: ["M12 2c2 3 3 6 3 9a3 3 0 0 1-6 0c0-3 1-6 3-9Z", "M12 14v8"],
  },
  {
    id: 3,
    title: "Good Health",
    color: "#4C9F38",
    paths: [
      "M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z",
    ],
  },
  {
    id: 4,
    title: "Quality Education",
    color: "#C5192D",
    paths: ["M22 10 12 5 2 10l10 5 10-5Z", "M6 12v5c0 1.5 3 3 6 3s6-1.5 6-3v-5"],
  },
  {
    id: 5,
    title: "Gender Equality",
    color: "#FF3A21",
    circles: [{ cx: 12, cy: 9, r: 5 }],
    paths: ["M12 14v8M9 19h6"],
  },
  {
    id: 6,
    title: "Clean Water",
    color: "#26BDE2",
    paths: ["M12 2s7 7.5 7 12.5A7 7 0 0 1 5 14.5C5 9.5 12 2 12 2Z"],
  },
  {
    id: 7,
    title: "Clean Energy",
    color: "#FCC30B",
    paths: ["M13 2 4 14h7l-1 8 9-12h-7l1-8Z"],
  },
  {
    id: 8,
    title: "Decent Work",
    color: "#A21942",
    rects: [{ x: 3, y: 7, width: 18, height: 13, rx: 2 }],
    paths: ["M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"],
  },
  {
    id: 9,
    title: "Industry",
    color: "#FD6925",
    paths: ["M3 21V10l6 4v-4l6 4V6l6 4v11H3Z"],
  },
  {
    id: 10,
    title: "Reduced Inequality",
    color: "#DD1367",
    paths: ["M6 3v18M18 3v18M3 8h6M15 16h6"],
  },
  {
    id: 11,
    title: "Sustainable Cities",
    color: "#FD9D24",
    paths: ["M4 21V9l5-4 5 4v12M14 21v-8l6-3v11H4"],
  },
  {
    id: 12,
    title: "Responsible Consumption",
    color: "#BF8B2E",
    paths: ["M17 2 21 6l-4 4M3 12v-2a4 4 0 0 1 4-4h14M7 22 3 18l4-4M21 12v2a4 4 0 0 1-4 4H3"],
  },
  {
    id: 13,
    title: "Climate Action",
    color: "#3F7E44",
    paths: ["M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 9 20 8c-2 5-1 9-5 12h-4z"],
  },
  {
    id: 14,
    title: "Life Below Water",
    color: "#0A97D9",
    paths: ["M2 12s4-5 10-5 10 5 10 5-4 5-10 5-10-5-10-5Z"],
    circles: [{ cx: 15, cy: 12, r: 1 }],
  },
  {
    id: 15,
    title: "Life On Land",
    color: "#56C02B",
    paths: ["M12 22V12M12 12 6 6M12 12l6-6M5 3l7 9 7-9"],
  },
  {
    id: 16,
    title: "Peace & Justice",
    color: "#00689D",
    paths: ["M12 3v18M5 7l-2 5a3 3 0 0 0 6 0L7 7M19 7l-2 5a3 3 0 0 0 6 0l-2-5M5 7h4M15 7h4"],
  },
  {
    id: 17,
    title: "Partnerships",
    color: "#19486A",
    paths: ["M8.5 8.5 4 13l4.5 4.5M15.5 8.5 20 13l-4.5 4.5M14 6l-4 12"],
  },
];

const initials = (name = "") =>
  name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0])
    .join("")
    .toUpperCase();

export default function SDGImpact({ fundedIds = [], impactByGoal = {} }) {
  const funded = new Set(fundedIds);

  return (
    <div className="sdg-tiles">
      {GOALS.map((goal) => {
        const impact = impactByGoal[goal.id];
        const partners = impact?.partners ?? [];
        const visiblePartners = partners.slice(0, MAX_PARTNER_LOGOS);
        const hiddenCount = partners.length - visiblePartners.length;

        return (
          <div
            key={goal.id}
            className={`sdg-tile ${funded.has(goal.id) ? "sdg-tile-funded" : ""}`}
            title={`${goal.id}. ${goal.title}${funded.has(goal.id) ? " — funded" : ""}`}
            tabIndex={0}
          >
            <span className="sdg-tile-num">{String(goal.id).padStart(2, "0")}</span>

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="white"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              {goal.circles?.map((c, i) => <circle key={i} {...c} />)}
              {goal.rects?.map((r, i) => <rect key={i} {...r} />)}
              {goal.paths?.map((d, i) => <path key={i} d={d} />)}
            </svg>

            <span className="sdg-tile-label">{goal.title}</span>

            {impact && (
              <div className="sdg-tile-tooltip">
                <span className="sdg-tile-tooltip-title">Associated partners</span>

                <div className="sdg-tile-tooltip-logos">
                  {visiblePartners.map((partner) =>
                    partner.logo_url ? (
                      <img
                        key={partner.name}
                        src={partner.logo_url}
                        alt={partner.name}
                        title={partner.name}
                        className="sdg-tile-tooltip-logo"
                        onError={(e) => {
                          e.currentTarget.style.display = "none";
                        }}
                      />
                    ) : (
                      <span
                        key={partner.name}
                        title={partner.name}
                        className="sdg-tile-tooltip-logo sdg-tile-tooltip-logo-fallback"
                      >
                        {initials(partner.name)}
                      </span>
                    )
                  )}
                </div>

                {hiddenCount > 0 && (
                  <div className="sdg-tile-tooltip-more-row">
                    <span
                      className="sdg-tile-tooltip-more"
                      title={`${hiddenCount} more partner${hiddenCount === 1 ? "" : "s"}`}
                    >
                      +{hiddenCount}
                    </span>
                  </div>
                )}

                <div className="sdg-tile-tooltip-stats">
                  <span>
                    <strong>{impact.projects}</strong> project
                    {impact.projects === 1 ? "" : "s"}
                  </span>
                  <span>
                    <strong>{impact.beneficiaries.toLocaleString()}</strong>{" "}
                    beneficiaries
                  </span>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
