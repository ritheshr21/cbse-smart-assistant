import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

const BACKEND = 'http://127.0.0.1:8000'
const API_PATHS = ['/chat', '/generate-quiz', '/evaluate', '/submit-mcq', '/health', '/pdfs']

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: Object.fromEntries(
      API_PATHS.map((path) => [path, { target: BACKEND, changeOrigin: true }])
    ),
  },
})
