<template>
  <div class="p-4 md:p-6">
    <div class="rounded-2xl shadow-lg bg-white/90 backdrop-blur-sm border border-indigo-100 overflow-hidden">
      <!-- Header -->
      <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-6">
        <h1 class="text-2xl font-bold text-white">My Remarks from Teachers</h1>
        <p class="text-white/80 text-sm mt-1">View feedback and comments from your teachers</p>
      </div>

      <!-- Content -->
      <div class="p-6">
        <!-- Loading State -->
        <div v-if="isLoading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>

        <!-- Two Column Layout -->
        <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Left Column: My Remarks (General Remarks) -->
          <div class="bg-white/95 rounded-xl border-2 border-indigo-100 overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300">
            <div class="bg-gradient-to-r from-indigo-50 to-violet-50 p-4 border-b-2 border-indigo-100">
              <h3 class="text-lg font-bold text-indigo-900 flex items-center gap-2">
                <i class="pi pi-comments text-indigo-600"></i>
                My Remarks
                <span v-if="unreadRemarksCount > 0" class="bg-red-500 text-white text-xs px-2 py-0.5 rounded-full ml-2">
                  {{ unreadRemarksCount }}
                </span>
              </h3>
              <p class="text-xs text-indigo-600 mt-1">General feedback from teachers</p>
            </div>
            <!-- Tabs -->
            <div class="flex gap-2 border-b border-indigo-200 px-4 pt-2">
              <button 
                @click="remarksTab = 'all'"
                class="px-3 py-2 text-sm font-medium transition-colors duration-200"
                :class="remarksTab === 'all' 
                  ? 'text-indigo-600 border-b-2 border-indigo-600' 
                  : 'text-gray-500 hover:text-indigo-600'">
                All
              </button>
              <button 
                @click="remarksTab = 'unread'"
                class="px-3 py-2 text-sm font-medium transition-colors duration-200 flex items-center gap-2"
                :class="remarksTab === 'unread' 
                  ? 'text-indigo-600 border-b-2 border-indigo-600' 
                  : 'text-gray-500 hover:text-indigo-600'">
                Unread
                <span v-if="unreadRemarksCount > 0" class="bg-red-500 text-white text-xs px-1.5 py-0.5 rounded-full">
                  {{ unreadRemarksCount }}
                </span>
              </button>
            </div>
            <div class="p-4 max-h-[700px] overflow-y-auto">
              <div v-if="filteredRemarks.length > 0" class="space-y-3">
                <div v-for="remark in filteredRemarks" 
                     :key="remark.id"
                     @click="openRemarkDetail(remark)"
                     class="bg-white p-4 rounded-xl border-2 hover:shadow-md transition-all duration-200 hover:border-indigo-300 cursor-pointer"
                     :class="remark.is_read ? 'border-indigo-100' : 'border-indigo-300 bg-indigo-50/30'">
                  <div class="flex items-start justify-between mb-3">
                    <div class="flex items-center gap-3">
                      <div class="bg-gradient-to-br from-indigo-600 to-violet-600 text-white font-bold w-10 h-10 flex items-center justify-center rounded-full shadow-md ring-2 ring-indigo-200">
                        {{ remark.teacherInitial }}
                      </div>
                      <div>
                        <div class="flex items-center gap-2">
                          <h4 class="font-bold text-indigo-900 text-sm">{{ remark.teacherName }}</h4>
                          <span v-if="!remark.is_read" class="text-xs text-blue-600 font-semibold">Unread</span>
                        </div>
                        <p class="text-xs text-indigo-600">{{ remark.subject }}</p>
                      </div>
                    </div>
                    <div class="flex flex-col items-end">
                      <span class="text-xs font-medium text-indigo-700 bg-indigo-50 px-2 py-1 rounded-full">
                        {{ remark.date }}
                      </span>
                      <span v-if="remark.time" class="text-xs text-indigo-500 mt-1">{{ remark.time }}</span>
                    </div>
                  </div>
                  <div class="bg-gradient-to-br from-indigo-50 to-violet-50 p-3 rounded-lg border border-indigo-100">
                    <p class="text-indigo-900 text-sm whitespace-pre-wrap leading-relaxed line-clamp-2">{{ remark.text }}</p>
                  </div>
                </div>
              </div>
              <!-- Empty State for My Remarks -->
              <div v-else class="flex flex-col items-center justify-center py-12 px-4">
                <div class="w-16 h-16 rounded-full bg-indigo-100 flex items-center justify-center mb-3">
                  <i class="pi pi-comments text-2xl text-indigo-400"></i>
                </div>
                <h4 class="text-base font-bold text-indigo-900 mb-1">No General Remarks</h4>
                <p class="text-indigo-600 text-center text-sm">
                  No general remarks yet
                </p>
              </div>
            </div>
          </div>

          <!-- Right Column: Output Remarks -->
          <div class="bg-white/95 rounded-xl border-2 border-indigo-100 overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300">
            <div class="bg-gradient-to-r from-indigo-50 to-violet-50 p-4 border-b-2 border-indigo-100">
              <h3 class="text-lg font-bold text-indigo-900 flex items-center gap-2">
                <i class="pi pi-file-edit text-indigo-600"></i>
                Output Remarks
              </h3>
              <p class="text-xs text-indigo-600 mt-1">Feedback on your submitted work</p>
            </div>
            
            <!-- Tabs for Output Remarks -->
            <div class="flex gap-6 px-4 pt-3 border-b border-indigo-100">
              <button 
                @click="outputRemarksTab = 'all'"
                :class="['pb-2 px-1 text-sm font-semibold transition-all duration-200 border-b-2', 
                         outputRemarksTab === 'all' 
                           ? 'text-indigo-700 border-indigo-600' 
                           : 'text-gray-500 border-transparent hover:text-indigo-600']">
                All
              </button>
              <button 
                @click="outputRemarksTab = 'unread'"
                :class="['pb-2 px-1 text-sm font-semibold transition-all duration-200 border-b-2 flex items-center gap-2', 
                         outputRemarksTab === 'unread' 
                           ? 'text-indigo-700 border-indigo-600' 
                           : 'text-gray-500 border-transparent hover:text-indigo-600']">
                Unread
                <span v-if="unreadOutputRemarksCount > 0" 
                      class="bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                  {{ unreadOutputRemarksCount }}
                </span>
              </button>
            </div>
            
            <div class="p-4 max-h-[700px] overflow-y-auto">
              <div v-if="filteredOutputRemarks.length > 0" class="space-y-3">
                <div v-for="remark in filteredOutputRemarks" 
                     :key="remark.id" 
                     class="bg-white p-4 rounded-xl border-2 border-indigo-100 hover:shadow-md transition-all duration-200 hover:border-indigo-300 hover:scale-[1.02]">
                  <div class="flex items-start justify-between mb-3">
                    <div class="flex items-center gap-3">
                      <div class="bg-gradient-to-br from-violet-600 to-purple-600 text-white font-bold w-10 h-10 flex items-center justify-center rounded-full shadow-md ring-2 ring-violet-200">
                        {{ remark.teacherInitial }}
                      </div>
                      <div>
                        <h4 class="font-bold text-indigo-900 text-sm">{{ remark.activityName }}</h4>
                        <p class="text-xs text-indigo-600">{{ remark.teacherName }} • {{ remark.subject }}</p>
                      </div>
                    </div>
                    <div class="flex flex-col items-end">
                      <span class="text-xs font-medium text-violet-700 bg-violet-50 px-2 py-1 rounded-full">
                        {{ remark.date }}
                      </span>
                      <span v-if="remark.time" class="text-xs text-violet-500 mt-1">{{ remark.time }}</span>
                    </div>
                  </div>
                  <div class="bg-gradient-to-br from-violet-50 to-purple-50 p-3 rounded-lg border border-violet-100">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="text-xs font-semibold text-violet-700">Score:</span>
                      <span class="text-sm font-bold text-violet-900">{{ remark.score }}</span>
                    </div>
                    <p class="text-indigo-900 text-sm whitespace-pre-wrap leading-relaxed">{{ remark.feedback }}</p>
                  </div>
                </div>
              </div>
              <!-- Empty State for Output Remarks -->
              <div v-else class="flex flex-col items-center justify-center py-12 px-4">
                <div class="w-16 h-16 rounded-full bg-violet-100 flex items-center justify-center mb-3">
                  <i class="pi pi-file-edit text-2xl text-violet-400"></i>
                </div>
                <h4 class="text-base font-bold text-indigo-900 mb-1">No Output Remarks</h4>
                <p class="text-indigo-600 text-center text-sm">
                  No feedback on outputs yet
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

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
            <span class="text-sm font-medium text-indigo-700">{{ selectedRemark.date }}</span>
            <span class="text-xs text-indigo-600">{{ selectedRemark.time }}</span>
          </div>
        </div>
      </div>

      <!-- Remark Content -->
      <div class="bg-white p-5 rounded-lg border-2 border-indigo-100 shadow-sm">
        <p class="text-indigo-900 leading-relaxed whitespace-pre-wrap text-base">{{ selectedRemark.text }}</p>
      </div>

      <!-- Teacher Info -->
      <div class="flex items-center gap-3 p-3 bg-indigo-50 rounded-lg">
        <div class="bg-gradient-to-br from-indigo-600 to-violet-600 text-white font-bold w-10 h-10 flex items-center justify-center rounded-full shadow-md">
          {{ selectedRemark.teacherInitial }}
        </div>
        <div>
          <p class="text-sm text-indigo-600 font-medium">From Teacher</p>
          <p class="text-indigo-900 font-semibold">{{ selectedRemark.teacherName }}</p>
        </div>
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from 'axios';
import Dialog from 'primevue/dialog';

