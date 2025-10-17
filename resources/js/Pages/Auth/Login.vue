<template>
    
    <!-- Main Container - Centered and Expanded -->
    <div class="flex min-h-screen bg-gradient-to-br from-gray-150 to-gray-100 items-center justify-center p-4">
        <!-- Expanded Form Container with Glow Effect -->
        <div class="w-full max-w-6xl flex bg-white rounded-xl shadow-xl overflow-hidden relative">
            <!-- Glow Effect -->
            <div class="absolute inset-0 bg-gradient-to-r from-purple-100 to-transparent opacity-20 pointer-events-none"></div>
            
            <!-- Left Panel (Purple) - Wider -->
            <!-- Left Panel with Melt Effect -->
            <div 
                class="w-full md:w-2/5 bg-gradient-to-b from-[#6366F1] to-[#7C3AED] flex flex-col justify-center items-center text-white p-6 relative overflow-hidden"
                :class="{ 'md:order-2': isRegisterActive }"
                style="min-height: 500px;"
            >
                <!-- Melt overlay -->
                <div 
                    class="absolute inset-0 bg-white/5 transform origin-top transition-all duration-700 ease-[cubic-bezier(0.68, -0.55, 0.27, 1.55)]"
                    :class="isRegisterActive ? 'scale-y-100' : 'scale-y-0'"
                ></div>
                <div class="max-w-md w-full text-center">
                    <h1 class="text-2xl font-bold mb-3 transform transition-all duration-500" 
                        :class="{'scale-105': isRegisterActive}">Hello, Welcome!</h1>
                    <p class="mb-4 text-purple-100 text-sm">{{ isRegisterActive ? 'Already have an account?' : 'Don\'t have an account yet?' }}</p>
                    <button 
                        @click="toggleForm" 
                        class="relative bg-white text-[#6366F1] px-6 py-2.5 rounded-xl font-semibold hover:bg-opacity-90 transition-all duration-300 ease-out
                               hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.98] text-sm overflow-hidden group"
                    >
                        <span class="relative z-10 flex items-center justify-center gap-2">
                            <i :class="['pi', isRegisterActive ? 'pi-sign-in' : 'pi-user-plus', 'text-sm']"></i>
                            {{ isRegisterActive ? 'Login' : 'Register' }}
                        </span>
                        <span class="absolute inset-0 bg-[#6366F1] opacity-0 group-hover:opacity-5 transition-opacity duration-300"></span>
                    </button>
                </div>
            </div>

            <!-- Right Panel (White) - Expanded Form Area -->
            <!-- Right Panel with Melt Effect -->
            <div 
                class="w-full md:w-3/5 bg-white flex justify-center items-center p-6 relative overflow-hidden"
                :class="{ 'md:order-1': isRegisterActive }"
                style="min-height: 500px;"
            >
                <!-- Melt overlay -->
                <div 
                    class="absolute inset-0 bg-purple-50/30 transform origin-top transition-all duration-700 ease-[cubic-bezier(0.68, -0.55, 0.27, 1.55)]"
                    :class="!isRegisterActive ? 'scale-y-100' : 'scale-y-0'"
                ></div>
                <div class="w-full max-w-xl">
                    <div class="h-4"></div>
                    <!-- Form Container with Melting Candle Effect -->
                    <div class="relative overflow-visible" style="min-height: 500px">
                        <!-- Login Form -->
                        <div 
                            class="absolute w-full transition-all duration-700 ease-[cubic-bezier(0.68, -0.55, 0.27, 1.55)] transform origin-top"
                            :class="{
                                'opacity-100 scale-y-100 translate-y-0': !isRegisterActive,
                                'opacity-0 scale-y-90 -translate-y-10': isRegisterActive,
                                'pointer-events-none': isRegisterActive
                            }"
                            style="backface-visibility: hidden; width: 100%;"
                        >
                            <h1 class="text-xl font-bold text-gray-800 text-center mb-2">Welcome back!</h1>
                            <p class="text-gray-600 text-center mb-4 text-sm">Enter your credentials to access your account.</p>

                            <form @submit.prevent="submitLogin" class="space-y-3">
                                <div class="mb-3">
                                    <label class="block text-gray-700 mb-1 font-medium text-sm">Email</label>
                                    <div class="relative">
                                        <InputText
                                            type="email"
                                            v-model="loginForm.email"
                                            placeholder="Enter your email"  
                                            class="w-full h-10 pl-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-transparent text-sm"
                                            :class="{'border-red-500': loginForm.errors.email}"
                                        />
                                    </div>
                                    <small class="text-red-500 text-xs" v-if="loginForm.errors.email">{{ loginForm.errors.email }}</small>
                                </div>

                                <div class="mb-3">
                                    <label class="block text-gray-700 mb-1 font-medium text-sm">Password</label>
                                    <div class="relative">
                                        <Password
                                            v-model="loginForm.password"
                                            placeholder="Enter your password"
                                            :feedback="false"
                                            :toggleMask="true"
                                            class="w-full"
                                            :inputClass="{'border-red-500': loginForm.errors.password, 'border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-transparent h-10 pl-3 text-sm': true}"
                                        />
                                    </div>
                                    <small class="text-red-500 text-xs" v-if="loginForm.errors.password">{{ loginForm.errors.password }}</small>
                                </div>

                                <!-- Remember Me & Forgot Password -->
                                <div class="flex justify-between items-center mb-4">
                                    <div class="flex items-center">
                                        <Checkbox v-model="loginForm.remember" :binary="true" inputId="remember" class="mr-2" />
                                        <label for="remember" class="text-gray-700 select-none cursor-pointer text-xs hover:text-gray-800 transition-colors duration-200">
                                        Remember me
                                    </label>
                                    </div>
                                    <a href="#" class="text-[#6366F1] hover:text-[#4F46E5] hover:underline transition-colors duration-200 text-xs font-medium">
                                        Forgot Password?
                                    </a>
                                </div>

                                <!-- Login Button -->
                                <button
                                    type="submit"
                                    :disabled="loginForm.processing"
                                    class="relative w-full h-10 text-sm font-semibold bg-gradient-to-r from-[#10B981] to-[#059669] border-none text-white rounded-xl hover:shadow-lg transition-all duration-300 ease-out
                                           hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.98] overflow-hidden group"
                                >
                                    <span class="relative z-10 flex items-center justify-center gap-2">
                                        <i v-if="!loginForm.processing" class="pi pi-sign-in"></i>
                                        <i v-else class="pi pi-spin pi-spinner"></i>
                                        {{ loginForm.processing ? 'Logging in...' : 'Login' }}
                                    </span>
                                    <span class="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
                                </button>
                            </form>
                        </div>

                        <!-- Register Form - Melting Candle Effect -->
                        <div 
                            class="absolute w-full transition-all duration-700 ease-[cubic-bezier(0.68, -0.55, 0.27, 1.55)] transform origin-top"
                            :class="{
                                'opacity-100 scale-y-100 translate-y-0': isRegisterActive,
                                'opacity-0 scale-y-90 translate-y-10': !isRegisterActive,
                                'pointer-events-none': !isRegisterActive
                            }"
                            style="backface-visibility: hidden; width: 100%;"
                        >
                            <h1 class="text-xl font-bold text-gray-800 text-center mb-2">Create Account</h1>
                            <p class="text-gray-600 text-center mb-4 text-sm">Fill in your details to get started.</p>

                            <form @submit.prevent="submitRegister" class="space-y-3">
                                <div class="mb-2">
                                    <label class="block text-gray-700 mb-1 font-medium text-sm">Full Name</label>
                                    <div class="relative">
                                        <InputText
                                            type="text"
                                            v-model="registerForm.name"
                                            placeholder="Enter your full name"  
                                            class="w-full h-9 pl-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-transparent text-sm"
                                            :class="{'border-red-500': registerForm.errors.name}"
                                        />
                                    </div>
                                    <small class="text-red-500 text-xs" v-if="registerForm.errors.name">{{ registerForm.errors.name }}</small>
                                </div>

                                <div class="mb-2">
                                    <label class="block text-gray-700 mb-1 font-medium text-sm">Email</label>
                                    <div class="relative">
                                        <InputText
                                            type="email"
                                            v-model="registerForm.email"
                                            placeholder="Enter your email"  
                                            class="w-full h-9 pl-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-transparent text-sm"
                                            :class="{'border-red-500': registerForm.errors.email}"
                                        />
                                    </div>
                                    <small class="text-red-500 text-xs" v-if="registerForm.errors.email">{{ registerForm.errors.email }}</small>
                                </div>

                                <div class="mb-2">
                                    <label class="block text-gray-700 mb-1 font-medium text-sm">Password</label>
                                    <div class="relative">
                                        <Password
                                            v-model="registerForm.password"
                                            placeholder="Create a password"
                                            :feedback="true"
                                            :toggleMask="true"
                                            class="w-full"
                                            :inputClass="{'border-red-500': registerForm.errors.password, 'border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-transparent h-9 pl-3 text-sm': true}"
                                        />
                                    </div>
                                    <small class="text-red-500 text-xs" v-if="registerForm.errors.password">{{ registerForm.errors.password }}</small>
                                </div>

                                <div class="mb-2">
                                    <label class="block text-gray-700 mb-1 font-medium text-sm">Confirm Password</label>
                                    <div class="relative">
                                        <Password
                                            v-model="registerForm.password_confirmation"
                                            placeholder="Confirm your password"
                                            :feedback="false"
                                            :toggleMask="true"
                                            class="w-full"
                                            :inputClass="{'border-red-500': registerForm.errors.password_confirmation, 'border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-transparent h-9 pl-3 text-sm': true}"
                                        />
                                    </div>
                                    <small class="text-red-500 text-xs" v-if="registerForm.errors.password_confirmation">
                                        {{ registerForm.errors.password_confirmation }}
                                    </small>
                                </div>

                                <!-- Role Selection -->
                                <div class="mb-2">
                                    <label class="block text-gray-700 mb-1 font-medium text-sm">Role</label>
                                    <div class="relative">
                                        <select
                                            v-model="registerForm.role"
                                            class="w-full h-9 pl-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-transparent appearance-none bg-white text-sm"
                                            :class="{'border-red-500': registerForm.errors.role}"
                                        >
                                            <option value="" disabled selected>Select your role</option>
                                            <option value="teacher">Teacher</option>
                                            <option value="student">Student</option>
                                        </select>
                                        <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                                            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                                            </svg>
                                        </div>
                                    </div>
                                    <small class="text-red-500 text-xs" v-if="registerForm.errors.role">{{ registerForm.errors.role }}</small>
                                </div>

                                <!-- Terms and Conditions -->
                                <div class="flex items-center mb-3">
                                    <Checkbox v-model="registerForm.terms" :binary="true" inputId="terms" class="mr-2" />
                                    <label for="terms" class="text-gray-700 select-none cursor-pointer text-xs">
                                        I agree to the <a href="#" class="text-[#6366F1] hover:underline">Terms and Conditions</a>
                                    </label>
                                </div>

                                <!-- Register Button -->
                                <button
                                    type="submit"
                                    :disabled="registerForm.processing"
                                    class="relative w-full h-10 text-sm font-semibold bg-gradient-to-r from-[#10B981] to-[#059669] border-none text-white rounded-xl hover:shadow-lg transition-all duration-300 ease-out
                                           hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.98] overflow-hidden group mb-2"
                                >
                                    <span class="relative z-10 flex items-center justify-center gap-2">
                                        <i v-if="!registerForm.processing" class="pi pi-user-plus"></i>
                                        <i v-else class="pi pi-spin pi-spinner"></i>
                                        {{ registerForm.processing ? 'Creating Account...' : 'Register' }}
                                    </span>
                                    <span class="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Checkbox from 'primevue/checkbox';

