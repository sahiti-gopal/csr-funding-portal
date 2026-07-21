import api from "../api/axios";

export const getDonorDocuments = async (donorId) => {
  const response = await api.get(`/donors/${donorId}/documents`);
  return response.data;
};

export const uploadDonorDocument = async (donorId, docId, file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post(
    `/donors/${donorId}/documents/${docId}/upload`,
    formData,
    { headers: { "Content-Type": undefined } }
  );
  return response.data;
};

export const reviewDonorDocument = async (donorId, docId) => {
  const response = await api.post(
    `/donors/${donorId}/documents/${docId}/review`
  );
  return response.data;
};

export const generateDocumentRequest = async (donorId) => {
  const response = await api.post(
    `/donors/${donorId}/documents/generate-request`
  );
  return response.data;
};

export const uploadPaymentDocument = async (paymentId, file, documentType = "Other") => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("document_type", documentType);

  const response = await api.post(
    `/payments/${paymentId}/documents`,
    formData,
    { headers: { "Content-Type": undefined } }
  );
  return response.data;
};
