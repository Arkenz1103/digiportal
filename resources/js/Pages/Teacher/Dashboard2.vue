<template>
    <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-800">Welcome back, {{ user?.name }}!</h1>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- My Classes -->
        <div class="bg-blue-100 rounded-lg p-6 shadow-sm">
            <div class="flex items-center justify-between">
                <div>
                    <h3 class="text-xl font-semibold text-gray-800">My Classes</h3>
                    <p class="mt-2 text-gray-600">View and manage your assigned classes</p>
                </div>
                <div class="bg-blue-200 p-3 rounded-full">
                    <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                </div>
            </div>
        </div>

        <!-- Students -->
        <div class="bg-green-100 rounded-lg p-6 shadow-sm">
            <div class="flex items-center justify-between">
                <div>
                    <h3 class="text-xl font-semibold text-gray-800">Students</h3>
                    <p class="mt-2 text-gray-600">View and manage your students</p>
                </div>
                <div class="bg-green-200 p-3 rounded-full">
                    <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import MainLayout from '../../Layouts/MainLayout.vue';

defineProps({
    user: {
        type: Object,
        required: true
    }
});
</script>
