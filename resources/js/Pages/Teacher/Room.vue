<template>
    <Head :title="`| ${className}`"/>
    <div class="min-h-screen bg-gray-50">
        <!-- Class Header -->
        <div :class="[themeClasses.header, 'p-6 shadow-md rounded-[10px]']">
            <div class="flex justify-between items-center">
                <div>
                    <h1 :class="[themeClasses.badge, 'text-xl font-bold inline-block px-4 py-2 rounded-lg shadow-sm']">
                        {{ className }}
                    </h1>
                    <p class="text-white mt-2">Teacher: {{ auth.user.name }}</p>
                </div>
                <div class="flex items-center gap-4">
                    <button class="text-white hover:bg-white/20 p-2 rounded-full transition-colors">
                        <i class="pi pi-cog text-xl"></i>
                    </button>
                </div>
            </div>
            
            <!-- Navigation Tabs -->
            <div class="flex gap-4 mt-6">
                <button 
                    v-for="tab in tabs" 
                    :key="tab.id"
                    @click="activeTab = tab.id"
                    :class="[
                        'text-white px-6 py-2 rounded-t-lg transition-colors',
                        activeTab === tab.id ? 'bg-white/20 font-medium' : 'hover:bg-white/10'
                    ]"
                >
                    <i :class="['pi', tab.icon, 'mr-2']"></i>
                    {{ tab.name }}
                </button>
            </div>
        </div>

        <!-- Main Content Area -->
        <div class="flex gap-6 p-6">
            <!-- Left Sidebar - Members (Only show in pupil tab) -->
            <div v-if="activeTab === 'pupil'" class="w-72">
                <div class="bg-white rounded-[10px] shadow-sm">
                    <!-- Members Header with Add Button -->
                    <div :class="[themeClasses.memberHeader, 'text-white p-4 rounded-t-[10px] flex justify-between items-center']">
                        <span class="font-medium">Members ({{ students.length }})</span>
                        <button @click="openAddStudentDialog" class="hover:bg-white/20 p-1 rounded-lg">
                            <i class="pi pi-plus"></i>
                        </button>
                    </div>
                    <div class="divide-y">
                        <div v-for="student in students" 
                             :key="student.id" 
                             @click="selectedStudent = student"
                             class="flex items-center justify-between p-3 cursor-pointer transition-all"
                             :class="{
                                 'bg-gray-200': selectedStudent?.id === student.id,
                                 'hover:bg-gray-100': selectedStudent?.id !== student.id
                             }">
                            <div class="flex items-center gap-3">
                                <div :class="[
                                    'w-8 h-8 rounded text-white flex items-center justify-center text-base font-medium',
                                    'bg-blue-600'
                                ]">
                                    {{ student.initial }}
                                </div>
                                <div class="font-medium text-gray-900">{{ student.name }}</div>
                            </div>
                            
                            <!-- Simple arrow without background -->
                            <div v-if="selectedStudent?.id === student.id">
                                <i class="pi pi-chevron-right text-gray-400"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Content Area -->
            <div :class="[
                'bg-white rounded-[10px] shadow-sm',
                activeTab === 'schedule' ? 'w-full' : 'flex-1'
            ]">
                <template v-if="activeTab === 'pupil'">
                    <!-- Portfolio/Progress Record Tabs -->
                    <div class="flex gap-2 mb-4">
                        <button 
                            @click="activeContentTab = 'portfolio'"
                            :class="[
                                'flex items-center gap-2 px-4 py-2 rounded-lg transition-colors',
                                activeContentTab === 'portfolio' 
                                    ? `bg-${props.theme}-500 text-white` 
                                    : 'bg-white text-gray-700 hover:bg-gray-50'
                            ]"
                        >
                            <i class="pi pi-images"></i>
                            Portfolio
                        </button>
                        <button 
                            @click="activeContentTab = 'progress'"
                            :class="[
                                'flex items-center gap-2 px-4 py-2 rounded-lg transition-colors',
                                activeContentTab === 'progress' 
                                    ? `bg-${props.theme}-500 text-white` 
                                    : 'bg-white text-gray-700 hover:bg-gray-50'
                            ]"
                        >
                            <i class="pi pi-chart-line"></i>
                            Progress Record
                        </button>
                    </div>

                    <!-- Content Area -->
                    <div class="bg-white rounded-[10px] p-6">
                        <template v-if="activeContentTab === 'portfolio'">
                            <!-- Recent/Shared Tabs -->
                            <div class="border-b border-gray-200 mb-6">
                                <div class="flex gap-8">
                                    <button 
                                        v-for="tab in [
                                            { name: 'Recent', id: 'recent', icon: 'pi-clock' },
                                            { name: 'Shared', id: 'shared', icon: 'pi-share-alt' }
                                        ]"
                                        :key="tab.id"
                                        @click="activePortfolioTab = tab.id"
                                        class="flex items-center gap-2 pb-4 relative"
                                        :class="[
                                            activePortfolioTab === tab.id
                                                ? 'text-blue-600 border-b-2 border-blue-600'
                                                : 'text-gray-600 hover:text-gray-900'
                                        ]"
                                    >
                                        <i :class="['pi', tab.icon]"></i>
                                        {{ tab.name }}
                                    </button>
                                </div>
                            </div>

                            <!-- Portfolio Grid -->
                            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                <!-- No Activities Message -->
                                <div v-if="filteredActivities.length === 0" class="col-span-full">
                                    <div class="flex flex-col items-center justify-center py-12">
                                        <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-3">
                                            <i class="pi pi-inbox text-gray-400 text-xl"></i>
                                        </div>
                                        <p class="text-gray-500 text-center">
                                            No activities available for this student.
                                        </p>
                                    </div>
                                </div>

                                <!-- Activities Grid (only show if there are activities) -->
                                <template v-else>
                                    <div v-for="activity in filteredActivities" 
                                         :key="activity.id"
                                         class="bg-white rounded-lg border border-gray-100 overflow-hidden">
                                        <!-- Activity Image -->
                                        <img :src="activity.image" :alt="activity.title"
                                            class="w-full h-48 object-cover">
                                        
                                        <!-- Activity Content -->
                                        <div class="p-4">
                                            <h4 class="font-medium text-gray-900 mb-2">{{ activity.title }}</h4>
                                            <p class="text-gray-600 text-sm">{{ activity.description }}</p>

                                            <!-- Comments Section -->
                                            <div class="mt-4 pt-3 border-t border-gray-100">
                                                <div class="flex items-center justify-between mb-2">
                                                    <div class="flex items-center gap-2 text-gray-500">
                                                        <i class="pi pi-comments text-[16px]"></i>
                                                        <span class="text-sm">Teacher's Comments</span>
                                                    </div>
                                                    <button 
                                                        @click="addComment(activity)"
                                                        class="flex items-center gap-1.5 text-blue-600 text-sm hover:text-blue-700"
                                                    >
                                                        <i class="pi pi-pencil text-[14px]"></i>
                                                        <span>Add</span>
                                                    </button>
                                                </div>
                                                <p class="text-sm text-gray-500 italic">
                                                    {{ activity.comment || 'No comments yet' }}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </template>
                            </div>
                        </template>

                        <template v-else>
                            <!-- Progress Record content -->
                            <div class="p-6">
                                <!-- Selected Student Indicator -->
                                <div class="flex items-center gap-3 mb-4">
                                    <div :class="`w-10 h-10 rounded-full bg-${props.theme}-600 flex items-center justify-center text-white font-medium`">
                                        {{ selectedStudent?.initial }}
                                    </div>
                                    <div>
                                        <h3 class="font-medium text-gray-900">{{ selectedStudent?.name }}</h3>
                                        <p class="text-sm text-gray-500">Student ID: {{ selectedStudent?.id }}</p>
                                    </div>
                                </div>

                                <!-- Teacher's Remarks Card -->
                                <div class="bg-blue-50 rounded-xl p-4 mb-6">
                                    <div class="flex items-center justify-between mb-2">
                                        <div class="flex items-center gap-2 text-blue-700">
                                            <i class="pi pi-comments"></i>
                                            <h3 class="font-medium">Teacher's Remarks</h3>
                                        </div>
                                        <span class="text-sm text-blue-600">Last updated: {{ studentRemarks.date }}</span>
                                    </div>
                                    <p class="text-blue-700 italic">
                                        {{ studentRemarks.text }}
                                    </p>
                                </div>

                                <!-- Search and Stats Row -->
                                <div class="flex items-center gap-4 mb-6">
                                    <!-- Search Bar -->
                                    <div class="relative flex-1">
                                        <input
                                            v-model="searchQuery"
                                            type="text"
                                            placeholder="Search outputs..."
                                            class="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring focus:ring-blue-200 transition-all"
                                        />
                                        <i class="pi pi-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
                                    </div>

                                    <!-- Minimized Statistics with Labels -->
                                    <div class="flex items-center gap-3">
                                        <!-- Total Activities -->
                                        <div class="flex flex-col items-center px-3 py-1.5 bg-gray-50 rounded-lg border border-gray-200">
                                            <span class="text-sm font-medium text-gray-700">{{ filteredRecords.length }}</span>
                                            <span class="text-[10px] text-gray-500 mt-0.5">Total Activities</span>
                                        </div>

                                        <!-- Completed -->
                                        <div class="flex flex-col items-center px-3 py-1.5 bg-green-50 rounded-lg border border-green-200">
                                            <div class="flex items-center gap-2">
                                                <i class="pi pi-check text-green-600"></i>
                                                <span class="text-sm font-medium text-green-700">{{ completedCount }}</span>
                                            </div>
                                            <span class="text-[10px] text-green-600 mt-0.5">Completed</span>
                                        </div>

                                        <!-- Pending -->
                                        <div class="flex flex-col items-center px-3 py-1.5 bg-red-50 rounded-lg border border-red-200">
                                            <div class="flex items-center gap-2">
                                                <i class="pi pi-clock text-red-600"></i>
                                                <span class="text-sm font-medium text-red-700">{{ pendingCount }}</span>
                                            </div>
                                            <span class="text-[10px] text-red-600 mt-0.5">Pending</span>
                                        </div>
                                    </div>
                                </div>

                                <!-- Search Results Notification -->
                                <div v-if="searchQuery" 
                                    class="p-3 mb-4 bg-blue-50 border border-blue-100 text-blue-700 rounded-lg flex items-center gap-2">
                                    <i class="pi pi-filter"></i>
                                    <span>Showing results for "<strong>{{ searchQuery }}</strong>"</span>
                                </div>

                                <!-- Records Table -->
                                <div class="bg-white rounded-xl border border-gray-100 overflow-hidden">
                                    <DataTable 
                                        :value="filteredRecords" 
                                        :scrollable="true" 
                                        scrollHeight="400px" 
                                        class="p-datatable-custom"
                                        stripedRows
                                        showGridlines>
                                        <Column field="subject" header="Subject">
                                            <template #body="slotProps">
                                                <span class="font-medium text-gray-900">{{ slotProps.data.subject }}</span>
                                            </template>
                                        </Column>
                                        <Column field="output" header="Output Name"></Column>
                                        <Column field="dueDate" header="Due Date"></Column>
                                        <Column field="time" header="Time"></Column>
                                        <Column field="status" header="Status">
                                            <template #body="slotProps">
                                                <div :class="[
                                                    'px-3 py-1 rounded-lg text-sm inline-flex items-center',
                                                    slotProps.data.status === 'Passed' 
                                                        ? 'bg-green-100 text-green-700' 
                                                        : 'bg-red-100 text-red-700'
                                                ]">
                                                    <i :class="[
                                                        'pi mr-1.5',
                                                        slotProps.data.status === 'Passed' 
                                                            ? 'pi-check text-green-600' 
                                                            : 'pi-clock text-red-600'
                                                    ]"></i>
                                                    {{ slotProps.data.status }}
                                                </div>
                                            </template>
                                        </Column>
                                        <Column field="history" header="History">
                                            <template #body="slotProps">
                                                <span class="text-gray-500 text-sm flex items-center gap-2">
                                                    <i class="pi pi-clock"></i>
                                                    {{ slotProps.data.history }}
                                                </span>
                                            </template>
                                        </Column>
                                    </DataTable>

                                    <!-- No Records Message -->
                                    <div v-if="filteredRecords.length === 0" 
                                         class="text-center py-12">
                                        <div :class="`w-16 h-16 rounded-full bg-${props.theme}-100 flex items-center justify-center mx-auto mb-4`">
                                            <i :class="`pi pi-inbox text-2xl text-${props.theme}-600`"></i>
                                        </div>
                                        <p class="text-gray-500">
                                            {{ searchQuery ? 'No records found matching your search.' : 'No records available for this student.' }}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                </template>

                <!-- Schedule Tab Content -->
                <template v-if="activeTab === 'schedule'">
                    <div class="p-6">
                        <!-- Calendar Header -->
                        <div class="flex justify-between items-center mb-6">
                            <h2 class="text-xl font-bold" :class="`text-${props.theme}-700`">NOVEMBER 2025</h2>
                            <div class="flex gap-4 items-center">
                                <span class="flex items-center gap-2">
                                    <div :class="`w-3 h-3 rounded-full bg-${props.theme}-100`"></div>
                                    <span class="text-sm text-gray-600">Class Day</span>
                                </span>
                                <span class="flex items-center gap-2">
                                    <div class="w-3 h-3 rounded-full bg-gray-100"></div>
                                    <span class="text-sm text-gray-600">No Class</span>
                                </span>
                            </div>
                        </div>

                        <!-- Days of the Week -->
                        <div class="grid grid-cols-7 text-center font-semibold text-gray-700 mb-4 bg-gray-50 p-3 rounded-lg">
                            <div>Mon</div>
                            <div>Tue</div>
                            <div>Wed</div>
                            <div>Thu</div>
                            <div>Fri</div>
                            <div class="text-red-500">Sat</div>
                            <div class="text-red-500">Sun</div>
                        </div>

                        <!-- Calendar Grid -->
                        <div class="grid grid-cols-7 gap-2">
                            <!-- Empty Spaces for the Start of the Month -->
                            <div v-for="i in 3" :key="'empty-' + i" class="p-4"></div>

                            <!-- Dates with Class Schedule -->
                            <div v-for="(day, date) in schedule" :key="date"
                                class="p-4 border rounded-lg hover:shadow-md cursor-pointer transition-all"
                                :class="{
                                    [`bg-${props.theme}-100 border-${props.theme}-200`]: isClassDay(date + 1),
                                    'bg-gray-50': !isClassDay(date + 1)
                                }"
                                @click="showScheduleDetails(date + 1)">
                                <div class="font-semibold text-gray-800">{{ date + 1 }}</div>
                                <div v-if="isClassDay(date + 1)" :class="`text-sm text-${props.theme}-600 mt-1`">
                                    {{ day.time }}
                                </div>
                            </div>
                        </div>

                        <!-- Current Schedule Display -->
                        <div v-if="selectedDate" :class="`mt-6 p-4 bg-${props.theme}-50 rounded-lg`">
                            <h3 :class="`font-semibold text-${props.theme}-800 mb-2`">
                                Selected Date: November {{ selectedDate }}
                            </h3>
                            <p v-if="isClassDay(selectedDate)" class="text-gray-700">
                                Class Time: {{ schedule[selectedDate - 1].time }}
                            </p>
                            <p v-else class="text-gray-700">
                                No class scheduled for this date
                            </p>
                        </div>
                    </div>
                </template>
            </div>
        </div>

        <!-- Add Student Dialog -->
        <Dialog v-model:visible="showAddStudentDialog" modal header="Add New Student" class="w-[500px]">
            <div class="p-4 bg-gray-50 rounded-lg mb-6">
                <div class="flex items-center justify-between">
                    <div>
                        <h3 class="font-medium text-gray-900">Classroom Code</h3>
                        <p class="text-sm text-gray-600">Share this code with your students</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <code class="px-4 py-2 bg-white rounded-lg border font-mono text-lg">
                            {{ classroomCode }}
                        </code>
                        <button 
                            @click="copyCode"
                            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                            :title="copied ? 'Copied!' : 'Copy code'"
                        >
                            <i class="pi" :class="copied ? 'pi-check text-green-500' : 'pi-copy'"></i>
                        </button>
                    </div>
                </div>
            </div>

            <div class="space-y-4">
                <!-- Email Input -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Student Email</label>
                    <input 
                        v-model="newStudent.email" 
                        type="email" 
                        class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="student@example.com"
                    >
                    <p class="text-xs text-gray-500 mt-1">
                        An invitation will be sent to this email address
                    </p>
                </div>

                <!-- Or Divider -->
                <div class="relative">
                    <div class="absolute inset-0 flex items-center">
                        <div class="w-full border-t border-gray-200"></div>
                    </div>
                    <div class="relative flex justify-center text-sm">
                        <span class="px-2 bg-white text-gray-500">or</span>
                    </div>
                </div>

                <!-- Join with Code Section -->
                <div class="bg-gray-50 p-4 rounded-lg">
                    <h3 class="font-medium text-gray-900 mb-2">Share Join Link</h3>
                    <div class="flex gap-2">
                        <input 
                            type="text" 
                            readonly 
                            :value="`https://yourapp.com/join/${classroomCode}`"
                            class="flex-1 px-3 py-2 bg-white border rounded-lg text-gray-600"
                        >
                        <button 
                            @click="copyLink"
                            class="px-4 py-2 border rounded-lg hover:bg-gray-100"
                        >
                            Copy Link
                        </button>
                    </div>
                </div>
            </div>

            <!-- Dialog Footer -->
            <template #footer>
                <div class="flex justify-between items-center">
                    <button 
                        @click="showAddStudentDialog = false"
                        class="px-4 py-2 border rounded-lg hover:bg-gray-50"
                    >
                        Cancel
                    </button>
                    <button 
                        @click="addStudent"
                        :disabled="!isValidStudent"
                        :class="[
                            'px-4 py-2 rounded-lg text-white',
                            isValidStudent ? `bg-${props.theme}-500 hover:bg-${props.theme}-600` : 'bg-gray-300 cursor-not-allowed'
                        ]"
                    >
                        Send Invitation
                    </button>
                </div>
            </template>
        </Dialog>

        <!-- Add these new dialogs -->
        <Dialog v-model:visible="commentDialog" 
            modal 
            header="Add Comment" 
            :style="{ width: '30rem' }">
            <div class="p-4">
                <textarea
                    v-model="newComment"
                    rows="4"
                    class="w-full p-3 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring focus:ring-blue-200"
                    placeholder="Enter your comment here..."
                ></textarea>
            </div>
            <template #footer>
                <div class="flex justify-end gap-2">
                    <button @click="commentDialog = false"
                        class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                        Cancel
                    </button>
                    <button @click="saveComment"
                        :class="`px-4 py-2 bg-${props.theme}-600 text-white hover:bg-${props.theme}-700 rounded-lg transition-colors`">
                        Save Comment
                    </button>
                </div>
            </template>
        </Dialog>

        <Dialog v-model:visible="activityDetailDialog" 
            modal 
            :header="selectedActivity?.title || 'Activity Details'" 
            :style="{ width: '50vw' }" 
            :breakpoints="{ '960px': '75vw', '641px': '90vw' }">
            <div v-if="selectedActivity" class="p-6">
                <div class="space-y-6">
                    <img :src="selectedActivity.image" 
                        :alt="selectedActivity.title"
                        class="w-full h-64 object-cover rounded-xl">

                    <div class="bg-gray-50 p-4 rounded-xl">
                        <h3 class="text-lg font-semibold text-gray-800 mb-4">Activity Overview</h3>
                        <div class="space-y-4">
                            <div>
                                <h4 class="text-sm font-medium text-gray-600">Description</h4>
                                <p class="text-gray-800 mt-1">{{ selectedActivity.description }}</p>
                            </div>
                            
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <h4 class="text-sm font-medium text-gray-600">Activity Type</h4>
                                    <p class="text-gray-800 mt-1">{{ selectedActivity.type || 'Class Activity' }}</p>
                                </div>
                                <div>
                                    <h4 class="text-sm font-medium text-gray-600">Date Assigned</h4>
                                    <p class="text-gray-800 mt-1">{{ selectedActivity.dateAssigned || 'Not specified' }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Head, usePage } from '@inertiajs/vue3';
