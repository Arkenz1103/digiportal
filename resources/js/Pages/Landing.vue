<script setup>
import { ref, onMounted } from 'vue';

// Use a runtime URL for the logo to avoid Vite import rewriting
const logoUrl = '/logo.jpg';

const animateElements = ref({
  header: false,
  hero: false,
  features: false,
  stats: false
});

onMounted(() => {
  // Stagger animations for smooth entrance
  setTimeout(() => { animateElements.value.header = true; }, 100);
  setTimeout(() => { animateElements.value.hero = true; }, 300);
  setTimeout(() => { animateElements.value.features = true; }, 600);
  setTimeout(() => { animateElements.value.stats = true; }, 900);
});

// Define emits
const emit = defineEmits(['navigate']);

// Navigation functions
const navigateToLogin = () => {
  emit('navigate', 'Login');
};

const navigateToContact = () => {
  alert('Contact: Naawan Central School\nEmail: naawancentral@deped.gov.ph\nPhone: (088) 123-4567');
};

// Features data
const features = [
  {
    icon: 'pi-palette',
    title: 'Creative Portfolio',
    description: 'Showcase student artwork and creative projects in a beautiful digital portfolio',
    color: 'from-purple-500 to-pink-500'
  },
  {
    icon: 'pi-chart-line',
    title: 'Track Progress',
    description: 'Monitor student growth and achievement with comprehensive analytics',
    color: 'from-blue-500 to-cyan-500'
  },
  {
    icon: 'pi-comments',
    title: 'Collaborate',
    description: 'Foster communication between teachers, students, and parents',
    color: 'from-green-500 to-emerald-500'
  },
  {
    icon: 'pi-star-fill',
    title: 'Engage & Inspire',
    description: 'Interactive newsfeed to celebrate and share student achievements',
    color: 'from-yellow-500 to-orange-500'
  }
];
</script>

