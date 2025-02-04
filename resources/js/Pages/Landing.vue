<script setup>
import { Head } from '@inertiajs/vue3';
import { ref, onMounted } from 'vue';

defineOptions({ layout: null });

const animateLogo = ref(false);
const animateContent = ref(false);

onMounted(() => {
  setTimeout(() => {
    animateLogo.value = true;
  }, 300);

  setTimeout(() => {
    animateContent.value = true;
  }, 600);
});
</script>

<template>
    <Head title="" />
    <div class="min-h-screen">
        <!-- Header with Animation -->
        <div
          class="bg-[#7386D5] text-white py-4"
          :class="animateLogo ? 'animate__animated animate__fadeInDown' : ''"
        >
            <div class="container mx-auto px-4 flex justify-between items-center">
                <div class="text-2xl font-bold">Naawan Central School</div>
                <a
                  href="/login"
                  class="bg-gray-200 text-gray-800 px-6 py-2 rounded-md hover:bg-gray-300 transition-colors"
                  :class="animateLogo ? 'animate__animated animate__fadeInUp' : ''"
                >
                    Login
                </a>
            </div>
        </div>

        <!-- Main Content with Animation -->
        <main class="container mx-auto flex flex-col md:flex-row items-center justify-center gap-16 px-4 py-16">
            <div
              class="w-64 md:w-96"
              :class="animateLogo ? 'animate__animated animate__fadeInLeft' : ''"
            >
                <img
                    src="https://scontent.fcgy1-3.fna.fbcdn.net/v/t39.30808-6/368255360_324082253303069_319860159441260390_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=XE8ve1NQcMkQ7kNvgG9ojE9&_nc_zt=23&_nc_ht=scontent.fcgy1-3.fna&_nc_gid=AalM_hMnH2zDI7prIRDEmDx&oh=00_AYDiGluYa3x5xbkixP4lVP0Y57VCG-r7u-DTBZyPAf7tCg&oe=67A49874"
                    class="w-full h-auto"
                />
            </div>
            <div
              class="max-w-2xl text-center md:text-left"
              :class="animateContent ? 'animate__animated animate__fadeInUp' : ''"
            >
                <h1 class="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-800 mb-1 leading-tight">
                    "Education is the most powerful weapon which you can use to change the world."
                </h1>
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

.animate__fadeInDown {
    animation-name: fadeInDown;
}

.animate__fadeInUp {
    animation-name: fadeInUp;
}

.animate__fadeInLeft {
    animation-name: fadeInLeft;
}

/* Keyframe Animations */
@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-50px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

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

@keyframes fadeInLeft {
    from {
        opacity: 0;
        transform: translateX(-50px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}
</style>
