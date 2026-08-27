import api from "../api/axios";

export const listConversations = async () => {
  const response = await api.get("/conversations");
  return response.data;
};

export const createConversation = async () => {
  const response = await api.post("/conversations");
  return response.data;
};

export const getConversation = async (id) => {
  const response = await api.get(`/conversations/${id}`);
  return response.data;
};

export const sendMessage = async (conversationId, message) => {
  const response = await api.post(`/conversations/${conversationId}/messages`, {
    message,
  });
  return response.data;
};

export const deleteConversation = async (id) => {
  const response = await api.delete(`/conversations/${id}`);
  return response.data;
};

export const submitMessageFeedback = async (messageId, rating) => {
  const response = await api.post(`/messages/${messageId}/feedback`, { rating });
  return response.data;
};
