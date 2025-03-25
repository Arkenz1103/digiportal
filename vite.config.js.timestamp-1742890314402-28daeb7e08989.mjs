// vite.config.js
import { defineConfig } from "file:///C:/digiportal/digiportal/node_modules/vite/dist/node/index.js";
import laravel from "file:///C:/digiportal/digiportal/node_modules/laravel-vite-plugin/dist/index.js";
import vue from "file:///C:/digiportal/digiportal/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import Components from "file:///C:/digiportal/digiportal/node_modules/unplugin-vue-components/dist/vite.js";
import { PrimeVueResolver } from "file:///C:/digiportal/digiportal/node_modules/@primevue/auto-import-resolver/index.mjs";
var vite_config_default = defineConfig({
  plugins: [
    vue(),
    laravel({
      input: ["resources/css/app.css", "resources/js/app.js"],
      refresh: true
    }),
    Components({
      resolvers: [
        PrimeVueResolver()
      ]
    })
  ]
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJDOlxcXFxkaWdpcG9ydGFsXFxcXGRpZ2lwb3J0YWxcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIkM6XFxcXGRpZ2lwb3J0YWxcXFxcZGlnaXBvcnRhbFxcXFx2aXRlLmNvbmZpZy5qc1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vQzovZGlnaXBvcnRhbC9kaWdpcG9ydGFsL3ZpdGUuY29uZmlnLmpzXCI7aW1wb3J0IHsgZGVmaW5lQ29uZmlnIH0gZnJvbSAndml0ZSc7XG5pbXBvcnQgbGFyYXZlbCBmcm9tICdsYXJhdmVsLXZpdGUtcGx1Z2luJztcbmltcG9ydCB2dWUgZnJvbSAnQHZpdGVqcy9wbHVnaW4tdnVlJztcbmltcG9ydCBDb21wb25lbnRzIGZyb20gJ3VucGx1Z2luLXZ1ZS1jb21wb25lbnRzL3ZpdGUnO1xuaW1wb3J0IHtQcmltZVZ1ZVJlc29sdmVyfSBmcm9tICdAcHJpbWV2dWUvYXV0by1pbXBvcnQtcmVzb2x2ZXInO1xuXG5leHBvcnQgZGVmYXVsdCBkZWZpbmVDb25maWcoe1xuICAgIHBsdWdpbnM6IFtcbiAgICAgICAgdnVlKCksXG4gICAgICAgIGxhcmF2ZWwoe1xuICAgICAgICAgICAgaW5wdXQ6IFsncmVzb3VyY2VzL2Nzcy9hcHAuY3NzJywgJ3Jlc291cmNlcy9qcy9hcHAuanMnXSxcbiAgICAgICAgICAgIHJlZnJlc2g6IHRydWUsXG4gICAgICAgIH0pLFxuICAgICAgICBDb21wb25lbnRzKHtcbiAgICAgICAgICAgIHJlc29sdmVyczogW1xuICAgICAgICAgICAgICBQcmltZVZ1ZVJlc29sdmVyKClcbiAgICAgICAgICAgIF1cbiAgICAgICAgfSksXG4gICAgXSxcbn0pO1xuIl0sCiAgIm1hcHBpbmdzIjogIjtBQUFnUSxTQUFTLG9CQUFvQjtBQUM3UixPQUFPLGFBQWE7QUFDcEIsT0FBTyxTQUFTO0FBQ2hCLE9BQU8sZ0JBQWdCO0FBQ3ZCLFNBQVEsd0JBQXVCO0FBRS9CLElBQU8sc0JBQVEsYUFBYTtBQUFBLEVBQ3hCLFNBQVM7QUFBQSxJQUNMLElBQUk7QUFBQSxJQUNKLFFBQVE7QUFBQSxNQUNKLE9BQU8sQ0FBQyx5QkFBeUIscUJBQXFCO0FBQUEsTUFDdEQsU0FBUztBQUFBLElBQ2IsQ0FBQztBQUFBLElBQ0QsV0FBVztBQUFBLE1BQ1AsV0FBVztBQUFBLFFBQ1QsaUJBQWlCO0FBQUEsTUFDbkI7QUFBQSxJQUNKLENBQUM7QUFBQSxFQUNMO0FBQ0osQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