// Define emits
const emit = defineEmits(['navigate']);

// Toggle between login and register forms
const isRegisterActive = ref(false);

const toggleForm = () => {
    isRegisterActive.value = !isRegisterActive.value;
};

// Login form
const loginForm = reactive({
    email: '',
    password: '',
    remember: false,
    processing: false,
    errors: {}
});

const submitLogin = async () => {
    loginForm.errors = {};
    
    let hasError = false;
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
        
        // Simulate API call - replace with actual backend call later
        setTimeout(() => {
            loginForm.processing = false;
            
            // For demo: redirect based on email or use a more robust system
            // You can replace this with actual authentication logic
            let userRole = 'student'; // Default to student
            
            // Simple role detection - you can enhance this
            if (loginForm.email.includes('teacher') || loginForm.email.includes('admin')) {
                userRole = 'teacher';
            } else if (loginForm.email.includes('student')) {
                userRole = 'student';
            }
            
            // Store user role for the session
            localStorage.setItem('digiportal_user_role', userRole);
            localStorage.setItem('digiportal_user_email', loginForm.email);
            
            // Set a default name based on role (you can enhance this)
            const userName = userRole === 'teacher' ? 'Teacher User' : 'Student User';
            localStorage.setItem('digiportal_user_name', userName);
            
            // Dispatch custom event to notify MainLayout of user data change
            window.dispatchEvent(new Event('userDataChanged'));
            
            // Navigate based on role
            if (userRole === 'teacher') {
                emit('navigate', 'TeacherHome');
            } else {
                emit('navigate', 'StudentNewsfeed');
            }
        }, 1000);
    }
};

