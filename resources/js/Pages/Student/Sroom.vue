<template>
  <div class="flex flex-col">
    <!-- Class Header -->
    <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-4 md:p-3 shadow-lg rounded-t-xl">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div class="space-y-2">
          <h1 class="text-xl md:text-2xl font-bold text-white px-4 py-2 md:px-5 md:py-2 rounded-lg inline-block bg-white/20">
            {{ props.className }}
          </h1>
          <p class="text-white/90 ml-2 flex items-center gap-2 text-sm">
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
      <div class="flex flex-wrap gap-2 md:gap-4 mt-3 md:mt-4">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="flex items-center gap-2 text-white/90 px-4 py-2 md:px-5 md:py-2.5 rounded-lg transition-all duration-300 relative overflow-hidden group"
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
                  <!-- Header Title -->
                  <div class="rounded-lg py-2 px-4">
                    <span class="text-2xl font-bold text-indigo-900">
                      {{ showSubmittedCollection ? 'Submitted Collection Activity' : `List of Activities - ${selectedFolder.title}` }}
                    </span>
                  </div>

                  <div class="flex flex-wrap gap-2">
                    <!-- Submitted Collection button -->
                    <button
                      v-if="selectedFolder && !selectedActivity && !showSubmittedCollection"
                      @click="openSubmittedCollection"
                      class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                    >
                      <i class="pi pi-folder-open"></i>
                      <span>Submitted Collection</span>
                    </button>
                    
                    <!-- Select Button (Submitted Collection) -->
                    <button
                      v-if="!selectedActivity && showSubmittedCollection && submittedCollection.length > 0"
                      @click="toggleSelectMode"
                      class="flex items-center gap-2 px-4 py-2 rounded-lg transition-colors duration-200"
                      :class="isSelectMode 
                        ? 'bg-indigo-600 text-white hover:bg-indigo-700' 
                        : 'bg-white text-indigo-600 border border-indigo-600 hover:bg-indigo-600 hover:text-white'"
                    >
                      <i :class="isSelectMode ? 'pi pi-times' : 'pi pi-check-square'"></i>
                      <span>{{ isSelectMode ? 'Cancel' : 'Select' }}</span>
                    </button>
                    
                    <!-- Remove Selected Button -->
                    <button
                      v-if="isSelectMode && selectedSubmissions.length > 0"
                      @click="deleteAction = 'selected'; showDeleteConfirmDialog = true"
                      class="flex items-center gap-2 px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 transition-colors duration-200"
                    >
                      <i class="pi pi-eye-slash"></i>
                      <span>Remove ({{ selectedSubmissions.length }})</span>
                    </button>
                    
                    <!-- Remove All Button -->
                    <button
                      v-if="!selectedActivity && showSubmittedCollection && submittedCollection.length > 0 && !isSelectMode"
                      @click="deleteAction = 'all'; showDeleteConfirmDialog = true"
                      class="flex items-center gap-2 px-4 py-2 rounded-lg bg-white text-red-600 border border-red-600 hover:bg-red-600 hover:text-white transition-colors duration-200"
                    >
                      <i class="pi pi-eye-slash"></i>
                      <span>Remove All</span>
                    </button>
                    
                    <!-- Back button -->
                    <button
                      v-if="!selectedActivity && showSubmittedCollection"
                      @click="closeSubmittedCollection"
                      class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                    >
                      <i class="pi pi-arrow-left"></i>
                      <span>Back to Activities</span>
                    </button>
                    <button
                      v-else-if="!selectedActivity"
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
                  <!-- Top Section: Activity Header Card -->
                  <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-6">
                    <!-- Header with Gradient -->
                    <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 px-6 py-4">
                      <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                          <div class="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                            <i class="pi pi-book text-white text-lg"></i>
                          </div>
                          <div>
                            <h2 class="text-xl font-bold text-white">{{ selectedActivity.title }}</h2>
                            <p class="text-sm text-white/80 mt-0.5">Activity Details</p>
                          </div>
                        </div>
                        <div class="flex items-center gap-2">
                          <span class="px-3 py-1.5 bg-white/20 text-white text-sm font-medium rounded-full">
                            <i class="pi pi-calendar mr-1.5"></i>
                            Due: {{ selectedActivity.date }}<span v-if="selectedActivity.formattedTime"> at {{ selectedActivity.formattedTime }}</span>
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Content Area -->
                    <div class="p-6">
                      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <!-- Left: Activity Info -->
                        <div class="lg:col-span-2 space-y-4">
                          <!-- Type -->
                          <div class="flex items-start gap-3">
                            <div class="w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center flex-shrink-0">
                              <i class="pi pi-tag text-indigo-600"></i>
                            </div>
                            <div class="flex-1">
                              <div class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Activity Type</div>
                              <div class="text-sm font-medium text-gray-900 capitalize">{{ selectedActivity.type }}</div>
                            </div>
                          </div>
                          
                          <!-- Instructions -->
                          <div class="flex items-start gap-3">
                            <div class="w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center flex-shrink-0">
                              <i class="pi pi-align-left text-indigo-600"></i>
                            </div>
                            <div class="flex-1">
                              <div class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Instructions</div>
                              <div class="text-sm text-gray-700 leading-relaxed">
                                {{ selectedActivity.description }}
                              </div>
                            </div>
                          </div>
                        </div>
                        
                        <!-- Right: Your Work Card -->
                        <div class="lg:col-span-1">
                          <div class="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl border-2 border-indigo-200 p-4 h-full">
                            <!-- Header -->
                            <div class="mb-4">
                              <div class="flex items-center justify-between mb-3">
                                <div class="flex items-center gap-2">
                                  <div class="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
                                    <i class="pi pi-briefcase text-white text-sm"></i>
                                  </div>
                                  <h3 class="text-base font-bold text-gray-800">Your Work</h3>
                                </div>
                                
                                <!-- Status Badge (Main Design) -->
                                <div class="flex flex-col items-end gap-1">
                                  <!-- Submitted Late: Was missing but then turned in -->
                                  <span
                                    v-if="hasSubmittedWork && existingSubmission?.is_late"
                                    class="px-3 py-1.5 rounded-lg bg-orange-100 text-orange-800 flex items-center gap-1.5 text-xs font-medium"
                                  >
                                    <i class="pi pi-clock text-xs"></i>
                                    <span>Submitted late</span>
                                  </span>
                                  <!-- Submitted: Turned in on time -->
                                  <span
                                    v-else-if="hasSubmittedWork"
                                    class="px-3 py-1.5 rounded-lg bg-green-100 text-green-800 flex items-center gap-1.5 text-xs font-medium"
                                  >
                                    <i class="pi pi-check-circle text-xs"></i>
                                    <span>Submitted</span>
                                  </span>
                                  <!-- Missing: Past due and not submitted -->
                                  <span
                                    v-else-if="!hasSubmittedWork && isPastDue"
                                    class="px-3 py-1.5 rounded-lg bg-red-100 text-red-800 flex items-center gap-1.5 text-xs font-medium"
                                  >
                                    <i class="pi pi-times-circle text-xs"></i>
                                    <span>Missing</span>
                                  </span>
                                  <!-- Pending: Assigned but not yet due -->
                                  <span
                                    v-else
                                    class="px-3 py-1.5 rounded-lg bg-yellow-100 text-yellow-800 flex items-center gap-1.5 text-xs font-medium"
                                  >
                                    <i class="pi pi-clock text-xs"></i>
                                    <span>Pending</span>
                                  </span>
                                  
                                  <!-- Submitted Date & Time (Show when submitted) -->
                                  <span
                                    v-if="hasSubmittedWork && existingSubmission?.submitted_at"
                                    class="text-xs text-gray-500"
                                  >
                                    {{ formatSubmittedDateTime(existingSubmission.submitted_at) }}
                                  </span>
                                </div>
                              </div>
                            </div>
                            
                            <!-- Action Buttons -->
                            <div class="flex flex-col gap-2 mb-4">
                              <button
                                v-if="hasSubmittedWork && hasScore"
                                @click="showScoreDialog = true"
                                class="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200 font-medium"
                              >
                                <i class="pi pi-star-fill"></i>
                                <span>View Score</span>
                              </button>
                              
                              <!-- Post Output Button (Shows if not posted to feed yet) -->
                              <button
                                v-if="hasSubmittedWork && existingSubmission && !existingSubmission.post_to_feed"
                                @click="openPostOutputDialog"
                                class="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-green-600 text-white hover:bg-green-700 transition-colors duration-200 font-medium"
                                title="Post your work to class feed"
                              >
                                <i class="pi pi-send"></i>
                                <span>Post Output</span>
                              </button>
                            </div>
                        
                            <!-- Files Display (Draft or Submitted) -->
                            <div v-if="draftFiles.length > 0 || (hasSubmittedWork && studentSubmissions.length > 0)" class="mb-3 space-y-2">
                          <!-- Show draft files if not submitted -->
                          <div
                            v-if="!hasSubmittedWork"
                            v-for="file in draftFiles"
                            :key="file.id"
                            class="flex items-center gap-2 p-2 bg-white rounded-lg border border-indigo-200 hover:border-indigo-300 transition-all group"
                          >
                            <!-- Thumbnail (Clickable) -->
                            <button
                              @click="viewDraftFile(file)"
                              class="w-10 h-10 rounded-md flex items-center justify-center flex-shrink-0 overflow-hidden hover:opacity-80 transition-opacity"
                              :class="file.type === 'image' ? 'bg-gray-100' : 'bg-indigo-100'"
                            >
                              <img
                                v-if="file.type === 'image' && file.path"
                                :src="file.path"
                                :alt="file.name"
                                class="w-full h-full object-cover"
                                @error="(e) => { e.target.style.display = 'none'; e.target.nextElementSibling.style.display = 'flex'; }"
                              />
                              <div 
                                class="w-full h-full flex items-center justify-center"
                                :style="file.type === 'image' ? 'display: none;' : ''"
                              >
                                <i v-if="file.type === 'image'" class="pi pi-image text-indigo-600 text-lg"></i>
                                <i v-else-if="file.type === 'pdf'" class="pi pi-file-pdf text-red-600 text-lg"></i>
                                <i v-else class="pi pi-file text-gray-600 text-lg"></i>
                              </div>
                            </button>
                            
                            <!-- File Info (Clickable) -->
                            <button
                              @click="viewDraftFile(file)"
                              class="flex-1 min-w-0 text-left"
                            >
                              <p class="text-xs font-medium text-gray-900 truncate">{{ file.name }}</p>
                              <p class="text-xs text-gray-500 capitalize">{{ file.type }}</p>
                            </button>
                            
                            <!-- Remove Button -->
                            <button
                              @click.stop="confirmRemoveFile(file)"
                              class="w-6 h-6 flex items-center justify-center rounded hover:bg-red-100 transition-colors"
                            >
                              <i class="pi pi-times text-red-600 text-sm"></i>
                            </button>
                          </div>
                          
                          <!-- Show submitted files (not clickable) -->
                          <div
                            v-else-if="hasSubmittedWork && studentSubmissions.length > 0"
                            v-for="submission in studentSubmissions.slice(0, 1)"
                            :key="submission.activityId"
                            class="flex items-center gap-2 p-2 bg-gray-50 rounded-lg border border-gray-200"
                          >
                            <!-- Thumbnail (Not clickable - disabled) -->
                            <div
                              class="w-10 h-10 rounded-md flex items-center justify-center flex-shrink-0 overflow-hidden opacity-70"
                              :class="submission.isImage ? 'bg-gray-100' : 'bg-gray-100'"
                            >
                              <img
                                v-if="submission.isImage && submission.previewUrl"
                                :src="submission.previewUrl"
                                :alt="submission.caption || 'Submitted work'"
                                class="w-full h-full object-cover"
                                @error="(e) => { e.target.style.display = 'none'; e.target.nextElementSibling.style.display = 'flex'; }"
                              />
                              <div 
                                class="w-full h-full flex items-center justify-center"
                                :style="submission.isImage && submission.previewUrl ? 'display: none;' : ''"
                              >
                                <i v-if="submission.isImage" class="pi pi-image text-gray-500 text-lg"></i>
                                <i v-else class="pi pi-file text-gray-500 text-lg"></i>
                              </div>
                            </div>
                            
                            <!-- File Info (Not clickable) -->
                            <div class="flex-1 min-w-0">
                              <p class="text-xs font-medium text-gray-700 truncate">{{ submission.caption || 'Submitted work' }}</p>
                              <p class="text-xs text-gray-500">Submitted</p>
                            </div>
                            
                            <!-- Lock Icon (Submitted) -->
                            <div class="w-6 h-6 flex items-center justify-center">
                              <i class="pi pi-lock text-gray-400 text-sm"></i>
                            </div>
                          </div>
                        </div>
                        
                        <!-- Action Buttons (Always visible) -->
                        <div class="space-y-2">
                          <!-- Hidden File Input -->
                          <input
                            type="file"
                            ref="autoSaveFileInput"
                            @change="handleAutoSaveFileUpload"
                            accept="image/*,.pdf,.doc,.docx"
                            class="hidden"
                          />
                          
                          <!-- Add Button (Only show if not submitted) -->
                          <button
                            v-if="!hasSubmittedWork"
                            @click="showUploadDialog = true"
                            :disabled="isSubmitting"
                            class="w-full px-4 py-2 bg-white border-2 border-indigo-200 rounded-lg text-indigo-600 text-sm font-semibold hover:bg-indigo-50 hover:border-indigo-300 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            <i v-if="!isSubmitting" class="pi pi-plus"></i>
                            <i v-else class="pi pi-spin pi-spinner"></i>
                            <span>{{ isSubmitting ? 'Uploading...' : 'Add or create' }}</span>
                          </button>
                          
                          <!-- Turn In / Resubmit Button -->
                          <button
                            v-if="!hasSubmittedWork"
                            @click="showTurnInDialog = true"
                            :disabled="draftFiles.length === 0"
                            class="w-full px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg text-sm font-semibold hover:from-indigo-700 hover:to-purple-700 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            <i class="pi pi-check-circle"></i>
                            <span>Turn in</span>
                          </button>
                          
                          <!-- Resubmit Button (Show when already submitted) -->
                          <div v-else class="space-y-2">
                            <!-- Resubmit Counter Info -->
                            <div v-if="existingSubmission && existingSubmission.resubmit_count > 0" class="text-xs text-center">
                              <span class="px-2 py-1 bg-orange-100 text-orange-700 rounded-full">
                                Resubmitted {{ existingSubmission.resubmit_count }} time{{ existingSubmission.resubmit_count > 1 ? 's' : '' }}
                              </span>
                            </div>
                            
                            <button
                              @click="handleResubmit"
                              :disabled="hasScore"
                              class="w-full px-4 py-2 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg text-sm font-semibold hover:from-orange-600 hover:to-orange-700 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:from-orange-500 disabled:hover:to-orange-600"
                              :title="hasScore ? 'Cannot resubmit - Already scored' : 'Resubmit your work'"
                            >
                              <i class="pi pi-refresh"></i>
                              <span>{{ hasScore ? 'Already Scored' : 'Resubmit' }}</span>
                            </button>
                            
                            <!-- Post to Feed Button -->
                            <button
                              v-if="existingSubmission && !existingSubmission.post_to_feed"
                              @click="requestPostToFeed"
                              :disabled="hasScore || isRequestingPost"
                              class="w-full px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-lg text-sm font-semibold hover:from-blue-600 hover:to-indigo-700 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                              :title="hasScore ? 'Cannot post scored work' : 'Request to post this work to class feed'"
                            >
                              <i class="pi pi-send"></i>
                              <span>{{ isRequestingPost ? 'Requesting...' : 'Post to Feed' }}</span>
                            </button>
                            
                            <!-- Already Posted/Pending Status -->
                            <div v-else-if="existingSubmission && existingSubmission.post_to_feed" class="w-full px-4 py-2 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm font-medium flex items-center justify-center gap-2">
                              <i class="pi pi-check-circle"></i>
                              <span v-if="existingSubmission.approval_status === 'pending'">Post Request Pending</span>
                              <span v-else-if="existingSubmission.approval_status === 'approved'">Posted to Feed</span>
                              <span v-else>Post Request Sent</span>
                            </div>
                          </div>
                        </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Scoring Criteria Section (Centered) -->
                  <div class="mb-6 flex justify-center">
                    <div class="w-full max-w-md">
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
                  </div>


                  <!-- Student Submissions Section -->
                  <div class="mt-6 border-t border-indigo-100 pt-6" v-if="studentSubmissions.length > 0">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">Your Submissions:</h3>

                    <!-- Student Submission Cards -->
                    <div class="flex flex-wrap justify-center gap-4">
                      <div v-for="(submission, index) in studentSubmissions" :key="index"
                           class="bg-white rounded-lg border border-indigo-100 overflow-hidden hover:shadow-md transition-all w-full max-w-2xl mx-auto">
                        <div class="aspect-video relative bg-gray-50 overflow-hidden flex items-center justify-center p-2">
                          <!-- Image Display -->
                          <img v-if="submission.isImage && submission.previewUrl"
                            :src="submission.previewUrl"
                            :alt="submission.caption || 'Submitted work'"
                            class="w-full h-full object-cover rounded-lg"
                            @error="handleImageError(submission)"
                            v-show="!submission.loadError"
                          />
                          <!-- PDF Display -->
                          <div v-else-if="!submission.isImage && submission.previewUrl" class="flex flex-col items-center justify-center text-red-600">
                            <i class="pi pi-file-pdf text-6xl mb-3"></i>
                            <span class="text-sm font-medium">Document</span>
                            <span class="text-xs text-gray-500 mt-1">{{ submission.caption || 'Untitled' }}</span>
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
                            <div class="flex items-center gap-2">
                              <span class="text-xs text-gray-500">{{ submission.date }}</span>
                            </div>
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

                <!-- Submitted Collection View -->
                <div v-else-if="showSubmittedCollection" class="space-y-4">
                  <!-- Loading State -->
                  <div v-if="isLoadingCollection" class="flex justify-center items-center py-12">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600"></div>
                  </div>

                  <!-- Empty State -->
                  <div v-else-if="submittedCollection.length === 0" class="bg-white/80 backdrop-blur-sm rounded-xl shadow-sm p-12 text-center">
                    <i class="pi pi-inbox text-4xl text-gray-400 mb-4"></i>
                    <p class="text-gray-500">No submitted works yet.</p>
                  </div>

                  <!-- Collection Cards (Enhanced Row Layout) -->
                  <div v-else class="space-y-3">
                    <div
                      v-for="item in submittedCollection"
                      :key="item.id"
                      @click="openPreviewDialog(item)"
                      class="bg-white rounded-xl border-2 border-gray-200 hover:border-indigo-400 hover:shadow-md transition-all duration-200 cursor-pointer"
                    >
                      <div class="flex items-center gap-6 p-5">
                        <!-- Checkbox (Select Mode) -->
                        <div v-if="isSelectMode" class="flex items-center">
                          <input
                            type="checkbox"
                            :checked="selectedSubmissions.includes(item.id)"
                            @change="toggleSubmissionSelection(item.id)"
                            @click.stop
                            class="w-5 h-5 text-indigo-600 border-2 border-gray-300 rounded focus:ring-2 focus:ring-indigo-500 cursor-pointer"
                          />
                        </div>
                        
                        <!-- Thumbnail/Icon -->
                        <div class="flex-shrink-0 w-20 h-20 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl flex items-center justify-center overflow-hidden shadow-sm border border-indigo-100">
                          <img
                            v-if="item.file_path && (item.file_type === 'image' || item.file_path.startsWith('data:image'))"
                            :src="item.file_path"
                            :alt="item.activity_title"
                            class="w-full h-full object-cover"
                            @error="(e) => e.target.style.display = 'none'"
                          />
                          <i v-else-if="item.file_type === 'pdf'" class="pi pi-file-pdf text-3xl text-red-500"></i>
                          <i v-else class="pi pi-file text-3xl text-indigo-400"></i>
                        </div>

                        <!-- Content - Full Width Row Layout -->
                        <div class="flex-1 flex items-center justify-between">
                          <!-- Folder -->
                          <div class="flex-1 min-w-[120px]">
                            <div class="text-gray-500 text-xs mb-1 font-medium">Folder:</div>
                            <div class="flex items-center gap-2 text-gray-900 font-semibold">
                              <i class="pi pi-folder text-sm text-indigo-600"></i>
                              <span>{{ item.folder_name }}</span>
                            </div>
                          </div>
                          
                          <!-- Activity Type -->
                          <div class="flex-1 min-w-[140px]">
                            <div class="text-gray-500 text-xs mb-1 font-medium">Activity Type:</div>
                            <div class="text-gray-900 font-semibold capitalize">{{ item.activity_type }}</div>
                          </div>
                          
                          <!-- Activity Title -->
                          <div class="flex-1 min-w-[140px]">
                            <div class="text-gray-500 text-xs mb-1 font-medium">Activity Title:</div>
                            <div class="text-gray-900 font-bold">{{ item.activity_title }}</div>
                          </div>
                          
                          <!-- Submitted Date/Time -->
                          <div class="flex-1 min-w-[180px] text-right">
                            <div class="text-gray-500 text-xs mb-1 font-medium">Submitted:</div>
                            <div class="text-gray-900 font-semibold">{{ formatSubmittedDateTime(item.submitted_at) }}</div>
                          </div>
                        </div>

                        <!-- Score (if scored) -->
                        <div v-if="item.status === 'scored'" class="flex-shrink-0 text-center pl-6 border-l-2 border-gray-200 min-w-[80px]">
                          <div class="text-gray-500 text-xs mb-1 font-medium">Score:</div>
                          <div class="text-2xl font-bold text-indigo-600">{{ item.score }}</div>
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
                    <!-- Modern Table Design -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                      <!-- Table Header -->
                      <div class="bg-gray-50 border-b border-gray-200">
                        <div class="grid grid-cols-12 gap-4 px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider">
                          <div class="col-span-2">
                            <span>Activity Type</span>
                          </div>
                          <div class="col-span-2">
                            <span>Activity Title</span>
                          </div>
                          <div class="col-span-3">
                            <span>Instruction</span>
                          </div>
                          <div class="col-span-2 text-center">
                            <span>Status</span>
                          </div>
                          <div class="col-span-1 text-center">
                            <span>Due Time</span>
                          </div>
                          <div class="col-span-2 text-center">
                            <span>Due Date</span>
                          </div>
                        </div>
                      </div>

                      <!-- Table Body -->
                      <div class="divide-y divide-gray-200">
                        <div v-for="(activity, index) in folderActivities" :key="activity.id"
                          class="group hover:bg-gray-50 transition-colors duration-150 cursor-pointer"
                          @click="openActivity(activity)">
                          
                          <div class="grid grid-cols-12 gap-4 px-6 py-4 items-center">
                            <!-- Activity Type with Icon -->
                            <div class="col-span-2">
                              <div class="flex items-center gap-2">
                                <div :class="[
                                  'w-8 h-8 rounded-lg flex items-center justify-center',
                                  activity.type === 'project' ? 'bg-purple-100' : 
                                  activity.type === 'contest' ? 'bg-blue-100' : 
                                  activity.type === 'quiz' ? 'bg-green-100' : 'bg-gray-100'
                                ]">
                                  <span :class="[
                                    'text-lg font-bold',
                                    activity.type === 'project' ? 'text-purple-600' : 
                                    activity.type === 'contest' ? 'text-blue-600' : 
                                    activity.type === 'quiz' ? 'text-green-600' : 'text-gray-600'
                                  ]">{{ activity.type.charAt(0).toUpperCase() }}</span>
                                </div>
                                <span class="text-sm text-gray-700 capitalize">{{ activity.type }}</span>
                              </div>
                            </div>

                            <!-- Title -->
                            <div class="col-span-2">
                              <div class="font-medium text-gray-900">
                                {{ activity.title }}
                                <div class="text-xs text-gray-500">ID: {{ activity.id }}</div>
                              </div>
                            </div>

                            <!-- Instructions -->
                            <div class="col-span-3">
                              <div 
                                class="text-sm text-gray-600 line-clamp-2 leading-relaxed"
                                :title="activity.description"
                                style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; word-break: break-word;"
                              >
                                {{ activity.description || 'No instructions provided' }}
                              </div>
                            </div>

                            <!-- Status Badge -->
                            <div class="col-span-2 text-center">
                              <span v-if="getActivityStatus(activity) === 'submitted' && activity.isLate" 
                                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                                <i class="pi pi-circle-fill text-[6px] mr-1.5 text-orange-500"></i>
                                Submitted Late
                              </span>
                              <span v-else-if="getActivityStatus(activity) === 'submitted'" 
                                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                <i class="pi pi-circle-fill text-[6px] mr-1.5 text-green-500"></i>
                                Submitted
                              </span>
                              <span v-else-if="getActivityStatus(activity) === 'missing'" 
                                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                <i class="pi pi-circle-fill text-[6px] mr-1.5 text-red-500"></i>
                                Missing
                              </span>
                              <span v-else 
                                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                                <i class="pi pi-circle-fill text-[6px] mr-1.5 text-yellow-500"></i>
                                Pending
                              </span>
                            </div>

                            <!-- Due Time -->
                            <div class="col-span-1 text-center">
                              <span v-if="activity.formattedTime" class="text-sm text-gray-700">{{ activity.formattedTime }}</span>
                              <span v-else class="text-sm text-gray-400">--:--</span>
                            </div>

                            <!-- Due Date -->
                            <div class="col-span-2 text-center">
                              <div class="text-sm text-gray-700">
                                {{ activity.date ? new Date(activity.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'No date' }}
                                <div v-if="activity.daysLeft" class="text-xs text-gray-500">
                                  <span v-if="activity.daysLeft === 'Today'" class="text-orange-600 font-medium">Due today</span>
                                  <span v-else-if="activity.daysLeft.includes('ago')" class="text-red-600">{{ activity.daysLeft }}</span>
                                  <span v-else class="text-gray-500">{{ activity.daysLeft }}</span>
                                </div>
                              </div>
                            </div>
                          </div>
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
                  <h2 class="text-xl md:text-2xl font-bold text-gray-900">My Activities</h2>
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
                  <h3 class="text-lg font-medium text-gray-900 mb-2">No Activity Folders</h3>
                  <p class="text-gray-500">Your teacher hasn't created any activity folders yet.</p>
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

        <!-- Portfolio Compilation Tab Content -->
        <template v-if="activeTab === 'compilation'">
          <div class="min-h-screen transition-all duration-700 relative overflow-hidden"
               :style="isEnvelopeOpen && portfolioEnvelopeCreated ? { 
                 background: `
                   radial-gradient(circle at 20% 50%, ${adjustBrightness(envelopeDesign.color, 20)} 0%, transparent 50%),
                   radial-gradient(circle at 80% 80%, ${adjustBrightness(envelopeDesign.color, -10)} 0%, transparent 50%),
                   radial-gradient(circle at 40% 20%, ${adjustBrightness(envelopeDesign.color, 10)} 0%, transparent 50%),
                   linear-gradient(135deg, ${envelopeDesign.color} 0%, ${adjustBrightness(envelopeDesign.color, -30)} 100%)
                 `,
                 backgroundSize: '200% 200%',
                 animation: 'gradientShift 12s ease infinite'
               } : { background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)' }">
            
            <!-- Animated Background Elements -->
            <div class="absolute inset-0 pointer-events-none overflow-hidden">
              <!-- Mesh Gradient Overlay -->
              <div v-if="isEnvelopeOpen && portfolioEnvelopeCreated" 
                   class="absolute inset-0 opacity-30"
                   :style="{
                     background: `
                       radial-gradient(at 0% 0%, ${envelopeDesign.color}40 0px, transparent 50%),
                       radial-gradient(at 100% 0%, ${adjustBrightness(envelopeDesign.color, 20)}40 0px, transparent 50%),
                       radial-gradient(at 100% 100%, ${adjustBrightness(envelopeDesign.color, -20)}40 0px, transparent 50%),
                       radial-gradient(at 0% 100%, ${envelopeDesign.color}40 0px, transparent 50%)
                     `
                   }">
              </div>
              
              <!-- Animated Pattern Overlay -->
              <div v-if="isEnvelopeOpen && portfolioEnvelopeCreated && envelopeDesign.pattern === 'dots'" 
                   class="absolute inset-0 opacity-5 animate-patternFloat"
                   style="background-image: radial-gradient(circle, white 3px, transparent 3px); background-size: 40px 40px;">
              </div>
              <div v-else-if="isEnvelopeOpen && portfolioEnvelopeCreated && envelopeDesign.pattern === 'lines'" 
                   class="absolute inset-0 opacity-5 animate-patternSlide"
                   style="background-image: repeating-linear-gradient(45deg, white 0, white 3px, transparent 3px, transparent 20px);">
              </div>
              <div v-else-if="isEnvelopeOpen && portfolioEnvelopeCreated && envelopeDesign.pattern === 'grid'" 
                   class="absolute inset-0 opacity-5 animate-patternPulse"
                   style="background-image: linear-gradient(white 2px, transparent 2px), linear-gradient(90deg, white 2px, transparent 2px); background-size: 40px 40px;">
              </div>
              
              <!-- Large Floating Orbs -->
              <div v-if="isEnvelopeOpen && portfolioEnvelopeCreated">
                <div v-for="i in 12" :key="`orb-${i}`"
                     class="absolute rounded-full blur-3xl opacity-20 animate-float"
                     :style="{
                       width: `${150 + Math.random() * 300}px`,
                       height: `${150 + Math.random() * 300}px`,
                       background: `radial-gradient(circle, ${adjustBrightness(envelopeDesign.color, 40)} 0%, transparent 70%)`,
                       left: `${Math.random() * 100}%`,
                       top: `${Math.random() * 100}%`,
                       animationDelay: `${Math.random() * 5}s`,
                       animationDuration: `${15 + Math.random() * 20}s`
                     }">
                </div>
              </div>
              
              <!-- Sparkle Effects -->
              <div v-if="isEnvelopeOpen && portfolioEnvelopeCreated">
                <div v-for="i in 30" :key="`sparkle-${i}`"
                     class="absolute bg-white rounded-full animate-sparkle"
                     :style="{
                       width: `${1 + Math.random() * 2}px`,
                       height: `${1 + Math.random() * 2}px`,
                       left: `${Math.random() * 100}%`,
                       top: `${Math.random() * 100}%`,
                       animationDelay: `${Math.random() * 3}s`,
                       animationDuration: `${2 + Math.random() * 4}s`,
                       boxShadow: '0 0 4px rgba(255, 255, 255, 0.8)'
                     }">
                </div>
              </div>
              
              <!-- Ambient Light Rays -->
              <div v-if="isEnvelopeOpen && portfolioEnvelopeCreated" class="absolute inset-0">
                <div v-for="i in 5" :key="`ray-${i}`"
                     class="absolute h-full opacity-10 animate-float"
                     :style="{
                       width: '2px',
                       background: `linear-gradient(to bottom, transparent, ${envelopeDesign.color}, transparent)`,
                       left: `${i * 20}%`,
                       animationDelay: `${i * 0.5}s`,
                       animationDuration: `${8 + i * 2}s`,
                       transform: 'rotate(15deg)'
                     }">
                </div>
              </div>
            </div>
            
            <!-- Content Area with Padding -->
            <div class="relative z-10 p-4 md:p-6">
            
            <!-- Show designed portfolio envelope if created -->
            <div v-if="portfolioEnvelopeCreated" class="max-w-3xl mx-auto relative z-10">
              <!-- Portfolio Envelope Display - Hide when opened -->
              <div 
                v-if="!isEnvelopeOpen"
                @click="toggleEnvelope"
                class="bg-white rounded-2xl shadow-xl overflow-hidden mb-6 cursor-pointer transform transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl"
              >
                <!-- Envelope Preview -->
                <div class="relative w-full aspect-[21/9]"
                     :style="{ backgroundColor: envelopeDesign.color }">
                  
                  <!-- Pattern Overlay -->
                  <div v-if="envelopeDesign.pattern === 'dots'" 
                       class="absolute inset-0 opacity-20"
                       style="background-image: radial-gradient(circle, white 2px, transparent 2px); background-size: 20px 20px;">
                  </div>
                  <div v-else-if="envelopeDesign.pattern === 'lines'" 
                       class="absolute inset-0 opacity-20"
                       style="background-image: repeating-linear-gradient(45deg, white 0, white 2px, transparent 2px, transparent 10px);">
                  </div>
                  <div v-else-if="envelopeDesign.pattern === 'grid'" 
                       class="absolute inset-0 opacity-20"
                       style="background-image: linear-gradient(white 1px, transparent 1px), linear-gradient(90deg, white 1px, transparent 1px); background-size: 20px 20px;">
                  </div>

                  <!-- Envelope Flap with Animation -->
                  <div 
                    class="absolute top-0 left-0 right-0 h-1/4 border-b-4 border-white/30 transition-all duration-700 ease-out origin-top"
                    :class="{ 
                      'rotate-x-180 -translate-y-full opacity-0': isEnvelopeOpen,
                      'rotate-x-0 translate-y-0 opacity-100': !isEnvelopeOpen
                    }"
                    :style="{ 
                      background: `linear-gradient(180deg, ${envelopeDesign.color} 0%, ${adjustBrightness(envelopeDesign.color, -20)} 100%)`,
                      transformStyle: 'preserve-3d',
                      perspective: '1000px'
                    }">
                      <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-0 h-0 
                                  border-l-[150px] border-r-[150px] border-t-[80px] border-l-transparent border-r-transparent transition-all duration-700"
                           :style="{ borderTopColor: adjustBrightness(envelopeDesign.color, -20) }">
                      </div>
                  </div>

                  <!-- Content Area with Slide-Up Animation -->
                  <div class="absolute inset-0 flex flex-col items-center justify-center p-4 text-center">
                      <div 
                        class="bg-white/20 backdrop-blur-md rounded-2xl p-6 shadow-xl border border-white/30 max-w-sm w-full transition-all duration-700 ease-out"
                        :class="{
                          'translate-y-0 opacity-100 scale-100': isEnvelopeOpen,
                          'translate-y-8 opacity-70 scale-95': !isEnvelopeOpen
                        }"
                      >
                          <h1 class="text-2xl font-bold text-white mb-2 transition-all duration-500" 
                              :class="{ 'scale-110': isEnvelopeOpen }"
                              style="text-shadow: 0 2px 8px rgba(0,0,0,0.3)">
                              {{ envelopeDesign.title }}
                          </h1>
                          <p class="text-base text-white/90 font-medium mb-1 transition-all duration-500 delay-100" 
                             :class="{ 'opacity-100': isEnvelopeOpen, 'opacity-80': !isEnvelopeOpen }"
                             style="text-shadow: 0 1px 4px rgba(0,0,0,0.2)">
                              {{ envelopeDesign.studentName }}
                          </p>
                          <p class="text-sm text-white/80 transition-all duration-500 delay-200" 
                             :class="{ 'opacity-100': isEnvelopeOpen, 'opacity-70': !isEnvelopeOpen }"
                             style="text-shadow: 0 1px 4px rgba(0,0,0,0.2)">
                              {{ envelopeDesign.className }}
                          </p>
                          
                          <!-- Open Indicator - Only show when closed -->
                          <div v-if="!isEnvelopeOpen" class="mt-4 text-white/60 text-xs animate-pulse">
                            <i class="pi pi-hand-pointer mr-1"></i>
                            Click to open
                          </div>
                      </div>
                  </div>
                </div>
              </div>

              <!-- Activities Carousel - Show when envelope is opened -->
              <div v-if="isEnvelopeOpen && portfolioActivities.length > 0" class="relative animate-fadeIn">
                <!-- Portfolio Tabs with Back Button -->
                <div class="flex justify-between items-center mb-6 animate-slideDown">
                  <!-- Tabs on the left -->
                  <div class="flex gap-2">
                    <button
                      @click="activePortfolioTab = 'all'"
                      class="flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all duration-200"
                      :class="activePortfolioTab === 'all' 
                        ? 'bg-indigo-600 text-white shadow-lg' 
                        : 'bg-white text-gray-700 hover:bg-gray-50 border-2 border-gray-200'"
                    >
                      <i class="pi pi-list"></i>
                      Activity Compilation
                      <span class="px-2 py-0.5 rounded-full text-xs font-semibold"
                            :class="activePortfolioTab === 'all' ? 'bg-white/20' : 'bg-gray-200'">
                        {{ portfolioActivities.length }}
                      </span>
                    </button>
                    <button
                      @click="activePortfolioTab = 'missing'"
                      class="flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all duration-200"
                      :class="activePortfolioTab === 'missing' 
                        ? 'bg-orange-600 text-white shadow-lg' 
                        : 'bg-white text-gray-700 hover:bg-gray-50 border-2 border-gray-200'"
                    >
                      <i class="pi pi-exclamation-triangle"></i>
                      Missing Activity Compilation
                      <span class="px-2 py-0.5 rounded-full text-xs font-semibold"
                            :class="activePortfolioTab === 'missing' ? 'bg-white/20' : 'bg-orange-100 text-orange-800'">
                        {{ missingActivities.length }}
                      </span>
                    </button>
                  </div>

                  <!-- Back Button on the right -->
                  <button
                    @click="isEnvelopeOpen = false"
                    class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-lg border-2 border-gray-300 hover:border-indigo-500 hover:text-indigo-600 hover:bg-indigo-50 transition-all duration-200 shadow-md hover:shadow-lg flex items-center gap-2"
                  >
                    <i class="pi pi-arrow-left text-sm"></i>
                    Back to Envelope
                  </button>
                </div>

                <!-- All Activities Tab Content -->
                <div v-if="activePortfolioTab === 'all'" 
                     class="rounded-2xl shadow-xl overflow-hidden min-h-[600px] relative animate-scaleIn"
                     :style="{ 
                       background: `linear-gradient(135deg, ${envelopeDesign.color} 0%, ${adjustBrightness(envelopeDesign.color, -20)} 100%)`,
                       animation: 'gradientShift 8s ease infinite'
                     }">
                  
                  <!-- Animated Pattern Overlay (matching envelope) -->
                  <div v-if="envelopeDesign.pattern === 'dots'" 
                       class="absolute inset-0 opacity-10 pointer-events-none animate-patternFloat"
                       style="background-image: radial-gradient(circle, white 2px, transparent 2px); background-size: 20px 20px;">
                  </div>
                  <div v-else-if="envelopeDesign.pattern === 'lines'" 
                       class="absolute inset-0 opacity-10 pointer-events-none animate-patternSlide"
                       style="background-image: repeating-linear-gradient(45deg, white 0, white 2px, transparent 2px, transparent 10px);">
                  </div>
                  <div v-else-if="envelopeDesign.pattern === 'grid'" 
                       class="absolute inset-0 opacity-10 pointer-events-none animate-patternPulse"
                       style="background-image: linear-gradient(white 1px, transparent 1px), linear-gradient(90deg, white 1px, transparent 1px); background-size: 20px 20px;">
                  </div>

                  <!-- Floating Particles Effect -->
                  <div class="absolute inset-0 pointer-events-none overflow-hidden">
                    <div v-for="i in 15" :key="i" 
                         class="absolute w-2 h-2 bg-white/20 rounded-full animate-float"
                         :style="{
                           left: `${Math.random() * 100}%`,
                           top: `${Math.random() * 100}%`,
                           animationDelay: `${Math.random() * 5}s`,
                           animationDuration: `${5 + Math.random() * 10}s`
                         }">
                    </div>
                  </div>

                  <!-- Activity Display -->
                  <div class="relative p-8 z-10">
                    <!-- Activity Counter with Pulse Animation -->
                    <div class="absolute top-4 right-4 z-10 text-white px-5 py-2.5 rounded-full text-sm font-bold shadow-2xl animate-pulse-slow transform transition-all duration-300 hover:scale-110"
                         :style="{ 
                           backgroundColor: adjustBrightness(envelopeDesign.color, -30),
                           boxShadow: `0 0 20px ${envelopeDesign.color}80, 0 0 40px ${envelopeDesign.color}40`
                         }">
                      <span class="relative z-10">{{ currentActivityIndex + 1 }} / {{ portfolioActivities.length }}</span>
                      <div class="absolute inset-0 rounded-full animate-ping opacity-20"
                           :style="{ backgroundColor: envelopeDesign.color }">
                      </div>
                    </div>

                    <!-- Activity Content -->
                    <div v-if="portfolioActivities[currentActivityIndex]" 
                         :key="currentActivityIndex">
                      <!-- Content Card with Glass Effect -->
                      <div class="bg-white/95 backdrop-blur-sm rounded-2xl p-6 shadow-2xl relative transform transition-all duration-500 hover:shadow-3xl hover:scale-[1.01]">
                      <!-- Activity Image/Preview -->
                      <div class="aspect-video bg-gradient-to-br from-white/50 to-white/30 rounded-xl mb-6 flex items-center justify-center overflow-hidden relative border-2 border-white/50 shadow-lg transform transition-all duration-300 hover:shadow-2xl"
                           :style="{ borderColor: `${envelopeDesign.color}40` }">
                        <img v-if="portfolioActivities[currentActivityIndex].submission_file && portfolioActivities[currentActivityIndex].submission_status === 'submitted'" 
                             :src="portfolioActivities[currentActivityIndex].submission_file"
                             alt="Activity submission"
                             class="w-full h-full object-contain"
                             @error="(e) => { console.error('Image load error:', portfolioActivities[currentActivityIndex].submission_file); e.target.style.display = 'none'; }"
                        />
                        <div v-else class="text-center flex flex-col items-center">
                          <i class="pi pi-file text-6xl text-indigo-300 mb-4"></i>
                          <p class="text-indigo-600 font-medium">
                            {{ portfolioActivities[currentActivityIndex].submission_status === 'missing' ? 'No Submission' : 'No File Available' }}
                          </p>
                        </div>
                      </div>

                      <!-- Submission Caption -->
                      <div v-if="portfolioActivities[currentActivityIndex].submission_caption" class="mb-4 p-4 bg-gray-50 rounded-lg">
                        <p class="text-sm text-gray-700 italic">
                          "{{ portfolioActivities[currentActivityIndex].submission_caption }}"
                        </p>
                      </div>

                      <!-- Score and Feedback -->
                      <div v-if="portfolioActivities[currentActivityIndex].submission_score !== null && portfolioActivities[currentActivityIndex].submission_score !== undefined" 
                           class="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                        <div class="flex items-center justify-between mb-2">
                          <span class="text-sm font-medium text-gray-700">Score:</span>
                          <span class="text-2xl font-bold text-green-700">{{ portfolioActivities[currentActivityIndex].submission_score }}</span>
                        </div>
                        <div v-if="portfolioActivities[currentActivityIndex].submission_feedback" class="mt-2 pt-2 border-t border-green-200">
                          <p class="text-sm text-gray-600">
                            <span class="font-medium">Feedback:</span> {{ portfolioActivities[currentActivityIndex].submission_feedback }}
                          </p>
                        </div>
                      </div>

                      <!-- Activity Details -->
                      <div class="space-y-4">
                        <div>
                          <div class="flex items-center gap-3 mb-3">
                            <span class="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-xs font-semibold uppercase">
                              {{ portfolioActivities[currentActivityIndex].activity_type || 'Activity' }}
                            </span>
                            <span class="text-sm text-gray-500">
                              {{ portfolioActivities[currentActivityIndex].folder_name }}
                            </span>
                          </div>
                          <h3 class="text-2xl font-bold text-gray-900 mb-2">
                            {{ portfolioActivities[currentActivityIndex].title }}
                          </h3>
                          <p class="text-gray-600">
                            {{ portfolioActivities[currentActivityIndex].description }}
                          </p>
                        </div>

                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-gray-200">
                          <div>
                            <span class="text-sm text-gray-500 block mb-1">Status:</span>
                            <span class="px-3 py-1 rounded-full text-sm font-medium inline-block"
                                  :class="portfolioActivities[currentActivityIndex].submission_status === 'submitted' 
                                    ? 'bg-green-100 text-green-800' 
                                    : 'bg-red-100 text-red-800'">
                              {{ portfolioActivities[currentActivityIndex].submission_status === 'submitted' ? 'Submitted' : 'Missing' }}
                            </span>
                          </div>
                          <div v-if="portfolioActivities[currentActivityIndex].submission_date">
                            <span class="text-sm text-gray-500 block mb-1">Submitted:</span>
                            <span class="text-sm font-medium text-gray-900">
                              {{ new Date(portfolioActivities[currentActivityIndex].submission_date).toLocaleDateString() }}
                            </span>
                          </div>
                          <div v-if="portfolioActivities[currentActivityIndex].due_date">
                            <span class="text-sm text-gray-500 block mb-1">Due Date:</span>
                            <span class="text-sm font-medium text-gray-900">
                              {{ new Date(portfolioActivities[currentActivityIndex].due_date).toLocaleDateString() }}
                            </span>
                          </div>
                          <div v-if="portfolioActivities[currentActivityIndex].due_time">
                            <span class="text-sm text-gray-500 block mb-1">Due Time:</span>
                            <span class="text-sm font-medium text-gray-900">
                              {{ portfolioActivities[currentActivityIndex].due_time }}
                            </span>
                          </div>
                        </div>
                      </div>
                      </div>
                      <!-- Close Content Card -->
                      
                      <!-- Navigation Arrows - Centered with image, inside card -->
                      <button
                        @click="previousActivity"
                        :disabled="currentActivityIndex === 0"
                        class="absolute left-2 top-[200px] w-16 h-16 bg-white/95 backdrop-blur-md rounded-full shadow-2xl flex items-center justify-center hover:bg-white hover:scale-125 transition-all duration-300 disabled:opacity-20 disabled:cursor-not-allowed z-30 group"
                        :style="{ 
                          borderColor: envelopeDesign.color, 
                          borderWidth: '3px',
                          boxShadow: `0 8px 32px ${envelopeDesign.color}40, 0 0 0 0 ${envelopeDesign.color}20`
                        }"
                      >
                        <i class="pi pi-chevron-left text-2xl transition-all duration-300 group-hover:scale-110" 
                           :style="{ color: envelopeDesign.color }"></i>
                        <div class="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                             :style="{ 
                               background: `radial-gradient(circle, ${envelopeDesign.color}20 0%, transparent 70%)`,
                               animation: 'pulse 2s infinite'
                             }">
                        </div>
                      </button>
                      <button
                        @click="nextActivity"
                        :disabled="currentActivityIndex >= portfolioActivities.length - 1"
                        class="absolute right-2 top-[200px] w-16 h-16 bg-white/95 backdrop-blur-md rounded-full shadow-2xl flex items-center justify-center hover:bg-white hover:scale-125 transition-all duration-300 disabled:opacity-20 disabled:cursor-not-allowed z-30 group"
                        :style="{ 
                          borderColor: envelopeDesign.color, 
                          borderWidth: '3px',
                          boxShadow: `0 8px 32px ${envelopeDesign.color}40, 0 0 0 0 ${envelopeDesign.color}20`
                        }"
                      >
                        <i class="pi pi-chevron-right text-2xl transition-all duration-300 group-hover:scale-110" 
                           :style="{ color: envelopeDesign.color }"></i>
                        <div class="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                             :style="{ 
                               background: `radial-gradient(circle, ${envelopeDesign.color}20 0%, transparent 70%)`,
                               animation: 'pulse 2s infinite'
                             }">
                        </div>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Activity Compilation Tab Content -->
                <div v-if="activePortfolioTab === 'missing'" class="bg-white rounded-2xl shadow-xl overflow-hidden p-8">
                  <div v-if="missingActivities.length > 0">
                    <h3 class="text-2xl font-bold text-gray-900 mb-6">Missing Activities to Compile</h3>
                    
                    <!-- Missing Activities List -->
                    <div class="space-y-4">
                      <div v-for="activity in missingActivities" :key="activity.id"
                           class="bg-gradient-to-r from-orange-50 to-red-50 border-2 border-orange-200 rounded-xl p-6 hover:shadow-lg transition-all">
                        <div class="flex items-start justify-between">
                          <div class="flex-1">
                            <div class="flex items-center gap-3 mb-3">
                              <span class="px-3 py-1 bg-red-100 text-red-800 rounded-full text-xs font-semibold">
                                Missing
                              </span>
                              <span class="text-sm text-gray-500">
                                {{ activity.folder_name }}
                              </span>
                            </div>
                            <h4 class="text-xl font-bold text-gray-900 mb-2">{{ activity.title }}</h4>
                            <p class="text-gray-600 mb-4">{{ activity.description }}</p>
                            <div class="flex items-center gap-4 text-sm text-gray-500">
                              <span v-if="activity.due_date">
                                <i class="pi pi-calendar mr-1"></i>
                                Due: {{ new Date(activity.due_date).toLocaleDateString() }}
                              </span>
                              <span v-if="activity.due_time">
                                <i class="pi pi-clock mr-1"></i>
                                {{ activity.due_time }}
                              </span>
                              <span class="capitalize">
                                <i class="pi pi-tag mr-1"></i>
                                {{ activity.activity_type }}
                              </span>
                            </div>
                          </div>
                          <button
                            @click="compileActivity(activity)"
                            class="ml-4 px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl flex items-center gap-2"
                          >
                            <i class="pi pi-plus"></i>
                            Compile Now
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Empty State -->
                  <div v-else class="text-center py-12">
                    <i class="pi pi-check-circle text-6xl text-green-500 mb-4"></i>
                    <h3 class="text-2xl font-bold text-gray-900 mb-2">All Activities Completed!</h3>
                    <p class="text-gray-600">You have submitted all activities. Great job!</p>
                  </div>
                </div>
              </div>

              <!-- Action Buttons - Only show when envelope is closed -->
              <div v-if="!isEnvelopeOpen" class="flex flex-col sm:flex-row gap-4 justify-center items-center mt-6">
                <button
                  @click="editEnvelopeDesign"
                  class="w-full sm:w-auto px-8 py-3.5 bg-white text-gray-700 font-semibold rounded-xl border-2 border-gray-300 hover:border-indigo-500 hover:text-indigo-600 hover:bg-indigo-50 transition-all duration-200 flex items-center justify-center gap-3 shadow-md hover:shadow-lg"
                >
                  <i class="pi pi-pencil text-lg"></i>
                  <span>Edit Design</span>
                </button>
                <button
                  @click="showSubmitPortfolioDialog = true"
                  :disabled="portfolioEnvelope?.is_submitted"
                  class="w-full sm:w-auto px-8 py-3.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl hover:from-indigo-700 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl flex items-center justify-center gap-3 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                >
                  <i class="pi pi-send text-lg"></i>
                  <span>{{ portfolioEnvelope?.is_submitted ? 'Already Submitted' : 'Submit Portfolio' }}</span>
                </button>
              </div>
            </div>

            <!-- Show message only if teacher requested compilation but envelope not created -->
            <div v-else-if="portfolioCompilationRequested" class="flex items-center justify-center min-h-[60vh]">
              <div class="max-w-2xl w-full bg-white rounded-xl shadow-lg p-8 md:p-12 text-center">
                <!-- Icon -->
                <div class="mx-auto flex items-center justify-center h-20 w-20 rounded-full bg-indigo-100 mb-6">
                  <i class="pi pi-book text-indigo-600 text-4xl"></i>
                </div>
                
                <!-- Title -->
                <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
                  Portfolio Compilation Ready
                </h2>
                
                <!-- Message -->
                <p class="text-gray-600 text-lg mb-8">
                  Your teacher has requested you to start compiling your portfolio. 
                  Click the button below to begin organizing your work and achievements.
                </p>
                
                <!-- Start Button -->
                <button
                  @click="startPortfolioCompilation"
                  class="px-8 py-4 bg-indigo-600 text-white text-lg font-semibold rounded-lg hover:bg-indigo-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1 inline-flex items-center gap-3"
                >
                  <i class="pi pi-play-circle text-xl"></i>
                  Start Portfolio Compilation
                </button>
                
                <!-- Additional Info -->
                <p class="text-sm text-gray-500 mt-6">
                  Make sure to review all your activities before compiling your portfolio.
                </p>
              </div>
            </div>
            
            <!-- Show waiting state if teacher hasn't requested compilation yet -->
            <div v-else class="flex items-center justify-center min-h-[60vh]">
              <div class="max-w-2xl w-full bg-white rounded-xl shadow-lg p-8 md:p-12 text-center">
                <!-- Icon -->
                <div class="mx-auto flex items-center justify-center h-20 w-20 rounded-full bg-gray-100 mb-6">
                  <i class="pi pi-clock text-gray-400 text-4xl"></i>
                </div>
                
                <!-- Title -->
                <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
                  Waiting for Teacher
                </h2>
                
                <!-- Message -->
                <p class="text-gray-600 text-lg mb-4">
                  Your teacher hasn't requested portfolio compilation yet.
                </p>
                <p class="text-gray-500 text-base">
                  You'll be notified when it's time to start compiling your portfolio.
                </p>
              </div>
            </div>
            </div>
            <!-- Close Content Area -->
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
            @click="isCompilingMissing ? submitMissingActivity() : submitNewProduct()"
            class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
            :disabled="!selectedFile || isSubmitting"
            :class="{'opacity-50 cursor-not-allowed': !selectedFile || isSubmitting}"
          >
            <i v-if="!isSubmitting" class="pi pi-check"></i>
            <i v-else class="pi pi-spin pi-spinner"></i>
            {{ isSubmitting ? 'Submitting...' : (isCompilingMissing ? 'Compile Activity' : 'Submit Work') }}
          </button>
        </div>
      </template>
    </Dialog>

    <!-- Missing Activities Dialog -->
    <Dialog v-model:visible="showMissingActivitiesDialog"
        modal
        header="Missing Activities"
        :style="{ width: '95%', maxWidth: '50rem' }">
        <div class="p-6">
            <div class="mb-6">
                <p class="text-gray-600 mb-4">
                    The following activities are missing submissions. You can compile them now to complete your portfolio.
                </p>
            </div>

            <!-- Missing Activities List -->
            <div class="space-y-3 max-h-96 overflow-y-auto">
                <div v-for="activity in missingActivities" :key="activity.id"
                     class="bg-red-50 border border-red-200 rounded-lg p-4 hover:bg-red-100 transition-colors">
                    <div class="flex items-start justify-between">
                        <div class="flex-1">
                            <h4 class="font-semibold text-gray-900 mb-1">{{ activity.title }}</h4>
                            <p class="text-sm text-gray-600 mb-2">{{ activity.description }}</p>
                            <div class="flex items-center gap-4 text-xs text-gray-500">
                                <span v-if="activity.due_date">
                                    <i class="pi pi-calendar mr-1"></i>
                                    Due: {{ new Date(activity.due_date).toLocaleDateString() }}
                                </span>
                                <span class="px-2 py-1 bg-red-100 text-red-800 rounded-full font-medium">
                                    Missing
                                </span>
                            </div>
                        </div>
                        <button
                            @click="compileActivity(activity)"
                            class="ml-4 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
                        >
                            <i class="pi pi-plus"></i>
                            Compile
                        </button>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-if="missingActivities.length === 0" class="text-center py-8">
                <i class="pi pi-check-circle text-4xl text-green-500 mb-3"></i>
                <p class="text-gray-600">All activities have been submitted!</p>
            </div>

            <!-- Close Button -->
            <div class="mt-6 flex justify-end">
                <button
                    @click="showMissingActivitiesDialog = false"
                    class="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                >
                    Close
                </button>
            </div>
        </div>
    </Dialog>

    <!-- Envelope Confirmation Dialog -->
    <Dialog v-model:visible="showEnvelopeConfirmDialog"
        modal
        header="Confirm Portfolio Envelope"
        :style="{ width: '90%', maxWidth: '30rem' }">
        <div class="p-6">
            <div class="mb-6 text-center">
                <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 mb-4">
                    <i class="pi pi-check-circle text-indigo-600 text-xl"></i>
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-2">Create Portfolio Envelope?</h3>
                <p class="text-sm text-gray-500">
                    Are you sure you want to create this portfolio envelope? Your teacher will be notified.
                </p>
            </div>
            <div class="flex justify-end gap-3">
                <button @click="showEnvelopeConfirmDialog = false"
                    class="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg">
                    Cancel
                </button>
                <button @click="confirmSaveEnvelope"
                    class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg flex items-center gap-2">
                    <i class="pi pi-check"></i>
                    Confirm
                </button>
            </div>
        </div>
    </Dialog>

    <!-- Remove from Collection Confirmation Dialog -->
    <Dialog v-model:visible="showDeleteConfirmDialog" modal :style="{ width: '90vw', maxWidth: '500px' }" :dismissableMask="true">
      <template #header>
        <div class="flex items-center gap-3">
          <i class="pi pi-eye-slash text-orange-600 text-xl"></i>
          <h3 class="text-lg font-bold text-gray-800">Remove from Collection</h3>
        </div>
      </template>

      <div class="py-4">
        <p class="text-gray-700 mb-4">
          <span v-if="deleteAction === 'all'">
            Remove all {{ submittedCollection.length }} submission(s) from your collection?
          </span>
          <span v-else>
            Remove {{ selectedSubmissions.length }} submission(s) from your collection?
          </span>
        </p>
        <p class="text-sm text-indigo-600 font-medium bg-indigo-50 p-3 rounded-lg">
          <i class="pi pi-info-circle mr-2"></i>
          Note: This will only hide them from this view. Your submissions will still be visible to your teacher and remain in the activity.
        </p>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3">
          <button
            @click="showDeleteConfirmDialog = false"
            class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors duration-200"
          >
            Cancel
          </button>
          <button
            @click="deleteSelectedSubmissions"
            class="px-5 py-2.5 text-sm font-medium text-white bg-orange-600 rounded-lg hover:bg-orange-700 transition-colors duration-200 flex items-center gap-2"
          >
            <i class="pi pi-eye-slash"></i>
            <span>Remove from Collection</span>
          </button>
        </div>
      </template>
    </Dialog>

    <!-- Post Output Dialog -->
    <Dialog v-model:visible="showPostOutputDialog" modal :style="{ width: '90vw', maxWidth: '600px' }" :dismissableMask="true">
      <template #header>
        <div class="flex items-center gap-3">
          <i class="pi pi-send text-green-600 text-xl"></i>
          <h3 class="text-lg font-bold text-gray-800">Post Output to Feed</h3>
        </div>
      </template>

      <div v-if="existingSubmission" class="space-y-4">
        <!-- Caption Input -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Caption</label>
          <textarea
            v-model="postOutputCaption"
            rows="3"
            placeholder="Add a caption to your work..."
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none"
          ></textarea>
        </div>

        <!-- Output Preview -->
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Your Output</label>
          <div class="bg-gray-50 rounded-lg p-4 border border-gray-200 flex items-center justify-center" style="min-height: 250px;">
            <img
              v-if="getSubmissionImageUrl()"
              :src="getSubmissionImageUrl()"
              :alt="selectedActivity?.title || 'Submission'"
              class="max-w-full max-h-[300px] object-contain rounded-lg shadow-sm"
              @error="(e) => { console.error('Image load error:', e.target.src); e.target.style.display = 'none'; }"
            />
            <div v-else class="text-center py-8">
              <i class="pi pi-file text-4xl text-gray-400 mb-2"></i>
              <p class="text-gray-600 text-sm">{{ existingSubmission?.file_type || 'File' }}</p>
              <p class="text-xs text-gray-500 mt-2">No preview available</p>
            </div>
          </div>
        </div>

        <!-- Include Score Checkbox (Only if scored) -->
        <div v-if="hasScore" class="flex items-start gap-3 bg-indigo-50 rounded-lg p-4 border border-indigo-200">
          <input
            type="checkbox"
            id="includeScore"
            v-model="includeScore"
            class="w-5 h-5 text-green-600 border-2 border-gray-300 rounded focus:ring-2 focus:ring-green-500 cursor-pointer mt-0.5"
          />
          <label for="includeScore" class="flex-1 cursor-pointer">
            <div class="font-semibold text-gray-900">Include overall score</div>
            <div class="text-sm text-gray-600 mt-1">
              Your score ({{ existingSubmission.score }} points) will be visible to your classmates
            </div>
          </label>
        </div>

        <!-- Info Message -->
        <div class="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
          <div class="flex items-start gap-3">
            <i class="pi pi-info-circle text-yellow-600 text-lg mt-0.5"></i>
            <div class="flex-1">
              <p class="text-sm text-gray-700">
                Your teacher will review and approve your post before it appears in the class feed.
              </p>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3">
          <button
            @click="closePostOutputDialog"
            :disabled="isPostingOutput"
            class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors duration-200 disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            @click="submitPostOutput"
            :disabled="isPostingOutput || !postOutputCaption.trim()"
            class="px-5 py-2.5 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <i class="pi pi-send"></i>
            <span>{{ isPostingOutput ? 'Sending...' : 'Send Request' }}</span>
          </button>
        </div>
      </template>
    </Dialog>

    <!-- Preview Collection Dialog -->
    <Dialog v-model:visible="showPreviewDialog" modal :style="{ width: '90vw', maxWidth: '900px' }" :dismissableMask="true">
      <template #header>
        <div class="flex items-center gap-3">
          <i class="pi pi-eye text-indigo-600 text-xl"></i>
          <h3 class="text-lg font-bold text-gray-800">Preview Submission</h3>
        </div>
      </template>

      <div v-if="selectedPreviewItem" class="space-y-4">
        <!-- Submission Image/File -->
        <div class="bg-gray-50 rounded-lg p-4 flex items-center justify-center" style="min-height: 250px;">
          <!-- Image Preview -->
          <img
            v-if="selectedPreviewItem.file_path && (selectedPreviewItem.file_type === 'image' || selectedPreviewItem.file_path.startsWith('data:image'))"
            :src="selectedPreviewItem.file_path"
            :alt="selectedPreviewItem.activity_title"
            class="max-w-full max-h-[300px] object-contain rounded-lg shadow-md"
            @error="handlePreviewImageError"
          />
          
          <!-- PDF Preview -->
          <div v-else-if="selectedPreviewItem.file_path && (selectedPreviewItem.file_type === 'pdf' || selectedPreviewItem.file_path.startsWith('data:application/pdf'))" class="w-full">
            <iframe
              :src="selectedPreviewItem.file_path"
              class="w-full h-[400px] rounded-lg border-2 border-gray-300"
              frameborder="0"
            ></iframe>
            <div class="mt-3 text-center">
              <a
                :href="selectedPreviewItem.file_path"
                target="_blank"
                download="document.pdf"
                class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                <i class="pi pi-download"></i>
                <span>Download PDF</span>
              </a>
            </div>
          </div>
          
          <!-- Document/Other File Types -->
          <div v-else-if="selectedPreviewItem.file_path && selectedPreviewItem.file_path.startsWith('data:')" class="text-center">
            <div class="mb-4">
              <i v-if="selectedPreviewItem.file_type === 'document'" class="pi pi-file-word text-6xl text-blue-500"></i>
              <i v-else class="pi pi-file text-6xl text-gray-500"></i>
            </div>
            <p class="text-gray-700 font-semibold mb-2">{{ selectedPreviewItem.file_type === 'document' ? 'Document' : 'File' }} Uploaded</p>
            <p class="text-sm text-gray-500 mb-4">Type: {{ selectedPreviewItem.file_type || 'Unknown' }}</p>
            
            <!-- Download button for base64 files -->
            <a
              :href="selectedPreviewItem.file_path"
              :download="`${selectedPreviewItem.activity_title || 'file'}.${getFileExtension(selectedPreviewItem.file_path)}`"
              class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              <i class="pi pi-download"></i>
              <span>Download File</span>
            </a>
            
            <div v-if="selectedPreviewItem.caption" class="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <p class="text-xs text-blue-700 font-semibold mb-1">Caption:</p>
              <p class="text-sm text-gray-700">{{ selectedPreviewItem.caption }}</p>
            </div>
          </div>
          
          <!-- No File Available -->
          <div v-else class="text-center">
            <i class="pi pi-file text-4xl text-gray-400 mb-3"></i>
            <p class="text-gray-600 font-semibold">File not available</p>
            <p class="text-sm text-gray-500 mt-2">Type: {{ selectedPreviewItem.file_type || 'Unknown' }}</p>
            <p class="text-xs text-gray-400 mt-2">
              {{ selectedPreviewItem.file_path ? 'File path exists but cannot be displayed' : 'No file was uploaded with this submission' }}
            </p>
            <div v-if="selectedPreviewItem.caption" class="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p class="text-xs text-yellow-700 font-semibold mb-1">Caption/Text Submission:</p>
              <p class="text-sm text-gray-700">{{ selectedPreviewItem.caption }}</p>
            </div>
          </div>
        </div>

        <!-- Submission Details -->
        <div class="grid grid-cols-2 gap-4 bg-indigo-50 rounded-lg p-4">
          <div>
            <div class="text-xs text-gray-600 mb-1">Activity Title:</div>
            <div class="font-semibold text-gray-900">{{ selectedPreviewItem.activity_title }}</div>
          </div>
          <div>
            <div class="text-xs text-gray-600 mb-1">Activity Type:</div>
            <div class="font-semibold text-gray-900 capitalize">{{ selectedPreviewItem.activity_type }}</div>
          </div>
          <div>
            <div class="text-xs text-gray-600 mb-1">Folder:</div>
            <div class="flex items-center gap-2 font-semibold text-gray-900">
              <i class="pi pi-folder text-indigo-600"></i>
              <span>{{ selectedPreviewItem.folder_name }}</span>
            </div>
          </div>
          <div>
            <div class="text-xs text-gray-600 mb-1">Submitted:</div>
            <div class="font-semibold text-gray-900">{{ formatSubmittedDateTime(selectedPreviewItem.submitted_at) }}</div>
          </div>
          <div v-if="selectedPreviewItem.status === 'scored'" class="col-span-2">
            <div class="text-xs text-gray-600 mb-1">Score:</div>
            <div class="text-2xl font-bold text-indigo-600">{{ selectedPreviewItem.score }} points</div>
          </div>
        </div>

        <!-- Caption (if exists) -->
        <div v-if="selectedPreviewItem.caption" class="bg-white rounded-lg p-4 border border-gray-200">
          <div class="text-xs text-gray-600 mb-2">Caption:</div>
          <p class="text-gray-800">{{ selectedPreviewItem.caption }}</p>
        </div>

        <!-- Feedback (if scored) -->
        <div v-if="selectedPreviewItem.status === 'scored' && selectedPreviewItem.feedback" class="bg-green-50 rounded-lg p-4 border border-green-200">
          <div class="text-xs text-green-700 font-semibold mb-2">Teacher Feedback:</div>
          <p class="text-gray-800">{{ selectedPreviewItem.feedback }}</p>
        </div>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3">
          <button
            @click="closePreviewDialog"
            class="px-5 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors duration-200"
          >
            Close
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

    <!-- Portfolio Envelope Designer Dialog -->
    <Dialog v-model:visible="showEnvelopeDesigner"
        modal
        header="Design Your Portfolio Envelope"
        :style="{ width: '95%', maxWidth: '70rem' }"
        :contentStyle="{ padding: '0' }">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
            <!-- Left Side: Design Controls -->
            <div class="space-y-6">
                <div class="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-6">
                    <h3 class="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                        <i class="pi pi-palette text-indigo-600"></i>
                        Customize Your Envelope
                    </h3>
                    
                    <!-- Portfolio Title -->
                    <div class="mb-6">
                        <label class="block text-sm font-medium text-gray-700 mb-2">Portfolio Title</label>
                        <input
                            v-model="envelopeDesign.title"
                            type="text"
                            placeholder="My Portfolio"
                            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                        />
                    </div>

                    <!-- Student Name -->
                    <div class="mb-6">
                        <label class="block text-sm font-medium text-gray-700 mb-2">Your Name</label>
                        <input
                            v-model="envelopeDesign.studentName"
                            type="text"
                            placeholder="Enter your name"
                            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                        />
                    </div>

                    <!-- Class Name -->
                    <div class="mb-6">
                        <label class="block text-sm font-medium text-gray-700 mb-2">Class</label>
                        <input
                            v-model="envelopeDesign.className"
                            type="text"
                            :placeholder="props.className"
                            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                        />
                    </div>

                    <!-- Envelope Color -->
                    <div class="mb-6">
                        <label class="block text-sm font-medium text-gray-700 mb-3">Envelope Color</label>
                        <div class="grid grid-cols-5 gap-3">
                            <button
                                v-for="color in envelopeColors"
                                :key="color.value"
                                @click="envelopeDesign.color = color.value"
                                :style="{ backgroundColor: color.value }"
                                :class="[
                                    'w-full h-12 rounded-lg transition-all duration-200 border-4',
                                    envelopeDesign.color === color.value ? 'border-gray-800 scale-110 shadow-lg' : 'border-transparent hover:scale-105'
                                ]"
                                :title="color.name"
                            ></button>
                        </div>
                    </div>

                    <!-- Pattern Selection -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-3">Pattern Style</label>
                        <div class="grid grid-cols-3 gap-3">
                            <button
                                v-for="pattern in envelopePatterns"
                                :key="pattern.value"
                                @click="envelopeDesign.pattern = pattern.value"
                                :class="[
                                    'px-4 py-3 rounded-lg border-2 transition-all duration-200 text-sm font-medium',
                                    envelopeDesign.pattern === pattern.value
                                        ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                                        : 'border-gray-300 bg-white text-gray-700 hover:border-indigo-400'
                                ]"
                            >
                                {{ pattern.name }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Side: Live Preview -->
            <div class="space-y-4">
                <div class="bg-gray-50 rounded-xl p-6">
                    <h3 class="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                        <i class="pi pi-eye text-indigo-600"></i>
                        Live Preview
                    </h3>
                    
                    <!-- Envelope Preview -->
                    <div class="relative w-full aspect-[4/3] rounded-xl overflow-hidden shadow-2xl"
                         :style="{ backgroundColor: envelopeDesign.color }">
                        
                        <!-- Pattern Overlay -->
                        <div v-if="envelopeDesign.pattern === 'dots'" 
                             class="absolute inset-0 opacity-20"
                             style="background-image: radial-gradient(circle, white 2px, transparent 2px); background-size: 20px 20px;">
                        </div>
                        <div v-else-if="envelopeDesign.pattern === 'lines'" 
                             class="absolute inset-0 opacity-20"
                             style="background-image: repeating-linear-gradient(45deg, white 0, white 2px, transparent 2px, transparent 10px);">
                        </div>
                        <div v-else-if="envelopeDesign.pattern === 'grid'" 
                             class="absolute inset-0 opacity-20"
                             style="background-image: linear-gradient(white 1px, transparent 1px), linear-gradient(90deg, white 1px, transparent 1px); background-size: 20px 20px;">
                        </div>

                        <!-- Envelope Flap -->
                        <div class="absolute top-0 left-0 right-0 h-1/3 border-b-4 border-white/30"
                             :style="{ 
                                 background: `linear-gradient(180deg, ${envelopeDesign.color} 0%, ${adjustBrightness(envelopeDesign.color, -20)} 100%)`
                             }">
                            <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-0 h-0 
                                        border-l-[100px] border-r-[100px] border-t-[60px] border-l-transparent border-r-transparent"
                                 :style="{ borderTopColor: adjustBrightness(envelopeDesign.color, -20) }">
                            </div>
                        </div>

                        <!-- Content Area -->
                        <div class="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                            <div class="bg-white/20 backdrop-blur-md rounded-2xl p-5 shadow-xl border border-white/30 max-w-sm">
                                <h2 class="text-xl font-bold text-white mb-2" style="text-shadow: 0 2px 8px rgba(0,0,0,0.3)">
                                    {{ envelopeDesign.title || 'My Portfolio' }}
                                </h2>
                                <p class="text-base text-white/90 font-medium mb-1" style="text-shadow: 0 1px 4px rgba(0,0,0,0.2)">
                                    {{ envelopeDesign.studentName || 'Student Name' }}
                                </p>
                                <p class="text-sm text-white/80" style="text-shadow: 0 1px 4px rgba(0,0,0,0.2)">
                                    {{ envelopeDesign.className || props.className }}
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="flex gap-3 mt-6">
                        <button
                            @click="showEnvelopeDesigner = false"
                            class="flex-1 px-4 py-3 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                        >
                            Cancel
                        </button>
                        <button
                            @click="showConfirmEnvelopeDialog"
                            class="flex-1 px-4 py-3 text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
                        >
                            <i class="pi pi-check"></i>
                            Save & Continue
                        </button>
                    </div>
                </div>
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
                {{ calculateTotalScore(submissionScore.criteria_scores) }}
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

    <!-- Submit Portfolio Confirmation Dialog -->
    <Dialog v-model:visible="showSubmitPortfolioDialog"
        modal
        header="Submit Portfolio"
        :style="{ width: '90%', maxWidth: '32rem' }">
        <div class="space-y-4">
            <div class="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                <i class="pi pi-exclamation-triangle text-amber-600 text-xl mt-1"></i>
                <div class="flex-1">
                    <h4 class="font-semibold text-gray-900 mb-1">Confirm Submission</h4>
                    <p class="text-sm text-gray-700">
                        Are you sure you want to submit your portfolio? Once submitted, your teacher will be able to view it.
                    </p>
                </div>
            </div>
            <div class="flex justify-end gap-3 pt-2">
                <button @click="showSubmitPortfolioDialog = false"
                    class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors">
                    Cancel
                </button>
                <button @click="confirmSubmitPortfolio"
                    :disabled="isSubmittingPortfolio"
                    class="px-5 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 rounded-lg transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2">
                    <i v-if="isSubmittingPortfolio" class="pi pi-spin pi-spinner"></i>
                    <i v-else class="pi pi-check"></i>
                    <span>{{ isSubmittingPortfolio ? 'Submitting...' : 'Confirm Submit' }}</span>
                </button>
            </div>
        </div>
    </Dialog>

    <!-- Remove File Confirmation Dialog -->
    <Dialog v-model:visible="showRemoveConfirmDialog" modal :style="{ width: '90vw', maxWidth: '450px' }" :dismissableMask="true">
      <template #header>
        <div class="flex items-center gap-3">
          <i class="pi pi-exclamation-triangle text-orange-600 text-xl"></i>
          <h3 class="text-lg font-bold text-gray-800">Remove Attached Work</h3>
        </div>
      </template>

      <div class="py-4">
        <p class="text-gray-700 mb-4">Are you sure you want to remove this attached work?</p>
        <div v-if="fileToRemove" class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg border border-gray-200">
          <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <i v-if="fileToRemove.type === 'image'" class="pi pi-image text-indigo-600 text-xl"></i>
            <i v-else-if="fileToRemove.type === 'pdf'" class="pi pi-file-pdf text-red-600 text-xl"></i>
            <i v-else class="pi pi-file text-gray-600 text-xl"></i>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">{{ fileToRemove.name }}</p>
            <p class="text-xs text-gray-500 capitalize">{{ fileToRemove.type }}</p>
          </div>
        </div>
        <p class="text-sm text-gray-500 mt-4">This action cannot be undone.</p>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3">
          <button
            @click="showRemoveConfirmDialog = false"
            class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors duration-200"
          >
            Cancel
          </button>
          <button
            @click="removeDraftFile"
            class="px-5 py-2.5 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors duration-200 flex items-center gap-2"
          >
            <i class="pi pi-trash"></i>
            <span>Remove</span>
          </button>
        </div>
      </template>
    </Dialog>

    <!-- Upload Dialog with Tabs -->
    <Dialog v-model:visible="showUploadDialog" modal :style="{ width: '90vw', maxWidth: '700px' }" :dismissableMask="true">
      <template #header>
        <div class="flex items-center gap-3">
          <i class="pi pi-cloud-upload text-indigo-600 text-xl"></i>
          <h3 class="text-lg font-bold text-gray-800">Add or Create Work</h3>
        </div>
      </template>

      <div class="space-y-4">
        <!-- Tabs Navigation -->
        <div class="flex border-b border-gray-200">
          <button
            v-for="tab in uploadTabs"
            :key="tab.id"
            @click="activeUploadTab = tab.id"
            :class="[
              'flex-1 px-4 py-3 text-sm font-medium transition-all duration-200 border-b-2',
              activeUploadTab === tab.id
                ? 'border-indigo-600 text-indigo-600 bg-indigo-50'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            ]"
          >
            <div class="flex items-center justify-center gap-2">
              <i :class="tab.icon"></i>
              <span>{{ tab.name }}</span>
            </div>
          </button>
        </div>

        <!-- Tab Content -->
        <div class="min-h-[300px]">
          <!-- From Device Tab -->
          <div v-if="activeUploadTab === 'device'" class="flex flex-col items-center justify-center py-12">
            <div class="text-center space-y-4">
              <div class="w-20 h-20 mx-auto bg-indigo-100 rounded-full flex items-center justify-center">
                <i class="pi pi-upload text-indigo-600 text-3xl"></i>
              </div>
              <div>
                <h4 class="text-lg font-semibold text-gray-900 mb-2">Upload from Device</h4>
                <p class="text-sm text-gray-500 mb-6">Select a file from your computer</p>
              </div>
              <button
                @click="triggerAutoSaveFileUpload"
                class="px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors duration-200 flex items-center gap-2 mx-auto"
              >
                <i class="pi pi-folder-open"></i>
                <span>Browse Files</span>
              </button>
              <p class="text-xs text-gray-400 mt-4">Supported formats: Images, PDF, Word documents</p>
            </div>
          </div>

          <!-- My Sketch Tab -->
          <div v-else-if="activeUploadTab === 'sketch'" class="py-4">
            <!-- Sub-tabs -->
            <div class="flex border-b border-gray-200 mb-4">
              <button
                @click="activeSketchSubTab = 'sketches'"
                :class="[
                  'px-4 py-2 text-sm font-medium transition-all duration-200 border-b-2',
                  activeSketchSubTab === 'sketches'
                    ? 'border-purple-600 text-purple-600 bg-purple-50'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                ]"
              >
                <div class="flex items-center gap-2">
                  <i class="pi pi-palette"></i>
                  <span>Sketches</span>
                </div>
              </button>
            </div>

            <!-- Sketches Sub-tab Content -->
            <div v-if="activeSketchSubTab === 'sketches'">
              <!-- Loading State -->
              <div v-if="loadingSketches" class="flex justify-center items-center py-12">
                <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
              </div>

              <!-- Empty State -->
              <div v-else-if="!loadingSketches && mySketches.length === 0" class="text-center py-12">
                <div class="w-12 h-12 mx-auto bg-gray-100 rounded-full flex items-center justify-center mb-3">
                  <i class="pi pi-inbox text-gray-400 text-lg"></i>
                </div>
                <p class="text-sm text-gray-500">No sketches saved yet</p>
                <p class="text-xs text-gray-400 mt-1">Create sketches in the Sketch page</p>
              </div>

              <!-- Sketches Grid - Extra Small Size -->
              <div v-else class="grid grid-cols-4 gap-2 max-h-[320px] overflow-y-auto px-1">
                <div
                  v-for="sketch in mySketches"
                  :key="sketch.id"
                  @click="selectSketch(sketch)"
                  class="relative group cursor-pointer rounded-md overflow-hidden border-2 transition-all duration-200 hover:border-purple-500 hover:shadow-md"
                  :class="selectedSketchId === sketch.id ? 'border-purple-600 ring-2 ring-purple-200' : 'border-gray-200'"
                >
                  <!-- Sketch Image -->
                  <div class="aspect-square bg-white p-1">
                    <img
                      :src="sketch.image_data"
                      :alt="sketch.title"
                      class="w-full h-full object-contain"
                    />
                  </div>
                  
                  <!-- Overlay on Hover -->
                  <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all duration-200"></div>
                  
                  <!-- Selected Checkmark -->
                  <div
                    v-if="selectedSketchId === sketch.id"
                    class="absolute top-1 right-1 w-4 h-4 bg-purple-600 rounded-full flex items-center justify-center"
                  >
                    <i class="pi pi-check text-white" style="font-size: 8px;"></i>
                  </div>
                  
                  <!-- Date Footer -->
                  <div class="bg-gray-700 bg-opacity-90 text-white text-[9px] px-1 py-0.5 text-center leading-tight">
                    <div class="font-medium">Created:</div>
                    <div>{{ formatSketchDate(sketch.created_at) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Submitted Collection Tab -->
          <div v-else-if="activeUploadTab === 'collection'" class="flex flex-col items-center justify-center py-12">
            <div class="text-center space-y-4">
              <div class="w-20 h-20 mx-auto bg-green-100 rounded-full flex items-center justify-center">
                <i class="pi pi-folder text-green-600 text-3xl"></i>
              </div>
              <div>
                <h4 class="text-lg font-semibold text-gray-900 mb-2">Submitted Collection</h4>
                <p class="text-sm text-gray-500 mb-6">Reuse from your previous submissions</p>
              </div>
              <div class="px-6 py-4 bg-gray-50 rounded-lg border border-gray-200">
                <p class="text-sm text-gray-600 italic">Coming soon...</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3">
          <button
            @click="showUploadDialog = false"
            class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors duration-200"
          >
            Cancel
          </button>
          <button
            v-if="activeUploadTab === 'sketch' && selectedSketchId"
            @click="useSelectedSketch"
            :disabled="isSubmitting"
            class="px-5 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <i v-if="!isSubmitting" class="pi pi-check"></i>
            <i v-else class="pi pi-spin pi-spinner"></i>
            <span>{{ isSubmitting ? 'Adding...' : 'Use This Sketch' }}</span>
          </button>
        </div>
      </template>
    </Dialog>

    <!-- Turn In Dialog -->
    <Dialog v-model:visible="showTurnInDialog" modal :style="{ width: '90vw', maxWidth: '600px' }" :dismissableMask="true">
      <template #header>
        <div class="flex items-center gap-3">
          <i class="pi pi-upload text-indigo-600 text-xl"></i>
          <h3 class="text-lg font-bold text-gray-800">Submit Your Work</h3>
        </div>
      </template>

      <div class="space-y-4">
        <!-- Caption Input -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Caption</label>
          <textarea
            v-model="submissionCaption"
            rows="4"
            placeholder="Add a caption to your work..."
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
          ></textarea>
        </div>

        <!-- Upload Your Work Section -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Upload Your Work</label>
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center bg-gray-50">
            <div v-if="draftFiles.length > 0" class="space-y-2">
              <div
                v-for="file in draftFiles"
                :key="file.id"
                class="flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-200"
              >
                <div class="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <i v-if="file.type === 'image'" class="pi pi-image text-indigo-600"></i>
                  <i v-else-if="file.type === 'pdf'" class="pi pi-file-pdf text-red-600"></i>
                  <i v-else class="pi pi-file text-gray-600"></i>
                </div>
                <div class="flex-1 text-left">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ file.name }}</p>
                  <p class="text-xs text-gray-500 capitalize">{{ file.type }}</p>
                </div>
              </div>
            </div>
            <div v-else class="text-gray-500">
              <i class="pi pi-upload text-3xl mb-2"></i>
              <p class="text-sm">Click to upload or drag and drop</p>
              <p class="text-xs text-gray-400">(PDF, DOC, DOCX, or Images)</p>
            </div>
          </div>
        </div>

        <!-- Post to Feed Checkbox -->
        <div class="flex items-center gap-2">
          <input
            type="checkbox"
            id="postToFeed"
            v-model="postToFeed"
            class="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
          />
          <label for="postToFeed" class="text-sm text-gray-700">
            Post this output to feeds (visible to class)
          </label>
        </div>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3">
          <button
            @click="showTurnInDialog = false"
            class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors duration-200"
          >
            Cancel
          </button>
          <button
            @click="turnInDraft"
            :disabled="isSubmitting || draftFiles.length === 0"
            class="px-5 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <i v-if="isSubmitting" class="pi pi-spin pi-spinner"></i>
            <i v-else class="pi pi-check"></i>
            <span>{{ isSubmitting ? 'Submitting...' : 'Submit Work' }}</span>
          </button>
        </div>
      </template>
    </Dialog>

    <!-- File Preview Dialog -->
    <Dialog v-model:visible="showFilePreview" modal :style="{ width: '90vw', maxWidth: '1200px' }" :dismissableMask="true">
      <template #header>
        <div class="flex items-center gap-3">
          <i class="pi pi-eye text-indigo-600 text-xl"></i>
          <h3 class="text-lg font-bold text-gray-800">File Preview</h3>
        </div>
      </template>

      <div v-if="previewFile" class="space-y-4">
        <!-- File Info -->
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center">
              <i v-if="previewFile.type === 'image'" class="pi pi-image text-indigo-600 text-xl"></i>
              <i v-else-if="previewFile.type === 'pdf'" class="pi pi-file-pdf text-red-600 text-xl"></i>
              <i v-else class="pi pi-file text-gray-600 text-xl"></i>
            </div>
            <div>
              <p class="font-semibold text-gray-900">{{ previewFile.name }}</p>
              <p class="text-sm text-gray-500 capitalize">{{ previewFile.type }}</p>
            </div>
          </div>
        </div>

        <!-- File Preview Content -->
        <div class="bg-gray-100 rounded-lg p-4 min-h-[300px] flex items-center justify-center">
          <!-- Image Preview -->
          <img
            v-if="previewFile.type === 'image' && previewFile.path"
            :src="previewFile.path"
            :alt="previewFile.name"
            class="max-w-full max-h-[400px] object-contain rounded-lg shadow-lg"
          />
          
          <!-- PDF Preview -->
          <iframe
            v-else-if="previewFile.type === 'pdf' && previewFile.path"
            :src="previewFile.path"
            class="w-full h-[600px] rounded-lg border border-gray-300"
          ></iframe>
          
          <!-- Document Preview -->
          <div v-else-if="previewFile.type === 'document'" class="text-center">
            <i class="pi pi-file text-6xl text-indigo-400 mb-4"></i>
            <p class="text-gray-700 font-medium mb-2">{{ previewFile.name }}</p>
            <p class="text-gray-500 text-sm">Document file</p>
          </div>
          
          <!-- Other Files -->
          <div v-else class="text-center">
            <i class="pi pi-file text-6xl text-gray-400 mb-4"></i>
            <p class="text-gray-700 font-medium mb-2">{{ previewFile.name }}</p>
            <p class="text-gray-500 text-sm">File preview not available</p>
          </div>
        </div>
      </div>

      <template #footer>
        <button
          @click="showFilePreview = false"
          class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors duration-200"
        >
          Close
        </button>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, inject, watch } from 'vue';
