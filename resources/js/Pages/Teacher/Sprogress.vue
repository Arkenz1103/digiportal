<template>
    <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-violet-50 to-blue-50">
        <!-- Class Header -->
        <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-6 md:p-4 shadow-lg rounded-b-3xl">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div class="space-y-3">
                    <h1 class="text-xl md:text-2xl font-bold text-white px-4 py-2 md:px-6 md:py-3 rounded-lg inline-block bg-white/20">
                        Grade 1 - A
                    </h1>
                    <p class="text-white/90 ml-2 flex items-center gap-2">
                        <i class="pi pi-user"></i>
                        Teacher: {{ auth.user.name }}
                    </p>
                </div>
                <div>
                    <button 
                        @click="router.visit('/teacher/class/grade1-a')"
                        class="flex items-center gap-2 px-4 py-2 bg-white/20 text-white hover:bg-white/30 rounded-lg transition-all">
                        <i class="pi pi-arrow-left"></i>
                        <span>Back to Folder</span>
                    </button>
                </div>
            </div>
            
            <!-- Page Title -->
            <div class="mt-6 md:mt-8">
                <h2 class="text-2xl md:text-3xl font-bold text-white">Student Progress Tracking</h2>
            </div>
        </div>

        <!-- Main Content -->
        <div class="p-6">
            <!-- Search Section -->
            <div class="mb-8">
                <div class="relative max-w-md">
                    <input type="text" placeholder="Search students..." 
                        class="w-full pl-10 pr-4 py-2 rounded-lg border border-indigo-200 focus:border-indigo-500 focus:ring focus:ring-indigo-200 transition-all duration-200 bg-white"
                    />
                    <div class="absolute left-3 top-1/2 -translate-y-1/2 text-indigo-500">
                        <i class="pi pi-search"></i>
                    </div>
                </div>
            </div>

            <!-- Student List Section -->
            <div class="bg-white/80 backdrop-blur-sm rounded-xl shadow-sm overflow-hidden border border-indigo-100">
                <!-- Table Header -->
                <div class="flex items-center px-6 py-4 bg-indigo-50 border-b border-indigo-100">
                    <div class="w-12 text-sm font-semibold text-indigo-900">#</div>
                    <div class="w-48 text-sm font-semibold text-indigo-900">Student Name</div>
                    <div class="w-32 text-sm font-semibold text-indigo-900">ID</div>
                    <div class="w-80 text-sm font-semibold text-indigo-900">Outputs</div>
                    <div class="w-56 text-sm font-semibold text-indigo-900">Outputs List</div>
                    <div class="flex-1 text-sm font-semibold text-indigo-900 text-right pr-12">Progress Records</div>
                </div>

                <!-- Student Items -->
                <div v-for="(student, index) in students" :key="student.id" 
                    class="group flex items-center px-6 py-5 hover:bg-indigo-50 border-b border-indigo-100 transition-all duration-200">
                    <div class="w-12 text-gray-500 font-medium">{{ index + 1 }}</div>
                    <div class="w-48 flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-600 to-violet-600 flex items-center justify-center">
                            <span class="text-white font-medium">{{ student.initial }}</span>
                        </div>
                        <span class="font-medium text-indigo-900 group-hover:text-indigo-700 transition-colors">{{ student.name }}</span>
                    </div>
                    <div class="w-32">
                        <span class="text-indigo-700 font-medium">{{ student.id }}</span>
                    </div>
                    <div class="w-80">
                        <span class="text-2xl font-bold text-indigo-700">{{ student.totalActivities }}</span>
                    </div>
                    <div class="w-56">
                        <button 
                            class="px-4 py-2 rounded-lg bg-indigo-100 text-indigo-700 font-medium hover:bg-indigo-600 hover:text-white transition-colors duration-200"
                            @click="viewOutputs(student)">
                            <span class="flex items-center gap-2">
                                <i class="pi pi-list"></i>
                                View Outputs
                            </span>
                        </button>
                    </div>
                    <div class="flex-1 text-right pr-12">
                        <button 
                            class="px-4 py-2 rounded-lg bg-indigo-100 text-indigo-700 font-medium hover:bg-indigo-600 hover:text-white transition-colors duration-200"
                            @click="viewDetails(student)">
                            <span class="flex items-center gap-2">
                                <i class="pi pi-chart-line"></i>
                                View Details
                            </span>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Outputs Dialog -->
        <Teleport to="body">
            <Transition name="fade">
                <div v-if="showOutputsDialog" class="absolute inset-0 bg-black/50 flex items-center justify-center z-50" @click="closeOutputsDialog">
                    <div class="relative bg-white rounded-xl shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden border border-indigo-100" @click.stop>
                        <!-- Dialog Header -->
                        <div class="flex items-center justify-between p-4 border-b border-indigo-100 bg-indigo-50">
                            <h3 class="text-xl font-bold text-indigo-900">{{ selectedStudent?.name }}'s Outputs</h3>
                            <button @click="closeOutputsDialog" class="p-2 rounded-full hover:bg-indigo-100 text-indigo-600 transition-colors">
                                <i class="pi pi-times"></i>
                            </button>
                        </div>
                        
                        <!-- Dialog Content -->
                        <div class="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
                            <!-- Loading State -->
                            <div v-if="isLoadingOutputs" class="flex justify-center items-center py-12">
                                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                            </div>
                            
                            <div v-else class="flex flex-col items-center">
                                <!-- Subject Tabs -->
                                <div class="w-full max-w-2xl mb-6">
                                    <div class="flex space-x-1 bg-indigo-100 p-1 rounded-lg">
                                        <button 
                                            v-for="subject in subjects" 
                                            :key="subject.id"
                                            @click="selectedSubject = subject.id"
                                            class="flex-1 px-4 py-2 rounded-md text-sm font-medium transition-all duration-200"
                                            :class="selectedSubject === subject.id 
                                                ? 'bg-white text-indigo-700 shadow-sm' 
                                                : 'text-indigo-600 hover:text-indigo-800 hover:bg-indigo-50'">
                                            {{ subject.name }}
                                        </button>
                                    </div>
                                </div>
                                
                                <!-- Image Gallery with Navigation -->
                                <div class="relative w-full max-w-2xl">
                                    <!-- Minimized View (Grid of thumbnails) -->
                                    <div v-if="isMinimizedView" class="grid grid-cols-3 gap-4">
                                        <div 
                                            v-for="(output, index) in getCurrentSubjectOutputs()" 
                                            :key="index"
                                            @click="expandImage(index)"
                                            class="relative group cursor-pointer bg-gray-100 rounded-lg overflow-hidden aspect-square hover:shadow-lg transition-all duration-200">
                                            <img 
                                                :src="output.url || output" 
                                                :alt="output.title || `Output ${index + 1}`"
                                                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                                            >
                                            <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-200 flex items-center justify-center">
                                                <div class="text-white opacity-0 group-hover:opacity-100 transition-opacity duration-200 text-center">
                                                    <i class="pi pi-expand text-2xl mb-1"></i>
                                                    <p class="text-xs font-medium">{{ output.title || `Output ${index + 1}` }}</p>
                                                    <p class="text-xs opacity-75">{{ output.subject ? output.subject.charAt(0).toUpperCase() + output.subject.slice(1) : selectedSubject }}</p>
                                                </div>
                                            </div>
                                            <!-- Date badge -->
                                            <div class="absolute top-2 right-2 bg-white/90 px-2 py-1 rounded text-xs font-medium text-gray-700">
                                                {{ output.date ? new Date(output.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '' }}
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <!-- Expanded View (Single full-size image) -->
                                    <div v-else class="flex items-center justify-center bg-gray-100 rounded-lg p-4 min-h-[400px]">
                                        <div class="relative">
                                            <img 
                                                :src="currentImage.url || currentImage" 
                                                :alt="currentImage.title || 'Student output'" 
                                                class="max-w-full h-auto max-h-[70vh] rounded shadow-md"
                                            >
                                            <div class="absolute top-2 right-2 bg-white/80 px-2 py-1 rounded text-sm font-medium">
                                                {{ currentImageIndex + 1 }}/{{ getCurrentSubjectOutputs().length }}
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
                                            class="px-4 py-2 bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200 transition-colors duration-200 flex items-center gap-2 mx-auto">
                                            <i class="pi pi-th-large"></i>
                                            <span>Back to Grid View</span>
                                        </button>
                                    </div>
                                </div>
                                
                                <!-- Image Details (only show in expanded view) -->
                                <div v-if="!isMinimizedView" class="mt-6 w-full">
                                    <div class="flex justify-between items-center mb-2">
                                        <h4 class="font-semibold text-lg text-indigo-900">Assignment Details</h4>
                                    </div>
                                    <div class="bg-indigo-50 p-4 rounded-lg border border-indigo-100">
                                        <div class="grid grid-cols-2 gap-4">
                                            <div>
                                                <p class="text-sm text-gray-500">Assignment</p>
                                                <p class="font-medium">{{ getCurrentAssignment().title }}</p>
                                            </div>
                                            <div>
                                                <p class="text-sm text-gray-500">Submitted</p>
                                                <p class="font-medium">{{ getCurrentAssignment().date }}</p>
                                            </div>
                                            <div>
                                                <p class="text-sm text-gray-500">Score</p>
                                                <p class="font-medium">{{ getCurrentAssignment().score }}</p>
                                            </div>
                                            <div>
                                                <p class="text-sm text-gray-500">Status</p>
                                                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" 
                                                      :class="getCurrentAssignment().status === 'Graded' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'">
                                                    {{ getCurrentAssignment().status }}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Dialog Footer -->
                        <div class="p-4 border-t border-indigo-100 flex justify-end">
                            <button 
                                @click="closeOutputsDialog"
                                class="px-4 py-2 rounded-lg bg-indigo-100 text-indigo-700 font-medium hover:bg-indigo-200 transition-colors duration-200">
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            </Transition>
        </Teleport>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import axios from 'axios';

// Define emits for navigation
const emit = defineEmits(['navigate']);

// Mock user data
const currentUser = ref({
    name: 'Teacher Name',
    email: 'teacher@example.com',
    role: 'teacher'
});

const auth = computed(() => ({
    user: currentUser.value
}));

// Sample student data
const students = ref([
    {
        id: 'STD001',
        name: 'John Smith',
        initial: 'JS',
        progress: 85,
        completedActivities: 8,
        totalActivities: 15
    },
    {
        id: 'STD002',
        name: 'Maria Garcia',
        initial: 'EW',
        progress: 92,
        completedActivities: 12,
        totalActivities: 15
    },
    {
        id: 'STD003',
        name: 'James Wilson',
        initial: 'MB',
        progress: 78,
        completedActivities: 7,
        totalActivities: 15
    },
]);

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
    if (selectedSubject.value === 'all') {
        return allAssignments.value[currentImageIndex.value] || 
               { title: 'Assignment', date: 'N/A', score: 'N/A', status: 'N/A', description: 'No description available' };
    }
    const subjectAssignments = assignments.value[selectedSubject.value] || [];
    return subjectAssignments[currentImageIndex.value] || 
           { title: 'Assignment', date: 'N/A', score: 'N/A', status: 'N/A', description: 'No description available' };
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
        student: student,
        className: 'Grade 1 - A', // You can make this dynamic based on current class
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
                    
                    console.log(`Activity ${activity.id} submissions:`, submissions);
                    
                    // Count all submissions (not filtered by student for now to see total)
                    totalOutputs += submissions.length;
                } catch (error) {
                    console.error(`Error checking submissions for activity ${activity.id}:`, error);
                }
            }
        }
        console.log(`Total outputs for student ${studentId}:`, totalOutputs);
        return totalOutputs;
    } catch (error) {
        console.error('Error calculating total outputs:', error);
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
                }
            }
        }
        return completedCount;
    } catch (error) {
        console.error('Error calculating completed activities:', error);
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
    }
};