// Register form
const registerForm = reactive({
    name: '',
    email: '',
    password: '',
    password_confirmation: '',
    role: '',
    terms: false,
    processing: false,
    errors: {}
});

const submitRegister = async () => {
    registerForm.errors = {};
    
    let hasError = false;
    if (!registerForm.name) {
        registerForm.errors.name = 'Name is required';
        hasError = true;
    }
    if (!registerForm.email) {
        registerForm.errors.email = 'Email is required';
        hasError = true;
    }
    if (!registerForm.password) {
        registerForm.errors.password = 'Password is required';
        hasError = true;
    }
    if (registerForm.password && !registerForm.password_confirmation) {
        registerForm.errors.password_confirmation = 'Please confirm your password';
        hasError = true;
    }
    if (registerForm.password !== registerForm.password_confirmation) {
        registerForm.errors.password_confirmation = 'Passwords do not match';
        hasError = true;
    }
    if (!registerForm.role) {
        registerForm.errors.role = 'Please select your role';
        hasError = true;
    }
    if (!registerForm.terms) {
        registerForm.errors.terms = 'You must agree to the terms and conditions';
        hasError = true;
    }
    
    if (!hasError) {
        registerForm.processing = true;
        
        // Simulate API call - replace with actual backend call later
        setTimeout(() => {
            registerForm.processing = false;
            
            // Store user data for the session
            localStorage.setItem('digiportal_user_role', registerForm.role);
            localStorage.setItem('digiportal_user_email', registerForm.email);
            localStorage.setItem('digiportal_user_name', registerForm.name);
            
            // Dispatch custom event to notify MainLayout of user data change
            window.dispatchEvent(new Event('userDataChanged'));
            
            // Navigate based on role
            if (registerForm.role === 'teacher') {
                emit('navigate', 'TeacherHome');
            } else {
                emit('navigate', 'StudentNewsfeed');
            }
            
            // Clear register form
            registerForm.name = '';
            registerForm.email = '';
            registerForm.password = '';
            registerForm.password_confirmation = '';
            registerForm.role = '';
            registerForm.terms = false;
        }, 1000);
    }
};
</script>

