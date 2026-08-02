import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import { getAppointments, updateAppointmentStatus } from "../services/api";

export default function DoctorDashboard() {
  const user = JSON.parse(localStorage.getItem("mamacare_user") || "{}");
  const [rows, setRows] = useState([]);
  const [error, setError] = useState("");
  const nav = useNavigate();
  const load = () => getAppointments({ doctor: user.name })
    .then(r => setRows(r.data))
    .catch(() => setError("Start the Flask backend to load the live queue."));

  useEffect(() => { load(); }, []);
  const updateStatus = async (appointment, nextStatus) => {
    try { await updateAppointmentStatus(appointment.id, nextStatus); load(); }
    catch { setError("Could not update this appointment."); }
  };

  const stats = [
    ["Waiting", rows.filter(x => x.status === "Waiting").length, "text-amber-600"],
    ["In consultation", rows.filter(x => x.status === "In Consultation").length, "text-blue-600"],
    ["Completed", rows.filter(x => x.status === "Completed").length, "text-emerald-600"],
  ];

  return <div className="flex min-h-screen bg-slate-50">
    <Sidebar role="doctor"/>
    <main className="flex-1 p-5 md:p-8">
      <p className="text-sm text-blue-600 font-semibold">CLINICAL WORKSPACE</p>
      <h1 className="text-2xl font-bold">Today’s patient queue</h1>
      <p className="text-sm text-slate-500 mb-6">Open a patient, review their context and write a prescription that appears instantly in their portal.</p>
      {error && <p className="p-3 mb-4 bg-amber-50 rounded-lg text-sm text-amber-800">{error}</p>}
      <div className="grid grid-cols-3 gap-4 mb-6">{stats.map(([label, value, color]) => <div key={label} className="bg-white p-4 rounded-2xl"><b className={`text-2xl ${color}`}>{value}</b><p className="text-xs text-slate-500">{label}</p></div>)}</div>
      <section className="bg-white rounded-2xl border border-slate-100 overflow-hidden">
        <table className="w-full text-sm"><thead className="bg-slate-50 text-slate-500 text-xs"><tr><th className="p-3 text-left">Token</th><th className="text-left">Patient</th><th className="text-left">Reason</th><th className="text-left">Status</th><th></th></tr></thead><tbody>{rows.map(a => <tr key={a.id} className="border-t"><td className="p-3 font-semibold">{a.token_no}</td><td><b>{a.patient_name}</b><br/><span className="text-xs text-slate-500">{a.appointment_time}</span></td><td>{a.reason}</td><td><span className="text-xs bg-slate-100 rounded px-2 py-1">{a.status}</span></td><td className="p-3 text-right"><button onClick={() => { localStorage.setItem("mamacare_appointment", JSON.stringify(a)); nav("/doctor/prescription"); }} className="text-blue-600 mr-3">Consult</button>{a.status === "Waiting" && <button onClick={() => updateStatus(a, "In Consultation")} className="text-slate-600">Start</button>}</td></tr>)}</tbody></table>
        {!rows.length && !error && <p className="p-5 text-sm text-slate-500">No appointments assigned yet.</p>}
      </section>
    </main>
  </div>;
}
