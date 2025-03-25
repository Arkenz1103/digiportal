<script setup>
import MainLayout from '@/Layouts/MainLayout.vue';
import { ref } from 'vue';
import { Head } from '@inertiajs/vue3';

const archivedItems = ref([
    {
        id: 1,
        title: 'Math Assignment 1',
        subject: 'Mathematics',
        date: '2024-02-01',
        type: 'assignment',
        score: '90/100',
        teacher: 'Ms. Johnson',
        description: 'Basic Algebra and Linear Equations'
    },
    {
        id: 2,
        title: 'English Essay',
        subject: 'English',
        date: '2024-01-25',
        type: 'essay',
        score: '95/100',
        teacher: 'Mr. Smith',
        description: 'Analysis of Shakespeare\'s Macbeth'
    },
    {
        id: 3,
        title: 'Science Project',
        subject: 'Science',
        date: '2024-01-15',
        type: 'project',
        score: '88/100',
        teacher: 'Mrs. Davis',
        description: 'Ecosystem and Environmental Studies'
    }
]);

const getTypeIcon = (type) => {
    switch (type) {
        case 'assignment':
            return 'pi-file-edit';
        case 'essay':
            return 'pi-pencil';
        case 'project':
            return 'pi-briefcase';
        default:
            return 'pi-file';
    }
};

const getTypeColor = (type) => {
    switch (type) {
        case 'assignment':
            return {
                bg: 'bg-blue-50',
                text: 'text-blue-600',
                border: 'border-blue-200',
                hover: 'hover:bg-blue-100'
            };
        case 'essay':
            return {
                bg: 'bg-purple-50',
                text: 'text-purple-600',
                border: 'border-purple-200',
                hover: 'hover:bg-purple-100'
            };
        case 'project':
            return {
                bg: 'bg-green-50',
                text: 'text-green-600',
                border: 'border-green-200',
                hover: 'hover:bg-green-100'
            };
        default:
            return {
                bg: 'bg-gray-50',
                text: 'text-gray-600',
                border: 'border-gray-200',
                hover: 'hover:bg-gray-100'
            };
    }
};

const getScoreColor = (score) => {
    const numericScore = parseInt(score.split('/')[0]);
    if (numericScore >= 90) return 'text-green-600 bg-green-50';
    if (numericScore >= 80) return 'text-blue-600 bg-blue-50';
    if (numericScore >= 70) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
};
</script>

<template>
    <Head title="Archived Items" />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-xl shadow-lg p-6">
            <!-- Header Section -->
            <div class="mb-8">
                <div class="flex items-center justify-between">
                    <h1 class="text-2xl font-bold text-gray-900">Archived Items</h1>
                    
                    <!-- Filter Button -->
                    <button class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                        <i class="pi pi-filter mr-2"></i>
                        Filter
                    </button>
                </div>

                <!-- Stats Cards -->
                <div class="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-3">
                    <div class="bg-gray-50 overflow-hidden rounded-lg">
                        <div class="px-4 py-5 sm:p-6">
                            <dt class="text-sm font-medium text-gray-500">Total Items</dt>
                            <dd class="mt-1 text-3xl font-semibold text-gray-900">{{ archivedItems.length }}</dd>
                        </div>
                    </div>
                    <div class="bg-gray-50 overflow-hidden rounded-lg">
                        <div class="px-4 py-5 sm:p-6">
                            <dt class="text-sm font-medium text-gray-500">Average Score</dt>
                            <dd class="mt-1 text-3xl font-semibold text-gray-900">91%</dd>
                        </div>
                    </div>
                    <div class="bg-gray-50 overflow-hidden rounded-lg">
                        <div class="px-4 py-5 sm:p-6">
                            <dt class="text-sm font-medium text-gray-500">Completed Items</dt>
                            <dd class="mt-1 text-3xl font-semibold text-gray-900">15</dd>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Archived Items List -->
            <div class="border border-gray-200 rounded-xl overflow-hidden">
                <div v-for="item in archivedItems" 
                     :key="item.id" 
                     class="border-b border-gray-200 last:border-0">
                    <div class="p-4 hover:bg-gray-50 transition-all duration-200">
                        <div class="flex items-center gap-4">
                            <!-- File Icon -->
                            <div class="w-10 h-10 flex items-center justify-center rounded-lg bg-blue-50 text-blue-600">
                                <i :class="['pi text-xl', getTypeIcon(item.type)]"></i>
                            </div>

                            <!-- Content -->
                            <div class="flex-1 min-w-0">
                                <div class="flex items-start justify-between">
                                    <div>
                                        <h3 class="text-base font-semibold text-gray-900">{{ item.title }}</h3>
                                        <p class="text-sm text-gray-500">{{ item.description }}</p>
                                    </div>
                                    <span class="px-2.5 py-1 rounded-full text-sm font-medium bg-green-50 text-green-700">
                                        {{ item.score }}
                                    </span>
                                </div>
                                
                                <!-- Metadata -->
                                <div class="mt-2 flex items-center gap-4 text-sm text-gray-500">
                                    <span class="flex items-center">
                                        <i class="pi pi-book mr-1.5"></i>
                                        {{ item.subject }}
                                    </span>
                                    <span class="flex items-center">
                                        <i class="pi pi-user mr-1.5"></i>
                                        {{ item.teacher }}
                                    </span>
                                    <span class="flex items-center">
                                        <i class="pi pi-calendar mr-1.5"></i>
                                        {{ new Date(item.date).toLocaleDateString() }}
                                    </span>
                                </div>
                            </div>

                            <!-- Actions -->
                            <div class="flex items-center gap-2">
                                <button class="p-2 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-blue-50">
                                    <i class="pi pi-eye"></i>
                                </button>
                                <button class="p-2 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-blue-50">
                                    <i class="pi pi-download"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Empty State -->
                <div v-if="archivedItems.length === 0" class="py-12 text-center">
                    <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gray-100 mb-4">
                        <i class="pi pi-folder-open text-gray-500 text-xl"></i>
                    </div>
                    <h3 class="text-lg font-medium text-gray-900">No archived items</h3>
                    <p class="mt-1 text-sm text-gray-500">Your completed assignments and projects will appear here</p>
                </div>
            </div>
        </div>
    </div>
</template> 