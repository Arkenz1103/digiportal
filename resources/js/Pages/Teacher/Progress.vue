<template>
  <div class="p-6 max-w-7xl mx-auto min-h-screen bg-gradient-to-br from-indigo-50 via-violet-50 to-blue-50">
    <!-- Header Section with Student Info -->
    <div class="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg overflow-hidden mb-6 border border-indigo-100">
      <div class="bg-gradient-to-r from-indigo-600 to-violet-600 p-6">
        <!-- Student Info Section -->
        <div class="flex flex-col">
          <div class="flex items-start justify-between">
            <div class="flex items-center gap-6">
              <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center shadow-lg ring-4 ring-white/30">
                <span class="text-indigo-600 text-3xl font-bold">{{ studentInfo.initial }}</span>
              </div>
              <div>
                <h2 class="text-2xl font-bold text-white mb-2">{{ studentInfo.name }}</h2>
                <div class="flex items-center gap-3">
                  <div class="inline-flex items-center gap-2 px-4 py-2 bg-white/20 backdrop-blur-sm rounded-lg border border-white/30">
                    <i class="pi pi-id-card text-white"></i>
                    <span class="text-white font-medium">{{ studentInfo.id }}</span>
                  </div>
                  <div class="inline-flex items-center gap-2 px-4 py-2 bg-white/20 backdrop-blur-sm rounded-lg border border-white/30">
                    <i class="pi pi-user text-white"></i>
                    <span class="text-white font-medium">Student</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Back Button -->
            <button @click="goBack" 
              class="flex items-center gap-2 px-5 py-2.5 bg-white text-indigo-700 hover:bg-indigo-50 rounded-lg transition-all shadow-md hover:shadow-lg font-medium">
              <i class="pi pi-arrow-left"></i>
              <span>Back to Student Progress</span>
            </button>
          </div>

          <!-- Teacher's Remarks Section -->
          <div class="mt-6 bg-white/20 backdrop-blur-sm p-5 rounded-lg border border-white/30">
            <div class="flex justify-between items-center mb-3">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-white/30 rounded-lg flex items-center justify-center">
                  <i class="pi pi-comments text-white text-lg"></i>
                </div>
                <div>
                  <h3 class="text-lg font-bold text-white">Teacher's Remarks</h3>
                  <span class="text-xs text-white/80">{{ remarksDate }}</span>
                </div>
              </div>
              <button @click="openRemarksDialog" class="text-sm text-white hover:text-white/80 font-medium transition-colors flex items-center gap-2 px-3 py-1.5 bg-white/20 rounded-lg hover:bg-white/30">
                View All
                <i class="pi pi-angle-right text-xs"></i>
              </button>
            </div>
            <p class="text-white/90 leading-relaxed">
              "{{ studentInfo.name }}" has shown consistent improvement in completing assignments on time. 
              Actively participates in class discussions and demonstrates a strong understanding of course material. 
              Shows particular strength in creative problem-solving.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Table Section -->
    <div class="bg-white/80 backdrop-blur-sm p-6 rounded-xl shadow-sm border border-indigo-100">
      <div class="flex flex-col space-y-6">
        <!-- Top row with statistics and search -->
        <div class="flex flex-col lg:flex-row gap-4">
          <!-- Search on the left -->
          <div class="w-full lg:w-1/3">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search outputs..."
                class="w-full pl-12 pr-4 py-2.5 rounded-lg border border-indigo-200 focus:border-indigo-500 focus:ring focus:ring-indigo-200 transition-all duration-200 text-gray-700 placeholder-indigo-400"
              />
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <i class="pi pi-search text-indigo-500"></i>
              </div>
            </div>
          </div>

            <!-- Statistics on the right -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 flex-1">
            <!-- Total Activities -->
            <div class="bg-gradient-to-br from-indigo-50 to-white p-4 rounded-lg border border-indigo-100 shadow-sm">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center">
                        <i class="pi pi-book text-xl text-indigo-600"></i>
                    </div>
                    <div>
                        <p class="text-xs text-indigo-600">Total Activities</p>
                        <p class="text-lg font-bold text-indigo-900">{{ records.length }}</p>
                    </div>
                </div>
            </div>

            <!-- Completed -->
            <div class="bg-gradient-to-br from-green-50 to-white p-4 rounded-lg border border-green-100 shadow-sm">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                        <i class="pi pi-check text-xl text-green-600"></i>
                    </div>
                    <div>
                        <p class="text-xs text-green-600">Completed</p>
                        <p class="text-lg font-bold text-indigo-900">{{ completedCount }}</p>
                    </div>
                </div>
            </div>

            <!-- Pending -->
            <div class="bg-gradient-to-br from-amber-50 to-white p-4 rounded-lg border border-amber-100 shadow-sm">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center">
                        <i class="pi pi-clock text-xl text-amber-600"></i>
                    </div>
                    <div>
                        <p class="text-xs text-amber-600">Pending</p>
                        <p class="text-lg font-bold text-indigo-900">{{ pendingCount }}</p>
                    </div>
                </div>
            </div>
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
          :value="filteredRecords" 
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
          <Column field="submittedDate" header="Submitted">
            <template #body="slotProps">
              <span class="text-sm" :class="slotProps.data.submittedDate === 'Not submitted' ? 'text-red-600 font-medium' : 'text-gray-700'">
                {{ slotProps.data.submittedDate }}
              </span>
            </template>
          </Column>
          <Column field="score" header="Score">
            <template #body="slotProps">
              <span class="text-sm font-bold" :class="slotProps.data.score === 'N/A' ? 'text-gray-400' : 'text-green-600'">
                {{ slotProps.data.score }}
              </span>
            </template>
          </Column>
          <Column field="status" header="Status">
            <template #body="slotProps">
              <Tag :value="slotProps.data.status" 
                   :severity="getStatusColor(slotProps.data.status)"
                   class="text-sm" />
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
  <Dialog v-model:visible="showRemarksDialog" modal header="Remarks History" :style="{width: '50vw'}" class="p-fluid">
    <div class="space-y-4">
      <!-- Current Remarks -->
      <div class="bg-indigo-50 p-4 rounded-lg border border-indigo-100">
        <div class="flex items-center justify-between mb-3">
          <span class="font-semibold text-indigo-900">Current Remarks</span>
          <span class="text-sm text-white bg-gradient-to-r from-indigo-500 to-violet-500 px-3 py-1 rounded-full">{{ remarksDate }}</span>
        </div>
        <p class="text-indigo-900/80 leading-relaxed">
          "{{ studentInfo.name }}" has shown consistent improvement in completing assignments on time. 
          Actively participates in class discussions and demonstrates a strong understanding of course material. 
          Shows particular strength in creative problem-solving.
        </p>
      </div>

      <!-- Previous Remarks -->
      <div v-for="(remark, index) in remarksHistory" :key="index" 
           class="bg-white p-4 rounded-lg border border-indigo-100 shadow-sm">
        <div class="flex items-center justify-between mb-2">
          <span class="font-semibold text-indigo-900">Previous Remarks</span>
          <span class="text-sm text-indigo-600">{{ remark.date }}</span>
        </div>
        <p class="text-indigo-900/80 leading-relaxed">{{ remark.content }}</p>
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from 'axios';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';

