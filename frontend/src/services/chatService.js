import api from "../api/axios";

export const sendChatMessage = async (message, page) => {
  const response = await api.post("/chat", { message, page });
  return response.data;
};