<style scoped>
/* Custom scrollbar */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: #c0c0c0;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #a0a0a0;
}

:deep(.p-password-input) {
    width: 100%;
    padding-left: 0.75rem;
    border-radius: 0.5rem;
    border: 1px solid #d1d5db;
    font-size: 0.875rem;
}

:deep(.p-password) {
    width: 100%;
}

:deep(.p-password-panel) {
    font-size: 0.75rem;
}

:deep(.p-password-meter) {
    height: 6px;
}

:deep(.p-button) {
    border: none;
    border-radius: 0.5rem;
    color: white;
    transition: all 0.3s ease;
}

:deep(.p-button:hover) {
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

:deep(.p-inputtext) {
    width: 100%;
    padding-left: 0.75rem;
    transition: all 0.3s ease;
    font-size: 0.875rem;
}

:deep(.p-checkbox) {
    width: 16px;
    height: 16px;
}

:deep(.p-checkbox .p-checkbox-box) {
    width: 16px;
    height: 16px;
}

:deep(.p-checkbox .p-checkbox-box.p-highlight) {
    background: #6366F1;
    border-color: #6366F1;
}

:deep(.p-checkbox-icon) {
    font-size: 10px;
}

:deep(.p-password .p-inputtext.p-invalid) {
    border-color: #dc2626;
}

/* Custom candle-like transition effects */
.translate-x-full {
    transform: translateX(100%);
}

.-translate-x-full {
    transform: translateX(-100%);
}

/* Glow effect for active form */
.form-active {
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .translate-x-full, .-translate-x-full {
        transform: translateY(100%);
    }
    
    .translate-x-0 {
        transform: translateY(0);
    }
    
    :deep(.p-inputtext),
    :deep(.p-password-input) {
        font-size: 0.75rem;
        padding-left: 0.75rem;
    }
}
</style>