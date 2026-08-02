import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";

const visits = [
  { date: "12 May 2024", label: "Visit 3", type: "Blood Test", notes: "All parameters normal except Vitamin D is low.", color: "bg-green-500" },
  { date: "20 Apr 2024", label: "Visit 2", type: "X-Ray Chest", notes: "No signs of infection. Lungs are clear.", color: "bg-blue-500" },
  { date: "10 Mar 2024", label: "Visit 1", type: "MRI Scan", notes: "No abnormalities detected.", color: "bg-purple-500" },
];

export default function PatientHistory() {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar role="patient" />
      <main className="flex-1 p-8">
        <h1 className="text-xl font-semibold text-gray-800 mb-1">Medical History</h1>
        <p className="text-sm text-gray-400 mb-6">Your complete medical journey</p>

        <div className="grid grid-cols-2 gap-6">
          {/* Timeline */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="relative">
              <div className="absolute left-3 top-0 bottom-0 w-0.5 bg-gray-100" />
              <div className="flex flex-col gap-6">
                {visits.map((v, i) => (
                  <div key={i} className="flex gap-4 relative">
                    <div className={`w-6 h-6 rounded-full ${v.color} flex-shrink-0 z-10 flex items-center justify-center`}>
                      <div className="w-2 h-2 bg-white rounded-full" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-xs text-gray-400">{v.date}</p>
                          <p className="font-semibold text-gray-800 text-sm">{v.label}</p>
                          <p className="text-sm text-gray-600">{v.type}</p>
                          <p className="text-xs text-gray-400 mt-1">{v.notes}</p>
                        </div>
                        <button className="text-blue-600 border border-blue-200 rounded-lg p-2 hover:bg-blue-50">
                          📄
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* AI Health Insights */}
          <div className="flex flex-col gap-4">
            <div className="bg-blue-50 rounded-xl p-5 shadow-sm">
              <h2 className="font-semibold text-blue-700 mb-2 text-sm">AI Health Insights</h2>
              <p className="text-sm text-gray-700 leading-relaxed">
                Your overall health is good. Maintain a balanced diet and regular exercise. Your Vitamin D levels need attention — consider supplements and more sunlight exposure.
              </p>
              <button className="mt-3 bg-blue-600 text-white text-xs px-4 py-2 rounded-lg hover:bg-blue-700 w-full">
                Download Summary
              </button>
            </div>

            <div className="bg-white rounded-xl p-5 shadow-sm">
              <h2 className="font-semibold text-gray-700 mb-2 text-sm">Need Help?</h2>
              <p className="text-xs text-gray-400 mb-3">
                Chat with our AI Assistant for any health-related questions.
              </p>
              <button className="bg-blue-600 text-white text-xs px-4 py-2 rounded-lg hover:bg-blue-700 w-full">
                Chat Now
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}