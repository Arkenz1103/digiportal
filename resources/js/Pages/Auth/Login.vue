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

        <!-- Floating Elements Background -->
        <div class="absolute inset-0 z-5 overflow-hidden pointer-events-none">
            <!-- Envelope Icons -->
            <div class="floating-element absolute top-20 left-10 text-white/40 text-7xl animate-float-slow">
                <i class="pi pi-envelope"></i>
            </div>
            <div class="floating-element absolute top-40 right-20 text-white/35 text-6xl animate-float-medium" style="animation-delay: 2s;">
                <i class="pi pi-envelope"></i>
            </div>
            
            <!-- Book Icons -->
            <div class="floating-element absolute top-60 left-1/4 text-white/45 text-8xl animate-float-slow" style="animation-delay: 1s;">
                <i class="pi pi-book"></i>
            </div>
            <div class="floating-element absolute bottom-40 right-1/4 text-white/40 text-7xl animate-float-medium" style="animation-delay: 3s;">
                <i class="pi pi-book"></i>
            </div>
            
            <!-- Pencil/Edit Icons -->
            <div class="floating-element absolute top-1/3 right-10 text-white/40 text-6xl animate-float-fast">
                <i class="pi pi-pencil"></i>
            </div>
            <div class="floating-element absolute bottom-1/3 left-20 text-white/35 text-7xl animate-float-slow" style="animation-delay: 2.5s;">
                <i class="pi pi-pencil"></i>
            </div>
            
            <!-- Image/Photo Icons -->
            <div class="floating-element absolute top-1/2 left-1/3 text-white/40 text-6xl animate-float-medium" style="animation-delay: 1.5s;">
                <i class="pi pi-image"></i>
            </div>
            <div class="floating-element absolute bottom-20 right-1/3 text-white/35 text-8xl animate-float-slow" style="animation-delay: 4s;">
                <i class="pi pi-image"></i>
            </div>
            
            <!-- Star Icons -->
            <div class="floating-element absolute top-1/4 right-1/3 text-white/45 text-5xl animate-float-fast" style="animation-delay: 0.5s;">
                <i class="pi pi-star-fill"></i>
            </div>
            <div class="floating-element absolute bottom-1/4 left-1/3 text-white/40 text-6xl animate-float-medium" style="animation-delay: 3.5s;">
                <i class="pi pi-star-fill"></i>
            </div>
            
            <!-- File/Document Icons -->
            <div class="floating-element absolute top-3/4 left-10 text-white/40 text-7xl animate-float-slow" style="animation-delay: 2s;">
                <i class="pi pi-file"></i>
            </div>
            <div class="floating-element absolute top-1/4 right-1/4 text-white/35 text-6xl animate-float-fast" style="animation-delay: 1s;">
                <i class="pi pi-file"></i>
            </div>
            
            <!-- Heart Icons -->
            <div class="floating-element absolute bottom-1/2 right-20 text-white/45 text-5xl animate-float-medium" style="animation-delay: 2.5s;">
                <i class="pi pi-heart-fill"></i>
            </div>
            
            <!-- Palette/Art Icon -->
            <div class="floating-element absolute top-1/2 right-1/3 text-white/40 text-7xl animate-float-slow" style="animation-delay: 3s;">
                <i class="pi pi-palette"></i>
            </div>
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
                <div class="p-5 text-center">
                    <div class="w-16 h-16 bg-white/20 backdrop-blur-md rounded-full mx-auto mb-2 flex items-center justify-center border-2 border-white/30 shadow-lg">
                        <i class="pi pi-user text-3xl text-white"></i>
                    </div>
                    
                    <p class="text-white text-lg font-bold">Sign in to continue to DigiPortal</p>
                </div>

                <!-- Form Section -->
                <div class="px-8 pb-6 pt-1">
                    <form @submit.prevent="submitLogin" class="space-y-4">

                        <!-- Role Selection -->
                        <div>
                            <label class="block text-white mb-2 font-bold text-base">Select Role</label>
                            <div class="relative">
                                <select
                                    v-model="loginForm.role"
                                    class="w-full h-12 px-5 border-2 border-white/40 rounded-2xl focus:ring-0 focus:border-white/60 appearance-none bg-white/20 backdrop-blur-md text-white font-medium cursor-pointer placeholder-white/60 transition-all"
                                    :class="{'border-red-400': loginForm.errors.role}"
                                >
                                    <option value="" disabled class="bg-white text-gray-800">Choose your role</option>
                                    <option value="teacher" class="bg-white text-gray-800">Teacher</option>
                                    <option value="student" class="bg-white text-gray-800">Student</option>
                                </select>
                                <div class="absolute inset-y-0 right-0 flex items-center pr-5 pointer-events-none">
                                    <i class="pi pi-chevron-down text-white text-base"></i>
                                </div>
                            </div>
                            <small class="text-red-200 text-sm mt-1 block" v-if="loginForm.errors.role">{{ loginForm.errors.role }}</small>
                        </div>

                        <!-- Email -->
                        <div>
                            <label class="block text-white mb-2 font-bold text-base">Email</label>
                            <InputText
                                type="email"
                                v-model="loginForm.email"
                                placeholder=""  
                                class="w-full h-12 px-5 border-2 border-white/40 rounded-2xl focus:ring-0 focus:border-white/60 bg-white text-gray-800 placeholder-gray-400 font-medium transition-all"
                                :class="{'border-red-400': loginForm.errors.email}"
                            />
                            <small class="text-red-200 text-sm mt-1 block" v-if="loginForm.errors.email">{{ loginForm.errors.email }}</small>
                        </div>

                        <!-- Password -->
                        <div>
                            <label class="block text-white mb-2 font-bold text-base">Password</label>
                            <div class="relative">
                                <i class="pi pi-lock absolute left-5 top-1/2 transform -translate-y-1/2 text-white/70 text-lg z-20"></i>
                                <Password
                                    v-model="loginForm.password"
                                    placeholder="Enter your password"
                                    :feedback="false"
                                    :toggleMask="true"
                                    class="w-full custom-password-clean"
                                    inputClass="w-full h-12 pl-14 pr-14 border-2 border-white/40 rounded-2xl focus:ring-0 focus:border-white/60 bg-white/20 backdrop-blur-md text-white placeholder-white/60 font-medium"
                                    :class="{'border-red-400': loginForm.errors.password}"
                                />
                            </div>
                            <small class="text-red-200 text-sm mt-1 block" v-if="loginForm.errors.password">{{ loginForm.errors.password }}</small>
                        </div>

                        <!-- Remember Me -->
                        <div class="flex items-center pt-1">
                            <Checkbox v-model="loginForm.remember" :binary="true" inputId="remember" class="mr-3" />
                            <label for="remember" class="text-white select-none cursor-pointer hover:text-white/90 transition-colors duration-200 font-medium text-base">
                                Remember me
                            </label>
                        </div>

                        <!-- Login Button -->
                        <button
                            type="submit"
                            :disabled="loginForm.processing"
                            class="w-full h-12 font-bold bg-white text-indigo-600 rounded-2xl hover:bg-white/95 transition-all duration-300 shadow-xl hover:shadow-2xl disabled:opacity-50 disabled:cursor-not-allowed text-lg mt-2"
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

