import axios from 'axios';

// Configure axios defaults for SESSION-BASED authentication
axios.defaults.withCredentials = true; // CRITICAL: Send cookies with every request
axios.defaults.headers.common['Accept'] = 'application/json';
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'; // Help Django recognize AJAX

// Add request interceptor
axios.interceptors.request.use(
    (config) => {
        // Ensure withCredentials is always true
        config.withCredentials = true;
        
        // Get CSRF token from cookie
        const csrfToken = getCookie('csrftoken');
        if (csrfToken) {
            config.headers['X-CSRFToken'] = csrfToken;
        }
        
        console.log('🔐 Axios request:', config.method.toUpperCase(), config.url);
        console.log('🍪 With credentials:', config.withCredentials);
        console.log('🔑 CSRF token:', !!csrfToken);
        
        return config;
    },
    (error) => {
        console.error('❌ Axios request error:', error);
        return Promise.reject(error);
    }
);

// Add response interceptor to handle authentication errors
axios.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // If 401 or 403, session might be invalid
        if (error.response && (error.response.status === 401 || error.response.status === 403)) {
            console.error('❌ Authentication error:', error.response.status);
            console.error('❌ Error data:', error.response.data);
            console.error('❌ Request URL:', error.config?.url);
            console.error('❌ Request method:', error.config?.method);
            
            // Log cookies for debugging
            console.error('🍪 Cookies:', document.cookie);
        }
        return Promise.reject(error);
    }
);

// Helper function to get cookie by name
function getCookie(name) {
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
}

export default axios;
