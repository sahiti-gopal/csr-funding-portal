import {
  Users,
  School,
  GraduationCap,
  MapPin,
  Heart,
  Tent,
  UserCheck,
  Building2,
  BookOpen,
} from "lucide-react";

import "../../styles/dashboard.css";

const ICONS = {
  students: Users,
  schools: School,
  teachers: GraduationCap,
  locations: MapPin,
  beneficiaries: Users,
  patients: Heart,
  camps: Tent,
  volunteers: UserCheck,
  sites: Building2,
  trainings: BookOpen,
};

export default function BeneficiaryCard({ metrics = [], locationsCount }) {
  const tiles = [...metrics];

  if (locationsCount != null) {
    tiles.push({
      icon: "locations",
      title: "Locations",
      value: locationsCount,
    });
  }

  return (
    <div className="pd-panel">
      <h4 className="pd-panel-title">
        Beneficiaries
      </h4>

      <div className="overview-grid pd-beneficiary-grid">
        {tiles.map((metric) => {
          const Icon = ICONS[metric.icon] ?? Users;

          return (
            <div
              className="overview-card"
              key={metric.title}
            >
              <span className="overview-icon">
                <Icon size={15} />
              </span>

              <div className="overview-title">
                {metric.title}
              </div>

              <div className="overview-value">
                {metric.value}
              </div>

              {metric.target != null && (
                <div className="overview-subtitle">
                  Target {metric.target}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
