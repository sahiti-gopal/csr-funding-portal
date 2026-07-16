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
}) {
  return (
    <div className="filters-card">

      <div className="filter-group">

        <span className="filter-label">Category</span>

        <div className="category-list">

          {categories.map((item) => {
            const value =
              item === "All Alerts" ? "All" : item;

            return (
              <button
                key={item}
                className={
                  category === value
                    ? "filter-chip active-chip"
                    : "filter-chip"
                }
                onClick={() => onCategoryChange(value)}
              >
                {item}
              </button>
            );
          })}

        </div>

      </div>

      <div className="filter-divider" />

      <div className="filter-group">

        <span className="filter-label">Priority</span>

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

    </div>
  );
}