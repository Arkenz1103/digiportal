<template>
  <div class="p-4 md:p-6">
    <div class="rounded-2xl shadow-lg bg-white/90 backdrop-blur-sm border border-indigo-100 overflow-hidden">
      <!-- Header -->
      <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-6">
        <h1 class="text-2xl font-bold text-white">My Remarks from Teachers</h1>
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
                      <div class="bg-gradient-to-br from-indigo-600 to-violet-600 text-white font-bold w-10 h-10 flex items-center justify-center rounded-full shadow-md ring-2 ring-indigo-200 overflow-hidden">
                        <img v-if="remark.teacherProfilePicture" :src="remark.teacherProfilePicture" :alt="remark.teacherName" class="w-full h-full object-cover" />
                        <span v-else>{{ remark.teacherInitial }}</span>
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
                     @click="openOutputRemarkDetail(remark)"
                     class="bg-white p-4 rounded-xl border-2 hover:shadow-md transition-all duration-200 hover:border-indigo-300 hover:scale-[1.02] cursor-pointer"
                     :class="remark.is_read ? 'border-indigo-100' : 'border-violet-300 bg-violet-50/30'">
                  <div class="flex items-start justify-between mb-3">
                    <div class="flex items-center gap-3">
                      <div class="bg-gradient-to-br from-violet-600 to-purple-600 text-white font-bold w-10 h-10 flex items-center justify-center rounded-full shadow-md ring-2 ring-violet-200 overflow-hidden">
                        <img v-if="remark.teacherProfilePicture" :src="remark.teacherProfilePicture" :alt="remark.teacherName" class="w-full h-full object-cover" />
                        <span v-else>{{ remark.teacherInitial }}</span>
                      </div>
                      <div>
                        <div class="flex items-center gap-2">
                          <h4 class="font-bold text-indigo-900 text-sm">{{ remark.activityName }}</h4>
                          <span v-if="!remark.is_read" class="text-xs text-violet-600 font-semibold">Unread</span>
                        </div>
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
        <div class="bg-gradient-to-br from-indigo-600 to-violet-600 text-white font-bold w-10 h-10 flex items-center justify-center rounded-full shadow-md overflow-hidden">
          <img v-if="selectedRemark.teacherProfilePicture" :src="selectedRemark.teacherProfilePicture" :alt="selectedRemark.teacherName" class="w-full h-full object-cover" />
          <span v-else>{{ selectedRemark.teacherInitial }}</span>
        </div>
        <div>
          <p class="text-sm text-indigo-600 font-medium">From Teacher</p>
          <p class="text-indigo-900 font-semibold">{{ selectedRemark.teacherName }}</p>
        </div>
      </div>
    </div>
  </Dialog>

  <!-- View Output Remark Dialog -->
  <Dialog v-model:visible="showOutputRemarkDialog" modal :showHeader="false" :style="{width: '650px', maxWidth: '90vw'}" class="p-fluid">
    <div class="flex justify-end pt-2 pr-2">
      <button @click="showOutputRemarkDialog = false" class="w-8 h-8 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors">
        <i class="pi pi-times text-gray-500"></i>
      </button>
    </div>
    <div v-if="selectedOutputRemark" class="space-y-4 px-2 pb-4">
      <!-- Teacher's Remark at the Top -->
      <div class="bg-gradient-to-r from-violet-50 to-purple-50 p-4 rounded-lg border-2 border-violet-200">
        <div class="flex items-center gap-2 mb-3">
          <i class="pi pi-comments text-violet-600 text-lg"></i>
          <span class="font-bold text-violet-900">Teacher's Remark</span>
        </div>
        <div class="flex items-start gap-3">
          <div class="bg-gradient-to-br from-violet-600 to-purple-600 text-white font-bold w-10 h-10 flex items-center justify-center rounded-full shadow-md flex-shrink-0 overflow-hidden">
            <img v-if="selectedOutputRemark.teacherProfilePicture" :src="selectedOutputRemark.teacherProfilePicture" :alt="selectedOutputRemark.teacherName" class="w-full h-full object-cover" />
            <span v-else>{{ selectedOutputRemark.teacherInitial }}</span>
          </div>
          <div class="flex-1">
            <p class="text-sm font-semibold text-violet-900">{{ selectedOutputRemark.teacherName }}</p>
            <p class="text-violet-700 text-sm mt-1 whitespace-pre-wrap">{{ selectedOutputRemark.feedback }}</p>
          </div>
        </div>
      </div>

      <!-- Activity Info Grid -->
      <div class="grid grid-cols-2 gap-x-6 gap-y-3 p-4 bg-gray-50 rounded-lg border border-gray-200">
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium">Subject</p>
          <p class="text-gray-900 font-medium">{{ selectedOutputRemark.subject }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium">Activity Type</p>
          <p class="text-gray-900 font-medium capitalize">{{ selectedOutputRemark.activityType || 'Assignment' }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium">Activity Title</p>
          <p class="text-gray-900 font-medium">{{ selectedOutputRemark.activityName }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium">Date & Time Submitted</p>
          <p class="text-gray-900 font-medium">{{ selectedOutputRemark.submittedDate || selectedOutputRemark.date }} <span class="text-gray-500">{{ selectedOutputRemark.submittedTime || selectedOutputRemark.time }}</span></p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium">Status</p>
          <span
            class="px-2 py-1 text-xs rounded font-medium inline-block mt-1"
            :class="{
              'bg-green-100 text-green-800': selectedOutputRemark.status === 'Scored',
              'bg-blue-100 text-blue-800': selectedOutputRemark.status === 'Submitted',
              'bg-amber-100 text-amber-700': selectedOutputRemark.status === 'Pending'
            }">
            {{ selectedOutputRemark.status || 'Submitted' }}
          </span>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium">Score</p>
          <p class="font-bold" :class="selectedOutputRemark.score === 'Not scored yet' ? 'text-gray-400' : 'text-green-600'">
            {{ selectedOutputRemark.score }}
          </p>
        </div>
      </div>

      <!-- File Display with Navigation -->
      <div class="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <!-- File Counter (if multiple files) -->
        <div v-if="outputFiles.length > 1" class="bg-indigo-600 text-white px-3 py-1.5 text-center text-sm font-medium">
          {{ currentOutputFileIndex + 1 }} / {{ outputFiles.length }}
        </div>
        
        <div class="relative" style="min-height: 300px;">
          <!-- Navigation Arrows -->
          <div v-if="outputFiles.length > 1" class="absolute inset-0 flex items-center justify-between px-2 pointer-events-none z-10">
            <button
              @click="prevOutputFile"
              :disabled="currentOutputFileIndex === 0"
              class="pointer-events-auto w-10 h-10 rounded-full bg-white/90 hover:bg-white shadow-lg flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <i class="pi pi-chevron-left text-indigo-600"></i>
            </button>
            <button
              @click="nextOutputFile"
              :disabled="currentOutputFileIndex >= outputFiles.length - 1"
              class="pointer-events-auto w-10 h-10 rounded-full bg-white/90 hover:bg-white shadow-lg flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <i class="pi pi-chevron-right text-indigo-600"></i>
            </button>
          </div>

          <!-- File Content -->
          <div class="flex items-center justify-center p-4 bg-gray-50" style="min-height: 300px;">
            <template v-if="currentOutputFile && currentOutputFile.file_path">
              <!-- Image -->
              <img v-if="isImageFile(currentOutputFile)"
                :src="getFileUrl(currentOutputFile.file_path)"
                :alt="selectedOutputRemark.activityName"
                class="max-w-full max-h-72 rounded shadow-lg object-contain"
              />
              <!-- PDF -->
              <div v-else-if="currentOutputFile.file_type === 'pdf'" class="flex flex-col items-center justify-center text-red-600">
                <i class="pi pi-file-pdf text-6xl mb-3"></i>
                <span class="text-base font-medium">PDF Document</span>
                <span class="text-sm text-gray-500 mt-1">{{ currentOutputFile.file_name || 'Document' }}</span>
                <a :href="getFileUrl(currentOutputFile.file_path)" target="_blank"
                  class="mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700 transition-colors">
                  <i class="pi pi-external-link mr-1"></i> View File
                </a>
              </div>
              <!-- Document -->
              <div v-else-if="currentOutputFile.file_type === 'document'" class="flex flex-col items-center justify-center text-blue-600">
                <i class="pi pi-file-word text-6xl mb-3"></i>
                <span class="text-base font-medium">Word Document</span>
                <span class="text-sm text-gray-500 mt-1">{{ currentOutputFile.file_name || 'Document' }}</span>
                <a :href="getFileUrl(currentOutputFile.file_path)" target="_blank"
                  class="mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700 transition-colors">
                  <i class="pi pi-external-link mr-1"></i> View File
                </a>
              </div>
              <!-- Other file types -->
              <div v-else class="flex flex-col items-center justify-center text-gray-500">
                <i class="pi pi-file text-6xl mb-3"></i>
                <span class="text-base font-medium">{{ currentOutputFile.file_type || 'File' }}</span>
                <a v-if="currentOutputFile.file_path" :href="getFileUrl(currentOutputFile.file_path)" target="_blank"
                  class="mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700 transition-colors">
                  <i class="pi pi-external-link mr-1"></i> View File
                </a>
              </div>
            </template>
            <template v-else-if="isLoadingOutput">
              <div class="flex flex-col items-center justify-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-3"></div>
                <p class="text-gray-500">Loading output...</p>
              </div>
            </template>
            <template v-else>
              <div class="text-center text-gray-400">
                <i class="pi pi-image text-5xl mb-2"></i>
                <p>No file available</p>
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <button @click="showOutputRemarkDialog = false" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors">
        Close
      </button>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from 'axios';
import Dialog from 'primevue/dialog';
import { useToast } from '../../composables/useToast';

// Define emits for navigation
const emit = defineEmits(['navigate']);

const { showSuccess, showError, showInfo, showWarning } = useToast();

// Archived view mode state
const isViewingArchived = ref(false);
const viewingArchivedSchoolYear = ref(null);

const remarks = ref([]);
const outputRemarks = ref([]);
const isLoading = ref(false);
const remarksTab = ref('all');
const outputRemarksTab = ref('all');
const showRemarkDetailDialog = ref(false);
const selectedRemark = ref(null);

// Output remark dialog state
const showOutputRemarkDialog = ref(false);
const selectedOutputRemark = ref(null);
const outputFiles = ref([]);
const currentOutputFileIndex = ref(0);
const isLoadingOutput = ref(false);

// Current output file computed
const currentOutputFile = computed(() => {
  if (outputFiles.value.length > 0 && currentOutputFileIndex.value < outputFiles.value.length) {
    return outputFiles.value[currentOutputFileIndex.value];
  }
  return null;
});

// File navigation
const prevOutputFile = () => {
  if (currentOutputFileIndex.value > 0) {
    currentOutputFileIndex.value--;
  }
};

const nextOutputFile = () => {
  if (currentOutputFileIndex.value < outputFiles.value.length - 1) {
    currentOutputFileIndex.value++;
  }
};

// Check if file is an image
const isImageFile = (file) => {
  if (!file) return false;
  const imageTypes = ['image', 'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'];
  const fileType = file.file_type?.toLowerCase() || '';
  const fileName = file.file_name?.toLowerCase() || '';
  const filePath = file.file_path?.toLowerCase() || '';
  
  return imageTypes.some(type => 
    fileType.includes(type) || 
    fileName.includes(type) || 
    filePath.includes(type)
  );
};

// Get file URL
const getFileUrl = (filePath) => {
  if (!filePath) return '';
  if (filePath.startsWith('http')) return filePath;
  if (filePath.startsWith('/media')) return filePath;
  return `/media/${filePath}`;
};

// Load remarks from API
const loadRemarks = async () => {
  isLoading.value = true;

  try {
    // Build URL with classroom_id if in archived view mode
    let remarksUrl = '/api/remarks/';
    let submissionRemarksUrl = '/api/student/submission-remarks/';
    
    if (isViewingArchived.value && viewingArchivedSchoolYear.value?.classroom_id) {
      const classroomId = viewingArchivedSchoolYear.value.classroom_id;
      remarksUrl += `?classroom_id=${classroomId}`;
      submissionRemarksUrl += `?classroom_id=${classroomId}`;
      console.log('📂 Loading archived remarks for classroom:', classroomId);
    }
    
    // Load general remarks
    const remarksResponse = await axios.get(remarksUrl);
    if (remarksResponse.data) {
      remarks.value = remarksResponse.data.map(remark => {
        const remarkDate = new Date(remark.created_at);
        return {
          id: remark.id,
          teacherName: remark.teacher_name || remark.teacher_username,
          teacherInitial: (remark.teacher_name || remark.teacher_username).split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2),
          teacherProfilePicture: remark.teacher_profile_picture || null,
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
      const remarksResponse = await axios.get(submissionRemarksUrl);
      if (remarksResponse.data) {
        outputRemarks.value = remarksResponse.data.map(remark => {
          const remarkDate = new Date(remark.created_at);
          return {
            id: remark.id,
            submissionId: remark.submission_id,
            activityName: remark.activity_title || 'Activity',
            teacherName: remark.teacher_name || remark.teacher_username,
            teacherInitial: (remark.teacher_name || remark.teacher_username || 'T').split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2),
            teacherProfilePicture: remark.teacher_profile_picture || null,
            subject: remark.activity_type || 'General',
            date: remarkDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }),
            time: remarkDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            score: remark.submission_score ? `${remark.submission_score}/10` : 'Not scored yet',
            feedback: remark.text,
            is_read: remark.is_read || false
          };
        });
        console.log('Loaded output remarks:', outputRemarks.value.length);
        console.log('Unread output remarks:', outputRemarks.value.filter(r => !r.is_read).length);
      }
    } catch (error) {
      console.error('Error loading output remarks:', error);
      showError('Failed to load output remarks', 'Error');
      outputRemarks.value = [];
    }
  } catch (error) {
    console.error('Error loading remarks:', error);
    showError('Failed to load remarks', 'Error');
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
      showError('Failed to mark remark as read', 'Error');
    }
  } else {
    console.log('Remark already read:', remark.id);
  }
};