const emit = defineEmits(['navigate']);

const searchQuery = ref("");
const records = ref([]);
const isLoading = ref(false);
const portfolioFolders = ref([]);

// Load student submissions
const loadStudentWork = async (studentId) => {
    isLoading.value = true;
    try {
        // Load portfolio folders
        const foldersResponse = await axios.get('/api/portfolio/folders/');
        portfolioFolders.value = foldersResponse.data || [];
        
        const allRecords = [];
        
        // Load submissions for each folder
        for (const folder of portfolioFolders.value) {
            try {
                const activitiesResponse = await axios.get(`/api/portfolio/folders/${folder.id}/activities/`);
                const activities = activitiesResponse.data || [];
                
                for (const activity of activities) {
                    try {
                        const submissionsResponse = await axios.get(`/api/activities/${activity.id}/submissions/`);
                        const submissions = submissionsResponse.data || [];
                        
                        // Filter submissions for this student
                        const studentSubmissions = submissions.filter(sub => 
                            sub.student.id === studentId || sub.student.username === studentId
                        );
                        
                        if (studentSubmissions.length > 0) {
                            studentSubmissions.forEach(submission => {
                                allRecords.push({
                                    subject: folder.name,
                                    output: activity.title,
                                    activityType: activity.activity_type,
                                    dueDate: activity.due_date ? new Date(activity.due_date).toLocaleDateString() : 'N/A',
                                    submittedDate: new Date(submission.submitted_at).toLocaleDateString(),
                                    time: new Date(submission.submitted_at).toLocaleTimeString(),
                                    status: submission.status === 'scored' ? 'Scored' : 'Submitted',
                                    score: submission.score || 'N/A',
                                    history: `Submitted ${getTimeAgo(submission.submitted_at)}`,
                                    fileType: submission.file_type,
                                    filePath: submission.file_path,
                                    caption: submission.caption
                                });
                            });
                        } else {
                            // Show activity even if not submitted
                            allRecords.push({
                                subject: folder.name,
                                output: activity.title,
                                activityType: activity.activity_type,
                                dueDate: activity.due_date ? new Date(activity.due_date).toLocaleDateString() : 'N/A',
                                submittedDate: 'Not submitted',
                                time: '-',
                                status: 'Missing',
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
        console.log('Loaded student work records:', records.value);
    } catch (error) {
        console.error('Error loading student work:', error);
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
    if (!searchQuery.value) return records.value;
    
    const query = searchQuery.value.toLowerCase();
    return records.value.filter(record => 
        record.subject.toLowerCase().includes(query) ||
        record.output.toLowerCase().includes(query) ||
        record.status.toLowerCase().includes(query) ||
        record.history.toLowerCase().includes(query)
    );
});

const getStatusColor = (status) => {
    switch (status) {
        case "Scored": return "success";
        case "Submitted": return "info";
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
            
            // Load the student's work
            if (studentData.value?.id) {
                loadStudentWork(studentData.value.id);
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

const showRemarksDialog = ref(false);
const remarksHistory = ref([
    {
        date: '2025-05-10',
        content: 'Student shows good progress in recent assignments. Participation in group activities has improved significantly.'
    },
    {
        date: '2025-05-03',
        content: 'Completed all assignments for the week. Needs to work on time management for future projects.'
    },
    {
        date: '2025-04-26',
        content: 'Excellent performance in recent project presentation. Shows strong leadership qualities in team activities.'
    }
]);

const openRemarksDialog = () => {
    showRemarksDialog.value = true;
};

const completedCount = computed(() => {
    return records.value.filter(record => record.status === "Scored" || record.status === "Submitted").length;
});

const pendingCount = computed(() => {
    return records.value.filter(record => record.status === "Missing").length;
});
</script>

<script>
import TeacherLayout from '@/Layouts/MainLayout.vue';

export default {
    layout: TeacherLayout
};
</script>

<style scoped>
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
    @apply bg-amber-100 text-amber-800 border border-amber-200;
}

:deep(.p-tag.p-tag-info) {
    @apply bg-blue-100 text-blue-800 border border-blue-200;
}
</style>