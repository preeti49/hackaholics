import axios from "axios";

const API = axios.create({ baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000/api" });

export const uploadFile = (formData) => API.post("/upload", formData);
export const extractFields = (payload) => API.post("/extract", payload);
export const generateFollowup = (payload) => API.post("/generate-followup", payload);
export const getDocuments = () => API.get("/documents");
export const getAnalytics = () => API.get("/analytics");
export const login = (payload) => API.post("/auth/login", payload);
export const register = (payload) => API.post("/auth/register", payload);
export const searchPatients = (query) => API.get(`/patients/search?q=${encodeURIComponent(query)}`);
export const getPatient = (id) => API.get(`/patients/${id}`);
export const updatePatient = (id, payload) => API.put(`/patients/${id}`, payload);
export const getAppointments = (params = {}) => API.get("/appointments", { params });
export const createAppointment = (payload) => API.post("/appointments/create", payload);
export const updateAppointmentStatus = (id, status) => API.put(`/appointments/${id}/status`, { status });
export const getAvailableDoctors = (specialty) => API.get("/appointments/available-doctors", { params: { specialty } });
export const savePrescription = (payload) => API.post("/prescriptions", payload);
export const getPrescriptions = (patient) => API.get("/prescriptions", { params: { patient } });
export const sendNotification = (payload) => API.post("/notifications/send", payload);
export const processAdministrativeBatch = (formData) => API.post("/administrative/process-batch", formData);
export const generatePaperwork = (payload) => API.post("/generate-paperwork", payload);
