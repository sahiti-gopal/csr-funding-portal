import { useMemo, useState } from "react";
import { Search, SlidersHorizontal } from "lucide-react";
import ProjectRow from "./ProjectRow";

const STATUS_FILTERS = ["All", "Active", "Completed", "Delayed", "On Hold"];

export default function ProjectTable({
  projects = [],
  title = "Projects",
}) {
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("All");

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
    <div className="project-table-card">

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

      <table className="project-table">

        <thead>
          <tr>
            <th>Project</th>
            <th>Company</th>
            <th>Region</th>
            <th>Budget</th>
            <th>Progress</th>
            <th>Status</th>
            <th>Deadline</th>
            <th></th>
          </tr>
        </thead>

        <tbody>

          {filteredProjects.length > 0 ? (

            filteredProjects.map((project) => (
              <ProjectRow
                key={project.id}
                project={project}
              />
            ))

          ) : (

            <tr>

              <td
                colSpan="8"
                style={{
                  textAlign: "center",
                  padding: "40px",
                }}
              >
                No projects found
              </td>

            </tr>

          )}

        </tbody>

      </table>

    </div>
  );
}