<template>
    <div class="min-h-screen relative overflow-hidden bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
        <!-- Animated Background Pattern -->
        <div class="absolute inset-0 overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-full opacity-30">
                <div class="absolute top-20 left-10 w-72 h-72 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob"></div>
                <div class="absolute top-40 right-20 w-72 h-72 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000"></div>
                <div class="absolute bottom-20 left-1/3 w-72 h-72 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000"></div>
            </div>
            
            <!-- Grid Pattern -->
            <div class="absolute inset-0 bg-grid-pattern opacity-5"></div>
        </div>

        <!-- Header -->
        <header 
            class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-xl shadow-lg border-b border-gray-200/50"
            :class="animateElements.header ? 'animate-slideInDown' : 'opacity-0 -translate-y-full'"
        >
            <div class="container mx-auto px-6 py-4">
                <div class="flex justify-between items-center">
                    <div class="flex items-center gap-4">
                        <div class="relative group">
                            <div class="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full blur opacity-75 group-hover:opacity-100 transition duration-300"></div>
                            <img
                                :src="logoUrl"
                                class="relative h-14 w-14 rounded-full border-2 border-white shadow-xl transform group-hover:scale-110 transition-transform duration-300"
                                alt="Naawan Central School Logo"
                            />
                        </div>
                        <div>
                            <div class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                                Naawan Central School
                            </div>
                            <div class="text-xs text-gray-600 font-medium">Digital Portfolio System</div>
                        </div>
                    </div>
                    <nav class="flex gap-3">
                        <button
                            @click="navigateToContact"
                            class="px-6 py-2.5 text-gray-700 hover:text-blue-600 font-semibold transition-all duration-300 hover:scale-105"
                        >
                            Contact Us
                        </button>
                        <button
                            @click="navigateToLogin"
                            class="px-8 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-full hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105 font-semibold"
                        >
                            Login
                        </button>
                    </nav>
                </div>
            </div>
        </header>

        <!-- Main Content -->
        <main class="relative z-10 pt-24">
            <!-- Hero Section -->
            <section class="container mx-auto px-6 py-20">
                <div 
                    class="max-w-6xl mx-auto"
                    :class="animateElements.hero ? 'animate-fadeInUp' : 'opacity-0 translate-y-10'"
                >
                    <div class="grid md:grid-cols-2 gap-12 items-center">
                        <!-- Left Content -->
                        <div class="text-left space-y-6">
                            <div class="inline-block px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold mb-4">
                                ✨ Welcome to DigiPortal
                            </div>
                            <h1 class="text-5xl md:text-6xl font-black text-gray-900 leading-tight">
                                Empower
                                <span class="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent"> Creative Learning</span>
                            </h1>
                            <p class="text-xl text-gray-600 leading-relaxed">
                                A modern digital portfolio system that celebrates student creativity, tracks progress, and fosters collaboration between teachers and learners.
                            </p>
                            <div class="flex gap-4 pt-4">
                                <button
                                    @click="navigateToLogin"
                                    class="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-xl hover:shadow-2xl hover:scale-105 font-bold text-lg flex items-center gap-2"
                                >
                                    <i class="pi pi-sign-in"></i>
                                    Get Started
                                </button>
                                <button
                                    @click="navigateToContact"
                                    class="px-8 py-4 bg-white text-gray-700 rounded-xl hover:bg-gray-50 transition-all duration-300 shadow-lg hover:shadow-xl font-semibold text-lg border-2 border-gray-200"
                                >
                                    Learn More
                                </button>
                            </div>
                        </div>

                        <!-- Right Visual -->
                        <div class="relative">
                            <div class="relative w-full aspect-square max-w-md mx-auto">
                                <!-- Decorative Elements -->
                                <div class="absolute inset-0 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-3xl transform rotate-6 opacity-20"></div>
                                <div class="absolute inset-0 bg-gradient-to-br from-purple-500 to-pink-600 rounded-3xl transform -rotate-6 opacity-20"></div>
                                
                                <!-- Main Circle -->
                                <div class="relative bg-white rounded-3xl shadow-2xl p-8 flex items-center justify-center">
                                    <div class="relative w-full h-full">
                                        <!-- Center Icon -->
                                        <div class="absolute inset-0 flex items-center justify-center">
                                            <div class="w-32 h-32 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-full flex items-center justify-center shadow-xl animate-pulse-slow">
                                                <i class="pi pi-graduation-cap text-5xl text-white"></i>
                                            </div>
                                        </div>

                                        <!-- Orbiting Icons -->
                                        <div class="orbit-container">
                                            <div class="orbit-item orbit-1">
                                                <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center shadow-lg">
                                                    <i class="pi pi-palette text-2xl text-white"></i>
                                                </div>
                                            </div>
                                            <div class="orbit-item orbit-2">
                                                <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full flex items-center justify-center shadow-lg">
                                                    <i class="pi pi-chart-line text-2xl text-white"></i>
                                                </div>
                                            </div>
                                            <div class="orbit-item orbit-3">
                                                <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center shadow-lg">
                                                    <i class="pi pi-comments text-2xl text-white"></i>
                                                </div>
                                            </div>
                                            <div class="orbit-item orbit-4">
                                                <div class="w-16 h-16 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-full flex items-center justify-center shadow-lg">
                                                    <i class="pi pi-star-fill text-2xl text-white"></i>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Features Section -->
            <section 
                class="container mx-auto px-6 py-20"
                :class="animateElements.features ? 'animate-fadeIn' : 'opacity-0'"
            >
                <div class="max-w-6xl mx-auto">
                    <div class="text-center mb-16">
                        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                            Why Choose <span class="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">DigiPortal</span>?
                        </h2>
                        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
                            Everything you need to showcase creativity, track progress, and inspire learning
                        </p>
                    </div>

                    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                        <div 
                            v-for="(feature, index) in features" 
                            :key="index"
                            class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100"
                        >
                            <div :class="`w-16 h-16 bg-gradient-to-br ${feature.color} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg`">
                                <i :class="`pi ${feature.icon} text-3xl text-white`"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-900 mb-3">{{ feature.title }}</h3>
                            <p class="text-gray-600 leading-relaxed">{{ feature.description }}</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Stats Section -->
            <section 
                class="container mx-auto px-6 py-20"
                :class="animateElements.stats ? 'animate-fadeInUp' : 'opacity-0 translate-y-10'"
            >
                <div class="max-w-6xl mx-auto">
                    <div class="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-3xl p-12 shadow-2xl">
                        <div class="grid md:grid-cols-3 gap-8 text-center text-white">
                            <div class="space-y-2">
                                <div class="text-5xl font-bold">1000+</div>
                                <div class="text-blue-100 text-lg">Student Portfolios</div>
                            </div>
                            <div class="space-y-2">
                                <div class="text-5xl font-bold">50+</div>
                                <div class="text-blue-100 text-lg">Active Teachers</div>
                            </div>
                            <div class="space-y-2">
                                <div class="text-5xl font-bold">5000+</div>
                                <div class="text-blue-100 text-lg">Creative Works</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- CTA Section -->
            <section class="container mx-auto px-6 py-20">
                <div class="max-w-4xl mx-auto text-center">
                    <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                        Ready to Start Your Creative Journey?
                    </h2>
                    <p class="text-xl text-gray-600 mb-8">
                        Join Naawan Central School's digital learning community today
                    </p>
                    <button
                        @click="navigateToLogin"
                        class="px-12 py-5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-2xl hover:shadow-3xl hover:scale-105 font-bold text-xl inline-flex items-center gap-3"
                    >
                        <i class="pi pi-rocket"></i>
                        Let's Create - Let's Explore!
                    </button>
                </div>
            </section>
        </main>

        <!-- Footer -->
        <footer class="relative z-10 bg-gray-900 text-white py-8">
            <div class="container mx-auto px-6 text-center">
                <p class="text-gray-400">© 2025 Naawan Central School. All rights reserved.</p>
                <p class="text-gray-500 text-sm mt-2">Digital Portfolio Management System</p>
            </div>
        </footer>
    </div>