/* Floating Elements Animations */
@keyframes float-slow {
    0%, 100% {
        transform: translateY(0px) translateX(0px) rotate(0deg);
        opacity: 0.4;
    }
    25% {
        transform: translateY(-30px) translateX(20px) rotate(5deg);
        opacity: 0.5;
    }
    50% {
        transform: translateY(-50px) translateX(-15px) rotate(-5deg);
        opacity: 0.45;
    }
    75% {
        transform: translateY(-20px) translateX(25px) rotate(3deg);
        opacity: 0.42;
    }
}

@keyframes float-medium {
    0%, 100% {
        transform: translateY(0px) translateX(0px) rotate(0deg) scale(1);
        opacity: 0.35;
    }
    33% {
        transform: translateY(-40px) translateX(-25px) rotate(-8deg) scale(1.1);
        opacity: 0.45;
    }
    66% {
        transform: translateY(-25px) translateX(30px) rotate(8deg) scale(0.95);
        opacity: 0.4;
    }
}

@keyframes float-fast {
    0%, 100% {
        transform: translateY(0px) translateX(0px) rotate(0deg) scale(1);
        opacity: 0.4;
    }
    20% {
        transform: translateY(-20px) translateX(15px) rotate(10deg) scale(1.05);
        opacity: 0.5;
    }
    40% {
        transform: translateY(-35px) translateX(-20px) rotate(-10deg) scale(0.95);
        opacity: 0.45;
    }
    60% {
        transform: translateY(-15px) translateX(25px) rotate(5deg) scale(1.1);
        opacity: 0.42;
    }
    80% {
        transform: translateY(-30px) translateX(-10px) rotate(-5deg) scale(1);
        opacity: 0.48;
    }
}

.animate-float-slow {
    animation: float-slow 15s ease-in-out infinite;
}

.animate-float-medium {
    animation: float-medium 12s ease-in-out infinite;
}

.animate-float-fast {
    animation: float-fast 8s ease-in-out infinite;
}

.floating-element {
    filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
    transition: all 0.3s ease;
}

/* Custom Password Input Styling */
:deep(.custom-password-clean .p-password-input) {
    width: 100%;
    height: 3rem;
    padding-left: 3.5rem;
    padding-right: 3.5rem;
    border: 2px solid rgba(255, 255, 255, 0.4);
    border-radius: 1rem;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    color: white;
    font-weight: 500;
    transition: all 0.3s ease;
}

:deep(.custom-password-clean .p-password-input::placeholder) {
    color: rgba(255, 255, 255, 0.6);
}

:deep(.custom-password-clean .p-password-input:focus) {
    border-color: rgba(255, 255, 255, 0.6);
    outline: none;
    box-shadow: none;
}

:deep(.custom-password-clean .p-icon) {
    color: rgba(255, 255, 255, 0.9);
}

/* Checkbox Styling */
:deep(.p-checkbox) {
    width: 22px;
    height: 22px;
}

:deep(.p-checkbox .p-checkbox-box) {
    width: 22px;
    height: 22px;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255, 255, 255, 0.5);
    border-radius: 0.375rem;
    transition: all 0.3s ease;
}

:deep(.p-checkbox .p-checkbox-box.p-highlight) {
    background: white;
    border-color: white;
}

:deep(.p-checkbox .p-checkbox-box.p-highlight .p-checkbox-icon) {
    color: #6366F1;
}

:deep(.p-checkbox-icon) {
    font-size: 13px;
}

/* Input Text Styling */
:deep(.p-inputtext) {
    transition: all 0.3s ease;
}

:deep(.p-inputtext::placeholder) {
    color: rgba(156, 163, 175, 0.8);
}

:deep(.p-inputtext:focus) {
    box-shadow: none;
}

/* Select Dropdown Styling */
select option {
    background: white;
    color: #1f2937;
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