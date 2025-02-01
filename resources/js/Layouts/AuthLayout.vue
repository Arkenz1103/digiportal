<template>
    <div class="relative min-h-screen bg-[#7386D5] p-6">

        <!-- Background Animation (Subtle) -->
        <div class="absolute inset-0 bg-[#7386D5] opacity-50 animate-pulse"></div>

        <div class="flex min-h-screen relative z-10">
            <!-- Left side with back button -->
            <div class="w-16 p-4 z-20 relative">
                <Link href="/" class="text-white hover:text-gray-800">
                    <i class="pi pi-arrow-left text-xl"></i>
                </Link>
            </div>

            <!-- Main content -->
            <div class="flex-1 flex items-center justify-center gap-24 px-4">
                <!-- School Logo with Animation -->
                <div class="order-first animate__animated animate__fadeIn animate__delay-1s">
                    <img
                        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlC4Z2-qQHdn_TKc6z-SJGsVH1_hJB4iu4DA&s"
                        alt="Naawan Central School Logo"
                        class="h-50 w-60 mr-3 rounded-full"
                    />
                </div>

                <!-- Login Content with Animation -->
                <div class="w-full max-w-md">
                    <!-- Welcome Text with a Bouncy Animation -->
                    <h1 class="text-2xl font-bold mb-8 text-white text-center animate__animated animate__bounceIn">
                        Welcome to EduBoard!
                    </h1>

                    <!-- Slot for page content -->
                    <slot />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Link } from '@inertiajs/vue3';
</script>

<style scoped>
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
