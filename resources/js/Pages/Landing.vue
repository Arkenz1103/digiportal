<script setup>
import { Head } from '@inertiajs/vue3';
import { ref, onMounted } from 'vue';

defineOptions({ layout: null });

const animateLogo = ref(false);

onMounted(() => {
  setTimeout(() => {
    animateLogo.value = true;
  }, 300);
});
</script>

<template>
    <Head title="" />
    <div class="min-h-screen">
        <!-- Header -->
        <div class="bg-[#7386D5] text-white py-4">
            <div class="container mx-auto px-4 flex justify-between items-center">
                <div class="text-2xl font-bold">Naawan Central School</div>
                <a
                  href="/login"
                  class="bg-gray-200 text-gray-800 px-6 py-2 rounded-md hover:bg-gray-300 transition-colors"
                >
                    Login
                </a>
            </div>
        </div>

        <!-- Main Content -->
        <main class="container mx-auto flex flex-col md:flex-row items-center justify-center gap-16 px-4 py-16">
            <div class="max-w-2xl text-center md:text-left">
                <h1 
  class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-500 mb-4 leading-snug text-center md:text-left"
  :class="animateLogo ? 'animate__animated animate__fadeInUp' : ''"
>
  "Turn Your Progress into a Story Worth Sharing with DigiPort."
</h1>

            </div>
            <div class="w-64 md:w-96">
                <img
                    src="C:\Users\ncslogo.jpg"
                    class="w-full h-auto"
                />
            </div>
        </main>
    </div>
</template>

<style scoped>
/* Importing Animate.css library for animations */
@import 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css';

/* Custom animation adjustments */
.animate__animated {
    animation-duration: 1s;
    animation-timing-function: ease-out;
}

.animate__fadeInUp {
    animation-name: fadeInUp;
}

/* Keyframe Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(50px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>