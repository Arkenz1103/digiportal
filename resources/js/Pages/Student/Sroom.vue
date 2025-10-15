<template>
  <Head :title="`| ${className}`"/>
  <div class="min-h-screen flex flex-col bg-gradient-to-br from-indigo-50 via-violet-50 to-blue-50">
    <!-- Class Header -->
    <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-6 md:p-4 shadow-lg rounded-t-xl">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div class="space-y-3">
          <h1 class="text-xl md:text-2xl font-bold text-white px-4 py-2 md:px-6 md:py-3 rounded-lg inline-block bg-white/20">
            {{ className }}
          </h1>
          <p class="text-white/90 ml-2 flex items-center gap-2">
            <i class="pi pi-user"></i>
            Student: {{ auth.user.name }}
          </p>
        </div>
        <div class="relative settings-dropdown" ref="settingsRef">
          <button
            @click.stop="toggleSettingsDropdown"
            type="button"
            class="flex items-center justify-center w-10 h-10 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-all duration-200 hover:shadow-md border border-white/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-indigo-700 focus:ring-white"
            aria-label="Settings"
            aria-haspopup="true"
            :aria-expanded="showSettingsDropdown"
          >
            <i class="pi pi-cog text-lg"></i>
          </button>

          <transition
            enter-active-class="transition ease-out duration-100"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
          >
            <div
              v-if="showSettingsDropdown"
              class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl z-50 border border-gray-200 overflow-hidden"
            >
              <button
                @click="showArchiveDialog = true"
                type="button"
                class="w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-red-50 hover:text-red-600 flex items-center gap-2"
              >
                <i class="pi pi-archive"></i>
                <span>Archive Class</span>
              </button>
            </div>
          </transition>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex flex-wrap gap-2 md:gap-4 mt-4 md:mt-6">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="flex items-center gap-2 text-white/90 px-4 py-2 md:px-6 md:py-3 rounded-lg transition-all duration-300 relative overflow-hidden group"
          :class="[
            activeTab === tab.id
              ? 'font-semibold text-white'
              : 'hover:text-white hover:bg-white/5'
          ]"
        >
          <span class="relative z-10 flex items-center gap-2">
            <i :class="['pi', tab.icon]"></i>
            <span>{{ tab.name }}</span>
          </span>
          <span 
            v-if="activeTab === tab.id"
            class="absolute bottom-0 left-0 right-0 h-0.5 bg-white rounded-full"
          ></span>
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="w-full bg-white/80 flex-1">
      <!-- Content Area -->
      <div :class="['mx-auto px-4 sm:px-6 pt-1 pb-8 transition-all duration-300', 
                  isSidebarCollapsed ? 'max-w-[95%]' : 'max-w-7xl']"
           :style="{ 'padding-left': isSidebarCollapsed ? '1.5rem' : '1.5rem', 'padding-right': '1.5rem' }">
        <template v-if="activeTab === 'portfolio'">
          <div v-if="!portfolioCreated" class="p-8">
            <div class="flex flex-col items-center justify-center text-center max-w-md mx-auto">
            </div>
          </div>
          <div v-else class="p-4 md:p-6">
            <!-- Portfolio Content -->
            <div>
              <!-- Activities List View -->
              <div v-if="selectedFolder" class="space-y-6">
                <!-- Combined Header with Back Button -->
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
                  <!-- List of Activities Header -->
                  <div class="rounded-lg py-2 px-4">
                    <span class="text-2xl font-bold text-indigo-900">List of Activities - Portfolio {{ selectedFolder.title }}</span>
                  </div>

                  <div class="flex flex-wrap gap-2">
                    <!-- Back button -->
                    <button
                      v-if="!selectedActivity"
                      @click="backToFolders"
                      class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                    >
                      <i class="pi pi-arrow-left"></i>
                      <span>Back to Folders</span>
                    </button>
                    <button
                      v-if="selectedActivity"
                      @click="selectedActivity = null"
                      class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                    >
                      <i class="pi pi-arrow-left"></i>
                      <span>Back to Activities</span>
                    </button>
                  </div>
                </div>

                <!-- Activity Detail View -->
                <div v-if="selectedActivity" class="bg-white rounded-xl shadow-lg p-6 mb-6 border border-indigo-100">
                  <!-- Activity Header with Title and Buttons -->
                  <div class="flex flex-col gap-4 mb-6">
                    <div class="flex justify-between items-center flex-wrap gap-4">
                      <div class="flex items-center gap-4">
                        <h2 class="text-lg font-bold text-gray-900">{{ selectedActivity.title }}</h2>
                        <span class="px-3 py-1 rounded-full text-sm font-medium text-gray-900 inline-block w-fit">
                          Due: {{ selectedActivity.date }}
                          <span class="text-xs block mt-1 text-gray-900/70">You cannot submit after the due date</span>
                        </span>
                      </div>
                      <div class="flex items-center gap-4 w-full sm:w-auto justify-center sm:justify-end mt-4 sm:mt-0">
                        <button
                          v-if="!hasSubmitted(selectedActivity)"
                          @click="addSampleProduct"
                          class="group flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                        >
                          <i class="pi pi-plus"></i>
                          <span>Turn in</span>
                        </button>
                        <span
                          v-else
                          class="px-4 py-2 rounded-lg bg-green-100 text-green-800"
                        >
                          <i class="pi pi-check-circle"></i>
                          <span>Submitted</span>
                        </span>
                      </div>
                    </div>

                    <!-- Activity Type and Description -->
                    <div class="mt-1/2 space-y-1/2">
                      <div class="flex items-start gap-2">
                        <span class="text-sm font-medium text-gray-900">Type:</span>
                        <span class="text-sm text-gray-600 capitalize">{{ selectedActivity.type }}</span>
                      </div>
                      <div class="flex items-start gap-2">
                        <span class="text-sm font-medium text-gray-900">Description:</span>
                        <p class="text-sm text-gray-600">{{ selectedActivity.description }}</p>
                      </div>
                    </div>
                  </div>

                  <!-- Student Submissions Section -->
                  <div class="mt-6 border-t border-indigo-100 pt-6" v-if="studentSubmissions.length > 0">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">Your Submissions:</h3>

                    <!-- Student Submission Cards -->
                    <div class="flex flex-wrap justify-center gap-4">
                      <div v-for="(submission, index) in studentSubmissions" :key="index"
                           class="bg-white rounded-lg border border-indigo-100 overflow-hidden hover:shadow-md transition-all w-full max-w-2xl mx-auto">
                        <div class="aspect-video relative bg-white overflow-hidden flex items-center justify-center p-4">
                          <template v-if="submission.isImage">
                            <img
                              :src="submission.previewUrl"
                              :alt="submission.caption || 'Submitted work'"
                              class="w-full h-full object-contain absolute inset-0 m-auto transition-opacity duration-200"
                              @error="handleImageError(submission)"
                              v-show="!submission.loadError"
                            />
                            <div v-if="submission.loadError" class="w-full h-full flex flex-col items-center justify-center bg-gray-50 text-gray-400">
                              <i class="pi pi-image text-4xl mb-2"></i>
                              <span class="text-sm">Image preview not available</span>
                            </div>
                          </template>
                          <div v-else class="w-full h-full flex flex-col items-center justify-center bg-gray-50 text-indigo-700">
                            <i class="pi pi-file text-4xl mb-2"></i>
                            <span class="text-sm">{{ submission.file?.name || 'File submission' }}</span>
                          </div>
                        </div>
                        <div class="p-4">
                          <p v-if="submission.caption" class="text-sm text-gray-600">{{ submission.caption }}</p>
                          <div class="flex justify-between items-center mt-2">
                            <span class="text-xs text-gray-500">{{ submission.date }}</span>
                            <span class="text-xs px-2 py-1 rounded"
                                  :class="submission.status === 'submitted' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'">
                              {{ submission.status }}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Activities Table -->
                <div v-else class="bg-white/80 backdrop-blur-sm rounded-xl shadow-sm overflow-hidden border border-indigo-100">
                  <!-- Table Header -->
                  <div class="flex items-center px-4 md:px-6 py-4 bg-indigo-50 border-b border-indigo-100">
                    <div class="w-32">
                      <span class="text-sm font-semibold text-indigo-900">Activity Type</span>
                    </div>
                    <div class="w-32 md:w-48">
                      <span class="text-sm font-semibold text-indigo-900">Activity Title</span>
                    </div>
                    <div class="flex-1">
                      <span class="text-sm font-semibold text-indigo-900">Description</span>
                    </div>
                    <div class="w-32 md:w-48 text-right">
                      <span class="text-sm font-semibold text-indigo-900">Due Date</span>
                    </div>
                  </div>

                  <!-- Activity Items -->
                  <div v-for="(activity, index) in folderActivities" :key="index"
                      class="group flex items-center px-4 md:px-6 py-4 hover:bg-indigo-50 border-b border-indigo-100 cursor-pointer transition-colors duration-200"
                      @click="openActivity(activity)">
                    <div class="w-32">
                      <span class="text-sm text-indigo-700 capitalize">{{ activity.type }}</span>
                    </div>
                    <div class="w-32 md:w-48">
                      <span class="font-medium text-indigo-700 transition-colors duration-100">{{ activity.title }}</span>
                    </div>
                    <div class="flex-1">
                      <span class="text-indigo-700 group-hover:text-indigo-900 transition-colors duration-200 line-clamp-2">{{ activity.description }}</span>
                    </div>
                    <div class="w-32 md:w-48 text-right">
                      <span class="text-sm text-indigo-600">{{ activity.date }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Folder Grid -->
              <div v-if="!selectedFolder" class="space-y-6">
                <!-- Header with title -->
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                  <h2 class="text-xl md:text-2xl font-bold text-gray-900">My Portfolio</h2>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
                  <div v-for="folder in portfolioFolders"
                    :key="folder.id"
                    @click="openFolderContent(folder)"
                    class="group bg-white rounded-xl shadow-sm border border-indigo-100 overflow-hidden hover:shadow-lg transition-all cursor-pointer transform hover:-translate-y-1 duration-200"
                  >
                    <!-- Folder Preview -->
                    <div class="relative h-36 mb-4 p-4 md:p-6">
                      <!-- Stacked Preview Images with Dynamic Animation -->
                      <div class="absolute top-5 right-5 w-28 h-32 flex items-center justify-center">
                        <div class="absolute w-24 h-28 rounded-md transform rotate-[-15deg] transition-all duration-300 group-hover:rotate-[-20deg] group-hover:scale-105 bg-gradient-to-br from-violet-500 to-blue-600 shadow-md ring-1 ring-white/40"></div>
                        <div class="absolute w-24 h-28 rounded-md transform rotate-[-5deg] transition-all duration-300 group-hover:rotate-[-10deg] group-hover:scale-105 bg-gradient-to-br from-violet-400 to-blue-500 shadow-sm ring-1 ring-white/30"></div>
                        <div class="absolute w-24 h-28 rounded-md transform rotate-[5deg] transition-all duration-300 group-hover:rotate-[10deg] group-hover:scale-105 bg-gradient-to-br from-violet-300 to-blue-400 ring-1 ring-white/20"></div>
                      </div>
                      <!-- Folder Title -->
                      <div class="relative z-10">
                        <h3 class="text-xl md:text-2xl font-bold mb-1 text-gray-900 group-hover:text-indigo-700 transition-colors">
                          {{ folder.title }}
                        </h3>
                        <div class="flex items-center space-x-2">
                          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                            {{ folder.items }} items
                          </span>
                        </div>
                      </div>
                    </div>

                    <!-- Interactive Footer -->
                    <div class="mt-4 pt-4 border-t border-gray-200 flex justify-between items-center p-4 md:p-6">
                      <div class="flex items-center space-x-2 text-sm text-indigo-700">
                        <i class="pi pi-folder text-indigo-700"></i>
                        <span>View Contents</span>
                      </div>
                      <i class="pi pi-arrow-right text-indigo-700 transform group-hover:translate-x-1 transition-transform"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>

        <!-- Schedule Tab Content -->
        <template v-if="activeTab === 'schedule'">
          <div class="p-4 md:p-6">
            <!-- Calendar Header -->
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
              <h2 class="text-xl font-bold text-gray-900">NOVEMBER 2025</h2>
              <div class="flex gap-4 items-center">
                <span class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full bg-indigo-100"></div>
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
                class="p-2 md:p-4 border rounded-lg hover:shadow-md cursor-pointer transition-all"
                :class="[
                  isClassDay(date + 1) ? 'bg-indigo-50 border-indigo-200' : 'bg-indigo-50 border-gray-200'
                ]"
                @click="showScheduleDetails(date + 1)">
                <div class="font-semibold text-gray-900">{{ date + 1 }}</div>
                <div v-if="isClassDay(date + 1)" class="text-xs md:text-sm mt-1 text-gray-900">
                  {{ day.time }}
                </div>
              </div>
            </div>

            <!-- Current Schedule Display -->
            <div v-if="selectedDate" class="mt-6 p-4 rounded-lg bg-indigo-100/10">
              <h3 class="font-semibold mb-2 text-gray-900">
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

    <!-- Submit Dialog -->
    <Dialog v-model:visible="showSubmitDialog" modal header="Submit Activity" :style="{ width: '450px' }">
      <div class="space-y-4">
        <div>
          <label for="product-caption" class="block text-sm font-medium text-gray-700 mb-1">Caption</label>
          <textarea
            id="product-caption"
            v-model="newProductCaption"
            rows="2"
            class="w-full px-3 py-2 border border-indigo-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Add a caption to your work..."
          ></textarea>
        </div>

      </div>
      <template #footer>
        <button
          @click="showSubmitDialog = false"
          class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
        >
          Cancel
        </button>
      </template>
    </Dialog>

    <!-- Add Product Dialog -->
    <Dialog v-model:visible="showProductUploadModal" modal header="Submit Your Work" :style="{ width: '550px' }">
      <div class="space-y-6">
        <!-- Caption Input moved to top -->
        <div>
          <label for="product-caption" class="block text-sm font-medium text-gray-700 mb-1">Caption</label>
          <textarea
            id="product-caption"
            v-model="newProductCaption"
            rows="2"
            class="w-full px-3 py-2 border border-indigo-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Add a caption to your work..."
          ></textarea>
        </div>

        <!-- File Upload Area -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Upload Your Work</label>

          <!-- File Upload Area -->
          <div v-if="!selectedFile" class="flex items-center justify-center w-full">
            <label class="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-indigo-100 rounded-lg cursor-pointer hover:bg-indigo-100/10">
              <div class="flex flex-col items-center justify-center pt-5 pb-6">
                <i class="pi pi-upload text-2xl text-indigo-700 mb-2"></i>
                <p class="text-sm text-gray-500">Click to upload or drag and drop</p>
                <p class="text-xs text-gray-500">(PDF, DOC, DOCX, or Images)</p>
              </div>
              <input
                type="file"
                class="hidden"
                @change="handleFileChange"
                accept=".pdf,.doc,.docx,image/*"
                required
              />
            </label>
          </div>

          <!-- Selected File Preview -->
          <div v-else class="bg-white rounded-lg border border-indigo-100 p-4">
            <div class="flex flex-col gap-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <!-- Image Preview for Images -->
                  <div v-if="previewUrl" class="h-16 w-16 relative rounded overflow-hidden">
                    <img
                      :src="previewUrl"
                      alt="Preview"
                      class="w-full h-full object-cover"
                    />
                  </div>
                  <!-- File Icon for Documents -->
                  <div v-else class="h-16 w-16 bg-indigo-50/30 rounded flex items-center justify-center">
                    <i class="pi pi-file-pdf text-2xl text-indigo-700"></i>
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">{{ selectedFile.name }}</p>
                    <p class="text-sm text-gray-500">
                      {{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB
                    </p>
                  </div>
                </div>
                <button
                  @click="clearFile"
                  class="text-gray-500 hover:text-red-500 p-2 rounded-full hover:bg-gray-100"
                >
                  <i class="pi pi-times"></i>
                </button>
              </div>

              <!-- File Preview -->
              <div class="mt-2">
                <div v-if="previewUrl" class="aspect-video bg-gray-50 rounded-md overflow-hidden border border-indigo-100">
                  <img
                    :src="previewUrl"
                    alt="File preview"
                    class="w-full h-full object-contain"
                  />
                </div>
                <div v-else class="aspect-video bg-gray-50 rounded-md border border-indigo-100 flex items-center justify-center">
                  <i class="pi pi-file text-4xl text-indigo-700"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Post Output Option -->
        <div class="flex items-center mt-4">
          <input
            type="checkbox"
            id="post-output"
            v-model="postOutputOption"
            class="w-4 h-4 text-indigo-700 border-indigo-100 rounded focus:ring-indigo-500"
          />
          <label for="post-output" class="ml-2 text-sm font-medium text-gray-700">
            Post this output to feeds (visible to class)
          </label>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-3">
          <button
            @click="showProductUploadModal = false"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="submitNewProduct"
            class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-100 transition-colors flex items-center gap-2"
            :disabled="!selectedFile"
            :class="{'opacity-50 cursor-not-allowed': !selectedFile}"
          >
            <i class="pi pi-check"></i>
            Submit Work
          </button>
        </div>
      </template>
    </Dialog>

    <!-- Archive Class Dialog -->
    <Dialog v-model:visible="showArchiveDialog"
        modal
        header="Archive Class"
        :style="{ width: '90%', maxWidth: '30rem' }">
        <div class="p-6">
            <div class="mb-6 text-center">
                <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
                    <i class="pi pi-exclamation-triangle text-red-600 text-xl"></i>
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-2">Archive this class?</h3>
                <p class="text-sm text-gray-500">
                    This will move the class to the archived section. You can restore it later if needed.
                </p>
            </div>
            <div class="flex justify-end gap-3">
                <button @click="showArchiveDialog = false"
                    class="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg">
                    Cancel
                </button>
                <button @click="confirmArchive"
                    class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg flex items-center gap-2">
                    <i class="pi pi-archive"></i>
                    Archive Class
                </button>
            </div>
        </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, inject } from 'vue';
import { Head, usePage, router } from '@inertiajs/vue3';
import MainLayout from '@/Layouts/MainLayout.vue';
import Dialog from 'primevue/dialog';

const page = usePage();
const auth = computed(() => page.props.auth);

const props = defineProps({
  className: {
    type: String,
    required: true,
    default: 'Digital Arts'
  },
  theme: {
    type: String,
    default: 'emerald'
  }
});

const activeTab = ref('portfolio');
const activeContentTab = ref('samples');

// Navigation tabs
const tabs = [
  { id: 'portfolio', name: 'Portfolio', icon: 'pi-folder' },
  { id: 'schedule', name: 'Schedule', icon: 'pi-calendar' },
];

// Portfolio state
const showPortfolioThemeDialog = ref(false);
const selectedTheme = ref(null);
const portfolioCreated = ref(true);
const selectedPortfolioTheme = ref('minimal'); // Default theme

// Portfolio folders data
const portfolioFolders = [
  { id: 'Mapeh', title: 'Mapeh', items: 10 }
];

// Selected folder and activity state
const selectedFolder = ref(null);
const selectedActivity = ref(null);

// Folder activities data
const folderActivities = ref([
  {
    type: 'project',
    title: 'Self-portrait',
    description: 'Artworks: Create a self-portrait using mixed media techniques',
    date: 'Nov 6, 2024'
  }
]);

// Student submissions
const studentSubmissions = ref([]);

// File upload state
const selectedFile = ref(null);
const previewUrl = ref(null);
const showSubmitDialog = ref(false);
const showProductUploadModal = ref(false);
const newProductCaption = ref('');
const postOutputOption = ref(false);

// Function to check if activity has been submitted
const hasSubmitted = (activity) => {
  return studentSubmissions.value.some(sub => sub.activityId === activity.title);
};

// Function to handle image loading errors
const handleImageError = (submission) => {
  submission.loadError = true;
  // Revoke the object URL to free memory
  if (submission.previewUrl) {
    URL.revokeObjectURL(submission.previewUrl);
  }
};

// Function to open folder content
const openFolderContent = (folder) => {
  selectedFolder.value = folder;
};

// Function to go back to folders view
const backToFolders = () => {
  selectedFolder.value = null;
};

// Function to open activity with all details
const openActivity = (activity) => {
  selectedActivity.value = activity;
};

// Handle file selection
const handleFileChange = (e) => {
  if (e.target.files && e.target.files[0]) {
    const file = e.target.files[0];
    selectedFile.value = file;

    // Create preview URL for images
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        previewUrl.value = e.target.result;
      };
      reader.readAsDataURL(file);
    } else {
      previewUrl.value = null;
    }
  }
};

