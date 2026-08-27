import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Backend routes that return a path like "/api/projects/documents/file/x.pdf"
// (see project_routes.py's _document_url) return it relative to the API's
// origin, not relative to the frontend page — needed for anything embedded
// directly (an <iframe src>, a download <a href>) rather than fetched via
// this axios instance. API_BASE_URL already ends in "/api", and the path
// already starts with it, so this only needs the origin in front of it.
const API_ORIGIN = API_BASE_URL.replace(/\/api\/?$/, "");

export const resolveApiFileUrl = (path) => (path ? `${API_ORIGIN}${path}` : null);

export default api;