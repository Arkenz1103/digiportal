<template>
    <!-- Professional Login Page with Animated Elements -->
    <div class="min-h-screen relative overflow-hidden flex items-center justify-center p-4">
        <!-- Animated Blue Gradient Background -->
        <div class="absolute inset-0 bg-gradient-to-br from-blue-50 via-blue-100 to-indigo-100">
            <!-- Animated Blobs -->
            <div class="absolute top-20 left-10 w-72 h-72 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
            <div class="absolute top-40 right-20 w-72 h-72 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
            <div class="absolute bottom-20 left-1/3 w-72 h-72 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
        </div>

        <!-- Floating Icons Background -->
        <div class="absolute inset-0 overflow-hidden pointer-events-none">
            <div class="floating-element absolute top-20 left-10 text-blue-300/30 text-6xl animate-float-slow">
                <i class="pi pi-book"></i>
            </div>
            <div class="floating-element absolute top-40 right-20 text-indigo-300/30 text-5xl animate-float-medium" style="animation-delay: 2s;">
                <i class="pi pi-pencil"></i>
            </div>
            <div class="floating-element absolute bottom-40 right-1/4 text-blue-300/30 text-7xl animate-float-slow" style="animation-delay: 1s;">
                <i class="pi pi-palette"></i>
            </div>
            <div class="floating-element absolute bottom-20 left-20 text-cyan-300/30 text-6xl animate-float-medium" style="animation-delay: 3s;">
                <i class="pi pi-star-fill"></i>
            </div>
            <div class="floating-element absolute top-1/2 right-10 text-indigo-300/30 text-5xl animate-float-fast">
                <i class="pi pi-image"></i>
            </div>
            <div class="floating-element absolute top-1/3 left-1/4 text-blue-300/30 text-6xl animate-float-slow" style="animation-delay: 2.5s;">
                <i class="pi pi-graduation-cap"></i>
            </div>
        </div>

        <!-- Back Button -->
        <button 
            @click="goToLanding"
            class="absolute top-6 left-6 flex items-center gap-2 bg-white/80 backdrop-blur-md px-4 py-2 rounded-lg text-gray-700 hover:bg-white/90 transition-all duration-200 font-medium shadow-lg z-20"
        >
            <i class="pi pi-arrow-left"></i>
            <span class="hidden sm:inline">Back</span>
        </button>

        <!-- Login Container -->
        <div class="w-full max-w-md relative z-10">
            <!-- Logo and Welcome Message -->
            <div class="text-center mb-8">
                <div class="flex justify-center mb-4">
                    <!-- Modern Logo SVG -->
                    <div class="w-24 h-24 relative transform hover:scale-110 transition-transform duration-300">
                        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" class="w-full h-full">
                            <defs>
                                <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" style="stop-color:#4F46E5;stop-opacity:1" />
                                    <stop offset="100%" style="stop-color:#7C3AED;stop-opacity:1" />
                                </linearGradient>
                            </defs>
                            <g transform="translate(50, 50)">
                                <!-- D Shape -->
                                <path d="M -20 -25 L -20 25 Q -20 25, -10 25 L -10 25 Q 5 25, 5 10 L 5 -10 Q 5 -25, -10 -25 Z" 
                                      fill="url(#logoGrad)" opacity="0.9"/>
                                <!-- P Shape -->
                                <path d="M 0 -25 L 0 25 M 0 -25 L 15 -25 Q 25 -25, 25 -15 L 25 -5 Q 25 5, 15 5 L 0 5" 
                                      fill="none" stroke="url(#logoGrad)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                                <!-- Digital Dot -->
                                <circle cx="0" cy="0" r="3" fill="#06B6D4"/>
                            </g>
                        </svg>
                    </div>
                </div>
                <h2 class="text-3xl font-bold text-gray-800 mb-2">Welcome to DigiPortal</h2>
                <p class="text-gray-600">Naawan Central School</p>
                <p class="text-sm text-gray-500 mt-1">Digital Portfolio System</p>
            </div>

            <form @submit.prevent="submitLogin" class="space-y-6">
                
                <!-- Role Selection -->
                <div>
                    <label class="block text-gray-700 text-sm font-semibold mb-2">
                        Select Role
                    </label>
                    <div class="grid grid-cols-2 gap-3">
                        <button
                            type="button"
                            @click="loginForm.role = 'teacher'"
                            :class="[
                                'py-3 px-4 rounded-lg border-2 transition-all duration-200 font-medium backdrop-blur-sm',
                                loginForm.role === 'teacher' 
                                    ? 'border-blue-500 bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-lg' 
                                    : 'border-blue-200 bg-white/50 hover:bg-blue-50 text-gray-700'
                            ]"
                        >
                            <i class="pi pi-user mr-2"></i>
                            Teacher
                        </button>
                        <button
                            type="button"
                            @click="loginForm.role = 'student'"
                            :class="[
                                'py-3 px-4 rounded-lg border-2 transition-all duration-200 font-medium backdrop-blur-sm',
                                loginForm.role === 'student' 
                                    ? 'border-blue-500 bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-lg' 
                                    : 'border-blue-200 bg-white/50 hover:bg-blue-50 text-gray-700'
                            ]"
                        >
                            <i class="pi pi-users mr-2"></i>
                            Student
                        </button>
                    </div>
                    <small class="text-red-500 text-xs mt-1 block" v-if="loginForm.errors.role">
                        {{ loginForm.errors.role }}
                    </small>
                </div>

                <!-- Email -->
                <div>
                    <label class="block text-gray-700 text-sm font-semibold mb-2">
                        Email Address
                    </label>
                    <div class="relative">
                        <i class="pi pi-envelope absolute left-3 top-1/2 -translate-y-1/2 text-blue-500"></i>
                        <input
                            type="email"
                            v-model="loginForm.email"
                            class="w-full pl-10 pr-4 py-3 bg-white/70 backdrop-blur-sm border border-blue-200 rounded-lg focus:outline-none focus:border-blue-500 focus:bg-white/90 focus:ring-2 focus:ring-blue-500/20 transition-all duration-200 text-gray-900"
                            :class="{'border-red-500': loginForm.errors.email}"
                            placeholder="Enter your email address"
                        />
                    </div>
                    <small class="text-red-500 text-xs mt-1 block" v-if="loginForm.errors.email">
                        {{ loginForm.errors.email }}
                    </small>
                </div>

                <!-- Password -->
                <div>
                    <label class="block text-gray-700 text-sm font-semibold mb-2">
                        Password
                    </label>
                    <div class="relative">
                        <i class="pi pi-lock absolute left-3 top-1/2 -translate-y-1/2 text-blue-500"></i>
                        <input
                            :type="showPassword ? 'text' : 'password'"
                            v-model="loginForm.password"
                            class="w-full pl-10 pr-12 py-3 bg-white/70 backdrop-blur-sm border border-blue-200 rounded-lg focus:outline-none focus:border-blue-500 focus:bg-white/90 focus:ring-2 focus:ring-blue-500/20 transition-all duration-200 text-gray-900"
                            :class="{'border-red-500': loginForm.errors.password}"
                            placeholder="Enter your password"
                        />
                        <button
                            type="button"
                            @click="showPassword = !showPassword"
                            class="absolute right-3 top-1/2 -translate-y-1/2 text-blue-500 hover:text-blue-700 transition-colors duration-200"
                        >
                            <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
                        </button>
                    </div>
                    <small class="text-red-500 text-xs mt-1 block" v-if="loginForm.errors.password">
                        {{ loginForm.errors.password }}
                    </small>
                    
                    <!-- Forgot Password Link -->
                    <div class="mt-2 text-right">
                        <a href="#" class="text-sm text-blue-600 hover:text-blue-700 font-medium transition-colors duration-200">
                            Forgot password?
                        </a>
                    </div>
                </div>

                <!-- Remember Me & Submit -->
                <div class="flex items-center">
                    <input
                        type="checkbox"
                        v-model="loginForm.remember"
                        id="remember"
                        class="w-4 h-4 text-blue-600 bg-white/70 border-blue-300 rounded focus:ring-blue-500 cursor-pointer"
                    />
                    <label for="remember" class="ml-2 text-sm text-gray-700 select-none cursor-pointer">
                        Remember me
                    </label>
                </div>

                <!-- Login Button -->
                <button
                    type="submit"
                    :disabled="loginForm.processing"
                    class="w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                >
                    <span v-if="!loginForm.processing" class="flex items-center justify-center gap-2">
                        <i class="pi pi-sign-in"></i>
                        Sign In
                    </span>
                    <span v-else class="flex items-center justify-center gap-2">
                        <i class="pi pi-spin pi-spinner"></i>
                        Signing in...
                    </span>
                </button>
            </form>

            <!-- Footer Text -->
            <p class="text-center text-sm text-gray-600 mt-6 backdrop-blur-sm bg-white/30 rounded-lg px-4 py-2">
                © 2025 Naawan Central School. All rights reserved.
            </p>
        </div>
    </div>
