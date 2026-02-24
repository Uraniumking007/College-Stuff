import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    port: 4200,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    target: 'es2015'
  }
})
