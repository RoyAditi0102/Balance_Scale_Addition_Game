import axios from 'axios';

const api = axios.create({
  baseURL:  'http://127.0.0.1:8000' || import.meta.env.VITE_API_BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type' : 'application/json',
  },
});

export default api;
