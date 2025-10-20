<script setup>
import { ref, onMounted } from 'vue';

// Use a runtime URL for the logo to avoid Vite import rewriting
const logoUrl = '/logo.jpg';

const animateElements = ref({
  header: false,
  title: false,
  cta: false
});

onMounted(() => {
  // Stagger animations for smooth entrance
  setTimeout(() => { animateElements.value.header = true; }, 100);
  setTimeout(() => { animateElements.value.title = true; }, 400);
  setTimeout(() => { animateElements.value.cta = true; }, 800);
});

// Define emits
const emit = defineEmits(['navigate']);

// Navigation functions
const navigateToLogin = () => {
  emit('navigate', 'Login');
};

const navigateToContact = () => {
  alert('Contact page coming soon!');
};
</script>

<template>
    <div class="min-h-screen relative overflow-hidden">
        <!-- Animated Background -->
        <div class="absolute inset-0 bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800">
            <!-- Animated Circles -->
            <div class="absolute top-0 left-0 w-96 h-96 bg-cyan-400 opacity-10 rounded-full mix-blend-multiply filter blur-xl animate-blob"></div>
            <div class="absolute top-0 right-0 w-96 h-96 bg-blue-300 opacity-10 rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-2000"></div>
            <div class="absolute bottom-0 left-1/2 w-96 h-96 bg-indigo-400 opacity-10 rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-4000"></div>
        </div>

        <!-- Header -->
        <header 
            class="fixed top-0 left-0 right-0 z-50 bg-white/10 backdrop-blur-xl text-white py-6 shadow-2xl border-b border-white/20"
            :class="animateElements.header ? 'animate-slideInDown' : 'opacity-0 -translate-y-full'"
        >
            <div class="container mx-auto px-4 flex justify-between items-center">
                <div class="flex items-center gap-4">
                    <div class="relative">
                        <img
                            :src="logoUrl"
                            class="h-12 w-12 rounded-full border-3 border-white shadow-lg transform hover:scale-110 transition-transform duration-300"
                            alt="Naawan Central School Logo"
                        />
                    </div>
                    <div>
                        <div class="text-2xl font-bold tracking-wide">Naawan Central School</div>
                    </div>
                </div>
                <nav class="flex gap-3">
                    <button
                        @click="navigateToContact"
                        class="bg-white text-[#6366F1] px-6 py-2 rounded-full hover:bg-gray-100 transition-all hover:shadow-lg hover:-translate-y-0.5 font-semibold"
                    >
                        Contact Us
                    </button>
                    <button
                        @click="navigateToLogin"
                        class="bg-white text-[#6366F1] px-6 py-2 rounded-full hover:bg-gray-100 transition-all hover:shadow-lg hover:-translate-y-0.5 font-semibold"
                    >
                        Login
                    </button>
                </nav>
            </div>
        </header>

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

        <!-- Main Content -->
        <main class="relative z-10 flex items-center justify-center min-h-screen pt-24">
            <div class="container mx-auto px-4">
                <div class="max-w-4xl mx-auto text-center">
                    <!-- Hero Title -->
                    <div 
                        class="mb-8 mt-16"
                        :class="animateElements.title ? 'animate-fadeInUp' : 'opacity-0 translate-y-10'"
                    >
                        <h1 class="text-5xl md:text-6xl font-black text-white mb-4 leading-tight drop-shadow-2xl">
                            Digital Portfolio
                        </h1>
                        <div class="h-1.5 w-24 bg-white/80 mx-auto rounded-full"></div>
                    </div>

                    <!-- CTA Button -->
                    <div 
                        class="mt-12"
                        :class="animateElements.cta ? 'animate-bounceIn' : 'opacity-0 scale-95'"
                    >
                        <button
                            @click="navigateToLogin"
                            class="w-full max-w-md h-16 font-bold bg-white text-indigo-600 rounded-xl hover:bg-white/90 transition-all duration-300 shadow-2xl hover:shadow-3xl transform hover:-translate-y-1 text-xl"
                        >
                            <span class="flex items-center justify-center gap-3">
                                ✨ Let's Create - Let's Explore! 🚀
                            </span>
                        </button>
                    </div>

                    <!-- Learning Wheel -->
                    <div class="mt-16 flex justify-center">
                        <div class="relative w-80 h-80 wheel-container">
                            <!-- Center Circle -->
                            <div class="absolute inset-0 flex items-center justify-center">
                                <div class="wheel-center w-32 h-32 bg-white/20 backdrop-blur-xl rounded-full border-4 border-white/40 shadow-2xl flex items-center justify-center animate-pulse-slow cursor-pointer">
                                    <i class="pi pi-graduation-cap text-5xl text-white"></i>
                                </div>
                            </div>

                            <!-- Orbiting Icons -->
                            <div class="wheel-item wheel-item-1 absolute w-20 h-20 bg-white/30 backdrop-blur-lg rounded-full border-3 border-white/50 shadow-xl flex items-center justify-center transition-all cursor-pointer">
                                <i class="pi pi-user text-3xl text-white"></i>
                            </div>
                            <div class="wheel-item wheel-item-2 absolute w-20 h-20 bg-white/30 backdrop-blur-lg rounded-full border-3 border-white/50 shadow-xl flex items-center justify-center transition-all cursor-pointer">
                                <i class="pi pi-user text-3xl text-white"></i>
                            </div>
                            <div class="wheel-item wheel-item-3 absolute w-20 h-20 bg-white/30 backdrop-blur-lg rounded-full border-3 border-white/50 shadow-xl flex items-center justify-center transition-all cursor-pointer">
                                <i class="pi pi-user text-3xl text-white"></i>
                            </div>
                            <div class="wheel-item wheel-item-4 absolute w-20 h-20 bg-white/30 backdrop-blur-lg rounded-full border-3 border-white/50 shadow-xl flex items-center justify-center transition-all cursor-pointer">
                                <i class="pi pi-user text-3xl text-white"></i>
                            </div>
                            <div class="wheel-item wheel-item-5 absolute w-20 h-20 bg-white/30 backdrop-blur-lg rounded-full border-3 border-white/50 shadow-xl flex items-center justify-center transition-all cursor-pointer">
                                <i class="pi pi-user text-3xl text-white"></i>
                            </div>
                            <div class="wheel-item wheel-item-6 absolute w-20 h-20 bg-white/30 backdrop-blur-lg rounded-full border-3 border-white/50 shadow-xl flex items-center justify-center transition-all cursor-pointer">
                                <i class="pi pi-user text-3xl text-white"></i>
                            </div>
                            <div class="wheel-item wheel-item-7 absolute w-20 h-20 bg-white/30 backdrop-blur-lg rounded-full border-3 border-white/50 shadow-xl flex items-center justify-center transition-all cursor-pointer">
                                <i class="pi pi-user text-3xl text-white"></i>
                            </div>
                            <div class="wheel-item wheel-item-8 absolute w-20 h-20 bg-white/30 backdrop-blur-lg rounded-full border-3 border-white/50 shadow-xl flex items-center justify-center transition-all cursor-pointer">
                                <i class="pi pi-user text-3xl text-white"></i>
                            </div>

                            <!-- Connecting Lines -->
                            <svg class="absolute inset-0 w-full h-full -z-10" viewBox="0 0 320 320">
                                <circle cx="160" cy="160" r="120" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2" stroke-dasharray="5,5" class="animate-spin-slow"/>
                            </svg>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

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

