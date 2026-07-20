import api from "../api/axios";

export const getDonors = async () => {
  const response = await api.get("/donors");
  return response.data;
};

export const getDonor = async (id) => {
  const response = await api.get(`/donors/${id}`);
  return response.data;
};

export const getDonorAiSummary = async (id) => {
  const response = await api.get(`/donors/${id}/ai-summary`);
  return response.data;
};
