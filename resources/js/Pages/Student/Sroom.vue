<template>
  <div class="flex flex-col">
    <!-- Class Header -->
    <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-6 md:p-4 shadow-lg rounded-t-xl">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div class="space-y-3">
          <h1 class="text-xl md:text-2xl font-bold text-white px-4 py-2 md:px-6 md:py-3 rounded-lg inline-block bg-white/20">
            {{ props.className }}
          </h1>
          <p class="text-white/90 ml-2 flex items-center gap-2">
            <i class="pi pi-user"></i>
            Student: {{ currentUser.name }}
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
      <div class="w-full px-4 sm:px-6 pt-1 pb-8 transition-all duration-300"
           :style="{ 'padding-left': '1.5rem', 'padding-right': '1.5rem' }">
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
                      @click="backToActivitiesList"
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
                          v-if="!hasSubmittedWork"
                          @click="addSampleProduct"
                          class="group flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                        >
                          <i class="pi pi-plus"></i>
                          <span>Turn in</span>
                        </button>
                        <template v-else>
                          <button
                            v-if="hasScore"
                            @click="showScoreDialog = true"
                            class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                          >
                            <i class="pi pi-star-fill"></i>
                            <span>View Score</span>
                          </button>
                          <span
                            class="px-4 py-2 rounded-lg bg-green-100 text-green-800 flex items-center gap-2"
                          >
                            <i class="pi pi-check-circle"></i>
                            <span>Submitted</span>
                          </span>
                        </template>
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

                  <!-- Scoring Criteria Section -->
                  <div class="mb-6">
                    <div v-if="selectedActivity.scoringCriteria && selectedActivity.scoringCriteria.length > 0" class="bg-indigo-50 rounded-lg p-4 border border-indigo-200">
                      <h3 class="text-base font-semibold text-gray-900 mb-3 flex items-center gap-2">
                        <i class="pi pi-star text-indigo-600"></i>
                        Scoring Criteria
                      </h3>
                      <div class="space-y-2">
                        <div
                          v-for="(criterion, index) in selectedActivity.scoringCriteria"
                          :key="index"
                          class="flex items-center justify-between p-3 bg-white rounded-lg border border-indigo-100"
                        >
                          <div class="flex items-center gap-2">
                            <div class="w-2 h-2 rounded-full bg-indigo-500"></div>
                            <span class="text-sm font-medium text-gray-900">{{ criterion.name }}</span>
                          </div>
                          <div class="flex items-center gap-1">
                            <span class="text-sm font-semibold text-indigo-600">{{ criterion.maxScore }}</span>
                            <span class="text-xs text-gray-500">pts</span>
                          </div>
                        </div>
                        <!-- Total Points -->
                        <div class="flex items-center justify-between p-3 bg-indigo-100 rounded-lg border border-indigo-200 mt-2">
                          <span class="text-sm font-semibold text-gray-900">Total Points</span>
                          <div class="flex items-center gap-1">
                            <span class="text-base font-bold text-indigo-700">{{ calculateTotalPoints(selectedActivity.scoringCriteria) }}</span>
                            <span class="text-xs text-gray-600">pts</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div v-else class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                      <div class="flex items-center gap-2 text-gray-600">
                        <i class="pi pi-info-circle"></i>
                        <span class="text-sm">No scoring criteria has been set for this activity yet.</span>
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
                        <div class="aspect-video relative bg-gray-100 overflow-hidden flex items-center justify-center p-4">
                          <template v-if="submission.isImage">
                            <img
                              :src="submission.previewUrl"
                              :alt="submission.caption || 'Submitted work'"
                              class="max-w-full max-h-full object-contain"
                              @error="handleImageError(submission)"
                              v-show="!submission.loadError"
                              style="display: block; margin: auto;"
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
                          <p v-if="submission.caption" class="text-sm text-gray-600 mb-2">{{ submission.caption }}</p>
                          
                          <!-- Score Display -->
                          <div v-if="submission.score !== null && submission.score !== undefined" class="mb-2 p-2 bg-indigo-50 rounded-lg">
                            <div class="flex items-center justify-between">
                              <span class="text-sm font-medium text-indigo-900">Score:</span>
                              <span class="text-lg font-bold text-indigo-700">{{ submission.score }}</span>
                            </div>
                            <p v-if="submission.feedback" class="text-xs text-gray-600 mt-1 italic">
                              "{{ submission.feedback }}"
                            </p>
                          </div>
                          
                          <div class="flex justify-between items-center mt-2">
                            <span class="text-xs text-gray-500">{{ submission.date }}</span>
                            <span class="text-xs px-2 py-1 rounded"
                                  :class="submission.status === 'scored' ? 'bg-green-100 text-green-800' : 
                                         submission.status === 'unscored' ? 'bg-yellow-100 text-yellow-800' : 
                                         'bg-blue-100 text-blue-800'">
                              {{ submission.status === 'scored' ? 'Scored' : submission.status === 'unscored' ? 'Unscored' : submission.status }}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Activities Table -->
                <div v-else class="bg-white/80 backdrop-blur-sm rounded-xl shadow-sm overflow-hidden border border-indigo-100">
                  <!-- Loading State -->
                  <div v-if="isLoadingActivities" class="flex justify-center items-center py-12">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                  </div>

                  <!-- Empty State -->
                  <div v-else-if="folderActivities.length === 0" class="text-center py-12">
                    <i class="pi pi-inbox text-4xl text-gray-400 mb-4"></i>
                    <p class="text-gray-500">No activities available yet.</p>
                  </div>

                  <!-- Activities List -->
                  <template v-else>
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
                    <div v-for="(activity, index) in folderActivities" :key="activity.id"
                      class="group border-b border-indigo-100 hover:bg-indigo-50 transition-colors duration-200"
                      @click="openActivity(activity)">
                      <!-- Main Activity Row -->
                      <div class="flex items-center px-4 md:px-6 py-4 cursor-pointer">
                        <div class="w-32">
                          <span class="text-sm text-indigo-700 capitalize">{{ activity.type }}</span>
                        </div>
                        <div class="w-32 md:w-48">
                          <span class="font-medium text-indigo-700 transition-colors duration-100">{{ activity.title }}</span>
                        </div>
                        <div class="flex-1">
                          <span class="text-indigo-700 group-hover:text-indigo-900 transition-colors duration-200 line-clamp-2">{{ activity.description }}</span>
                        </div>
                        <div class="w-32 md:w-48 text-right flex items-center justify-end gap-2">
                          <span class="text-sm text-indigo-600">{{ activity.date }}</span>
                          <span v-if="activity.hasSubmitted" class="px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 flex items-center gap-1">
                            <i class="pi pi-check-circle"></i>
                            Submitted
                          </span>
                        </div>
                      </div>
                    </div>
                  </template>
                </div>
              </div>

              <!-- Folder Grid -->
              <div v-if="!selectedFolder" class="space-y-6">
                <!-- Header with title -->
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                  <h2 class="text-xl md:text-2xl font-bold text-gray-900">My Portfolio</h2>
                </div>
                <!-- Loading State -->
                <div v-if="isLoadingFolders" class="flex justify-center items-center py-12">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                  <span class="ml-3 text-gray-600">Loading folders...</span>
                </div>
                
                <!-- Empty State -->
                <div v-else-if="portfolioFolders.length === 0" class="text-center py-12">
                  <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-gray-100 mb-4">
                    <i class="pi pi-folder text-gray-400 text-xl"></i>
                  </div>
                  <h3 class="text-lg font-medium text-gray-900 mb-2">No Portfolio Folders</h3>
                  <p class="text-gray-500">Your teacher hasn't created any portfolio folders yet.</p>
                </div>
                
                <!-- Folders Grid -->
                <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
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
            class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
            :disabled="!selectedFile || isSubmitting"
            :class="{'opacity-50 cursor-not-allowed': !selectedFile || isSubmitting}"
          >
            <i v-if="!isSubmitting" class="pi pi-check"></i>
            <i v-else class="pi pi-spin pi-spinner"></i>
            {{ isSubmitting ? 'Submitting...' : 'Submit Work' }}
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

    <!-- View Score Dialog -->
    <Dialog 
      v-model:visible="showScoreDialog" 
      modal 
      :closable="true"
      :style="{ width: '90%', maxWidth: '600px' }"
      :contentStyle="{ padding: '0' }"
      position="center"
      class="score-dialog"
    >
      <template #header>
        <div class="flex items-center gap-2 px-5 py-3 bg-gradient-to-r from-indigo-600 to-purple-600">
          <i class="pi pi-star-fill text-white text-lg"></i>
          <h3 class="text-lg font-bold text-white">Your Score</h3>
        </div>
      </template>

      <div v-if="submissionScore" class="p-4 space-y-4">
        <!-- Scoring Criteria Breakdown -->
        <div v-if="parsedCriteriaScores && parsedCriteriaScores.length > 0" class="space-y-3">
          <h4 class="text-sm font-semibold text-gray-800 flex items-center gap-2">
            <i class="pi pi-list text-indigo-600 text-sm"></i>
            Score Breakdown
          </h4>
          <div class="space-y-2">
            <div v-for="(criterion, index) in parsedCriteriaScores" :key="index" 
                 class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200 hover:border-indigo-300 transition-all">
              <div class="flex items-center gap-2">
                <div class="w-6 h-6 bg-indigo-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-xs font-bold text-indigo-600">{{ index + 1 }}</span>
                </div>
                <p class="text-sm font-semibold text-gray-800">{{ criterion.name }}</p>
              </div>
              <div class="flex items-baseline gap-1 bg-white px-3 py-1.5 rounded-md shadow-sm">
                <span class="text-lg font-bold text-indigo-700">{{ criterion.score }}</span>
                <span class="text-sm text-gray-400">/</span>
                <span class="text-sm font-medium text-gray-600">{{ criterion.maxScore }}</span>
                <span class="text-xs text-gray-500">pts</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Show message if no criteria breakdown available -->
        <div v-else class="p-3 bg-amber-50 rounded-lg border border-amber-200 text-center">
          <i class="pi pi-info-circle text-amber-600 text-sm"></i>
          <p class="text-xs text-amber-700 font-medium mt-1">No detailed score breakdown available</p>
        </div>

        <!-- Total Score -->
        <div class="p-4 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-lg shadow-md">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <i class="pi pi-trophy text-yellow-300 text-lg"></i>
              <span class="text-base font-bold text-white">Total Score</span>
            </div>
            <div class="flex items-baseline gap-1 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-md">
              <span class="text-3xl font-bold text-white">
                {{ submissionScore.score }}
              </span>
              <span class="text-xl text-white/80">/</span>
              <span class="text-xl font-semibold text-white/90">
                {{ calculateMaxScore(submissionScore.criteria_scores) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Feedback -->
        <div v-if="submissionScore.feedback" class="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
          <h4 class="text-sm font-semibold text-gray-800 mb-2 flex items-center gap-2">
            <i class="pi pi-comment text-blue-600 text-sm"></i>
            Teacher's Feedback
          </h4>
          <div class="bg-white p-3 rounded-md">
            <p class="text-sm text-gray-700 italic">"{{ submissionScore.feedback }}"</p>
          </div>
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, inject } from 'vue';
import axios from 'axios';
import Dialog from 'primevue/dialog';

const props = defineProps({
  className: {
    type: String,
    required: false,
    default: 'Grade 1 - A'
  },
  theme: {
    type: String,
    default: 'emerald'
  }
});

// Get selected class from localStorage
const selectedClass = ref(null);
const currentUser = ref({
    name: 'Student Name',
    email: 'student@example.com',
    role: 'student'
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
const portfolioFolders = ref([]);
const isLoadingFolders = ref(false);

// Selected folder and activity state
const selectedFolder = ref(null);
const selectedActivity = ref(null);

// Folder activities data
const folderActivities = ref([]);
const isLoadingActivities = ref(false);

// Student submissions
const studentSubmissions = ref([]);

// File upload state
const selectedFile = ref(null);
const previewUrl = ref(null);
const showSubmitDialog = ref(false);
const showProductUploadModal = ref(false);
const newProductCaption = ref('');
const postOutputOption = ref(false);
const isSubmitting = ref(false);

// Check if student has already submitted (reactive state)
const hasSubmittedWork = ref(false);
const existingSubmission = ref(null);
const hasScore = ref(false);
const showScoreDialog = ref(false);
const submissionScore = ref(null);

// Computed property to safely parse criteria scores
const parsedCriteriaScores = computed(() => {
  if (!submissionScore.value || !submissionScore.value.criteria_scores) {
    console.log('⚠️ No criteria_scores found');
    return [];
  }
  
  try {
    const criteria = typeof submissionScore.value.criteria_scores === 'string'
      ? JSON.parse(submissionScore.value.criteria_scores)
      : submissionScore.value.criteria_scores;
    
    console.log('✅ Parsed criteria scores:', criteria);
    return criteria;
  } catch (error) {
    console.error('❌ Error parsing criteria scores:', error);
    return [];
  }
});

// Function to handle image loading errors
const handleImageError = (submission) => {
  console.error('❌ Image failed to load:', submission.caption);
  submission.loadError = true;
};

// Function to open folder content
const openFolderContent = async (folder) => {
  selectedFolder.value = folder;
  
  // Save folder view state
  localStorage.setItem('student_current_view', JSON.stringify({
    selectedFolder: folder,
    selectedActivity: null
  }));
  console.log('💾 Saved view state: Folder', folder.title);
  
  // Load activities for this folder
  await loadFolderActivities(folder.id);
};

// Function to load activities from database
const loadFolderActivities = async (folderId) => {
  isLoadingActivities.value = true;
  try {
    const response = await axios.get(`/api/portfolio/folders/${folderId}/activities/`);
    if (response.data) {
      // Format activities for display and check submission status for each
      const activitiesWithStatus = await Promise.all(
        response.data.map(async (activity) => {
          // Check if student has submitted for this activity
          let hasSubmitted = false;
          try {
            const submissionResponse = await axios.get(`/api/activities/${activity.id}/submissions/`);
            hasSubmitted = submissionResponse.data && submissionResponse.data.length > 0;
          } catch (error) {
            console.error(`Error checking submission for activity ${activity.id}:`, error);
          }

          // Parse scoring criteria if it exists
          let scoringCriteria = [];
          if (activity.scoring_criteria) {
            try {
              scoringCriteria = typeof activity.scoring_criteria === 'string' 
                ? JSON.parse(activity.scoring_criteria) 
                : activity.scoring_criteria;
              console.log('Parsed scoring criteria for activity:', activity.title, scoringCriteria);
            } catch (error) {
              console.error('Error parsing scoring criteria:', error);
            }
          } else {
            console.log('No scoring criteria found for activity:', activity.title);
          }

          return {
            id: activity.id,
            type: activity.activity_type,
            title: activity.title,
            description: activity.description,
            date: activity.due_date ? new Date(activity.due_date).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'short',
              day: 'numeric'
            }) : '',
            due_date: activity.due_date,
            hasSubmitted: hasSubmitted,
            scoringCriteria: scoringCriteria
          };
        })
      );
      
      folderActivities.value = activitiesWithStatus;
      console.log('Loaded activities for student:', folderActivities.value);
    }
  } catch (error) {
    console.error('Error loading activities:', error);
    folderActivities.value = [];
  } finally {
    isLoadingActivities.value = false;
  }
};

// Function to load portfolio folders
const loadPortfolioFolders = async () => {
  isLoadingFolders.value = true;
  try {
    const response = await axios.get('/api/portfolio/folders/');
    
    console.log('Student API Response:', response.data); // Debug log
    
    if (response.data && Array.isArray(response.data)) {
      portfolioFolders.value = response.data.map(folder => ({
        id: folder.id,
        title: folder.name,
        items: folder.activities ? folder.activities.length : 0,
        description: folder.description || ''
      }));
    } else {
      console.warn('API did not return an array:', response.data);
      portfolioFolders.value = [];
    }
  } catch (error) {
    console.error('Error loading folders:', error);
    portfolioFolders.value = [];
  } finally {
    isLoadingFolders.value = false;
  }
};

// Function to go back to folders view
const backToFolders = () => {
  selectedFolder.value = null;
  selectedActivity.value = null;
  studentSubmissions.value = [];
  
  // Clear saved view state
  localStorage.removeItem('student_current_view');
  console.log('🗑️ Cleared view state');
};

// Function to go back to activities list
const backToActivitiesList = () => {
  selectedActivity.value = null;
  studentSubmissions.value = [];
  hasSubmittedWork.value = false;
  
  // Update view state to folder only
  if (selectedFolder.value) {
    localStorage.setItem('student_current_view', JSON.stringify({
      selectedFolder: selectedFolder.value,
      selectedActivity: null
    }));
    console.log('💾 Updated view state: Back to folder', selectedFolder.value.title);
  }
};

// Calculate total points from scoring criteria
const calculateTotalPoints = (criteria) => {
  if (!criteria || criteria.length === 0) return 0;
  return criteria.reduce((total, criterion) => {
    return total + (parseInt(criterion.maxScore) || 0);
  }, 0);
};

// Calculate max score from criteria_scores JSON
const calculateMaxScore = (criteriaScoresJson) => {
  if (!criteriaScoresJson) return 0;
  try {
    const criteria = typeof criteriaScoresJson === 'string' 
      ? JSON.parse(criteriaScoresJson) 
      : criteriaScoresJson;
    return criteria.reduce((total, criterion) => {
      return total + (parseInt(criterion.maxScore) || 0);
    }, 0);
  } catch (error) {
    console.error('Error calculating max score:', error);
    return 0;
  }
};

// Function to open activity with all details
const openActivity = async (activity) => {
  selectedActivity.value = activity;
  
  // Reset score state when opening new activity
  hasScore.value = false;
  submissionScore.value = null;
  
  // Save current view state to localStorage
  localStorage.setItem('student_current_view', JSON.stringify({
    selectedFolder: selectedFolder.value,
    selectedActivity: {
      id: activity.id,
      title: activity.title
    }
  }));
  console.log('💾 Saved view state: Activity', activity.title);
  
  // Use the hasSubmitted status from the activity object if available
  if (activity.hasSubmitted !== undefined) {
    hasSubmittedWork.value = activity.hasSubmitted;
  } else {
    // Otherwise, check submission status from API
    await checkSubmissionStatus(activity.id);
  }
  
  // Load submissions for this activity
  await loadActivitySubmissions(activity.id);
};

// Load submissions for the current activity
const loadActivitySubmissions = async (activityId) => {
  try {
    const response = await axios.get(`/api/activities/${activityId}/submissions/`);
    console.log('📥 API Response - Submissions:', response.data);
    
    if (response.data && response.data.length > 0) {
      // Map API response to display format
      studentSubmissions.value = response.data.map(submission => {
        let previewUrl = submission.file_path;
        
        console.log('🖼️ Processing submission:', {
          caption: submission.caption,
          file_type: submission.file_type,
          has_file_path: !!submission.file_path,
          file_path_length: submission.file_path?.length,
          file_path_starts_with: submission.file_path?.substring(0, 20),
          status: submission.status,
          score: submission.score
        });
        
        // Check if this submission has been scored
        if (submission.status === 'scored' && submission.score !== null) {
          hasScore.value = true;
          submissionScore.value = {
            score: submission.score,
            feedback: submission.feedback,
            criteria_scores: submission.criteria_scores
          };
          console.log('✅ Submission has been scored:', submissionScore.value);
        }
        
        // Format base64 image data if needed
        if (submission.file_type === 'image') {
          if (!previewUrl || previewUrl.trim() === '') {
            console.error('❌ Empty file_path for image submission:', submission.caption);
            previewUrl = null; // Will show error state
          } else {
            // Remove any whitespace or newlines
            previewUrl = previewUrl.trim();
            
            // Check if it's already a data URL
            if (!previewUrl.startsWith('data:')) {
              // Detect image type from base64 header
              let imageType = 'png'; // default
              
              if (previewUrl.startsWith('/9j/')) {
                imageType = 'jpeg';
              } else if (previewUrl.startsWith('iVBOR')) {
                imageType = 'png';
              }
              
              // Format as data URL
              previewUrl = `data:image/${imageType};base64,${previewUrl}`;
              console.log('✅ Formatted as data URL:', imageType, 'Length:', previewUrl.length);
            } else {
              console.log('✅ Already a data URL, Length:', previewUrl.length);
            }
          }
        }
        
        return {
          activityId: activityId,
          caption: submission.caption,
          previewUrl: previewUrl,
          isImage: submission.file_type === 'image',
          date: new Date(submission.submitted_at).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
          }),
          status: submission.status,
          score: submission.score,
          feedback: submission.feedback,
          loadError: false
        };
      });
      console.log('✅ Total submissions loaded:', studentSubmissions.value.length);
    } else {
      studentSubmissions.value = [];
      console.log('⚠️ No submissions found');
    }
  } catch (error) {
    console.error('❌ Error loading submissions:', error);
    studentSubmissions.value = [];
  }
};

