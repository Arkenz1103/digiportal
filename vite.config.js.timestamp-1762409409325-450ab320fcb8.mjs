// vite.config.js
import { defineConfig } from "file:///C:/Users/ACER/Downloads/digiportal/node_modules/vite/dist/node/index.js";
import vue from "file:///C:/Users/ACER/Downloads/digiportal/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import Components from "file:///C:/Users/ACER/Downloads/digiportal/node_modules/unplugin-vue-components/dist/vite.js";
import { PrimeVueResolver } from "file:///C:/Users/ACER/Downloads/digiportal/node_modules/@primevue/auto-import-resolver/index.mjs";
var vite_config_default = defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [
        PrimeVueResolver()
      ]
    })
  ],
  server: {
    port: 5173,
    strictPort: true,
    host: "localhost",
    cors: true,
    hmr: {
      host: "localhost",
      protocol: "ws",
      overlay: true
    },
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false
      }
    },
    watch: {
      usePolling: true,
      interval: 100,
      ignored: [
        "**/be/**",
        // Ignore Django backend folder
        "**/node_modules/**",
        "**/.git/**",
        "**/__pycache__/**",
        "**/*.pyc"
      ]
    }
  },
  build: {
    manifest: true,
    outDir: "public/build",
    rollupOptions: {
      input: "resources/js/app.js"
    }
  },
  resolve: {
    alias: {
      "@": "/resources/js"
    }
  },
  optimizeDeps: {
    include: ["vue", "axios"],
    exclude: []
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxBQ0VSXFxcXERvd25sb2Fkc1xcXFxkaWdpcG9ydGFsXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxBQ0VSXFxcXERvd25sb2Fkc1xcXFxkaWdpcG9ydGFsXFxcXHZpdGUuY29uZmlnLmpzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9DOi9Vc2Vycy9BQ0VSL0Rvd25sb2Fkcy9kaWdpcG9ydGFsL3ZpdGUuY29uZmlnLmpzXCI7aW1wb3J0IHsgZGVmaW5lQ29uZmlnIH0gZnJvbSAndml0ZSc7XG5pbXBvcnQgdnVlIGZyb20gJ0B2aXRlanMvcGx1Z2luLXZ1ZSc7XG5pbXBvcnQgQ29tcG9uZW50cyBmcm9tICd1bnBsdWdpbi12dWUtY29tcG9uZW50cy92aXRlJztcbmltcG9ydCB7UHJpbWVWdWVSZXNvbHZlcn0gZnJvbSAnQHByaW1ldnVlL2F1dG8taW1wb3J0LXJlc29sdmVyJztcblxuZXhwb3J0IGRlZmF1bHQgZGVmaW5lQ29uZmlnKHtcbiAgICBwbHVnaW5zOiBbXG4gICAgICAgIHZ1ZSgpLFxuICAgICAgICBDb21wb25lbnRzKHtcbiAgICAgICAgICAgIHJlc29sdmVyczogW1xuICAgICAgICAgICAgICBQcmltZVZ1ZVJlc29sdmVyKClcbiAgICAgICAgICAgIF1cbiAgICAgICAgfSksXG4gICAgXSxcbiAgICBzZXJ2ZXI6IHtcbiAgICAgICAgcG9ydDogNTE3MyxcbiAgICAgICAgc3RyaWN0UG9ydDogdHJ1ZSxcbiAgICAgICAgaG9zdDogJ2xvY2FsaG9zdCcsXG4gICAgICAgIGNvcnM6IHRydWUsXG4gICAgICAgIGhtcjoge1xuICAgICAgICAgICAgaG9zdDogJ2xvY2FsaG9zdCcsXG4gICAgICAgICAgICBwcm90b2NvbDogJ3dzJyxcbiAgICAgICAgICAgIG92ZXJsYXk6IHRydWUsXG4gICAgICAgIH0sXG4gICAgICAgIHByb3h5OiB7XG4gICAgICAgICAgICAnL2FwaSc6IHtcbiAgICAgICAgICAgICAgICB0YXJnZXQ6ICdodHRwOi8vbG9jYWxob3N0OjgwMDAnLFxuICAgICAgICAgICAgICAgIGNoYW5nZU9yaWdpbjogdHJ1ZSxcbiAgICAgICAgICAgICAgICBzZWN1cmU6IGZhbHNlLFxuICAgICAgICAgICAgfSxcbiAgICAgICAgfSxcbiAgICAgICAgd2F0Y2g6IHtcbiAgICAgICAgICAgIHVzZVBvbGxpbmc6IHRydWUsXG4gICAgICAgICAgICBpbnRlcnZhbDogMTAwLFxuICAgICAgICAgICAgaWdub3JlZDogW1xuICAgICAgICAgICAgICAgICcqKi9iZS8qKicsICAgICAgICAgICAvLyBJZ25vcmUgRGphbmdvIGJhY2tlbmQgZm9sZGVyXG4gICAgICAgICAgICAgICAgJyoqL25vZGVfbW9kdWxlcy8qKicsXG4gICAgICAgICAgICAgICAgJyoqLy5naXQvKionLFxuICAgICAgICAgICAgICAgICcqKi9fX3B5Y2FjaGVfXy8qKicsXG4gICAgICAgICAgICAgICAgJyoqLyoucHljJyxcbiAgICAgICAgICAgIF1cbiAgICAgICAgfSxcbiAgICB9LFxuICAgIGJ1aWxkOiB7XG4gICAgICAgIG1hbmlmZXN0OiB0cnVlLFxuICAgICAgICBvdXREaXI6ICdwdWJsaWMvYnVpbGQnLFxuICAgICAgICByb2xsdXBPcHRpb25zOiB7XG4gICAgICAgICAgICBpbnB1dDogJ3Jlc291cmNlcy9qcy9hcHAuanMnLFxuICAgICAgICB9LFxuICAgIH0sXG4gICAgcmVzb2x2ZToge1xuICAgICAgICBhbGlhczoge1xuICAgICAgICAgICAgJ0AnOiAnL3Jlc291cmNlcy9qcycsXG4gICAgICAgIH0sXG4gICAgfSxcbiAgICBvcHRpbWl6ZURlcHM6IHtcbiAgICAgICAgaW5jbHVkZTogWyd2dWUnLCAnYXhpb3MnXSxcbiAgICAgICAgZXhjbHVkZTogW10sXG4gICAgfSxcbn0pO1xuIl0sCiAgIm1hcHBpbmdzIjogIjtBQUFrUyxTQUFTLG9CQUFvQjtBQUMvVCxPQUFPLFNBQVM7QUFDaEIsT0FBTyxnQkFBZ0I7QUFDdkIsU0FBUSx3QkFBdUI7QUFFL0IsSUFBTyxzQkFBUSxhQUFhO0FBQUEsRUFDeEIsU0FBUztBQUFBLElBQ0wsSUFBSTtBQUFBLElBQ0osV0FBVztBQUFBLE1BQ1AsV0FBVztBQUFBLFFBQ1QsaUJBQWlCO0FBQUEsTUFDbkI7QUFBQSxJQUNKLENBQUM7QUFBQSxFQUNMO0FBQUEsRUFDQSxRQUFRO0FBQUEsSUFDSixNQUFNO0FBQUEsSUFDTixZQUFZO0FBQUEsSUFDWixNQUFNO0FBQUEsSUFDTixNQUFNO0FBQUEsSUFDTixLQUFLO0FBQUEsTUFDRCxNQUFNO0FBQUEsTUFDTixVQUFVO0FBQUEsTUFDVixTQUFTO0FBQUEsSUFDYjtBQUFBLElBQ0EsT0FBTztBQUFBLE1BQ0gsUUFBUTtBQUFBLFFBQ0osUUFBUTtBQUFBLFFBQ1IsY0FBYztBQUFBLFFBQ2QsUUFBUTtBQUFBLE1BQ1o7QUFBQSxJQUNKO0FBQUEsSUFDQSxPQUFPO0FBQUEsTUFDSCxZQUFZO0FBQUEsTUFDWixVQUFVO0FBQUEsTUFDVixTQUFTO0FBQUEsUUFDTDtBQUFBO0FBQUEsUUFDQTtBQUFBLFFBQ0E7QUFBQSxRQUNBO0FBQUEsUUFDQTtBQUFBLE1BQ0o7QUFBQSxJQUNKO0FBQUEsRUFDSjtBQUFBLEVBQ0EsT0FBTztBQUFBLElBQ0gsVUFBVTtBQUFBLElBQ1YsUUFBUTtBQUFBLElBQ1IsZUFBZTtBQUFBLE1BQ1gsT0FBTztBQUFBLElBQ1g7QUFBQSxFQUNKO0FBQUEsRUFDQSxTQUFTO0FBQUEsSUFDTCxPQUFPO0FBQUEsTUFDSCxLQUFLO0FBQUEsSUFDVDtBQUFBLEVBQ0o7QUFBQSxFQUNBLGNBQWM7QUFBQSxJQUNWLFNBQVMsQ0FBQyxPQUFPLE9BQU87QUFBQSxJQUN4QixTQUFTLENBQUM7QUFBQSxFQUNkO0FBQ0osQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