// Clear selected file
const clearFile = () => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
  }
  selectedFile.value = null;
  previewUrl.value = null;
};

// Submit work function
const submitWork = (type) => {
  // Here you would handle the submission based on type ('private' or 'public')
  console.log(`Submitting work as ${type} with file:`, selectedFile.value);

  // Close dialog and reset form
  showSubmitDialog.value = false;

  // Show success message or redirect as needed
  // For demo purposes, we'll just clear the form
  clearFile();
};

// Settings Dropdown State
const showSettingsDropdown = ref(false);
const showArchiveDialog = ref(false);
const showAddActivityDialog = ref(false);
const settingsRef = ref(null);
const isSidebarCollapsed = inject('isSidebarCollapsed', ref(false));

// Toggle settings dropdown
const toggleSettingsDropdown = () => {
    showSettingsDropdown.value = !showSettingsDropdown.value;
};

// Close settings dropdown when clicking outside (robust)
const handleDocumentClick = (event) => {
  if (settingsRef.value && !settingsRef.value.contains(event.target)) {
    showSettingsDropdown.value = false;
  }
};

// Close menu when clicking outside
const handleClickOutside = (event) => {
  if (settingsRef.value && !settingsRef.value.contains(event.target)) {
    showSettingsDropdown.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleDocumentClick, true);
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleDocumentClick, true);
  document.removeEventListener('click', handleClickOutside);
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

