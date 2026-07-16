import { CheckCircle2 } from "lucide-react";

const categories = [
  "All Alerts",
  "Donor Risk",
  "Documents",
  "Reports",
  "System",
];

const priorities = [
  "All",
  "High",
  "Medium",
  "Low",
];

export default function AlertFilters({
  category,
  priority,
  onCategoryChange,
  onPriorityChange,
  onMarkRead,
}) {
  return (
    <div className="filters-card">

      <div className="filters-top">

        <div className="category-list">

          {categories.map((item) => (
            <button
              key={item}
              className={
                category === item
                  ? "filter-chip active-chip"
                  : "filter-chip"
              }
              onClick={() => onCategoryChange(item)}
            >
              {item}
            </button>
          ))}

        </div>

        <button
          className="mark-read-btn"
          onClick={onMarkRead}
        >
          <CheckCircle2 size={16} />

          MARK ALL READ
        </button>

      </div>

      <div className="priority-list">

        {priorities.map((item) => (
          <button
            key={item}
            className={
              priority === item.toUpperCase() ||
              priority === item
                ? "priority-chip2 active-priority"
                : "priority-chip2"
            }
            onClick={() =>
              onPriorityChange(
                item === "All"
                  ? "All"
                  : item.toUpperCase()
              )
            }
          >
            {item}
          </button>
        ))}

      </div>

    </div>
  );
}