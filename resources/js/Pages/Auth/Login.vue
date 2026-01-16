<template>
    <div class="min-h-screen relative overflow-hidden bg-white">
        <!-- Subtle Background Pattern -->
        <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgIDxwYXRoIGQ9Ik0wIDBoNDB2NDBINHoiIGZpbGw9IiNmZmYiLz4KICAgIDxwYXRoIGQ9Ik0wIDBoMjB2MjBIMHoiIGZpbGw9IiNmOWY5ZjkiLz4KPC9zdmc+')] opacity-5"></div>

        <!-- Back Button -->
        <button @click="goToLanding" class="absolute top-6 left-6 flex items-center gap-2 bg-white px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-50 transition-all duration-200 font-medium shadow-md z-20 border border-gray-200 hover:border-gray-300">
            <i class="pi pi-arrow-left text-gray-600"></i>
            <span class="hidden sm:inline text-gray-700">Back</span>
        </button>

        <!-- Main Container -->
        <div class="relative z-10 min-h-screen flex items-center justify-center p-4">
            <div class="w-full max-w-5xl">
                <!-- Split Card with Rounded Corners -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-0 rounded-3xl overflow-hidden shadow-2xl bg-white" style="min-height: 500px;">
                    <!-- Left Side - Welcome -->
                    <div class="bg-gradient-to-br from-indigo-900 to-purple-900 p-8 md:p-12 flex flex-col justify-center items-center text-center rounded-l-3xl">
                        <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">Welcome Back!</h2>
                        <p class="text-purple-100 text-base leading-relaxed mb-8">Enter your personal details to use all of site features</p>
                    </div>

                    <!-- Right Side - Login Form -->
                    <div class="bg-white p-8 md:p-12 flex flex-col justify-center">
                        <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-2">Sign In</h2>
                        <p class="text-gray-600 text-sm mb-6">Please enter your credentials to continue</p>

                        <form @submit.prevent="submitForm" class="space-y-4">
                            <!-- Role Selection -->
                            <div>
                                <label class="block text-gray-700 text-xs font-semibold mb-2 uppercase">Select Role</label>
                                <div class="grid grid-cols-3 gap-3">
                                    <button type="button" @click="form.role = 'admin'" :class="['py-3 px-4 rounded-lg border-2 font-semibold transition-all', form.role === 'admin' ? 'border-indigo-700 bg-indigo-700 text-white' : 'border-gray-300 bg-gray-100 text-gray-700 hover:border-indigo-700']">
                                        <i class="pi pi-shield mr-2"></i>Admin
                                    </button>
                                    <button type="button" @click="form.role = 'teacher'" :class="['py-3 px-4 rounded-lg border-2 font-semibold transition-all', form.role === 'teacher' ? 'border-purple-700 bg-purple-700 text-white' : 'border-gray-300 bg-gray-100 text-gray-700 hover:border-purple-700']">
                                        <i class="pi pi-user mr-2"></i>Teacher
                                    </button>
                                    <button type="button" @click="form.role = 'student'" :class="['py-3 px-4 rounded-lg border-2 font-semibold transition-all', form.role === 'student' ? 'border-purple-700 bg-purple-700 text-white' : 'border-gray-300 bg-gray-100 text-gray-700 hover:border-purple-700']">
                                        <i class="pi pi-users mr-2"></i>Student
                                    </button>
                                </div>
                            </div>

                            <div>
                                <input type="email" v-model="form.email" placeholder="Email" :class="['w-full px-4 py-3 bg-gray-100 border rounded-lg focus:outline-none focus:ring-2 transition-all', form.errors.email ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-purple-500']" />
                                <p v-if="form.errors.email" class="text-red-500 text-xs mt-1">{{ form.errors.email }}</p>
                            </div>
                            <div>
                                <div class="relative">
                                    <input :type="showPassword ? 'text' : 'password'" v-model="form.password" placeholder="Password" :class="['w-full px-4 py-3 bg-gray-100 border rounded-lg focus:outline-none focus:ring-2 transition-all pr-10', form.errors.password ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-purple-500']" />
                                    <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700">
                                        <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
                                    </button>
                                </div>
                                <p v-if="form.errors.password" class="text-red-500 text-xs mt-1">{{ form.errors.password }}</p>
                            </div>
                            <div class="flex items-center justify-between text-sm">
                                <label class="flex items-center gap-2 cursor-pointer">
                                    <input type="checkbox" v-model="form.remember" class="w-4 h-4 accent-purple-700" />
                                    <span class="text-gray-600">Remember me</span>
                                </label>
                                <a href="#" class="text-purple-700 font-semibold hover:underline">Forgot Your Password?</a>
                            </div>
                            <button type="submit" :disabled="form.processing" :class="['w-full py-3 bg-gradient-to-r from-purple-700 to-purple-900 text-white font-bold rounded-lg transition-all duration-300 uppercase text-sm tracking-wider flex items-center justify-center gap-2', form.processing ? 'opacity-90 scale-95' : 'hover:shadow-lg hover:scale-105 active:scale-95']">
                                <span v-if="form.processing" class="inline-block animate-spin">
                                    <i class="pi pi-spinner text-lg"></i>
                                </span>
                                {{ form.processing ? 'Signing in...' : 'Sign In' }}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <!-- Toast Notification -->
        <transition name="toast-fade">
            <div v-if="toast.show" class="fixed bottom-6 right-6 z-50">
                <div :class="['px-6 py-4 rounded-lg shadow-lg flex items-center gap-3 backdrop-blur-md border',
                    toast.type === 'error' ? 'bg-red-500/90 border-red-400 text-white' :
                    toast.type === 'success' ? 'bg-green-500/90 border-green-400 text-white' :
                    'bg-blue-500/90 border-blue-400 text-white']">
                    <i :class="['pi text-lg',
                        toast.type === 'error' ? 'pi-exclamation-circle' :
                        toast.type === 'success' ? 'pi-check-circle' :
                        'pi-info-circle']"></i>
                    <span class="font-semibold">{{ toast.message }}</span>
                </div>
            </div>
        </transition>

        <!-- Footer -->
        <div class="absolute bottom-6 left-0 right-0 text-center">
            <p class="text-gray-400 text-xs">© 2025 Naawan Central School. All rights reserved.</p>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

