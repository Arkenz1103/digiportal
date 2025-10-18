import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import Components from 'unplugin-vue-components/vite';
import {PrimeVueResolver} from '@primevue/auto-import-resolver';

export default defineConfig({
    plugins: [
        vue(),
        Components({
            resolvers: [
              PrimeVueResolver()
            ]
        }),
    ],
    server: {
        port: 5173,
        strictPort: true,
        host: 'localhost',
        cors: true,
        hmr: {
            host: 'localhost',
            protocol: 'ws',
            overlay: true,
        },
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                secure: false,
            },
        },
        watch: {
            usePolling: true,
            interval: 100,
            ignored: [
                '**/be/**',           // Ignore Django backend folder
                '**/node_modules/**',
                '**/.git/**',
                '**/__pycache__/**',
                '**/*.pyc',
            ]
        },
    },
    build: {
        manifest: true,
        outDir: 'public/build',
        rollupOptions: {
            input: 'resources/js/app.js',
        },
    },
    resolve: {
        alias: {
            '@': '/resources/js',
        },
    },
    optimizeDeps: {
        include: ['vue', 'axios'],
        exclude: [],
    },
});
