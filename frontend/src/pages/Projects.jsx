import { useEffect, useState } from "react";

import ProjectTable from "../components/project/ProjectTable";
import { getProjects } from "../services/projectService";
import "../styles/dashboard.css";
import "../styles/projects.css";

export default function Projects() {
  const [projects, setProjects] = useState([]);

  const loadProjects = () => {
    getProjects()
      .then(setProjects)
      .catch(console.error);
  };

  useEffect(() => {
    loadProjects();
  }, []);

  return (
    <div className="projects-page">

      <div className="dashboard-head">

        <div className="dashboard-title">
          <h4 className="section-heading">Projects</h4>
        </div>

      </div>

      <ProjectTable title="All Projects" projects={projects} />

    </div>
  );
}
