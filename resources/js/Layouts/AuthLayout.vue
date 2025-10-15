<template>
    <div class="relative min-h-screen bg-gray-50 p-1 overflow-hidden">
        <!-- Artsy Background Animation -->
        <div class="absolute inset-0 overflow-hidden z-0">
            <!-- Floating elements with violet theme -->
            <div v-for="i in 25" :key="'circle-'+i" 
                class="absolute rounded-full opacity-20 animate-float"
                :class="[
                    i % 2 === 0 ? 'bg-[#B8AAFF]' : 'bg-[#9D8AFF]',
                    i % 3 === 0 ? 'animate-float-reverse' : '',
                    i % 4 === 0 ? 'rounded-none transform rotate-45' : ''
                ]"
                :style="{
                    width: `${Math.random() * 300 + 50}px`,
                    height: `${Math.random() * 300 + 50}px`,
                    left: `${Math.random() * 100}%`,
                    top: `${Math.random() * 100}%`,
                    animationDuration: `${Math.random() * 30 + 20}s`,
                    animationDelay: `${Math.random() * 5}s`
                }"
            ></div>
            
            <!-- Improved wavy lines in violet shades -->
            <div class="absolute inset-0 opacity-15">
                <svg viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg" class="w-full h-full">
                    <path 
                        d="M0,100 C150,200 350,0 500,100 C650,200 750,300 1000,100 C1150,0 1200,150 1200,200" 
                        fill="none" 
                        stroke="#B8AAFF" 
                        stroke-width="6"
                        stroke-dasharray="10 5"
                        class="animate-wave"
                    />
                    <path 
                        d="M0,300 C150,400 350,200 500,300 C650,400 750,500 1000,300 C1150,200 1200,350 1200,400" 
                        fill="none" 
                        stroke="#9D8AFF" 
                        stroke-width="6"
                        stroke-dasharray="15 7"
                        class="animate-wave-slow"
                    />
                    <path 
                        d="M0,500 C150,600 350,400 500,500 C650,600 750,700 1000,500 C1150,400 1200,550 1200,600" 
                        fill="none" 
                        stroke="#7E5BFF" 
                        stroke-width="6"
                        stroke-dasharray="20 10"
                        class="animate-wave-slower"
                    />
                </svg>
            </div>
        </div>

        <div class="flex min-h-full relative z-10">
            <!-- Left side with back button -->
            <div class="w-16 p-4 z-20 relative">
                <Link href="/" class="flex items-center justify-center w-10 h-10 rounded-full bg-white/80 backdrop-blur-sm text-[#0E1836] hover:text-[#B8AAFF] hover:bg-white/90 transition-all duration-200 shadow-md">
                    <i class="pi pi-arrow-left text-xl"></i>
                </Link>
            </div>

            <!-- Main content - Expanded form area -->
            <div class="flex-1 flex items-center justify-center px-4 py-8">
                <div class="w-full max-w-6xl rounded-2xl relative z-20">
                    <!-- Expanded form slot with more padding -->
                    <div class="px-6 pb-6">
                        <slot />
                    </div>

                    <!-- Additional footer content with improved styling -->
                    <div class="mt-6 pt-6 border-t border-gray-100/50 text-center text-gray-600 text-sm backdrop-blur-sm bg-white/30 rounded-b-2xl p-4">
                        Need help? <a href="#" class="text-[#B8AAFF] hover:text-[#7E5BFF] font-medium transition-colors">Contact support</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Link } from '@inertiajs/vue3';
</script>

<style scoped>
/* Enhanced floating animation */
@keyframes float {
    0% {
        transform: translateY(0) rotate(0deg);
        opacity: 0.15;
    }
    50% {
        transform: translateY(-30px) rotate(5deg);
        opacity: 0.25;
    }
    100% {
        transform: translateY(0) rotate(0deg);
        opacity: 0.15;
    }
}

@keyframes float-reverse {
    0% {
        transform: translateY(0) rotate(0deg);
        opacity: 0.15;
    }
    50% {
        transform: translateY(30px) rotate(-5deg);
        opacity: 0.25;
    }
    100% {
        transform: translateY(0) rotate(0deg);
        opacity: 0.15;
    }
}

@keyframes wave {
    0% {
        transform: translateX(0);
    }
    50% {
        transform: translateX(-30px);
    }
    100% {
        transform: translateX(0);
    }
}

.animate-float {
    animation: float 20s infinite ease-in-out;
}

.animate-float-reverse {
    animation: float-reverse 25s infinite ease-in-out;
}

.animate-wave {
    animation: wave 15s infinite ease-in-out;
}

.animate-wave-slow {
    animation: wave 20s infinite ease-in-out reverse;
}

.animate-wave-slower {
    animation: wave 25s infinite ease-in-out;
}

/* Form styling with violet theme */
:deep(.form-input) {
    border: 2px solid #E5E7EB;
    border-radius: 0.75rem;
    padding: 0.875rem 1.25rem;
    width: 100%;
    transition: all 0.3s;
    background-color: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(4px);
}

:deep(.form-input:focus) {
    border-color: #B8AAFF;
    box-shadow: 0 0 0 4px rgba(184, 170, 255, 0.25);
    outline: none;
    background-color: rgba(255, 255, 255, 0.95);
}

:deep(.btn-primary) {
    background-color: #B8AAFF;
    border: none;
    color: white;
    padding: 0.875rem 1.75rem;
    border-radius: 0.75rem;
    font-weight: 600;
    transition: all 0.3s;
    box-shadow: 0 4px 6px -1px rgba(184, 170, 255, 0.2), 0 2px 4px -1px rgba(184, 170, 255, 0.1);
}

:deep(.btn-primary:hover) {
    background-color: #9D8AFF;
    transform: translateY(-2px);
    box-shadow: 0 6px 10px -1px rgba(184, 170, 255, 0.3), 0 4px 6px -1px rgba(184, 170, 255, 0.15);
}

:deep(.btn-primary:active) {
    transform: translateY(0);
    box-shadow: 0 2px 4px -1px rgba(184, 170, 255, 0.2);
}

:deep(.form-label) {
    color: #0E1836;
    font-weight: 500;
    margin-bottom: 0.625rem;
    display: block;
    font-size: 0.9375rem;
    letter-spacing: 0.01em;
}

:deep(.form-link) {
    color: #B8AAFF;
    font-weight: 500;
    transition: all 0.2s;
}

:deep(.form-link:hover) {
    color: #7E5BFF;
    text-decoration: underline;
}
</style>