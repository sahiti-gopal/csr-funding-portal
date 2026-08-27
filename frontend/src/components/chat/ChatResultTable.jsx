const MAX_VISIBLE_ROWS = 20;

export default function ChatResultTable({ table }) {
  if (!table || !table.rows || table.rows.length === 0) return null;

  const { columns, rows } = table;
  const visibleRows = rows.slice(0, MAX_VISIBLE_ROWS);
  const hiddenCount = rows.length - visibleRows.length;

  return (
    <div className="chat-result-table-wrap">
      <table className="chat-result-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col.replace(/_/g, " ")}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {visibleRows.map((row, i) => (
            <tr key={i}>
              {columns.map((col) => (
                <td key={col}>{String(row[col] ?? "")}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {hiddenCount > 0 && (
        <div className="chat-result-table-more">+{hiddenCount} more rows</div>
      )}
    </div>
  );
}
