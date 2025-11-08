<template>

    <div>
        <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 shadow-lg rounded-t-xl h-40 md:h-36 flex items-center px-6 md:px-8">
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
                        
                        <!-- Loading State -->
                        <div v-if="isLoading" class="flex justify-center items-center py-20">
                            <div class="text-center">
                                <div class="animate-spin rounded-full h-16 w-16 border-4 border-indigo-600 border-t-transparent mx-auto mb-4"></div>
                                <p class="text-gray-600">Loading archived classes...</p>
                            </div>
                        </div>

                        <!-- Empty State -->
                        <div v-else-if="filteredClasses.length === 0" class="text-center py-20">
                            <div class="bg-white rounded-2xl shadow-xl p-12 max-w-md mx-auto border-2 border-indigo-100">
                                <div class="w-20 h-20 bg-gradient-to-br from-indigo-100 to-violet-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                    <i class="pi pi-inbox text-4xl text-indigo-600"></i>
                                </div>
                                <h3 class="text-2xl font-bold text-gray-800 mb-2">No Archived Classes</h3>
                                <p class="text-gray-600">You don't have any archived classes yet</p>
                            </div>
                        </div>

                        <!-- Archived Classes Grid -->
                        <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 md:gap-6">
                            <!-- Archived Class Card -->
                            <div 
                                v-for="classroom in filteredClasses"
                                :key="classroom.id"
                                class="group bg-white rounded-xl shadow-sm border border-indigo-100 overflow-hidden hover:shadow-md transition-all cursor-pointer"
                                @click="showSubjectActivities(classroom)"
                            >
                                <!-- Header with Class Name -->
                                <div class="bg-gradient-to-r from-indigo-600 to-violet-600 p-4">
                                    <h3 class="text-lg font-semibold text-white">{{ classroom.name }}</h3>
                                    <p class="text-xs text-white/90">Archived on {{ formatDate(classroom.archivedDate) }}</p>
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
                                                <p class="font-medium">{{ classroom.studentCount }}</p>
                                            </div>
                                        </div>
                                        <div class="flex items-center space-x-2">
                                            <div class="p-2 rounded-lg bg-violet-50">
                                                <i class="pi pi-folder text-violet-600"></i>
                                            </div>
                                            <div>
                                                <p class="text-xs text-gray-500">Items</p>
                                                <p class="font-medium">{{ classroom.activityCount }}</p>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="flex items-center justify-between text-sm text-gray-500 border-t border-gray-100 pt-3 mt-3">
                                        <div class="flex items-center">
                                            <i class="pi pi-calendar mr-1"></i>
                                            <span>SY {{ classroom.academicYear }}</span>
                                        </div>
                                        <button 
                                            class="text-indigo-600 hover:text-indigo-800 transition-colors"
                                            @click.stop="restoreClass(classroom)"
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
                                    <!-- Create Portfolio button removed - archived classes are view-only -->
                                </div>
                            </div>
                        </template>

                        <!-- Portfolio Folders View -->
                        <div v-if="!showingActivities" class="bg-white/90 rounded-2xl p-6 shadow-sm border border-indigo-100">
                            <!-- Loading State -->
                            <div v-if="isLoading" class="flex justify-center items-center py-12">
                                <div class="text-center">
                                    <div class="animate-spin rounded-full h-12 w-12 border-4 border-indigo-600 border-t-transparent mx-auto mb-3"></div>
                                    <p class="text-gray-600 text-sm">Loading portfolios...</p>
                                </div>
                            </div>

                            <!-- Empty State -->
                            <div v-else-if="portfolioFolders.length === 0" class="text-center py-12">
                                <div class="w-16 h-16 bg-gradient-to-br from-indigo-100 to-violet-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <i class="pi pi-folder-open text-3xl text-indigo-600"></i>
                                </div>
                                <h3 class="text-lg font-bold text-gray-800 mb-2">No Portfolios Found</h3>
                                <p class="text-gray-600 text-sm">This archived class has no portfolio folders</p>
                            </div>

                            <!-- Portfolio Folders Grid -->
                            <div v-else class="space-y-6">
                                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
                                    <!-- Portfolio Folder Card -->
                                    <div 
                                        v-for="folder in portfolioFolders"
                                        :key="folder.id"
                                        class="group bg-white rounded-xl shadow-sm border border-indigo-100 overflow-hidden hover:shadow-lg transition-all cursor-pointer transform hover:-translate-y-1 duration-200"
                                        @click="showActivities(folder)"
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
                                                    {{ folder.name }}
                                                </h3>
                                                <div class="flex items-center space-x-2">
                                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                                                        {{ folder.itemCount }} items
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
                                    <span class="text-2xl font-bold text-[#0E1836]">List of Items - Portfolio {{ selectedFolder?.name }}</span>
                                </div>
                                <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
                                    <!-- Add Item and Track Progress buttons removed - archived classes are view-only -->
                                    <button 
                                        @click="showingActivities = false" 
                                        class="flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200 w-full sm:w-auto"
                                    >
                                        <i class="pi pi-arrow-left"></i>
                                        <span>Back to Folders</span>
                                    </button>
                                </div>
                            </div>

                            <!-- Loading State -->
                            <div v-if="isLoading" class="flex justify-center items-center py-12">
                                <div class="text-center">
                                    <div class="animate-spin rounded-full h-12 w-12 border-4 border-indigo-600 border-t-transparent mx-auto mb-3"></div>
                                    <p class="text-gray-600 text-sm">Loading activities...</p>
                                </div>
                            </div>

                            <!-- Empty State -->
                            <div v-else-if="activities.length === 0" class="bg-white rounded-xl shadow-sm border border-indigo-100 p-12 text-center">
                                <div class="w-16 h-16 bg-gradient-to-br from-indigo-100 to-violet-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <i class="pi pi-list text-3xl text-indigo-600"></i>
                                </div>
                                <h3 class="text-lg font-bold text-gray-800 mb-2">No Activities Found</h3>
                                <p class="text-gray-600 text-sm">This portfolio has no activities</p>
                            </div>

                            <!-- Activities Table -->
                            <div v-else class="bg-white rounded-xl shadow-sm overflow-hidden border border-indigo-100">
                                <!-- Table Header -->
                                <div class="grid grid-cols-12 gap-4 px-6 py-3 bg-indigo-50 border-b border-indigo-100 text-sm font-semibold text-indigo-900">
                                    <div class="col-span-3">Activity Type</div>
                                    <div class="col-span-3">Activity Title</div>
                                    <div class="col-span-5">Description</div>
                                    <div class="col-span-1 text-right">Due Date</div>
                                </div>

                                <!-- Activity Item -->
                                <div v-for="activity in activities" :key="activity.id" 
                                    class="grid grid-cols-12 gap-4 px-6 py-4 hover:bg-[#B8AAFF]/10 border-b border-[#B6CFFF] cursor-pointer transition-colors duration-200">
                                    <div class="col-span-3 text-gray-600 capitalize">{{ activity.type }}</div>
                                    <div class="col-span-3 font-medium text-gray-600">{{ activity.title }}</div>
                                    <div class="col-span-5 text-gray-600">{{ activity.description }}</div>
                                    <div class="col-span-1 text-right text-gray-500">{{ formatDate(activity.date) }}</div>
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
import { ref, computed, onMounted } from 'vue';
import axios from '../../axios';

