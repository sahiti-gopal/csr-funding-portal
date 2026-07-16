export default function ProgressBar({
  value,
  color = "#2563EB",
  height = 8,
}) {
  return (
    <div
      className="pay-progress-track"
      style={{
        height,
      }}
    >
      <div
        className="pay-progress-fill"
        style={{
          width: `${value}%`,
          background: color,
        }}
      />
    </div>
  );
}