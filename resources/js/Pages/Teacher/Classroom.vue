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
            <div v-else-if="classrooms.length === 0" class="text-center py-20">
                <div class="bg-white rounded-2xl shadow-xl p-12 max-w-md mx-auto">
                    <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <i class="pi pi-building text-4xl text-gray-400"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-800 mb-2">No Classroom Assigned</h3>
                    <p class="text-gray-600">You haven't been assigned to any classroom yet.</p>
                </div>
            </div>

            <!-- Classroom Cards -->
            <div v-else class="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
                <div v-for="classroom in classrooms" :key="classroom.id" 
                    class="bg-white rounded-xl shadow-lg overflow-hidden">
                    
                    <!-- Classroom Header -->
                    <div class="bg-gradient-to-r from-indigo-500 to-purple-600 p-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <h2 class="text-2xl font-bold text-white">{{ classroom.name }}</h2>
                                <p class="text-indigo-100 mt-1">{{ classroom.room_number }}</p>
                            </div>
                            <div class="text-right">
                                <p class="text-white text-3xl font-bold">{{ classroom.student_count }}</p>
                                <p class="text-indigo-100 text-sm">Students</p>
                            </div>
                        </div>
                        <div class="mt-4 flex items-center gap-4">
                            <span class="px-3 py-1 bg-white/20 backdrop-blur-sm text-white rounded-full text-sm">
                                <i class="pi pi-users mr-1"></i>
                                Capacity: {{ classroom.student_count }}/{{ classroom.capacity }}
                            </span>
                            <span v-if="classroom.is_full" class="px-3 py-1 bg-red-500 text-white rounded-full text-sm">
                                <i class="pi pi-exclamation-circle mr-1"></i>
                                Full
                            </span>
                        </div>
                    </div>

                    <!-- Quick Stats -->
                    <div class="grid grid-cols-3 divide-x divide-gray-200 bg-gray-50">
                        <div class="p-4 text-center">
                            <p class="text-2xl font-bold text-gray-900">{{ classroom.grade_level }}</p>
                            <p class="text-sm text-gray-600">Grade Level</p>
                        </div>
                        <div class="p-4 text-center">
                            <p class="text-2xl font-bold text-gray-900">{{ classroom.section }}</p>
                            <p class="text-sm text-gray-600">Section</p>
                        </div>
                        <div class="p-4 text-center">
                            <p class="text-2xl font-bold text-gray-900">{{ getAttendanceRate(classroom) }}%</p>
                            <p class="text-sm text-gray-600">Attendance</p>
                        </div>
                    </div>

                    <!-- Students List -->
                    <div class="p-6">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-semibold text-gray-900">Students</h3>
                            <button @click="toggleStudentList(classroom)"
                                class="text-indigo-600 hover:text-indigo-700 text-sm font-medium">
                                {{ classroom.showStudents ? 'Hide' : 'Show All' }}
                                <i class="pi ml-1" :class="classroom.showStudents ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
                            </button>
                        </div>

                        <!-- Student Grid -->
                        <div v-if="classroom.showStudents" class="space-y-3 max-h-96 overflow-y-auto">
                            <div v-for="(student, index) in classroom.students" :key="student.id"
                                class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                                <span class="text-sm text-gray-500 font-medium w-8">{{ index + 1 }}.</span>
                                <div class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                                    {{ getInitials(student.name) }}
                                </div>
                                <div class="flex-1">
                                    <p class="font-medium text-gray-900">{{ student.name }}</p>
                                    <p class="text-xs text-gray-500">{{ student.id_number }}</p>
                                </div>
                                <button @click="viewStudent(student)"
                                    class="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors">
                                    <i class="pi pi-eye"></i>
                                </button>
                            </div>
                        </div>

                        <!-- Preview when collapsed -->
                        <div v-else class="flex -space-x-2">
                            <div v-for="(student, index) in classroom.students.slice(0, 5)" :key="student.id"
                                class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold border-2 border-white">
                                {{ getInitials(student.name) }}
                            </div>
                            <div v-if="classroom.students.length > 5"
                                class="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-600 font-bold border-2 border-white">
                                +{{ classroom.students.length - 5 }}
                            </div>
                        </div>
                    </div>

                    <!-- Actions -->
                    <div class="px-6 pb-6 flex gap-3">
                        <button @click="viewClassroomDetails(classroom)"
                            class="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium">
                            <i class="pi pi-chart-bar mr-2"></i>
                            View Details
                        </button>
                        <button @click="exportClassroom(classroom)"
                            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium">
                            <i class="pi pi-download"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Student Detail Modal -->
        <div v-if="selectedStudent" @click="selectedStudent = null"
            class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
            <div @click.stop class="bg-white rounded-xl shadow-2xl max-w-md w-full p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-xl font-bold text-gray-900">Student Details</h3>
                    <button @click="selectedStudent = null" class="text-gray-400 hover:text-gray-600">
                        <i class="pi pi-times text-xl"></i>
                    </button>
                </div>
                
                <div class="text-center mb-6">
                    <div class="w-24 h-24 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-2xl mx-auto mb-3">
                        {{ getInitials(selectedStudent.name) }}
                    </div>
                    <h4 class="text-lg font-semibold text-gray-900">{{ selectedStudent.name }}</h4>
                    <p class="text-sm text-gray-500">{{ selectedStudent.id_number }}</p>
                </div>

                <div class="space-y-3">
                    <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <i class="pi pi-envelope text-indigo-600"></i>
                        <div>
                            <p class="text-xs text-gray-500">Email</p>
                            <p class="text-sm font-medium text-gray-900">{{ selectedStudent.email }}</p>
                        </div>
                    </div>
                </div>

                <button @click="selectedStudent = null"
                    class="w-full mt-6 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium">
                    Close
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const isLoading = ref(false);
const classrooms = ref([]);
const selectedStudent = ref(null);