const remarks = ref([]);
const outputRemarks = ref([]);
const isLoading = ref(false);
const remarksTab = ref('all');
const outputRemarksTab = ref('all');
const showRemarkDetailDialog = ref(false);
const selectedRemark = ref(null);

// Load remarks from API
const loadRemarks = async () => {
  isLoading.value = true;
  
  try {
    // Load general remarks
    const remarksResponse = await axios.get('/api/remarks/');
    if (remarksResponse.data) {
      remarks.value = remarksResponse.data.map(remark => {
        const remarkDate = new Date(remark.created_at);
        return {
          id: remark.id,
          teacherName: remark.teacher_name || remark.teacher_username,
          teacherInitial: (remark.teacher_name || remark.teacher_username).split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2),
          subject: 'General',
          date: remarkDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }),
          time: remarkDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          text: remark.text,
          is_read: remark.is_read || false
        };
      });
      console.log('Loaded general remarks:', remarks.value.length);
      console.log('Unread remarks:', remarks.value.filter(r => !r.is_read).length);
    }
    
    // Load output-specific remarks (from student's own submissions)
    try {
      const remarksResponse = await axios.get('/api/student/submission-remarks/');
      if (remarksResponse.data) {
        outputRemarks.value = remarksResponse.data.map(remark => {
          const remarkDate = new Date(remark.created_at);
          return {
            id: remark.id,
            submissionId: remark.submission_id,
            activityName: remark.activity_title || 'Activity',
            teacherName: remark.teacher_name || remark.teacher_username,
            teacherInitial: (remark.teacher_name || remark.teacher_username || 'T').split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2),
            subject: remark.activity_type || 'General',
            date: remarkDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }),
            time: remarkDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            score: remark.submission_score ? `${remark.submission_score}/10` : 'Not scored yet',
            feedback: remark.text
          };
        });
        console.log('Loaded output remarks:', outputRemarks.value.length);
      }
    } catch (error) {
      console.error('Error loading output remarks:', error);
      outputRemarks.value = [];
    }
  } catch (error) {
    console.error('Error loading remarks:', error);
  } finally {
    isLoading.value = false;
  }
};

