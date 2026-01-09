<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        <!-- Header -->
        <div class="bg-white shadow-sm border-b border-gray-200">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                <div class="flex items-center justify-between">
                    <div>
                        <h1 class="text-2xl font-bold text-gray-900">My Classroom</h1>
                        <p class="text-sm text-gray-600 mt-1">Manage your students, track attendance, and monitor performance</p>
                    </div>
                    <div class="flex items-center gap-3">
                        <button @click="showQuickActions = true"
                            class="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2">
                            <i class="pi pi-bolt text-yellow-500"></i>
                            <span class="hidden sm:inline">Quick Actions</span>
                        </button>
                        <div class="flex items-center gap-2 bg-white px-3 py-1 rounded-full border border-gray-200">
                            <span class="text-sm text-gray-500">School Year:</span>
                            <span class="text-sm font-medium text-indigo-700">2024-2025</span>
                        </div>
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

            <!-- Quick Stats Overview -->
            <div v-else>
                <!-- Statistics Cards -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div class="bg-white rounded-lg shadow-sm p-4 border-l-4 border-blue-500">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm text-gray-600">Total Students</p>
                                <p class="text-2xl font-bold text-gray-900">{{ getTotalStudents() }}</p>
                            </div>
                            <i class="pi pi-users text-blue-500 text-2xl"></i>
                        </div>
                    </div>
                    
                    <div class="bg-white rounded-lg shadow-sm p-4 border-l-4 border-green-500">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm text-gray-600">Present Today</p>
                                <p class="text-2xl font-bold text-gray-900">{{ getPresentToday() }}</p>
                            </div>
                            <i class="pi pi-check-circle text-green-500 text-2xl"></i>
                        </div>
                    </div>
                    
                    <div class="bg-white rounded-lg shadow-sm p-4 border-l-4 border-yellow-500">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm text-gray-600">Avg Performance</p>
                                <p class="text-2xl font-bold text-gray-900">{{ getAvgPerformance() }}%</p>
                            </div>
                            <i class="pi pi-chart-line text-yellow-500 text-2xl"></i>
                        </div>
                    </div>
                    
                    <div class="bg-white rounded-lg shadow-sm p-4 border-l-4 border-purple-500">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm text-gray-600">Activities</p>
                                <p class="text-2xl font-bold text-gray-900">{{ getTotalActivities() }}</p>
                            </div>
                            <i class="pi pi-book text-purple-500 text-2xl"></i>
                        </div>
                    </div>
                </div>

                <!-- Classroom Cards -->
                <div class="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
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
                    <div class="grid grid-cols-4 divide-x divide-gray-200 bg-gray-50">
                        <div class="p-4 text-center hover:bg-white transition-colors cursor-pointer">
                            <p class="text-2xl font-bold text-gray-900">{{ classroom.grade_level }}</p>
                            <p class="text-sm text-gray-600">Grade</p>
                        </div>
                        <div class="p-4 text-center hover:bg-white transition-colors cursor-pointer">
                            <p class="text-2xl font-bold text-gray-900">{{ classroom.section }}</p>
                            <p class="text-sm text-gray-600">Section</p>
                        </div>
                        <div class="p-4 text-center hover:bg-white transition-colors cursor-pointer">
                            <p class="text-2xl font-bold text-green-600">{{ getAttendanceRate(classroom) }}%</p>
                            <p class="text-sm text-gray-600">Present</p>
                        </div>
                        <div class="p-4 text-center hover:bg-white transition-colors cursor-pointer">
                            <p class="text-2xl font-bold text-blue-600">{{ getAvgScore(classroom) }}</p>
                            <p class="text-sm text-gray-600">Avg Score</p>
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

                    <!-- Quick Actions Bar -->
                    <div class="bg-white px-6 py-3 border-t border-gray-100">
                        <div class="flex items-center justify-between mb-3">
                            <h4 class="text-sm font-semibold text-gray-700">Quick Actions</h4>
                            <button @click="toggleQuickActions(classroom)"
                                class="text-gray-400 hover:text-gray-600">
                                <i class="pi" :class="classroom.showActions ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
                            </button>
                        </div>
                        
                        <div v-if="classroom.showActions" class="grid grid-cols-2 gap-2">
                            <button @click="takeAttendance(classroom)"
                                class="px-3 py-2 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors text-sm font-medium flex items-center justify-center gap-2">
                                <i class="pi pi-check-square"></i>
                                Attendance
                            </button>
                            <button @click="createActivity(classroom)"
                                class="px-3 py-2 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors text-sm font-medium flex items-center justify-center gap-2">
                                <i class="pi pi-plus"></i>
                                Activity
                            </button>
                            <button @click="sendAnnouncement(classroom)"
                                class="px-3 py-2 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors text-sm font-medium flex items-center justify-center gap-2">
                                <i class="pi pi-megaphone"></i>
                                Announce
                            </button>
                            <button @click="viewReports(classroom)"
                                class="px-3 py-2 bg-yellow-50 text-yellow-700 rounded-lg hover:bg-yellow-100 transition-colors text-sm font-medium flex items-center justify-center gap-2">
                                <i class="pi pi-chart-bar"></i>
                                Reports
                            </button>
                        </div>
                    </div>

                    <!-- Actions -->
                    <div class="px-6 pb-6 flex gap-3">
                        <button @click="viewClassroomDetails(classroom)"
                            class="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium">
                            <i class="pi pi-eye mr-2"></i>
                            View Full Details
                        </button>
                        <button @click="exportClassroom(classroom)"
                            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium">
                            <i class="pi pi-download"></i>
                        </button>
                    </div>
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

// Define emits for navigation
const emit = defineEmits(['navigate']);

const isLoading = ref(false);
const classrooms = ref([]);
const selectedStudent = ref(null);
const showQuickActions = ref(false);

// Load classroom data
const loadClassrooms = async () => {
    isLoading.value = true;
    try {
        const response = await axios.get('/api/classrooms/');
        if (response.data && response.data.classrooms) {
            classrooms.value = response.data.classrooms.map(classroom => ({
                ...classroom,
                showStudents: false,
                showActions: false
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

// Get average score for classroom
const getAvgScore = (classroom) => {
    // This would normally come from the backend
    return Math.floor(75 + Math.random() * 20);
};

// Toggle quick actions visibility
const toggleQuickActions = (classroom) => {
    classroom.showActions = !classroom.showActions;
};

// Statistics methods
const getTotalStudents = () => {
    return classrooms.value.reduce((total, classroom) => total + (classroom.student_count || 0), 0);
};

const getPresentToday = () => {
    // This would come from attendance data
    const total = getTotalStudents();
    return Math.floor(total * 0.92); // Mock 92% attendance
};

const getAvgPerformance = () => {
    // This would come from grades/scores data
    return 85; // Mock average
};

const getTotalActivities = () => {
    // This would come from activities data
    return 24; // Mock count
};

// Quick action methods
const takeAttendance = (classroom) => {
    console.log('Taking attendance for:', classroom.name);
    // Navigate to attendance page or open modal
};

const createActivity = (classroom) => {
    console.log('Creating activity for:', classroom.name);
    // Navigate to create activity page
};

const sendAnnouncement = (classroom) => {
    console.log('Sending announcement to:', classroom.name);
    // Open announcement modal
};

const viewReports = (classroom) => {
    console.log('Viewing reports for:', classroom.name);
    // Navigate to reports page
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
