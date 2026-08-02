// Field labels shown to the user
export const FIELD_LABELS = {
  patient_name: "Patient Name",
  age: "Age",
  phone: "Phone Number",
  email: "Email Address",
  address: "Address",
  insurance_number: "Insurance Number",
  policy_document: "Policy Document",
  emergency_contact: "Emergency Contact",
  diagnosis: "Diagnosis",
  doctor_name: "Doctor Name",
  visit_date: "Visit Date",
};

// Returns array of { field, label, value, missing }
export function formatValidation(validation) {
  return Object.entries(validation || {}).map(([field, data]) => ({
    field,
    label: FIELD_LABELS[field] || field,
    value: data.value,
    missing: data.missing,
  }));
}

// Color class based on completeness score
export function scoreColor(score) {
  if (score === 100) return "text-green-600 bg-green-50";
  if (score >= 60) return "text-yellow-600 bg-yellow-50";
  return "text-red-600 bg-red-50";
}

// Progress bar color
export function progressColor(score) {
  if (score === 100) return "bg-green-500";
  if (score >= 60) return "bg-yellow-400";
  return "bg-red-400";
}

// Status badge color
export const STATUS_COLORS = {
  "Completed": "bg-green-100 text-green-700",
  "Pending Review": "bg-yellow-100 text-yellow-700",
  "Missing Info": "bg-red-100 text-red-700",
  "Insurance Pending": "bg-blue-100 text-blue-700",
};