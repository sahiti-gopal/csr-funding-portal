export default function ProgressBar({
  value,
  color = "#2563EB",
  height = 8,
}) {
  return (
    <div
      className="progress-track"
      style={{
        height,
      }}
    >
      <div
        className="progress-fill"
        style={{
          width: `${value}%`,
          background: color,
        }}
      />
    </div>
  );
}