import axios from 'axios';
window.axios = axios;

// API configuration for Django backend
window.axios.defaults.baseURL = 'http://localhost:8000';
window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
window.axios.defaults.withCredentials = true;

// Add CSRF token handling
const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

// Set CSRF token for POST requests
window.axios.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');
