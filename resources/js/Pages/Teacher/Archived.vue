<template>
    <Head title="Archived Classes" />

    <div class="max-w-7xl mx-auto p-6">
        <div class="bg-white rounded-xl shadow-lg p-6">
            <div class="mb-6">
                <h1 class="text-2xl font-bold text-gray-900">Archived Classes</h1>
            </div>

            <!-- Archived Classes Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="class_ in archivedClasses" 
                    :key="class_.id" 
                    class="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
                >
                    <div class="p-6">
                        <!-- Class Header -->
                        <div class="flex items-start justify-between mb-4">
                            <div>
                                <h3 class="text-lg font-semibold text-gray-900">{{ class_.name }}</h3>
                                <p class="text-sm text-gray-500">{{ class_.academicYear }}</p>
                            </div>
                            <div :class="`w-2 h-2 rounded-full bg-${class_.theme}-500`"></div>
                        </div>

                        <!-- Class Stats -->
                        <div class="grid grid-cols-2 gap-4 mb-4">
                            <div class="bg-gray-50 p-3 rounded-lg">
                                <p class="text-sm text-gray-600">Students</p>
                                <p class="text-lg font-semibold text-gray-900">{{ class_.studentCount }}</p>
                            </div>
                            <div class="bg-gray-50 p-3 rounded-lg">
                                <p class="text-sm text-gray-600">Activities</p>
                                <p class="text-lg font-semibold text-gray-900">{{ class_.activityCount }}</p>
                            </div>
                        </div>

                        <!-- Archive Date -->
                        <div class="text-sm text-gray-500 mb-4">
                            Archived on {{ formatDate(class_.archivedDate) }}
                        </div>

                        <!-- Actions -->
                        <div class="flex gap-2">
                            <button 
                                @click="viewClass(class_)"
                                class="flex-1 px-3 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                            >
                                View Details
                            </button>
                            <button 
                                @click="restoreClass(class_)"
                                class="flex-1 px-3 py-2 text-sm text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                            >
                                Restore
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-if="archivedClasses.length === 0" 
                class="text-center py-12"
            >
                <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gray-100 mb-4">
                    <i class="pi pi-folder-open text-gray-500 text-xl"></i>
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-2">No Archived Classes</h3>
                <p class="text-gray-500">Classes that you archive will appear here</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { Head } from '@inertiajs/vue3';

// Sample archived classes data
const archivedClasses = ref([
    {
        id: 1,
        name: 'Grade 1 - A',
        theme: 'emerald',
        academicYear: '2022-2023',
        studentCount: 25,
        activityCount: 48,
        archivedDate: '2023-12-20'
    },
    {
        id: 2,
        name: 'Grade 2 - B',
        theme: 'blue',
        academicYear: '2022-2023',
        studentCount: 28,
        activityCount: 52,
        archivedDate: '2023-12-21'
    },
    {
        id: 3,
        name: 'Grade 3 - A',
        theme: 'purple',
        academicYear: '2022-2023',
        studentCount: 30,
        activityCount: 45,
        archivedDate: '2023-12-19'
    }
]);

// Format date helper
const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

// View class details
const viewClass = (class_) => {
    // Implement view functionality
    console.log('Viewing class:', class_.name);
};

// Restore class
const restoreClass = (class_) => {
    // Implement restore functionality
    console.log('Restoring class:', class_.name);
};
</script>

<style scoped>
/* Add any component-specific styles here */
</style> 