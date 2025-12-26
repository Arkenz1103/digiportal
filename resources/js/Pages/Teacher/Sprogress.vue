<template>
    <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-violet-50 to-blue-50">
        <!-- Class Header -->
        <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-6 md:p-4 shadow-lg rounded-b-3xl">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div class="space-y-3">
                    <h1 class="text-xl md:text-2xl font-bold text-white px-4 py-2 md:px-6 md:py-3 rounded-lg inline-block bg-white/20">
                        {{ currentClassName }}
                    </h1>
                    <p class="text-white/90 ml-2 flex items-center gap-2">
                        <i class="pi pi-user"></i>
                        Teacher: {{ auth.user.name }}
                    </p>
                </div>
            </div>

            <!-- Page Title -->
            <div class="mt-6 md:mt-8">
                <h2 class="text-2xl md:text-3xl font-bold text-white">Student Progress</h2>
            </div>
        </div>

        <!-- Main Content -->
        <div class="p-6">
            <!-- Search Section with Back Button -->
            <div class="mb-6 flex items-center justify-between">
                <div class="flex items-center gap-3">
                    <!-- Back Button on the left -->
                    <button
                        @click="goBackToRoom"
                        class="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white hover:bg-indigo-700 rounded-lg transition-all shadow-sm">
                        <i class="pi pi-arrow-left text-sm"></i>
                        <span class="text-sm font-medium">Back to Activities</span>
                    </button>

                    <!-- Search Bar -->
                    <div class="relative" style="width: 300px;">
                        <input
                            type="text"
                            v-model="searchQuery"
                            placeholder="Search by student name or ID..."
                            class="w-full pl-10 pr-10 py-2 rounded-lg border border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-200 transition-all bg-white text-gray-700 placeholder-gray-400 text-sm"
                        />
                        <div class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                            <i class="pi pi-search text-sm"></i>
                        </div>
                        <div v-if="searchQuery" class="absolute right-3 top-1/2 -translate-y-1/2">
                            <button
                                @click="searchQuery = ''"
                                class="text-gray-400 hover:text-gray-600 transition-colors">
                                <i class="pi pi-times text-xs"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Export Class Record Button -->
                <button
                    @click="showExportConfirmDialog = true"
                    class="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white hover:bg-emerald-700 rounded-lg transition-all shadow-sm">
                    <i class="pi pi-file-excel text-sm"></i>
                    <span class="text-sm font-medium">Export Class Record</span>
                </button>
            </div>

            <!-- Search Results Info -->
            <div v-if="searchQuery" class="mb-4">
                <p v-if="filteredStudents.length === 0" class="text-sm text-gray-500 ml-2">
                    No students found matching "{{ searchQuery }}"
                </p>
                <p v-else class="text-sm text-indigo-600 ml-2">
                    Found {{ filteredStudents.length }} student(s)
                </p>
            </div>

            <!-- Student List Section - Matching Activities List Design -->
            <div class="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
                <!-- Table Header -->
                <div class="grid grid-cols-12 gap-2 px-6 py-4 bg-gradient-to-r from-indigo-600 to-violet-600">
                    <div class="col-span-1 text-sm font-bold text-white">#</div>
                    <div class="col-span-3 text-sm font-bold text-white">Student Name</div>
                    <div class="col-span-2 text-sm font-bold text-white">Student ID</div>
                    <div class="col-span-2 text-sm font-bold text-white text-center">Outputs</div>
                    <div class="col-span-2 text-sm font-bold text-white text-center">Progress</div>
                    <div class="col-span-2 text-sm font-bold text-white text-center">Download</div>
                </div>

                <!-- Student Items -->
                <div v-for="(student, index) in displayedStudents" :key="student.id"
                    class="grid grid-cols-12 gap-2 items-center px-6 py-4 border-b border-gray-100 hover:bg-indigo-50/50 transition-colors">
                    <div class="col-span-1">
                        <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center">
                            <span class="text-indigo-700 font-bold text-sm">{{ index + 1 }}</span>
                        </div>
                    </div>
                    <div class="col-span-3 flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center shadow-md overflow-hidden">
                            <img v-if="student.profile_picture" :src="student.profile_picture" :alt="student.name" class="w-full h-full object-cover" />
                            <span v-else class="text-white font-bold text-sm">{{ getInitials(student.name) }}</span>
                        </div>
                        <div>
                            <span class="font-semibold text-gray-800 block text-sm">{{ student.name }}</span>
                            <span class="text-xs text-gray-500">{{ student.gradeLevel }} - {{ student.section }}</span>
                        </div>
                    </div>
                    <div class="col-span-2">
                        <span class="text-gray-700 font-medium text-sm">{{ student.id }}</span>
                    </div>
                    <div class="col-span-2 flex justify-center">
                        <button
                            class="px-4 py-2 rounded-lg bg-gradient-to-r from-indigo-500 to-violet-500 text-white font-medium hover:from-indigo-600 hover:to-violet-600 transition-all shadow-md text-xs"
                            @click="viewOutputs(student)">
                            <span class="flex items-center gap-1">
                                <i class="pi pi-images text-xs"></i>
                                View
                            </span>
                        </button>
                    </div>
                    <div class="col-span-2 flex justify-center">
                        <button
                            class="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-medium hover:from-blue-600 hover:to-cyan-600 transition-all shadow-md text-xs"
                            @click="viewDetails(student)">
                            <span class="flex items-center gap-1">
                                <i class="pi pi-chart-line text-xs"></i>
                                Details
                            </span>
                        </button>
                    </div>
                    <div class="col-span-2 flex justify-center">
                        <button
                            class="px-4 py-2 rounded-lg bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-medium hover:from-emerald-600 hover:to-teal-600 transition-all shadow-md text-xs"
                            @click="confirmStudentExport(student)"
                            title="Export student report (.xlsx)">
                            <span class="flex items-center gap-1">
                                <i class="pi pi-file-excel text-xs"></i>
                                Export
                            </span>
                        </button>
                    </div>
                </div>

                <!-- Load More Button -->
                <div v-if="hasMoreStudents" class="p-4 text-center border-t border-gray-100 bg-gradient-to-r from-indigo-50 to-violet-50">
                    <button 
                        @click="loadMoreStudents"
                        class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors duration-200 flex items-center gap-2 mx-auto">
                        <i class="pi pi-chevron-down"></i>
                        <span>Load More ({{ remainingStudents }} more)</span>
                    </button>
                </div>

                <!-- Empty State -->
                <div v-if="filteredStudents.length === 0 && !searchQuery" class="p-8 text-center">
                    <i class="pi pi-users text-4xl text-gray-300 mb-4"></i>
                    <p class="text-gray-500">No students found in this classroom</p>
                </div>
            </div>
        </div>

        <!-- Export Class Record Confirmation Dialog -->
        <Teleport to="body">
            <Transition name="fade">
                <div v-if="showExportConfirmDialog" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click="showExportConfirmDialog = false">
                    <div class="bg-white rounded-xl shadow-2xl w-[400px] overflow-hidden" @click.stop>
                        <div class="p-6 text-center">
                            <div class="w-16 h-16 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-4">
                                <i class="pi pi-file-excel text-3xl text-emerald-600"></i>
                            </div>
                            <h3 class="text-lg font-bold text-gray-800 mb-2">Export Class Record</h3>
                            <p class="text-gray-600 text-sm mb-6">Are you sure you want to export the class record? This will generate an Excel file with all students' progress.</p>
                            <div class="flex gap-3 justify-center">
                                <button
                                    @click="showExportConfirmDialog = false"
                                    class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-colors">
                                    Cancel
                                </button>
                                <button
                                    @click="confirmExportClassRecord"
                                    class="px-6 py-2 rounded-lg bg-emerald-600 text-white font-medium hover:bg-emerald-700 transition-colors">
                                    Export
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </Transition>
        </Teleport>

        <!-- Export Student Record Confirmation Dialog -->
        <Teleport to="body">
            <Transition name="fade">
                <div v-if="showStudentExportConfirmDialog" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click="showStudentExportConfirmDialog = false">
                    <div class="bg-white rounded-xl shadow-2xl w-[400px] overflow-hidden" @click.stop>
                        <div class="p-6 text-center">
                            <div class="w-16 h-16 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-4">
                                <i class="pi pi-user text-3xl text-emerald-600"></i>
                            </div>
                            <h3 class="text-lg font-bold text-gray-800 mb-2">Export Student Report</h3>
                            <p class="text-gray-600 text-sm mb-6">Export progress report for <span class="font-semibold text-indigo-600">{{ studentToExport?.name }}</span>?</p>
                            <div class="flex gap-3 justify-center">
                                <button
                                    @click="showStudentExportConfirmDialog = false"
                                    class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-colors">
                                    Cancel
                                </button>
                                <button
                                    @click="confirmStudentExportAction"
                                    class="px-6 py-2 rounded-lg bg-emerald-600 text-white font-medium hover:bg-emerald-700 transition-colors">
                                    Export
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </Transition>
        </Teleport>

        <!-- Outputs Dialog -->
        <Teleport to="body">
            <Transition name="fade">
                <div v-if="showOutputsDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click="closeOutputsDialog">
                    <div class="relative bg-white rounded-2xl shadow-2xl w-[900px] h-[600px] overflow-hidden border border-indigo-200 flex flex-col" @click.stop>
                        <!-- Dialog Header -->
                        <div class="flex items-center justify-between px-6 py-4 border-b border-indigo-100 bg-gradient-to-r from-indigo-50 to-violet-50 flex-shrink-0">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center text-white font-bold shadow-lg overflow-hidden">
                                    <img v-if="selectedStudent?.profile_picture" :src="selectedStudent.profile_picture" :alt="selectedStudent.name" class="w-full h-full object-cover" />
                                    <span v-else>{{ getInitials(selectedStudent?.name) }}</span>
                                </div>
                                <div>
                                    <h3 class="text-xl font-bold text-indigo-900">{{ selectedStudent?.name }}'s Outputs</h3>
                                    <p class="text-sm text-indigo-600">Student ID: {{ selectedStudent?.id }}</p>
                                </div>
                            </div>
                            <button
                                @click="closeOutputsDialog"
                                class="p-2 rounded-full hover:bg-indigo-100 text-indigo-600 transition-all duration-200 hover:rotate-90 transform">
                                <i class="pi pi-times text-xl"></i>
                            </button>
                        </div>

                        <!-- Dialog Content -->
                        <div class="flex-1 p-6 overflow-y-auto bg-gradient-to-br from-gray-50 to-indigo-50/30">
                            <!-- Loading State -->
                            <div v-if="isLoadingOutputs" class="flex flex-col justify-center items-center py-20">
                                <div class="animate-spin rounded-full h-16 w-16 border-4 border-indigo-200 border-t-indigo-600 mb-4"></div>
                                <p class="text-indigo-600 font-medium">Loading outputs...</p>
                            </div>

                            <div v-else class="flex flex-col items-center">
                                <!-- Subject Tabs -->
                                <div class="w-full max-w-3xl mb-6">
                                    <div class="flex space-x-1.5 bg-gradient-to-r from-indigo-50 to-violet-50 p-1.5 rounded-lg shadow-sm border border-indigo-200">
                                        <button
                                            v-for="subject in subjects"
                                            :key="subject.id"
                                            @click="selectedSubject = subject.id"
                                            class="flex-1 px-3 py-1.5 rounded-md text-xs font-semibold transition-all duration-300 transform"
                                            :class="selectedSubject === subject.id
                                                ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-md scale-105'
                                                : 'text-indigo-700 hover:text-indigo-900 hover:bg-white/60 hover:shadow-sm hover:scale-102'">
                                            {{ subject.name }}
                                        </button>
                                    </div>
                                </div>

                                <!-- Image Gallery with Navigation -->
                                <div class="relative w-full max-w-3xl">
                                    <!-- Empty State -->
                                    <div v-if="getCurrentSubjectOutputs().length === 0" class="flex flex-col items-center justify-center py-16 px-4">
                                        <div class="w-24 h-24 rounded-full bg-indigo-100 flex items-center justify-center mb-4">
                                            <i class="pi pi-images text-4xl text-indigo-400"></i>
                                        </div>
                                        <h4 class="text-lg font-semibold text-gray-700 mb-2">No Outputs Yet</h4>
                                        <p class="text-gray-500 text-center max-w-md">
                                            This student hasn't submitted any outputs for {{ selectedSubject === 'all' ? 'any subject' : 'this subject' }} yet.
                                        </p>
                                    </div>

                                    <!-- Minimized View (Grid of thumbnails) -->
                                    <div v-else-if="isMinimizedView" class="grid grid-cols-4 gap-4">
                                        <div
                                            v-for="(output, index) in getCurrentSubjectOutputs()"
                                            :key="index"
                                            @click="expandImage(index)"
                                            class="relative group cursor-pointer bg-white rounded-lg overflow-hidden aspect-square hover:shadow-lg transition-all duration-200 border border-gray-200 hover:border-indigo-300">
                                            <!-- PDF File -->
                                            <div v-if="isPdfFile(output)" class="w-full h-full flex flex-col items-center justify-center bg-gray-50 group-hover:bg-gray-100 transition-colors">
                                                <i class="pi pi-file-pdf text-4xl text-red-500 mb-2"></i>
                                                <span class="text-xs text-gray-600 text-center px-2 truncate w-full">{{ getFileName(output) }}</span>
                                            </div>
                                            <!-- Image File -->
                                            <img
                                                v-else
                                                :src="output.url || output"
                                                :alt="output.title || `Output ${index + 1}`"
                                                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                                            >
                                            <!-- Date badge only -->
                                            <div class="absolute top-2 right-2 bg-white/90 px-2 py-1 rounded text-xs font-medium text-gray-700">
                                                {{ output.date ? new Date(output.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '' }}
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Expanded View (Single full-size image/file) -->
                                    <div v-else class="flex items-center justify-center bg-gray-100 rounded-lg p-4 min-h-[350px]">
                                        <div class="relative">
                                            <!-- PDF File - Show embed or link -->
                                            <div v-if="isPdfFile(currentImage)" class="flex flex-col items-center justify-center p-8">
                                                <i class="pi pi-file-pdf text-6xl text-red-500 mb-4"></i>
                                                <p class="text-gray-700 font-medium mb-4">{{ getFileName(currentImage) }}</p>
                                                <a 
                                                    :href="currentImage.url || currentImage" 
                                                    target="_blank"
                                                    class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2">
                                                    <i class="pi pi-external-link"></i>
                                                    Open PDF
                                                </a>
                                            </div>
                                            <!-- Image File -->
                                            <img
                                                v-else
                                                :src="currentImage.url || currentImage"
                                                :alt="currentImage.title || 'Student output'"
                                                class="max-w-full h-auto max-h-[380px] rounded-lg shadow-lg"
                                            >
                                            <!-- Counter badge -->
                                            <div class="absolute top-4 right-4 bg-indigo-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                                                {{ currentImageIndex + 1 }} / {{ getCurrentSubjectOutputs().length }}
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Navigation Buttons (only show in expanded view) -->
                                    <div v-if="!isMinimizedView">
                                        <button
                                            @click="prevImage"
                                            class="absolute left-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-white/80 flex items-center justify-center shadow-md hover:bg-white transition-colors"
                                            :disabled="currentImageIndex === 0"
                                            :class="{ 'opacity-50 cursor-not-allowed': currentImageIndex === 0 }">
                                            <i class="pi pi-chevron-left"></i>
                                        </button>

                                        <button
                                            @click="nextImage"
                                            class="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-white/80 flex items-center justify-center shadow-md hover:bg-white transition-colors"
                                            :disabled="currentImageIndex === getCurrentSubjectOutputs().length - 1"
                                            :class="{ 'opacity-50 cursor-not-allowed': currentImageIndex === getCurrentSubjectOutputs().length - 1 }">
                                            <i class="pi pi-chevron-right"></i>
                                        </button>
                                    </div>

                                    <!-- Back to Grid Button (only show in expanded view) -->
                                    <div v-if="!isMinimizedView" class="mt-4 text-center">
                                        <button
                                            @click="showMinimizedView"
                                            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm">
                                            <i class="pi pi-th-large mr-2"></i>
                                            Back to Grid View
                                        </button>
                                    </div>
                                </div>

                                <!-- Image Details (only show in expanded view) -->
                                <div v-if="!isMinimizedView" class="mt-6 w-full">
                                    <h4 class="font-semibold text-gray-800 mb-3">Output Details</h4>
                                    <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                                        <div class="grid grid-cols-2 gap-4">
                                            <!-- Activity -->
                                            <div>
                                                <p class="text-xs text-gray-500 uppercase mb-1">Activity</p>
                                                <p class="font-medium text-gray-900">{{ getCurrentAssignment().title }}</p>
                                            </div>

                                            <!-- Type -->
                                            <div>
                                                <p class="text-xs text-gray-500 uppercase mb-1">Type</p>
                                                <p class="font-medium text-gray-900">{{ getCurrentAssignment().type }}</p>
                                            </div>

                                            <!-- Submitted Date & Time -->
                                            <div>
                                                <p class="text-xs text-gray-500 uppercase mb-1">Date & Time Submitted</p>
                                                <p class="font-medium text-gray-900">{{ getCurrentAssignment().date }} {{ getCurrentAssignment().time }}</p>
                                            </div>

                                            <!-- Score -->
                                            <div>
                                                <p class="text-xs text-gray-500 uppercase mb-1">Score</p>
                                                <p class="font-medium text-gray-900">{{ getFormattedScore() }}</p>
                                            </div>

                                            <!-- Status -->
                                            <div class="col-span-2">
                                                <p class="text-xs text-gray-500 uppercase mb-1">Status</p>
                                                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                                                      :class="getStatusClass()">
                                                    {{ getDisplayStatus() }}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </Transition>
        </Teleport>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import * as XLSX from 'xlsx';
import { useToast } from '../../composables/useToast';

const { showSuccess, showError, showInfo, showWarning } = useToast();

// Helper function to get initials from name (first and last name initials)
const getInitials = (name) => {
    if (!name) return '?';
    const parts = name.trim().split(' ').filter(p => p.length > 0);
    if (parts.length >= 2) {
        return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
    }
    return name.charAt(0).toUpperCase();
};

// Define props
const props = defineProps({
    className: {
        type: String,
        default: null
    }
});

// Define emits for navigation
const emit = defineEmits(['navigate']);

// Download dropdown state
const showDownloadDropdown = ref(false);
const downloadDropdownRef = ref(null);

// Export confirmation dialog states
const showExportConfirmDialog = ref(false);
const showStudentExportConfirmDialog = ref(false);
const studentToExport = ref(null);

// Confirm student export - show dialog
const confirmStudentExport = (student) => {
    studentToExport.value = student;
    showStudentExportConfirmDialog.value = true;
};

// Execute student export after confirmation
const confirmStudentExportAction = () => {
    showStudentExportConfirmDialog.value = false;
    if (studentToExport.value) {
        downloadStudentRecord(studentToExport.value);
    }
};

// Execute class record export after confirmation
const confirmExportClassRecord = () => {
    showExportConfirmDialog.value = false;
    downloadRecords('all_students');
};

// Toggle download dropdown
const toggleDownloadDropdown = () => {
    showDownloadDropdown.value = !showDownloadDropdown.value;
};

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
    if (downloadDropdownRef.value && !downloadDropdownRef.value.contains(event.target)) {
        showDownloadDropdown.value = false;
    }
};