import MainLayout from '@/Layouts/MainLayout.vue';
import Dialog from 'primevue/dialog';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';

const page = usePage();
const auth = computed(() => page.props.auth);

const props = defineProps({
    className: {
        type: String,
        required: true
    },
    theme: {
        type: String,
        default: 'emerald'
    }
});

// Computed theme classes
const themeClasses = computed(() => ({
    header: `bg-${props.theme}-400`,
    badge: `bg-${props.theme}-200`,
    memberHeader: `bg-${props.theme}-600`,
    buttons: `bg-${props.theme}-500`,
    activeTab: `bg-${props.theme}-400`
}));

const activeTab = ref('pupil');
const activeContentTab = ref('portfolio');
const activePortfolioTab = ref('recent');

// Tab configurations
const tabs = [
    { id: 'pupil', name: 'Pupil', icon: 'pi-users' },
    { id: 'schedule', name: 'Schedule', icon: 'pi-calendar' }
];

const contentTabs = [
    { id: 'portfolio', name: 'Portfolio', icon: 'pi-images' },
    { id: 'progress', name: 'Progress Record', icon: 'pi-chart-line' }
];

const portfolioTabs = [
    { id: 'recent', name: 'Recent' },
    { id: 'shared', name: 'Shared' }
];

// Sample student data
const selectedStudent = ref(null);
const students = [
    { 
        id: 'STD001', 
        name: 'Alice Smith', 
        initial: 'A',
        portfolios: [
            { id: 1, title: 'Portfolio Item 1', addedDate: '2 days ago' },
            { id: 2, title: 'Portfolio Item 2', addedDate: '2 days ago' },
            { id: 3, title: 'Portfolio Item 3', addedDate: '2 days ago' },
            { id: 4, title: 'Portfolio Item 4', addedDate: '3 days ago' },
            { id: 5, title: 'Portfolio Item 5', addedDate: '3 days ago' },
            { id: 6, title: 'Portfolio Item 6', addedDate: '4 days ago' },
        ]
    },
    { 
        id: 'STD002', 
        name: 'Bob Johnson', 
        initial: 'B',
        portfolios: [
            { id: 7, title: 'Portfolio Item 1', addedDate: '1 day ago' },
            { id: 8, title: 'Portfolio Item 2', addedDate: '1 day ago' },
            { id: 9, title: 'Portfolio Item 3', addedDate: '2 days ago' },
        ]
    },
    { id: 'STD003', name: 'Carol Williams', initial: 'C', portfolios: [] },
    { id: 'STD004', name: 'David Brown', initial: 'D', portfolios: [] },
];

