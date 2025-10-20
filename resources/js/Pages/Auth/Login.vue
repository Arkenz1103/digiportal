<template>
    <!-- Main Container with Animated Background -->
    <div class="flex min-h-screen items-center justify-center p-4 relative overflow-hidden">
        <!-- Animated Background -->
        <div class="absolute inset-0 bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800">
            <!-- Animated Circles -->
            <div class="absolute top-0 left-0 w-96 h-96 bg-cyan-400 opacity-10 rounded-full mix-blend-multiply filter blur-xl animate-blob"></div>
            <div class="absolute top-0 right-0 w-96 h-96 bg-blue-300 opacity-10 rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-2000"></div>
            <div class="absolute bottom-0 left-1/2 w-96 h-96 bg-indigo-400 opacity-10 rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-4000"></div>
        </div>

        <!-- Back Button -->
        <button 
            @click="goToLanding"
            class="absolute top-6 left-6 flex items-center justify-center w-12 h-12 bg-white/20 backdrop-blur-md text-white rounded-xl shadow-lg hover:bg-white/30 transition-all duration-200 z-10 border border-white/30"
        >
            <i class="pi pi-arrow-left text-xl"></i>
        </button>

        <!-- Login Card -->
        <div class="w-full max-w-md relative z-10">
            <div class="bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl overflow-hidden border border-white/20">
                <!-- Header Section -->
                <div class="p-6 text-center">
                    <div class="w-16 h-16 bg-white/20 backdrop-blur-md rounded-full mx-auto mb-3 flex items-center justify-center border-2 border-white/30 shadow-lg">
                        <i class="pi pi-user text-3xl text-white"></i>
                    </div>
                    
                    <p class="text-white text-lg font-bold">Sign in to continue to DigiPortal</p>
                </div>

                <!-- Form Section -->
                <div class="p-8 pt-0">
                    <form @submit.prevent="submitLogin" class="space-y-5">

                        <!-- Role Selection -->
                        <div>
                            <label class="block text-white mb-2 font-semibold text-sm">Select Role</label>
                            <div class="relative">
                                <select
                                    v-model="loginForm.role"
                                    class="w-full h-14 px-4 border-2 border-white/30 rounded-xl focus:ring-2 focus:ring-white/50 focus:border-white/50 appearance-none bg-white/10 backdrop-blur-md text-white font-medium cursor-pointer placeholder-white/50"
                                    :class="{'border-red-400': loginForm.errors.role}"
                                >
                                    <option value="" disabled class="bg-indigo-600 text-white">Choose your role</option>
                                    <option value="teacher" class="bg-indigo-600 text-white">Teacher</option>
                                    <option value="student" class="bg-indigo-600 text-white">Student</option>
                                </select>
                                <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
                                    <i class="pi pi-chevron-down text-white/70 text-sm"></i>
                                </div>
                            </div>
                            <small class="text-red-200 text-sm" v-if="loginForm.errors.role">{{ loginForm.errors.role }}</small>
                        </div>

                        <!-- Email -->
                        <div>
                            <label class="block text-white mb-2 font-semibold text-sm">Email</label>
                            <div class="relative">
                                <i class="pi pi-envelope absolute left-4 top-1/2 transform -translate-y-1/2 text-white/70 text-lg"></i>
                                <InputText
                                    type="email"
                                    v-model="loginForm.email"
                                    placeholder="Enter your email"  
                                    class="w-full h-14 pl-12 pr-4 border-2 border-white/30 rounded-xl focus:ring-2 focus:ring-white/50 focus:border-white/50 bg-white/10 backdrop-blur-md text-white placeholder-white/50 font-medium"
                                    :class="{'border-red-400': loginForm.errors.email}"
                                />
                            </div>
                            <small class="text-red-200 text-sm" v-if="loginForm.errors.email">{{ loginForm.errors.email }}</small>
                        </div>

                        <!-- Password -->
                        <div>
                            <label class="block text-white mb-2 font-semibold text-sm">Password</label>
                            <div class="relative">
                                <i class="pi pi-lock absolute left-4 top-1/2 transform -translate-y-1/2 text-white/70 text-lg z-20"></i>
                                <Password
                                    v-model="loginForm.password"
                                    placeholder="Enter your password"
                                    :feedback="false"
                                    :toggleMask="true"
                                    class="w-full custom-password"
                                    inputClass="w-full h-14 pl-12 pr-12 border-2 border-white/30 rounded-xl focus:ring-2 focus:ring-white/50 focus:border-white/50 bg-white/10 backdrop-blur-md text-white placeholder-white/50 font-medium"
                                    :class="{'border-red-400': loginForm.errors.password}"
                                />
                            </div>
                            <small class="text-red-200 text-sm" v-if="loginForm.errors.password">{{ loginForm.errors.password }}</small>
                        </div>

                        <!-- Remember Me -->
                        <div class="flex items-center">
                            <Checkbox v-model="loginForm.remember" :binary="true" inputId="remember" class="mr-3" />
                            <label for="remember" class="text-white select-none cursor-pointer hover:text-white/80 transition-colors duration-200 font-medium">
                                Remember me
                            </label>
                        </div>

                        <!-- Login Button -->
                        <button
                            type="submit"
                            :disabled="loginForm.processing"
                            class="w-full h-14 font-bold bg-white text-indigo-600 rounded-xl hover:bg-white/90 transition-all duration-300 shadow-2xl hover:shadow-3xl transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed text-lg"
                        >
                            <span class="flex items-center justify-center gap-2">
                                <i v-if="!loginForm.processing" class="pi pi-sign-in text-xl"></i>
                                <i v-else class="pi pi-spin pi-spinner text-xl"></i>
                                {{ loginForm.processing ? 'Logging in...' : 'Login' }}
                            </span>
                        </button>
                    </form>
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

