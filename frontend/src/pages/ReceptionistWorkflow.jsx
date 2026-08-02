import { useState } from "react";
import Sidebar from "../components/Sidebar";
import { uploadFile, extractFields, generateFollowup, sendNotification, processAdministrativeBatch, generatePaperwork } from "../services/api";

const steps = ["Upload Document", "Extract Information", "Check Missing Fields", "Insurance (if required)", "Review & Submit"];

export default function ReceptionistWorkflow() {
  const [file, setFile] = useState(null);
  const [patientName, setPatientName] = useState("");
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);
  const [result, setResult] = useState(null);
  const [followup, setFollowup] = useState("");
  const [notificationStatus, setNotificationStatus] = useState("");
  const [batchFiles, setBatchFiles] = useState([]);
  const [workflowType, setWorkflowType] = useState("Intake Form");
  const [batchResults, setBatchResults] = useState([]);
  const [paperworkDraft, setPaperworkDraft] = useState("");

  const handleUploadAndExtract = async () => {
    if (!file || !patientName) return alert("Please provide file and patient name");
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("patient_name", patientName);

      const uploadRes = await uploadFile(formData);
      const { document_id, filename, file_type } = uploadRes.data;
      setStep(1);

      const extractRes = await extractFields({ document_id, filename, file_type });
      setResult(extractRes.data);
      setStep(extractRes.data.missing_fields.length > 0 ? 2 : 4);

      if (extractRes.data.missing_fields.length > 0) {
        const followupRes = await generateFollowup({
          patient_name: patientName,
          missing_fields: extractRes.data.missing_fields,
        });
        setFollowup(followupRes.data.followup_message);
        setStep(3);
      }
    } catch (err) {
      alert("Error processing document. Check backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const notifyPatient = async (channel) => {
    try {
      await sendNotification({ patient_name: patientName, document_id: result?.document_id, title: `Missing information — ${channel}`, message: followup, missing_fields: result?.missing_fields || [] });
      setNotificationStatus(`${channel} request saved and sent to the patient inbox.`);
    } catch { setNotificationStatus("Could not send the request. Please check the backend."); }
  };

  const processBatch = async () => {
    if (!batchFiles.length || !patientName) return alert("Enter a patient name and choose one or more files.");
    setLoading(true);
    try {
      const formData = new FormData();
      batchFiles.forEach(file => formData.append("files", file));
      formData.append("patient_name", patientName);
      formData.append("workflow_type", workflowType);
      const response = await processAdministrativeBatch(formData);
      setBatchResults(response.data.results || []);
    } catch { setNotificationStatus("Batch processing could not complete. The files were not submitted."); }
    finally { setLoading(false); }
  };

  const draftPaperwork = async (item) => {
    const response = await generatePaperwork({ workflow_type: workflowType, patient_name: patientName, fields: item.extracted_fields, missing_fields: item.missing_fields });
    setPaperworkDraft(response.data.draft);
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar role="receptionist" />
      <main className="flex-1 p-8">
        <h1 className="text-xl font-semibold text-gray-800 mb-6">Document Workflow</h1>

        {/* Step bar */}
        <div className="flex items-center gap-0 mb-8">
          {steps.map((s, i) => (
            <div key={s} className="flex items-center">
              <div className="flex flex-col items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold
                  ${i <= step ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-500"}`}>
                  {i + 1}
                </div>
                <span className="text-xs text-gray-500 mt-1 w-20 text-center">{s}</span>
              </div>
              {i < steps.length - 1 && (
                <div className={`h-0.5 w-16 mb-5 ${i < step ? "bg-blue-600" : "bg-gray-200"}`}/>
              )}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-2 gap-6">
          {/* Upload */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="font-semibold text-gray-700 mb-4">Upload Document</h2>
            <input
              type="text"
              placeholder="Patient Name"
              value={patientName}
              onChange={(e) => setPatientName(e.target.value)}
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm mb-3 focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
            <label className="border-2 border-dashed border-gray-200 rounded-xl p-6 flex flex-col items-center gap-2 cursor-pointer hover:border-blue-400 transition-colors">
              <span className="text-3xl">📄</span>
              <span className="text-sm text-gray-500">Drag & Drop or click to browse</span>
              <span className="text-xs text-gray-400">PDF, JPG, PNG</span>
              {file && <span className="text-xs text-blue-600 font-medium">{file.name}</span>}
              <input type="file" accept=".pdf,.jpg,.jpeg,.png" className="hidden"
                onChange={(e) => setFile(e.target.files[0])} />
            </label>
            <button
              onClick={handleUploadAndExtract}
              disabled={loading}
              className="mt-4 w-full bg-blue-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "Processing..." : "Extract Information"}
            </button>
          </div>

          {/* Results */}
          {result && (
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold text-gray-700">Extracted Information</h2>
                <span className={`text-xs px-2 py-1 rounded-full font-medium
                  ${result.completeness_score === 100 ? "bg-green-100 text-green-700"
                  : result.completeness_score >= 60 ? "bg-yellow-100 text-yellow-700"
                  : "bg-red-100 text-red-700"}`}>
                  {result.completeness_score}% complete
                </span>
              </div>

              <div className="space-y-2 mb-4">
                {Object.entries(result.extracted_fields || {}).map(([key, val]) => (
                  <div key={key} className="flex items-center justify-between text-sm">
                    <span className="text-gray-500 capitalize">{key.replace(/_/g, " ")}</span>
                    <span className={val ? "text-gray-800 font-medium" : "text-red-500 font-medium"}>
                      {val || "Missing"}
                    </span>
                  </div>
                ))}
              </div>

              {result.missing_fields?.length > 0 && (
                <div className="bg-red-50 rounded-lg p-3 mt-3">
                  <p className="text-xs font-semibold text-red-700 mb-1">Missing Information</p>
                  {result.missing_fields.map((f) => (
                    <div key={f} className="flex items-center gap-2 text-xs text-red-600">
                      <span>•</span> {f.replace(/_/g, " ")}
                    </div>
                  ))}
                </div>
              )}

              {result.is_priority && (
                <div className="bg-orange-50 border border-orange-200 rounded-lg p-2 mt-3 text-xs text-orange-700 font-medium">
                  ⚠ Priority case detected
                </div>
              )}
            </div>
          )}
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm mt-6 border border-blue-100">
          <div className="flex items-start justify-between gap-4 mb-4"><div><p className="text-xs font-semibold text-blue-600">ADMINISTRATIVE AUTOMATION</p><h2 className="font-semibold text-gray-800">Batch intake & prior-authorisation processing</h2><p className="text-sm text-gray-500 mt-1">Upload up to 10 intake, insurance or prior-authorisation files. The system extracts fields, flags gaps, and prepares staff-review drafts—without making clinical decisions.</p></div></div>
          <div className="grid md:grid-cols-3 gap-3"><input value={patientName} onChange={e=>setPatientName(e.target.value)} className="border border-gray-200 rounded-lg px-3 py-2 text-sm" placeholder="Patient name"/><select value={workflowType} onChange={e=>setWorkflowType(e.target.value)} className="border border-gray-200 rounded-lg px-3 py-2 text-sm"><option>Intake Form</option><option>Prior Authorization</option><option>Insurance Paperwork</option><option>Auto classify</option></select><input type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.txt,.docx" onChange={e=>setBatchFiles([...e.target.files])} className="border border-gray-200 rounded-lg px-3 py-2 text-sm"/></div>
          <button onClick={processBatch} disabled={loading} className="mt-3 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm disabled:opacity-50">{loading ? "Processing files..." : "Process batch"}</button>
          {batchResults.length > 0 && <div className="mt-5 space-y-3">{batchResults.map((item, index) => <div key={index} className="border rounded-xl p-4"><div className="flex justify-between gap-3"><div><b className="text-sm">{item.filename}</b><p className="text-xs text-gray-500 mt-1">{item.document_type || workflowType} · {item.completeness_score ?? 0}% complete · {item.status}</p>{item.missing_fields?.length > 0 && <p className="text-xs text-red-600 mt-1">Missing: {item.missing_fields.join(", ")}</p>}</div><button onClick={()=>draftPaperwork(item)} className="text-blue-600 text-sm font-medium">Draft paperwork</button></div></div>)}</div>}
          {paperworkDraft && <div className="mt-4 bg-slate-50 rounded-xl p-4"><div className="flex justify-between"><b className="text-sm">Staff review draft</b><button onClick={()=>navigator.clipboard?.writeText(paperworkDraft)} className="text-xs text-blue-600">Copy draft</button></div><pre className="whitespace-pre-wrap text-xs text-gray-700 mt-2 font-sans">{paperworkDraft}</pre></div>}
        </div>

        {/* AI Follow-up Message */}
        {followup && (
          <div className="bg-white rounded-xl p-6 shadow-sm mt-6">
            <h2 className="font-semibold text-gray-700 mb-3">AI Suggestion — Follow-up Message</h2>
            <div className="bg-gray-50 rounded-lg p-4 text-sm text-gray-700 leading-relaxed">{followup}</div>
            <div className="flex gap-3 mt-4">
              <button onClick={() => notifyPatient("Email")} className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-green-700">
                Send Email
              </button>
              <button onClick={() => notifyPatient("SMS")} className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700">Send SMS</button>
              <button className="border border-gray-200 text-gray-600 px-4 py-2 rounded-lg text-sm hover:bg-gray-50"
                onClick={() => { setResult(null); setFollowup(""); setFile(null); setStep(0); }}>
                Extract Again
              </button>
            </div>
            {notificationStatus && <p className="text-xs text-green-700 mt-3">{notificationStatus}</p>}
          </div>
        )}
      </main>
    </div>
  );
}
