import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  define: {
    "process.env.VITE_API_URL": JSON.stringify("https://balance-scale-addition-game.onrender.com"),
  },
  plugins: [vue()],
})
