import axios from "axios";
import { auth } from "../app/firebase";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/api"
});

api.interceptors.request.use(async (config) => {
  const user = auth.currentUser;
  if (user) {
    try {
      const token = await user.getIdToken(true);
      config.headers.Authorization = `Bearer ${token}`;
    } catch (_) {
      // Token no disponible, la petición se envía sin auth
    }
  }
  return config;
});

export default api;