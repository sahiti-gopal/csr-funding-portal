import api from "../api/axios";

export const getProjectTypes = async () => {
  const response = await api.get("/project-types");
  return response.data;
};