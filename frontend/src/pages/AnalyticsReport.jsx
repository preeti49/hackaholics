import { useEffect, useState } from "react";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import Sidebar from "../components/Sidebar";
import { getAnalytics } from "../services/api";

const COLORS = ["#3B82F6", "#F59E0B", "#EF4444", "#10B981"];

const barData = [
  { name: "Insurance No.", missing: 38 },
  { name: "Policy Doc.", missing: 28 },
  { name: "Contact No.", missing: 18 },
  { name: "Address", missing: 12 },
  { name: "Others", missing: 8 },
];

export default function AnalyticsReports() {
  const [analytics, setAnalytics] = useState({
    total: 124, pending: 30, missing: 20, avg_completeness: 68
  });

  useEffect(() => {
    getAnalytics().then(r => setAnalytics(r.data)).catch(() => {});
  }, []);

  const pieData = [
    { name: "Completed", value: 60 },
    { name: "Pending", value: 30 },
    { name: "Missing Info", value: analytics.missing || 20 },
    { name: "Insurance", value: 14 },
  ];

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar role="receptionist" />
      <main className="flex-1 p-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-xl font-semibold text-gray-800">Analytics Overview</h1>
          <div className="flex gap-3">
            <select className="border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none">
              <option>This Month</option>
              <option>Last Month</option>
              <option>Last 3 Months</option>
            </select>
            <button className="bg-blue-600 text-white px-4 py-1.5 rounded-lg text-sm hover:bg-blue-700">
              Export
            </button>
          </div>
        </div>

        {/* Stat cards */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          {[
            { label: "Total Documents", value: analytics.total || 124, color: "text-blue-600" },
            { label: "Average Completeness", value: `${analytics.avg_completeness || 68}%`, color: "text-green-600" },
            { label: "Emails / SMS Sent", value: 32, color: "text-yellow-600" },
            { label: "Insurance Applied", value: 15, color: "text-purple-600" },
          ].map(s => (
            <div key={s.label} className="bg-white rounded-xl p-5 shadow-sm">
              <p className={`text-3xl font-bold ${s.color}`}>{s.value}</p>
              <p className="text-xs text-gray-400 mt-1">{s.label}</p>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-2 gap-6">
          {/* Pie chart */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="font-semibold text-gray-700 mb-4 text-sm">Documents Status</h2>
            <div className="flex items-center gap-6">
              <ResponsiveContainer width={160} height={160}>
                <PieChart>
                  <Pie data={pieData} cx="50%" cy="50%" innerRadius={45} outerRadius={70} dataKey="value">
                    {pieData.map((_, i) => (
                      <Cell key={i} fill={COLORS[i % COLORS.length]} />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
              <div className="flex flex-col gap-2">
                <p className="text-2xl font-bold text-gray-800 text-center">{analytics.total || 124}<br />
                  <span className="text-xs font-normal text-gray-400">Total</span>
                </p>
                {pieData.map((d, i) => (
                  <div key={d.name} className="flex items-center gap-2 text-xs">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ background: COLORS[i] }} />
                    <span className="text-gray-500">{d.name} ({d.value})</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Bar chart */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="font-semibold text-gray-700 mb-4 text-sm">Missing Fields Analysis</h2>
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={barData} barSize={28}>
                <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip />
                <Bar dataKey="missing" fill="#3B82F6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </main>
    </div>
  );
}