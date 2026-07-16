import { useEffect, useState } from "react";

import ProjectTable from "../components/project/ProjectTable";
import ProjectForm from "../components/forms/ProjectForm";
import { createProject, getProjects } from "../services/projectService";
import "../styles/projects.css";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [showForm, setShowForm] = useState(false);

  const loadProjects = () => {
    getProjects()
      .then(setProjects)
      .catch(console.error);
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleCreate = async (form) => {
    try {
      await createProject(form);
      setShowForm(false);
      loadProjects();
    } catch (err) {
      console.error(err);
    }
  };

  const stateCount = new Set(
    projects.map((p) => p.region).filter(Boolean)
  ).size;

  return (
    <div className="projects-page">

      <div className="projects-header">

        <div>
          <h1>Projects</h1>
          <p>
            {projects.length} projects across {stateCount} states
          </p>
        </div>

        <button
          className="new-project-btn"
          onClick={() => setShowForm(true)}
        >
          + New Project
        </button>

      </div>

      {showForm && (
        <div className="modal-overlay" onClick={() => setShowForm(false)}>
          <div
            className="modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-header">
              <h3>New Project</h3>
              <button
                className="modal-close-btn"
                onClick={() => setShowForm(false)}
              >
                ×
              </button>
            </div>

            <ProjectForm onSubmit={handleCreate} />
          </div>
        </div>
      )}

      <ProjectTable title="All Projects" projects={projects} />

    </div>
  );
}
