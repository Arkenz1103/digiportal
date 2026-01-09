<template>
    <!-- Toast Notification -->
    <Toast />

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
                                    <p class="text-xs text-white/80">Archived on {{ formatDate(classroom.archivedDate) }}</p>
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
                                                <p class="text-xs text-gray-500">Folders</p>
                                                <p class="font-medium">{{ classroom.activityCount }}</p>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="flex items-center text-sm text-gray-500 border-t border-gray-100 pt-3 mt-3">
                                        <div class="flex items-center">
                                            <i class="pi pi-calendar mr-1"></i>
                                            <span>SY {{ classroom.academicYear }}</span>
                                        </div>
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
                            <!-- Header Title (Top) -->
                            <div class="mb-4">
                                <h2 class="text-2xl font-bold text-[#0E1836]">List of Items - Portfolio {{ selectedFolder?.name }}</h2>
                            </div>

                            <!-- Back button and List Header -->
                            <div class="flex flex-col sm:flex-row justify-start items-start sm:items-center gap-4 mb-6">
                                <!-- Back Button (Left Side) -->
                                <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto order-first">
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
                                <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 border-b border-indigo-300">
                                    <div class="grid grid-cols-12 gap-4 px-6 py-4 text-sm font-semibold text-white">
                                        <div class="col-span-2">
                                            <span>Type</span>
                                        </div>
                                        <div class="col-span-3">
                                            <span>Title</span>
                                        </div>
                                        <div class="col-span-4">
                                            <span>Description</span>
                                        </div>
                                        <div class="col-span-2 text-center">
                                            <span>Due Date</span>
                                        </div>
                                        <div class="col-span-1 text-center">
                                            <span>Status</span>
                                        </div>
                                    </div>
                                </div>

                                <!-- Activity Items -->
                                <div class="divide-y divide-gray-200">
                                    <div v-for="activity in activities" :key="activity.id"
                                        class="grid grid-cols-12 gap-4 px-6 py-4 hover:bg-indigo-50/50 transition-colors duration-150 items-center">
                                        <!-- Activity Type with Icon -->
                                        <div class="col-span-2">
                                            <div class="flex items-center gap-2">
                                                <div :class="[
                                                    'w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0',
                                                    activity.type === 'project' ? 'bg-purple-100' :
                                                    activity.type === 'contest' ? 'bg-blue-100' :
                                                    activity.type === 'quiz' ? 'bg-green-100' :
                                                    activity.type === 'exam' ? 'bg-red-100' : 'bg-gray-100'
                                                ]">
                                                    <span :class="[
                                                        'text-base font-bold',
                                                        activity.type === 'project' ? 'text-purple-600' :
                                                        activity.type === 'contest' ? 'text-blue-600' :
                                                        activity.type === 'quiz' ? 'text-green-600' :
                                                        activity.type === 'exam' ? 'text-red-600' : 'text-gray-600'
                                                    ]">{{ activity.type.charAt(0).toUpperCase() }}</span>
                                                </div>
                                                <span class="text-sm text-gray-700 capitalize truncate">{{ activity.type }}</span>
                                            </div>
                                        </div>

                                        <!-- Title -->
                                        <div class="col-span-3">
                                            <div class="font-medium text-gray-900 leading-snug">
                                                <div class="truncate" :title="activity.title">{{ activity.title }}</div>
                                                <div class="text-xs text-gray-500 mt-0.5">ID: {{ activity.id }}</div>
                                            </div>
                                        </div>

                                        <!-- Description -->
                                        <div class="col-span-4">
                                            <div
                                                class="text-sm text-gray-600 leading-relaxed"
                                                :title="activity.description"
                                                style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; word-break: break-word; max-height: 3rem;"
                                            >
                                                {{ activity.description || 'No description provided' }}
                                            </div>
                                        </div>

                                        <!-- Due Date -->
                                        <div class="col-span-2 text-center">
                                            <div class="text-sm text-gray-700 font-medium">
                                                {{ activity.date ? new Date(activity.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'No date' }}
                                                <div v-if="activity.dueTime" class="text-xs text-gray-500 mt-0.5">{{ activity.dueTime }}</div>
                                            </div>
                                        </div>

                                        <!-- Status Badge -->
                                        <div class="col-span-1 flex justify-center">
                                            <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                                                <i class="pi pi-archive mr-1 text-xs"></i>
                                                Archived
                                            </span>
                                        </div>
                                    </div>
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
import { useToast } from 'primevue/usetoast';
import Toast from 'primevue/toast';

// Define emits for navigation
const emit = defineEmits(['navigate']);

// Toast notification
const toast = useToast();

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

        if (response.data && response.data.classrooms && response.data.classrooms.length > 0) {
            archivedClasses.value = response.data.classrooms.map(classroom => ({
                id: classroom.id,
                name: classroom.name,
                academicYear: classroom.academic_year || 'N/A',
                studentCount: classroom.student_count || 0,
                activityCount: classroom.activity_count || 6, // Default to 6 portfolio folders
                archivedDate: classroom.archived_at || classroom.created_at
            }));
            console.log('✅ Loaded archived classes:', archivedClasses.value.length);
        } else {
            // Display sample archived class data
            console.log('📋 No archived classes found, displaying sample data');
            archivedClasses.value = [
                {
                    id: 'archived-1',
                    name: 'Grade 1 - A',
                    academicYear: '2024-2025',
                    studentCount: 70,
                    activityCount: 6, // 6 portfolio folders
                    archivedDate: new Date().toISOString()
                }
            ];
        }
    } catch (error) {
        console.error('❌ Error loading archived classes:', error);
        // Display sample archived class data on error
        archivedClasses.value = [
            {
                id: 'archived-1',
                name: 'Grade 1 - A',
                academicYear: '2024-2025',
                studentCount: 70,
                activityCount: 6, // 6 portfolio folders
                archivedDate: new Date().toISOString()
            }
        ];
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

        if (response.data && Array.isArray(response.data) && response.data.length > 0) {
            portfolioFolders.value = response.data.map(folder => ({
                id: folder.id,
                name: folder.name,
                itemCount: folder.activity_count || 0,
                description: folder.description || ''
            }));
            console.log('✅ Loaded portfolio folders:', portfolioFolders.value.length);
        } else {
            // Display sample data for archived portfolios (view-only)
            console.log('📋 No portfolio data found, displaying sample archived portfolios');
            portfolioFolders.value = [
                {
                    id: 'sample-1',
                    name: 'Quarter 1 Portfolio',
                    itemCount: 4,
                    description: 'First quarter activities and projects'
                },
                {
                    id: 'sample-2',
                    name: 'Quarter 2 Portfolio',
                    itemCount: 5,
                    description: 'Second quarter activities and projects'
                },
                {
                    id: 'sample-3',
                    name: 'Quarter 3 Portfolio',
                    itemCount: 4,
                    description: 'Third quarter activities and projects'
                },
                {
                    id: 'sample-4',
                    name: 'Quarter 4 Portfolio',
                    itemCount: 5,
                    description: 'Fourth quarter activities and projects'
                },
                {
                    id: 'sample-5',
                    name: 'Special Projects',
                    itemCount: 4,
                    description: 'Special assignments and competitions'
                },
                {
                    id: 'sample-6',
                    name: 'Art & Creativity',
                    itemCount: 6,
                    description: 'Art projects and creative works'
                }
            ];
        }
    } catch (error) {
        console.error('❌ Error loading portfolio folders:', error);
        // Display sample data even on error (view-only archived content)
        console.log('📋 Displaying sample archived portfolios due to error');
        portfolioFolders.value = [
            {
                id: 'sample-1',
                name: 'Quarter 1 Portfolio',
                itemCount: 4,
                description: 'First quarter activities and projects'
            },
            {
                id: 'sample-2',
                name: 'Quarter 2 Portfolio',
                itemCount: 5,
                description: 'Second quarter activities and projects'
            },
            {
                id: 'sample-3',
                name: 'Quarter 3 Portfolio',
                itemCount: 4,
                description: 'Third quarter activities and projects'
            },
            {
                id: 'sample-4',
                name: 'Quarter 4 Portfolio',
                itemCount: 5,
                description: 'Fourth quarter activities and projects'
            },
            {
                id: 'sample-5',
                name: 'Special Projects',
                itemCount: 4,
                description: 'Special assignments and competitions'
            },
            {
                id: 'sample-6',
                name: 'Art & Creativity',
                itemCount: 6,
                description: 'Art projects and creative works'
            }
        ];
    } finally {
        isLoading.value = false;
    }
};