</template>


<script setup>
import { ref, reactive } from 'vue';

// Define emits
const emit = defineEmits(['navigate']);

// Show/hide password toggle
const showPassword = ref(false);

const goToLanding = () => {
    emit('navigate', 'Landing');
};

// Function to get CSRF token from cookie
const getCsrfToken = () => {
    const name = 'csrftoken';
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

// Login form
const loginForm = reactive({
    role: '',
    email: '',
    password: '',
    remember: false,
    processing: false,
    errors: {}
});

const submitLogin = async () => {
    loginForm.errors = {};
    
    let hasError = false;
    if (!loginForm.role) {
        loginForm.errors.role = 'Please select your role';
        hasError = true;
    }
    if (!loginForm.email) {
        loginForm.errors.email = 'Email is required';
        hasError = true;
    }
    if (!loginForm.password) {
        loginForm.errors.password = 'Password is required';
        hasError = true;
    }
    
    if (!hasError) {
        loginForm.processing = true;
        
        try {
            // Get CSRF token
            const csrfToken = getCsrfToken();
            
            // Call the actual backend login API
            const response = await fetch('/api/auth/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken || '',
                },
                credentials: 'include', // Include cookies
                body: JSON.stringify({
                    email: loginForm.email,
                    password: loginForm.password,
                    role: loginForm.role
                })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                // Store user data in localStorage
                localStorage.setItem('digiportal_user_role', data.user.role);
                localStorage.setItem('digiportal_user_email', data.user.email);
                localStorage.setItem('digiportal_user_name', data.user.name || data.user.username);
                localStorage.setItem('digiportal_user_id', data.user.id);
                
                // Store authentication token if provided
                if (data.token) {
                    localStorage.setItem('digiportal_auth_token', data.token);
                }
                
                console.log('✅ Login successful, session cookie should be set');
                console.log('🍪 Cookies after login:', document.cookie);
                
                // Dispatch custom event to notify MainLayout of user data change
                window.dispatchEvent(new Event('userDataChanged'));
                
                // CRITICAL: Wait a moment to ensure session cookie is fully set
                await new Promise(resolve => setTimeout(resolve, 100));
                
                console.log('✅ Proceeding to navigation...');
                
                // Navigate based on role
                if (data.user.role === 'teacher') {
                    emit('navigate', 'TeacherHome');
                } else if (data.user.role === 'student') {
                    emit('navigate', 'StudentNewsfeed');
                } else {
                    emit('navigate', 'Landing');
                }
            } else {
                // Handle login error
                loginForm.errors.email = data.error || 'Invalid email or password';
            }
        } catch (error) {
            console.error('Login error:', error);
            loginForm.errors.email = 'Login failed. Please check your credentials and try again.';
        } finally {
            loginForm.processing = false;
        }
    }
};
</script>

