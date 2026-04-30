// frontend/src/api/client.js
import axios from "axios";

const client = axios.create({
  baseURL: "/", // Uses Vite proxy — no hardcoded port
  timeout: 5000,
});

export default client;
