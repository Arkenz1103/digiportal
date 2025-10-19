<!-- eslint-disable vue/no-unknown-at-rule -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-violet-50 p-6">
    <!-- Header Section with Student Info -->
    <div class="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg overflow-hidden mb-6 border border-indigo-100">
      <div class="bg-gradient-to-r from-indigo-600 to-violet-600 p-4">
        <!-- Student Info Section -->
        <div class="flex flex-col">
          <div class="flex items-start justify-between">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-white rounded-full flex items-center justify-center shadow-lg ring-2 ring-white/30">
                <span class="text-indigo-600 text-2xl font-bold">{{ studentInfo.initial }}</span>
              </div>
              <div>
                <h2 class="text-xl font-bold text-white mb-1.5">{{ studentInfo.name }}</h2>
                <div class="flex items-center gap-2">
                  <div class="inline-flex items-center gap-1.5 px-3 py-1 bg-white/20 backdrop-blur-sm rounded-lg border border-white/30">
                    <i class="pi pi-id-card text-white text-xs"></i>
                    <span class="text-white text-sm font-medium">{{ studentInfo.id }}</span>
                  </div>
                  <div class="inline-flex items-center gap-1.5 px-3 py-1 bg-white/20 backdrop-blur-sm rounded-lg border border-white/30">
                    <i class="pi pi-user text-white text-xs"></i>
                    <span class="text-white text-sm font-medium">Student</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Back Button -->
            <button @click="goBack" 
              class="flex items-center gap-2 px-4 py-2 bg-white text-indigo-700 hover:bg-indigo-50 rounded-lg transition-all shadow-md hover:shadow-lg text-sm font-medium">
              <i class="pi pi-arrow-left text-sm"></i>
              <span>Back to Student Progress</span>
            </button>
          </div>

          <!-- Teacher's Remarks Section -->
          <div class="mt-4 bg-white/20 backdrop-blur-sm p-4 rounded-lg border border-white/30">
            <div class="flex justify-between items-center mb-2">
              <div class="flex items-center gap-2">
                <div class="w-8 h-8 bg-white/30 rounded-lg flex items-center justify-center">
                  <i class="pi pi-comments text-white text-sm"></i>
                </div>
                <div>
                  <h3 class="text-base font-bold text-white">Recent Remarks</h3>
                  <span class="text-xs text-white/80">{{ remarksDate }} • {{ remarksTime }}</span>
                </div>
              </div>
              <button 
                @click="openRemarksDialog" 
                class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-white/20 backdrop-blur-sm rounded-lg border border-white/30 hover:bg-white/30 transition-all duration-200 shadow-sm hover:shadow-md">
                
                <span>View All</span>
              </button>
            </div>
            <p v-if="latestRemark" class="text-white/90 leading-relaxed">
              {{ latestRemark.text }}
            </p>
            <p v-else class="text-white/60 italic text-sm">
              No remarks yet for this student.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Table Section -->
    <div class="bg-white/80 backdrop-blur-sm p-6 rounded-xl shadow-sm border border-indigo-100">
      <div class="flex flex-col space-y-6">
        <!-- Statistics boxes -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            <!-- Total Activities -->
            <div 
                @click="setFilter('all')"
                class="bg-gradient-to-br from-indigo-50 to-white p-4 rounded-xl border shadow-sm cursor-pointer transition-all duration-200 hover:shadow-md transform hover:scale-105"
                :class="activeFilter === 'all' ? 'border-indigo-500 border-2 ring-2 ring-indigo-200' : 'border-indigo-100'">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center flex-shrink-0">
                        <i class="pi pi-book text-xl text-indigo-600"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                        <p class="text-sm text-indigo-600 font-semibold whitespace-nowrap">Total Activities</p>
                        <p class="text-2xl font-bold text-indigo-900">{{ records.length }}</p>
                    </div>
                </div>
            </div>

            <!-- Completed -->
            <div 
                @click="setFilter('completed')"
                class="bg-gradient-to-br from-green-50 to-white p-4 rounded-xl border shadow-sm cursor-pointer transition-all duration-200 hover:shadow-md transform hover:scale-105"
                :class="activeFilter === 'completed' ? 'border-green-500 border-2 ring-2 ring-green-200' : 'border-green-100'">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center flex-shrink-0">
                        <i class="pi pi-check text-xl text-green-600"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                        <p class="text-sm text-green-600 font-semibold whitespace-nowrap">Completed</p>
                        <p class="text-2xl font-bold text-green-700">{{ completedCount }}</p>
                    </div>
                </div>
            </div>

            <!-- Pending -->
            <div 
                @click="setFilter('pending')"
                class="bg-gradient-to-br from-amber-50 to-white p-4 rounded-xl border shadow-sm cursor-pointer transition-all duration-200 hover:shadow-md transform hover:scale-105"
                :class="activeFilter === 'pending' ? 'border-amber-500 border-2 ring-2 ring-amber-200' : 'border-amber-100'">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center flex-shrink-0">
                        <i class="pi pi-clock text-xl text-amber-600"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                        <p class="text-sm text-amber-600 font-semibold whitespace-nowrap">Pending</p>
                        <p class="text-2xl font-bold text-amber-700">{{ pendingCount }}</p>
                    </div>
                </div>
            </div>

            <!-- Missing -->
            <div 
                @click="setFilter('missing')"
                class="bg-gradient-to-br from-red-50 to-white p-4 rounded-xl border shadow-sm cursor-pointer transition-all duration-200 hover:shadow-md transform hover:scale-105"
                :class="activeFilter === 'missing' ? 'border-red-500 border-2 ring-2 ring-red-200' : 'border-red-100'">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center flex-shrink-0">
                        <i class="pi pi-times-circle text-xl text-red-600"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                        <p class="text-sm text-red-600 font-semibold whitespace-nowrap">Missing</p>
                        <p class="text-2xl font-bold text-red-700">{{ missingCount }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Search Bar -->
        <div class="w-full max-w-md">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by folder or activity..."
              class="w-full pl-10 pr-10 py-2 rounded-lg border-2 border-indigo-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-200 text-gray-700 placeholder-gray-400 text-sm shadow-sm"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <i class="pi pi-search text-indigo-500 text-sm"></i>
            </div>
            <button
              v-if="searchQuery"
              @click="searchQuery = ''"
              class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
            >
              <i class="pi pi-times text-xs"></i>
            </button>
          </div>
        </div>

        <!-- Search Results Notification -->
        <div v-if="searchQuery" 
          class="p-3 bg-indigo-50 border border-indigo-200 text-indigo-900 rounded-lg flex items-center gap-2">
          <i class="pi pi-filter text-indigo-600"></i>
          <span>Showing results for "<strong class="font-medium">{{ searchQuery }}</strong>"</span>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="flex justify-center items-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>

        <!-- Updated DataTable -->
        <DataTable v-else
          :value="paginatedRecords" 
          :scrollable="true" 
          scrollHeight="400px" 
          class="p-datatable-rounded"
          stripedRows
          showGridlines>
          <Column field="subject" header="Folder" class="font-semibold">
            <template #body="slotProps">
              <div class="flex items-center gap-2">
                <i class="pi pi-folder text-indigo-600"></i>
                <span class="font-medium text-indigo-900">{{ slotProps.data.subject }}</span>
              </div>
            </template>
          </Column>
          <Column field="output" header="Activity" style="min-width: 200px">
            <template #body="slotProps">
              <div>
                <div class="font-medium text-gray-900">{{ slotProps.data.output }}</div>
                <div class="text-xs text-gray-500">{{ slotProps.data.activityType }}</div>
              </div>
            </template>
          </Column>
          <Column field="dueDate" header="Due Date">
            <template #body="slotProps">
              <span class="text-sm text-gray-700">{{ slotProps.data.dueDate }}</span>
            </template>
          </Column>
          <Column field="status" header="Status">
            <template #body="slotProps">
              <span 
                class="px-3 py-1.5 text-sm rounded-lg font-medium inline-block"
                :class="{
                  'bg-green-100 text-green-800 border border-green-200': slotProps.data.status === 'Scored',
                  'bg-blue-100 text-blue-800 border border-blue-200': slotProps.data.status === 'Submitted',
                  'bg-amber-100 text-amber-700 border border-amber-300': slotProps.data.status === 'Pending',
                  'bg-red-100 text-red-800 border border-red-200': slotProps.data.status === 'Missing'
                }">
                {{ slotProps.data.status }}
              </span>
            </template>
          </Column>
          <Column field="score" header="Score">
            <template #body="slotProps">
              <span class="text-sm font-bold" :class="slotProps.data.score === 'N/A' ? 'text-gray-400' : 'text-green-700'">
                {{ slotProps.data.score }}
              </span>
            </template>
          </Column>
          <Column header="Actions" style="min-width: 120px">
            <template #body="slotProps">
              <button v-if="slotProps.data.filePath" 
                      @click="viewOutput(slotProps.data)"
                      class="px-3 py-1.5 bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200 transition-colors text-sm font-medium">
                <i class="pi pi-eye mr-1"></i>
                View
              </button>
              <span v-else class="text-xs text-gray-400">No output</span>
            </template>
          </Column>
        </DataTable>

        <!-- Load More Button -->
        <div v-if="!isLoading && hasMoreRecords" class="flex justify-center mt-6">
          <button
            @click="loadMore"
            class="flex flex-col items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-all duration-200 shadow-md hover:shadow-lg group"
          >
            <span class="text-sm font-medium">Load More Activities</span>
            <i class="pi pi-chevron-down text-lg group-hover:translate-y-1 transition-transform duration-200"></i>
          </button>
        </div>

        <!-- End of Records Message -->
        <div v-if="!isLoading && !hasMoreRecords && filteredRecords.length > 0" class="flex justify-center mt-6">
          <div class="text-sm text-gray-500 flex items-center gap-2">
            <i class="pi pi-check-circle text-indigo-600"></i>
            <span>All activities loaded</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- View Output Dialog -->
  <Dialog v-model:visible="showOutputDialog" modal header="View Student Output" :style="{width: '60vw'}" class="p-fluid">
    <div v-if="selectedOutput" class="space-y-4">
      <div class="bg-indigo-50 p-4 rounded-lg">
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <p class="text-sm text-indigo-600 font-medium">Activity</p>
            <p class="text-indigo-900 font-semibold">{{ selectedOutput.output }}</p>
          </div>
          <div>
            <p class="text-sm text-indigo-600 font-medium">Folder</p>
            <p class="text-indigo-900 font-semibold">{{ selectedOutput.subject }}</p>
          </div>
          <div>
            <p class="text-sm text-indigo-600 font-medium">Submitted</p>
            <p class="text-indigo-900">{{ selectedOutput.submittedDate }}</p>
          </div>
          <div>
            <p class="text-sm text-indigo-600 font-medium">Score</p>
            <p class="text-indigo-900 font-bold" :class="selectedOutput.score === 'N/A' ? 'text-gray-400' : 'text-green-600'">
              {{ selectedOutput.score }}
            </p>
          </div>
        </div>
        <div v-if="selectedOutput.caption">
          <p class="text-sm text-indigo-600 font-medium mb-1">Caption</p>
          <p class="text-indigo-900">{{ selectedOutput.caption }}</p>
        </div>
      </div>
      
      <div v-if="selectedOutput.fileType === 'image'" class="bg-gray-100 rounded-lg p-4 flex items-center justify-center">
        <img :src="selectedOutput.filePath" :alt="selectedOutput.output" class="max-w-full max-h-96 rounded shadow-lg">
      </div>
      <div v-else class="bg-gray-100 rounded-lg p-8 text-center">
        <i class="pi pi-file text-4xl text-gray-400 mb-2"></i>
        <p class="text-gray-600">{{ selectedOutput.fileType || 'File' }} submission</p>
      </div>
    </div>
  </Dialog>

  <!-- Remarks History Dialog -->
  <Dialog v-model:visible="showRemarksDialog" modal header="Remarks History" :style="{width: '700px', maxWidth: '90vw', height: '600px'}" class="p-fluid">
    <div class="space-y-4 h-full flex flex-col">
      <!-- Tabs -->
      <div class="flex gap-2 border-b border-indigo-200">
        <button 
          @click="remarksTab = 'all'"
          class="px-4 py-2 font-medium transition-colors duration-200"
          :class="remarksTab === 'all' 
            ? 'text-indigo-600 border-b-2 border-indigo-600' 
            : 'text-gray-500 hover:text-indigo-600'">
          All
        </button>
        <button 
          @click="remarksTab = 'unread'"
          class="px-4 py-2 font-medium transition-colors duration-200 flex items-center gap-2"
          :class="remarksTab === 'unread' 
            ? 'text-indigo-600 border-b-2 border-indigo-600' 
            : 'text-gray-500 hover:text-indigo-600'">
          Unread
          <span v-if="unreadRemarksCount > 0" class="bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
            {{ unreadRemarksCount }}
          </span>
        </button>
      </div>

      <!-- Remarks List -->
      <div v-if="filteredRemarks.length > 0" class="space-y-3 overflow-y-auto flex-1 pr-2">
        <div v-for="remark in filteredRemarks" :key="remark.id" 
             @click="openRemarkDetail(remark)"
             class="bg-white p-4 rounded-lg border-2 shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer"
             :class="remark.is_read ? 'border-indigo-100' : 'border-indigo-300 bg-indigo-50/30'">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2">
              <span class="font-semibold text-indigo-900">Remarked</span>
              <span v-if="!remark.is_read" class="text-xs text-blue-600 font-semibold">Unread</span>
            </div>
            <div class="flex flex-col items-end">
              <span class="text-sm text-indigo-600">{{ new Date(remark.created_at).toLocaleDateString() }}</span>
              <span class="text-xs text-indigo-500">{{ new Date(remark.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}</span>
            </div>
          </div>
          <p class="text-indigo-900/80 leading-relaxed line-clamp-2">{{ remark.text }}</p>
        </div>
      </div>
      <div v-else class="text-center py-8">
        <i class="pi pi-comments text-4xl text-indigo-200 mb-2"></i>
        <p class="text-indigo-400">
          {{ remarksTab === 'unread' ? 'No unread remarks' : 'No remarks history available' }}
        </p>
      </div>
    </div>
  </Dialog>

  <!-- Remark Detail Dialog -->
  <Dialog v-model:visible="showRemarkDetailDialog" modal header="Remark Details" :style="{width: '600px', maxWidth: '90vw'}" class="p-fluid">
    <div v-if="selectedRemark" class="space-y-4">
      <!-- Remark Header -->
      <div class="bg-gradient-to-r from-indigo-50 to-violet-50 p-4 rounded-lg border border-indigo-200">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center gap-2">
            <i class="pi pi-comments text-indigo-600 text-xl"></i>
            <span class="font-bold text-indigo-900 text-lg">Remarked</span>
          </div>
          <div class="flex flex-col items-end">
            <span class="text-sm font-medium text-indigo-700">{{ new Date(selectedRemark.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) }}</span>
            <span class="text-xs text-indigo-600">{{ new Date(selectedRemark.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}</span>
          </div>
        </div>
      </div>

      <!-- Remark Content -->
      <div class="bg-white p-5 rounded-lg border-2 border-indigo-100 shadow-sm">
        <p class="text-indigo-900 leading-relaxed whitespace-pre-wrap text-base">{{ selectedRemark.text }}</p>
      </div>

      <!-- Student Info -->
      <div class="flex items-center gap-3 p-3 bg-indigo-50 rounded-lg">
        <i class="pi pi-user text-indigo-600"></i>
        <div>
          <p class="text-sm text-indigo-600 font-medium">Student</p>
          <p class="text-indigo-900 font-semibold">{{ studentInfo.name }}</p>
        </div>
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import axios from 'axios';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';

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

const currentClassName = ref('All Classes');

const searchQuery = ref("");
const records = ref([]);
const isLoading = ref(false);
const portfolioFolders = ref([]);
const displayLimit = ref(10);
const activeFilter = ref('all');
const studentRemarks = ref([]);
const latestRemark = ref(null);

// Load student submissions
const loadStudentWork = async (studentId) => {
    isLoading.value = true;
    console.log('🔍 loadStudentWork called with studentId:', studentId);
    console.log('   Type:', typeof studentId);
    
    try {
        // Load portfolio folders
        const foldersResponse = await axios.get('/api/portfolio/folders/');
        portfolioFolders.value = foldersResponse.data || [];
        console.log('📁 Loaded portfolio folders:', portfolioFolders.value.length);
        
        const allRecords = [];
        
        // Load submissions for each folder
        for (const folder of portfolioFolders.value) {
            console.log(`\n📂 Processing folder: ${folder.name} (ID: ${folder.id})`);
            try {
                const activitiesResponse = await axios.get(`/api/portfolio/folders/${folder.id}/activities/`);
                const activities = activitiesResponse.data || [];
                
                for (const activity of activities) {
                    console.log(`   📝 Activity: ${activity.title} (ID: ${activity.id})`);
                    try {
                        const submissionsResponse = await axios.get(`/api/activities/${activity.id}/submissions/`);
                        const submissions = submissionsResponse.data || [];
                        console.log(`      Total submissions: ${submissions.length}`);
                        
                        // Filter submissions for this student
                        // Compare using database ID (numeric comparison)
                        const studentSubmissions = submissions.filter(sub => {
                            const submissionStudentId = sub.student?.id || sub.student_id;
                            const match = Number(submissionStudentId) === Number(studentId) || 
                                   sub.student?.username === studentId;
                            if (submissions.length > 0 && submissions.indexOf(sub) === 0) {
                                console.log(`      Checking submission - Student ID: ${submissionStudentId}, Looking for: ${studentId}, Match: ${match}`);
                            }
                            return match;
                        });
                        console.log(`      Student submissions found: ${studentSubmissions.length}`);
                        
                        if (studentSubmissions.length > 0) {
                            studentSubmissions.forEach(submission => {
                                // Calculate score display
                                let scoreDisplay = 'N/A';
                                let totalScore = submission.total_score;
                                let maxScore = submission.max_score;
                                
                                // Try to calculate from criteria_scores if available
                                if (submission.criteria_scores) {
                                    try {
                                        const criteria = typeof submission.criteria_scores === 'string' 
                                            ? JSON.parse(submission.criteria_scores) 
                                            : submission.criteria_scores;
                                        
                                        if (Array.isArray(criteria) && criteria.length > 0) {
                                            totalScore = criteria.reduce((sum, c) => sum + (parseInt(c.score) || 0), 0);
                                            maxScore = criteria.reduce((sum, c) => sum + (parseInt(c.maxScore) || 0), 0);
                                        }
                                    } catch (error) {
                                        console.error('Error parsing criteria_scores:', error);
                                    }
                                }
                                
                                // Format score display
                                if (totalScore !== null && totalScore !== undefined && 
                                    maxScore !== null && maxScore !== undefined) {
                                    scoreDisplay = `${totalScore}/${maxScore}`;
                                } else if (submission.score !== null && submission.score !== undefined) {
                                    scoreDisplay = `${submission.score}/10`;
                                }
                                
                                allRecords.push({
                                    subject: folder.name,
                                    output: activity.title,
                                    activityType: activity.activity_type,
                                    dueDate: activity.due_date ? new Date(activity.due_date).toLocaleDateString() : 'N/A',
                                    dueDateRaw: activity.due_date,
                                    submittedDate: new Date(submission.submitted_at).toLocaleDateString(),
                                    time: new Date(submission.submitted_at).toLocaleTimeString(),
                                    status: submission.status === 'scored' ? 'Scored' : 'Submitted',
                                    score: scoreDisplay,
                                    history: `Submitted ${getTimeAgo(submission.submitted_at)}`,
                                    fileType: submission.file_type,
                                    filePath: submission.file_path,
                                    caption: submission.caption
                                });
                            });
                        } else {
                            // Determine status based on due date
                            const now = new Date();
                            const dueDate = activity.due_date ? new Date(activity.due_date) : null;
                            let status = 'Pending';
                            
                            if (dueDate && now > dueDate) {
                                status = 'Missing'; // Past due date
                            }
                            
                            // Show activity even if not submitted
                            allRecords.push({
                                subject: folder.name,
                                output: activity.title,
                                activityType: activity.activity_type,
                                dueDate: activity.due_date ? new Date(activity.due_date).toLocaleDateString() : 'N/A',
                                dueDateRaw: activity.due_date,
                                submittedDate: 'Not submitted',
                                time: '-',
                                status: status,
                                score: 'N/A',
                                history: 'Not submitted',
                                fileType: null,
                                filePath: null,
                                caption: null
                            });
                        }
                    } catch (error) {
                        console.error(`Error loading submissions for activity ${activity.id}:`, error);
                    }
                }
            } catch (error) {
                console.error(`Error loading activities for folder ${folder.id}:`, error);
            }
        }
        
        records.value = allRecords;
        console.log('\n✅ SUMMARY:');
        console.log(`   Total records loaded: ${records.value.length}`);
        console.log(`   Folders processed: ${portfolioFolders.value.length}`);
        console.log('   Records:', records.value);
    } catch (error) {
        console.error('❌ Error loading student work:', error);
    } finally {
        isLoading.value = false;
    }
};

// Helper function to get time ago
const getTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    
    if (seconds < 60) return 'just now';
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    const days = Math.floor(hours / 24);
    if (days < 7) return `${days} day${days > 1 ? 's' : ''} ago`;
    return date.toLocaleDateString();
};

const filteredRecords = computed(() => {
    let filtered = records.value;
    
    // Filter by status
    if (activeFilter.value !== 'all') {
        if (activeFilter.value === 'completed') {
            filtered = filtered.filter(record => 
                record.status === 'Scored' || record.status === 'Submitted'
            );
        } else if (activeFilter.value === 'pending') {
            filtered = filtered.filter(record => record.status === 'Pending');
        } else if (activeFilter.value === 'missing') {
            filtered = filtered.filter(record => record.status === 'Missing');
        }
    }
    
    // Filter by search query
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase().trim();
        filtered = filtered.filter(record => 
            record.subject.toLowerCase().includes(query) ||
            record.output.toLowerCase().includes(query) ||
            record.activityType.toLowerCase().includes(query)
        );
    }
    
    return filtered;
});

const paginatedRecords = computed(() => {
    return filteredRecords.value.slice(0, displayLimit.value);
});

const hasMoreRecords = computed(() => {
    return filteredRecords.value.length > displayLimit.value;
});

const loadMore = () => {
    displayLimit.value += 10;
};

const getStatusColor = (status) => {
    switch (status) {
        case "Scored": return "success";
        case "Submitted": return "info";
        case "Pending": return "warning";
        case "Missing": return "danger";
        default: return "warning";
    }
};

// View output dialog
const showOutputDialog = ref(false);
const selectedOutput = ref(null);

const viewOutput = (output) => {
    selectedOutput.value = output;
    showOutputDialog.value = true;
};

const props = defineProps({
    selectedStudent: {
        type: Object,
        required: false,
        default: () => ({
            id: 'N/A',
            name: 'Unknown Student'
        })
    }
});

// Student info - get from localStorage
const studentData = ref(null);

const studentInfo = computed(() => ({
    name: studentData.value?.name || props.selectedStudent?.name || 'Unknown Student',
    id: studentData.value?.id || props.selectedStudent?.id || 'N/A',
    initial: ((studentData.value?.name || props.selectedStudent?.name || '?').charAt(0))
}));

onMounted(() => {
    console.log('Progress.vue mounted');
    
    // Get student data from localStorage (set by Sprogress.vue)
    const stored = localStorage.getItem('selected_student_progress');
    if (stored) {
        try {
            const data = JSON.parse(stored);
            studentData.value = data.student;
            console.log('Loaded student from localStorage:', studentData.value);
            console.log('Student display ID:', studentData.value?.id);
            console.log('Student database ID:', studentData.value?.dbId);
            
            // Load the student's work using database ID (dbId), not display ID
            const studentIdToUse = studentData.value?.dbId || studentData.value?.id;
            if (studentIdToUse) {
                console.log('Loading student work for database ID:', studentIdToUse);
                loadStudentWork(studentIdToUse);
                loadStudentRemarks(studentIdToUse);
            } else {
                console.error('No valid student ID found');
            }
        } catch (error) {
            console.error('Error parsing student data:', error);
        }
    } else {
        console.warn('No student data in localStorage');
    }
});

const goBack = () => {
    // Navigate back to student progress page using emit
    emit('navigate', 'TeacherSprogress');
};

const remarksDate = ref(new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
}));