<style scoped>
/* Animated Blob Background */
@keyframes blob {
    0%, 100% {
        transform: translate(0px, 0px) scale(1) rotate(0deg);
    }
    33% {
        transform: translate(30px, -50px) scale(1.1) rotate(120deg);
    }
    66% {
        transform: translate(-20px, 20px) scale(0.9) rotate(240deg);
    }
}

.animate-blob {
    animation: blob 20s infinite ease-in-out;
}

.animation-delay-2000 {
    animation-delay: 2s;
}

.animation-delay-4000 {
    animation-delay: 4s;
}

/* Floating Elements Animations */
@keyframes float-slow {
    0%, 100% {
        transform: translateY(0px) translateX(0px) rotate(0deg);
    }
    25% {
        transform: translateY(-20px) translateX(10px) rotate(5deg);
    }
    50% {
        transform: translateY(-30px) translateX(-10px) rotate(-5deg);
    }
    75% {
        transform: translateY(-10px) translateX(15px) rotate(3deg);
    }
}

@keyframes float-medium {
    0%, 100% {
        transform: translateY(0px) translateX(0px) rotate(0deg) scale(1);
    }
    33% {
        transform: translateY(-25px) translateX(-15px) rotate(-8deg) scale(1.05);
    }
    66% {
        transform: translateY(-15px) translateX(20px) rotate(8deg) scale(0.95);
    }
}

@keyframes float-fast {
    0%, 100% {
        transform: translateY(0px) translateX(0px) rotate(0deg);
    }
    20% {
        transform: translateY(-15px) translateX(10px) rotate(10deg);
    }
    40% {
        transform: translateY(-25px) translateX(-10px) rotate(-10deg);
    }
    60% {
        transform: translateY(-10px) translateX(15px) rotate(5deg);
    }
    80% {
        transform: translateY(-20px) translateX(-5px) rotate(-5deg);
    }
}

.animate-float-slow {
    animation: float-slow 20s ease-in-out infinite;
}

.animate-float-medium {
    animation: float-medium 15s ease-in-out infinite;
}

.animate-float-fast {
    animation: float-fast 10s ease-in-out infinite;
}

.floating-element {
    filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
}

/* Custom checkbox styling */
input[type="checkbox"] {
    cursor: pointer;
}

input[type="checkbox"]:checked {
    background-color: #2563eb;
    border-color: #2563eb;
}

/* Smooth focus transitions */
input:focus {
    transition: all 0.2s ease;
}

/* Glass morphism effect for inputs */
input[type="text"],
input[type="password"],
input[type="email"] {
    backdrop-filter: blur(10px);
}

/* Button hover effect */
button[type="submit"]:not(:disabled):hover {
    transform: translateY(-2px);
}

/* Spinner animation */
@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

.pi-spinner {
    animation: spin 1s linear infinite;
}

/* Remove default input styling for autofill */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px rgba(255, 255, 255, 0.7) inset !important;
    -webkit-text-fill-color: #1f2937 !important;
}

/* Responsive adjustments */
@media (max-width: 640px) {
    .floating-element {
        font-size: 0.8em;
    }
    
    .animate-blob {
        width: 200px;
        height: 200px;
    }
}

@media (max-width: 480px) {
    .p-8 {
        padding: 1.5rem;
    }
}
</style>