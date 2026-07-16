import {
  Activity,
  CheckCircle2,
  Upload,
  Landmark,
  FileCheck,
  Clock3,
  AlertTriangle,
} from "lucide-react";

function getRelativeTime(date) {
  if (!date) return "-";

  const now = new Date();
  const value = new Date(date);

  const seconds = Math.floor(
    (now - value) / 1000
  );

  if (seconds < 60)
    return "Just now";

  const minutes = Math.floor(
    seconds / 60
  );

  if (minutes < 60)
    return `${minutes} min ago`;

  const hours = Math.floor(
    minutes / 60
  );

  if (hours < 24)
    return `${hours} hour${
      hours > 1 ? "s" : ""
    } ago`;

  const days = Math.floor(
    hours / 24
  );

  if (days < 30)
    return `${days} day${
      days > 1 ? "s" : ""
    } ago`;

  return value.toLocaleDateString();
}

export default function RecentActivity({
  data = [],
}) {
  const getIcon = (type = "") => {
    switch (type) {
      case "PAYMENT_RECEIVED":
        return Landmark;

      case "DOCUMENT_UPLOADED":
        return Upload;

      case "DOCUMENT_VERIFIED":
        return FileCheck;

      case "FUND_ALLOCATED":
        return CheckCircle2;

      case "PAYMENT_OVERDUE":
        return AlertTriangle;

      default:
        return Clock3;
    }
  };

  return (
    <div className="recent-activity-card">

      <div className="section-header">

        <div>

          <h3>

            <Activity
              size={20}
              style={{
                marginRight: 8,
                verticalAlign: "middle",
              }}
            />

            Recent Payment Activity

          </h3>

          <p>

            Latest payment events and
            funding updates

          </p>

        </div>

      </div>

      <div className="activity-list">

        {data.length === 0 ? (

          <div
            style={{
              padding: 40,
              textAlign: "center",
              color: "#64748B",
            }}
          >

            No recent activity

          </div>

        ) : (

          data.map((item) => {

            const Icon =
              getIcon(item.type);

            return (

              <div
                key={item.id}
                className="activity-row"
              >

                <div
                  className="activity-icon"
                >

                  <Icon size={20} />

                </div>

                <div
                  className="activity-content"
                >

                  <h4>

                    {item.title}

                  </h4>

                  <span>

                    {getRelativeTime(
                      item.date
                    )}

                  </span>

                </div>

              </div>

            );

          })

        )}

      </div>

    </div>
  );
}