// Download records function - generates Excel/CSV from displayed student data
const downloadRecords = async (exportType) => {
    showDownloadDropdown.value = false;

    try {
        // Get students to export and sort by last name alphabetically
        const studentsToExport = [...filteredStudents.value].sort((a, b) => {
            // Extract last name (assume format is "First Last" or just use full name)
            const getLastName = (name) => {
                const parts = name.trim().split(' ');
                return parts.length > 1 ? parts[parts.length - 1].toLowerCase() : name.toLowerCase();
            };
            return getLastName(a.name).localeCompare(getLastName(b.name));
        });

        if (studentsToExport.length === 0) {
            showError('No students to export', 'Export Error');
            return;
        }

        const timestamp = new Date().toISOString().slice(0, 10);
        const className = currentClassName.value.replace(/\s+/g, '_') || 'Class';

        if (exportType === 'all_students') {
            // Full Progress Export - Excel with one sheet per subject
            showInfo('Generating class record...', 'Export');

            // Fetch all activities and submissions for all students
            const classRecordData = await fetchClassRecordData(studentsToExport);
            
            if (!classRecordData || Object.keys(classRecordData.subjects).length === 0) {
                showError('No activities found for this class', 'Export Error');
                return;
            }

            // Create Excel workbook with multiple sheets
            const workbook = XLSX.utils.book_new();

            // Create a sheet for each subject
            for (const [subjectName, subjectData] of Object.entries(classRecordData.subjects)) {
                const activities = subjectData.activities;
                
                if (activities.length === 0) continue;

                // Calculate the number of columns needed
                const totalColumns = 3 + activities.length; // No, Student ID, Student Name + activities

                // Build sheet data as array of arrays
                const sheetData = [];

                // Row 1: Empty row for spacing
                sheetData.push(Array(totalColumns).fill(''));

                // Row 2: Centered title - ACTIVITY CLASS RECORD - SUBJECT
                const titleRow = Array(totalColumns).fill('');
                titleRow[0] = `ACTIVITY CLASS RECORD - ${subjectName.toUpperCase()}`;
                sheetData.push(titleRow);

                // Row 3: Empty row for spacing
                sheetData.push(Array(totalColumns).fill(''));

                // Row 4: Header row with activity title and type
                const headerRow = ['No', 'Student ID', 'Student Name'];
                activities.forEach((act) => {
                    headerRow.push(`${act.title} (${act.type})`);
                });
                sheetData.push(headerRow);

                // Data rows: each student with their scores (sorted by last name)
                studentsToExport.forEach((student, index) => {
                    const studentId = student.dbId || student.id;
                    const row = [index + 1, student.id, student.name];

                    activities.forEach((act) => {
                        const submission =
                            classRecordData.submissions[`${studentId}-${act.id}`];
                        if (
                            submission &&
                            submission.status === 'scored' &&
                            submission.score
                        ) {
                            // Show only the score (e.g., "8/10")
                            row.push(submission.score);
                        } else {
                            // Not scored or not submitted = None
                            row.push('None');
                        }
                    });
                    sheetData.push(row);
                });

                // Create worksheet from data
                const worksheet = XLSX.utils.aoa_to_sheet(sheetData);

                // Merge cells for the title row to center it
                const mergeRange = { s: { r: 1, c: 0 }, e: { r: 1, c: totalColumns - 1 } };
                worksheet['!merges'] = [mergeRange];

                // Set column widths
                const colWidths = [
                    { wch: 5 },   // No
                    { wch: 12 },  // Student ID
                    { wch: 25 },  // Student Name
                ];
                activities.forEach(() => {
                    colWidths.push({ wch: 15 }); // Activity columns
                });
                worksheet['!cols'] = colWidths;

                // Sanitize sheet name (Excel has 31 char limit and no special chars)
                let sheetName = subjectName.substring(0, 31).replace(/[\\\/\?\*\[\]]/g, '');
                
                // Add worksheet to workbook
                XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);
            }

            // Generate Excel file and download
            const filename = `ClassRecord_${className}_${timestamp}.xlsx`;
            XLSX.writeFile(workbook, filename);

            showSuccess('Class record downloaded!', 'Export');
            return;
        }

        // For other export types, use CSV
        let csvContent = '';
        let filename = '';

        if (exportType === 'summary') {
            // Summary export - basic student info
            csvContent = 'No,Student ID,Student Name,Grade Level,Section,Classroom,Teacher\n';
            studentsToExport.forEach((student, index) => {
                csvContent += `${index + 1},"${student.id}","${student.name}","${student.gradeLevel || 'N/A'}","${student.section || 'N/A'}","${student.classroom || 'N/A'}","${student.teacher || 'N/A'}"\n`;
            });
            filename = `Student_Summary_${className}_${timestamp}.csv`;

        } else if (exportType === 'scored_only') {
            // Scored activities only
            showInfo('Fetching scored activities...', 'Export');
            const classRecordData = await fetchClassRecordData(studentsToExport);
            
            csvContent = `SCORED ACTIVITIES REPORT - ${currentClassName.value}\n`;
            csvContent += `Generated: ${new Date().toLocaleString()}\n\n`;
            csvContent += `No,Student ID,Student Name,Subject,Activity,Type,Score,Date Submitted\n`;

            let rowNum = 1;
            for (const [subjectName, subjectData] of Object.entries(classRecordData.subjects)) {
                for (const student of studentsToExport) {
                    const studentId = student.dbId || student.id;
                    for (const act of subjectData.activities) {
                        const submission = classRecordData.submissions[`${studentId}-${act.id}`];
                        if (submission && submission.status === 'scored') {
                            csvContent += `${rowNum++},"${student.id}","${student.name}","${subjectName}","${act.title}","${act.type}","${submission.score}","${submission.submitted_at || 'N/A'}"\n`;
                        }
                    }
                }
            }
            filename = `ScoredActivities_${className}_${timestamp}.csv`;

        } else if (exportType === 'missing_only') {
            // Missing activities only
            showInfo('Fetching missing activities...', 'Export');
            const classRecordData = await fetchClassRecordData(studentsToExport);
            
            csvContent = `MISSING ACTIVITIES REPORT - ${currentClassName.value}\n`;
            csvContent += `Generated: ${new Date().toLocaleString()}\n\n`;
            csvContent += `No,Student ID,Student Name,Subject,Activity,Type,Due Date\n`;

            let rowNum = 1;
            for (const [subjectName, subjectData] of Object.entries(classRecordData.subjects)) {
                for (const student of studentsToExport) {
                    const studentId = student.dbId || student.id;
                    for (const act of subjectData.activities) {
                        const submission = classRecordData.submissions[`${studentId}-${act.id}`];
                        if (!submission) {
                            csvContent += `${rowNum++},"${student.id}","${student.name}","${subjectName}","${act.title}","${act.type}","${act.due_date || 'N/A'}"\n`;
                        }
                    }
                }
            }
            filename = `MissingActivities_${className}_${timestamp}.csv`;

        } else {
            // Default - basic list
            csvContent = 'No,Student ID,Student Name,Grade Level,Section,Classroom,Teacher\n';
            studentsToExport.forEach((student, index) => {
                csvContent += `${index + 1},"${student.id}","${student.name}","${student.gradeLevel || 'N/A'}","${student.section || 'N/A'}","${student.classroom || 'N/A'}","${student.teacher || 'N/A'}"\n`;
            });
            filename = `Student_List_${className}_${timestamp}.csv`;
        }

        // Create and download CSV file
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

        showSuccess('Downloaded successfully!', 'Export');
    } catch (error) {
        console.error('Download error:', error);
        showError('Failed to download records', 'Export Error');
    }
};

