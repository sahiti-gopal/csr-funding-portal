export default function AIInsights({ projects }) {
  if (!projects.length) return null;

  const totalBudget = projects.reduce(
    (sum, p) => sum + Number(p.budget),
    0
  );

  const active = projects.filter(
    (p) => p.status === "Active"
  ).length;

  const completed = projects.filter(
    (p) => p.status === "Completed"
  ).length;

  const categoryMap = {};

  projects.forEach((p) => {
    categoryMap[p.project_type] =
      (categoryMap[p.project_type] || 0) + Number(p.budget);
  });

  const topCategory = Object.keys(categoryMap).sort(
    (a, b) => categoryMap[b] - categoryMap[a]
  )[0];

  const completion =
    ((completed / projects.length) * 100).toFixed(0);

  return (
    <div
      style={{
        background: "#eef8ff",
        padding: 20,
        borderRadius: 14,
        marginTop: 30,
        marginBottom: 30,
        borderLeft: "6px solid #2563eb",
      }}
    >
      <h2>🤖 AI Portfolio Insights</h2>

      <p>
        ✔ Highest CSR investment is in
        <strong> {topCategory}</strong>.
      </p>

      <p>
        ✔ Active initiatives :
        <strong> {active}</strong>
      </p>

      <p>
        ✔ Portfolio completion :
        <strong> {completion}%</strong>
      </p>

      <p>
        ✔ Total CSR investment :
        <strong>
          ₹{totalBudget.toLocaleString()}
        </strong>
      </p>

      <p>
        💡 Recommendation: Increase investment in
        under-funded CSR sectors to improve
        portfolio diversification.
      </p>
    </div>
  );
}