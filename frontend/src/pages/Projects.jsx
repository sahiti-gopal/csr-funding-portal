import { useEffect, useMemo, useState } from "react";
import {
  Briefcase,
  Activity,
  CircleCheck,
  TriangleAlert,
} from "lucide-react";

import ProjectTable from "../components/project/ProjectTable";
import { getProjects } from "../services/projectService";
import "../styles/dashboard.css";
import "../styles/projects.css";

const CARD_FILTERS = {
  total: () => true,
  active: (p) => p.status === "Active",
  completed: (p) => p.status === "Completed",
  atRisk: (p) => p.status === "Delayed" || p.status === "On Hold",
};

const CARD_TITLES = {
  total: "All Projects",
  active: "Active Projects",
  completed: "Completed Projects",
  atRisk: "Delayed / On Hold Projects",
};

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [activeCard, setActiveCard] = useState("total");

  const loadProjects = () => {
    getProjects()
      .then(setProjects)
      .catch(console.error);
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const filteredProjects = useMemo(() => {
    const matches = CARD_FILTERS[activeCard] ?? CARD_FILTERS.total;
    return projects.filter(matches);
  }, [projects, activeCard]);

  const stats = useMemo(() => {
    const active = projects.filter((p) => p.status === "Active").length;
    const completed = projects.filter((p) => p.status === "Completed").length;
    const atRisk = projects.filter(
      (p) => p.status === "Delayed" || p.status === "On Hold"
    ).length;

    return [
      {
        key: "total",
        title: "Total Projects",
        value: projects.length,
        icon: Briefcase,
      },
      {
        key: "active",
        title: "Active",
        value: active,
        icon: Activity,
      },
      {
        key: "completed",
        title: "Completed",
        value: completed,
        icon: CircleCheck,
      },
      {
        key: "atRisk",
        title: "Delayed / On Hold",
        value: atRisk,
        icon: TriangleAlert,
      },
    ];
  }, [projects]);

  return (
    <div className="projects-page">

      <div className="dashboard-head">

        <div className="dashboard-title">
          <span className="eyebrow">Portfolio</span>
          <h4 className="section-heading">Projects</h4>
        </div>

      </div>

      <div className="overview-grid project-stats">

        {stats.map((card) => {
          const Icon = card.icon;

          return (
            <div
              key={card.key}
              className={`overview-card stat-card ${
                activeCard === card.key ? "active" : ""
              }`}
              onClick={() => setActiveCard(card.key)}
            >
              <span className="stat-icon">
                <Icon size={15} />
              </span>

              <span className="eyebrow">{card.title}</span>

              <div className="overview-value">{card.value}</div>
            </div>
          );
        })}

      </div>

      <ProjectTable
        title={CARD_TITLES[activeCard] ?? "All Projects"}
        projects={filteredProjects}
      />

    </div>
  );
}
