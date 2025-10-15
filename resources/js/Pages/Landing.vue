<script setup>
import { ref, onMounted } from 'vue';

// Use a runtime URL for the logo to avoid Vite import rewriting
const logoUrl = '/logo.jpg';

const animateElements = ref({
  header: false,
  title: false,
  subtitle: false,
  description: false,
  cta: false,
  features: false
});

const isLoaded = ref(false);

onMounted(() => {
  // Stagger animations for smooth entrance
  setTimeout(() => { animateElements.value.header = true; }, 100);
  setTimeout(() => { animateElements.value.title = true; }, 400);
  setTimeout(() => { animateElements.value.subtitle = true; }, 700);
  setTimeout(() => { animateElements.value.description = true; }, 1000);
  setTimeout(() => { animateElements.value.cta = true; }, 1300);
  setTimeout(() => { animateElements.value.features = true; }, 1600);
  setTimeout(() => { isLoaded.value = true; }, 2000);
});

// Define emits
const emit = defineEmits(['navigate']);

// Navigation functions
const navigateToLogin = () => {
  emit('navigate', 'login');
};

const navigateToContact = () => {
  alert('Contact page coming soon!');
};
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100 relative overflow-hidden">
        <!-- Animated Background Elements -->
        <div class="absolute inset-0 overflow-hidden">
            <div class="absolute -top-40 -right-40 w-80 h-80 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
            <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
            <div class="absolute top-40 left-40 w-80 h-80 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
        </div>

        <!-- Header -->
        <header 
            class="relative z-10 bg-gradient-to-r from-[#6366F1] to-[#7C3AED] text-white py-6 shadow-2xl"
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
                        <div class="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-white animate-pulse"></div>
                    </div>
                    <div>
                        <div class="text-2xl font-bold tracking-wide">Naawan Central School</div>
                        <div class="text-sm opacity-90">Creative Learning Platform</div>
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
        <main class="relative z-10 container mx-auto px-4 py-16 md:py-24">
            <div class="max-w-6xl mx-auto text-center">
                <!-- Main Title -->
                <div class="mb-16">
                    <h1
                        class="text-6xl md:text-7xl lg:text-8xl font-black text-transparent bg-clip-text bg-gradient-to-r from-[#6366F1] via-[#7C3AED] to-[#EC4899] mb-6 leading-tight tracking-tight"
                        :class="animateElements.title ? 'animate-bounceInDown' : 'opacity-0 translate-y-10'"
                    >
                        CREATIVE LEARNING
                    </h1>

                    <!-- Subtitle -->
                    <h2
                        class="text-4xl md:text-5xl font-bold text-gray-800 mb-8 relative"
                        :class="animateElements.subtitle ? 'animate-fadeInUp' : 'opacity-0 translate-y-10'"
                    >
                        For Young Artists & Explorers!
                        <div class="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-32 h-1 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full"></div>
                    </h2>

                    <!-- Description -->
                    <p
                        class="text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed"
                        :class="animateElements.description ? 'animate-fadeIn' : 'opacity-0'"
                    >
                        🎨 Creative kids having fun while learning! 🌟
                        <br>
                        <span class="text-lg text-gray-500 mt-2 block">Unleash your imagination and discover the joy of creative expression</span>
                    </p>

                    <!-- CTA Button -->
                    <div 
                        class="mb-20"
                        :class="animateElements.cta ? 'animate-bounceIn' : 'opacity-0 scale-95'"
                    >
                        <button
                            @click="navigateToLogin"
                            class="group relative inline-flex items-center justify-center px-12 py-6 text-2xl font-bold text-white bg-gradient-to-r from-[#10B981] via-[#059669] to-[#047857] rounded-2xl shadow-2xl hover:shadow-3xl transform hover:-translate-y-2 transition-all duration-300 border-4 border-white"
                        >
                            <span class="relative z-10 flex items-center gap-3">
                                ✨ Let's Create - Let's Learn! 🚀
                            </span>
                            <div class="absolute inset-0 bg-gradient-to-r from-[#059669] to-[#047857] rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        </button>
                    </div>
                </div>

                <!-- Features Grid -->
                <div
                    class="grid grid-cols-1 md:grid-cols-3 gap-8 lg:gap-12"
                    :class="animateElements.features ? 'animate-fadeInUp' : 'opacity-0 translate-y-10'"
                >
                    <!-- Feature 1 -->
                    <div class="group relative bg-white/80 backdrop-blur-sm p-8 rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-4 border border-purple-100">
                        <div class="absolute inset-0 bg-gradient-to-br from-purple-400/20 to-pink-400/20 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                        <div class="relative z-10">
                            <div class="text-7xl mb-6 transform group-hover:scale-110 transition-transform duration-300">🎨</div>
                            <h3 class="text-2xl font-bold mb-4 text-gray-800 group-hover:text-purple-600 transition-colors">Colorful Boards</h3>
                            <p class="text-gray-600 leading-relaxed">Paint your ideas in vibrant colors and bring your imagination to life with our interactive canvas</p>
                            <div class="mt-4 w-full h-1 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500"></div>
                        </div>
                    </div>

                    <!-- Feature 2 -->
                    <div class="group relative bg-white/80 backdrop-blur-sm p-8 rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-4 border border-blue-100">
                        <div class="absolute inset-0 bg-gradient-to-br from-blue-400/20 to-cyan-400/20 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                        <div class="relative z-10">
                            <div class="text-7xl mb-6 transform group-hover:scale-110 transition-transform duration-300">✏️</div>
                            <h3 class="text-2xl font-bold mb-4 text-gray-800 group-hover:text-blue-600 transition-colors">Draw & Doodle</h3>
                            <p class="text-gray-600 leading-relaxed">Express yourself freely with our intuitive drawing tools and unleash your creative potential</p>
                            <div class="mt-4 w-full h-1 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-full transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500"></div>
                        </div>
                    </div>

                    <!-- Feature 3 -->
                    <div class="group relative bg-white/80 backdrop-blur-sm p-8 rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-4 border border-yellow-100">
                        <div class="absolute inset-0 bg-gradient-to-br from-yellow-400/20 to-orange-400/20 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                        <div class="relative z-10">
                            <div class="text-7xl mb-6 transform group-hover:scale-110 transition-transform duration-300">🌟</div>
                            <h3 class="text-2xl font-bold mb-4 text-gray-800 group-hover:text-yellow-600 transition-colors">Share & Shine</h3>
                            <p class="text-gray-600 leading-relaxed">Show your masterpieces to friends and celebrate your creative achievements together</p>
                            <div class="mt-4 w-full h-1 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500"></div>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <!-- Footer -->
        <footer class="relative z-10 bg-gradient-to-r from-[#6366F1] via-[#7C3AED] to-[#EC4899] text-white py-12 mt-24">
            <div class="container mx-auto px-4">
                <div class="text-center">
                    <div class="flex justify-center items-center gap-2 mb-4">
                        <span class="text-2xl">🎨</span>
                        <p class="text-xl font-semibold">Made with ❤️ for creative kids</p>
                        <span class="text-2xl">✨</span>
                    </div>
                    <p class="text-lg opacity-90">Naawan Central School - Creative Learning Platform</p>
                    <div class="mt-6 flex justify-center gap-6">
                        <div class="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                        <div class="w-2 h-2 bg-white rounded-full animate-pulse" style="animation-delay: 0.2s;"></div>
                        <div class="w-2 h-2 bg-white rounded-full animate-pulse" style="animation-delay: 0.4s;"></div>
                    </div>
                </div>
            </div>
        </footer>
    </div>
</template>

<style scoped>
/* Modern CSS Animations */
@keyframes blob {
    0% { transform: translate(0px, 0px) scale(1); }
    33% { transform: translate(30px, -50px) scale(1.1); }
    66% { transform: translate(-20px, 20px) scale(0.9); }
    100% { transform: translate(0px, 0px) scale(1); }
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
</style>