// Open output remark detail dialog and load submission files
const openOutputRemarkDetail = async (remark) => {
  selectedOutputRemark.value = remark;
  showOutputRemarkDialog.value = true;
  outputFiles.value = [];
  currentOutputFileIndex.value = 0;
  isLoadingOutput.value = true;

  // Mark as read when opened - update locally first for immediate UI feedback
  if (!remark.is_read) {
    // Update the remark in the outputRemarks array to trigger reactivity
    const remarkIndex = outputRemarks.value.findIndex(r => r.id === remark.id);
    if (remarkIndex !== -1) {
      outputRemarks.value[remarkIndex].is_read = true;
    }
    remark.is_read = true;
    console.log('Output remark marked as read locally:', remark.id);
    
    // Try to persist to backend (optional - don't block on failure)
    try {
      const csrfToken = getCsrfToken();
      await axios.post(`/api/submission-remarks/${remark.id}/mark-read/`, {}, {
        headers: {
          'X-CSRFToken': csrfToken
        }
      });
      console.log('Output remark marked as read on server:', remark.id);
    } catch (error) {
      console.error('Error marking output remark as read on server:', error);
      // Continue anyway - local state is already updated
    }
  }

  // Load submission files if we have a submission ID
  if (remark.submissionId) {
    try {
      const response = await axios.get(`/api/submissions/${remark.submissionId}/`);
      if (response.data) {
        // Update remark with additional submission data
        selectedOutputRemark.value = {
          ...remark,
          submittedDate: response.data.submitted_at ? new Date(response.data.submitted_at).toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' }) : remark.date,
          submittedTime: response.data.submitted_at ? new Date(response.data.submitted_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) : remark.time,
          status: response.data.score ? 'Scored' : 'Submitted',
          activityType: response.data.activity_type || remark.subject
        };

        // Load files - check multiple possible field names
        if (response.data.submission_files && response.data.submission_files.length > 0) {
          outputFiles.value = response.data.submission_files.map(file => ({
            file_path: file.file_path || file.file || file.url,
            file_type: file.file_type || file.type || 'image',
            file_name: file.file_name || file.name || 'Submission'
          }));
        } else if (response.data.files && response.data.files.length > 0) {
          outputFiles.value = response.data.files.map(file => ({
            file_path: file.file_path || file.file || file.url,
            file_type: file.file_type || file.type || 'image',
            file_name: file.file_name || file.name || 'Submission'
          }));
        } else if (response.data.file_path || response.data.file) {
          // Single file fallback
          outputFiles.value = [{
            file_path: response.data.file_path || response.data.file,
            file_type: response.data.file_type || 'image',
            file_name: response.data.file_name || 'Submission'
          }];
        }
        
        console.log('Loaded output files:', outputFiles.value);
      }
    } catch (error) {
      console.error('Error loading submission details:', error);
      // Don't show error - just show empty state
    }
  }

  isLoadingOutput.value = false;
};

onMounted(() => {
  // Check if we're in archived view mode
  const savedArchivedView = localStorage.getItem('student_viewing_archived_school_year');
  if (savedArchivedView) {
    try {
      const archivedData = JSON.parse(savedArchivedView);
      isViewingArchived.value = true;
      viewingArchivedSchoolYear.value = archivedData;
      console.log('📂 Sremarked: Restored archived view mode:', archivedData.name);
    } catch (e) {
      console.error('Error parsing student archived view data:', e);
      localStorage.removeItem('student_viewing_archived_school_year');
    }
  }
  
  loadRemarks();
});
</script>

<script>
import StudentLayout from '@/Layouts/MainLayout.vue';

export default {
    layout: StudentLayout,
    inheritAttrs: false
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
