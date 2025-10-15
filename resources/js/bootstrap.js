import axios from 'axios';
window.axios = axios;

// API configuration (can be updated later if you add a backend)
window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
