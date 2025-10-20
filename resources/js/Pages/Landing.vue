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
            class="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-[#6366F1] to-[#7C3AED] text-white py-6 shadow-2xl backdrop-blur-md bg-opacity-90"
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
                        class="bg-white/20 backdrop-blur-sm text-white px-6 py-2 rounded-full hover:bg-white/30 transition-all hover:shadow-lg hover:-translate-y-0.5 font-semibold border border-white/30"
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

        <!-- Main Content -->
        <main class="relative z-10 flex items-center justify-center min-h-screen pt-24">
            <div class="container mx-auto px-4">
                <div class="max-w-4xl mx-auto text-center">
                    <!-- Hero Title -->
                    <div 
                        class="mb-12"
                        :class="animateElements.title ? 'animate-fadeInUp' : 'opacity-0 translate-y-10'"
                    >
                        <h1 class="text-6xl md:text-8xl font-black text-white mb-6 leading-tight drop-shadow-2xl">
                            Digital Portfolio
                        </h1>
                        <div class="h-2 w-32 bg-white/80 mx-auto rounded-full"></div>
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
                                ✨ Let's Create - Let's Learn! 🚀
                            </span>
                        </button>
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
