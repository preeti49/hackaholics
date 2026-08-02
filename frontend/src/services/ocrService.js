import { uploadFile, extractFields } from "./api";

export async function processDocument({ file, patientName, language = "English" }) {
  // Step 1: upload
  const formData = new FormData();
  formData.append("file", file);
  formData.append("patient_name", patientName);
  const uploadRes = await uploadFile(formData);

  const { document_id, filename, file_type } = uploadRes.data;

  // Step 2: extract + validate
  const extractRes = await extractFields({ document_id, filename, file_type, language });

  return {
    documentId: document_id,
    filename,
    ...extractRes.data,
  };
}