// Set first student as default selected
onMounted(() => {
    selectedStudent.value = students[0];
});

// Add these for the calendar functionality
const selectedDate = ref(null);

// Generate random schedule
const generateRandomSchedule = () => {
    const times = [
        '8:00 AM - 9:30 AM',
        '9:45 AM - 11:15 AM',
        '1:00 PM - 2:30 PM',
        '2:45 PM - 4:15 PM'
    ];
    
    return Array.from({ length: 30 }, () => ({
        time: times[Math.floor(Math.random() * times.length)]
    }));
};

const schedule = ref(generateRandomSchedule());

// Helper function to determine if it's a class day (Monday & Wednesday)
const isClassDay = (date) => {
    const dayOfWeek = new Date(2025, 10, date).getDay(); // 0 = Sunday, 1 = Monday, etc.
    return dayOfWeek === 1 || dayOfWeek === 3; // Monday or Wednesday
};

// Show schedule details
const showScheduleDetails = (date) => {
    selectedDate.value = date;
};

// Add Student Dialog State
const showAddStudentDialog = ref(false);
const classroomCode = ref(generateClassCode()); // Generate on component mount
const copied = ref(false);

// Generate random classroom code
function generateClassCode() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    return Array.from({ length: 6 }, () => 
        chars.charAt(Math.floor(Math.random() * chars.length))
    ).join('');
}

