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
    port: 80,
    strictPort: false,
    host: "0.0.0.0",
    // Allow access from custom domain
    cors: true,
    hmr: {
      host: "digiport.ph",
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
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxBQ0VSXFxcXERvd25sb2Fkc1xcXFxkaWdpcG9ydGFsXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxBQ0VSXFxcXERvd25sb2Fkc1xcXFxkaWdpcG9ydGFsXFxcXHZpdGUuY29uZmlnLmpzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9DOi9Vc2Vycy9BQ0VSL0Rvd25sb2Fkcy9kaWdpcG9ydGFsL3ZpdGUuY29uZmlnLmpzXCI7aW1wb3J0IHsgZGVmaW5lQ29uZmlnIH0gZnJvbSAndml0ZSc7XG5pbXBvcnQgdnVlIGZyb20gJ0B2aXRlanMvcGx1Z2luLXZ1ZSc7XG5pbXBvcnQgQ29tcG9uZW50cyBmcm9tICd1bnBsdWdpbi12dWUtY29tcG9uZW50cy92aXRlJztcbmltcG9ydCB7UHJpbWVWdWVSZXNvbHZlcn0gZnJvbSAnQHByaW1ldnVlL2F1dG8taW1wb3J0LXJlc29sdmVyJztcblxuZXhwb3J0IGRlZmF1bHQgZGVmaW5lQ29uZmlnKHtcbiAgICBwbHVnaW5zOiBbXG4gICAgICAgIHZ1ZSgpLFxuICAgICAgICBDb21wb25lbnRzKHtcbiAgICAgICAgICAgIHJlc29sdmVyczogW1xuICAgICAgICAgICAgICBQcmltZVZ1ZVJlc29sdmVyKClcbiAgICAgICAgICAgIF1cbiAgICAgICAgfSksXG4gICAgXSxcbiAgICBzZXJ2ZXI6IHtcbiAgICAgICAgcG9ydDogODAsXG4gICAgICAgIHN0cmljdFBvcnQ6IGZhbHNlLFxuICAgICAgICBob3N0OiAnMC4wLjAuMCcsIC8vIEFsbG93IGFjY2VzcyBmcm9tIGN1c3RvbSBkb21haW5cbiAgICAgICAgY29yczogdHJ1ZSxcbiAgICAgICAgaG1yOiB7XG4gICAgICAgICAgICBob3N0OiAnZGlnaXBvcnQucGgnLFxuICAgICAgICAgICAgcHJvdG9jb2w6ICd3cycsXG4gICAgICAgICAgICBvdmVybGF5OiB0cnVlLFxuICAgICAgICB9LFxuICAgICAgICBwcm94eToge1xuICAgICAgICAgICAgJy9hcGknOiB7XG4gICAgICAgICAgICAgICAgdGFyZ2V0OiAnaHR0cDovL2xvY2FsaG9zdDo4MDAwJyxcbiAgICAgICAgICAgICAgICBjaGFuZ2VPcmlnaW46IHRydWUsXG4gICAgICAgICAgICAgICAgc2VjdXJlOiBmYWxzZSxcbiAgICAgICAgICAgIH0sXG4gICAgICAgIH0sXG4gICAgICAgIHdhdGNoOiB7XG4gICAgICAgICAgICB1c2VQb2xsaW5nOiB0cnVlLFxuICAgICAgICAgICAgaW50ZXJ2YWw6IDEwMCxcbiAgICAgICAgICAgIGlnbm9yZWQ6IFtcbiAgICAgICAgICAgICAgICAnKiovYmUvKionLCAgICAgICAgICAgLy8gSWdub3JlIERqYW5nbyBiYWNrZW5kIGZvbGRlclxuICAgICAgICAgICAgICAgICcqKi9ub2RlX21vZHVsZXMvKionLFxuICAgICAgICAgICAgICAgICcqKi8uZ2l0LyoqJyxcbiAgICAgICAgICAgICAgICAnKiovX19weWNhY2hlX18vKionLFxuICAgICAgICAgICAgICAgICcqKi8qLnB5YycsXG4gICAgICAgICAgICBdXG4gICAgICAgIH0sXG4gICAgfSxcbiAgICBidWlsZDoge1xuICAgICAgICBtYW5pZmVzdDogdHJ1ZSxcbiAgICAgICAgb3V0RGlyOiAncHVibGljL2J1aWxkJyxcbiAgICAgICAgcm9sbHVwT3B0aW9uczoge1xuICAgICAgICAgICAgaW5wdXQ6ICdyZXNvdXJjZXMvanMvYXBwLmpzJyxcbiAgICAgICAgfSxcbiAgICB9LFxuICAgIHJlc29sdmU6IHtcbiAgICAgICAgYWxpYXM6IHtcbiAgICAgICAgICAgICdAJzogJy9yZXNvdXJjZXMvanMnLFxuICAgICAgICB9LFxuICAgIH0sXG4gICAgb3B0aW1pemVEZXBzOiB7XG4gICAgICAgIGluY2x1ZGU6IFsndnVlJywgJ2F4aW9zJ10sXG4gICAgICAgIGV4Y2x1ZGU6IFtdLFxuICAgIH0sXG59KTtcbiJdLAogICJtYXBwaW5ncyI6ICI7QUFBa1MsU0FBUyxvQkFBb0I7QUFDL1QsT0FBTyxTQUFTO0FBQ2hCLE9BQU8sZ0JBQWdCO0FBQ3ZCLFNBQVEsd0JBQXVCO0FBRS9CLElBQU8sc0JBQVEsYUFBYTtBQUFBLEVBQ3hCLFNBQVM7QUFBQSxJQUNMLElBQUk7QUFBQSxJQUNKLFdBQVc7QUFBQSxNQUNQLFdBQVc7QUFBQSxRQUNULGlCQUFpQjtBQUFBLE1BQ25CO0FBQUEsSUFDSixDQUFDO0FBQUEsRUFDTDtBQUFBLEVBQ0EsUUFBUTtBQUFBLElBQ0osTUFBTTtBQUFBLElBQ04sWUFBWTtBQUFBLElBQ1osTUFBTTtBQUFBO0FBQUEsSUFDTixNQUFNO0FBQUEsSUFDTixLQUFLO0FBQUEsTUFDRCxNQUFNO0FBQUEsTUFDTixVQUFVO0FBQUEsTUFDVixTQUFTO0FBQUEsSUFDYjtBQUFBLElBQ0EsT0FBTztBQUFBLE1BQ0gsUUFBUTtBQUFBLFFBQ0osUUFBUTtBQUFBLFFBQ1IsY0FBYztBQUFBLFFBQ2QsUUFBUTtBQUFBLE1BQ1o7QUFBQSxJQUNKO0FBQUEsSUFDQSxPQUFPO0FBQUEsTUFDSCxZQUFZO0FBQUEsTUFDWixVQUFVO0FBQUEsTUFDVixTQUFTO0FBQUEsUUFDTDtBQUFBO0FBQUEsUUFDQTtBQUFBLFFBQ0E7QUFBQSxRQUNBO0FBQUEsUUFDQTtBQUFBLE1BQ0o7QUFBQSxJQUNKO0FBQUEsRUFDSjtBQUFBLEVBQ0EsT0FBTztBQUFBLElBQ0gsVUFBVTtBQUFBLElBQ1YsUUFBUTtBQUFBLElBQ1IsZUFBZTtBQUFBLE1BQ1gsT0FBTztBQUFBLElBQ1g7QUFBQSxFQUNKO0FBQUEsRUFDQSxTQUFTO0FBQUEsSUFDTCxPQUFPO0FBQUEsTUFDSCxLQUFLO0FBQUEsSUFDVDtBQUFBLEVBQ0o7QUFBQSxFQUNBLGNBQWM7QUFBQSxJQUNWLFNBQVMsQ0FBQyxPQUFPLE9BQU87QUFBQSxJQUN4QixTQUFTLENBQUM7QUFBQSxFQUNkO0FBQ0osQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
