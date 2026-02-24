import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        // Proxy API calls to FastAPI backend during local development
        proxy: {
            '/upload': 'http://localhost:8000',
        }
    }
})
