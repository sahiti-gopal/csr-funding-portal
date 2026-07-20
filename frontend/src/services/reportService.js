import api from "../api/axios";

export const listReports = async () => {
  const response = await api.get("/reports");
  return response.data;
};

export const previewReport = async (donorId, financialYear) => {
  const response = await api.get("/reports/preview", {
    params: { donor_id: donorId, financial_year: financialYear },
  });
  return response.data;
};

export const generateReport = async (donorId, financialYear) => {
  const response = await api.post("/reports", {
    donor_id: donorId,
    financial_year: financialYear,
  });
  return response.data;
};

export const getReport = async (id) => {
  const response = await api.get(`/reports/${id}`);
  return response.data;
};

export const retryReport = async (id) => {
  const response = await api.post(`/reports/${id}/retry`);
  return response.data;
};

export const approveReport = async (id) => {
  const response = await api.post(`/reports/${id}/approve`);
  return response.data;
};

export const deliverReport = async (id) => {
  const response = await api.post(`/reports/${id}/deliver`);
  return response.data;
};
