import './bootstrap';

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

// PrimeVue
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import 'primeicons/primeicons.css'

// Global CSS
import '../css/app.css'

// Import routes
import { routes } from './utils/routes'

// Import main App component
import App from './App.vue'

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Router guards
router.beforeEach((to, from, next) => {
  // Update document title
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // Handle authentication (for future implementation)
  if (to.meta.requiresAuth) {
    // For now, just proceed - you can add auth logic later
    console.log(`Route ${to.name} requires authentication`)
  }
  
  next()
})

// Create Vue app
const app = createApp(App)

// Use router
app.use(router)

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

app.mount('#app')
