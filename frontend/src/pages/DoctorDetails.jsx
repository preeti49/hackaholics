import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";

export default function DoctorDetails() {
  const navigate = useNavigate();

  const visits = [
    { date: "12 May 2024", label: "Visit 3", note: "Blood Test — All parameters normal except Vitamin D is low." },
    { date: "20 Apr 2024", label: "Visit 2", note: "X-Ray Chest — No signs of infection. Lungs are clear." },
    { date: "10 Mar 2024", label: "Visit 1", note: "MRI Scan — No abnormalities detected." },
  ];

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar role="doctor" />
      <main className="flex-1 p-8">
        <h1 className="text-xl font-semibold text-gray-800 mb-6">Patient Details</h1>

        <div className="bg-white rounded-xl p-6 shadow-sm mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-gray-200 rounded-full flex items-center justify-center text-2xl">👤</div>
              <div>
                <h2 className="font-semibold text-gray-800 text-lg">Rohit Kumar</h2>
                <p className="text-sm text-gray-400">Age: 28 · Gender: Male · Blood Group: B+</p>
                <p className="text-sm text-gray-400">Phone: 9876543210 · Email: rohit@gmail.com</p>
              </div>
            </div>
            <div className="bg-blue-600 text-white rounded-xl p-4 text-center min-w-24">
              <p className="text-xs opacity-80">Token No.</p>
              <p className="text-2xl font-bold">1054</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6">
          {/* Visit history */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex gap-4 border-b mb-4">
              {["Visit History", "Reports", "Prescriptions", "Insurance"].map((t, i) => (
                <button key={t} className={`pb-3 text-sm font-medium border-b-2 -mb-px transition-colors
                  ${i === 0 ? "border-blue-600 text-blue-600" : "border-transparent text-gray-400 hover:text-gray-600"}`}>
                  {t}
                </button>
              ))}
            </div>
            <div className="space-y-4">
              {visits.map((v, i) => (
                <div key={i} className="flex gap-3">
                  <div className="flex flex-col items-center">
                    <div className="w-3 h-3 rounded-full bg-blue-500 mt-1" />
                    {i < visits.length - 1 && <div className="w-0.5 flex-1 bg-gray-100 my-1" />}
                  </div>
                  <div className="flex-1 pb-2">
                    <p className="text-xs text-gray-400">{v.date}</p>
                    <p className="font-medium text-gray-800 text-sm">{v.label}</p>
                    <p className="text-xs text-gray-500">{v.note}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick actions */}
          <div className="flex flex-col gap-3">
            <div className="bg-white rounded-xl p-5 shadow-sm">
              <h2 className="font-semibold text-gray-700 mb-3 text-sm">Quick Actions</h2>
              <div className="flex flex-col gap-2">
                <button
                  onClick={() => navigate("/doctor/prescription")}
                  className="bg-blue-600 text-white py-2 rounded-lg text-sm hover:bg-blue-700"
                >
                  New Prescription
                </button>
                <button className="bg-yellow-500 text-white py-2 rounded-lg text-sm hover:bg-yellow-600">
                  Request MRI / Test
                </button>
                <button className="bg-green-600 text-white py-2 rounded-lg text-sm hover:bg-green-700">
                  Upload Report
                </button>
                <button className="bg-orange-500 text-white py-2 rounded-lg text-sm hover:bg-orange-600">
                  Start Consultation
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}