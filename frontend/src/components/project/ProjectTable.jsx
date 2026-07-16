import ProjectRow from "./ProjectRow";

export default function ProjectTable({
  projects = [],
  title = "Projects",
}) {
  return (
    <div className="project-table-card">

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

          {projects.length > 0 ? (

            projects.map((project) => (
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
