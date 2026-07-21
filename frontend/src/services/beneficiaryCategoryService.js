import api from "../api/axios";

export const getBeneficiaryCategories = async () => {
  const response = await api.get("/beneficiary-categories");
  return response.data;
};

export const createBeneficiaryCategory = async (payload) => {
  const response = await api.post("/beneficiary-categories", payload);
  return response.data;
};

export const updateBeneficiaryCategory = async (id, payload) => {
  const response = await api.put(`/beneficiary-categories/${id}`, payload);
  return response.data;
};

export const deleteBeneficiaryCategory = async (id) => {
  const response = await api.delete(`/beneficiary-categories/${id}`);
  return response.data;
};