// Add sample product function
const addSampleProduct = () => {
  // Show the product upload modal
  showProductUploadModal.value = true;
  // Reset form fields
  newProductCaption.value = '';
  postOutputOption.value = false;
  clearFile();
};

// Archive the current class
const confirmArchive = () => {
  // TODO: Implement actual archive functionality
  console.log('Archiving class:', className.value);

  // Show success message
  // In a real app, you would make an API call here
  alert('Class archived successfully!');

  // Close the dialog
  showArchiveDialog.value = false;

  // Optionally redirect to the archived classes page
  // router.get('/archived-classes');
};

// Submit new product
const submitNewProduct = () => {
  if (selectedFile.value) {
    // Create a new submission object
    const newSubmission = {
      activityId: selectedActivity.value.title,
      caption: newProductCaption.value,
      previewUrl: previewUrl.value,
      file: selectedFile.value,
      isImage: selectedFile.value.type.startsWith('image/'),
      date: new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      }),
      status: postOutputOption.value ? 'shared' : 'submitted',
      loadError: false // Initialize load error state
    };

    // Add the submission to the student's submissions
    studentSubmissions.value.push(newSubmission);

    // Close modal and reset form
    showProductUploadModal.value = false;
    newProductCaption.value = '';
    postOutputOption.value = false;
    clearFile();

    // Show success message
    console.log('Work submitted successfully:', newSubmission);
  }
};

