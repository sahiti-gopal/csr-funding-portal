import { useEffect, useMemo, useState } from "react";
import { Search, SlidersHorizontal } from "lucide-react";

import ProjectTable from "../components/project/ProjectTable";
import { getProjects } from "../services/projectService";
import "../styles/dashboard.css";
import "../styles/projects.css";

const STATUS_FILTERS = ["All", "Active", "Completed", "Delayed", "On Hold"];

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("All");

  const loadProjects = () => {
    getProjects()
      .then(setProjects)
      .catch(console.error);
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const filteredProjects = useMemo(() => {
    return projects.filter((project) => {
      const matchesSearch =
        search.trim() === "" ||
        project.project_name
          ?.toLowerCase()
          .includes(search.toLowerCase()) ||
        project.sponsor_name
          ?.toLowerCase()
          .includes(search.toLowerCase()) ||
        project.region
          ?.toLowerCase()
          .includes(search.toLowerCase());

      const matchesStatus =
        status === "All" ||
        project.status === status;

      return matchesSearch && matchesStatus;
    });
  }, [projects, search, status]);

  return (
    <div className="projects-page">

      <div className="dashboard-head">

        <div className="dashboard-title">
          <h4 className="section-heading">Projects</h4>
        </div>

        <div className="project-toolbar">

          <div className="search-box-wrap">
            <Search size={16} className="search-icon" />
            <input
              className="search-box"
              placeholder="Search by name, region, or company..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <SlidersHorizontal size={16} className="filter-icon" />

          <div className="status-filters">
            {STATUS_FILTERS.map((option) => (
              <button
                key={option}
                className={`status-filter-chip ${
                  status === option ? "active" : ""
                }`}
                onClick={() => setStatus(option)}
              >
                {option}
              </button>
            ))}
          </div>

        </div>

      </div>

      <ProjectTable title="All Projects" projects={filteredProjects} />

    </div>
  );
}
