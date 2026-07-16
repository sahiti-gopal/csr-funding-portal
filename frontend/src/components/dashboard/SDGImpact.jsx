const goals = [
  { id: 1, title: "No Poverty", color: "#E5243B" },
  { id: 2, title: "Zero Hunger", color: "#DDA63A" },
  { id: 3, title: "Good Health", color: "#4C9F38" },
  { id: 4, title: "Quality Education", color: "#C5192D" },
  { id: 5, title: "Gender Equality", color: "#FF3A21" },
  { id: 6, title: "Clean Water", color: "#26BDE2" },
  { id: 7, title: "Clean Energy", color: "#FCC30B" },
  { id: 8, title: "Decent Work", color: "#A21942" },
  { id: 9, title: "Industry", color: "#FD6925" },
  { id: 10, title: "Reduced Inequality", color: "#DD1367" },
  { id: 11, title: "Sustainable Cities", color: "#FD9D24" },
  { id: 12, title: "Responsible Consumption", color: "#BF8B2E" },
  { id: 13, title: "Climate Action", color: "#3F7E44" },
  { id: 14, title: "Life Below Water", color: "#0A97D9" },
  { id: 15, title: "Life On Land", color: "#56C02B" },
  { id: 16, title: "Peace & Justice", color: "#00689D" },
  { id: 17, title: "Partnerships", color: "#19486A" },
];

export default function SDGImpact() {
  return (
    <div className="sdg-grid">
      {goals.map((goal) => (
        <div
          key={goal.id}
          className="sdg-card"
          style={{
            background: goal.color,
          }}
        >
          <span className="sdg-number">
            {goal.id}
          </span>

          <span className="sdg-title">
            {goal.title}
          </span>
        </div>
      ))}
    </div>
  );
}