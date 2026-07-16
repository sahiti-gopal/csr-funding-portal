export default function StatusBadge({
  status,
}) {
  const cls =
    status === "Paid"
      ? "paid"
      : status === "Pending"
      ? "pending"
      : status === "Overdue"
      ? "overdue"
      : "scheduled";

  return (
    <span className={`status-badge ${cls}`}>
      {status}
    </span>
  );
}