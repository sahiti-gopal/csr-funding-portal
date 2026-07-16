import api from "../api/axios";

export const getBeneficiaryCategories = async () => {
  const response = await api.get("/beneficiary-categories");
  return response.data;
};