import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
export default defineConfig({
  define: {
    "process.env.VITE_API_URL": "https://your-backend-service.onrender.com",
  },
});

