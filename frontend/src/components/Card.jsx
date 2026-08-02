export default function Card({ title, value, color = "text-blue-600", subtitle }) {
  return (
    <div className="bg-white rounded-xl p-5 shadow-sm">
      <p className={`text-3xl font-bold ${color}`}>{value}</p>
      <p className="text-xs text-gray-500 mt-1 font-medium">{title}</p>
      {subtitle && <p className="text-xs text-gray-400 mt-0.5">{subtitle}</p>}
    </div>
  );
}