// Copy code to clipboard
const copyCode = async () => {
    await navigator.clipboard.writeText(classroomCode.value);
    copied.value = true;
    setTimeout(() => copied.value = false, 2000);
};

// Copy join link
const copyLink = async () => {
    await navigator.clipboard.writeText(`https://yourapp.com/join/${classroomCode.value}`);
    // Show success message or toast
};

// Modified student state
const newStudent = ref({
    email: '',
    name: '', // Will be set after email verification
    initial: '',
    portfolios: []
});

// Modified validation
const isValidStudent = computed(() => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(newStudent.value.email);
});

// Modified add student function
const addStudent = () => {
    if (!isValidStudent.value) return;

    // In a real application, you would:
    // 1. Send invitation email to the student
    // 2. Create a pending invitation in the database
    // 3. Wait for the student to accept and complete their profile

    // For demo purposes, we'll create the student immediately
    const student = {
        id: newStudent.value.email, // Use email as ID
        email: newStudent.value.email,
        name: newStudent.value.email.split('@')[0], // Temporary name from email
        initial: newStudent.value.email[0].toUpperCase(),
        portfolios: []
    };

    students.push(student);
    showAddStudentDialog.value = false;
    newStudent.value = { email: '' };
    selectedStudent.value = student;
};

// Open dialog function
const openAddStudentDialog = () => {
    newStudent.value = { email: '' }; // Reset form
    showAddStudentDialog.value = true;
};