// Filtered remarks based on tab
const filteredRemarks = computed(() => {
  if (remarksTab.value === 'unread') {
    return remarks.value.filter(remark => !remark.is_read);
  }
  return remarks.value;
});

// Count unread remarks
const unreadRemarksCount = computed(() => {
  return remarks.value.filter(remark => !remark.is_read).length;
});

// Filtered output remarks based on tab
const filteredOutputRemarks = computed(() => {
  if (outputRemarksTab.value === 'unread') {
    return outputRemarks.value.filter(remark => !remark.is_read);
  }
  return outputRemarks.value;
});

// Count unread output remarks
const unreadOutputRemarksCount = computed(() => {
  return outputRemarks.value.filter(remark => !remark.is_read).length;
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

// Open remark detail dialog and mark as read
const openRemarkDetail = async (remark) => {
  selectedRemark.value = remark;
  showRemarkDetailDialog.value = true;
  
  // Mark as read when opened
  if (!remark.is_read) {
    try {
      console.log('Marking remark as read:', remark.id);
      const csrfToken = getCsrfToken();
      const response = await axios.post(`/api/remarks/${remark.id}/mark-read/`, {}, {
        headers: {
          'X-CSRFToken': csrfToken
        }
      });
      console.log('Mark as read response:', response.data);
      remark.is_read = true;
      console.log('Remark marked as read successfully');
    } catch (error) {
      console.error('Error marking remark as read:', error);
      console.error('Error response:', error.response?.data);
    }
  } else {
    console.log('Remark already read:', remark.id);
  }
};

onMounted(() => {
  loadRemarks();
});
</script>

<script>
import StudentLayout from '@/Layouts/MainLayout.vue';

export default {
    layout: StudentLayout
};
</script>

<style scoped>
/* Theme variables */
:root {
  --theme-indigo: #4f46e5;
  --theme-violet: #7c3aed;
  --theme-blue: #3b82f6;
  --theme-light: #f5f3ff;
  --theme-dark: #1e1b4b;
}
</style>