/* Learning Wheel Positioning */
.wheel-item {
    position: absolute;
    top: 50%;
    left: 50%;
    opacity: 0;
    transform: translate(-50%, -50%) scale(0);
    transition: all 0.5s ease;
    pointer-events: none;
}

.wheel-container:hover .wheel-item {
    opacity: 1;
    pointer-events: auto;
}

.wheel-item:hover {
    transform: translate(-50%, -50%) scale(1.2) !important;
    box-shadow: 0 10px 30px rgba(255, 255, 255, 0.3);
    z-index: 10;
}

.wheel-center:hover {
    transform: scale(1.1);
    box-shadow: 0 15px 40px rgba(255, 255, 255, 0.4);
}

.wheel-item-1 {
    transform: translate(-50%, -50%) translateY(-130px);
    transition-delay: 0.1s;
}

.wheel-item-2 {
    transform: translate(-50%, -50%) translate(92px, -92px);
    transition-delay: 0.15s;
}

.wheel-item-3 {
    transform: translate(-50%, -50%) translateX(130px);
    transition-delay: 0.2s;
}

.wheel-item-4 {
    transform: translate(-50%, -50%) translate(92px, 92px);
    transition-delay: 0.25s;
}

.wheel-item-5 {
    transform: translate(-50%, -50%) translateY(130px);
    transition-delay: 0.3s;
}

.wheel-item-6 {
    transform: translate(-50%, -50%) translate(-92px, 92px);
    transition-delay: 0.35s;
}

.wheel-item-7 {
    transform: translate(-50%, -50%) translateX(-130px);
    transition-delay: 0.4s;
}

.wheel-item-8 {
    transform: translate(-50%, -50%) translate(-92px, -92px);
    transition-delay: 0.45s;
}

@keyframes spin-slow {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

@keyframes pulse-slow {
    0%, 100% {
        transform: scale(1);
        opacity: 1;
    }
    50% {
        transform: scale(1.05);
        opacity: 0.9;
    }
}

.animate-spin-slow {
    animation: spin-slow 30s linear infinite;
}

.animate-pulse-slow {
    animation: pulse-slow 3s ease-in-out infinite;
}

/* Responsive Design */
@media (max-width: 768px) {
    .text-6xl { font-size: 3.5rem; }
    .text-7xl { font-size: 4rem; }
    .text-8xl { font-size: 4.5rem; }
    .text-4xl { font-size: 2.5rem; }
    .text-5xl { font-size: 3rem; }
    
    .px-12 { padding-left: 2rem; padding-right: 2rem; }
    .py-6 { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    .text-2xl { font-size: 1.5rem; }
}

@media (max-width: 640px) {
    .text-6xl { font-size: 2.5rem; }
    .text-7xl { font-size: 3rem; }
    .text-8xl { font-size: 3.5rem; }
    .text-4xl { font-size: 2rem; }
    .text-5xl { font-size: 2.5rem; }
    
    .px-12 { padding-left: 1.5rem; padding-right: 1.5rem; }
    .py-6 { padding-top: 1rem; padding-bottom: 1rem; }
    .text-2xl { font-size: 1.25rem; }
    
    .gap-8 { gap: 1.5rem; }
    .p-8 { padding: 1.5rem; }
}

/* Enhanced Hover Effects */
.group:hover .group-hover\:scale-110 {
    transform: scale(1.1);
}

.group:hover .group-hover\:text-purple-600 {
    color: rgb(147 51 234);
}

.group:hover .group-hover\:text-blue-600 {
    color: rgb(37 99 235);
}

.group:hover .group-hover\:text-yellow-600 {
    color: rgb(202 138 4);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .w-96 {
        width: 16rem;
        height: 16rem;
    }
    
    .text-6xl { font-size: 3rem; }
    .text-8xl { font-size: 4rem; }
}
</style>