const remarksTime = ref(new Date().toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
}));

const showRemarksDialog = ref(false);
const remarksTab = ref('all');
const showRemarkDetailDialog = ref(false);
const selectedRemark = ref(null);

// Load student remarks from API
const loadStudentRemarks = async (studentId) => {
    try {
        const response = await axios.get(`/api/remarks/?student_id=${studentId}`);
        if (response.data) {
            // Use is_read from backend
            studentRemarks.value = response.data;
            // Set latest remark
            if (response.data.length > 0) {
                latestRemark.value = response.data[0];
            }
            console.log('Loaded student remarks:', response.data.length);
        }
    } catch (error) {
        console.error('Error loading student remarks:', error);
    }
};

const openRemarksDialog = () => {
    showRemarksDialog.value = true;
};

// Filtered remarks based on tab
const filteredRemarks = computed(() => {
    if (remarksTab.value === 'unread') {
        return studentRemarks.value.filter(remark => !remark.is_read);
    }
    return studentRemarks.value;
});

// Count unread remarks
const unreadRemarksCount = computed(() => {
    return studentRemarks.value.filter(remark => !remark.is_read).length;
});

// Get CSRF token from cookie
const getCsrfToken = () => {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

// Open remark detail dialog and mark as read for current user
const openRemarkDetail = async (remark) => {
    selectedRemark.value = remark;
    showRemarkDetailDialog.value = true;
    
    // Mark as read for the current user (teacher)
    if (!remark.is_read) {
        try {
            console.log('Marking remark as read for current user:', remark.id);
            const csrfToken = getCsrfToken();
            const response = await axios.post(`/api/remarks/${remark.id}/mark-read/`, {}, {
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });
            console.log('Mark as read response:', response.data);
            remark.is_read = true;
            console.log('Remark marked as read successfully for current user');
        } catch (error) {
            console.error('Error marking remark as read:', error);
            console.error('Error response:', error.response?.data);
        }
    }
};

const completedCount = computed(() => {
    return records.value.filter(record => record.status === "Scored" || record.status === "Submitted").length;
});

const pendingCount = computed(() => {
    return records.value.filter(record => record.status === "Pending").length;
});

const missingCount = computed(() => {
    return records.value.filter(record => record.status === "Missing").length;
});

// Reset display limit when search query or filter changes
watch([searchQuery, activeFilter], () => {
    displayLimit.value = 10;
});

const setFilter = (filter) => {
    activeFilter.value = filter;
};
</script>

<script>
import TeacherLayout from '@/Layouts/MainLayout.vue';

export default {
    layout: TeacherLayout
};
</script>

<style scoped>
/* stylelint-disable at-rule-no-unknown */
/* Tailwind @apply directives - linter warnings can be ignored */
input:focus {
    outline: none;
    @apply ring-2 ring-indigo-200 border-indigo-400;
}

:deep(.p-datatable) {
    @apply rounded-lg overflow-hidden mt-4 border border-indigo-100;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
    @apply bg-indigo-50 text-indigo-900 font-semibold p-4 border-b border-indigo-100;
}

:deep(.p-datatable .p-datatable-tbody > tr) {
    @apply transition-colors duration-200;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
    @apply bg-indigo-50;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
    @apply p-4 border-b border-indigo-50;
}

:deep(.p-datatable .p-datatable-tbody > tr:last-child > td) {
    @apply border-b-0;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
    .lg\:w-64 {
        @apply w-full;
    }
}

/* Smooth transitions */
.bg-gradient-to-br {
    @apply transition-all duration-300 ease-in-out;
}

/* Custom scrollbar */
:deep(::-webkit-scrollbar) {
    @apply w-2 h-2;
}

:deep(::-webkit-scrollbar-track) {
    @apply bg-indigo-50 rounded-full;
}

:deep(::-webkit-scrollbar-thumb) {
    @apply bg-indigo-200 rounded-full hover:bg-indigo-300;
}

/* Dialog styles */
:deep(.p-dialog) {
    @apply rounded-xl overflow-hidden shadow-xl border border-indigo-100;
}

:deep(.p-dialog .p-dialog-header) {
    @apply bg-indigo-50 border-b border-indigo-100 p-4;
}

:deep(.p-dialog .p-dialog-content) {
    @apply bg-white p-6;
}

:deep(.p-dialog .p-dialog-footer) {
    @apply bg-indigo-50 border-t border-indigo-100 p-4 flex justify-end gap-2;
}

/* Tag styles */
:deep(.p-tag) {
    @apply px-3 py-1.5 text-sm rounded-lg;
}

:deep(.p-tag.p-tag-success) {
    @apply bg-green-100 text-green-800 border border-green-200;
}

:deep(.p-tag.p-tag-danger) {
    @apply bg-red-100 text-red-800 border border-red-200;
}

:deep(.p-tag.p-tag-warning) {
    background-color: #fef3c7 !important;
    color: #d97706 !important;
    border: 1px solid #fcd34d !important;
}

:deep(.p-tag.p-tag-info) {
    @apply bg-blue-100 text-blue-800 border border-blue-200;
}
</style>