</template>

<style scoped>
/* Grid Pattern Background */
.bg-grid-pattern {
    background-image: 
        linear-gradient(to right, rgba(0, 0, 0, 0.05) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 0, 0, 0.05) 1px, transparent 1px);
    background-size: 40px 40px;
}

/* Animated Blob Background */
@keyframes blob {
    0%, 100% {
        transform: translate(0px, 0px) scale(1);
    }
    33% {
        transform: translate(30px, -50px) scale(1.1);
    }
    66% {
        transform: translate(-20px, 20px) scale(0.9);
    }
}

.animate-blob {
    animation: blob 10s infinite ease-in-out;
}

.animation-delay-2000 {
    animation-delay: 2s;
}

.animation-delay-4000 {
    animation-delay: 4s;
}

/* Orbit Animations */
.orbit-container {
    position: relative;
    width: 100%;
    height: 100%;
}

.orbit-item {
    position: absolute;
    top: 50%;
    left: 50%;
    animation: orbit 20s linear infinite;
}

.orbit-1 {
    animation-delay: 0s;
}

.orbit-2 {
    animation-delay: -5s;
}

.orbit-3 {
    animation-delay: -10s;
}

.orbit-4 {
    animation-delay: -15s;
}

@keyframes orbit {
    0% {
        transform: translate(-50%, -50%) rotate(0deg) translateX(140px) rotate(0deg);
    }
    100% {
        transform: translate(-50%, -50%) rotate(360deg) translateX(140px) rotate(-360deg);
    }
}

@keyframes slideInDown {
    from {
        opacity: 0;
        transform: translate3d(0, -100%, 0);
    }
    to {
        opacity: 1;
        transform: translate3d(0, 0, 0);
    }
}

