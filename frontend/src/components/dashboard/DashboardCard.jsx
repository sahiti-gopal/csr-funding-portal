export default function DashboardCard({
  title,
  value,
  color,
}) {
  return (
    <div
      style={{
        background:"#fff",
        borderRadius:18,
        padding:22,
        boxShadow:"0 8px 20px rgba(0,0,0,.06)",
        borderTop:`5px solid ${color}`,
      }}
    >
      <p
        style={{
          color:"#6B7280",
          fontSize:14,
        }}
      >
        {title}
      </p>

      <h2
        style={{
          marginTop:10,
          fontSize:34,
        }}
      >
        {value}
      </h2>
    </div>
  );
}