const checkSubmissionStatus = async (activityId) => {
  try {
    const response = await axios.get(`/api/activities/${activityId}/submissions/`);
    if (response.data && response.data.length > 0) {
      hasSubmittedWork.value = true;
      existingSubmission.value = response.data[0];
      console.log('Student already submitted:', existingSubmission.value);
    } else {
      hasSubmittedWork.value = false;
      existingSubmission.value = null;
    }
  } catch (error) {
    console.error('Error checking submission status:', error);
    hasSubmittedWork.value = false;
  }
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

// Function to authenticate with backend
const authenticateWithBackend = async () => {
  try {
    // First check if already authenticated
    const checkResponse = await axios.get('/api/validate-session/');
    if (checkResponse.data.authenticated) {
      console.log('Already authenticated:', checkResponse.data.user);
      return true;
    }
  } catch (error) {
    // Not authenticated, try to create session
    try {
      const authResponse = await axios.post('/api/validate-session/', {
        role: 'student'
      });
      console.log('Authentication successful:', authResponse.data.user);
      return true;
    } catch (authError) {
      console.error('Authentication failed:', authError);
      return false;
    }
  }
};

// Load portfolio folders when component mounts
onMounted(async () => {
  // Authenticate with backend first, then load folders
  const authenticated = await authenticateWithBackend();
  if (authenticated) {
    loadPortfolioFolders();
    
    // Restore previous view state after refresh
    const savedView = localStorage.getItem('student_current_view');
    if (savedView) {
      try {
        const viewState = JSON.parse(savedView);
        console.log('🔄 Restoring view state:', viewState);
        
        if (viewState.selectedFolder) {
          selectedFolder.value = viewState.selectedFolder;
          // Load activities for this folder
          await loadFolderActivities(viewState.selectedFolder.id);
          
          if (viewState.selectedActivity) {
            // Find the activity in the loaded activities
            const activity = folderActivities.value.find(a => a.id === viewState.selectedActivity.id);
            if (activity) {
              await openActivity(activity);
              console.log('✅ Restored activity view:', activity.title);
            }
          }
        }
      } catch (error) {
        console.error('❌ Error restoring view state:', error);
        localStorage.removeItem('student_current_view');
      }
    }
  } else {
    console.error('Failed to authenticate with backend');
  }
});

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
  console.log('Archiving class:', props.className);

  // Show success message
  // In a real app, you would make an API call here
  alert('Class archived successfully!');

  // Close the dialog
  showArchiveDialog.value = false;

  // Optionally redirect to the archived classes page
  // You can implement navigation here if needed
};