import axios from 'axios';
import Dialog from 'primevue/dialog';
import { useToast } from '../../composables/useToast';

// Initialize toast
const { showSuccess, showError, showInfo, showWarning } = useToast();

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
const portfolioCompilationRequested = ref(false); // Track if teacher requested compilation
const showEnvelopeDesigner = ref(false); // Track if envelope designer is shown
const showEnvelopeConfirmDialog = ref(false); // Track confirmation dialog
const portfolioEnvelopeCreated = ref(false); // Track if envelope has been created
const isEnvelopeOpen = ref(false); // Track if envelope is opened
const envelopeDesign = ref({
  color: '#4F46E5',
  pattern: 'solid',
  title: 'My Portfolio',
  studentName: '',
  className: ''
});

// Portfolio activities
const portfolioActivities = ref([]);
const currentActivityIndex = ref(0);
const showMissingActivitiesDialog = ref(false);
const missingActivities = ref([]);
const activePortfolioTab = ref('all'); // 'all' or 'missing'

// Navigation tabs
const tabs = [
  { id: 'portfolio', name: 'Activities', icon: 'pi-folder' },
  { id: 'compilation', name: 'Portfolio Compilation', icon: 'pi-book' },
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
const isRequestingPost = ref(false);
const isCompilingMissing = ref(false); // Flag for missing activity compilation

// Check if student has already submitted (reactive state)
const hasSubmittedWork = ref(false);
const existingSubmission = ref(null);
const hasScore = ref(false);
const showScoreDialog = ref(false);
const submissionScore = ref(null);

// Submitted Collection state
const showSubmittedCollection = ref(false);
const submittedCollection = ref([]);
const isLoadingCollection = ref(false);

// Draft submission state
const draftSubmission = ref(null);
const draftFiles = ref([]);
const showFilePreview = ref(false);
const previewFile = ref(null);
const showTurnInDialog = ref(false);
const submissionCaption = ref('');
const postToFeed = ref(false);
const showRemoveConfirmDialog = ref(false);
const fileToRemove = ref(null);

// Portfolio submission state
const showSubmitPortfolioDialog = ref(false);
const isSubmittingPortfolio = ref(false);
const portfolioEnvelope = ref(null);

// Check if activity is past due date/time
const isPastDue = computed(() => {
  if (!selectedActivity.value || !selectedActivity.value.due_date) {
    return false;
  }
  
  const now = new Date();
  let dueDateTime;
  
  if (selectedActivity.value.due_time) {
    // Combine date and time
    dueDateTime = new Date(`${selectedActivity.value.due_date}T${selectedActivity.value.due_time}`);
  } else {
    // If no time specified, use end of day (23:59:59)
    dueDateTime = new Date(selectedActivity.value.due_date);
    dueDateTime.setHours(23, 59, 59, 999);
  }
  
  return now > dueDateTime;
});

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
          let isLate = false;
          try {
            const submissionResponse = await axios.get(`/api/activities/${activity.id}/submissions/`);
            if (submissionResponse.data && submissionResponse.data.length > 0) {
              hasSubmitted = true;
              isLate = submissionResponse.data[0].is_late || false;
            }
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

          // Format due time if available
          let formattedTime = '';
          if (activity.due_time) {
            const [hours, minutes] = activity.due_time.split(':');
            const hour = parseInt(hours);
            const ampm = hour >= 12 ? 'PM' : 'AM';
            const displayHour = hour % 12 || 12;
            formattedTime = `${displayHour}:${minutes} ${ampm}`;
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
            due_time: activity.due_time,
            formattedTime: formattedTime,
            hasSubmitted: hasSubmitted,
            isLate: isLate,
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
  showSubmittedCollection.value = false;
  
  // Update view state to folder only
  if (selectedFolder.value) {
    localStorage.setItem('student_current_view', JSON.stringify({
      selectedFolder: selectedFolder.value,
      selectedActivity: null
    }));
    console.log('💾 Updated view state: Back to folder', selectedFolder.value.title);
  }
};

// Load submitted collection
const loadSubmittedCollection = async () => {
  isLoadingCollection.value = true;
  try {
    const response = await axios.get('/api/submissions/my-collection/');
    if (response.data) {
      submittedCollection.value = response.data;
      console.log('✅ Loaded submitted collection:', submittedCollection.value.length, 'items');
    }
  } catch (error) {
    console.error('❌ Error loading submitted collection:', error);
    showError('Failed to load submitted collection', 'Load Failed');
  } finally {
    isLoadingCollection.value = false;
  }
};

// Show submitted collection
const openSubmittedCollection = async () => {
  showSubmittedCollection.value = true;
  await loadSubmittedCollection();
};

// Close submitted collection
const closeSubmittedCollection = () => {
  showSubmittedCollection.value = false;
  // Reset selection state
  isSelectMode.value = false;
  selectedSubmissions.value = [];
};

// Toggle select mode
const toggleSelectMode = () => {
  isSelectMode.value = !isSelectMode.value;
  if (!isSelectMode.value) {
    selectedSubmissions.value = [];
  }
};

// Toggle submission selection
const toggleSubmissionSelection = (submissionId) => {
  const index = selectedSubmissions.value.indexOf(submissionId);
  if (index > -1) {
    selectedSubmissions.value.splice(index, 1);
  } else {
    selectedSubmissions.value.push(submissionId);
  }
};

// Open preview dialog
const openPreviewDialog = (item) => {
  // Don't open if clicking checkbox in select mode
  if (isSelectMode.value) return;
  
  selectedPreviewItem.value = item;
  showPreviewDialog.value = true;
  console.log('📸 Opening preview for submission:', item.id);
  console.log('   File path:', item.file_path ? `${item.file_path.substring(0, 50)}...` : 'No file path');
  console.log('   File path starts with data:', item.file_path?.startsWith('data:'));
  console.log('   File type:', item.file_type);
  console.log('   Activity title:', item.activity_title);
  console.log('   Caption:', item.caption);
  
  // Debug file type detection
  if (item.file_path && item.file_path.startsWith('data:')) {
    const mimeMatch = item.file_path.match(/data:([^;]+);/);
    console.log('   Detected MIME type:', mimeMatch ? mimeMatch[1] : 'Unknown');
  }
};

// Handle preview image load error
const handlePreviewImageError = (event) => {
  console.error('❌ Preview image failed to load:', event.target.src);
  console.error('   Selected item:', selectedPreviewItem.value);
};

// Close preview dialog
const closePreviewDialog = () => {
  showPreviewDialog.value = false;
  selectedPreviewItem.value = null;
};

// Get submission image URL
const getSubmissionImageUrl = () => {
  // Try multiple sources for the image URL
  if (studentSubmissions.value && studentSubmissions.value.length > 0) {
    const submission = studentSubmissions.value[0];
    const url = submission.previewUrl || submission.file_url || submission.file_path || submission.file;
    console.log('📸 Getting image from studentSubmissions:', url);
    return url;
  }
  
  if (existingSubmission.value) {
    const url = existingSubmission.value.file_url || existingSubmission.value.file_path || existingSubmission.value.file;
    console.log('📸 Getting image from existingSubmission:', url);
    return url;
  }
  
  console.warn('⚠️ No image URL found');
  return null;
};

// Open post output dialog
const openPostOutputDialog = () => {
  if (!existingSubmission.value) {
    console.error('❌ No existing submission found');
    return;
  }
  
  console.log('📤 Opening post output dialog');
  console.log('   Submission ID:', existingSubmission.value.id);
  console.log('   File path:', existingSubmission.value.file_path);
  console.log('   File type:', existingSubmission.value.file_type);
  console.log('   Caption:', existingSubmission.value.caption);
  console.log('   Student submissions:', studentSubmissions.value);
  console.log('   Image URL:', getSubmissionImageUrl());
  
  // Pre-fill caption if exists
  postOutputCaption.value = existingSubmission.value.caption || '';
  includeScore.value = false;
  showPostOutputDialog.value = true;
};

// Close post output dialog
const closePostOutputDialog = () => {
  showPostOutputDialog.value = false;
  postOutputCaption.value = '';
  includeScore.value = false;
};

// Submit post output request
const submitPostOutput = async () => {
  if (!existingSubmission.value) return;
  
  if (!postOutputCaption.value || !postOutputCaption.value.trim()) {
    showError('Please add a caption to your work', 'Caption Required');
    return;
  }
  
  try {
    isPostingOutput.value = true;
    
    console.log('📤 Sending post approval request...');
    console.log('   Submission ID:', existingSubmission.value.id);
    console.log('   Caption:', postOutputCaption.value);
    console.log('   Include Score:', includeScore.value);
    
    const response = await axios.post(
      `/api/submissions/${existingSubmission.value.id}/request-post-approval/`,
      {
        caption: postOutputCaption.value.trim(),
        include_score: includeScore.value
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    
    console.log('✅ Post output request sent:', response.data);
    showSuccess('Your request to post output has been sent to your teacher for approval', 'Request Sent');
    
    closePostOutputDialog();
  } catch (error) {
    console.error('❌ Error submitting post output request:', error);
    console.error('   Error response:', error.response?.data);
    console.error('   Error status:', error.response?.status);
    
    const errorMessage = error.response?.data?.error || 'Failed to send post output request';
    showError(errorMessage, 'Request Failed');
  } finally {
    isPostingOutput.value = false;
  }
};

// Delete selected submissions
const deleteSelectedSubmissions = async () => {
  try {
    let deletePromises;
    let count;
    
    if (deleteAction.value === 'all') {
      // Delete all submissions
      deletePromises = submittedCollection.value.map(item =>
        axios.delete(`/api/submissions/${item.id}/`)
      );
      count = submittedCollection.value.length;
    } else {
      // Delete selected submissions
      deletePromises = selectedSubmissions.value.map(id =>
        axios.delete(`/api/submissions/${id}/`)
      );
      count = selectedSubmissions.value.length;
    }
    
    await Promise.all(deletePromises);
    
    console.log('✅ Removed submissions from collection:', count);
    showSuccess(`${count} submission(s) removed from collection`, 'Removed');
    
    // Reload submitted collection
    await loadSubmittedCollection();
    
    // Clear selection and exit select mode
    selectedSubmissions.value = [];
    isSelectMode.value = false;
    showDeleteConfirmDialog.value = false;
    deleteAction.value = null;
  } catch (error) {
    console.error('❌ Error deleting submissions:', error);
    showError('Failed to delete submissions', 'Delete Failed');
  }
};

// Function to get activity status
const getActivityStatus = (activity) => {
  // Check if past due date and time first
  let isPastDue = false;
  if (activity.due_date) {
    const now = new Date();
    
    // Create due date/time
    let dueDateTime;
    if (activity.due_time) {
      // Combine date and time
      dueDateTime = new Date(`${activity.due_date}T${activity.due_time}`);
    } else {
      // If no time specified, use end of day (23:59:59)
      dueDateTime = new Date(activity.due_date);
      dueDateTime.setHours(23, 59, 59, 999);
    }
    
    isPastDue = now > dueDateTime;
  }
  
  // If already submitted
  if (activity.hasSubmitted) {
    // Check if it was submitted late
    if (activity.isLate || (isPastDue && activity.submittedAt)) {
      activity.isLate = true; // Set the flag for the template
    }
    return 'submitted';
  }
  
  // If past due date/time and not submitted, return 'missing'
  if (isPastDue) {
    return 'missing';
  }
  
  // Otherwise, return 'pending'
  return 'pending';
};

// Calculate total points from scoring criteria
const calculateTotalPoints = (criteria) => {
  if (!criteria || criteria.length === 0) return 0;
  return criteria.reduce((total, criterion) => {
    return total + (parseInt(criterion.maxScore) || 0);
  }, 0);
};

// Get file extension from base64 data URL
const getFileExtension = (dataUrl) => {
  if (!dataUrl || !dataUrl.startsWith('data:')) return 'file';
  
  const mimeMatch = dataUrl.match(/data:([^;]+);/);
  if (!mimeMatch) return 'file';
  
  const mimeType = mimeMatch[1];
  const mimeToExt = {
    'image/jpeg': 'jpg',
    'image/jpg': 'jpg',
    'image/png': 'png',
    'image/gif': 'gif',
    'image/webp': 'webp',
    'application/pdf': 'pdf',
    'application/msword': 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'application/vnd.ms-excel': 'xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
    'text/plain': 'txt'
  };
  
  return mimeToExt[mimeType] || 'file';
};

// Format submitted date and time (Philippine Time)
const formatSubmittedDateTime = (dateTimeString) => {
  if (!dateTimeString) return '';
  
  try {
    const date = new Date(dateTimeString);
    
    // Format date: Oct 24, 2025 (Philippine Time)
    const dateStr = date.toLocaleDateString('en-PH', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      timeZone: 'Asia/Manila'
    });
    
    // Format time: 4:18 PM (Philippine Time)
    const timeStr = date.toLocaleTimeString('en-PH', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
      timeZone: 'Asia/Manila'
    });
    
    return `${dateStr} at ${timeStr}`;
  } catch (error) {
    console.error('Error formatting date:', error);
    return dateTimeString;
  }
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

// Calculate total score from criteria_scores JSON (sum of actual scores)
const calculateTotalScore = (criteriaScoresJson) => {
  if (!criteriaScoresJson) return 0;
  try {
    const criteria = typeof criteriaScoresJson === 'string' 
      ? JSON.parse(criteriaScoresJson) 
      : criteriaScoresJson;
    return criteria.reduce((total, criterion) => {
      return total + (parseInt(criterion.score) || 0);
    }, 0);
  } catch (error) {
    console.error('Error calculating total score:', error);
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
  
  // Load draft submissions separately
  await loadDraftSubmissions(activity.id);
};

// Load draft submissions for the current activity
const loadDraftSubmissions = async (activityId) => {
  try {
    // Request submissions including drafts
    const response = await axios.get(`/api/activities/${activityId}/submissions/?include_drafts=true`);
    console.log('📥 Checking for draft submissions:', response.data);
    
    // Filter for draft submissions only
    const drafts = response.data.filter(sub => sub.status === 'draft');
    
    if (drafts.length > 0) {
      // Load the most recent draft
      const latestDraft = drafts[0];
      draftSubmission.value = latestDraft;
      
      // Use file_url from backend (already formatted correctly)
      let filePath = latestDraft.file_url || latestDraft.file_path || latestDraft.file;
      
      draftFiles.value = [{
        id: latestDraft.id,
        name: latestDraft.caption || 'Uploaded file',
        type: latestDraft.file_type,
        path: filePath
      }];
      console.log('✅ Loaded draft submission:', draftSubmission.value);
      console.log('📎 File path:', filePath);
    } else {
      draftSubmission.value = null;
      draftFiles.value = [];
      console.log('ℹ️ No draft submissions found');
    }
  } catch (error) {
    console.error('❌ Error loading draft submissions:', error);
  }
};

// Load submissions for the current activity
const loadActivitySubmissions = async (activityId) => {
  try {
    const response = await axios.get(`/api/activities/${activityId}/submissions/`);
    console.log('📥 API Response - Submissions:', response.data);
    
    if (response.data && response.data.length > 0) {
      // Map API response to display format
      studentSubmissions.value = response.data.map(submission => {
        // Use file_url from backend (already formatted correctly)
        let previewUrl = submission.file_url || submission.file_path || submission.file;
        
        console.log('🖼️ Processing submission:', {
          id: submission.id,
          caption: submission.caption,
          file_type: submission.file_type,
          has_file_url: !!submission.file_url,
          file_url: submission.file_url,
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
          is_late: submission.is_late || false,
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
      
      // Check if submission has been scored
      if (existingSubmission.value.status === 'scored' && existingSubmission.value.score !== null && existingSubmission.value.score !== undefined) {
        hasScore.value = true;
        submissionScore.value = {
          score: existingSubmission.value.score,
          feedback: existingSubmission.value.feedback,
          criteria_scores: existingSubmission.value.criteria_scores
        };
        console.log('✅ Submission has been scored:', submissionScore.value);
      } else {
        hasScore.value = false;
        submissionScore.value = null;
      }
      
      console.log('✅ Student already submitted:', existingSubmission.value);
      console.log('📊 Status:', existingSubmission.value.status, 'Score:', existingSubmission.value.score);
      console.log('📅 Submitted at (from backend):', existingSubmission.value.submitted_at);
      console.log('📅 Formatted:', formatSubmittedDateTime(existingSubmission.value.submitted_at));
    } else {
      hasSubmittedWork.value = false;
      existingSubmission.value = null;
      hasScore.value = false;
      submissionScore.value = null;
    }
  } catch (error) {
    console.error('Error checking submission status:', error);
    hasSubmittedWork.value = false;
    hasScore.value = false;
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

// Function to handle class change event
const handleClassChange = async (event) => {
  console.log('🔄 Class changed, reloading data...', event.detail);
  
  // Clear current view state
  selectedFolder.value = null;
  selectedActivity.value = null;
  studentSubmissions.value = [];
  hasSubmittedWork.value = false;
  localStorage.removeItem('student_current_view');
  
  // Reload folders
  await loadPortfolioFolders();
};

// Check if teacher has requested portfolio compilation
const checkPortfolioCompilationStatus = async () => {
  try {
    const className = props.className || selectedClass.value?.name;
    
    if (!className) {
      console.log('No class selected, skipping portfolio compilation check');
      return;
    }
    
    // Check for portfolio compilation notification
    const response = await axios.get(`/api/notifications/portfolio-compilation/${encodeURIComponent(className)}/`);
    
    if (response.data && response.data.compilation_requested) {
      portfolioCompilationRequested.value = true;
      console.log('✅ Portfolio compilation has been requested by teacher');
    } else {
      portfolioCompilationRequested.value = false;
      console.log('ℹ️ Portfolio compilation not yet requested');
    }
  } catch (error) {
    console.error('❌ Error checking portfolio compilation status:', error);
    // Default to false if there's an error
    portfolioCompilationRequested.value = false;
  }
};

// Load portfolio folders when component mounts
onMounted(async () => {
  // Authenticate with backend first, then load folders
  const authenticated = await authenticateWithBackend();
  if (authenticated) {
    // Check if student has an existing portfolio envelope
    await checkExistingEnvelope();
    
    // Restore previous view state after refresh
    const savedView = localStorage.getItem('student_current_view');
    if (savedView) {
      try {
        const viewState = JSON.parse(savedView);
        console.log('🔄 Restoring view state:', viewState);
        
        if (viewState.selectedFolder) {
          // First load all folders to ensure we have the latest data
          await loadPortfolioFolders();
          
          // Restore folder selection
          selectedFolder.value = viewState.selectedFolder;
          
          // Load activities for this folder
          await loadFolderActivities(viewState.selectedFolder.id);
          
          if (viewState.selectedActivity) {
            // Find the activity in the loaded activities
            const activity = folderActivities.value.find(a => a.id === viewState.selectedActivity.id);
            if (activity) {
              // Restore activity selection and load submissions
              selectedActivity.value = activity;
              
              // Reset score state
              hasScore.value = false;
              submissionScore.value = null;
              
              // Check submission status
              await checkSubmissionStatus(activity.id);
              
              // Load submissions for this activity
              await loadActivitySubmissions(activity.id);
              
              // Load draft submissions separately
              await loadDraftSubmissions(activity.id);
              
              console.log('✅ Restored activity view:', activity.title);
              console.log('✅ Submissions loaded:', studentSubmissions.value.length);
              console.log('✅ Draft files loaded:', draftFiles.value.length);
            } else {
              console.warn('⚠️ Activity not found in loaded activities');
            }
          }
        } else {
          // No saved view, just load folders normally
          await loadPortfolioFolders();
        }
      } catch (error) {
        console.error('❌ Error restoring view state:', error);
        localStorage.removeItem('student_current_view');
        // Fallback to loading folders normally
        await loadPortfolioFolders();
      }
    } else {
      // No saved view, just load folders normally
      await loadPortfolioFolders();
    }
  } else {
    console.error('Failed to authenticate with backend');
  }
  
  // Check for portfolio compilation request
  await checkPortfolioCompilationStatus();
  
  // Listen for class change events
  window.addEventListener('classChanged', handleClassChange);
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
const isSelectMode = ref(false);
const selectedSubmissions = ref([]);
const showDeleteConfirmDialog = ref(false);
const deleteAction = ref(null); // 'all' or 'selected'
const showPreviewDialog = ref(false);
const selectedPreviewItem = ref(null);
const showPostOutputDialog = ref(false);
const postOutputCaption = ref('');
const includeScore = ref(false);
const isPostingOutput = ref(false);
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
  window.removeEventListener('classChanged', handleClassChange);
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

// Upload dialog state
const showUploadDialog = ref(false);
const activeUploadTab = ref('device');
const uploadTabs = [
  { id: 'device', name: 'From Device', icon: 'pi pi-desktop' },
  { id: 'sketch', name: 'My Sketch', icon: 'pi pi-palette' },
  { id: 'collection', name: 'Submitted Collection', icon: 'pi pi-folder' }
];

// My Sketches state
const mySketches = ref([]);
const loadingSketches = ref(false);
const selectedSketchId = ref(null);
const activeSketchSubTab = ref('sketches');

// Watch for dialog opening to load sketches
watch(showUploadDialog, async (newValue) => {
  if (newValue && activeUploadTab.value === 'sketch') {
    await loadMySketches();
  }
});

// Watch for tab changes to load sketches when switching to sketch tab
watch(activeUploadTab, async (newValue) => {
  if (newValue === 'sketch' && showUploadDialog.value) {
    await loadMySketches();
  }
  // Reset selected sketch when changing tabs
  selectedSketchId.value = null;
  // Reset to sketches sub-tab
  activeSketchSubTab.value = 'sketches';
});

// Load sketches from API
const loadMySketches = async () => {
  loadingSketches.value = true;
  try {
    const response = await axios.get('/api/sketches/');
    mySketches.value = response.data;
    console.log('✅ Loaded sketches:', mySketches.value.length);
  } catch (error) {
    console.error('❌ Error loading sketches:', error);
    showError('Failed to load sketches', 'Error');
  } finally {
    loadingSketches.value = false;
  }
};

// Select a sketch
const selectSketch = (sketch) => {
  selectedSketchId.value = sketch.id;
};

// Format sketch date
const formatSketchDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    month: '2-digit',
    day: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  });
};

// Use selected sketch as submission
const useSelectedSketch = async () => {
  if (!selectedSketchId.value) return;
  
  const selectedSketch = mySketches.value.find(s => s.id === selectedSketchId.value);
  if (!selectedSketch) return;

  isSubmitting.value = true;

  try {
    console.log('📤 Using sketch as draft:', selectedSketch.title);

    // Convert base64 image to blob
    const base64Data = selectedSketch.image_data;
    const response = await fetch(base64Data);
    const blob = await response.blob();
    
    // Create a file from the blob
    const file = new File([blob], `${selectedSketch.title}.png`, { type: 'image/png' });

    // Create FormData for file upload as DRAFT
    const formData = new FormData();
    formData.append('file', file);
    formData.append('caption', selectedSketch.title);
    formData.append('post_to_feed', false);
    formData.append('is_draft', true);

    // Upload the file as draft
    const uploadResponse = await axios.post(
      `/api/activities/${selectedActivity.value.id}/submissions/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    console.log('✅ Sketch saved as draft:', uploadResponse.data);
    
    // Store draft submission
    draftSubmission.value = uploadResponse.data;
    draftFiles.value.push({
      id: uploadResponse.data.id,
      name: selectedSketch.title,
      type: uploadResponse.data.file_type,
      path: uploadResponse.data.file_path
    });
    
    // Show success message
    showSuccess('Sketch added as draft!', 'Saved');

    // Close dialog and reset
    showUploadDialog.value = false;
    selectedSketchId.value = null;
  } catch (error) {
    console.error('❌ Error using sketch:', error);
    showError(
      error.response?.data?.error || 'Failed to use sketch',
      'Error'
    );
  } finally {
    isSubmitting.value = false;
  }
};

// Auto-save file upload functions
const autoSaveFileInput = ref(null);

const triggerAutoSaveFileUpload = () => {
  if (autoSaveFileInput.value) {
    autoSaveFileInput.value.click();
    showUploadDialog.value = false; // Close dialog after file selection
  }
};

const handleAutoSaveFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  isSubmitting.value = true;

  try {
    // Create FormData for file upload as DRAFT
    const formData = new FormData();
    formData.append('file', file);
    formData.append('caption', file.name);
    formData.append('post_to_feed', false);
    formData.append('is_draft', true);  // Mark as draft

    console.log('📤 Saving file as draft:', file.name);

    // Upload the file as draft
    const response = await axios.post(
      `/api/activities/${selectedActivity.value.id}/submissions/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    console.log('✅ File saved as draft:', response.data);
    
    // Store draft submission
    draftSubmission.value = response.data;
    draftFiles.value.push({
      id: response.data.id,
      name: file.name,
      type: response.data.file_type,
      path: response.data.file_path
    });
    
    // Show success message
    showSuccess('File added as draft!', 'Saved');

    // Reset file input
    event.target.value = '';
  } catch (error) {
    console.error('❌ Error saving draft:', error);
    showError(
      error.response?.data?.error || 'Failed to save draft',
      'Save Failed'
    );
  } finally {
    isSubmitting.value = false;
  }
};

// Turn in the draft submission
const turnInDraft = async () => {
  if (!draftSubmission.value) {
    showWarning('Please add a file first', 'No File');
    return;
  }

  isSubmitting.value = true;

  try {
    console.log('📤 Turning in draft submission:', draftSubmission.value.id);

    // Update the draft to final submission with caption
    const response = await axios.put(
      `/api/submissions/${draftSubmission.value.id}/`,
      {
        status: 'unscored',
        is_draft: false,
        caption: submissionCaption.value || draftSubmission.value.caption,
        post_to_feed: postToFeed.value
      }
    );

    console.log('✅ Submission turned in successfully:', response.data);
    
    // Show success message
    showSuccess('Work submitted successfully!', 'Submitted');

    // Update state
    hasSubmittedWork.value = true;
    existingSubmission.value = response.data;
    draftSubmission.value = null;
    submissionCaption.value = '';
    postToFeed.value = false;
    showTurnInDialog.value = false;

    // Keep draftFiles empty since we'll show submitted files instead
    draftFiles.value = [];

    // Reload submissions to populate studentSubmissions array
    await loadActivitySubmissions(selectedActivity.value.id);
    
    // Also reload to update the submission status
    await checkSubmissionStatus(selectedActivity.value.id);
    
    console.log('📊 After turn in - State:', {
      hasSubmittedWork: hasSubmittedWork.value,
      studentSubmissions: studentSubmissions.value.length,
      existingSubmission: existingSubmission.value
    });
  } catch (error) {
    console.error('❌ Error turning in submission:', error);
    showError(
      error.response?.data?.error || 'Failed to submit work',
      'Submit Failed'
    );
  } finally {
    isSubmitting.value = false;
  }
};

// Handle resubmission
const handleResubmit = async () => {
  if (!selectedActivity.value || studentSubmissions.value.length === 0) return;
  
  try {
    console.log('🔄 Starting resubmission process...');
    
    // Get the existing submission
    const existingSubmissionData = studentSubmissions.value[0];
    const submissionId = existingSubmissionData.activityId || existingSubmissionData.id;
    
    // Find the actual submission ID from backend
    const submissionsResponse = await axios.get(`/api/activities/${selectedActivity.value.id}/submissions/`);
    const actualSubmission = submissionsResponse.data.find(sub => sub.status !== 'draft');
    
    if (!actualSubmission) {
      showError('No submission found to resubmit', 'Error');
      return;
    }
    
    console.log('📝 Converting submission to draft:', actualSubmission.id);
    console.log('📊 Current resubmit count:', actualSubmission.resubmit_count || 0);
    
    // Convert submission back to draft status
    const response = await axios.put(`/api/submissions/${actualSubmission.id}/`, {
      status: 'draft'
    });
    
    console.log('✅ Converted to draft:', response.data);
    
    // Update state - now it's a draft again
    hasSubmittedWork.value = false;
    existingSubmission.value = null;
    studentSubmissions.value = [];
    
    // Set as draft submission with the file
    draftSubmission.value = response.data;
    
    // Load the file into draftFiles so it can be viewed/removed
    const filePath = response.data.file_url || response.data.file_path || response.data.file;
    draftFiles.value = [{
      id: response.data.id,
      name: response.data.caption || 'Submitted file',
      type: response.data.file_type,
      path: filePath
    }];
    
    console.log('✅ Draft file loaded:', draftFiles.value);
    
    // Show resubmit count info
    const resubmitCount = response.data.resubmit_count || 0;
    const maxResubmits = 3;
    const remaining = maxResubmits - resubmitCount;
    
    showSuccess(
      `You can now edit and resubmit your work. Resubmits remaining: ${remaining}/${maxResubmits}`, 
      'Ready to Resubmit'
    );
  } catch (error) {
    console.error('❌ Error preparing resubmission:', error);
    
    // Handle specific error responses
    if (error.response && error.response.data) {
      const errorData = error.response.data;
      
      if (errorData.reason === 'already_scored') {
        showError('Cannot resubmit work that has already been scored by your teacher', 'Resubmit Not Allowed');
      } else if (errorData.reason === 'max_limit_reached') {
        showError(
          `You have reached the maximum resubmit limit (${errorData.max_resubmits} times). No more resubmissions allowed.`,
          'Resubmit Limit Reached'
        );
      } else {
        showError(errorData.error || 'Failed to prepare resubmission', 'Error');
      }
    } else {
      showError('Failed to prepare resubmission', 'Error');
    }
  }
};

// Request to post existing submission to feed
const requestPostToFeed = async () => {
  if (!existingSubmission.value) {
    showError('No submission found', 'Error');
    return;
  }
  
  try {
    isRequestingPost.value = true;
    console.log('📢 Requesting to post submission to feed:', existingSubmission.value.id);
    
    // Update the submission to request posting to feed
    const response = await axios.put(`/api/submissions/${existingSubmission.value.id}/`, {
      post_to_feed: true
    });
    
    if (response.data) {
      console.log('✅ Post request sent:', response.data);
      
      // Update local state
      existingSubmission.value = response.data;
      
      // Update the submission in the list
      const submissionIndex = studentSubmissions.value.findIndex(s => s.id === response.data.id);
      if (submissionIndex !== -1) {
        studentSubmissions.value[submissionIndex] = {
          ...studentSubmissions.value[submissionIndex],
          post_to_feed: true,
          approval_status: response.data.approval_status
        };
      }
      
      showSuccess(
        'Your post request has been sent to your teacher for approval!',
        'Request Sent'
      );
    }
  } catch (error) {
    console.error('❌ Error requesting post to feed:', error);
    showError(
      error.response?.data?.error || 'Failed to send post request',
      'Request Failed'
    );
  } finally {
    isRequestingPost.value = false;
  }
};

// Confirm remove file
const confirmRemoveFile = (file) => {
  fileToRemove.value = file;
  showRemoveConfirmDialog.value = true;
};

// Remove draft file
const removeDraftFile = async () => {
  if (!fileToRemove.value) return;
  
  try {
    console.log('🗑️ Removing draft file:', fileToRemove.value.id);
    await axios.delete(`/api/submissions/${fileToRemove.value.id}/`);
    
    // Remove from local state
    draftFiles.value = draftFiles.value.filter(f => f.id !== fileToRemove.value.id);
    if (draftFiles.value.length === 0) {
      draftSubmission.value = null;
    }
    
    showSuccess('File removed', 'Removed');
    console.log('✅ File removed successfully');
    
    // Close dialog and reset
    showRemoveConfirmDialog.value = false;
    fileToRemove.value = null;
  } catch (error) {
    console.error('❌ Error removing file:', error);
    const errorMsg = error.response?.data?.error || 'Failed to remove file';
    showError(errorMsg, 'Error');
  }
};

// View draft file
const viewDraftFile = async (file) => {
  try {
    // Fetch the full submission data to get the file path
    const response = await axios.get(`/api/submissions/${file.id}/`);
    console.log('📥 Loaded submission data:', response.data);
    
    // Use file_url from backend (already formatted correctly)
    let filePath = response.data.file_url || response.data.file_path || response.data.file;
    
    previewFile.value = {
      ...file,
      path: filePath,
      fullData: response.data
    };
    showFilePreview.value = true;
    console.log('👁️ Viewing file:', previewFile.value);
    console.log('📎 Preview path:', filePath);
  } catch (error) {
    console.error('❌ Error loading file:', error);
    showError('Failed to load file preview', 'Error');
  }
};


// Archive the current class
const confirmArchive = () => {
  // TODO: Implement actual archive functionality
  console.log('Archiving class:', props.className);

  // Show success message
  // In a real app, you would make an API call here
  showSuccess('Class archived successfully!', 'Archived');

  // Close the dialog
  showArchiveDialog.value = false;

  // Optionally redirect to the archived classes page
  // You can implement navigation here if needed
};

// Envelope designer colors
const envelopeColors = [
  { name: 'Indigo', value: '#4F46E5' },
  { name: 'Purple', value: '#9333EA' },
  { name: 'Blue', value: '#3B82F6' },
  { name: 'Teal', value: '#14B8A6' },
  { name: 'Green', value: '#10B981' },
  { name: 'Red', value: '#EF4444' },
  { name: 'Orange', value: '#F97316' },
  { name: 'Pink', value: '#EC4899' },
  { name: 'Gray', value: '#6B7280' },
  { name: 'Navy', value: '#1E3A8A' }
];

// Envelope patterns
const envelopePatterns = [
  { name: 'Solid', value: 'solid' },
  { name: 'Dots', value: 'dots' },
  { name: 'Lines', value: 'lines' },
  { name: 'Grid', value: 'grid' }
];

// Start portfolio compilation - show envelope designer
const startPortfolioCompilation = () => {
  // Initialize with current user data
  envelopeDesign.value.studentName = currentUser.value.name;
  envelopeDesign.value.className = props.className;
  
  // Show the envelope designer
  showEnvelopeDesigner.value = true;
};

// Helper function to adjust color brightness
const adjustBrightness = (color, percent) => {
  const num = parseInt(color.replace('#', ''), 16);
  const amt = Math.round(2.55 * percent);
  const R = (num >> 16) + amt;
  const G = (num >> 8 & 0x00FF) + amt;
  const B = (num & 0x0000FF) + amt;
  return '#' + (
    0x1000000 +
    (R < 255 ? (R < 1 ? 0 : R) : 255) * 0x10000 +
    (G < 255 ? (G < 1 ? 0 : G) : 255) * 0x100 +
    (B < 255 ? (B < 1 ? 0 : B) : 255)
  ).toString(16).slice(1);
};

// Show confirmation dialog
const showConfirmEnvelopeDialog = () => {
  // Validate required fields
  if (!envelopeDesign.value.title || !envelopeDesign.value.studentName) {
    showWarning('Please fill in all required fields (Title and Student Name)', 'Missing Information');
    return;
  }
  
  // Show confirmation dialog
  showEnvelopeConfirmDialog.value = true;
};

// Confirm and save envelope design
const confirmSaveEnvelope = async () => {
  console.log('Saving envelope design:', envelopeDesign.value);
  
  try {
    // Save to backend
    const response = await axios.post('/api/portfolio-envelope/create/', {
      title: envelopeDesign.value.title,
      student_name: envelopeDesign.value.studentName,
      class_name: envelopeDesign.value.className || props.className,
      color: envelopeDesign.value.color,
      pattern: envelopeDesign.value.pattern
    });
    
    console.log('✅ Portfolio envelope created:', response.data);
    
    // Mark envelope as created and close dialogs
    portfolioEnvelopeCreated.value = true;
    showEnvelopeConfirmDialog.value = false;
    showEnvelopeDesigner.value = false;
    
    showSuccess('Portfolio envelope created successfully!', 'Envelope Created');
  } catch (error) {
    console.error('❌ Error creating portfolio envelope:', error);
    showError(error.response?.data?.error || error.message, 'Failed to Create Envelope');
  }
};

// Edit envelope design
const editEnvelopeDesign = async () => {
  try {
    // Fetch existing envelope data
    const classNameValue = props.className;
    const response = await axios.get(`/api/portfolio-envelope/student/${encodeURIComponent(classNameValue)}/`);
    
    if (response.data && response.data.envelope) {
      // Load existing envelope data into the designer
      envelopeDesign.value = {
        title: response.data.envelope.title,
        studentName: response.data.envelope.student_name,
        className: response.data.envelope.class_name,
        color: response.data.envelope.color,
        pattern: response.data.envelope.pattern
      };
      console.log('✅ Loaded existing envelope data for editing');
    }
  } catch (error) {
    console.error('❌ Error loading envelope data:', error);
    // If no envelope found, use default values
    envelopeDesign.value.studentName = currentUser.value.name;
    envelopeDesign.value.className = props.className;
  }
  
  showEnvelopeDesigner.value = true;
};

// Toggle envelope open/close
const toggleEnvelope = async () => {
  isEnvelopeOpen.value = !isEnvelopeOpen.value;
  console.log('Envelope toggled:', isEnvelopeOpen.value ? 'opened' : 'closed');
  
  // Fetch activities when envelope is opened
  if (isEnvelopeOpen.value && portfolioActivities.value.length === 0) {
    await fetchPortfolioActivities();
  }
};

// Fetch portfolio activities
const fetchPortfolioActivities = async () => {
  try {
    const classNameValue = props.className;
    const response = await axios.get(`/api/portfolio-envelope/activities/${encodeURIComponent(classNameValue)}/`);
    
    if (response.data) {
      portfolioActivities.value = response.data.all_activities || [];
      missingActivities.value = response.data.missing_activities || [];
      currentActivityIndex.value = 0;
      console.log(`✅ Loaded ${portfolioActivities.value.length} activities (${missingActivities.value.length} missing)`);
      console.log('📋 Activities data:', portfolioActivities.value);
      console.log('🎯 Current activity:', portfolioActivities.value[currentActivityIndex.value]);
    }
  } catch (error) {
    console.error('❌ Error fetching portfolio activities:', error);
  }
};

// Navigate activities
const nextActivity = () => {
  console.log('Next clicked. Current:', currentActivityIndex.value, 'Total:', portfolioActivities.value.length);
  if (currentActivityIndex.value < portfolioActivities.value.length - 1) {
    currentActivityIndex.value++;
    console.log('Moved to:', currentActivityIndex.value);
  } else {
    console.log('Already at last activity');
  }
};

const previousActivity = () => {
  console.log('Previous clicked. Current:', currentActivityIndex.value);
  if (currentActivityIndex.value > 0) {
    currentActivityIndex.value--;
    console.log('Moved to:', currentActivityIndex.value);
  } else {
    console.log('Already at first activity');
  }
};

// Submit portfolio
const confirmSubmitPortfolio = async () => {
  try {
    isSubmittingPortfolio.value = true;
    const classNameValue = props.className;
    
    console.log('📤 Submitting portfolio for class:', classNameValue);
    
    const response = await axios.post(`/api/portfolio-envelope/submit/${encodeURIComponent(classNameValue)}/`);
    
    if (response.data.success) {
      console.log('✅ Portfolio submitted successfully');
      
      // Update the envelope data to reflect submission
      if (portfolioEnvelope.value) {
        portfolioEnvelope.value.is_submitted = true;
        portfolioEnvelope.value.submitted_at = response.data.submitted_at;
      }
      
      // Close dialog
      showSubmitPortfolioDialog.value = false;
      
      // Show success message
      showSuccess(`Submitted on: ${response.data.submitted_date} at ${response.data.submitted_time}`, 'Portfolio Submitted');
    }
  } catch (error) {
    console.error('❌ Error submitting portfolio:', error);
    const errorMessage = error.response?.data?.error || error.message || 'Failed to submit portfolio';
    showError(errorMessage, 'Submission Failed');
  } finally {
    isSubmittingPortfolio.value = false;
  }
};

// Show missing activities dialog
const showMissingActivities = () => {
  showMissingActivitiesDialog.value = true;
};

// Compile missing activity
const compileActivity = (activity) => {
  console.log('Compiling activity:', activity.title);
  // Close the missing activities dialog
  showMissingActivitiesDialog.value = false;
  // Set the selected activity and open submission dialog
  selectedActivity.value = activity;
  showProductUploadModal.value = true;
  selectedFile.value = null;
  newProductCaption.value = '';
  postOutputOption.value = false;
  isCompilingMissing.value = true; // Flag to indicate this is a missing activity submission
};

// Submit missing activity from portfolio compilation
const submitMissingActivity = async () => {
  if (isSubmitting.value) {
    console.log('Already submitting, please wait...');
    return;
  }

  if (!selectedFile.value || !selectedActivity.value) {
    showWarning('Please select a file', 'No File Selected');
    return;
  }

  isSubmitting.value = true;

  try {
    // Convert file to base64
    const reader = new FileReader();
    const filePath = await new Promise((resolve, reject) => {
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = reject;
      reader.readAsDataURL(selectedFile.value);
    });

    console.log('Submitting missing activity:', selectedActivity.value.id);

    // Submit to missing activity API
    const response = await axios.post(
      `/api/portfolio-envelope/submit-missing/${selectedActivity.value.id}/`,
      {
        file: filePath,
        caption: newProductCaption.value || ''
      }
    );

    if (response.data) {
      console.log('✅ Missing activity submitted successfully:', response.data);

      // Close dialog and reset
      showProductUploadModal.value = false;
      newProductCaption.value = '';
      postOutputOption.value = false;
      isCompilingMissing.value = false;
      clearFile();

      // Refresh activities to update status
      await fetchPortfolioActivities();

      showSuccess('Your teacher will review it.', 'Activity Submitted');
    }
  } catch (error) {
    console.error('❌ Error submitting missing activity:', error);
    showError(error.response?.data?.error || 'Failed to submit activity. Please try again.', 'Submission Failed');
  } finally {
    isSubmitting.value = false;
  }
};

// Check if student has existing envelope
const checkExistingEnvelope = async () => {
  try {
    const classNameValue = props.className;
    const response = await axios.get(`/api/portfolio-envelope/student/${encodeURIComponent(classNameValue)}/`);
    
    if (response.data && response.data.envelope) {
      // Store full envelope data including submission status
      portfolioEnvelope.value = response.data.envelope;
      
      // Load existing envelope data for design
      envelopeDesign.value = {
        title: response.data.envelope.title,
        studentName: response.data.envelope.student_name,
        className: response.data.envelope.class_name,
        color: response.data.envelope.color,
        pattern: response.data.envelope.pattern
      };
      portfolioEnvelopeCreated.value = true;
      
      if (response.data.envelope.is_submitted) {
        console.log('✅ Existing envelope found (Already Submitted)');
      } else {
        console.log('✅ Existing envelope found (Not Yet Submitted)');
      }
    } else {
      portfolioEnvelopeCreated.value = false;
      portfolioEnvelope.value = null;
    }
  } catch (error) {
    console.log('ℹ️ No existing envelope found:', error.response?.status);
    portfolioEnvelopeCreated.value = false;
    portfolioEnvelope.value = null;
  }
};

// Submit new product
const submitNewProduct = async () => {
  // Prevent multiple submissions
  if (isSubmitting.value) {
    console.log('Already submitting, please wait...');
    return;
  }

  if (!selectedFile.value || !selectedActivity.value) {
    showWarning('Please select a file and activity', 'Missing Selection');
    return;
  }

  isSubmitting.value = true;

  try {
    // Get file type
    const fileType = selectedFile.value.type.startsWith('image/') ? 'image' : 
                     selectedFile.value.type.includes('pdf') ? 'pdf' : 'document';

    // Convert file to base64 for storage
    let filePath = '';
    if (fileType === 'image' && previewUrl.value) {
      // Use existing preview URL (already base64)
      filePath = previewUrl.value;
    } else {
      // Convert file to base64
      const reader = new FileReader();
      filePath = await new Promise((resolve, reject) => {
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = reject;
        reader.readAsDataURL(selectedFile.value);
      });
    }

    console.log('Submitting work for activity:', selectedActivity.value);
    console.log('File path length:', filePath?.length);
    console.log('File type:', fileType);

    // Check if submission is late
    const isLateSubmission = isPastDue.value;

    // Submit to API
    const response = await axios.post(`/api/activities/${selectedActivity.value.id}/submissions/`, {
      caption: newProductCaption.value,
      file_path: filePath,
      file_type: fileType,
      post_to_feed: postOutputOption.value,
      is_late: isLateSubmission
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
        is_late: response.data.is_late || false,  // Use backend's determination
        loadError: false
      };

      studentSubmissions.value.push(newSubmission);

      // Close modal and reset form
      showProductUploadModal.value = false;
      newProductCaption.value = '';
      postOutputOption.value = false;
      clearFile();

      showSuccess('Work submitted successfully!', 'Submitted');
    }
  } catch (error) {
    console.error('Error submitting work:', error);
    showError(error.response?.data?.error || error.message, 'Submission Failed');
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

/* Portfolio Activity Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes gradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes patternFloat {
  0%, 100% {
    transform: translateY(0) translateX(0);
  }
  50% {
    transform: translateY(-10px) translateX(5px);
  }
}

@keyframes patternSlide {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 40px 40px;
  }
}

@keyframes patternPulse {
  0%, 100% {
    opacity: 0.1;
  }
  50% {
    opacity: 0.15;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) translateX(0);
    opacity: 0.2;
  }
  50% {
    transform: translateY(-100px) translateX(50px);
    opacity: 0.4;
  }
}

.animate-fadeIn {
  animation: fadeIn 0.6s ease-out;
}

.animate-slideDown {
  animation: slideDown 0.5s ease-out;
}

.animate-scaleIn {
  animation: scaleIn 0.5s ease-out;
}

.animate-patternFloat {
  animation: patternFloat 6s ease-in-out infinite;
}

.animate-patternSlide {
  animation: patternSlide 20s linear infinite;
}

.animate-patternPulse {
  animation: patternPulse 3s ease-in-out infinite;
}

.animate-float {
  animation: float linear infinite;
}

@keyframes sparkle {
  0%, 100% {
    opacity: 0;
    transform: scale(0) rotate(0deg);
  }
  50% {
    opacity: 1;
    transform: scale(1.5) rotate(180deg);
  }
}

@keyframes pulse-slow {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

@keyframes glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
  }
  50% {
    box-shadow: 0 0 40px rgba(255, 255, 255, 0.6);
  }
}

.animate-sparkle {
  animation: sparkle linear infinite;
}

.animate-pulse-slow {
  animation: pulse-slow 3s ease-in-out infinite;
}

.animate-shimmer {
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  background-size: 1000px 100%;
  animation: shimmer 3s infinite;
}

.animate-glow {
  animation: glow 2s ease-in-out infinite;
}

/* Enhanced hover effects */
.hover-lift {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.hover-lift:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

/* Glass morphism enhanced */
.glass-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
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
