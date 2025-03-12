import { createApp } from 'vue'
import './assets/style.css'
import App from './App.vue'
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

createApp(App).mount('#app')