// Submit new product
const submitNewProduct = async () => {
  // Prevent multiple submissions
  if (isSubmitting.value) {
    console.log('Already submitting, please wait...');
    return;
  }

  if (!selectedFile.value || !selectedActivity.value) {
    alert('Please select a file and activity');
    return;
  }

  isSubmitting.value = true;

  try {
    // Get file type
    const fileType = selectedFile.value.type.startsWith('image/') ? 'image' : 
                     selectedFile.value.type.includes('pdf') ? 'pdf' : 'document';

    // For now, we'll store the file as a data URL (base64)
    // In production, you should upload to a file server
    const filePath = previewUrl.value || URL.createObjectURL(selectedFile.value);

    console.log('Submitting work for activity:', selectedActivity.value);

    // Submit to API
    const response = await axios.post(`/api/activities/${selectedActivity.value.id}/submissions/`, {
      caption: newProductCaption.value,
      file_path: filePath,
      file_type: fileType,
      post_to_feed: postOutputOption.value
    });

    if (response.data) {
      console.log('Work submitted successfully:', response.data);

      // Update submission status
      hasSubmittedWork.value = true;
      existingSubmission.value = response.data;

      // Add to local submissions array
      const newSubmission = {
        activityId: selectedActivity.value.id,
        caption: newProductCaption.value,
        previewUrl: filePath,
        file: selectedFile.value,
        isImage: fileType === 'image',
        date: new Date().toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
        }),
        status: 'submitted',
        loadError: false
      };

      studentSubmissions.value.push(newSubmission);

      // Close modal and reset form
      showProductUploadModal.value = false;
      newProductCaption.value = '';
      postOutputOption.value = false;
      clearFile();

      alert('Work submitted successfully!');
    }
  } catch (error) {
    console.error('Error submitting work:', error);
    alert('Failed to submit work: ' + (error.response?.data?.error || error.message));
  } finally {
    isSubmitting.value = false;
  }
};

</script>

<style scoped>
/* Image container styles */
.aspect-video {
  aspect-ratio: 16 / 9;
  position: relative;
  overflow: hidden;
  background-color: #f1f5f9;
}

/* Image styles */
.aspect-video img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
  transition: all 0.3s ease-in-out;
}

/* Fallback container styles */
.aspect-video .fallback-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  background-color: #f9fafb;
  color: #9ca3af;
}

/* Add these styles for consistent calendar styling */
.calendar-day {
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.calendar-day:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.calendar-day-active {
  font-weight: 600;
  color: #111827;
}

.calendar-time {
  font-size: 0.875rem;
  margin-top: 0.25rem;
  color: #111827;
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
  line-clamp: 2;
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
