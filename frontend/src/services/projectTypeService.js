import api from "../api/axios";

export const getProjectTypes = async () => {
  const response = await api.get("/project-types");
  return response.data;
};

export const createProjectType = async (payload) => {
  const response = await api.post("/project-types", payload);
  return response.data;
};

export const updateProjectType = async (id, payload) => {
  const response = await api.put(`/project-types/${id}`, payload);
  return response.data;
};

export const deleteProjectType = async (id) => {
  const response = await api.delete(`/project-types/${id}`);
  return response.data;
};