// Component state
const showingSubject = ref(false);
const showingActivities = ref(false);
const selectedClass = ref(null);
const selectedFolder = ref(null);
const currentFilter = ref('all');
const isLoading = ref(false);

// Data refs
const archivedClasses = ref([]);
const portfolioFolders = ref([]);
const activities = ref([]);

// Load archived classrooms from backend
const loadArchivedClasses = async () => {
    isLoading.value = true;
    try {
        console.log('📚 Loading archived classrooms...');
        const response = await axios.get('/api/classrooms/', {
            params: { archived: true }
        });
        
        if (response.data && response.data.classrooms) {
            archivedClasses.value = response.data.classrooms.map(classroom => ({
                id: classroom.id,
                name: classroom.name,
                academicYear: classroom.academic_year || 'N/A',
                studentCount: classroom.student_count || 0,
                activityCount: classroom.activity_count || 0,
                archivedDate: classroom.archived_at || classroom.created_at
            }));
            console.log('✅ Loaded archived classes:', archivedClasses.value.length);
        }
    } catch (error) {
        console.error('❌ Error loading archived classes:', error);
        archivedClasses.value = [];
    } finally {
        isLoading.value = false;
    }
};

// Load portfolio folders for selected archived class
const loadPortfolioFolders = async (classId) => {
    isLoading.value = true;
    try {
        console.log('📁 Loading portfolio folders for class:', classId);
        const response = await axios.get('/api/portfolio-folders/', {
            params: { classroom_id: classId }
        });
        
        if (response.data && Array.isArray(response.data)) {
            portfolioFolders.value = response.data.map(folder => ({
                id: folder.id,
                name: folder.name,
                itemCount: folder.activity_count || 0,
                description: folder.description || ''
            }));
            console.log('✅ Loaded portfolio folders:', portfolioFolders.value.length);
        }
    } catch (error) {
        console.error('❌ Error loading portfolio folders:', error);
        portfolioFolders.value = [];
    } finally {
        isLoading.value = false;
    }
};

// Load activities for selected portfolio folder
const loadActivities = async (folderId) => {
    isLoading.value = true;
    try {
        console.log('📋 Loading activities for folder:', folderId);
        const response = await axios.get(`/api/portfolio-folders/${folderId}/activities/`);
        
        if (response.data && Array.isArray(response.data)) {
            activities.value = response.data.map(activity => ({
                id: activity.id,
                type: activity.activity_type || 'activity',
                title: activity.title,
                description: activity.description || 'No description',
                date: activity.due_date || activity.created_at,
                dueTime: activity.due_time || ''
            }));
            console.log('✅ Loaded activities:', activities.value.length);
        }
    } catch (error) {
        console.error('❌ Error loading activities:', error);
        activities.value = [];
    } finally {
        isLoading.value = false;
    }
};

// Show portfolio folders for selected class
const showSubjectActivities = async (classroom) => {
    console.log('🔍 Viewing class:', classroom.name);
    selectedClass.value = classroom;
    showingSubject.value = true;
    await loadPortfolioFolders(classroom.id);
};

// Show activities for selected portfolio folder
const showActivities = async (folder) => {
    console.log('🔍 Viewing folder:', folder.name);
    selectedFolder.value = folder;
    showingActivities.value = true;
    await loadActivities(folder.id);
};

// Go back to archived classes list
const goBack = () => {
    showingSubject.value = false;
    showingActivities.value = false;
    selectedClass.value = null;
    selectedFolder.value = null;
    portfolioFolders.value = [];
    activities.value = [];
};

// Restore archived class
const restoreClass = async (classroom) => {
    if (confirm(`Are you sure you want to restore "${classroom.name}"?`)) {
        try {
            console.log('🔄 Restoring class:', classroom.name);
            await axios.put(`/api/classrooms/${classroom.id}/`, {
                is_archived: false
            });
            alert('Class restored successfully!');
            // Reload archived classes
            await loadArchivedClasses();
        } catch (error) {
            console.error('❌ Error restoring class:', error);
            alert('Failed to restore class. Please try again.');
        }
    }
};

// Load archived classes on mount
onMounted(() => {
    loadArchivedClasses();
});

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