defineOptions({
  layout: MainLayout
});
</script>

<style scoped>
/* Image container styles */
.aspect-video {
  aspect-ratio: 16 / 9;
  @apply relative overflow-hidden bg-slate-100;
}

/* Image styles */
.aspect-video img {
  @apply max-h-full max-w-full object-contain;
  @apply transition-all duration-300 ease-in-out;
}

/* Fallback container styles */
.aspect-video .fallback-container {
  @apply flex flex-col items-center justify-center h-full w-full;
  @apply bg-gray-50 text-gray-400;
}

/* Add these styles for consistent calendar styling */
.calendar-day {
  @apply p-4 border rounded-lg hover:shadow-md cursor-pointer transition-all;
}

.calendar-day-active {
  @apply font-semibold text-gray-900;
}

.calendar-time {
  @apply text-sm mt-1 text-gray-900;
}

/* DataTable styles */
:deep(.p-datatable) {
  border-radius: 0.75rem;
  overflow: hidden;
  margin-top: 1rem;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
  background-color: #f9fafb;
  color: #111827;
  font-weight: 600;
  padding: 1rem;
  border-bottom: 2px solid #e5e7eb;
}

:deep(.p-datatable .p-datatable-tbody > tr) {
  transition: background-color 0.2s;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
  background-color: #f9fafb;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
  padding: 1rem;
}

/* Dialog styles */
:deep(.p-dialog-header) {
  background: linear-gradient(90deg, #4338ca, #6d28d9, #2563eb);
  color: white;
}

:deep(.p-dialog-content) {
  background-color: white;
}

/* Add this new style for better responsive layout */
@media (max-width: 1024px) {
  .lg\:w-64 {
    width: 100%;
  }
}

/* Add these styles for smooth transitions */
.bg-gradient-to-br {
  transition: all 0.3s ease;
}

.h-2 {
  transition: width 0.5s ease;
}

/* Line clamp for text truncation */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Add theme variables */
:root {
  --theme-purple: #4338ca;
  --theme-blue: #2563eb;
  --theme-light: #f9fafb;
  --theme-accent: #6366f1;
  --theme-dark: #111827;
}
</style>
