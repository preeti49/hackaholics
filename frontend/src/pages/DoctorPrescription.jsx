import { useState } from "react";
import Sidebar from "../components/Sidebar";
import { savePrescription } from "../services/api";
import AiAssistant from "../components/AiAssistant";

const defaultMeds = [
  { name: "D3 Tablet", dosage: "60K IU", duration: "Once a week" },
  { name: "Calcium Tablet", dosage: "500 mg", duration: "Once a day" },
];

export default function DoctorPrescription() {
  const [meds, setMeds] = useState(defaultMeds);
  const [saved, setSaved] = useState(false);
  const [diagnosis, setDiagnosis] = useState("Vitamin D Deficiency");
  const [symptoms, setSymptoms] = useState("Fatigue, Body Pain");
  const [advice, setAdvice] = useState("Take sunlight daily for 20 minutes. Eat Vitamin D rich food.");
  const appointment = JSON.parse(localStorage.getItem("mamacare_appointment") || "{}");
  const user = JSON.parse(localStorage.getItem("mamacare_user") || "{}");

  const addMed = () => setMeds([...meds, { name: "", dosage: "", duration: "" }]);

  const updateMed = (i, field, val) => {
    const updated = [...meds];
    updated[i][field] = val;
    setMeds(updated);
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar role="doctor" />
      <main className="flex-1 p-8">
        <h1 className="text-xl font-semibold text-gray-800 mb-6">New Prescription</h1>

        <div className="grid grid-cols-2 gap-6">
          {/* Prescription form */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="space-y-4 mb-6">
              <div>
                <label className="text-xs font-medium text-gray-500 mb-1 block">Diagnosis</label>
                <input value={diagnosis} onChange={e => setDiagnosis(e.target.value)}
                  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300" />
              </div>
              <div>
                <label className="text-xs font-medium text-gray-500 mb-1 block">Symptoms</label>
                <input value={symptoms} onChange={e => setSymptoms(e.target.value)}
                  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300" />
              </div>
              <div>
                <label className="text-xs font-medium text-gray-500 mb-1 block">Advice / Notes</label>
                <textarea value={advice} onChange={e => setAdvice(e.target.value)}
                  rows={3}
                  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300 resize-none" />
              </div>
            </div>

            <h3 className="font-semibold text-gray-700 text-sm mb-3">Medicines</h3>
            <table className="w-full text-sm mb-3">
              <thead>
                <tr className="text-gray-400 text-xs border-b">
                  <th className="text-left pb-2 font-medium">Medicine Name</th>
                  <th className="text-left pb-2 font-medium">Dosage</th>
                  <th className="text-left pb-2 font-medium">Duration</th>
                </tr>
              </thead>
              <tbody>
                {meds.map((m, i) => (
                  <tr key={i} className="border-b last:border-0">
                    <td className="py-2">
                      <input value={m.name} onChange={e => updateMed(i, "name", e.target.value)}
                        className="w-full border border-gray-100 rounded px-2 py-1 text-xs focus:outline-none" />
                    </td>
                    <td className="py-2">
                      <input value={m.dosage} onChange={e => updateMed(i, "dosage", e.target.value)}
                        className="w-full border border-gray-100 rounded px-2 py-1 text-xs focus:outline-none" />
                    </td>
                    <td className="py-2">
                      <input value={m.duration} onChange={e => updateMed(i, "duration", e.target.value)}
                        className="w-full border border-gray-100 rounded px-2 py-1 text-xs focus:outline-none" />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <button onClick={addMed} className="text-blue-600 text-xs hover:underline mb-4 block">
              + Add Medicine
            </button>

            {saved && (
              <div className="bg-green-50 text-green-700 text-xs px-3 py-2 rounded-lg mb-3">
                Prescription saved successfully!
              </div>
            )}
            <button
              onClick={async () => {
                try {
                  await savePrescription({ patient_name: appointment.patient_name || "Rahul Sharma", doctor_name: user.name || "Dr. Arvind Sharma", appointment_id: appointment.id, diagnosis, symptoms, advice, medicines: meds });
                  setSaved(true);
                } catch { alert("Could not save. Please make sure the backend is running."); }
              }}
              className="w-full bg-green-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-green-700"
            >
              Save Prescription
            </button>
          </div>

          {/* Additional actions */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="font-semibold text-gray-700 mb-4 text-sm">Additional Actions</h2>
            <div className="flex flex-col gap-3">
              <button className="flex items-center gap-3 border border-gray-200 rounded-xl p-4 hover:bg-gray-50 text-left">
                <span className="text-xl">🩻</span>
                <div>
                  <p className="font-medium text-gray-800 text-sm">Request MRI</p>
                  <p className="text-xs text-gray-400">Send MRI request to lab</p>
                </div>
              </button>
              <button className="flex items-center gap-3 border border-gray-200 rounded-xl p-4 hover:bg-gray-50 text-left">
                <span className="text-xl">🩸</span>
                <div>
                  <p className="font-medium text-gray-800 text-sm">Request Blood Test</p>
                  <p className="text-xs text-gray-400">Send blood test request</p>
                </div>
              </button>
              <button className="flex items-center gap-3 border border-gray-200 rounded-xl p-4 hover:bg-gray-50 text-left">
                <span className="text-xl">📄</span>
                <div>
                  <p className="font-medium text-gray-800 text-sm">Upload Report</p>
                  <p className="text-xs text-gray-400">Attach lab or scan report</p>
                </div>
              </button>
            </div>
          </div>
        </div>
      <AiAssistant context="prescription" />
      </main>
    </div>
  );
}
