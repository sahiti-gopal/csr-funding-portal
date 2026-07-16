import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
} from "recharts";

const fundingData = [
  { name: "Corporate", value: 40, color: "#3B82F6" },
  { name: "Foundation", value: 30, color: "#8B5CF6" },
  { name: "Government", value: 20, color: "#10B981" },
  { name: "Individual", value: 10, color: "#F59E0B" },
];

const statusData = [
  { name: "Active", value: 65, color: "#22C55E" },
  { name: "Completed", value: 18, color: "#3B82F6" },
  { name: "Expiring Soon", value: 12, color: "#F59E0B" },
  { name: "Inactive", value: 5, color: "#EF4444" },
];

function ChartCard({
  title,
  subtitle,
  data,
  center,
}) {
  return (
    <div className="chart-card">

      <div className="chart-header">

        <h3>{title}</h3>

        <p>{subtitle}</p>

      </div>

      <div className="chart-body">

        <div className="chart-wrapper">

          <ResponsiveContainer
            width={180}
            height={180}
          >
            <PieChart>

              <Pie
                data={data}
                innerRadius={52}
                outerRadius={78}
                dataKey="value"
              >

                {data.map((item) => (
                  <Cell
                    key={item.name}
                    fill={item.color}
                  />
                ))}

              </Pie>

            </PieChart>
          </ResponsiveContainer>

          <div className="chart-center">

            <strong>{center}</strong>

          </div>

        </div>

        <div className="chart-legend">

          {data.map((item) => (

            <div
              key={item.name}
              className="legend-row"
            >

              <div className="legend-left">

                <span
                  className="legend-dot"
                  style={{
                    background: item.color,
                  }}
                />

                {item.name}

              </div>

              <strong>
                {item.value}%
              </strong>

            </div>

          ))}

        </div>

      </div>

    </div>
  );
}

export default function DonorCharts() {
  return (
    <div className="charts-grid">

      <ChartCard
        title="Donor Funding Distribution"
        subtitle="By donor type · ₹21.2 Cr total"
        data={fundingData}
        center="41 Types"
      />

      <ChartCard
        title="Donor Status Overview"
        subtitle="Current status breakdown · 100 total"
        data={statusData}
        center="100 Total"
      />

    </div>
  );
}