const emit = defineEmits(['navigate']);

const showPassword = ref(false);
const toast = reactive({
    show: false,
    message: '',
    type: 'error' // 'error', 'success', 'info'
});

const form = reactive({
    role: '',
    email: '',
    password: '',
    remember: false,
    processing: false,
    errors: {}
});

const showToast = (message, type = 'error') => {
    toast.message = message;
    toast.type = type;
    toast.show = true;
    setTimeout(() => {
        toast.show = false;
    }, 4000);
};


const goToLanding = () => {
    emit('navigate', 'Landing');
};

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

const submitForm = async () => {
    form.errors = {};
    let hasError = false;

    if (!form.role) {
        form.errors.role = 'Please select your role';
        hasError = true;
    }
    if (!form.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
        form.errors.email = 'Valid email is required';
        hasError = true;
    }
    if (!form.password || form.password.length < 6) {
        form.errors.password = 'Password must be at least 6 characters';
        hasError = true;
    }

    if (!hasError) {
        form.processing = true;
        try {
            const csrfToken = getCsrfToken();
            const endpoint = '/api/auth/login/';
            const payload = { email: form.email, password: form.password, role: form.role };

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken || '',
                },
                credentials: 'include',
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Check if selected role matches user's actual role
                if (data.user.role !== form.role) {
                    showToast(`This account is registered as a ${data.user.role}, not a ${form.role}. Please select the correct role.`, 'error');
                    return;
                }

                localStorage.setItem('digiportal_user_role', data.user.role);
                localStorage.setItem('digiportal_user_email', data.user.email);
                localStorage.setItem('digiportal_user_name', data.user.name || data.user.username);
                localStorage.setItem('digiportal_user_id', data.user.id);
                if (data.token) {
                    localStorage.setItem('digiportal_auth_token', data.token);
                }
                window.dispatchEvent(new Event('userDataChanged'));
                await new Promise(resolve => setTimeout(resolve, 100));
                if (data.user.role === 'teacher') {
                    emit('navigate', 'TeacherHome');
                } else if (data.user.role === 'student') {
                    // Check if student has a classroom assigned
                    if (data.user.has_classroom === false) {
                        // No classroom - redirect to School Year page to join one
                        emit('navigate', 'StudentSchoolYear');
                    } else {
                        emit('navigate', 'StudentNewsfeed');
                    }
                } else if (data.user.role === 'admin') {
                    emit('navigate', 'AdminDashboard');
                } else {
                    emit('navigate', 'Landing');
                }
            } else {
                if (data.errors) {
                    // Set errors for all fields returned from backend
                    for (const key in data.errors) {
                        const errorMsg = Array.isArray(data.errors[key]) ? data.errors[key][0] : data.errors[key];
                        form.errors[key] = errorMsg;
                    }
                    // Show toast for first error
                    const firstError = Object.values(data.errors)[0];
                    const errorMsg = Array.isArray(firstError) ? firstError[0] : firstError;
                    showToast(errorMsg || 'Authentication failed', 'error');
                } else {
                    showToast(data.message || 'Authentication failed', 'error');
                }
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('An unexpected error occurred', 'error');
        } finally {
            form.processing = false;
        }
    }
};
</script>

<style scoped>
@keyframes blob {
    0%, 100% { transform: translate(0px, 0px) scale(1) rotate(0deg); }
    33% { transform: translate(30px, -50px) scale(1.1) rotate(120deg); }
    66% { transform: translate(-20px, 20px) scale(0.9) rotate(240deg); }
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

.slide-login-enter-active,
.slide-login-leave-active,
.slide-signup-enter-active,
.slide-signup-leave-active {
    transition: all 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Toast Animations */
.toast-fade-enter-active,
.toast-fade-leave-active {
    transition: all 0.3s ease-in-out;
}

.toast-fade-enter-from {
    opacity: 0;
    transform: translateX(100px) translateY(20px);
}

.toast-fade-leave-to {
    opacity: 0;
    transform: translateX(100px) translateY(20px);
}

.slide-login-enter-from {
    opacity: 0;
    transform: translateX(-100%);
}

.slide-login-leave-to {
    opacity: 0;
    transform: translateX(100%);
}

.slide-signup-enter-from {
    opacity: 0;
    transform: translateX(100%);
}

.slide-signup-leave-to {
    opacity: 0;
    transform: translateX(-100%);
}
</style>
