export default function KPICard({
  title,
  value,
  color,
  icon,
}) {
  return (
    <div
      style={{
        background: "#fff",
        borderRadius: 14,
        padding: 20,
        boxShadow: "0 4px 12px rgba(0,0,0,.08)",
        borderTop: `5px solid ${color}`,
      }}
    >
      <div
        style={{
          fontSize: 14,
          color: "#6b7280",
          marginBottom: 10,
        }}
      >
        {icon} {title}
      </div>

      <div
        style={{
          fontSize: 30,
          fontWeight: "bold",
          color: "#111827",
        }}
      >
        {value}
      </div>
    </div>
  );
}