<template>
    <!-- Toast Notification -->
    <Toast />
    
    <!-- Submission View Dialog -->
    <Dialog v-model:visible="showSubmissionDialog" modal :style="{ width: '90vw', maxWidth: '800px' }" :dismissableMask="true">
        <template #header>
            <div class="flex items-center gap-3">
                <div :class="[
                    'w-10 h-10 rounded-lg flex items-center justify-center',
                    selectedSubmission?.type === 'Project' ? 'bg-purple-100' : 
                    selectedSubmission?.type === 'Contest' ? 'bg-blue-100' : 
                    selectedSubmission?.type === 'Quiz' ? 'bg-green-100' : 
                    selectedSubmission?.type === 'Exam' ? 'bg-red-100' : 'bg-gray-100'
                ]">
                    <span :class="[
                        'text-xl font-bold',
                        selectedSubmission?.type === 'Project' ? 'text-purple-600' : 
                        selectedSubmission?.type === 'Contest' ? 'text-blue-600' : 
                        selectedSubmission?.type === 'Quiz' ? 'text-green-600' : 
                        selectedSubmission?.type === 'Exam' ? 'text-red-600' : 'text-gray-600'
                    ]">{{ selectedSubmission?.type?.charAt(0) }}</span>
                </div>
                <div>
                    <h3 class="text-lg font-bold text-gray-800">{{ selectedSubmission?.title }}</h3>
                    <p class="text-sm text-gray-500">ID: {{ selectedSubmission?.id }}</p>
                </div>
            </div>
        </template>

        <div class="space-y-6 py-4" v-if="selectedSubmission">
            <!-- Activity Details -->
            <div class="bg-gray-50 rounded-lg p-4">
                <h4 class="font-semibold text-gray-800 mb-2">Activity Details</h4>
                <p class="text-sm text-gray-600">{{ selectedSubmission.description }}</p>
                <div class="flex items-center gap-4 mt-3 text-sm">
                    <span class="text-gray-500">
                        <i class="pi pi-calendar mr-1"></i>
                        Due: {{ selectedSubmission.date }} {{ selectedSubmission.time }}
                    </span>
                    <span :class="[
                        'px-2 py-1 rounded-full text-xs font-medium',
                        selectedSubmission.submission.status === 'Scored' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                    ]">
                        {{ selectedSubmission.submission.status }}
                    </span>
                </div>
            </div>

            <!-- Submission Info -->
            <div class="border-t pt-4">
                <h4 class="font-semibold text-gray-800 mb-3">Your Submission</h4>
                
                <!-- Submission Date & Time -->
                <div class="grid grid-cols-2 gap-4 mb-4">
                    <div>
                        <p class="text-xs text-gray-500 mb-1">Submitted On</p>
                        <p class="text-sm font-medium text-gray-800">{{ selectedSubmission.submission.submittedDate }}</p>
                        <p class="text-xs text-gray-500">{{ selectedSubmission.submission.submittedTime }}</p>
                    </div>
                    <div v-if="selectedSubmission.submission.score">
                        <p class="text-xs text-gray-500 mb-1">Score</p>
                        <p class="text-2xl font-bold text-indigo-600">{{ selectedSubmission.submission.score }}/{{ selectedSubmission.submission.maxScore }}</p>
                    </div>
                </div>

                <!-- Caption -->
                <div class="mb-4" v-if="selectedSubmission.submission.caption">
                    <p class="text-xs text-gray-500 mb-1">Caption</p>
                    <p class="text-sm text-gray-700 bg-gray-50 rounded p-3">{{ selectedSubmission.submission.caption }}</p>
                </div>

                <!-- Attached Files -->
                <div v-if="selectedSubmission.submission.files && selectedSubmission.submission.files.length > 0">
                    <p class="text-xs text-gray-500 mb-2">Attached Files</p>
                    <div class="grid grid-cols-2 gap-3">
                        <div v-for="(file, idx) in selectedSubmission.submission.files" :key="idx"
                            class="border border-gray-200 rounded-lg p-3 hover:border-indigo-300 transition-colors">
                            <div class="flex items-center gap-2">
                                <i :class="[
                                    'pi text-2xl',
                                    file.type === 'image' ? 'pi-image text-purple-500' :
                                    file.type === 'pdf' ? 'pi-file-pdf text-red-500' :
                                    file.type === 'doc' ? 'pi-file-word text-blue-500' :
                                    'pi-file text-gray-500'
                                ]"></i>
                                <div class="flex-1 min-w-0">
                                    <p class="text-sm font-medium text-gray-800 truncate">{{ file.name }}</p>
                                    <p class="text-xs text-gray-500">{{ file.size }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Teacher Feedback -->
                <div v-if="selectedSubmission.submission.feedback" class="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div class="flex items-start gap-2">
                        <i class="pi pi-comment text-blue-600 mt-1"></i>
                        <div>
                            <p class="text-xs font-semibold text-blue-800 mb-1">Teacher's Feedback</p>
                            <p class="text-sm text-blue-900">{{ selectedSubmission.submission.feedback }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <template #footer>
            <div class="flex items-center justify-end">
                <button
                    @click="showSubmissionDialog = false"
                    class="px-5 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors duration-200"
                >
                    Close
                </button>
            </div>
        </template>
    </Dialog>
    
    <!-- Restore Confirmation Dialog -->
    <Dialog v-model:visible="showRestoreConfirm" modal :style="{ width: '90vw', maxWidth: '450px' }" :dismissableMask="true">
        <template #header>
            <div class="flex items-center gap-3">
                <i class="pi pi-undo text-indigo-600 text-xl"></i>
                <h3 class="text-lg font-bold text-gray-800">Restore Class</h3>
            </div>
        </template>

        <div class="py-4">
            <p class="text-gray-700">Are you sure you want to restore <strong>"{{ classToRestore?.name }}"</strong>? This class will be moved back to your active classes.</p>
        </div>

        <template #footer>
            <div class="flex items-center justify-end gap-3">
                <button
                    @click="showRestoreConfirm = false"
                    class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors duration-200"
                >
                    Cancel
                </button>
                <button
                    @click="confirmRestore"
                    class="px-5 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors duration-200 flex items-center gap-2"
                >
                    <i class="pi pi-undo"></i>
                    <span>Restore</span>
                </button>
            </div>
        </template>
    </Dialog>

    <div>
        <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 shadow-lg rounded-t-xl h-40 md:h-36 flex items-center px-6 md:px-8">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div class="space-y-3">
                    <h1 class="text-xl md:text-2xl font-bold text-white px-4 py-2 md:px-6 md:py-3 rounded-xl inline-block bg-white/20 backdrop-blur-sm">
                        Archived Classes
                    </h1>
                    <p class="text-white/90 ml-2 flex items-center gap-2">
                        <i class="pi pi-user"></i>
                        Student
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
                                    'px-4 py-2 rounded-lg text-sm font-medium transition-all',
                                    currentFilter === period.toLowerCase()
                                        ? 'bg-indigo-600 text-white shadow-md'
                                        : 'text-indigo-700 bg-white hover:bg-indigo-50 border border-indigo-100'
                                ]"
                            >
                                {{ period }}
                            </button>
                        </div>
                        
                        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 md:gap-6">
                            <!-- Grade 1 - A Card -->
                            <div 
                                class="group bg-white rounded-xl shadow-sm border border-indigo-100 overflow-hidden hover:shadow-md hover:border-indigo-200 transition-all cursor-pointer"
                                @click="showSubjectActivities('Grade 1 - A')"
                            >
                            <!-- Header with Class Name -->
                            <div class="bg-gradient-to-r from-indigo-600 via-violet-600 to-blue-600 p-4">
                                <h3 class="text-lg font-semibold text-white">Grade 1 - A</h3>
                                <p class="text-xs text-white/80">Archived on May 30, 2025</p>
                            </div>
                            
                            <!-- Class Details -->
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-3">
                                    <div class="flex items-center space-x-2">
                                        <div class="p-2 rounded-lg bg-indigo-50">
                                            <i class="pi pi-users text-indigo-600"></i>
                                        </div>
                                        <div>
                                            <p class="text-xs text-indigo-700">Classmates</p>
                                            <p class="font-medium text-indigo-900">70</p>
                                        </div>
                                    </div>
                                    <div class="flex items-center space-x-2">
                                        <div class="p-2 rounded-lg bg-violet-50">
                                            <i class="pi pi-folder text-violet-600"></i>
                                        </div>
                                        <div>
                                            <p class="text-xs text-violet-700">Folders</p>
                                            <p class="font-medium text-violet-900">6</p>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="flex items-center text-sm text-indigo-600 border-t border-indigo-100 pt-3 mt-3">
                                    <div class="flex items-center">
                                        <i class="pi pi-calendar mr-1"></i>
                                        <span>SY 2024-2025</span>
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
                            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                                <h3 class="text-xl font-bold text-indigo-900">My Portfolio</h3>
                                <div class="w-full sm:w-auto">
                                    <button 
                                        @click="goBack"
                                        class="flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-all duration-200 w-full sm:w-auto shadow-sm"
                                    >
                                        <i class="pi pi-arrow-left"></i>
                                        <span class="font-medium">Back to Classes</span>
                                    </button>
                                </div>
                            </div>
                        </template>

                        <!-- Portfolio Folders View -->
                        <div v-if="!showingActivities" class="bg-white/90 backdrop-blur-sm rounded-xl p-6 shadow-sm border border-indigo-100">
                            <div class="space-y-6">
                                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
                                    <!-- Portfolio Folders -->
                                    <div 
                                        v-for="folder in portfolioFolders"
                                        :key="folder.id"
                                        class="group bg-white rounded-xl shadow-sm border border-indigo-100 overflow-hidden hover:shadow-lg transition-all cursor-pointer transform hover:-translate-y-1 duration-200"
                                        @click="showActivities(folder.name)"
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
                                            <div class="flex items-center space-x-2 text-sm text-indigo-600 font-medium">
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
                                    <span class="text-2xl font-bold text-indigo-900">List of Activities - {{ selectedSubject }}</span>
                                </div>
                                <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
                                    <button 
                                        @click="showingActivities = false" 
                                        class="flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-all duration-200 w-full sm:w-auto shadow-sm"
                                    >
                                        <i class="pi pi-arrow-left"></i>
                                        <span>Back to Folders</span>
                                    </button>
                                </div>
                            </div>

                            <!-- Activities Table -->
                            <div class="bg-white/90 backdrop-blur-sm rounded-xl shadow-sm overflow-hidden border border-indigo-100">
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
                                    <div v-for="(activity, index) in activities" :key="index" 
                                        @click="viewSubmission(activity)"
                                        class="grid grid-cols-12 gap-4 px-6 py-4 hover:bg-indigo-50/50 transition-colors duration-150 items-center cursor-pointer">
                                        <!-- Activity Type with Icon -->
                                        <div class="col-span-2">
                                            <div class="flex items-center gap-2">
                                                <div :class="[
                                                    'w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0',
                                                    activity.type === 'Project' ? 'bg-purple-100' : 
                                                    activity.type === 'Contest' ? 'bg-blue-100' : 
                                                    activity.type === 'Quiz' ? 'bg-green-100' : 
                                                    activity.type === 'Exam' ? 'bg-red-100' : 'bg-gray-100'
                                                ]">
                                                    <span :class="[
                                                        'text-base font-bold',
                                                        activity.type === 'Project' ? 'text-purple-600' : 
                                                        activity.type === 'Contest' ? 'text-blue-600' : 
                                                        activity.type === 'Quiz' ? 'text-green-600' : 
                                                        activity.type === 'Exam' ? 'text-red-600' : 'text-gray-600'
                                                    ]">{{ activity.type.charAt(0) }}</span>
                                                </div>
                                                <span class="text-sm text-gray-700 capitalize truncate">{{ activity.type }}</span>
                                            </div>
                                        </div>

                                        <!-- Title with ID -->
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
                                                {{ activity.description }}
                                            </div>
                                        </div>

                                        <!-- Due Date with Time -->
                                        <div class="col-span-2 text-center">
                                            <div class="text-sm text-gray-700 font-medium">
                                                {{ activity.date }}
                                                <div v-if="activity.time" class="text-xs text-gray-500 mt-0.5">{{ activity.time }}</div>
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
import { ref, computed } from 'vue';
import { useToast } from 'primevue/usetoast';
import Toast from 'primevue/toast';
import Dialog from 'primevue/dialog';

