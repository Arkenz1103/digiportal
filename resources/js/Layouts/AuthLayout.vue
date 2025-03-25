<template>
    <div class="relative h-screen bg-[#7386D5] p-6 overflow-hidden">

        <!-- Background Animation (Subtle) -->
        <div class="absolute inset-0 bg-[#7386D5] opacity-50 animate-pulse"></div>

        <div class="flex h-full relative z-10">
            <!-- Left side with back button -->
            <div class="w-16 p-4 z-20 relative">
                <Link href="/" class="text-white hover:text-gray-800">
                    <i class="pi pi-arrow-left text-xl"></i>
                </Link>
            </div>

            <!-- Main content -->
            <div class="flex-1 flex items-center justify-center gap-64 px-4">
                <!-- Login Content -->
                <div class="w-full max-w-lg">
                    <slot />
                </div>

                <!-- School Logo on the Right (Bigger, No Animation) -->
                <div class="order-last">
                    <img
                       src="C:\Users\ncslogo.jpg"
                    class="w-full h-auto"
                    />
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { Link } from '@inertiajs/vue3';
</script>

<style scoped>
/* Prevent scrolling */
html, body {
    height: 100%;
    margin: 0;
    overflow: hidden;
}

/* Importing Animate.css library for animations */
@import 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css';

/* Custom gradient background animation */
.animate__animated {
    animation-duration: 1s;
    animation-timing-function: ease-out;
}

.animate__fadeIn {
    animation-name: fadeIn;
}

.animate__bounceIn {
    animation-name: bounceIn;
}

/* Keyframe Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes bounceIn {
    from {
        transform: scale(0);
        opacity: 0;
    }
    50% {
        transform: scale(1.1);
    }
    100% {
        transform: scale(1);
        opacity: 1;
    }
}
</style>
