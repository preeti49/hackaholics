export default function Table({ columns, data, onRowClick }) {
  if (!data || data.length === 0) {
    return (
      <div className="text-center py-10 text-sm text-gray-400">
        No records found.
      </div>
    );
  }

  return (
    <table className="w-full text-sm">
      <thead>
        <tr className="text-gray-400 text-xs border-b">
          {columns.map((col) => (
            <th key={col.key} className="text-left pb-3 font-medium pr-4">
              {col.label}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr
            key={i}
            onClick={() => onRowClick && onRowClick(row)}
            className={`border-b last:border-0 ${onRowClick ? "cursor-pointer hover:bg-gray-50" : ""}`}
          >
            {columns.map((col) => (
              <td key={col.key} className="py-3 pr-4">
                {col.render ? col.render(row[col.key], row) : (
                  <span className="text-gray-700">{row[col.key] ?? "—"}</span>
                )}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}