// Toast notification
const toast = useToast();

// Component state
const showingSubject = ref(false);
const showingActivities = ref(false);
const selectedSubject = ref('Sample Class');
const currentFilter = ref('all');
const showSubmissionDialog = ref(false);
const selectedSubmission = ref(null);

// Portfolio folders data
const portfolioFolders = ref([
    { id: 1, name: 'Quarter 1 Portfolio', itemCount: 4 },
    { id: 2, name: 'Quarter 2 Portfolio', itemCount: 5 },
    { id: 3, name: 'Quarter 3 Portfolio', itemCount: 4 },
    { id: 4, name: 'Quarter 4 Portfolio', itemCount: 5 },
    { id: 5, name: 'Special Projects', itemCount: 4 },
    { id: 6, name: 'Art & Creativity', itemCount: 6 }
]);

// Activities data by folder with submission data
const activitiesByFolder = {
    'Quarter 1 Portfolio': [
        { 
            id: 101, type: 'Project', title: 'All About Me Poster', 
            description: 'Create a colorful poster introducing yourself. Include your name, age, favorite things, and a self-portrait...', 
            date: 'Jun 15, 2024', time: '10:00 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Jun 14, 2024',
                submittedTime: '3:45 PM',
                score: 95,
                maxScore: 100,
                caption: 'Here is my colorful poster about myself! I included my favorite hobbies like drawing and reading, my family, and a self-portrait. I used lots of bright colors!',
                files: [
                    { name: 'all-about-me-poster.jpg', type: 'image', size: '2.4 MB' },
                    { name: 'poster-draft.pdf', type: 'pdf', size: '1.1 MB' }
                ],
                feedback: 'Excellent work! Your poster is very creative and colorful. I love how you organized the information and your self-portrait is wonderful. Great job!'
            }
        },
        { 
            id: 102, type: 'Quiz', title: 'Number Recognition Quiz', 
            description: 'Identify and write numbers 1-50. Match numerals with number words.', 
            date: 'Jun 20, 2024', time: '9:00 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Jun 19, 2024',
                submittedTime: '8:30 AM',
                score: 48,
                maxScore: 50,
                caption: 'I completed all the number matching exercises and wrote the numbers carefully.',
                files: [
                    { name: 'number-quiz-answers.pdf', type: 'pdf', size: '856 KB' }
                ],
                feedback: 'Great job! You got almost all the numbers correct. Just remember that 13 is "thirteen" not "threeteen". Keep practicing!'
            }
        },
        { 
            id: 103, type: 'Project', title: 'Family Tree Artwork', 
            description: 'Draw your family tree with pictures or drawings of family members. Label each person with their name an...', 
            date: 'Jun 28, 2024', time: '2:00 PM',
            submission: {
                status: 'Scored',
                submittedDate: 'Jun 27, 2024',
                submittedTime: '1:15 PM',
                score: 92,
                maxScore: 100,
                caption: 'My family tree shows my parents, grandparents, and my little sister. I drew everyone and added their names and ages.',
                files: [
                    { name: 'family-tree-drawing.jpg', type: 'image', size: '3.2 MB' },
                    { name: 'family-photos.jpg', type: 'image', size: '2.8 MB' }
                ],
                feedback: 'Beautiful family tree! I can see you put a lot of effort into drawing each family member. Your labels are clear and neat. Well done!'
            }
        },
        { 
            id: 104, type: 'Quiz', title: 'Alphabet Assessment', 
            description: 'Recite the alphabet and identify uppercase and lowercase letters A-Z.', 
            date: 'Jul 5, 2024', time: '11:00 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Jul 4, 2024',
                submittedTime: '10:20 AM',
                score: 50,
                maxScore: 50,
                caption: 'I practiced the alphabet many times and can identify all uppercase and lowercase letters!',
                files: [
                    { name: 'alphabet-worksheet.pdf', type: 'pdf', size: '1.5 MB' }
                ],
                feedback: 'Perfect score! You know your alphabet very well. Excellent work on identifying both uppercase and lowercase letters!'
            }
        }
    ],
    'Quarter 2 Portfolio': [
        { 
            id: 201, type: 'Project', title: 'Weather Journal', 
            description: 'Keep a daily weather journal for one week. Draw pictures and write simple sentences about the weather each day.', 
            date: 'Aug 12, 2024', time: '1:00 PM',
            submission: {
                status: 'Scored',
                submittedDate: 'Aug 11, 2024',
                submittedTime: '11:20 AM',
                score: 88,
                maxScore: 100,
                caption: 'I kept a weather journal for 7 days! I drew pictures of sunny, rainy, and cloudy days and wrote about what I saw.',
                files: [
                    { name: 'weather-journal-week1.pdf', type: 'pdf', size: '3.1 MB' },
                    { name: 'weather-drawings.jpg', type: 'image', size: '2.7 MB' }
                ],
                feedback: 'Great observations! Your drawings are detailed and your sentences are clear. Remember to capitalize the first word of each sentence.'
            }
        },
        { 
            id: 202, type: 'Quiz', title: 'Addition & Subtraction Quiz', 
            description: 'Solve basic addition and subtraction problems within 20. Show your work using drawings or number lines.', 
            date: 'Aug 18, 2024', time: '10:30 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Aug 17, 2024',
                submittedTime: '9:15 AM',
                score: 45,
                maxScore: 50,
                caption: 'I solved all the math problems and showed my work with number lines like you taught us!',
                files: [
                    { name: 'math-quiz-answers.pdf', type: 'pdf', size: '1.2 MB' }
                ],
                feedback: 'Excellent work! You showed your thinking clearly. Just watch out for borrowing in subtraction - review problem #8.'
            }
        },
        { 
            id: 203, type: 'Contest', title: 'Spelling Bee Competition', 
            description: 'Participate in the class spelling bee. Study the provided word list of 25 first-grade vocabulary words.', 
            date: 'Aug 25, 2024', time: '9:00 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Aug 25, 2024',
                submittedTime: '9:45 AM',
                score: 22,
                maxScore: 25,
                caption: 'I practiced all the spelling words with my mom every night. I made it to round 4!',
                files: [
                    { name: 'spelling-practice-sheet.pdf', type: 'pdf', size: '890 KB' }
                ],
                feedback: 'You did wonderfully! 4th place is amazing. Keep practicing those tricky words like "because" and "friend".'
            }
        },
        { 
            id: 204, type: 'Project', title: 'Plant Growth Observation', 
            description: 'Plant a seed and observe its growth over two weeks. Draw and label the plant parts as they develop.', 
            date: 'Sep 2, 2024', time: '3:00 PM',
            submission: {
                status: 'Scored',
                submittedDate: 'Sep 1, 2024',
                submittedTime: '2:30 PM',
                score: 96,
                maxScore: 100,
                caption: 'I planted a bean seed and watched it grow for 2 weeks! I drew pictures every 3 days and labeled the roots, stem, and leaves.',
                files: [
                    { name: 'plant-growth-photos.jpg', type: 'image', size: '4.5 MB' },
                    { name: 'observation-journal.pdf', type: 'pdf', size: '2.3 MB' }
                ],
                feedback: 'Outstanding science project! Your observations are detailed and your drawings show the growth stages perfectly. Great job!'
            }
        },
        { 
            id: 205, type: 'Exam', title: 'Reading Comprehension Test', 
            description: 'Read short passages and answer questions about characters, setting, and main ideas.', 
            date: 'Sep 10, 2024', time: '8:30 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Sep 10, 2024',
                submittedTime: '9:15 AM',
                score: 42,
                maxScore: 50,
                caption: 'I read all the stories carefully and answered the questions about the characters and what happened.',
                files: [
                    { name: 'reading-test-answers.pdf', type: 'pdf', size: '1.8 MB' }
                ],
                feedback: 'Good reading comprehension! You understood the main ideas well. Practice finding details in the text to support your answers.'
            }
        }
    ],
    'Quarter 3 Portfolio': [
        { 
            id: 301, type: 'Project', title: 'Community Helpers Presentation', 
            description: 'Research a community helper (doctor, firefighter, teacher, etc.) and create a presentation with pictures and facts.', 
            date: 'Oct 8, 2024', time: '11:00 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Oct 7, 2024',
                submittedTime: '4:10 PM',
                score: 94,
                maxScore: 100,
                caption: 'I researched firefighters! I learned about their equipment, how they help people, and what they do every day. I made a poster with pictures.',
                files: [
                    { name: 'firefighter-presentation.pdf', type: 'pdf', size: '5.2 MB' },
                    { name: 'firefighter-photos.jpg', type: 'image', size: '3.8 MB' }
                ],
                feedback: 'Wonderful presentation! You included great facts and your poster is very informative. I learned new things about firefighters from you!'
            }
        },
        { 
            id: 302, type: 'Quiz', title: 'Shapes and Patterns Quiz', 
            description: 'Identify 2D and 3D shapes. Create and extend patterns using shapes and colors.', 
            date: 'Oct 15, 2024', time: '9:30 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Oct 14, 2024',
                submittedTime: '8:45 AM',
                score: 47,
                maxScore: 50,
                caption: 'I identified all the shapes - circles, squares, triangles, cubes, and spheres. I also made my own patterns!',
                files: [
                    { name: 'shapes-quiz.pdf', type: 'pdf', size: '1.4 MB' },
                    { name: 'pattern-designs.jpg', type: 'image', size: '2.1 MB' }
                ],
                feedback: 'Great job identifying shapes! Your patterns are creative. Remember that a cube has 6 faces, not 4.'
            }
        },
        { 
            id: 303, type: 'Project', title: 'Story Writing - My Adventure', 
            description: 'Write and illustrate a short story about an imaginary adventure. Include a beginning, middle, and end.', 
            date: 'Oct 22, 2024', time: '2:30 PM',
            submission: {
                status: 'Scored',
                submittedDate: 'Oct 21, 2024',
                submittedTime: '1:50 PM',
                score: 90,
                maxScore: 100,
                caption: 'My story is about a magical adventure to a candy land! I wrote 3 pages and drew pictures for each part of the story.',
                files: [
                    { name: 'my-adventure-story.pdf', type: 'pdf', size: '4.7 MB' },
                    { name: 'story-illustrations.jpg', type: 'image', size: '3.5 MB' }
                ],
                feedback: 'What an imaginative story! Your beginning, middle, and end are clear. Your illustrations bring the story to life. Great creativity!'
            }
        },
        { 
            id: 304, type: 'Contest', title: 'Math Olympics', 
            description: 'Compete in math games and challenges. Topics include counting, addition, subtraction, and word problems.', 
            date: 'Oct 28, 2024', time: '10:00 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Oct 28, 2024',
                submittedTime: '11:30 AM',
                score: 85,
                maxScore: 100,
                caption: 'I participated in all the math games! My favorite was the word problem relay race. Our team came in 2nd place!',
                files: [
                    { name: 'math-olympics-worksheet.pdf', type: 'pdf', size: '1.9 MB' }
                ],
                feedback: 'Excellent teamwork and math skills! You solved the word problems accurately. Keep up the great work!'
            }
        }
    ],
    'Quarter 4 Portfolio': [
        { 
            id: 401, type: 'Project', title: 'Animal Habitat Diorama', 
            description: 'Create a 3D diorama showing an animal in its natural habitat. Include labels for the animal and habitat features.', 
            date: 'Nov 12, 2024', time: '1:30 PM',
            submission: {
                status: 'Scored',
                submittedDate: 'Nov 11, 2024',
                submittedTime: '12:45 PM',
                score: 98,
                maxScore: 100,
                caption: 'I made a rainforest diorama with a jaguar! I used a shoebox, painted trees, added moss, and labeled all the parts.',
                files: [
                    { name: 'diorama-photos.jpg', type: 'image', size: '6.2 MB' },
                    { name: 'habitat-research.pdf', type: 'pdf', size: '2.8 MB' }
                ],
                feedback: 'Amazing diorama! Your attention to detail is impressive. The labels are clear and your jaguar looks realistic. Excellent work!'
            }
        },
        { 
            id: 402, type: 'Quiz', title: 'Money and Time Quiz', 
            description: 'Count coins and make change. Tell time to the hour and half-hour on analog and digital clocks.', 
            date: 'Nov 18, 2024', time: '10:00 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Nov 17, 2024',
                submittedTime: '9:20 AM',
                score: 46,
                maxScore: 50,
                caption: 'I practiced counting coins and telling time. I can make change and read both types of clocks now!',
                files: [
                    { name: 'money-time-quiz.pdf', type: 'pdf', size: '1.6 MB' }
                ],
                feedback: 'Great progress! You counted coins correctly. Just remember the minute hand points to 6 for half past the hour.'
            }
        },
        { 
            id: 403, type: 'Project', title: 'Biography Book Report', 
            description: 'Read a biography of a famous person and create a book report poster with important facts about their life.', 
            date: 'Nov 25, 2024', time: '11:30 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Nov 24, 2024',
                submittedTime: '10:15 AM',
                score: 93,
                maxScore: 100,
                caption: 'I read about Helen Keller! I made a poster with facts about her childhood, how she learned to communicate, and her achievements.',
                files: [
                    { name: 'helen-keller-poster.jpg', type: 'image', size: '4.9 MB' },
                    { name: 'book-report-notes.pdf', type: 'pdf', size: '1.7 MB' }
                ],
                feedback: 'Wonderful book report! You captured the important facts about Helen Keller\'s inspiring life. Your poster is well-organized and informative!'
            }
        },
        { 
            id: 404, type: 'Exam', title: 'End of Year Assessment', 
            description: 'Comprehensive test covering all subjects: reading, writing, math, science, and social studies.', 
            date: 'Dec 5, 2024', time: '8:00 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Dec 5, 2024',
                submittedTime: '10:30 AM',
                score: 89,
                maxScore: 100,
                caption: 'I studied hard for the final exam! I reviewed all my notes and practiced all the subjects.',
                files: [
                    { name: 'final-exam-answers.pdf', type: 'pdf', size: '3.4 MB' }
                ],
                feedback: 'Excellent performance on your final exam! You showed great understanding across all subjects. Have a wonderful summer!'
            }
        },
        { 
            id: 405, type: 'Project', title: 'Summer Reading Plan', 
            description: 'Create a list of 10 books you want to read over summer vacation. Design a reading log to track your progress.', 
            date: 'Dec 12, 2024', time: '2:00 PM',
            submission: {
                status: 'Scored',
                submittedDate: 'Dec 11, 2024',
                submittedTime: '1:30 PM',
                score: 100,
                maxScore: 100,
                caption: 'I picked 10 exciting books to read this summer! I made a colorful reading log to track when I finish each book.',
                files: [
                    { name: 'summer-reading-list.pdf', type: 'pdf', size: '2.1 MB' },
                    { name: 'reading-log-template.pdf', type: 'pdf', size: '1.3 MB' }
                ],
                feedback: 'Perfect! Your book choices are diverse and age-appropriate. I love your creative reading log design. Happy reading this summer!'
            }
        }
    ],
    'Special Projects': [
        { 
            id: 501, type: 'Contest', title: 'Science Fair - Volcano Experiment', 
            description: 'Build a model volcano and demonstrate a chemical reaction. Explain the science behind volcanic eruptions.', 
            date: 'Jul 20, 2024', time: '9:00 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Jul 19, 2024',
                submittedTime: '3:00 PM',
                score: 97,
                maxScore: 100,
                caption: 'I built a volcano using papier-mâché and made it erupt with baking soda and vinegar! I explained how real volcanoes work.',
                files: [
                    { name: 'volcano-experiment-video.mp4', type: 'doc', size: '45.3 MB' },
                    { name: 'volcano-photos.jpg', type: 'image', size: '5.8 MB' },
                    { name: 'science-explanation.pdf', type: 'pdf', size: '2.4 MB' }
                ],
                feedback: 'Fantastic science project! Your volcano looked amazing and your explanation of the chemical reaction was clear. Great presentation!'
            }
        },
        { 
            id: 502, type: 'Project', title: 'Cultural Heritage Day', 
            description: 'Share information about your family\'s cultural background. Bring traditional food, clothing, or artifacts to present.', 
            date: 'Aug 30, 2024', time: '10:30 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Aug 29, 2024',
                submittedTime: '5:20 PM',
                score: 100,
                maxScore: 100,
                caption: 'I shared about my Filipino heritage! I brought traditional food (lumpia), showed our traditional clothing (barong), and taught everyone some Tagalog words.',
                files: [
                    { name: 'cultural-presentation.pdf', type: 'pdf', size: '7.2 MB' },
                    { name: 'family-traditions.jpg', type: 'image', size: '4.1 MB' }
                ],
                feedback: 'What a wonderful presentation! You taught us so much about Filipino culture. Thank you for sharing your heritage with the class!'
            }
        },
        { 
            id: 503, type: 'Contest', title: 'Talent Show Performance', 
            description: 'Prepare a 3-minute talent performance (singing, dancing, magic trick, etc.) for the school talent show.', 
            date: 'Sep 15, 2024', time: '6:00 PM',
            submission: {
                status: 'Scored',
                submittedDate: 'Sep 15, 2024',
                submittedTime: '7:15 PM',
                score: 95,
                maxScore: 100,
                caption: 'I performed a dance routine to my favorite song! I practiced for 3 weeks and remembered all the moves. It was so fun!',
                files: [
                    { name: 'talent-show-performance.mp4', type: 'doc', size: '38.7 MB' },
                    { name: 'practice-photos.jpg', type: 'image', size: '3.9 MB' }
                ],
                feedback: 'Amazing performance! Your energy and enthusiasm were wonderful. You practiced hard and it showed. The audience loved it!'
            }
        },
        { 
            id: 504, type: 'Project', title: 'Recycling Awareness Campaign', 
            description: 'Design posters and create a presentation to teach classmates about recycling and environmental protection.', 
            date: 'Oct 10, 2024', time: '1:00 PM',
            submission: {
                status: 'Scored',
                submittedDate: 'Oct 9, 2024',
                submittedTime: '12:30 PM',
                score: 91,
                maxScore: 100,
                caption: 'I made 3 posters about recycling plastic, paper, and metal. I also created a presentation teaching everyone how to reduce, reuse, and recycle!',
                files: [
                    { name: 'recycling-posters.pdf', type: 'pdf', size: '8.4 MB' },
                    { name: 'presentation-slides.pdf', type: 'pdf', size: '5.1 MB' }
                ],
                feedback: 'Excellent environmental awareness project! Your posters are eye-catching and informative. You\'re helping make our planet better!'
            }
        }
    ],
    'Art & Creativity': [
        { 
            id: 601, type: 'Project', title: 'Self-Portrait in Different Styles', 
            description: 'Create three self-portraits using different art styles: realistic, abstract, and cartoon. Use various media.', 
            date: 'Jun 25, 2024', time: '2:00 PM',
            submission: {
                status: 'Scored',
                submittedDate: 'Jun 24, 2024',
                submittedTime: '1:15 PM',
                score: 96,
                maxScore: 100,
                caption: 'I created 3 self-portraits! One realistic with colored pencils, one abstract with paint, and one cartoon style with markers. Each one shows me in a different way!',
                files: [
                    { name: 'realistic-portrait.jpg', type: 'image', size: '4.2 MB' },
                    { name: 'abstract-portrait.jpg', type: 'image', size: '3.8 MB' },
                    { name: 'cartoon-portrait.jpg', type: 'image', size: '2.9 MB' }
                ],
                feedback: 'Incredible artistic range! Each portrait captures your personality in a unique way. Your use of different media shows great skill!'
            }
        },
        { 
            id: 602, type: 'Project', title: 'Clay Sculpture - Favorite Animal', 
            description: 'Sculpt your favorite animal using clay. Paint and decorate it after it dries.', 
            date: 'Jul 15, 2024', time: '11:00 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Jul 14, 2024',
                submittedTime: '10:30 AM',
                score: 94,
                maxScore: 100,
                caption: 'I sculpted a dolphin! I shaped the clay carefully, let it dry for 2 days, then painted it blue and gray with shiny details.',
                files: [
                    { name: 'dolphin-sculpture-photos.jpg', type: 'image', size: '5.7 MB' },
                    { name: 'sculpture-process.jpg', type: 'image', size: '4.3 MB' }
                ],
                feedback: 'Beautiful sculpture! Your dolphin looks so realistic. Great attention to detail in the painting. Wonderful work!'
            }
        },
        { 
            id: 603, type: 'Project', title: 'Watercolor Landscape Painting', 
            description: 'Paint a landscape scene using watercolors. Include foreground, middle ground, and background elements.', 
            date: 'Aug 5, 2024', time: '10:00 AM',
            submission: {
                status: 'Scored',
                submittedDate: 'Aug 4, 2024',
                submittedTime: '9:20 AM',
                score: 92,
                maxScore: 100,
                caption: 'I painted a sunset at the beach! The foreground has sand and shells, middle ground has palm trees, and background has the ocean and sunset sky.',
                files: [
                    { name: 'watercolor-landscape.jpg', type: 'image', size: '6.1 MB' },
                    { name: 'painting-sketches.jpg', type: 'image', size: '2.8 MB' }
                ],
                feedback: 'Stunning watercolor work! Your layering of foreground, middle, and background creates great depth. The sunset colors are beautiful!'
            }
        },
        { 
            id: 604, type: 'Contest', title: 'School Art Exhibition', 
            description: 'Submit your best artwork for the annual school art exhibition. Theme: "My World, My Imagination".', 
            date: 'Sep 20, 2024', time: '3:00 PM',
            submission: {
                status: 'Scored',
                submittedDate: 'Sep 19, 2024',
                submittedTime: '2:45 PM',
                score: 98,
                maxScore: 100,
                caption: 'I created a mixed media artwork showing my imaginary world where kids can fly and play in the clouds! I used paint, glitter, and collage.',
                files: [
                    { name: 'exhibition-artwork.jpg', type: 'image', size: '7.9 MB' },
                    { name: 'artwork-description.pdf', type: 'pdf', size: '1.2 MB' }
                ],
                feedback: 'Absolutely magical! Your imagination shines through. This piece won 2nd place in the exhibition. Congratulations!'
            }
        },
        { 
            id: 605, type: 'Project', title: 'Collage - Seasons of the Year', 
            description: 'Create a four-panel collage representing spring, summer, fall, and winter using magazine cutouts and drawings.', 
            date: 'Oct 30, 2024', time: '1:30 PM',
            submission: {
                status: 'Scored',
                submittedDate: 'Oct 29, 2024',
                submittedTime: '12:50 PM',
                score: 97,
                maxScore: 100,
                caption: 'I made a 4-panel collage! Spring has flowers, summer has sunshine and beach, fall has colorful leaves, and winter has snowflakes and snowmen.',
                files: [
                    { name: 'seasons-collage.jpg', type: 'image', size: '8.3 MB' },
                    { name: 'collage-materials.jpg', type: 'image', size: '3.6 MB' }
                ],
                feedback: 'Excellent representation of all four seasons! Your choice of images and colors perfectly captures each season. Creative and well-organized!'
            }
        },
        { 
            id: 606, type: 'Project', title: 'Origami Art Display', 
            description: 'Learn and create 5 different origami designs. Mount them on a poster board with instructions.', 
            date: 'Nov 20, 2024', time: '2:30 PM',
            submission: {
                status: 'Scored',
                submittedDate: 'Nov 19, 2024',
                submittedTime: '1:40 PM',
                score: 100,
                maxScore: 100,
                caption: 'I learned to make 5 origami designs: crane, frog, boat, butterfly, and flower! I mounted them on a poster with step-by-step instructions for each one.',
                files: [
                    { name: 'origami-display.jpg', type: 'image', size: '5.4 MB' },
                    { name: 'origami-instructions.pdf', type: 'pdf', size: '3.7 MB' }
                ],
                feedback: 'Perfect origami work! Each design is folded precisely and your instructions are clear. You could teach others how to make these!'
            }
        }
    ]
};

