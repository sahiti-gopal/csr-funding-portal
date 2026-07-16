import ProgressBar from "./ProgressBar";

export default function FundUtilization({
  projects = [],
}) {

  if (!projects.length) {

    return (

      <div className="fund-card">

        <div className="section-header">

          <div>

            <h3>Fund Utilization</h3>

            <p>No utilization data available.</p>

          </div>

        </div>

      </div>

    );

  }

  return (

    <div className="fund-card">

      <div className="section-header">

        <div>

          <h3>Fund Utilization</h3>

          <p>
            Allocation across funded projects
          </p>

        </div>

      </div>

      <div className="fund-list">

        {projects.map((project) => (

          <div
            key={project.id}
            className="fund-row"
          >

            <div className="fund-top">

              <div>

                <h4>{project.name}</h4>

                <span>
                  Utilized
                </span>

              </div>

              <strong>

                ₹{(
                  project.utilized / 100000
                ).toFixed(1)} L

              </strong>

            </div>

            <ProgressBar
              value={project.progress}
              color="#2563EB"
            />

            <div className="fund-footer">

              <span>

                {project.progress}% utilized

              </span>

              <span>

                Remaining ₹
                {(project.remaining / 100000).toFixed(1)}L

              </span>

            </div>

          </div>

        ))}

      </div>

    </div>

  );

}