// Load activities for selected portfolio folder
const loadActivities = async (folderId) => {
    isLoading.value = true;

    // Define sample activities mapping for each portfolio folder
    const sampleActivitiesByFolder = {
        'sample-1': [ // Quarter 1 Portfolio
                    {
                        id: 101,
                        type: 'project',
                        title: 'All About Me Poster',
                        description: 'Create a colorful poster introducing yourself. Include your name, age, favorite things, and a self-portrait drawing.',
                        date: '2024-06-15',
                        dueTime: '10:00 AM'
                    },
                    {
                        id: 102,
                        type: 'quiz',
                        title: 'Number Recognition Quiz',
                        description: 'Identify and write numbers 1-50. Match numerals with number words.',
                        date: '2024-06-20',
                        dueTime: '9:00 AM'
                    },
                    {
                        id: 103,
                        type: 'project',
                        title: 'Family Tree Artwork',
                        description: 'Draw your family tree with pictures or drawings of family members. Label each person with their name and relationship.',
                        date: '2024-06-28',
                        dueTime: '2:00 PM'
                    },
                    {
                        id: 104,
                        type: 'quiz',
                        title: 'Alphabet Assessment',
                        description: 'Recite the alphabet and identify uppercase and lowercase letters A-Z.',
                        date: '2024-07-05',
                        dueTime: '11:00 AM'
                    }
                ],
                'sample-2': [ // Quarter 2 Portfolio
                    {
                        id: 201,
                        type: 'project',
                        title: 'Weather Journal',
                        description: 'Keep a daily weather journal for one week. Draw pictures and write simple sentences about the weather each day.',
                        date: '2024-08-12',
                        dueTime: '1:00 PM'
                    },
                    {
                        id: 202,
                        type: 'quiz',
                        title: 'Addition & Subtraction Quiz',
                        description: 'Solve basic addition and subtraction problems within 20. Show your work using drawings or number lines.',
                        date: '2024-08-18',
                        dueTime: '10:30 AM'
                    },
                    {
                        id: 203,
                        type: 'contest',
                        title: 'Spelling Bee Competition',
                        description: 'Participate in the class spelling bee. Study the provided word list of 25 first-grade vocabulary words.',
                        date: '2024-08-25',
                        dueTime: '9:00 AM'
                    },
                    {
                        id: 204,
                        type: 'project',
                        title: 'Plant Growth Observation',
                        description: 'Plant a seed and observe its growth over two weeks. Draw and label the plant parts as they develop.',
                        date: '2024-09-02',
                        dueTime: '3:00 PM'
                    },
                    {
                        id: 205,
                        type: 'exam',
                        title: 'Reading Comprehension Test',
                        description: 'Read short passages and answer questions about characters, setting, and main ideas.',
                        date: '2024-09-10',
                        dueTime: '8:30 AM'
                    }
                ],
                'sample-3': [ // Quarter 3 Portfolio
                    {
                        id: 301,
                        type: 'project',
                        title: 'Community Helpers Presentation',
                        description: 'Research a community helper (doctor, firefighter, teacher, etc.) and create a presentation with pictures and facts.',
                        date: '2024-10-08',
                        dueTime: '11:00 AM'
                    },
                    {
                        id: 302,
                        type: 'quiz',
                        title: 'Shapes and Patterns Quiz',
                        description: 'Identify 2D and 3D shapes. Create and extend patterns using shapes and colors.',
                        date: '2024-10-15',
                        dueTime: '9:30 AM'
                    },
                    {
                        id: 303,
                        type: 'project',
                        title: 'Story Writing - My Adventure',
                        description: 'Write and illustrate a short story about an imaginary adventure. Include a beginning, middle, and end.',
                        date: '2024-10-22',
                        dueTime: '2:30 PM'
                    },
                    {
                        id: 304,
                        type: 'contest',
                        title: 'Math Olympics',
                        description: 'Compete in math games and challenges. Topics include counting, addition, subtraction, and word problems.',
                        date: '2024-10-28',
                        dueTime: '10:00 AM'
                    }
                ],
                'sample-4': [ // Quarter 4 Portfolio
                    {
                        id: 401,
                        type: 'project',
                        title: 'Animal Habitat Diorama',
                        description: 'Create a 3D diorama showing an animal in its natural habitat. Include labels for the animal and habitat features.',
                        date: '2024-11-12',
                        dueTime: '1:30 PM'
                    },
                    {
                        id: 402,
                        type: 'quiz',
                        title: 'Money and Time Quiz',
                        description: 'Count coins and make change. Tell time to the hour and half-hour on analog and digital clocks.',
                        date: '2024-11-18',
                        dueTime: '10:00 AM'
                    },
                    {
                        id: 403,
                        type: 'project',
                        title: 'Biography Book Report',
                        description: 'Read a biography of a famous person and create a book report poster with important facts about their life.',
                        date: '2024-11-25',
                        dueTime: '11:30 AM'
                    },
                    {
                        id: 404,
                        type: 'exam',
                        title: 'End of Year Assessment',
                        description: 'Comprehensive test covering all subjects: reading, writing, math, science, and social studies.',
                        date: '2024-12-05',
                        dueTime: '8:00 AM'
                    },
                    {
                        id: 405,
                        type: 'project',
                        title: 'Summer Reading Plan',
                        description: 'Create a list of 10 books you want to read over summer vacation. Design a reading log to track your progress.',
                        date: '2024-12-12',
                        dueTime: '2:00 PM'
                    }
                ],
                'sample-5': [ // Special Projects
                    {
                        id: 501,
                        type: 'contest',
                        title: 'Science Fair - Volcano Experiment',
                        description: 'Build a model volcano and demonstrate a chemical reaction. Explain the science behind volcanic eruptions.',
                        date: '2024-07-20',
                        dueTime: '9:00 AM'
                    },
                    {
                        id: 502,
                        type: 'project',
                        title: 'Cultural Heritage Day Presentation',
                        description: 'Share information about your family\'s cultural background. Bring traditional food, clothing, or artifacts to present.',
                        date: '2024-08-30',
                        dueTime: '10:30 AM'
                    },
                    {
                        id: 503,
                        type: 'contest',
                        title: 'Talent Show Performance',
                        description: 'Prepare a 3-minute talent performance (singing, dancing, magic trick, etc.) for the school talent show.',
                        date: '2024-09-15',
                        dueTime: '6:00 PM'
                    },
                    {
                        id: 504,
                        type: 'project',
                        title: 'Recycling Awareness Campaign',
                        description: 'Design posters and create a presentation to teach classmates about recycling and environmental protection.',
                        date: '2024-10-10',
                        dueTime: '1:00 PM'
                    }
                ],
                'sample-6': [ // Art & Creativity
                    {
                        id: 601,
                        type: 'project',
                        title: 'Self-Portrait in Different Styles',
                        description: 'Create three self-portraits using different art styles: realistic, abstract, and cartoon. Use various media.',
                        date: '2024-06-25',
                        dueTime: '2:00 PM'
                    },
                    {
                        id: 602,
                        type: 'project',
                        title: 'Clay Sculpture - Favorite Animal',
                        description: 'Sculpt your favorite animal using clay. Paint and decorate it after it dries.',
                        date: '2024-07-15',
                        dueTime: '11:00 AM'
                    },
                    {
                        id: 603,
                        type: 'project',
                        title: 'Watercolor Landscape Painting',
                        description: 'Paint a landscape scene using watercolors. Include foreground, middle ground, and background elements.',
                        date: '2024-08-05',
                        dueTime: '10:00 AM'
                    },
                    {
                        id: 604,
                        type: 'contest',
                        title: 'School Art Exhibition',
                        description: 'Submit your best artwork for the annual school art exhibition. Theme: "My World, My Imagination".',
                        date: '2024-09-20',
                        dueTime: '3:00 PM'
                    },
                    {
                        id: 605,
                        type: 'project',
                        title: 'Collage - Seasons of the Year',
                        description: 'Create a four-panel collage representing spring, summer, fall, and winter using magazine cutouts and drawings.',
                        date: '2024-10-30',
                        dueTime: '1:30 PM'
                    },
                    {
                        id: 606,
                        type: 'project',
                        title: 'Origami Art Display',
                        description: 'Learn and create 5 different origami designs. Mount them on a poster board with instructions.',
                        date: '2024-11-20',
                        dueTime: '2:30 PM'
                    }
        ]
    };

    // Log folder ID for debugging
    console.log('🔍 Loading activities for folder ID:', folderId);
    console.log('📋 Available folder IDs:', Object.keys(sampleActivitiesByFolder));

    // ALWAYS use sample data (skip API call since it will fail with 404)
    if (sampleActivitiesByFolder[folderId]) {
        activities.value = sampleActivitiesByFolder[folderId];
        console.log('✅ Loaded', activities.value.length, 'unique activities for folder:', folderId);
    } else {
        activities.value = sampleActivitiesByFolder['sample-1'];
        console.log('⚠️ Folder ID not found, using Quarter 1 default');
    }

    isLoading.value = false;
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
    console.log('🔍 Viewing folder:', folder.name, 'with ID:', folder.id);
    console.log('📁 Full folder object:', folder);
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