@keyframes bounceInDown {
    0%, 60%, 75%, 90%, 100% {
        animation-timing-function: cubic-bezier(0.215, 0.610, 0.355, 1.000);
    }
    0% {
        opacity: 0;
        transform: translate3d(0, -3000px, 0) scaleY(3);
    }
    60% {
        opacity: 1;
        transform: translate3d(0, 25px, 0) scaleY(0.9);
    }
    75% {
        transform: translate3d(0, -10px, 0) scaleY(0.95);
    }
    90% {
        transform: translate3d(0, 5px, 0) scaleY(0.985);
    }
    100% {
        transform: translate3d(0, 0, 0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translate3d(0, 100%, 0);
    }
    to {
        opacity: 1;
        transform: translate3d(0, 0, 0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes bounceIn {
    0%, 20%, 40%, 60%, 80%, 100% {
        animation-timing-function: cubic-bezier(0.215, 0.610, 0.355, 1.000);
    }
    0% {
        opacity: 0;
        transform: scale3d(0.3, 0.3, 0.3);
    }
    20% {
        transform: scale3d(1.1, 1.1, 1.1);
    }
    40% {
        transform: scale3d(0.9, 0.9, 0.9);
    }
    60% {
        opacity: 1;
        transform: scale3d(1.03, 1.03, 1.03);
    }
    80% {
        transform: scale3d(0.97, 0.97, 0.97);
    }
    100% {
        opacity: 1;
        transform: scale3d(1, 1, 1);
    }
}

/* Animation Classes */
.animate-blob {
    animation: blob 7s infinite;
}

.animation-delay-2000 {
    animation-delay: 2s;
}

.animation-delay-4000 {
    animation-delay: 4s;
}

.animate-slideInDown {
    animation: slideInDown 0.8s ease-out;
}

.animate-bounceInDown {
    animation: bounceInDown 1.2s ease-out;
}

.animate-fadeInUp {
    animation: fadeInUp 0.8s ease-out;
}

.animate-fadeIn {
    animation: fadeIn 1s ease-out;
}

.animate-bounceIn {
    animation: bounceIn 1s ease-out;
}

/* Custom Utilities */
.border-3 {
    border-width: 3px;
}

.shadow-3xl {
    box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.25);
}

/* Pulse Animation */
@keyframes pulse-slow {
    0%, 100% {
        transform: scale(1);
        opacity: 1;
    }
    50% {
        transform: scale(1.05);
        opacity: 0.95;
    }
}

.animate-pulse-slow {
    animation: pulse-slow 3s ease-in-out infinite;
}

/* Responsive Design */
@media (max-width: 1024px) {
    .orbit-item {
        animation: orbit 25s linear infinite;
    }
    
    @keyframes orbit {
        0% {
            transform: translate(-50%, -50%) rotate(0deg) translateX(120px) rotate(0deg);
        }
        100% {
            transform: translate(-50%, -50%) rotate(360deg) translateX(120px) rotate(-360deg);
        }
    }
}

@media (max-width: 768px) {
    .text-5xl { font-size: 2.5rem; }
    .text-6xl { font-size: 3rem; }
    .text-4xl { font-size: 2rem; }
    
    header .text-2xl { font-size: 1.5rem; }
    header .text-xs { font-size: 0.65rem; }
    
    .grid.md\\:grid-cols-2 {
        grid-template-columns: 1fr;
    }
    
    .orbit-item {
        animation: orbit 20s linear infinite;
    }
    
    @keyframes orbit {
        0% {
            transform: translate(-50%, -50%) rotate(0deg) translateX(100px) rotate(0deg);
        }
        100% {
            transform: translate(-50%, -50%) rotate(360deg) translateX(100px) rotate(-360deg);
        }
    }
    
    .orbit-item > div {
        width: 3rem;
        height: 3rem;
    }
    
    .orbit-item i {
        font-size: 1.25rem;
    }
}

@media (max-width: 640px) {
    .text-5xl { font-size: 2rem; }
    .text-6xl { font-size: 2.5rem; }
    .text-4xl { font-size: 1.75rem; }
    .text-xl { font-size: 1.125rem; }
    
    header nav {
        gap: 0.5rem;
    }
    
    header nav button {
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
    }
    
    .px-8 { padding-left: 1.5rem; padding-right: 1.5rem; }
    .py-4 { padding-top: 1rem; padding-bottom: 1rem; }
    
    .orbit-item {
        animation: orbit 18s linear infinite;
    }
    
    @keyframes orbit {
        0% {
            transform: translate(-50%, -50%) rotate(0deg) translateX(80px) rotate(0deg);
        }
        100% {
            transform: translate(-50%, -50%) rotate(360deg) translateX(80px) rotate(-360deg);
        }
    }
}
</style>
