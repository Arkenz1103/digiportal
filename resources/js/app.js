import './bootstrap';

import { createApp } from 'vue'

// PrimeVue
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import ToastService from 'primevue/toastservice';
import 'primeicons/primeicons.css'

// Global CSS
import '../css/app.css'
import '../css/toast.css'

// Import App component
import App from './App.vue'

// Initialize theme globally
import { useTheme } from './composables/useTheme';
const { initializeTheme } = useTheme();
initializeTheme();

// Create Vue app with App component
const app = createApp(App)

// Use PrimeVue
app.use(PrimeVue, {
  theme: {
      preset: Aura,
      options: {
        prefix: 'ncs-lms',
        darkModeSelector: 'light',
        cssLayer: false
      }
  },
  zIndex: {
      modal: 1100,        //dialog, drawer
      overlay: 1000,      //select, popover
      menu: 1000,         //overlay menus
      tooltip: 1100       //tooltip
  }
})

// Use ToastService
app.use(ToastService)

app.mount('#app')
