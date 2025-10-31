<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        <!-- Header -->
        <div class="bg-white shadow-sm border-b border-gray-200">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                <div class="flex items-center justify-between">
                    <h1 class="text-2xl font-bold text-gray-900">My Classroom</h1>
                    <div class="flex items-center gap-2">
                        <span class="text-sm text-gray-500">School Year:</span>
                        <span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium">
                            2024-2025
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Loading State -->
            <div v-if="isLoading" class="flex justify-center items-center py-20">
                <div class="text-center">
                    <div class="animate-spin rounded-full h-16 w-16 border-4 border-indigo-600 border-t-transparent mx-auto mb-4"></div>
                    <p class="text-gray-600">Loading classroom data...</p>
                </div>
            </div>

            <!-- No Classroom Assigned -->
            <div v-else-if="!classroom" class="text-center py-20">
                <div class="bg-white rounded-2xl shadow-xl p-12 max-w-md mx-auto">
                    <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <i class="pi pi-building text-4xl text-gray-400"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-800 mb-2">No Classroom Assigned</h3>
                    <p class="text-gray-600">You haven't been assigned to any classroom yet.</p>
                    <p class="text-sm text-gray-500 mt-2">Please contact your teacher for classroom assignment.</p>
                </div>
            </div>

            <!-- Classroom Info -->
            <div v-else>
                <!-- Classroom Card -->
                <div class="bg-white rounded-xl shadow-lg overflow-hidden mb-6">
                    <!-- Header with gradient -->
                    <div class="bg-gradient-to-r from-indigo-500 to-purple-600 p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <h2 class="text-3xl font-bold text-white">{{ classroom.name }}</h2>
                                <p class="text-indigo-100 mt-1">{{ classroom.room_number }}</p>
                            </div>
                            <div class="text-right">
                                <div class="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center">
                                    <i class="pi pi-users text-3xl text-white"></i>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Classroom Info Grid -->
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 p-6 bg-gray-50">
                        <div class="text-center">
                            <p class="text-2xl font-bold text-gray-900">Grade {{ classroom.grade_level }}</p>
                            <p class="text-sm text-gray-600">Grade Level</p>
                        </div>
                        <div class="text-center">
                            <p class="text-2xl font-bold text-gray-900">{{ classroom.section }}</p>
                            <p class="text-sm text-gray-600">Section</p>
                        </div>
                        <div class="text-center">
                            <p class="text-2xl font-bold text-gray-900">{{ classroom.student_count }}</p>
                            <p class="text-sm text-gray-600">Classmates</p>
                        </div>
                        <div class="text-center">
                            <p class="text-2xl font-bold text-gray-900">{{ classroom.room_number.replace('Room ', '') }}</p>
                            <p class="text-sm text-gray-600">Room</p>
                        </div>
                    </div>

                    <!-- Teacher Info -->
                    <div v-if="classroom.teacher" class="p-6 border-t border-gray-200">
                        <h3 class="text-lg font-semibold text-gray-900 mb-4">Class Teacher</h3>
                        <div class="flex items-center gap-4 p-4 bg-indigo-50 rounded-lg">
                            <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl">
                                {{ getInitials(classroom.teacher.name) }}
                            </div>
                            <div>
                                <p class="font-semibold text-gray-900 text-lg">{{ classroom.teacher.name }}</p>
                                <p class="text-sm text-gray-600">{{ classroom.teacher.email }}</p>
                                <p v-if="classroom.teacher.department" class="text-sm text-indigo-600 mt-1">
                                    <i class="pi pi-briefcase mr-1"></i>
                                    {{ classroom.teacher.department }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Classmates Section -->
                <div class="bg-white rounded-xl shadow-lg p-6">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-xl font-bold text-gray-900">My Classmates</h3>
                        <span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium">
                            {{ classroom.students.length }} Students
                        </span>
                    </div>

                    <!-- Search Bar -->
                    <div class="mb-6">
                        <div class="relative">
                            <i class="pi pi-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
                            <input v-model="searchQuery" type="text" 
                                placeholder="Search classmates..."
                                class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
                        </div>
                    </div>

                    <!-- Classmates Grid -->
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        <div v-for="student in filteredStudents" :key="student.id"
                            class="flex items-center gap-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                            <div class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                                {{ getInitials(student.name) }}
                            </div>
                            <div class="flex-1">
                                <p class="font-medium text-gray-900">{{ student.name }}</p>
                                <p class="text-xs text-gray-500">{{ student.id_number }}</p>
                            </div>
                            <button v-if="student.id !== currentUserId" @click="viewClassmate(student)"
                                class="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors">
                                <i class="pi pi-user"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Empty State -->
                    <div v-if="filteredStudents.length === 0" class="text-center py-8">
                        <i class="pi pi-search text-4xl text-gray-300 mb-3"></i>
                        <p class="text-gray-500">No classmates found matching "{{ searchQuery }}"</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Classmate Detail Modal -->
        <div v-if="selectedClassmate" @click="selectedClassmate = null"
            class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
            <div @click.stop class="bg-white rounded-xl shadow-2xl max-w-md w-full p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-xl font-bold text-gray-900">Classmate Profile</h3>
                    <button @click="selectedClassmate = null" class="text-gray-400 hover:text-gray-600">
                        <i class="pi pi-times text-xl"></i>
                    </button>
                </div>
                
                <div class="text-center mb-6">
                    <div class="w-24 h-24 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-2xl mx-auto mb-3">
                        {{ getInitials(selectedClassmate.name) }}
                    </div>
                    <h4 class="text-lg font-semibold text-gray-900">{{ selectedClassmate.name }}</h4>
                    <p class="text-sm text-gray-500">{{ selectedClassmate.id_number }}</p>
                </div>

                <div class="space-y-3">
                    <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <i class="pi pi-envelope text-indigo-600"></i>
                        <div>
                            <p class="text-xs text-gray-500">Email</p>
                            <p class="text-sm font-medium text-gray-900">{{ selectedClassmate.email }}</p>
                        </div>
                    </div>
                </div>

                <button @click="selectedClassmate = null"
                    class="w-full mt-6 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium">
                    Close
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const isLoading = ref(false);
const classroom = ref(null);
const searchQuery = ref('');
const selectedClassmate = ref(null);
const currentUserId = ref(null);

// Get current user ID from localStorage
onMounted(() => {
    currentUserId.value = parseInt(localStorage.getItem('digiportal_user_id'));
    loadClassroom();
});

// Load classroom data
const loadClassroom = async () => {
    isLoading.value = true;
    try {
        const response = await axios.get('/api/classrooms/');
        if (response.data && response.data.classrooms && response.data.classrooms.length > 0) {
            classroom.value = response.data.classrooms[0]; // Students should only have one classroom
            console.log('Loaded classroom:', classroom.value);
        } else {
            classroom.value = null;
        }
    } catch (error) {
        console.error('Error loading classroom:', error);
        classroom.value = null;
    } finally {
        isLoading.value = false;
    }
};

// Filter students based on search query
const filteredStudents = computed(() => {
    if (!classroom.value || !classroom.value.students) return [];
    
    if (!searchQuery.value) {
        return classroom.value.students;
    }
    
    const query = searchQuery.value.toLowerCase();
    return classroom.value.students.filter(student => 
        student.name.toLowerCase().includes(query) ||
        (student.id_number && student.id_number.toLowerCase().includes(query))
    );
});

// Get initials from name
const getInitials = (name) => {
    if (!name) return '?';
    const parts = name.split(' ');
    if (parts.length >= 2) {
        return parts[0][0] + parts[parts.length - 1][0];
    }
    return name.substring(0, 2).toUpperCase();
};

// View classmate details
const viewClassmate = (student) => {
    selectedClassmate.value = student;
};
</script>

<style scoped>
/* Smooth transitions */
* {
    transition: all 0.2s ease;
}

/* Hover effects */
.hover\:bg-gray-100:hover {
    transform: translateY(-1px);
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #f3f4f6;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: #9ca3af;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #6b7280;
}
</style>
