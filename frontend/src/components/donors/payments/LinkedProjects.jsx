import { useMemo, useState } from "react";
import {
  ArrowUpDown,
  FolderOpen,
  MapPin,
} from "lucide-react";

import ProgressBar from "./ProgressBar";
import { formatCurrency } from "../../../utils/format";

export default function LinkedProjects({
  projects = [],
}) {
  const [sortField, setSortField] =
    useState("progress");

  const [ascending, setAscending] =
    useState(false);

  const sortedProjects = useMemo(() => {
    const rows = [...projects];

    rows.sort((a, b) => {
      let x = a[sortField];
      let y = b[sortField];

      if (
        [
          "allocated",
          "utilized",
          "remaining",
          "progress",
        ].includes(sortField)
      ) {
        x = Number(x || 0);
        y = Number(y || 0);
      }

      if (x > y)
        return ascending ? 1 : -1;

      if (x < y)
        return ascending ? -1 : 1;

      return 0;
    });

    return rows;
  }, [
    projects,
    sortField,
    ascending,
  ]);

  const changeSort = (field) => {
    if (field === sortField) {
      setAscending(!ascending);
    } else {
      setSortField(field);
      setAscending(false);
    }
  };

  return (
    <div className="linked-projects-card">

      <div className="section-header">

        <div>

          <h3>
            Linked Projects
          </h3>

          <p>
            Projects funded by this donor
          </p>

        </div>

      </div>

      <div className="linked-projects-table">

        <table>

          <thead>

            <tr>

              <th
                onClick={() =>
                  changeSort("name")
                }
                style={{
                  cursor: "pointer",
                }}
              >
                Project
                <ArrowUpDown
                  size={15}
                />
              </th>

              <th
                onClick={() =>
                  changeSort("location")
                }
                style={{
                  cursor: "pointer",
                }}
              >
                Region
                <ArrowUpDown
                  size={15}
                />
              </th>

              <th
                onClick={() =>
                  changeSort(
                    "allocated"
                  )
                }
                style={{
                  cursor: "pointer",
                }}
              >
                Allocated
                <ArrowUpDown
                  size={15}
                />
              </th>

              <th
                onClick={() =>
                  changeSort(
                    "utilized"
                  )
                }
                style={{
                  cursor: "pointer",
                }}
              >
                Utilized
                <ArrowUpDown
                  size={15}
                />
              </th>

              <th
                onClick={() =>
                  changeSort(
                    "remaining"
                  )
                }
                style={{
                  cursor: "pointer",
                }}
              >
                Remaining
                <ArrowUpDown
                  size={15}
                />
              </th>

              <th
                style={{
                  width: 240,
                  cursor: "pointer",
                }}
                onClick={() =>
                  changeSort(
                    "progress"
                  )
                }
              >
                Progress
                <ArrowUpDown
                  size={15}
                />
              </th>

            </tr>

          </thead>

          <tbody>

            {sortedProjects.length ===
            0 ? (

              <tr>

                <td
                  colSpan={6}
                  style={{
                    textAlign:
                      "center",
                    padding:
                      "50px",
                    color:
                      "#64748B",
                  }}
                >
                  No linked projects
                  available.
                </td>

              </tr>

            ) : (

              sortedProjects.map(
                (project) => (

                  <tr
                    key={
                      project.id
                    }
                    className="project-row"
                  >

                    <td>

                      <div
                        style={{
                          display:
                            "flex",
                          gap: 10,
                          alignItems:
                            "center",
                        }}
                      >

                        <FolderOpen
                          size={18}
                          color="#2563EB"
                        />

                        <strong>

                          {
                            project.name
                          }

                        </strong>

                      </div>

                    </td>

                    <td>

                      <div
                        style={{
                          display:
                            "flex",
                          gap: 6,
                          alignItems:
                            "center",
                        }}
                      >

                        <MapPin
                          size={15}
                          color="#64748B"
                        />

                        {project.location ||
                          "-"}

                      </div>

                    </td>

                    <td>

                      {formatCurrency(
                        project.allocated
                      )}

                    </td>

                    <td>

                      {formatCurrency(
                        project.utilized
                      )}

                    </td>

                    <td>

                      {formatCurrency(
                        project.remaining
                      )}

                    </td>

                    <td>

                      <div className="project-progress">

                        <ProgressBar
                          value={
                            project.progress
                          }
                          color="#2563EB"
                        />

                        <span>

                          {
                            project.progress
                          }
                          %

                        </span>

                      </div>

                    </td>

                  </tr>

                )
              )

            )}

          </tbody>

        </table>

      </div>

    </div>
  );
}