// Load classroom data
const loadClassrooms = async () => {
    isLoading.value = true;
    try {
        const response = await axios.get('/api/classrooms/');
        if (response.data && response.data.classrooms) {
            classrooms.value = response.data.classrooms.map(classroom => ({
                ...classroom,
                showStudents: false
            }));
            console.log('Loaded classrooms:', classrooms.value);
        }
    } catch (error) {
        console.error('Error loading classrooms:', error);
        classrooms.value = [];
    } finally {
        isLoading.value = false;
    }
};

// Toggle student list visibility
const toggleStudentList = (classroom) => {
    classroom.showStudents = !classroom.showStudents;
};

// Get student initials
const getInitials = (name) => {
    if (!name) return '?';
    const parts = name.split(' ');
    if (parts.length >= 2) {
        return parts[0][0] + parts[parts.length - 1][0];
    }
    return name.substring(0, 2).toUpperCase();
};

// Get attendance rate (mock data for now)
const getAttendanceRate = (classroom) => {
    // This would normally come from the backend
    return Math.floor(85 + Math.random() * 15);
};

// View student details
const viewStudent = (student) => {
    selectedStudent.value = student;
};

// View classroom details
const viewClassroomDetails = (classroom) => {
    console.log('View details for classroom:', classroom);
    // Navigate to detailed view or open modal
};

// Export classroom data
const exportClassroom = (classroom) => {
    console.log('Export classroom:', classroom);
    // Implement export functionality
};

onMounted(() => {
    loadClassrooms();
});
</script>

<style scoped>
/* Custom scrollbar for student list */
.max-h-96::-webkit-scrollbar {
    width: 6px;
}

.max-h-96::-webkit-scrollbar-track {
    background: #f3f4f6;
    border-radius: 10px;
}

.max-h-96::-webkit-scrollbar-thumb {
    background: #9ca3af;
    border-radius: 10px;
}

.max-h-96::-webkit-scrollbar-thumb:hover {
    background: #6b7280;
}
</style>