const goToLanding = () => {
    emit('navigate', 'Landing');
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
        
        // Simulate API call - replace with actual backend call later
        setTimeout(() => {
            loginForm.processing = false;
            
            // Use the selected role from dropdown
            const userRole = loginForm.role;
            
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

</script>

<style scoped>
/* Animated Blob Background */
@keyframes blob {
    0% {
        transform: translate(0px, 0px) scale(1);
    }
    33% {
        transform: translate(30px, -50px) scale(1.1);
    }
    66% {
        transform: translate(-20px, 20px) scale(0.9);
    }
    100% {
        transform: translate(0px, 0px) scale(1);
    }
}

.animate-blob {
    animation: blob 7s infinite;
}

.animation-delay-2000 {
    animation-delay: 2s;
}

.animation-delay-4000 {
    animation-delay: 4s;
}

/* Custom Password Input Styling */
:deep(.custom-password .p-password-input) {
    width: 100%;
    height: 3.5rem;
    padding-left: 3rem;
    padding-right: 3rem;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 0.75rem;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    color: white;
    font-weight: 500;
}

:deep(.custom-password .p-password-input::placeholder) {
    color: rgba(255, 255, 255, 0.5);
}

:deep(.custom-password .p-password-input:focus) {
    border-color: rgba(255, 255, 255, 0.5);
    outline: none;
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3);
}

:deep(.custom-password .p-icon) {
    color: rgba(255, 255, 255, 0.7);
}

/* Checkbox Styling */
:deep(.p-checkbox) {
    width: 20px;
    height: 20px;
}

:deep(.p-checkbox .p-checkbox-box) {
    width: 20px;
    height: 20px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 0.375rem;
}

:deep(.p-checkbox .p-checkbox-box.p-highlight) {
    background: white;
    border-color: white;
}

:deep(.p-checkbox .p-checkbox-box.p-highlight .p-checkbox-icon) {
    color: #6366F1;
}

:deep(.p-checkbox-icon) {
    font-size: 12px;
}

/* Input Text Styling */
:deep(.p-inputtext) {
    transition: all 0.3s ease;
}

:deep(.p-inputtext::placeholder) {
    color: rgba(255, 255, 255, 0.5);
}

/* Select Dropdown Styling */
select option {
    background: #6366F1;
    color: white;
    padding: 10px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .w-96 {
        width: 16rem;
        height: 16rem;
    }
}
</style>