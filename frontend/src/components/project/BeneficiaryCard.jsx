import {
  Users,
  School,
  GraduationCap,
} from "lucide-react";

const ICONS = {
  students: Users,
  schools: School,
  teachers: GraduationCap,
};

export default function BeneficiaryCard({ metrics = [] }) {
  return (
    <div className="pd-panel">
      <h4 className="pd-panel-title">
        Beneficiaries
      </h4>

      <div className="beneficiary-kpis">
        {metrics.map((metric) => {
          const Icon = ICONS[metric.icon] ?? Users;

          return (
            <div
              className="beneficiary-kpi"
              key={metric.title}
            >
              <div className="beneficiary-icon">
                <Icon size={26} />
              </div>

              <h2 className="beneficiary-value">
                {metric.value}
              </h2>

              <p className="beneficiary-title">
                {metric.title}
              </p>

              <span className="beneficiary-target">
                Target {metric.target}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}