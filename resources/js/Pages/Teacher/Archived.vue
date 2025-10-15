<template>

    <div>
        <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-6 md:p-4 shadow-lg rounded-b-3xl">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div class="space-y-3">
                    <h1 class="text-xl md:text-2xl font-bold text-white px-4 py-2 md:px-6 md:py-3 rounded-lg inline-block bg-white/20">
                        Archived Classes
                    </h1>
                    <p class="text-white/90 ml-2 flex items-center gap-2">
                        <i class="pi pi-user"></i>
                        Teacher
                    </p>
                </div>
            </div>
        </div>

        <div class="p-4 md:p-6">
            <div class="rounded-2xl shadow-lg bg-white/90 backdrop-blur-sm border border-indigo-100 p-6">
                <!-- Archived Classes Grid -->
                <div class="space-y-6">
                    <div v-if="!showingSubject">
                        <!-- Filter -->
                        <div class="flex items-center gap-2 mb-6">
                            <button 
                                v-for="period in ['All', 'Current Year', 'Last Year']" 
                                :key="period"
                                @click="currentFilter = period.toLowerCase()"
                                :class="[
                                    'px-3 py-1.5 rounded-lg text-sm transition-colors',
                                    currentFilter === period.toLowerCase()
                                        ? 'bg-indigo-600 text-white'
                                        : 'text-gray-700 hover:bg-indigo-100'
                                ]"
                            >
                                {{ period }}
                            </button>
                        </div>
                        
                        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 md:gap-6">
                            <!-- Grade 1 - A Card -->
                            <div 
                                class="group bg-white rounded-xl shadow-sm border border-indigo-100 overflow-hidden hover:shadow-md transition-all cursor-pointer"
                                @click="showSubjectActivities('Grade 1 - A')"
                            >
                            <!-- Header with Class Name -->
                            <div class="bg-gradient-to-r from-indigo-600 to-violet-600 p-4">
                                <h3 class="text-lg font-semibold text-white">Grade 1 - A</h3>
                                <p class="text-xs text-white/90">Archived on May 30, 2025</p>
                            </div>
                            
                            <!-- Class Details -->
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-3">
                                    <div class="flex items-center space-x-2">
                                        <div class="p-2 rounded-lg bg-indigo-50">
                                            <i class="pi pi-users text-indigo-600"></i>
                                        </div>
                                        <div>
                                            <p class="text-xs text-gray-500">Students</p>
                                            <p class="font-medium">25</p>
                                        </div>
                                    </div>
                                    <div class="flex items-center space-x-2">
                                        <div class="p-2 rounded-lg bg-violet-50">
                                            <i class="pi pi-folder text-violet-600"></i>
                                        </div>
                                        <div>
                                            <p class="text-xs text-gray-500">Items</p>
                                            <p class="font-medium">5</p>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="flex items-center justify-between text-sm text-gray-500 border-t border-gray-100 pt-3 mt-3">
                                    <div class="flex items-center">
                                        <i class="pi pi-calendar mr-1"></i>
                                        <span>SY 2024-2025</span>
                                    </div>
                                    <button 
                                        class="text-indigo-600 hover:text-indigo-800 transition-colors"
                                        @click.stop="restoreClass({name: 'Grade 1 - A'})"
                                    >
                                        <i class="pi pi-undo mr-1"></i>
                                        Restore
                                    </button>
                                </div>
                            </div>
                        </div>
                        </div>
                    </div>

                    <!-- Subject View -->
                    <div v-else class="space-y-6">
                        <!-- Header with Title and Actions -->
                        <template v-if="!showingActivities">
                            <div class="flex items-center justify-between mb-6">
                                <h3 class="text-lg font-semibold text-[#0E1836]">Pupils Portfolio</h3>
                                <div class="flex items-center gap-3">
                                    <button 
                                        @click="goBack"
                                        class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                                    >
                                        <i class="pi pi-arrow-left"></i>
                                        <span class="font-medium">Back to Classes</span>
                                    </button>
                                    <button 
                                        @click="createNewFolder"
                                        class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                                    >
                                        <i class="pi pi-plus"></i>
                                        <span>Create Portfolio</span>
                                    </button>
                                </div>
                            </div>
                        </template>

                        <!-- Portfolio Folders View -->
                        <div v-if="!showingActivities" class="bg-white/90 rounded-2xl p-6 shadow-sm border border-indigo-100">
                            <div class="space-y-6">
                                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
                                    <!-- MAPEH Portfolio Folder -->
                                    <div 
                                        class="group bg-white rounded-xl shadow-sm border border-indigo-100 overflow-hidden hover:shadow-lg transition-all cursor-pointer transform hover:-translate-y-1 duration-200"
                                        @click="showActivities('Mapeh')"
                                    >
                                        <!-- Folder Preview -->
                                        <div class="relative h-36 mb-4 p-4 md:p-6">
                                            <!-- Stacked Preview Images with Dynamic Animation -->
                                            <div class="absolute top-5 right-5 w-28 h-32 flex items-center justify-center">
                                                <div class="absolute w-24 h-28 rounded-lg transform rotate-[-15deg] transition-all duration-300 group-hover:rotate-[-20deg] group-hover:scale-105 bg-gradient-to-br from-indigo-500 to-violet-600"></div>
                                                <div class="absolute w-24 h-28 rounded-lg transform rotate-[-5deg] transition-all duration-300 group-hover:rotate-[-10deg] group-hover:scale-105 bg-gradient-to-br from-indigo-400 to-violet-500"></div>
                                                <div class="absolute w-24 h-28 rounded-lg transform rotate-[5deg] transition-all duration-300 group-hover:rotate-[10deg] group-hover:scale-105 bg-gradient-to-br from-indigo-300 to-violet-400"></div>
                                            </div>
                                            <!-- Folder Title -->
                                            <div class="relative z-10">
                                                <h3 class="text-xl md:text-2xl font-bold mb-1 text-indigo-900 group-hover:text-indigo-600 transition-colors">
                                                    Mapeh
                                                </h3>
                                                <div class="flex items-center space-x-2">
                                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                                                        4 items
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                        
                                        <!-- Interactive Footer -->
                                        <div class="mt-4 pt-4 border-t border-indigo-100 flex justify-between items-center p-4 md:p-6">
                                            <div class="flex items-center space-x-2 text-sm text-indigo-600">
                                                <i class="pi pi-folder text-indigo-600"></i>
                                                <span>View Contents</span>
                                            </div>
                                            <i class="pi pi-arrow-right text-indigo-600 transform group-hover:translate-x-1 transition-transform"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Activities List View -->
                        <div v-else class="space-y-6">
                            <!-- Back button and List Header -->
                            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                                <div class="rounded-lg py-2 px-4">
                                    <span class="text-2xl font-bold text-[#0E1836]">List of Items - {{ selectedSubject }}</span>
                                </div>
                                <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
                                    <button 
                                        class="flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200 w-full sm:w-auto"
                                    >
                                        <i class="pi pi-plus"></i>
                                        <span>Add Item</span>
                                    </button>
                                    <button 
                                        class="flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200 w-full sm:w-auto"
                                    >
                                        <i class="pi pi-chart-line"></i>
                                        <span>Track Progress</span>
                                    </button>
                                    <button 
                                        @click="showingActivities = false" 
                                        class="flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200 w-full sm:w-auto"
                                    >
                                        <i class="pi pi-arrow-left"></i>
                                        <span>Back to Folders</span>
                                    </button>
                                </div>
                            </div>

                            <!-- Activities Table -->
                            <div class="bg-white rounded-xl shadow-sm overflow-hidden border border-indigo-100">
                                <!-- Table Header -->
                                <div class="grid grid-cols-12 gap-4 px-6 py-3 bg-indigo-50 border-b border-indigo-100 text-sm font-semibold text-indigo-900">
                                    <div class="col-span-3">Activity Type</div>
                                    <div class="col-span-3">Activity Title</div>
                                    <div class="col-span-5">Description</div>
                                    <div class="col-span-1 text-right">Due Date</div>
                                </div>

                                <!-- Activity Item -->
                                <div v-for="(activity, index) in activities" :key="index" 
                                    class="grid grid-cols-12 gap-4 px-6 py-4 hover:bg-[#B8AAFF]/10 border-b border-[#B6CFFF] cursor-pointer transition-colors duration-200">
                                    <div class="col-span-3 text-gray-600">{{ activity.type }}</div>
                                    <div class="col-span-3 font-medium text-gray-600">{{ activity.title }}</div>
                                    <div class="col-span-5 text-gray-600">{{ activity.description }}</div>
                                    <div class="col-span-1 text-right text-gray-500">{{ activity.date }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Component state
const showingSubject = ref(false);
const showingActivities = ref(false);
const selectedSubject = ref('Sample Class');
const currentFilter = ref('all');

// Activities data
const activities = ref([
    {
        type: 'project',
        title: 'Self-portrait',
        description: 'Artworks: Create a self-portrait using mixed media techniques',
        date: 'Nov 6, 2024'
    }
]);

// Sample archived class data
const archivedClasses = ref([
    {
        id: 1,
        name: 'Sample Class',
        academicYear: '2024-2025',
        studentCount: 25,
        activityCount: 5,
        archivedDate: '2023-12-19'
    }
]);

// Methods
const showSubjectActivities = (subject) => {
    selectedSubject.value = subject;
    showingSubject.value = true;
};

const showActivities = (subject) => {
    selectedSubject.value = `Portfolio ${subject}`;
    showingActivities.value = true;
};

const goBack = () => {
    showingSubject.value = false;
};

const viewClass = (class_) => {
    console.log('Viewing class:', class_.name);
};

const restoreClass = (class_) => {
    if (confirm('Are you sure you want to restore this class?')) {
        console.log('Restoring class:', class_.name);
        // Add your restore logic here
    }
};

// Computed properties
const filteredClasses = computed(() => {
    if (currentFilter.value === 'all') return archivedClasses.value;
    const currentYear = new Date().getFullYear();
    
    return archivedClasses.value.filter(class_ => {
        if (!class_ || !class_.academicYear) return false;
        
        try {
            const classYear = parseInt(class_.academicYear.split('-')[0]);
            if (isNaN(classYear)) return false;
            
            if (currentFilter.value === 'current year') {
                return classYear === currentYear;
            }
            if (currentFilter.value === 'last year') {
                return classYear === currentYear - 1;
            }
            return true;
        } catch (error) {
            console.error('Error filtering classes:', error);
            return false;
        }
    });
});

// Format date helper
const formatDate = (dateString) => {
    try {
        if (!dateString) return '';
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return '';
        
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    } catch (error) {
        console.error('Error formatting date:', error);
        return '';
    }
};

</script>

<style scoped>
/* Add theme variables */
:root {
    --theme-purple: #B8AAFF;
    --theme-blue: #B6CFFF;
    --theme-light: #F2FDFF;
    --theme-accent: #7BBBFE;
    --theme-dark: #0E1836;
}

/* Add these styles for smooth transitions */
.bg-gradient-to-br {
    transition: all 0.3s ease;
}

/* Add this new style for better responsive layout */
@media (max-width: 1024px) {
    .lg\:w-64 {
        width: 100%;
    }
}
</style>