// Fetch class record data - all activities grouped by subject with student submissions
const fetchClassRecordData = async (students) => {
    try {
        // Get classroom context
        const classContext = localStorage.getItem('progress_class_context');
        let classroomId = '';
        
        if (classContext) {
            const context = JSON.parse(classContext);
            classroomId = context.classroomId || '';
        }

        // Fetch all activities and submissions from API
        const response = await axios.get(`/api/students/progress/class-record/${classroomId ? `?classroom_id=${classroomId}` : ''}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching class record data:', error);
        
        // Fallback: return empty structure
        return {
            subjects: {},
            submissions: {}
        };
    }
};

// Download individual student record - fetches all activities and submissions as XLSX
const downloadStudentRecord = async (student) => {
    try {
        showInfo('Generating student report...', 'Export');

        // Get the student's database ID
        const studentDbId = student.dbId || student.id;

        // Fetch student's progress details from API
        const response = await axios.get(`/api/students/${studentDbId}/progress/`);
        const progressData = response.data;

        const timestamp = new Date().toISOString().slice(0, 10);

        // Create Excel workbook
        const workbook = XLSX.utils.book_new();

        // Group activities by subject/folder
        const activitiesBySubject = {};
        if (progressData.activities && progressData.activities.length > 0) {
            progressData.activities.forEach((activity) => {
                const folder = activity.folder_name || 'Other';
                if (!activitiesBySubject[folder]) {
                    activitiesBySubject[folder] = [];
                }
                activitiesBySubject[folder].push(activity);
            });
        }

        // Create a sheet for each subject
        for (const [subjectName, activities] of Object.entries(activitiesBySubject)) {
            const sheetData = [];

            // Calculate completed and incomplete for this subject
            const completed = activities.filter(a => a.status && a.status !== 'Missing' && a.status !== 'Pending').length;
            const incomplete = activities.length - completed;

            // Row 1: Empty for spacing
            sheetData.push([]);

            // Row 2: Centered title
            sheetData.push([`STUDENT PROGRESS REPORT - ${subjectName.toUpperCase()}`]);

            // Row 3: Empty for spacing
            sheetData.push([]);

            // Student Information Section
            sheetData.push(['STUDENT INFORMATION']);
            sheetData.push(['Student Name:', student.name]);
            sheetData.push(['Student ID:', student.id]);
            sheetData.push(['Grade Level:', student.gradeLevel || 'N/A']);
            sheetData.push(['Section:', student.section || 'N/A']);
            sheetData.push(['Teacher:', student.teacher || 'N/A']);
            sheetData.push([]); // Empty row

            // Summary Section for this subject
            sheetData.push(['SUMMARY']);
            sheetData.push(['Total Activities:', activities.length]);
            sheetData.push(['Completed:', completed]);
            sheetData.push(['Incomplete:', incomplete]);
            sheetData.push([]); // Empty row

            // Activities Detail Section
            sheetData.push(['ACTIVITIES DETAIL']);
            sheetData.push(['No', 'Activity Title', 'Type', 'Due Date & Time', 'Status', 'Date & Time Submitted', 'Score']);

            // Add activities for this subject
            activities.forEach((activity, index) => {
                const score = activity.score || 'None';
                const status = activity.status || 'Pending';
                const dueDateTime = activity.due_datetime || 'N/A';
                const submittedDateTime = activity.submitted_datetime || 'N/A';
                const activityType = activity.activity_type || 'N/A';

                sheetData.push([
                    index + 1,
                    activity.title,
                    activityType,
                    dueDateTime,
                    status,
                    submittedDateTime,
                    score
                ]);
            });

            // Create worksheet
            const worksheet = XLSX.utils.aoa_to_sheet(sheetData);

            // Set column widths - first column wider for labels
            worksheet['!cols'] = [
                { wch: 18 },  // No / Labels (Student Name:, Total Activities:, etc.)
                { wch: 30 },  // Activity Title / Values
                { wch: 12 },  // Type
                { wch: 20 },  // Due Date & Time
                { wch: 15 },  // Status
                { wch: 22 },  // Date & Time Submitted
                { wch: 10 }   // Score
            ];

            // Sanitize sheet name (Excel has 31 char limit)
            let sheetName = subjectName.substring(0, 31).replace(/[\\\/\?\*\[\]]/g, '');

            // Add worksheet to workbook
            XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);
        }

        // If no activities, create a single sheet with message
        if (Object.keys(activitiesBySubject).length === 0) {
            const sheetData = [];
            sheetData.push(['STUDENT PROGRESS REPORT']);
            sheetData.push([`Generated: ${new Date().toLocaleString()}`]);
            sheetData.push([]);
            sheetData.push(['STUDENT INFORMATION']);
            sheetData.push(['Student Name:', student.name]);
            sheetData.push(['Student ID:', student.id]);
            sheetData.push(['Grade Level:', student.gradeLevel || 'N/A']);
            sheetData.push(['Section:', student.section || 'N/A']);
            sheetData.push(['Teacher:', student.teacher || 'N/A']);
            sheetData.push([]);
            sheetData.push(['No activities found for this student']);

            const worksheet = XLSX.utils.aoa_to_sheet(sheetData);
            worksheet['!cols'] = [{ wch: 18 }, { wch: 30 }];
            XLSX.utils.book_append_sheet(workbook, worksheet, 'Progress Report');
        }

        // Generate filename and download
        const filename = `${student.name.replace(/\s+/g, '_')}_Progress_${timestamp}.xlsx`;
        XLSX.writeFile(workbook, filename);

        showSuccess('Student report downloaded!', 'Export');
    } catch (error) {
        console.error('Download error:', error);
        showError('Failed to download student record. Please try again.', 'Export Error');
    }
};

// Get class name from localStorage (set by Room.vue)
const currentClassName = ref('All Classes');

// Load class name from localStorage on mount
const loadClassName = () => {
    const classContext = localStorage.getItem('progress_class_context');
    if (classContext) {
        try {
            const context = JSON.parse(classContext);
            if (context.className) {
                currentClassName.value = context.className;
                console.log('Loaded class name:', context.className);
            }
        } catch (e) {
            console.error('Error parsing class context:', e);
        }
    }
};

// Mock user data
const currentUser = ref({
    name: 'Teacher Name',
    email: 'teacher@example.com',
    role: 'teacher'
});

const auth = computed(() => ({
    user: currentUser.value
}));

// Student data (loaded from API)
const students = ref([]);

// Pagination
const visibleStudentCount = ref(10);

// Search query
const searchQuery = ref('');

// Filtered students based on search
const filteredStudents = computed(() => {
    if (!searchQuery.value) {
        return students.value;
    }

    const query = searchQuery.value.toLowerCase();
    return students.value.filter(student => {
        const nameMatch = student.name.toLowerCase().includes(query);
        const idMatch = student.id.toLowerCase().includes(query);
        const usernameMatch = student.username?.toLowerCase().includes(query);
        const classroomMatch = student.classroom?.toLowerCase().includes(query);
        return nameMatch || idMatch || usernameMatch || classroomMatch;
    });
});

// Displayed students (paginated)
const displayedStudents = computed(() => {
    return filteredStudents.value.slice(0, visibleStudentCount.value);
});

// Check if there are more students to load
const hasMoreStudents = computed(() => {
    return visibleStudentCount.value < filteredStudents.value.length;
});

// Remaining students count
const remainingStudents = computed(() => {
    return filteredStudents.value.length - visibleStudentCount.value;
});

// Load more students
const loadMoreStudents = () => {
    visibleStudentCount.value += 10;
};

// Dialog state
const showOutputsDialog = ref(false);
const selectedStudent = ref(null);
const currentImageIndex = ref(0);
const selectedSubject = ref('all');
const isLoadingOutputs = ref(false);

// Portfolio folders (loaded from API)
const portfolioFolders = ref([]);

// Subject tabs data (dynamically loaded from folders)
const subjects = ref([
    { id: 'all', name: 'All' }
]);

// Student outputs organized by folder (loaded from API)
const studentOutputs = ref({
    mapeh: [
        {
            url: 'https://images.unsplash.com/photo-1578926375605-eaf7559b1458?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            date: new Date('2025-05-15'),
            title: 'Art Project - Watercolor Painting'
        },
        {
            url: 'https://images.unsplash.com/photo-1588072432836-e10032774350?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            date: new Date('2025-05-10'),
            title: 'Art History Quiz #1'
        },
        {
            url: 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            date: new Date('2025-05-05'),
            title: 'Sketchbook Assignment'
        },
        {
            url: 'https://images.unsplash.com/photo-1501504905252-473c47e087f8?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            date: new Date('2025-05-01'),
            title: 'Modern Art Quiz'
        }
    ],
    english: [
        {
            url: 'https://images.unsplash.com/photo-1455390582262-044cdead277a?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            date: new Date('2025-05-14'),
            title: 'Essay - My Summer Vacation'
        },
        {
            url: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            date: new Date('2025-05-08'),
            title: 'Book Report - Charlotte\'s Web'
        }
    ],
    math: [
        {
            url: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            date: new Date('2025-05-12'),
            title: 'Addition and Subtraction Worksheet'
        }
    ]
});

// Combined outputs for 'All' tab, sorted by most recent
const allOutputs = computed(() => {
    const combined = [];

    // Combine all outputs with subject info
    Object.entries(studentOutputs.value).forEach(([subject, outputs]) => {
        outputs.forEach(output => {
            combined.push({
                ...output,
                subject: subject
            });
        });
    });

    // Sort by date (most recent first)
    return combined.sort((a, b) => b.date - a.date);
});

// Sample assignments data organized by subject
const assignments = ref({
    mapeh: [
        {
            title: 'Art Project - Watercolor Painting',
            date: 'May 1, 2025',
            score: '9/10',
            status: 'Graded',
            description: 'Watercolor landscape painting assignment'
        },
        {
            title: 'Art History Quiz #1',
            date: 'May 5, 2025',
            score: '8/10',
            status: 'Graded',
            description: 'Quiz on Renaissance art history'
        },
        {
            title: 'Sketchbook Assignment',
            date: 'May 10, 2025',
            score: 'Pending',
            status: 'Submitted',
            description: 'Daily sketchbook entries for one week'
        },
        {
            title: 'Modern Art Quiz',
            date: 'May 15, 2025',
            score: '10/10',
            status: 'Graded',
            description: 'Quiz on 20th century modern art movements'
        }
    ],
    english: [
        {
            title: 'Essay - My Summer Vacation',
            date: 'May 2, 2025',
            score: '9/10',
            status: 'Graded',
            description: 'Personal narrative essay assignment'
        },
        {
            title: 'Book Report - Charlotte\'s Web',
            date: 'May 8, 2025',
            score: '8/10',
            status: 'Graded',
            description: 'Literary analysis book report'
        }
    ],
    math: [
        {
            title: 'Addition and Subtraction Worksheet',
            date: 'May 3, 2025',
            score: '10/10',
            status: 'Graded',
            description: 'Basic arithmetic operations practice'
        }
    ]
});

// Combined assignments for 'All' tab
const allAssignments = computed(() => {
    const combined = [];

    // Combine all assignments with subject info
    Object.entries(assignments.value).forEach(([subject, assignmentList]) => {
        assignmentList.forEach(assignment => {
            combined.push({
                ...assignment,
                subject: subject
            });
        });
    });

    // Sort by date (most recent first)
    return combined.sort((a, b) => new Date(b.date) - new Date(a.date));
});

// State for minimized view
const isMinimizedView = ref(true);
const expandedImageIndex = ref(null);

// Computed property for current image based on selected subject
const currentImage = computed(() => {
    if (selectedSubject.value === 'all') {
        return allOutputs.value[currentImageIndex.value];
    }
    const subjectOutputs = studentOutputs.value[selectedSubject.value] || [];
    return subjectOutputs[currentImageIndex.value];
});

// Get current assignment details based on selected subject and image index
const getCurrentAssignment = () => {
    const outputs = getCurrentSubjectOutputs();
    const currentOutput = outputs[currentImageIndex.value];

    if (!currentOutput) {
        return {
            title: 'Assignment',
            date: 'N/A',
            score: 'N/A',
            status: 'N/A',
            description: 'No description available'
        };
    }

    // Format the data from the actual submission
    console.log('📊 getCurrentAssignment - currentOutput:', currentOutput);

    // Use total_score and max_score if available, otherwise calculate from criteria_scores
    let scoreDisplay = 'Not scored';
    let totalScore = currentOutput.total_score;
    let maxScore = currentOutput.max_score;

    // If max_score is missing or is default 10, try to calculate from criteria_scores
    if (currentOutput.criteria_scores && (!maxScore || maxScore === 10)) {
        try {
            const criteria = typeof currentOutput.criteria_scores === 'string'
                ? JSON.parse(currentOutput.criteria_scores)
                : currentOutput.criteria_scores;

            if (Array.isArray(criteria) && criteria.length > 0) {
                totalScore = criteria.reduce((sum, c) => sum + (parseInt(c.score) || 0), 0);
                maxScore = criteria.reduce((sum, c) => sum + (parseInt(c.maxScore) || 0), 0);
                console.log('📊 Calculated from criteria_scores:', { totalScore, maxScore, criteria });
            }
        } catch (error) {
            console.error('Error parsing criteria_scores:', error);
        }
    }

    // Display the score
    if (totalScore !== null && totalScore !== undefined &&
        maxScore !== null && maxScore !== undefined) {
        const total = parseInt(totalScore);
        const max = parseInt(maxScore);
        if (!isNaN(total) && !isNaN(max) && max > 0) {
            scoreDisplay = `${total}/${max}`;
        }
    } else if (currentOutput.score !== null && currentOutput.score !== undefined) {
        // Final fallback to simple score
        const scoreValue = parseInt(currentOutput.score);
        if (!isNaN(scoreValue)) {
            scoreDisplay = `${scoreValue}/10`;
        }
    }

    const submittedDate = currentOutput.date ? new Date(currentOutput.date) : null;

    return {
        title: currentOutput.title || 'Activity',
        type: currentOutput.activity_type || 'N/A',
        date: submittedDate ? submittedDate.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }) : 'N/A',
        time: submittedDate ? submittedDate.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        }) : 'N/A',
        score: scoreDisplay,
        status: currentOutput.status === 'scored' ? 'Scored' : 'Submitted',
        description: currentOutput.caption || 'No description available'
    };
};

// Get formatted score with overall
const getFormattedScore = () => {
    const outputs = getCurrentSubjectOutputs();
    const currentOutput = outputs[currentImageIndex.value];
    
    if (!currentOutput) return 'None';
    
    let totalScore = currentOutput.total_score;
    let maxScore = currentOutput.max_score;
    
    // Try to calculate from criteria_scores if available
    if (currentOutput.criteria_scores && (!maxScore || maxScore === 10)) {
        try {
            const criteria = typeof currentOutput.criteria_scores === 'string'
                ? JSON.parse(currentOutput.criteria_scores)
                : currentOutput.criteria_scores;
            if (Array.isArray(criteria) && criteria.length > 0) {
                totalScore = criteria.reduce((sum, c) => sum + (parseInt(c.score) || 0), 0);
                maxScore = criteria.reduce((sum, c) => sum + (parseInt(c.maxScore) || 0), 0);
            }
        } catch (error) {
            console.error('Error parsing criteria_scores:', error);
        }
    }
    
    if (totalScore !== null && totalScore !== undefined && maxScore !== null && maxScore !== undefined) {
        const total = parseInt(totalScore);
        const max = parseInt(maxScore);
        if (!isNaN(total) && !isNaN(max) && max > 0) {
            return `${total}/${max}`;
        }
    }
    
    if (currentOutput.score !== null && currentOutput.score !== undefined) {
        return `${currentOutput.score}/10`;
    }
    
    return 'None';
};

// Get single display status
const getDisplayStatus = () => {
    const outputs = getCurrentSubjectOutputs();
    const currentOutput = outputs[currentImageIndex.value];
    
    if (!currentOutput) return 'N/A';
    
    // Priority: Resubmitted > Submitted Late > Submitted/Scored
    if (currentOutput.resubmit_count > 0) {
        return `Resubmitted x${currentOutput.resubmit_count}`;
    }
    if (currentOutput.is_late) {
        return 'Submitted Late';
    }
    if (currentOutput.status === 'scored') {
        return 'Scored';
    }
    return 'Submitted';
};

// Get status class for styling
const getStatusClass = () => {
    const outputs = getCurrentSubjectOutputs();
    const currentOutput = outputs[currentImageIndex.value];
    
    if (!currentOutput) return 'bg-gray-100 text-gray-700';
    
    if (currentOutput.resubmit_count > 0) {
        return 'bg-blue-100 text-blue-700';
    }
    if (currentOutput.is_late) {
        return 'bg-orange-100 text-orange-700';
    }
    if (currentOutput.status === 'scored') {
        return 'bg-green-100 text-green-700';
    }
    return 'bg-indigo-100 text-indigo-700';
};

// Check if file is a PDF
const isPdfFile = (output) => {
    if (!output) return false;
    const url = output.url || output;
    if (typeof url !== 'string') return false;
    
    // Check file extension
    if (url.toLowerCase().endsWith('.pdf')) return true;
    
    // Check file_type property
    if (output.file_type && output.file_type.toLowerCase().includes('pdf')) return true;
    
    return false;
};

// Get file name from output
const getFileName = (output) => {
    if (!output) return 'File';
    
    // Try to get from file_name property
    if (output.file_name) return output.file_name;
    
    // Extract from URL
    const url = output.url || output;
    if (typeof url === 'string') {
        const parts = url.split('/');
        const fileName = parts[parts.length - 1];
        // Remove query params if any
        return fileName.split('?')[0] || 'File';
    }
    
    return 'File';
};

// Get current subject outputs for navigation
const getCurrentSubjectOutputs = () => {
    if (selectedSubject.value === 'all') {
        return allOutputs.value;
    }
    return studentOutputs.value[selectedSubject.value] || [];
};

// Function to expand image to full view
const expandImage = (index) => {
    currentImageIndex.value = index;
    expandedImageIndex.value = index;
    isMinimizedView.value = false;
};

// Function to return to minimized view
const showMinimizedView = () => {
    isMinimizedView.value = true;
    expandedImageIndex.value = null;
};

// Navigation functions
const nextImage = () => {
    const currentOutputs = getCurrentSubjectOutputs();
    if (currentImageIndex.value < currentOutputs.length - 1) {
        currentImageIndex.value++;
    }
};

const prevImage = () => {
    if (currentImageIndex.value > 0) {
        currentImageIndex.value--;
    }
};

const viewDetails = (student) => {
    // Store selected student data for progress page
    localStorage.setItem('selected_student_progress', JSON.stringify({
        student: {
            ...student,
            gradeLevel: student.gradeLevel || student.grade_level || '',
            section: student.section || '',
            classroom: student.classroom || `${student.gradeLevel || student.grade_level || ''} - ${student.section || ''}`
        },
        className: `${student.gradeLevel || student.grade_level || ''} - ${student.section || ''}`,
        timestamp: new Date().toISOString()
    }));

    // Navigate to progress page
    emit('navigate', 'TeacherProgress');
};

// Calculate total outputs (submissions) for a student
const calculateTotalOutputs = async (studentId) => {
    let totalOutputs = 0;
    try {
        for (const folder of portfolioFolders.value) {
            const activitiesResponse = await axios.get(`/api/portfolio/folders/${folder.id}/activities/`);
            const activities = activitiesResponse.data || [];

            for (const activity of activities) {
                try {
                    const submissionsResponse = await axios.get(`/api/activities/${activity.id}/submissions/`);
                    const submissions = submissionsResponse.data || [];

                    // Count only submissions from THIS student
                    const studentSubmissions = submissions.filter(sub =>
                        sub.student.id === studentId || sub.student.username === studentId
                    );
                    totalOutputs += studentSubmissions.length;

                    if (studentSubmissions.length > 0) {
                        console.log(`Activity ${activity.id}: Student ${studentId} has ${studentSubmissions.length} submission(s)`);
                    }
                } catch (error) {
                    console.error(`Error checking submissions for activity ${activity.id}:`, error);
                    showError(`Failed to check submissions for activity ${activity.id}`, 'Error');
                }
            }
        }
        console.log(`Total outputs for student ${studentId}:`, totalOutputs);
        return totalOutputs;
    } catch (error) {
        console.error('Error calculating total outputs:', error);
        showError('Failed to calculate student outputs', 'Error');
        return 0;
    }
};

// Calculate completed activities for a student
const calculateCompletedActivities = async (studentId) => {
    let completedCount = 0;
    try {
        for (const folder of portfolioFolders.value) {
            const activitiesResponse = await axios.get(`/api/portfolio/folders/${folder.id}/activities/`);
            const activities = activitiesResponse.data || [];

            for (const activity of activities) {
                try {
                    const submissionsResponse = await axios.get(`/api/activities/${activity.id}/submissions/`);
                    const submissions = submissionsResponse.data || [];

                    // Check if this student has submitted
                    const hasSubmitted = submissions.some(sub => sub.student.id === studentId || sub.student.username === studentId);
                    if (hasSubmitted) {
                        completedCount++;
                    }
                } catch (error) {
                    console.error(`Error checking submissions for activity ${activity.id}:`, error);
                    showError(`Failed to check submissions for activity ${activity.id}`, 'Error');
                }
            }
        }
        return completedCount;
    } catch (error) {
        console.error('Error calculating completed activities:', error);
        showError('Failed to calculate completed activities', 'Error');
        return 0;
    }
};

// Update student progress data
const updateStudentProgress = async () => {
    // Update each student's outputs count
    for (const student of students.value) {
        const totalOutputs = await calculateTotalOutputs(student.id);
        student.totalActivities = totalOutputs; // Store in totalActivities for display
        student.completedActivities = totalOutputs; // Keep for compatibility
        student.progress = 100; // Not used anymore but keep for compatibility
    }

    console.log('Updated student outputs:', students.value);
};

// Load portfolio folders
const loadPortfolioFolders = async () => {
    try {
        const response = await axios.get('/api/portfolio/folders/');
        if (response.data) {
            portfolioFolders.value = response.data;

            // Update subjects based on folders
            subjects.value = [
                { id: 'all', name: 'All' },
                ...response.data.map(folder => ({
                    id: folder.id.toString(),
                    name: folder.name
                }))
            ];

            console.log('Loaded portfolio folders:', portfolioFolders.value);

            // Update student progress after loading folders
            await updateStudentProgress();
        }
    } catch (error) {
        console.error('Error loading portfolio folders:', error);
        showError('Failed to load portfolio folders', 'Error');
    }
};

// Load student submissions for a specific student
const loadStudentSubmissions = async (studentId) => {
    isLoadingOutputs.value = true;
    console.log('🔍 Loading submissions for student DATABASE ID:', studentId);

    try {
        // Clear previous outputs
        studentOutputs.value = {};

        // Load all submissions in parallel for better performance
        const folderPromises = portfolioFolders.value.map(async (folder) => {
            try {
                // Get activities for this folder
                const activitiesResponse = await axios.get(`/api/portfolio/folders/${folder.id}/activities/`);
                const activities = activitiesResponse.data || [];

                // Get submissions for each activity (only published ones)
                const folderOutputs = [];
                console.log(`📁 Folder "${folder.name}" has ${activities.length} activities`);

                // Filter only published activities
                const publishedActivities = activities.filter(activity => activity.is_published === true);
                console.log(`   📌 Published activities: ${publishedActivities.length}`);

                // Load submissions in parallel for this folder
                const activityPromises = publishedActivities.map(async (activity) => {
                    try {
                        const submissionsResponse = await axios.get(`/api/activities/${activity.id}/submissions/`);
                        const submissions = submissionsResponse.data || [];

                        // Filter submissions for THIS specific student only
                        const studentSubmissions = submissions.filter(submission => {
                            let submissionStudentId = null;
                            if (submission.student) {
                                submissionStudentId = typeof submission.student === 'object' 
                                    ? submission.student.id 
                                    : submission.student;
                            } else if (submission.student_id) {
                                submissionStudentId = submission.student_id;
                            }
                            return submissionStudentId === studentId || Number(submissionStudentId) === Number(studentId);
                        });

                        // Process each submission
                        studentSubmissions.forEach(submission => {
                            // Check if submission has multiple files
                            const submissionFiles = submission.files || [];
                            console.log(`📄 Submission ${submission.id} has ${submissionFiles.length} files:`, submissionFiles);
                            
                            if (submissionFiles.length > 0) {
                                // Handle multiple files per submission
                                submissionFiles.forEach((file, fileIndex) => {
                                    const fileUrl = file.file_url || file.file_path || file.file;
                                    console.log(`   📎 File ${fileIndex + 1}: ${fileUrl}`);
                                    if (fileUrl) {
                                        folderOutputs.push({
                                            url: fileUrl,
                                            date: new Date(submission.submitted_at),
                                            title: submission.activity_title || activity.title,
                                            activity_type: submission.activity_type || activity.activity_type,
                                            caption: submission.caption,
                                            score: submission.score,
                                            total_score: submission.total_score,
                                            max_score: submission.max_score,
                                            criteria_scores: submission.criteria_scores,
                                            status: submission.status,
                                            studentName: submission.student_name || submission.student?.username,
                                            resubmit_count: submission.resubmit_count || 0,
                                            is_late: submission.is_late || false,
                                            last_resubmit_at: submission.last_resubmit_at,
                                            submitted_at: submission.submitted_at,
                                            file_type: file.file_type || 'image',
                                            file_index: fileIndex + 1,
                                            total_files: submissionFiles.length,
                                            submission_id: submission.id
                                        });
                                    }
                                });
                            } else {
                                // Single file submission (legacy)
                                const fileUrl = submission.file_url || submission.file_path;
                                if (fileUrl) {
                                    folderOutputs.push({
                                        url: fileUrl,
                                        date: new Date(submission.submitted_at),
                                        title: submission.activity_title || activity.title,
                                        activity_type: submission.activity_type || activity.activity_type,
                                        caption: submission.caption,
                                        score: submission.score,
                                        total_score: submission.total_score,
                                        max_score: submission.max_score,
                                        criteria_scores: submission.criteria_scores,
                                        status: submission.status,
                                        studentName: submission.student_name || submission.student?.username,
                                        resubmit_count: submission.resubmit_count || 0,
                                        is_late: submission.is_late || false,
                                        last_resubmit_at: submission.last_resubmit_at,
                                        submitted_at: submission.submitted_at,
                                        file_type: submission.file_type || 'image',
                                        file_index: 1,
                                        total_files: 1,
                                        submission_id: submission.id
                                    });
                                }
                            }
                        });
                    } catch (error) {
                        console.error(`Error loading submissions for activity ${activity.id}:`, error);
                    }
                });

                await Promise.all(activityPromises);

                // Store outputs by folder id
                if (folderOutputs.length > 0) {
                    return { folderId: folder.id.toString(), outputs: folderOutputs };
                }
                return null;
            } catch (error) {
                console.error(`Error loading activities for folder ${folder.id}:`, error);
                return null;
            }
        });

        // Wait for all folders to load
        const results = await Promise.all(folderPromises);
        
        // Combine results
        results.forEach(result => {
            if (result) {
                studentOutputs.value[result.folderId] = result.outputs;
                console.log(`✅ Stored ${result.outputs.length} outputs for folder ID: ${result.folderId}`);
            }
        });

        console.log('📦 Total loaded student outputs:', studentOutputs.value);
    } catch (error) {
        console.error('❌ Error loading student submissions:', error);
        showError('Failed to load student submissions', 'Error');
    } finally {
        isLoadingOutputs.value = false;
    }

};

const viewOutputs = async (student) => {
    console.log('👤 View Outputs clicked for student:', student);
    console.log('Student ID (display):', student.id);
    console.log('Student DB ID:', student.dbId);
    console.log('Student object:', JSON.stringify(student, null, 2));

    selectedStudent.value = student;
    currentImageIndex.value = 0; // Reset to first image
    selectedSubject.value = 'all'; // Reset to 'All' subject
    isMinimizedView.value = true; // Start with minimized view
    expandedImageIndex.value = null; // Reset expanded image
    showOutputsDialog.value = true;

    // Load student submissions using database ID, not display ID
    await loadStudentSubmissions(student.dbId || student.id);
};

// Load students from API
const loadStudents = async () => {
    try {
        // Get class context from localStorage (set by Room.vue)
        const classContext = localStorage.getItem('progress_class_context');
        let classParam = '';

        if (classContext) {
            try {
                const context = JSON.parse(classContext);
                if (context.className) {
                    classParam = `?class=${encodeURIComponent(context.className)}`;
                    console.log('Loading students for class:', context.className);
                }
            } catch (e) {
                console.error('Error parsing class context:', e);
            }
        }

        const response = await axios.get(`/api/students/progress/${classParam}`);
        if (response.data) {
            students.value = response.data.map(student => ({
                id: student.student_id,
                dbId: student.id, // Store database ID for API calls
                name: student.name,
                initial: student.name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2),
                username: student.username,
                email: student.email,
                profile_picture: student.profile_picture || null,
                totalActivities: student.total_outputs,
                completedActivities: student.scored_outputs,
                progress: student.total_outputs > 0
                    ? Math.round((student.scored_outputs / student.total_outputs) * 100)
                    : 0,
                averageScore: student.average_score,
                classroom: student.classroom || 'N/A',
                gradeLevel: student.grade_level || '',
                section: student.section || '',
                teacher: student.teacher || ''
            }));
            // Reset pagination when loading new data
            visibleStudentCount.value = 10;
            console.log('Loaded students:', students.value);
        }
    } catch (error) {
        console.error('Error loading students:', error);
        showError('Failed to load students', 'Error');
    }
};

// Function to handle class change event
const handleClassChange = (event) => {
    console.log('🔄 Class changed in Sprogress, clearing view state and navigating...', event.detail);

    // Clear the teacher view state so Room shows folders view
    localStorage.removeItem('teacher_current_view');

    // Navigate back to TeacherRoom when class is changed
    emit('navigate', 'TeacherRoom');
};

// Load folders on mount
onMounted(() => {
    loadClassName();
    loadStudents();
    loadPortfolioFolders();

    // Listen for class change events
    window.addEventListener('classChanged', handleClassChange);

    // Listen for click outside to close dropdown
    document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
    // Clean up event listener
    window.removeEventListener('classChanged', handleClassChange);
    document.removeEventListener('click', handleClickOutside);
});

// Watch for subject changes and reset view state
watch(selectedSubject, () => {
    currentImageIndex.value = 0;
    isMinimizedView.value = true;
    expandedImageIndex.value = null;
});

const closeOutputsDialog = () => {
    showOutputsDialog.value = false;
};

// Navigate back to Room page (same as Outputs.vue)
const goBackToRoom = () => {
    // Get class context from localStorage
    const classContext = localStorage.getItem('progress_class_context');
    console.log('Going back with class context:', classContext);

    if (classContext) {
        try {
            const context = JSON.parse(classContext);
            // Use the subject (folder name) that was saved, NOT the className
            if (context.subject) {
                // Store return context (same format as Outputs.vue)
                const returnData = {
                    subject: context.subject,  // This is the folder name like "aaa"
                    showActivities: true,
                    timestamp: Date.now()  // Add timestamp to expire after 5 seconds
                };
                console.log('Storing return context:', returnData);
                localStorage.setItem('return_to_activities', JSON.stringify(returnData));
            }
        } catch (e) {
            console.error('Error:', e);
        }
    }

    emit('navigate', 'TeacherRoom');
};
</script>

<style>
/* Transition animations for dialog */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