// Add these new refs and data
const commentDialog = ref(false);
const activityDetailDialog = ref(false);
const selectedActivity = ref(null);
const newComment = ref('');

const studentActivities = ref([
    { 
        id: 1, 
        studentId: 'STD001',
        title: "Activity 1", 
        description: "Science experiment on gravity.", 
        image: "/assets/images/activity1.jpg",
        comment: null
    },
    { 
        id: 2, 
        studentId: 'STD001',
        title: "Activity 2", 
        description: "Math quiz results in advanced algebra.", 
        image: "/assets/images/activity2.jpg",
        comment: null
    },
    {
        id: 3,
        studentId: 'STD002',
        title: "Activity 3", 
        description: "Watercolor painting of local wildlife.", 
        image: "/assets/images/activity3.jpg",
        comment: null
    },
    {
        id: 4,
        studentId: 'STD002',
        title: "Activity 4", 
        description: "History essay on Ancient Egyptian civilization.", 
        image: "/assets/images/activity4.jpg",
        comment: null
    },
    {
        id: 5,
        studentId: 'STD003',
        title: "Activity 5", 
        description: "Chemistry lab experiments on chemical reactions.", 
        image: "/assets/images/activity5.jpg",
        comment: null
    },
    {
        id: 6,
        studentId: 'STD003',
        title: "Activity 6", 
        description: "Literature analysis of Shakespeare's Macbeth.", 
        image: "/assets/images/activity6.jpg",
        comment: null
    }
]);

