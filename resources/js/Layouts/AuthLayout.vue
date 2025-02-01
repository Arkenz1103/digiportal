<template>
    <div class="flex min-h-screen">
        <!-- Left side with back button -->
        <div class="w-16 p-4">
            <Link href="/" class="text-gray-600 hover:text-gray-800">
                <i class="pi pi-arrow-left text-xl"></i>
            </Link>
        </div>

        <!-- Main content -->
        <div class="flex-1 flex items-center justify-center gap-24 px-4">
            <!-- School Logo -->
            <div class="order-first">
                <img
                    src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlC4Z2-qQHdn_TKc6z-SJGsVH1_hJB4iu4DA&s"
                    alt="Naawan Central School Logo"
                    class="h-50 w-60 mr-3 rounded-full"
                />
            </div>

            <!-- Login Content -->
            <div class="w-full max-w-md">
                <!-- Welcome Text -->
                <h1 class="text-2xl font-bold mb-8 text-[#1B2850] text-center">Welcome to EduBoard!</h1>

                <!-- Slot for page content -->
                <slot />
            </div>
        </div>
    </div>
</template>

<script setup>
import { Link } from '@inertiajs/vue3';
</script>