const activities = ref([]);

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

const showActivities = (folderName) => {
    selectedSubject.value = folderName;
    activities.value = activitiesByFolder[folderName] || [];
    showingActivities.value = true;
};

const viewSubmission = (activity) => {
    console.log('📄 Viewing submission for:', activity.title);
    selectedSubmission.value = activity;
    showSubmissionDialog.value = true;
};

const goBack = () => {
    showingSubject.value = false;
};

const viewClass = (class_) => {
    console.log('Viewing class:', class_.name);
};

// Restore class with confirmation
const showRestoreConfirm = ref(false);
const classToRestore = ref(null);

const restoreClass = (classroom) => {
    classToRestore.value = classroom;
    showRestoreConfirm.value = true;
};

const confirmRestore = async () => {
    if (!classToRestore.value) return;
    
    try {
        console.log('🔄 Restoring class:', classToRestore.value.name);
        // Simulated API call - replace with actual API when available
        // await axios.put(`/api/classrooms/${classToRestore.value.id}/`, { is_archived: false });
        
        toast.add({
            severity: 'success',
            summary: 'Class Restored',
            detail: `"${classToRestore.value.name}" has been restored successfully!`,
            life: 3000
        });
        
        // Reload would go here
        // await loadArchivedClasses();
    } catch (error) {
        console.error('❌ Error restoring class:', error);
        toast.add({
            severity: 'error',
            summary: 'Restore Failed',
            detail: 'Failed to restore class. Please try again.',
            life: 3000
        });
    } finally {
        showRestoreConfirm.value = false;
        classToRestore.value = null;
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