const sharedActivities = ref([
    { 
        id: 1, 
        studentId: 'STD001',
        title: "Group Project", 
        description: "Led team research on renewable energy sources.", 
        image: "/assets/images/group-project.jpg",
        comment: null
    },
    { 
        id: 2, 
        studentId: 'STD001',
        title: "Class Presentation", 
        description: "Presented findings on climate change impact.", 
        image: "/assets/images/presentation.jpg",
        comment: null
    },
    {
        id: 3,
        studentId: 'STD002',
        title: "Team Debate", 
        description: "Participated in inter-class debate competition.", 
        image: "/assets/images/debate.jpg",
        comment: null
    },
    {
        id: 4,
        studentId: 'STD002',
        title: "Music Performance", 
        description: "Performed in school orchestra concert.", 
        image: "/assets/images/music.jpg",
        comment: null
    },
    {
        id: 5,
        studentId: 'STD003',
        title: "Sports Tournament", 
        description: "Won second place in school basketball tournament.", 
        image: "/assets/images/sports.jpg",
        comment: null
    },
    {
        id: 6,
        studentId: 'STD003',
        title: "Art Exhibition", 
        description: "Displayed artwork in school gallery.", 
        image: "/assets/images/art-exhibit.jpg",
        comment: null
    }
]);

