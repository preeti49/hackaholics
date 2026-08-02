import { Routes, Route } from "react-router-dom";
import LandingPage from "../pages/LandingPage";
import PatientDashboard from "../pages/PatientDashboard";
import PatientHistory from "../pages/PatientHistory";
import DoctorDashboard from "../pages/DoctorDashboard";
import DoctorDetails from "../pages/DoctorDetails";
import DoctorPrescription from "../pages/DoctorPrescription";
import ReceptionistDashboard from "../pages/ReceptionistDashboard";
import ReceptionistWorkflow from "../pages/ReceptionistWorkflow";
import AnalyticsReports from "../pages/AnalyticsReport";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/patient/dashboard" element={<PatientDashboard />} />
      <Route path="/patient/history" element={<PatientHistory />} />
      <Route path="/doctor/dashboard" element={<DoctorDashboard />} />
      <Route path="/doctor/patient/:id" element={<DoctorDetails />} />
      <Route path="/doctor/prescription" element={<DoctorPrescription />} />
      <Route path="/receptionist/dashboard" element={<ReceptionistDashboard />} />
      <Route path="/receptionist/workflow" element={<ReceptionistWorkflow />} />
      <Route path="/analytics" element={<AnalyticsReports />} />
    </Routes>
  );
}