// Load student submissions for a specific student
const loadStudentSubmissions = async (studentId) => {
    isLoadingOutputs.value = true;
    try {
        // Clear previous outputs
        studentOutputs.value = {};
        
        // Load submissions for each folder
        for (const folder of portfolioFolders.value) {
            try {
                // Get activities for this folder
                const activitiesResponse = await axios.get(`/api/portfolio/folders/${folder.id}/activities/`);
                const activities = activitiesResponse.data || [];
                
                // Get submissions for each activity
                const folderOutputs = [];
                for (const activity of activities) {
                    try {
                        const submissionsResponse = await axios.get(`/api/activities/${activity.id}/submissions/`);
                        const submissions = submissionsResponse.data || [];
                        
                        // Add all submissions to outputs (showing all student work)
                        submissions.forEach(submission => {
                            if (submission.file_type === 'image' && submission.file_path) {
                                folderOutputs.push({
                                    url: submission.file_path,
                                    date: new Date(submission.submitted_at),
                                    title: activity.title,
                                    activityType: activity.activity_type,
                                    caption: submission.caption,
                                    score: submission.score,
                                    status: submission.status,
                                    studentName: submission.student_name || submission.student?.username
                                });
                            }
                        });
                        
                        console.log(`Activity ${activity.id} - ${activity.title}: ${submissions.length} submissions`);
                    } catch (error) {
                        console.error(`Error loading submissions for activity ${activity.id}:`, error);
                    }
                }
                
                // Store outputs by folder id
                if (folderOutputs.length > 0) {
                    studentOutputs.value[folder.id.toString()] = folderOutputs;
                }
            } catch (error) {
                console.error(`Error loading activities for folder ${folder.id}:`, error);
            }
        }
        
        console.log('Loaded student outputs:', studentOutputs.value);
    } catch (error) {
        console.error('Error loading student submissions:', error);
    } finally {
        isLoadingOutputs.value = false;
    }
};

const viewOutputs = async (student) => {
    selectedStudent.value = student;
    currentImageIndex.value = 0; // Reset to first image
    selectedSubject.value = 'all'; // Reset to 'All' subject
    isMinimizedView.value = true; // Start with minimized view
    expandedImageIndex.value = null; // Reset expanded image
    showOutputsDialog.value = true;
    
    // Load student submissions
    await loadStudentSubmissions(student.id);
};

// Load folders on mount
onMounted(() => {
    loadPortfolioFolders();
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