// Update the portfolio grid section to filter activities by selected student
const filteredActivities = computed(() => {
    if (!selectedStudent.value) return [];
    return activePortfolioTab.value === 'recent'
        ? studentActivities.value.filter(activity => activity.studentId === selectedStudent.value.id)
        : sharedActivities.value.filter(activity => activity.studentId === selectedStudent.value.id);
});

// Add these new methods
const addComment = (activity) => {
    selectedActivity.value = activity;
    newComment.value = activity.comment || '';
    commentDialog.value = true;
};

const saveComment = () => {
    if (selectedActivity.value && newComment.value.trim()) {
        selectedActivity.value.comment = newComment.value;
        selectedActivity.value.commentDate = new Date().toLocaleDateString();
        commentDialog.value = false;
        selectedActivity.value = null;
        newComment.value = '';
    }
};

const showActivityDetails = (activity) => {
    selectedActivity.value = activity;
    activityDetailDialog.value = true;
};

// Add these refs and computed properties
const searchQuery = ref("");
const remarksDate = ref("");
const records = ref([
    // Records for Alice Smith (STD001)
    { 
        studentId: 'STD001',
        subject: "Math", 
        output: "Algebra Quiz", 
        dueDate: "10/10/24 - 10/22/24", 
        time: "12:00 PM", 
        status: "Passed", 
        history: "Last Edit 5 days ago" 
    },
    { 
        studentId: 'STD001',
        subject: "Science", 
        output: "Physics Lab Report", 
        dueDate: "12/12/24 - 12/16/24", 
        time: "3:30 PM", 
        status: "Missing", 
        history: "Last Edit 2 days ago" 
    },
    
    // Records for Bob Johnson (STD002)
    { 
        studentId: 'STD002',
        subject: "English", 
        output: "Literature Essay", 
        dueDate: "12/12/24 - 12/16/24", 
        time: "3:30 PM", 
        status: "Passed", 
        history: "Last Edit 2 days ago" 
    },
    { 
        studentId: 'STD002',
        subject: "Art", 
        output: "Landscape Painting", 
        dueDate: "01/15/25 - 01/20/25", 
        time: "2:00 PM", 
        status: "Missing", 
        history: "Last Edit 3 days ago" 
    },

    // Records for Carol Williams (STD003)
    { 
        studentId: 'STD003',
        subject: "Chemistry", 
        output: "Chemical Reactions Lab", 
        dueDate: "02/10/25 - 02/15/25", 
        time: "1:00 PM", 
        status: "Passed", 
        history: "Last Edit 1 day ago" 
    },
    { 
        studentId: 'STD003',
        subject: "History", 
        output: "World War II Essay", 
        dueDate: "03/05/25 - 03/10/25", 
        time: "11:00 AM", 
        status: "Missing", 
        history: "Last Edit 4 days ago" 
    }
]);

// Update the filtered records computed property to filter by both search query and selected student
const filteredRecords = computed(() => {
    // First filter by selected student
    let studentRecords = records.value.filter(record => 
        record.studentId === selectedStudent.value?.id
    );
    
    // Then apply search filter if there's a query
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        return studentRecords.filter(record => 
            record.subject.toLowerCase().includes(query) ||
            record.output.toLowerCase().includes(query) ||
            record.status.toLowerCase().includes(query) ||
            record.history.toLowerCase().includes(query)
        );
    }
    
    return studentRecords;
});

// Update the completed and pending counts to only count selected student's records
const completedCount = computed(() => {
    return records.value.filter(record => 
        record.studentId === selectedStudent.value?.id && 
        record.status === "Passed"
    ).length;
});

const pendingCount = computed(() => {
    return records.value.filter(record => 
        record.studentId === selectedStudent.value?.id && 
        record.status === "Missing"
    ).length;
});

// Add a computed property for student-specific remarks
const studentRemarks = computed(() => {
    const remarks = {
        'STD001': {
            text: "Alice shows excellent progress in mathematics and consistent effort in science subjects.",
            date: "February 15, 2024"
        },
        'STD002': {
            text: "Bob demonstrates strong creative abilities and has improved significantly in written assignments.",
            date: "February 14, 2024"
        },
        'STD003': {
            text: "Carol excels in laboratory work and shows great attention to detail in all assignments.",
            date: "February 13, 2024"
        }
    };
    
    return remarks[selectedStudent.value?.id] || {
        text: "No remarks available yet.",
        date: new Date().toLocaleDateString()
    };
});

// Helper function to get status color based on status
const getStatusColor = (status) => {
    switch (status) {
        case 'Completed':
            return 'success';
        case 'Pending':
            return 'warning';
        default:
            return 'secondary';
    }
};

defineOptions({
    layout: MainLayout
});
</script>

<style scoped>
.aspect-video {
    aspect-ratio: 16 / 9;
}

/* Add these styles for consistent calendar styling */
.calendar-day {
    @apply p-4 border rounded-lg hover:shadow-md cursor-pointer transition-all;
}

.calendar-day-active {
    @apply font-semibold text-gray-800;
}

.calendar-time {
    @apply text-sm mt-1;
}

/* DataTable styles */
:deep(.p-datatable) {
    border-radius: 0.75rem;
    overflow: hidden;
    margin-top: 1rem;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
    background-color: #f8fafc;
    color: #1e293b;
    font-weight: 600;
    padding: 1rem;
    border-bottom: 2px solid #e2e8f0;
}

:deep(.p-datatable .p-datatable-tbody > tr) {
    transition: background-color 0.2s;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
    background-color: #f1f5f9;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
    padding: 1rem;
}

/* Responsive and transition styles */
@media (max-width: 1024px) {
    .lg\:w-64 {
        width: 100%;
    }
}

.bg-gradient-to-br {
    transition: all 0.3s ease;
}

.h-2 {
    transition: width 0.5s ease;
}
</style> 