        <template>
  <div class="flex flex-col">
    <!-- Class Header -->
    <div class="bg-white p-4 md:p-3 shadow-lg rounded-t-xl border-b border-gray-200">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div class="space-y-2">
          <h1 class="text-xl md:text-2xl font-bold text-gray-900 px-4 py-2 md:px-5 md:py-2 rounded-lg inline-block bg-gray-100">
            {{ actualClassName }}
          </h1>
          <p class="text-gray-600 ml-2 flex items-center gap-2 text-sm">
            <i class="pi pi-user"></i>
            Student: {{ currentUser.name }}
          </p>
        </div>

      </div>

      <!-- Navigation Tabs -->
      <div class="flex flex-wrap gap-2 md:gap-4 mt-3 md:mt-4">
        <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id" class="flex items-center gap-2 text-gray-600 px-4 py-2 md:px-5 md:py-2.5 rounded-lg transition-all duration-300 relative overflow-hidden group" :class="[activeTab === tab.id ? 'font-semibold text-indigo-700 bg-indigo-50' : 'hover:text-indigo-600 hover:bg-gray-50']">
          <span class="relative z-10 flex items-center gap-2">
            <i :class="['pi', tab.icon]"></i>
            <span>{{ tab.name }}</span>
          </span>
          <span v-if="activeTab === tab.id" class="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-600 rounded-full"></span>
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="w-full bg-white/80 flex-1">
      <!-- Content Area -->
      <div class="w-full px-4 sm:px-6 pt-1 pb-8 transition-all duration-300"
           :style="{ 'padding-left': '1.5rem', 'padding-right': '1.5rem' }">
        <template v-if="activeTab === 'portfolio'">
          <div v-if="!portfolioCreated" class="p-8 bg-white rounded-xl shadow-sm">
            <div class="flex flex-col items-center justify-center text-center max-w-md mx-auto">
            </div>
          </div>
          <div v-else class="p-4 md:p-6 bg-white rounded-xl shadow-sm min-h-screen">
            <!-- Portfolio Content -->
            <div>
              <!-- Activities List View -->
              <div v-if="selectedFolder" class="space-y-6">
                <!-- Header Title (Top) -->
                <div class="mb-4">
                  <h2 class="text-2xl font-bold text-indigo-900">
                    {{ showSubmittedCollection ? 'Submitted Collection Activity' : `List of Activities - ${selectedFolder?.title || 'Activities'}` }}
                  </h2>
                </div>

                <!-- Combined Header with Back Button on Left -->
                <div class="flex flex-col sm:flex-row justify-start sm:items-center gap-4 mb-4">
                  <!-- Back Button (Left Side) -->
                  <div class="flex flex-wrap gap-2 order-first">
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

                  <!-- Action Buttons (Right Side) -->
                  <div class="flex flex-wrap gap-2 ml-auto">
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
                  </div>
                </div>

                <!-- Activity Detail View -->
                <div v-if="selectedActivity" class="bg-white rounded-xl shadow-lg p-6 mb-6 border border-indigo-100">
                  <!-- Top Section: Activity Header Card -->
                  <div class="bg-white shadow-sm border-b border-gray-200 mb-4">
                    <!-- Content Area -->
                    <div class="p-4">
                      <div class="flex flex-col lg:flex-row gap-6">
                        <!-- Left: Activity Info -->
                        <div class="flex-1 flex flex-col gap-4">
                          <div class="flex flex-col gap-2">
                            <p class="text-sm text-black">
                              <span class="font-bold">Activity Title:</span> {{ selectedActivity.title }}
                            </p>
                            <p class="text-sm text-black">
                              <span class="font-bold">Activity Type:</span> <span class="capitalize">{{ selectedActivity.type || 'Not specified' }}</span>
                            </p>
                            <p class="text-sm text-black">
                              <span class="font-bold">Due date & time:</span> {{ selectedActivity.date || 'No due date set' }}<span v-if="selectedActivity.formattedTime"> at {{ selectedActivity.formattedTime }}</span>
                            </p>
                          </div>
                          <div class="flex flex-col gap-2">
                            <div class="flex items-center justify-between flex-wrap gap-2">
                              <div class="flex items-center gap-2 flex-wrap">
                                <p class="text-sm text-black">
                                  <span class="font-bold">Instruction:</span>
                                </p>
                                <!-- Attached Files next to Instruction label -->
                                <div v-if="selectedActivity.instruction_files && selectedActivity.instruction_files.length > 0" class="flex items-center gap-1 flex-wrap">
                                  <a 
                                    v-for="file in selectedActivity.instruction_files.slice(0, 2)" 
                                    :key="file.id"
                                    :href="file.file_url"
                                    target="_blank"
                                    class="flex items-center gap-1 px-2 py-1 bg-indigo-50 border border-indigo-200 rounded-lg text-xs hover:bg-indigo-100 transition-colors"
                                  >
                                    <i class="pi pi-file text-indigo-600"></i>
                                    <span class="text-indigo-700 max-w-[100px] truncate">{{ file.file_name }}</span>
                                  </a>
                                  <span 
                                    v-if="selectedActivity.instruction_files.length > 2"
                                    class="flex items-center px-2 py-1 bg-gray-100 border border-gray-200 rounded-lg text-xs text-gray-600"
                                  >
                                    +{{ selectedActivity.instruction_files.length - 2 }} more
                                  </span>
                                </div>
                              </div>
                              <button 
                                @click="showAllInstructionFilesDialog = true"
                                class="flex items-center gap-1 px-2 py-1 text-xs text-indigo-600 hover:text-indigo-800 hover:bg-indigo-50 rounded transition-colors"
                                title="Expand instruction"
                              >
                                <i class="pi pi-expand text-xs"></i>
                                <span>Expand</span>
                              </button>
                            </div>
                            <div class="text-sm text-black whitespace-pre-wrap break-words max-h-40 overflow-y-auto bg-gray-50 p-3 rounded-lg border border-gray-200">
                              <span v-if="selectedActivity.description">{{ selectedActivity.description }}</span>
                              <span v-else class="text-gray-500 italic">No instructions provided</span>
                            </div>
                          </div>
                        </div>

                        <!-- Right: Your Work Card -->
                        <div class="lg:col-span-1">
                          <div class="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl border-2 border-indigo-200 p-4 w-96 h-auto">
                            <!-- Header -->
                            <div class="mb-4">
                              <div class="flex items-center justify-between mb-3">
                                <div class="flex items-center gap-2">
                                  <div class="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
                                    <i class="pi pi-briefcase text-white text-sm"></i>
                                  </div>
                                  <div>
                                    <h3 class="text-base font-bold text-gray-800">Your Work</h3>
                                    <span v-if="draftFiles.length > 0 && (!hasSubmittedWork || isResubmitting)" class="text-xs text-gray-500">
                                      {{ draftFiles.length }} file{{ draftFiles.length > 1 ? 's' : '' }} attached
                                    </span>
                                  </div>
                                </div>

                                <!-- Status Badge (Main Design) -->
                                <div class="flex flex-col items-end gap-1">
                                  <!-- Resubmitting: In resubmission mode (takes priority) -->
                                  <span
                                    v-if="isResubmitting"
                                    class="px-3 py-1.5 rounded-lg bg-orange-100 text-orange-800 flex items-center gap-1.5 text-xs font-medium"
                                  >
                                    <i class="pi pi-refresh text-xs"></i>
                                    <span>Resubmitting</span>
                                  </span>
                                  <!-- Resubmitted: Has been resubmitted -->
                                  <span
                                    v-else-if="hasSubmittedWork && existingSubmission?.resubmit_count > 0"
                                    class="px-3 py-1.5 rounded-lg bg-blue-100 text-blue-800 flex items-center gap-1.5 text-xs font-medium"
                                  >
                                    <i class="pi pi-refresh text-xs"></i>
                                    <span>Resubmitted</span>
                                    <span class="text-xs">({{ existingSubmission.resubmit_count }}x)</span>
                                  </span>
                                  <!-- Submitted Late: Was missing but then turned in -->
                                  <span
                                    v-else-if="hasSubmittedWork && existingSubmission?.is_late"
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
                            </div>

                            <!-- Files Display (Draft or Submitted) -->
                            <div v-if="draftFiles.length > 0 || (hasSubmittedWork && studentSubmissions.length > 0)" class="mb-3 space-y-2 max-h-48 overflow-y-auto">
                          <!-- Show draft files if not submitted OR in resubmission mode -->
                          <div
                            v-if="!hasSubmittedWork || isResubmitting"
                            v-for="file in draftFiles"
                            :key="`${file.id}-${file.path}`"
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
                                :key="file.path"
                                :src="file.path"
                                :alt="file.name"
                                class="w-full h-full object-cover"
                                @load="() => console.log('✅ Image loaded successfully:', file.path)"
                                @error="(e) => { console.error('❌ Image load error:', file.path); e.target.style.display = 'none'; e.target.nextElementSibling.style.display = 'flex'; }"
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

                          <!-- Show submitted files (clickable for preview) - only when NOT in resubmission mode -->
                          <button
                            v-else-if="hasSubmittedWork && !isResubmitting && studentSubmissions.length > 0"
                            v-for="submission in studentSubmissions"
                            :key="submission.activityId"
                            @click="viewDraftFile(submission)"
                            class="flex items-center gap-2 p-2 bg-white rounded-lg border border-indigo-200 hover:border-indigo-300 transition-all group w-full text-left"
                          >
                            <!-- Thumbnail (Clickable) -->
                            <div
                              class="w-10 h-10 rounded-md flex items-center justify-center flex-shrink-0 overflow-hidden hover:opacity-80 transition-opacity"
                              :class="submission.isImage ? 'bg-gray-100' : 'bg-indigo-100'"
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
                                <i v-if="submission.isImage" class="pi pi-image text-indigo-600 text-lg"></i>
                                <i v-else class="pi pi-file text-gray-600 text-lg"></i>
                              </div>
                            </div>

                            <!-- File Info (Clickable) -->
                            <div class="flex-1 min-w-0">
                              <p class="text-xs font-medium text-gray-900 truncate">{{ submission.caption || 'Submitted work' }}</p>
                              <p class="text-xs text-gray-500">Submitted</p>
                            </div>

                            <!-- View Icon (Submitted) -->
                            <div class="w-6 h-6 flex items-center justify-center">
                              <i class="pi pi-eye text-indigo-600 text-sm"></i>
                            </div>
                          </button>
                        </div>

                        <!-- Action Buttons (Always visible) -->
                        <div class="space-y-2">
                          <!-- Hidden File Input - Multiple files -->
                          <input
                            type="file"
                            ref="autoSaveFileInput"
                            @change="handleAutoSaveFileUpload"
                            accept="image/*,.pdf,.doc,.docx"
                            multiple
                            class="hidden"
                          />

                          <!-- Add/Upload Button (Show if not submitted OR in resubmission mode) -->
                          <button
                            v-if="!hasSubmittedWork || isResubmitting"
                            @click="isReplacingFile = false; showUploadDialog = true"
                            :disabled="isSubmitting"
                            class="w-full px-4 py-2 bg-white border-2 border-indigo-200 rounded-lg text-indigo-600 text-sm font-semibold hover:bg-indigo-50 hover:border-indigo-300 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            <i v-if="isSubmitting" class="pi pi-spin pi-spinner"></i>
                            <i v-else-if="draftFiles.length > 0" class="pi pi-plus-circle"></i>
                            <i v-else class="pi pi-plus"></i>
                            <span v-if="isSubmitting">Uploading...</span>
                            <span v-else-if="draftFiles.length > 0">Add More Files</span>
                            <span v-else>Upload Files</span>
                          </button>

                          <!-- Turn In Button (Show if not submitted OR in resubmission mode) -->
                          <button
                            v-if="!hasSubmittedWork || isResubmitting"
                            @click="openTurnInDialog"
                            :disabled="draftFiles.length === 0"
                            class="w-full px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg text-sm font-semibold hover:from-indigo-700 hover:to-purple-700 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            <i class="pi pi-check-circle"></i>
                            <span>Turn in</span>
                          </button>

                          <!-- Resubmit Button (Show when already submitted AND NOT in resubmission mode) -->
                          <div v-else-if="hasSubmittedWork && !isResubmitting" class="space-y-2">
                            <!-- Resubmit Counter Info -->
                            <div v-if="existingSubmission && existingSubmission.resubmit_count > 0" class="text-xs text-center">
                              <span class="px-2 py-1 bg-orange-100 text-orange-700 rounded-full">
                                Resubmitted {{ existingSubmission.resubmit_count }} time{{ existingSubmission.resubmit_count > 1 ? 's' : '' }}
                              </span>
                            </div>

                            <button
                              @click="handleResubmit"
                              :disabled="hasScore || (existingSubmission && existingSubmission.resubmit_count >= 3)"
                              class="w-full px-4 py-2 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg text-sm font-semibold hover:from-orange-600 hover:to-orange-700 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:from-orange-500 disabled:hover:to-orange-600"
                              :title="hasScore ? 'Cannot resubmit - Already scored' : (existingSubmission && existingSubmission.resubmit_count >= 3) ? 'Maximum resubmit limit reached (3x)' : 'Resubmit your work'"
                            >
                              <i class="pi pi-refresh"></i>
                              <span>{{ hasScore ? 'Already Scored' : (existingSubmission && existingSubmission.resubmit_count >= 3) ? 'Max Limit Reached' : 'Resubmit' }}</span>
                            </button>

                            <!-- Post to Feed Button -->
                            <button
                              v-if="existingSubmission && !existingSubmission.post_to_feed"
                              @click="openPostToFeedDialog"
                              :disabled="isRequestingPost"
                              class="w-full px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-lg text-sm font-semibold hover:from-blue-600 hover:to-indigo-700 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                              title="Request to post this work to class feed"
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
                      <!-- Load More Button for Submitted -->
                      <div v-if="displayedSubmittedCount < folderActivities.filter(a => getActivityStatus(a) === 'submitted' || getActivityStatus(a) === 'resubmitted').length" class="p-4 text-center border-t border-gray-200 bg-gray-50">
                        <button @click="displayedSubmittedCount += itemsPerPage" class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors duration-200 flex items-center gap-2 mx-auto">
                          <i class="pi pi-chevron-down"></i>
                          <span>Load More ({{ folderActivities.filter(a => getActivityStatus(a) === 'submitted' || getActivityStatus(a) === 'resubmitted').length - displayedSubmittedCount }} more)</span>
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Scoring Criteria Section (2-Column Layout with Max 2 Rows) -->
                  <div v-if="!hasScore" class="mb-6">
                    <div v-if="selectedActivity.scoringCriteria && selectedActivity.scoringCriteria.length > 0" class="bg-white rounded-lg p-4 border border-gray-200">
                      <h3 class="text-sm font-bold text-gray-900">Scoring Criteria:</h3>
                      <div class="grid grid-cols-2 gap-3 max-h-40 overflow-y-auto">
                        <div
                          v-for="(criterion, index) in selectedActivity.scoringCriteria"
                          :key="index"
                          class="p-3 bg-gray-50 rounded-lg border border-gray-200"
                        >
                          <p class="text-xs font-semibold text-gray-700 truncate">{{ criterion.name }}</p>
                          <p class="text-xs text-gray-600 mt-1">{{ criterion.maxScore }} pts</p>
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
                    <div class="flex items-center justify-between mb-4">
                      <h3 class="text-lg font-semibold text-gray-900">Your Submissions:</h3>
                      <span class="text-sm text-gray-500">{{ currentSubmissionIndex + 1 }} / {{ studentSubmissions.length }}</span>
                    </div>

                    <!-- Submission Carousel -->
                    <div class="relative">
                      <!-- Navigation Arrows -->
                      <button 
                        v-if="studentSubmissions.length > 1"
                        @click="prevSubmission"
                        :disabled="currentSubmissionIndex === 0"
                        class="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-4 z-10 w-10 h-10 rounded-full bg-white shadow-lg flex items-center justify-center hover:bg-gray-50 transition-colors border border-gray-200"
                        :class="{ 'opacity-50 cursor-not-allowed': currentSubmissionIndex === 0 }">
                        <i class="pi pi-chevron-left text-gray-600"></i>
                      </button>

                      <button 
                        v-if="studentSubmissions.length > 1"
                        @click="nextSubmission"
                        :disabled="currentSubmissionIndex === studentSubmissions.length - 1"
                        class="absolute right-0 top-1/2 -translate-y-1/2 translate-x-4 z-10 w-10 h-10 rounded-full bg-white shadow-lg flex items-center justify-center hover:bg-gray-50 transition-colors border border-gray-200"
                        :class="{ 'opacity-50 cursor-not-allowed': currentSubmissionIndex === studentSubmissions.length - 1 }">
                        <i class="pi pi-chevron-right text-gray-600"></i>
                      </button>

                      <!-- Single Submission Card -->
                      <div class="bg-white rounded-lg border border-indigo-100 overflow-hidden shadow-sm max-w-2xl mx-auto">
                        <div class="aspect-video relative bg-gray-50 overflow-hidden flex items-center justify-center p-2">
                          <!-- Image Display -->
                          <img v-if="currentSubmission?.isImage && currentSubmission?.previewUrl"
                            :src="currentSubmission.previewUrl"
                            :alt="currentSubmission.caption || 'Submitted work'"
                            class="w-full h-full object-contain rounded-lg"
                            @error="handleImageError(currentSubmission)"
                            v-show="!currentSubmission.loadError"
                          />
                          <!-- PDF Display -->
                          <div v-else-if="!currentSubmission?.isImage && currentSubmission?.previewUrl" class="flex flex-col items-center justify-center text-red-600">
                            <i class="pi pi-file-pdf text-6xl mb-3"></i>
                            <span class="text-sm font-medium">Document</span>
                            <span class="text-xs text-gray-500 mt-1">{{ currentSubmission.caption || 'Untitled' }}</span>
                            <a 
                              :href="currentSubmission.previewUrl" 
                              target="_blank"
                              @click.stop
                              class="mt-3 px-4 py-2 bg-indigo-600 text-white text-sm rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2">
                              <i class="pi pi-external-link"></i>
                              Open PDF
                            </a>
                          </div>
                        </div>
                        <div class="p-4">
                          <p v-if="currentSubmission?.caption" class="text-sm text-gray-600 mb-2">{{ currentSubmission.caption }}</p>

                          <!-- Score Display -->
                          <div v-if="currentSubmission?.score !== null && currentSubmission?.score !== undefined" class="mb-2 p-2 bg-indigo-50 rounded-lg">
                            <div class="flex items-center justify-between">
                              <span class="text-sm font-medium text-indigo-900">Score:</span>
                              <span class="text-lg font-bold text-indigo-700">{{ currentSubmission.score }}</span>
                            </div>
                            <p v-if="currentSubmission?.feedback" class="text-xs text-gray-600 mt-1 italic">
                              "{{ currentSubmission.feedback }}"
                            </p>
                          </div>

                          <div class="flex justify-between items-center mt-2">
                            <div class="flex items-center gap-2">
                              <span class="text-xs text-gray-500">{{ currentSubmission?.date }}</span>
                            </div>
                            <span class="text-xs px-2 py-1 rounded"
                                  :class="currentSubmission?.status === 'scored' ? 'bg-green-100 text-green-800' :
                                         currentSubmission?.status === 'unscored' ? 'bg-yellow-100 text-yellow-800' :
                                         'bg-blue-100 text-blue-800'">
                              {{ currentSubmission?.status === 'scored' ? 'Scored' : currentSubmission?.status === 'unscored' ? 'Unscored' : currentSubmission?.status }}
                            </span>
                          </div>
                        </div>
                      </div>

                      <!-- Dot Indicators -->
                      <div v-if="studentSubmissions.length > 1" class="flex justify-center gap-2 mt-4">
                        <button 
                          v-for="(_, index) in studentSubmissions" 
                          :key="index"
                          @click="currentSubmissionIndex = index"
                          class="w-2.5 h-2.5 rounded-full transition-colors"
                          :class="index === currentSubmissionIndex ? 'bg-indigo-600' : 'bg-gray-300 hover:bg-gray-400'">
                        </button>
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
                      @click="isSelectMode ? toggleSubmissionSelection(item.id) : openPreviewDialog(item)"
                      @keydown.enter.prevent="isSelectMode ? toggleSubmissionSelection(item.id) : openPreviewDialog(item)"
                      @keydown.space.prevent="isSelectMode ? toggleSubmissionSelection(item.id) : openPreviewDialog(item)"
                      tabindex="0"
                      role="button"
                      :aria-pressed="isSelectMode ? selectedSubmissions.includes(item.id) : undefined"
                      class="rounded-xl border-2 transition-all duration-200 cursor-pointer"
                      :class="[
                        isSelectMode && selectedSubmissions.includes(item.id)
                          ? 'bg-indigo-50 border-indigo-600 shadow-md transform scale-[1.01]'
                          : 'bg-white border-gray-200 hover:border-indigo-400 hover:shadow-md hover:bg-indigo-50/10'
                      ]"
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
                            @error="(e) => { e.target.style.display = 'none'; e.target.parentElement.innerHTML = '<i class=\'pi pi-image text-3xl text-gray-400\'></i>'; }"
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
                            <div class="text-gray-900 font-bold whitespace-normal break-words">{{ item.activity_title }}</div>
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
                <div v-else class="space-y-6">
                  <!-- Loading State -->
                  <div v-if="isLoadingActivities" class="flex justify-center items-center py-12">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                  </div>

                  <!-- Empty State -->
                  <div v-else-if="folderActivities.length === 0" class="text-center py-12 bg-white/80 backdrop-blur-sm rounded-xl shadow-sm border border-indigo-100">
                    <i class="pi pi-inbox text-4xl text-gray-400 mb-4"></i>
                    <p class="text-gray-500">No activities available yet.</p>
                  </div>

                  <!-- Activities Sections -->
                  <template v-else>
                    <!-- Pending Outputs Section (Moved to top) -->
                    <div v-if="folderActivities.filter(a => getActivityStatus(a) === 'pending' || getActivityStatus(a) === 'missing').length > 0"
                         class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-6">
                      <!-- Section Header -->
                      <div class="bg-gray-50 border-b border-gray-200 px-6 py-4">
                        <div class="flex items-center justify-between">
                          <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-full bg-amber-100 flex items-center justify-center text-amber-600">
                              <i class="pi pi-clock text-lg"></i>
                            </div>
                            <div>
                              <h3 class="text-lg font-bold text-gray-800">Pending Outputs</h3>
                              <p class="text-sm text-gray-600">
                                {{ folderActivities.filter(a => getActivityStatus(a) === 'pending' || getActivityStatus(a) === 'missing').length }}
                                {{ folderActivities.filter(a => getActivityStatus(a) === 'pending' || getActivityStatus(a) === 'missing').length === 1 ? 'activity' : 'activities' }}
                              </p>
                            </div>
                          </div>
                          <span class="px-3 py-1 bg-amber-100 text-amber-800 text-xs font-medium rounded-full border border-amber-200 shadow-sm">
                            {{ folderActivities.filter(a => getActivityStatus(a) === 'pending' || getActivityStatus(a) === 'missing').length }} Pending
                          </span>
                        </div>
                      </div>
                    <!-- Modern Table Design -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                      <!-- Table Header -->
                      <div class="bg-gray-50 border-b border-gray-200">
                        <div class="grid grid-cols-12 gap-4 px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider items-center">
                          <div class="col-span-2 text-center">
                            <span>Activity ID#</span>
                          </div>
                          <div class="col-span-2 text-center">
                            <span>Activity Title</span>
                          </div>
                          <div class="col-span-2 text-center">
                            <span>Type</span>
                          </div>
                          <div class="col-span-2 text-center">
                            <span>Status</span>
                          </div>
                          <div class="col-span-2 text-center">
                            <span>Due Time</span>
                          </div>
                          <div class="col-span-2 text-center">
                            <span>Due Date</span>
                          </div>
                        </div>
                      </div>

                      <!-- Table Body - Pending/Missing Activities Only -->
                      <div class="divide-y divide-gray-200">
                        <div v-for="(activity, index) in folderActivities.filter(a => getActivityStatus(a) === 'pending' || getActivityStatus(a) === 'missing').slice(0, displayedPendingCount)" :key="activity.id"
                          class="group hover:bg-gray-50 transition-colors duration-150 cursor-pointer"
                          @click="openActivity(activity)">

                          <div class="grid grid-cols-12 gap-4 px-6 py-4 items-center">
                            <!-- Activity ID# -->
                            <div class="col-span-2 text-center">
                              <span class="text-sm text-gray-700 font-medium">{{ activity.id }}</span>
                            </div>

                            <!-- Title -->
                            <div class="col-span-2 text-center">
                              <span class="font-medium text-gray-900 whitespace-normal break-words" :title="activity.title">{{ activity.title }}</span>
                            </div>

                            <!-- Activity Type -->
                            <div class="col-span-2 text-center">
                              <span class="text-sm text-gray-700 capitalize font-medium">{{ activity.type }}</span>
                            </div>

                            <!-- Status Badge -->
                            <div class="col-span-2 text-center">
                              <span v-if="getActivityStatus(activity) === 'missing'"
                                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                <i class="pi pi-circle-fill text-[6px] mr-1.5 text-red-500"></i>
                                Missing
                              </span>
                              <span v-else
                                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                <i class="pi pi-circle-fill text-[6px] mr-1.5 text-blue-500"></i>
                                Pending
                              </span>
                            </div>

                            <!-- Due Time -->
                            <div class="col-span-2 text-center">
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
                    </div>
                    <!-- End Pending Outputs Section -->

                    <!-- Submitted Outputs Section -->
                    <div v-if="folderActivities.filter(a => getActivityStatus(a) === 'submitted' || getActivityStatus(a) === 'resubmitted').length > 0"
                         class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                      <!-- Section Header -->
                      <div class="bg-gray-50 border-b border-gray-200 px-6 py-4">
                        <div class="flex items-center justify-between">
                          <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center text-green-600">
                              <i class="pi pi-check-circle text-lg"></i>
                            </div>
                            <div>
                              <h3 class="text-lg font-bold text-gray-800">Submitted Outputs</h3>
                              <p class="text-sm text-gray-600">
                                {{ folderActivities.filter(a => getActivityStatus(a) === 'submitted' || getActivityStatus(a) === 'resubmitted').length }}
                                {{ folderActivities.filter(a => getActivityStatus(a) === 'submitted' || getActivityStatus(a) === 'resubmitted').length === 1 ? 'activity' : 'activities' }}
                              </p>
                            </div>
                          </div>
                          <span class="px-3 py-1 bg-emerald-100 text-emerald-800 text-xs font-medium rounded-full border border-emerald-200 shadow-sm">
                            {{ folderActivities.filter(a => getActivityStatus(a) === 'submitted' || getActivityStatus(a) === 'resubmitted').length }} Submitted
                          </span>
                        </div>
                      </div>
                    <!-- Modern Table Design -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                      <!-- Table Header -->
                      <div class="bg-gray-50 border-b border-gray-200">
                        <div class="grid grid-cols-12 gap-4 px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider items-center">
                          <div class="col-span-2 text-center">
                            <span>Activity ID#</span>
                          </div>
                          <div class="col-span-2 text-center">
                            <span>Activity Title</span>
                          </div>
                          <div class="col-span-2 text-center">
                            <span>Type</span>
                          </div>
                          <div class="col-span-2 text-center">
                            <span>Status</span>
                          </div>
                          <div class="col-span-2 text-center">
                            <span>Due Time</span>
                          </div>
                          <div class="col-span-2 text-center">
                            <span>Due Date</span>
                          </div>
                        </div>
                      </div>

                      <!-- Table Body - Submitted Activities Only -->
                      <div class="divide-y divide-gray-200">
                        <div v-for="(activity, index) in folderActivities.filter(a => getActivityStatus(a) === 'submitted' || getActivityStatus(a) === 'resubmitted').slice(0, displayedSubmittedCount)" :key="activity.id"
                          class="group hover:bg-gray-50 transition-colors duration-150 cursor-pointer"
                          @click="openActivity(activity)">

                          <div class="grid grid-cols-12 gap-4 px-6 py-4 items-center">
                            <!-- Activity ID# -->
                            <div class="col-span-2 text-center">
                              <span class="text-sm text-gray-700 font-medium">{{ activity.id }}</span>
                            </div>

                            <!-- Title -->
                            <div class="col-span-2 text-center">
                              <span class="font-medium text-gray-900 whitespace-normal break-words" :title="activity.title">{{ activity.title }}</span>
                            </div>

                            <!-- Activity Type -->
                            <div class="col-span-2 text-center">
                              <span class="text-sm text-gray-700 capitalize font-medium">{{ activity.type }}</span>
                            </div>

                            <!-- Status Badge -->
                            <div class="col-span-2 text-center">
                              <span v-if="getActivityStatus(activity) === 'resubmitted'"
                                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                <i class="pi pi-refresh text-[10px] mr-1.5 text-blue-500"></i>
                                Resubmitted
                                <span v-if="activity.resubmit_count" class="ml-1">({{ activity.resubmit_count }}x)</span>
                              </span>
                              <span v-else-if="getActivityStatus(activity) === 'submitted' && activity.isLate"
                                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                                <i class="pi pi-circle-fill text-[6px] mr-1.5 text-orange-500"></i>
                                Submitted Late
                              </span>
                              <span v-else-if="getActivityStatus(activity) === 'submitted'"
                                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                <i class="pi pi-circle-fill text-[6px] mr-1.5 text-green-500"></i>
                                Submitted
                              </span>
                            </div>

                            <!-- Due Time -->
                            <div class="col-span-2 text-center">
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
                      <!-- Load More Button for Submitted -->
                      <div v-if="displayedSubmittedCount < folderActivities.filter(a => getActivityStatus(a) === 'submitted' || getActivityStatus(a) === 'resubmitted').length" class="p-4 text-center border-t border-gray-200 bg-gray-50">
                        <button @click="displayedSubmittedCount += itemsPerPage" class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors duration-200 flex items-center gap-2 mx-auto">
                          <i class="pi pi-chevron-down"></i>
                          <span>Load More ({{ folderActivities.filter(a => getActivityStatus(a) === 'submitted' || getActivityStatus(a) === 'resubmitted').length - displayedSubmittedCount }} more)</span>
                        </button>
                      </div>
                    </div>
                    </div>
                    <!-- End Submitted Outputs Section -->
                  </template>
                </div>
              </div>

              <!-- Folder Grid -->
              <div v-if="!selectedFolder" class="space-y-6">
                <!-- Header with title -->
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                  <div>
                    <h2 class="text-xl font-bold text-gray-900">My Activities</h2>
                  </div>
                </div>

                <!-- Loading State -->
                <div v-if="isLoadingFolders" class="flex flex-col justify-center items-center py-16 bg-white rounded-xl shadow-sm border border-gray-200">
                  <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
                  <span class="text-gray-600 font-medium">Loading your activity folders...</span>
                </div>

                <!-- Empty State -->
                <div v-else-if="portfolioFolders.length === 0" class="text-center py-16 bg-white rounded-xl shadow-sm border border-gray-200">
                  <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-indigo-100 mb-4">
                    <i class="pi pi-folder text-indigo-600 text-2xl"></i>
                  </div>
                  <h3 class="text-xl font-bold text-gray-900 mb-2">No Activity Folders Yet</h3>
                  <p class="text-gray-600 mb-4">Your teacher hasn't created any activity folders yet.</p>
                  <p class="text-sm text-gray-500">Check back later or contact your teacher for more information.</p>
                </div>

                <!-- Folders Grid -->
                <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
                  <div v-for="folder in portfolioFolders"
                    :key="folder.id"
                    @click="openFolderContent(folder)"
                    class="group cursor-pointer"
                  >
                    <div class="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-lg transition-all duration-300 relative h-full flex flex-col group-hover:border-indigo-300">
                      <!-- Header with Gradient Background -->
                      <div class="relative h-32 bg-gradient-to-r from-indigo-600 to-blue-600 rounded-t-xl">
                        <!-- Decorative Background Pattern -->
                        <div class="absolute inset-0 opacity-10">
                          <div class="absolute top-0 right-0 w-40 h-40 bg-white rounded-full transform translate-x-1/3 -translate-y-1/3"></div>
                        </div>

                        <!-- Content -->
                        <div class="relative z-10 p-4 h-full flex flex-col justify-between text-white">
                          <div>
                            <h3 class="text-lg font-bold truncate">{{ folder.title }}</h3>
                            <p class="text-sm text-white/80 truncate">Subject Folder</p>
                          </div>
                          <div class="text-xs text-white/70">{{ folder.items }} activities</div>
                        </div>

                        <!-- Student Avatar/Profile Picture -->
                        <div class="absolute bottom-2 right-4 w-16 h-16 rounded-full bg-white shadow-lg border-4 border-white flex items-center justify-center overflow-hidden">
                          <div v-if="currentUser?.profile_picture" class="w-full h-full">
                            <img :src="currentUser.profile_picture" :alt="currentUser?.name" class="w-full h-full object-cover">
                          </div>
                          <div v-else class="w-full h-full bg-gradient-to-br from-indigo-400 to-blue-500 flex items-center justify-center text-white font-bold text-lg">
                            {{ currentUser?.name?.charAt(0) || 'S' }}
                          </div>
                        </div>
                      </div>

                      <!-- Footer with Menu Button -->
                      <div class="p-4 flex items-center justify-end border-t border-gray-100 overflow-visible">
                        <!-- Menu Button (Vertical 3 dots) -->
                        <div class="relative z-20">
                          <button
                            @click.stop="activeFolderMenuIndex = activeFolderMenuIndex === folder.id ? null : folder.id"
                            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                            :title="`Menu for ${folder.title}`"
                          >
                            <i class="pi pi-ellipsis-v text-gray-500"></i>
                          </button>

                          <!-- Dropdown Menu -->
                          <div v-if="activeFolderMenuIndex === folder.id" class="absolute right-0 bottom-full mb-2 w-48 bg-white rounded-md shadow-lg z-20 py-1">
                            <a @click.stop="openFolderContent(folder)" href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center">
                              <i class="pi pi-eye mr-2"></i> View Contents
                            </a>
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

        <!-- Portfolio Compilation Tab Content -->
        <template v-if="activeTab === 'compilation'">
          <!-- Loading State -->
          <div v-if="isLoadingCompilationStatus" class="text-center p-8">
            <i class="pi pi-spin pi-spinner text-4xl text-gray-400"></i>
            <p class="mt-2 text-gray-500">Checking compilation status...</p>
          </div>

          <!-- Main Content -->
          <div v-else class="min-h-screen transition-all duration-700 relative overflow-hidden"
               :style="isEnvelopeOpen && portfolioEnvelopeCreated ? {
                 background: `
                   radial-gradient(circle at 20% 50%, ${adjustBrightness(envelopeDesign.color, 20)} 0%, transparent 50%),
                   radial-gradient(circle at 80% 80%, ${adjustBrightness(envelopeDesign.color, -10)} 0%, transparent 50%),
                   radial-gradient(circle at 40% 20%, ${adjustBrightness(envelopeDesign.color, 10)} 0%, transparent 50%),
                   linear-gradient(135deg, ${envelopeDesign.color} 0%, ${adjustBrightness(envelopeDesign.color, -30)} 100%)
                 `,
                 backgroundSize: '200% 200%',
                 animation: 'gradientShift 12s ease infinite'
               } : { background: 'white' }">

            <!-- Animated Background Elements - Only when envelope is open -->
            <div v-if="isEnvelopeOpen && portfolioEnvelopeCreated" class="absolute inset-0 pointer-events-none overflow-hidden">
              <!-- Mesh Gradient Overlay -->
              <div class="absolute inset-0 opacity-30"
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
              <div v-if="envelopeDesign.pattern === 'dots'"
                   class="absolute inset-0 opacity-5 animate-patternFloat"
                   style="background-image: radial-gradient(circle, white 3px, transparent 3px); background-size: 40px 40px;">
              </div>
              <div v-else-if="envelopeDesign.pattern === 'lines'"
                   class="absolute inset-0 opacity-5 animate-patternSlide"
                   style="background-image: repeating-linear-gradient(45deg, white 0, white 3px, transparent 3px, transparent 20px);">
              </div>
              <div v-else-if="envelopeDesign.pattern === 'grid'"
                   class="absolute inset-0 opacity-5 animate-patternPulse"
                   style="background-image: linear-gradient(white 2px, transparent 2px), linear-gradient(90deg, white 2px, transparent 2px); background-size: 40px 40px;">
              </div>

              <!-- Large Floating Orbs -->
              <div>
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
              <div>
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
              <div class="absolute inset-0">
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
                        <img v-if="portfolioActivities[currentActivityIndex].submission_file && (portfolioActivities[currentActivityIndex].submission_file.startsWith('data:image') || portfolioActivities[currentActivityIndex].submission_file.match(/\.(jpeg|jpg|gif|png|webp)$/i))"
                             :src="portfolioActivities[currentActivityIndex].submission_file"
                             alt="Activity submission"
                             class="w-full h-full object-contain"
                             @error="(e) => { console.error('Image load error:', portfolioActivities[currentActivityIndex].submission_file); e.target.style.display = 'none'; }"
                        />
                        <div v-else-if="portfolioActivities[currentActivityIndex].submission_file" class="text-center flex flex-col items-center">
                            <i class="pi pi-file-pdf text-6xl text-red-500 mb-4" v-if="portfolioActivities[currentActivityIndex].submission_file.includes('pdf')"></i>
                            <i class="pi pi-file text-6xl text-indigo-300 mb-4" v-else></i>
                            <p class="text-gray-600 font-medium mb-2">File Attached</p>
                            <a :href="portfolioActivities[currentActivityIndex].submission_file"
                               target="_blank"
                               class="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700 transition-colors">
                                View File
                            </a>
                        </div>
                        <div v-else class="text-center flex flex-col items-center">
                          <div v-if="portfolioActivities[currentActivityIndex].submission_status === 'submitted_compilation'" class="flex flex-col items-center">
                              <i class="pi pi-check-circle text-6xl text-green-500 mb-4"></i>
                              <p class="text-green-600 font-medium">Activity Compiled</p>
                          </div>
                          <div v-else class="flex flex-col items-center">
                              <i class="pi pi-file text-6xl text-indigo-300 mb-4"></i>
                              <p class="text-indigo-600 font-medium">
                                {{ portfolioActivities[currentActivityIndex].submission_status === 'missing' ? 'No Submission' : 'No File Available' }}
                              </p>
                          </div>
                        </div>
                      </div>

                      <!-- Submission Caption -->
                      <div v-if="portfolioActivities[currentActivityIndex].submission_caption" class="mb-4 p-4 bg-gray-50 rounded-lg">
                        <p class="text-sm text-gray-700 italic">
                          "{{ portfolioActivities[currentActivityIndex].submission_caption }}"
                        </p>
                      </div>

                      <!-- Score and Feedback -->
                      <div v-if="portfolioActivities[currentActivityIndex].is_compilation || (portfolioActivities[currentActivityIndex].submission_score !== null && portfolioActivities[currentActivityIndex].submission_score !== undefined)"
                           class="mb-4 p-4 rounded-lg"
                           :class="portfolioActivities[currentActivityIndex].is_compilation ? 'bg-purple-50 border border-purple-200' : 'bg-green-50 border border-green-200'">
                        <div class="flex items-center justify-between mb-2">
                          <span class="text-sm font-medium text-gray-700">Status:</span>
                          <span class="text-xl font-bold"
                                :class="(portfolioActivities[currentActivityIndex].is_compilation && portfolioActivities[currentActivityIndex].submission_score == null) ? 'text-purple-700' : 'text-green-700'">
                                {{ (portfolioActivities[currentActivityIndex].is_compilation && portfolioActivities[currentActivityIndex].submission_score == null) ? 'Compiled' : portfolioActivities[currentActivityIndex].submission_score }}
                          </span>
                        </div>
                        <div v-if="portfolioActivities[currentActivityIndex].submission_feedback"
                             class="mt-2 pt-2 border-t"
                             :class="portfolioActivities[currentActivityIndex].is_compilation ? 'border-purple-200' : 'border-green-200'">
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
                            <span class="px-3 py-1 rounded-full text-sm font-medium inline-block capitalize"
                                  :class="{
                                    'bg-green-100 text-green-800': portfolioActivities[currentActivityIndex].submission_status === 'scored',
                                    'bg-purple-100 text-purple-800': portfolioActivities[currentActivityIndex].submission_status === 'submitted_compilation',
                                    'bg-blue-100 text-blue-800': portfolioActivities[currentActivityIndex].submission_status === 'scored_resubmitted',
                                    'bg-orange-100 text-orange-800': portfolioActivities[currentActivityIndex].submission_status === 'scored_late',
                                    'bg-red-100 text-red-800': portfolioActivities[currentActivityIndex].submission_status === 'missing'
                                  }">
                              {{ portfolioActivities[currentActivityIndex].submission_status === 'submitted_compilation' ? 'Submitted Compilation' : portfolioActivities[currentActivityIndex].submission_status }}
                              <span v-if="portfolioActivities[currentActivityIndex].is_resubmitted" class="ml-1 text-xs">({{ portfolioActivities[currentActivityIndex].resubmit_count }}x)</span>
                            </span>
                          </div>
                          <div v-if="portfolioActivities[currentActivityIndex].submitted_date">
                            <span class="text-sm text-gray-500 block mb-1">Date Submitted:</span>
                            <span class="text-sm font-medium text-gray-900">
                              {{ portfolioActivities[currentActivityIndex].submitted_date }}
                            </span>
                          </div>
                          <div v-if="portfolioActivities[currentActivityIndex].submitted_time">
                            <span class="text-sm text-gray-500 block mb-1">Time Submitted:</span>
                            <span class="text-sm font-medium text-gray-900">
                              {{ portfolioActivities[currentActivityIndex].submitted_time }}
                            </span>
                          </div>
                          <div v-if="portfolioActivities[currentActivityIndex].scored_at">
                            <span class="text-sm text-gray-500 block mb-1">Scored At:</span>
                            <span class="text-sm font-medium text-green-600">
                              {{ new Date(portfolioActivities[currentActivityIndex].scored_at).toLocaleString('en-US', {
                                month: 'short',
                                day: 'numeric',
                                year: 'numeric',
                                hour: 'numeric',
                                minute: '2-digit',
                                hour12: true
                              }) }}
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
                           class="bg-orange-50 border border-orange-200 rounded-xl p-6 hover:bg-orange-100 transition-colors">
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
                            <h4 class="text-xl font-bold text-gray-900 whitespace-normal break-words mb-2">{{ activity.title }}</h4>
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
                          <!-- Show different buttons based on draft status -->
                          <div v-if="compilationDrafts[activity.id]" class="ml-4 flex gap-2">
                            <button
                              @click="editCompilation(activity)"
                              class="px-6 py-3 bg-white text-indigo-600 font-semibold rounded-lg border-2 border-indigo-600 hover:bg-indigo-50 transition-all shadow-lg hover:shadow-xl flex items-center gap-2"
                            >
                              <i class="pi pi-pencil"></i>
                              Edit Compilation
                            </button>
                            <button
                              @click="openSubmitCompilationDialog(activity)"
                              class="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg hover:shadow-xl flex items-center gap-2"
                            >
                              <i class="pi pi-upload"></i>
                              Upload & Submit
                            </button>
                          </div>
                          <button
                            v-else
                            @click="compileActivity(activity)"
                            class="ml-4 px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl flex items-center gap-2"
                          >
                            <i class="pi pi-upload"></i>
                            Upload File
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

            <!-- Show waiting screen if compilation not requested -->
            <div v-if="!isCompilationReady" class="text-center p-12 max-w-lg mx-auto bg-white rounded-2xl shadow-sm border border-gray-100">
              <div class="w-14 h-14 mx-auto bg-gray-100/80 rounded-full flex items-center justify-center mb-6">
                <i class="pi pi-clock text-xl text-gray-400"></i>
              </div>
              <h2 class="text-2xl font-bold text-gray-800">Waiting for Teacher</h2>
              <p class="text-gray-500 mt-3">Your teacher hasn't requested portfolio compilation yet.</p>
              <p class="text-gray-500 mt-1">You'll be notified when it's time to start compiling your portfolio.</p>
            </div>

            <!-- Show compilation ready screen if requested but not started -->
            <div v-else-if="isCompilationReady && !portfolioEnvelopeCreated" class="text-center p-12 max-w-lg mx-auto bg-white rounded-2xl shadow-sm border border-gray-100">
              <div class="w-16 h-16 mx-auto bg-indigo-100/80 rounded-full flex items-center justify-center mb-6">
                <i class="pi pi-book text-2xl text-indigo-500"></i>
              </div>
              <h2 class="text-2xl font-bold text-gray-800">Portfolio Compilation Ready</h2>
              <p class="text-gray-600 mt-3 max-w-md mx-auto">Your teacher has requested you to start compiling your portfolio. Click the button below to begin organizing your work and achievements.</p>
              <button @click="startPortfolioCompilation" class="w-full sm:w-auto mt-8 px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-3 transform hover:scale-105 mx-auto">
                <i class="pi pi-play-circle text-xl"></i>
                <span>Start Portfolio Compilation</span>
              </button>
            </div>

            <!-- Close Content Area -->
          </div>
        </div>
      </template>

        <!-- Schedule Tab Content -->
        <template v-if="activeTab === 'schedule'">
          <div class="p-4 md:p-6">
            <!-- Calendar Header -->
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
              <h2 class="text-xl font-bold text-gray-900">NOVEMBER 2025</h2>
              <div class="flex items-center gap-2 bg-white px-3 py-1 rounded-full border border-gray-200">
                <span class="text-sm text-gray-500">School Year:</span>
                <span class="text-sm font-medium text-indigo-700">2024-2025</span>
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

        <!-- Classroom Tab Content -->
        <template v-if="activeTab === 'classroom'">
          <div class="p-4 md:p-6 min-h-screen bg-white">
            <!-- Classroom Header -->
            <div class="bg-white shadow-sm border-b border-gray-200 rounded-t-xl -mx-6 -mt-6 px-6 py-4 mb-6">
              <div class="flex items-center justify-between">
                <div>
                  <h1 class="text-2xl font-bold text-gray-900">My Classroom </h1>
                </div>
                <div class="flex items-center gap-2 bg-white px-3 py-1 rounded-full border border-gray-200">
                  <span class="text-sm text-gray-500">School Year:</span>
                  <span class="text-sm font-medium text-indigo-700">2024-2025</span>
                </div>
              </div>
            </div>

            <!-- Classroom Card -->
            <div class="bg-white rounded-xl shadow-lg overflow-hidden">
              <!-- Classroom Header -->
              <div class="bg-white border-b border-gray-200 p-6">
                <div class="flex items-center justify-between">
                  <div>
                    <h2 class="text-2xl font-bold text-gray-900">{{ actualClassName }}</h2>
                    <p class="text-gray-600 mt-1">Room 111</p>
                  </div>
                  <div class="text-right">
                    <p class="text-gray-900 text-3xl font-bold">{{ studentClassmates.length }}</p>
                    <p class="text-gray-600 text-sm">Classmates</p>
                  </div>
                </div>
              </div>

              <!-- Class Adviser Section -->
              <div class="p-6 border-b border-gray-200 bg-gray-50">
                <h3 class="text-sm font-semibold text-gray-700 mb-3">Class Adviser</h3>
                <div class="flex items-center gap-3 p-3 bg-white rounded-lg">
                  <div class="w-12 h-12 bg-gray-100 border border-gray-200 rounded-full flex items-center justify-center text-gray-700 font-bold text-lg">
                    {{ getTeacherInitials(classTeacher) }}
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">{{ classTeacher }}</p>
                    <p class="text-sm text-gray-600">{{ classTeacherEmail }}</p>
                    <p class="text-xs text-gray-500 flex items-center gap-1 mt-1">
                      <i class="pi pi-book text-gray-500"></i>
                      Mathematics
                    </p>
                  </div>
                </div>
              </div>

              <!-- Classmates List -->
              <div class="p-6">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-lg font-semibold text-gray-900">My Classmates</h3>
                  <span class="text-sm text-indigo-600 font-medium">{{ studentClassmates.length }} students</span>
                </div>

                <!-- Search Bar -->
                <div class="mb-4">
                  <div class="relative">
                    <input
                      v-model="classmateSearchQuery"
                      type="text"
                      placeholder="Search classmates by name..."
                      class="w-full px-4 py-2.5 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
                    />
                    <i class="pi pi-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                  </div>
                </div>

                <!-- Classmates Grid -->
                <div class="space-y-3 max-h-96 overflow-y-auto">
                  <div v-for="(classmate, index) in filteredClassmates" :key="classmate.id"
                    class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <span class="text-sm text-gray-500 font-medium w-8">{{ index + 1 }}.</span>
                    <div class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                      {{ getInitials(classmate.name) }}
                    </div>
                    <div class="flex-1">
                      <p class="font-medium text-gray-900">{{ classmate.name }}</p>
                      <p class="text-xs text-gray-500">{{ classmate.email }}</p>
                    </div>
                  </div>

                  <!-- No Results -->
                  <div v-if="filteredClassmates.length === 0" class="text-center py-8">
                    <i class="pi pi-search text-gray-400 text-3xl mb-3"></i>
                    <p class="text-gray-500">No classmates found matching "{{ classmateSearchQuery }}"</p>
                  </div>
                </div>

                <!-- Empty State -->
                <div v-if="studentClassmates.length === 0" class="text-center py-8">
                  <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i class="pi pi-users text-gray-400 text-2xl"></i>
                  </div>
                  <h3 class="text-lg font-medium text-gray-900 mb-2">No Classmates Yet</h3>
                  <p class="text-gray-500">Your classmates will appear here once they join.</p>
                </div>
              </div>
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
            @click="submitWork()"
            class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
            :disabled="!selectedFile || isSubmitting"
            :class="{'opacity-50 cursor-not-allowed': !selectedFile || isSubmitting}"
          >
            <i v-if="!isSubmitting" class="pi pi-check"></i>
            <i v-else class="pi pi-spin pi-spinner"></i>
            {{ isSubmitting ? 'Submitting...' : 'Submit' }}
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
                            <h4 class="font-semibold text-gray-900 whitespace-normal break-words mb-1">{{ activity.title }}</h4>
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

    <!-- Post to Feed Confirmation Dialog -->
    <Dialog v-model:visible="showPostToFeedConfirmDialog" modal :style="{ width: '90vw', maxWidth: '600px' }" :dismissableMask="true">
      <template #header>
        <div class="flex items-center gap-3">
          <i class="pi pi-send text-blue-600 text-xl"></i>
          <h3 class="text-lg font-bold text-gray-800">Post to Feed</h3>
        </div>
      </template>

      <div class="space-y-4">
        <p class="text-gray-700">
          Select the files you want to post to the class feed and add a caption.
        </p>

        <!-- File Selection (Multiple) -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <label class="block text-sm font-medium text-gray-700">Select Files to Post</label>
            <span v-if="postToFeedSelectedFiles.length > 0" class="text-xs text-blue-600 font-medium">
              {{ postToFeedSelectedFiles.length }} file{{ postToFeedSelectedFiles.length > 1 ? 's' : '' }} selected
            </span>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 max-h-48 overflow-y-auto p-2 bg-gray-50 rounded-lg border border-gray-200">
            <button
              v-for="(submission, index) in studentSubmissions"
              :key="submission.id || index"
              @click="toggleFileSelection(submission)"
              class="relative p-2 rounded-lg border-2 transition-all hover:shadow-md"
              :class="isFileSelected(submission) ? 'border-blue-500 bg-blue-50' : 'border-gray-200 bg-white hover:border-gray-300'"
            >
              <!-- Thumbnail -->
              <div class="aspect-square rounded-md overflow-hidden bg-gray-100 mb-2">
                <img
                  v-if="submission.isImage && submission.previewUrl"
                  :src="submission.previewUrl"
                  :alt="submission.caption || 'File'"
                  class="w-full h-full object-cover"
                />
                <div v-else class="w-full h-full flex items-center justify-center">
                  <i :class="['text-2xl', submission.isImage ? 'pi pi-image text-indigo-500' : 'pi pi-file-pdf text-red-500']"></i>
                </div>
              </div>
              <!-- File name -->
              <p class="text-xs text-gray-600 truncate">{{ submission.caption || `File ${index + 1}` }}</p>
              <!-- Selected indicator -->
              <div v-if="isFileSelected(submission)" class="absolute top-1 right-1 w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center">
                <i class="pi pi-check text-white text-xs"></i>
              </div>
            </button>
          </div>
          <p v-if="studentSubmissions.length === 0" class="text-sm text-gray-500 italic text-center py-4">
            No files available to post
          </p>
          <!-- Select All / Deselect All -->
          <div v-if="studentSubmissions.length > 1" class="flex gap-2">
            <button
              @click="selectAllFiles"
              class="text-xs text-blue-600 hover:text-blue-800 font-medium"
            >
              Select All
            </button>
            <span class="text-gray-300">|</span>
            <button
              @click="deselectAllFiles"
              class="text-xs text-gray-600 hover:text-gray-800 font-medium"
            >
              Deselect All
            </button>
          </div>
        </div>

        <!-- Caption Input -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">Caption (Optional)</label>
          <textarea
            v-model="postToFeedCaption"
            placeholder="Add a caption for your post..."
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none text-sm"
          ></textarea>
        </div>

        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div class="flex items-start gap-3">
            <i class="pi pi-info-circle text-blue-600 text-lg mt-0.5"></i>
            <div class="text-sm text-blue-800">
              <p class="font-semibold mb-1">What happens next?</p>
              <ul class="list-disc list-inside space-y-1 text-blue-700">
                <li>Your teacher will be notified of your request</li>
                <li>Your work will be visible to the class once approved</li>
                <li>You cannot undo this action after approval</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-3">
          <button
            @click="showPostToFeedConfirmDialog = false; postToFeedSelectedFiles = []; postToFeedCaption = '';"
            class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors duration-200"
          >
            Cancel
          </button>
          <button
            @click="confirmPostToFeed"
            :disabled="isRequestingPost || postToFeedSelectedFiles.length === 0"
            class="px-5 py-2.5 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <i class="pi pi-send"></i>
            <span>{{ isRequestingPost ? 'Sending...' : `Confirm (${postToFeedSelectedFiles.length})` }}</span>
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
                            :placeholder="actualClassName"
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
                                    {{ envelopeDesign.className || actualClassName }}
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
          <div>
            <h3 class="text-lg font-bold text-gray-800">Add or Create Work</h3>
            <p v-if="draftFiles.length > 0" class="text-xs text-gray-500">
              {{ draftFiles.length }} file{{ draftFiles.length > 1 ? 's' : '' }} already attached
            </p>
          </div>
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
                <p class="text-sm text-gray-500 mb-6">Select one or more files from your computer</p>
              </div>
              <button
                @click="triggerAutoSaveFileUpload"
                class="px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors duration-200 flex items-center gap-2 mx-auto"
              >
                <i class="pi pi-folder-open"></i>
                <span>Browse Files</span>
              </button>
              <p class="text-xs text-gray-400 mt-4">Supported formats: Images, PDF, Word documents • Multiple files allowed</p>
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
          <div v-else-if="activeUploadTab === 'collection'" class="p-4 h-[400px] overflow-y-auto">
             <div v-if="loadingCollection" class="flex flex-col items-center justify-center py-20">
               <i class="pi pi-spin pi-spinner text-4xl text-purple-600 mb-4"></i>
               <p class="text-gray-500">Loading collection...</p>
             </div>
             <div v-else-if="submittedCollection.length === 0" class="flex flex-col items-center justify-center py-20 text-gray-500">
               <i class="pi pi-folder-open text-4xl mb-3 text-gray-300"></i>
               <p>No submitted work found in your collection.</p>
             </div>
             <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
               <div
                 v-for="item in submittedCollection"
                 :key="item.id"
                 @click="selectCollectionItem(item)"
                 class="group relative rounded-lg overflow-hidden border-2 cursor-pointer transition-all duration-200"
                 :class="[
                   selectedCollectionId === item.id
                     ? 'border-purple-500 ring-2 ring-purple-200 shadow-md'
                     : 'border-gray-200 hover:border-purple-300 hover:shadow-sm'
                 ]"
               >
                 <!-- Thumbnail/Preview -->
                 <div class="aspect-square bg-gray-100 flex items-center justify-center p-2">
                   <img
                     v-if="item.file_type === 'image'"
                     :src="item.file_path"
                     class="w-full h-full object-cover rounded"
                     alt="Submission"
                   />
                   <div v-else class="text-center">
                     <i class="pi pi-file text-3xl text-gray-400 mb-2"></i>
                     <span class="text-xs uppercase font-bold text-gray-500 block">{{ item.file_type || 'FILE' }}</span>
                   </div>
                 </div>

                 <!-- Selection Overlay -->
                 <div
                   v-if="selectedCollectionId === item.id"
                   class="absolute inset-0 bg-purple-500 bg-opacity-10 z-10 flex items-center justify-center"
                 >
                   <div class="bg-white rounded-full p-2 shadow-sm">
                     <i class="pi pi-check text-purple-600 font-bold"></i>
                   </div>
                 </div>

                 <!-- Info Overlay (always visible at bottom) -->
                 <div class="absolute bottom-0 left-0 right-0 bg-white bg-opacity-95 p-2 text-xs border-t border-gray-100">
                   <div class="font-medium truncate text-gray-800" :title="item.activity_title">
                     {{ item.activity_title }}
                   </div>
                   <div class="text-gray-500 text-[10px] mt-0.5">
                     {{ formatSketchDate(item.submitted_at) }}
                   </div>
                 </div>
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
            v-if="activeUploadTab === 'collection' && selectedCollectionId"
            @click="useSelectedCollectionItem"
            :disabled="isSubmitting"
            class="px-5 py-2.5 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors duration-200 flex items-center gap-2 shadow-sm"
          >
            <i v-if="isSubmitting" class="pi pi-spin pi-spinner"></i>
            <i v-else class="pi pi-plus"></i>
            <span>{{ isSubmitting ? 'Adding...' : 'Add to Draft' }}</span>
          </button>
          <button
            v-if="activeUploadTab === 'sketch' && selectedSketchId"
            @click="useSelectedSketch"
            :disabled="isSubmitting"
            class="px-5 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <i v-if="!isSubmitting" class="pi pi-plus"></i>
            <i v-else class="pi pi-spin pi-spinner"></i>
            <span>{{ isSubmitting ? 'Adding...' : 'Add to Draft' }}</span>
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
          <div
            @click="triggerCompilationFileUpload"
            class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center bg-gray-50 cursor-pointer hover:border-indigo-400 hover:bg-indigo-50 transition-colors">
            <input
              ref="compilationFileInput"
              type="file"
              @change="handleCompilationFileUpload"
              accept="image/*,.pdf,.doc,.docx"
              class="hidden"
            />
            <div v-if="draftFiles.length > 0" class="space-y-2">
              <div
                v-for="file in draftFiles"
                :key="`turn-in-${file.id}-${file.path}`"
                class="flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-200"
              >
                <!-- Thumbnail with actual image -->
                <div class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 overflow-hidden"
                     :class="file.type === 'image' ? 'bg-gray-100' : 'bg-indigo-100'">
                  <img
                    v-if="file.type === 'image' && file.path"
                    :key="file.path"
                    :src="file.path"
                    :alt="file.name"
                    class="w-full h-full object-cover"
                    @load="() => console.log('✅ Turn-in dialog image loaded:', file.path)"
                    @error="(e) => { console.error('❌ Turn-in dialog image error:', file.path); e.target.style.display = 'none'; e.target.nextElementSibling.style.display = 'flex'; }"
                  />
                  <div
                    class="w-full h-full flex items-center justify-center"
                    :style="file.type === 'image' && file.path ? 'display: none;' : ''">
                    <i v-if="file.type === 'image'" class="pi pi-image text-indigo-600"></i>
                    <i v-else-if="file.type === 'pdf'" class="pi pi-file-pdf text-red-600"></i>
                    <i v-else class="pi pi-file text-gray-600"></i>
                  </div>
                </div>
                <div class="flex-1 text-left">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ file.name }}</p>
                  <p class="text-xs text-gray-500 capitalize">{{ file.type }}</p>
                </div>
                <!-- Remove Button -->
                <button
                  @click.stop="confirmRemoveFile(file)"
                  class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-red-100 transition-colors"
                  title="Remove file"
                >
                  <i class="pi pi-times text-red-600"></i>
                </button>
              </div>
            </div>
            <div v-else class="text-gray-500">
              <i class="pi pi-upload text-3xl mb-2"></i>
              <p class="text-sm">Click to upload or drag and drop</p>
              <p class="text-xs text-gray-400">(PDF, DOC, DOCX, or Images)</p>
            </div>
          </div>
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
            @click="submitTurnInWork"
            :disabled="isSubmitting || draftFiles.length === 0"
            class="px-5 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <i v-if="isSubmitting" class="pi pi-spin pi-spinner"></i>
            <i v-else class="pi pi-check"></i>
            <span>{{ isSubmitting ? 'Submitting...' : 'Submit' }}</span>
          </button>
        </div>
      </template>
    </Dialog>

    <!-- Submit Compilation Confirmation Dialog -->
    <Dialog v-model:visible="showSubmitCompilationDialog" modal :style="{ width: '90vw', maxWidth: '450px' }" :dismissableMask="true">
      <template #header>
        <div class="flex items-center gap-3">
          <i class="pi pi-send text-indigo-600 text-xl"></i>
          <h3 class="text-lg font-bold text-gray-800">Submit Compilation</h3>
        </div>
      </template>

      <div class="py-4">
        <p class="text-gray-700">Are you sure you want to submit this compilation? Once submitted, it will be sent to your teacher for review.</p>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3">
          <button
            @click="showSubmitCompilationDialog = false"
            class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors duration-200"
          >
            Cancel
          </button>
          <button
            @click="submitCompilation"
            :disabled="isSubmitting"
            class="px-5 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <i v-if="isSubmitting" class="pi pi-spin pi-spinner"></i>
            <i v-else class="pi pi-send"></i>
            <span>{{ isSubmitting ? 'Submitting...' : 'Submit Now' }}</span>
          </button>
        </div>
      </template>
    </Dialog>

    <!-- Resubmit Confirmation Dialog -->
    <Dialog v-model:visible="showResubmitConfirmDialog" modal :style="{ width: '90vw', maxWidth: '500px' }" :dismissableMask="true">
      <template #header>
        <div class="flex items-center gap-3">
          <i class="pi pi-exclamation-triangle text-orange-600 text-xl"></i>
          <h3 class="text-lg font-bold text-gray-800">Confirm Resubmission</h3>
        </div>
      </template>

      <div class="space-y-4">
        <!-- Warning Message -->
        <div class="bg-orange-50 border border-orange-200 rounded-lg p-4">
          <div class="flex gap-3">
            <i class="pi pi-info-circle text-orange-600 text-lg flex-shrink-0 mt-0.5"></i>
            <div class="flex-1">
              <p class="text-sm text-gray-800 font-medium mb-2">You are about to resubmit your work</p>
              <p class="text-sm text-gray-600">
                This will count as resubmission #<strong>{{ (existingSubmission?.resubmit_count || 0) + 1 }}</strong> of 3 maximum allowed.
              </p>
            </div>
          </div>
        </div>

        <!-- Resubmit Info -->
        <div class="space-y-2">
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-600">Current resubmissions:</span>
            <span class="font-semibold text-gray-900">{{ existingSubmission?.resubmit_count || 0 }} / 3</span>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-600">Remaining resubmissions:</span>
            <span class="font-semibold" :class="(3 - (existingSubmission?.resubmit_count || 0)) <= 1 ? 'text-red-600' : 'text-green-600'">
              {{ 3 - (existingSubmission?.resubmit_count || 0) }} left
            </span>
          </div>
        </div>

        <!-- File Preview -->
        <div v-if="draftFiles.length > 0" class="border border-gray-200 rounded-lg p-3 bg-gray-50">
          <p class="text-xs text-gray-500 mb-2">File to submit:</p>
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 overflow-hidden"
                 :class="draftFiles[0].type === 'image' ? 'bg-gray-100' : 'bg-indigo-100'">
              <img
                v-if="draftFiles[0].type === 'image' && draftFiles[0].path"
                :src="draftFiles[0].path"
                :alt="draftFiles[0].name"
                class="w-full h-full object-cover"
              />
              <i v-else-if="draftFiles[0].type === 'pdf'" class="pi pi-file-pdf text-red-600"></i>
              <i v-else class="pi pi-file text-gray-600"></i>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">{{ draftFiles[0].name }}</p>
              <p class="text-xs text-gray-500 capitalize">{{ draftFiles[0].type }}</p>
            </div>
          </div>
        </div>

        <!-- Confirmation Question -->
        <p class="text-sm text-gray-700 font-medium">
          Are you sure you want to proceed with this resubmission?
        </p>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3">
          <button
            @click="showResubmitConfirmDialog = false"
            class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors duration-200"
          >
            Cancel
          </button>
          <button
            @click="confirmResubmitAction"
            class="px-5 py-2.5 text-sm font-medium text-white bg-orange-600 rounded-lg hover:bg-orange-700 transition-colors duration-200 flex items-center gap-2"
          >
            <i class="pi pi-check"></i>
            <span>Confirm Resubmit</span>
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
        <!-- File Info with Edit Caption -->
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200 space-y-3">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center">
              <i v-if="previewFile.type === 'image'" class="pi pi-image text-indigo-600 text-xl"></i>
              <i v-else-if="previewFile.type === 'pdf'" class="pi pi-file-pdf text-red-600 text-xl"></i>
              <i v-else class="pi pi-file text-gray-600 text-xl"></i>
            </div>
            <div class="flex-1">
              <p class="font-semibold text-gray-900">{{ previewFile.name }}</p>
              <p class="text-sm text-gray-500 capitalize">{{ previewFile.type }}</p>
            </div>
            <!-- View File Button - opens file in new tab -->
            <button
              v-if="previewFile.path"
              @click="openFileInNewTab(previewFile.path, previewFile.type)"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 flex items-center gap-2"
            >
              <i class="pi pi-external-link"></i>
              <span>View File</span>
            </button>
          </div>

          <!-- Caption Editor -->
          <div v-if="!hasSubmittedWork">
            <label class="block text-sm font-medium text-gray-700 mb-2">Caption</label>
            <textarea
              v-model="previewFileCaption"
              rows="2"
              placeholder="Add a caption for your work..."
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none text-sm"
            ></textarea>
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

          <!-- PDF Preview - Card style like Word docs -->
          <div v-else-if="previewFile.type === 'pdf'" class="w-full">
            <div class="text-center">
              <div class="bg-white rounded-lg p-8 border border-gray-200 max-w-md mx-auto">
                <i class="pi pi-file-pdf text-6xl text-red-500 mb-4"></i>
                <p class="text-gray-700 font-medium mb-2">{{ previewFile.name }}</p>
                <p class="text-gray-500 text-sm mb-2">PDF Document</p>
                <p class="text-gray-400 text-xs">Click "View File" button above to open PDF</p>
              </div>
            </div>
          </div>

          <!-- Document Preview (Word docs) -->
          <div v-else-if="previewFile.type === 'document'" class="w-full">
            <div class="text-center">
              <div class="bg-white rounded-lg p-8 border border-gray-200 max-w-md mx-auto">
                <i class="pi pi-file-word text-6xl text-blue-500 mb-4"></i>
                <p class="text-gray-700 font-medium mb-2">{{ previewFile.name }}</p>
                <p class="text-gray-500 text-sm mb-2">Word Document</p>
                <p class="text-gray-400 text-xs">Click "View File" button above to open in Google Docs Viewer</p>
              </div>
            </div>
          </div>

          <!-- Other Files -->
          <div v-else class="text-center w-full">
            <div class="bg-white rounded-lg p-8 border border-gray-200 max-w-md mx-auto">
              <i class="pi pi-file text-6xl text-gray-400 mb-4"></i>
              <p class="text-gray-700 font-medium mb-2">{{ previewFile.name }}</p>
              <p class="text-gray-500 text-sm mb-4">{{ previewFile.type || 'File' }}</p>
              <p class="text-gray-400 text-xs">Click "View File" to open the file.</p>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex items-center justify-between w-full gap-3">
          <!-- Left side: Replace File button (only if draft OR resubmitting) -->
          <div v-if="!hasSubmittedWork || isResubmitting" class="flex gap-2">
            <button
              @click="replaceCurrentFile"
              class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors duration-200 flex items-center gap-2"
            >
              <i class="pi pi-refresh"></i>
              <span>Replace File</span>
            </button>
            <button
              @click="savePreviewCaption"
              :disabled="!previewFileCaption || previewFileCaption === previewFile?.name"
              class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <i class="pi pi-save"></i>
              <span>Save Caption</span>
            </button>
          </div>
          <div v-else></div>

          <!-- Right side: Close button -->
          <button
            @click="showFilePreview = false"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors duration-200"
          >
            Close
          </button>
        </div>
      </template>
    </Dialog>

    <!-- All Instruction Files Dialog -->
    <Dialog v-model:visible="showAllInstructionFilesDialog" modal header="Activity Instruction" :style="{ width: '90vw', maxWidth: '600px' }" :dismissableMask="true">
      <div class="space-y-4">
        <!-- Instruction Text -->
        <div v-if="selectedActivity && selectedActivity.description" class="p-4 bg-gray-50 rounded-lg border border-gray-200">
          <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap break-words">{{ selectedActivity.description }}</p>
        </div>
        <div v-else-if="!selectedActivity?.instruction_files || selectedActivity.instruction_files.length === 0" class="p-4 bg-gray-50 rounded-lg border border-gray-200">
          <p class="text-sm text-gray-500 italic">No instructions provided</p>
        </div>

        <!-- Attached Files -->
        <div v-if="selectedActivity && selectedActivity.instruction_files && selectedActivity.instruction_files.length > 0">
          <h4 class="text-sm font-semibold text-gray-700 mb-2">Attached Files:</h4>
          <div class="flex flex-col gap-2">
            <a 
              v-for="file in selectedActivity.instruction_files" 
              :key="file.id"
              :href="file.file_url"
              target="_blank"
              class="flex items-center gap-2 px-3 py-2 bg-indigo-50 border border-indigo-200 rounded-lg text-sm hover:bg-indigo-100 transition-colors"
            >
              <i class="pi pi-file text-indigo-600"></i>
              <span class="text-indigo-700 flex-1">{{ file.file_name }}</span>
              <i class="pi pi-external-link text-indigo-400"></i>
            </a>
          </div>
        </div>
      </div>
      <template #footer>
        <button
          @click="showAllInstructionFilesDialog = false"
          class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
        >
          Close
        </button>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, inject, watch, nextTick } from 'vue';
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
    role: 'student',
    classroom: null
});

// Computed property for actual classroom name
const actualClassName = computed(() => {
    // Priority: selectedClass > currentUser.classroom > props.className
    if (selectedClass.value && selectedClass.value.name) {
        return selectedClass.value.name;
    }
    if (currentUser.value.classroom) {
        return currentUser.value.classroom;
    }
    return props.className;
});

const activeTab = ref('classroom');
const activeContentTab = ref('samples');
const portfolioData = ref({ teacher_requested_compilation: false }); // Reactive object for portfolio state

const isCompilationReady = computed(() => {
    return portfolioData.value?.teacher_requested_compilation === true;
});
const isLoadingCompilationStatus = ref(true); // Start in a loading state
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
  { id: 'classroom', name: 'Classroom', icon: 'pi-building' },
  { id: 'portfolio', name: 'Activities', icon: 'pi-folder' },
  { id: 'compilation', name: 'Portfolio Compilation', icon: 'pi-book' }
];

// Portfolio state
const showPortfolioThemeDialog = ref(false);
const selectedTheme = ref(null);
const portfolioCreated = ref(true);
const selectedPortfolioTheme = ref('minimal'); // Default theme

// Portfolio folders data
const portfolioFolders = ref([]);

// Classroom data for students
const studentClassmates = ref([]);
const classTeacher = ref('Teacher Name');
const classTeacherEmail = ref('');
const classmateSearchQuery = ref('');

// Filtered classmates based on search
const filteredClassmates = computed(() => {
    if (!classmateSearchQuery.value.trim()) {
        return studentClassmates.value;
    }

    const query = classmateSearchQuery.value.toLowerCase().trim();
    return studentClassmates.value.filter(classmate => {
        const name = (classmate.name || '').toLowerCase();
        return name.includes(query);
    });
});

// Helper function to get teacher initials
const getTeacherInitials = (name) => {
    if (!name) return 'T';
    const parts = name.split(' ');
    if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
};

// Helper function to get student initials
const getInitials = (name) => {
    if (!name) return '?';
    const parts = name.split(' ');
    if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
};

const isLoadingFolders = ref(false);

// Selected folder and activity state
const selectedFolder = ref(null);
const selectedActivity = ref(null);

// Folder activities data
const folderActivities = ref([]);
const isLoadingActivities = ref(false);
const itemsPerPage = 5;
const displayedPendingCount = ref(itemsPerPage);
const displayedSubmittedCount = ref(itemsPerPage);

// Student submissions
const studentSubmissions = ref([]);
const currentSubmissionIndex = ref(0);

// Computed property for current submission
const currentSubmission = computed(() => {
    return studentSubmissions.value[currentSubmissionIndex.value] || null;
});

// Navigation functions for submissions carousel
const nextSubmission = () => {
    if (currentSubmissionIndex.value < studentSubmissions.value.length - 1) {
        currentSubmissionIndex.value++;
    }
};

const prevSubmission = () => {
    if (currentSubmissionIndex.value > 0) {
        currentSubmissionIndex.value--;
    }
};

// Submitted collection state
const submittedCollection = ref([]);
const isLoadingCollection = ref(false);
const loadingCollection = isLoadingCollection; // Alias for template compatibility
const showSubmittedCollection = ref(false);

// File upload state
const selectedFile = ref(null);
const previewUrl = ref(null);
const showSubmitDialog = ref(false);
const showScoreDialog = ref(false);
const showProductUploadModal = ref(false);
const newProductCaption = ref('');
const postOutputOption = ref(false);
const isSubmitting = ref(false);
const isRequestingPost = ref(false);
const isCompilingMissing = ref(false); // Flag for missing activity compilation

// Computed: Check if in resubmission mode
// True if: has submitted work AND (has draft files loaded OR existing submission is in draft status with last_resubmit_at set)
const isResubmitting = computed(() => {
  // If has draft files loaded, we're in resubmission mode
  if (hasSubmittedWork.value && draftFiles.value.length > 0) {
    return true;
  }

  // If existing submission is in draft status AND has last_resubmit_at set, we're in resubmission mode
  // This handles the case when page is refreshed during resubmission
  if (existingSubmission.value &&
      existingSubmission.value.status === 'draft' &&
      existingSubmission.value.last_resubmit_at) {
    return true;
  }

  return false;
});

// Check if student has already submitted (reactive state)
const hasSubmittedWork = ref(false);
const existingSubmission = ref(null);
const hasScore = ref(false);
const submissionScore = ref(null);


// Draft submission state
const draftSubmission = ref(null);
const draftFiles = ref([]);
const showFilePreview = ref(false);
const showAllInstructionFilesDialog = ref(false);
const previewFile = ref(null);
const previewFileCaption = ref('');
const replaceFileInput = ref(null);
const showTurnInDialog = ref(false);
const showResubmitConfirmDialog = ref(false);
const submissionCaption = ref('');
const postToFeed = ref(false);
const showRemoveConfirmDialog = ref(false);
const fileToRemove = ref(null);
const showSubmitCompilationDialog = ref(false);
const compilationDrafts = ref({}); // Store drafts by activity ID
const selectedMissingActivity = ref(null);
const showPostToFeedConfirmDialog = ref(false);
const postToFeedSelectedFiles = ref([]); // Selected files for post to feed (multiple)
const postToFeedCaption = ref(''); // Caption for post to feed
const compilationFileInput = ref(null);

// Portfolio submission state
const showSubmitPortfolioDialog = ref(false);
const isSubmittingPortfolio = ref(false);
const portfolioEnvelope = ref(null);

// Check if activity is past due date/time
const isPastDue = computed(() => {
  try {
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
  } catch (error) {
    console.error('Error in isPastDue computed:', error);
    return false;
  }
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

  // Switch to the Activities tab
  activeTab.value = 'portfolio';

  // Save folder view state
  localStorage.setItem('student_current_view', JSON.stringify({
    activeTab: activeTab.value,
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
      // Filter only published activities
      const publishedActivities = response.data.filter(activity => activity.is_published === true);

      // Format activities for display and check submission status for each
      const activitiesWithStatus = await Promise.all(
        publishedActivities.map(async (activity) => {
          // Check if student has submitted for this activity
          let hasSubmitted = false;
          let isLate = false;
          let resubmitCount = 0;
          try {
            const submissionResponse = await axios.get(`/api/activities/${activity.id}/submissions/`);
            if (submissionResponse.data && submissionResponse.data.length > 0) {
              // Filter out draft submissions
              const actualSubmissions = submissionResponse.data.filter(sub => sub.status !== 'draft');
              if (actualSubmissions.length > 0) {
                hasSubmitted = true;
                isLate = actualSubmissions[0].is_late || false;
                resubmitCount = actualSubmissions[0].resubmit_count || 0;
              }
            }
          } catch (error) {
            console.error(`Error checking submission for activity ${activity.id}:`, error);
            showError(`Failed to check submission for activity ${activity.id}`, 'Error');
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
            resubmit_count: resubmitCount,
            scoringCriteria: scoringCriteria,
            instruction_files: activity.instruction_files || []
          };
        })
      );

      folderActivities.value = activitiesWithStatus;
      console.log('Loaded activities for student:', folderActivities.value);
    }
  } catch (error) {
    console.error('Error loading activities:', error);
    showError('Failed to load activities', 'Error');
    folderActivities.value = [];
  } finally {
    isLoadingActivities.value = false;
  }
};

// Function to load portfolio folders
const loadPortfolioFolders = async (classId = null) => {
  isLoadingFolders.value = true;
  try {
    // If a classId is provided, fetch folders for that specific class
    // Otherwise, the backend will use the student's default class
    const url = classId ? `/api/portfolio/folders/?classroom_id=${classId}` : '/api/portfolio/folders/';
    const response = await axios.get(url);

    console.log('Student API Response:', response.data); // Debug log

    if (response.data && Array.isArray(response.data)) {
      portfolioFolders.value = response.data.map(folder => {
        // Filter only published activities
        const publishedActivities = folder.activities ? folder.activities.filter(activity => activity.is_published === true) : [];
        return {
          id: folder.id,
          title: folder.name,
          items: publishedActivities.length,
          description: folder.description || ''
        };
      });
    } else {
      console.warn('API did not return an array:', response.data);
      portfolioFolders.value = [];
    }
  } catch (error) {
    console.error('Error loading folders:', error);
    showError('Failed to load portfolio folders', 'Error');
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
  currentSubmissionIndex.value = 0;

  // Clear saved view state
  localStorage.removeItem('student_current_view');
  console.log('🗑️ Cleared view state');
};

// Function to go back to activities list
const backToActivitiesList = () => {
  selectedActivity.value = null;
  studentSubmissions.value = [];
  currentSubmissionIndex.value = 0;
  hasSubmittedWork.value = false;
  showSubmittedCollection.value = false;

  // Update view state to folder only
  if (selectedFolder.value) {
    localStorage.setItem('student_current_view', JSON.stringify({
      activeTab: activeTab.value,
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
  // Hide the broken image and show placeholder
  event.target.style.display = 'none';
  // Set a fallback placeholder SVG
  event.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect fill="%23f3f4f6" width="400" height="300"/%3E%3Ctext fill="%239ca3af" font-family="sans-serif" font-size="18" dy="10.5" font-weight="bold" x="50%25" y="50%25" text-anchor="middle"%3EImage not available%3C/text%3E%3C/svg%3E';
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

    // Check if it has been resubmitted
    if (activity.resubmit_count > 0) {
      return 'resubmitted';
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
  try {
    // Fetch complete activity details from API to ensure we have all data
    const response = await axios.get(`/api/activities/${activity.id}/`);
    const activityData = response.data;
    console.log('📥 Activity data from API:', activityData);
    console.log('📎 Instruction files:', activityData.instruction_files);

    // Parse scoring criteria if it exists
    let scoringCriteria = [];
    if (activityData.scoring_criteria) {
      try {
        scoringCriteria = typeof activityData.scoring_criteria === 'string'
          ? JSON.parse(activityData.scoring_criteria)
          : activityData.scoring_criteria;
      } catch (error) {
        console.error('Error parsing scoring criteria:', error);
      }
    }

    // Format due time if available
    let formattedTime = '';
    if (activityData.due_time) {
      const [hours, minutes] = activityData.due_time.split(':');
      const hour = parseInt(hours);
      const ampm = hour >= 12 ? 'PM' : 'AM';
      const displayHour = hour % 12 || 12;
      formattedTime = `${displayHour}:${minutes} ${ampm}`;
    }

    // Set the complete activity data
    selectedActivity.value = {
      id: activityData.id,
      title: activityData.title,
      type: activityData.activity_type,
      description: activityData.description,
      date: activityData.due_date ? new Date(activityData.due_date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      }) : '',
      dueDate: activityData.due_date,
      dueTime: activityData.due_time,
      formattedTime: formattedTime,
      scoringCriteria: scoringCriteria,
      instruction_files: activityData.instruction_files || []
    };

    // Reset score state when opening new activity
    hasScore.value = false;
    submissionScore.value = null;

    // Save current view state to localStorage
    localStorage.setItem('student_current_view', JSON.stringify({
      activeTab: activeTab.value,
      selectedFolder: selectedFolder.value,
      selectedActivity: {
        id: activity.id,
        title: activity.title
      }
    }));
    console.log('💾 Saved view state: Tab:', activeTab.value, 'Activity:', activity.title);

    // Check submission status from API
    await checkSubmissionStatus(activity.id);

    // Load submissions for this activity
    await loadActivitySubmissions(activity.id);

    // Load draft submissions separately
    await loadDraftSubmissions(activity.id);
  } catch (error) {
    console.error('Error opening activity:', error);
    showError('Failed to load activity details', 'Error');
  }
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

      // Check if the submission has multiple files
      if (latestDraft.files && latestDraft.files.length > 0) {
        // Load all files from the files array
        draftFiles.value = latestDraft.files.map(f => ({
          id: f.id,
          submissionId: latestDraft.id,
          name: f.file_name || 'Uploaded file',
          type: f.file_type,
          path: f.file_url ? `${f.file_url}?t=${Date.now()}` : f.file_path,
          size: f.file_size,
          order: f.order
        }));
        console.log('✅ Loaded draft with multiple files:', draftFiles.value.length);
      } else {
        // Fallback to single file from main submission
        let filePath = latestDraft.file_url || latestDraft.file_path || latestDraft.file;
        const cacheBustedPath = filePath ? `${filePath}?t=${Date.now()}` : filePath;

        // Try to get the actual filename from the file path
        let fileName = latestDraft.caption || 'Uploaded file';
        if (filePath && fileName === 'Uploaded file') {
          const pathParts = filePath.split('/');
          const fileNameFromPath = pathParts[pathParts.length - 1];
          if (fileNameFromPath && !fileNameFromPath.includes('?')) {
            fileName = fileNameFromPath;
          }
        }

        draftFiles.value = [{
          id: latestDraft.id,
          name: fileName,
          type: latestDraft.file_type,
          path: cacheBustedPath,
          resubmit_count: latestDraft.resubmit_count || 0
        }];
      }
      
      console.log('✅ Loaded draft submission:', draftSubmission.value);
      console.log('📎 Draft files:', draftFiles.value);
      console.log('📊 Resubmit count:', latestDraft.resubmit_count);
    } else {
      draftSubmission.value = null;
      draftFiles.value = [];
      console.log('ℹ️ No draft submissions found');
    }
  } catch (error) {
    console.error('❌ Error loading draft submissions:', error);
    showError('Failed to load draft submissions', 'Error');
  }
};

// Load submissions for the current activity
const loadActivitySubmissions = async (activityId) => {
  try {
    const response = await axios.get(`/api/activities/${activityId}/submissions/`);
    console.log('📥 API Response - Submissions:', response.data);

    if (response.data && response.data.length > 0) {
      // Map API response to display format
      // If a submission has multiple files, create separate entries for each file
      studentSubmissions.value = [];
      currentSubmissionIndex.value = 0; // Reset carousel index
      
      response.data.forEach(submission => {
        console.log('🖼️ Processing submission:', {
          id: submission.id,
          caption: submission.caption,
          file_type: submission.file_type,
          has_files: !!submission.files,
          files_count: submission.files?.length || 0,
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

        // Check if submission has multiple files
        if (submission.files && submission.files.length > 0) {
          // Create an entry for each file
          submission.files.forEach((file, index) => {
            studentSubmissions.value.push({
              id: file.id,
              submissionId: submission.id,
              activityId: activityId,
              caption: file.file_name || submission.caption || `File ${index + 1}`,
              previewUrl: file.file_url || file.file_path,
              isImage: file.file_type === 'image',
              date: new Date(submission.submitted_at).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
              }),
              status: submission.status,
              score: submission.score,
              feedback: submission.feedback,
              is_late: submission.is_late || false,
              loadError: false,
              order: file.order || index
            });
          });
        } else {
          // Fallback to single file from main submission
          let previewUrl = submission.file_url || submission.file_path || submission.file;
          
          studentSubmissions.value.push({
            id: submission.id,
            submissionId: submission.id,
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
          });
        }
      });
      
      console.log('✅ Total submission files loaded:', studentSubmissions.value.length);
    } else {
      studentSubmissions.value = [];
      console.log('⚠️ No submissions found');
    }
  } catch (error) {
    console.error('❌ Error loading submissions:', error);
    showError('Failed to load submissions', 'Error');
    studentSubmissions.value = [];
  }
};

const checkSubmissionStatus = async (activityId) => {
  try {
    const response = await axios.get(`/api/activities/${activityId}/submissions/?include_drafts=true`);

    // Check if there are any submissions (including drafts)
    if (response.data && response.data.length > 0) {
      // Separate drafts and actual submissions
      const actualSubmissions = response.data.filter(sub => sub.status !== 'draft');
      const draftSubmissions = response.data.filter(sub => sub.status === 'draft');

      // Check if draft is in resubmission mode (has last_resubmit_at set)
      if (draftSubmissions.length > 0) {
        const draft = draftSubmissions[0];

        // If draft has last_resubmit_at, it's in resubmission mode - load it
        if (draft.last_resubmit_at) {
          console.log('🔄 Found draft in resubmission mode, loading for editing...');
          hasSubmittedWork.value = true;
          existingSubmission.value = draft;

          // Check if the draft has multiple files
          if (draft.files && draft.files.length > 0) {
            draftFiles.value = draft.files.map(f => ({
              id: f.id,
              submissionId: draft.id,
              name: f.file_name || 'Uploaded file',
              type: f.file_type,
              path: f.file_url ? `${f.file_url}?t=${Date.now()}` : f.file_path,
              size: f.file_size,
              order: f.order,
              resubmit_count: draft.resubmit_count || 0
            }));
          } else {
            // Fallback to single file
            const filePath = draft.file_url || draft.file_path;
            const cacheBustedPath = filePath ? `${filePath}?t=${Date.now()}` : filePath;

            // Try to get actual filename
            let fileName = draft.caption || 'Resubmitting work';
            if (filePath && fileName === 'Resubmitting work') {
              const pathParts = filePath.split('/');
              const fileNameFromPath = pathParts[pathParts.length - 1];
              if (fileNameFromPath && !fileNameFromPath.includes('?')) {
                fileName = fileNameFromPath;
              }
            }

            draftFiles.value = [{
              id: draft.id,
              name: fileName,
              type: draft.file_type,
              path: cacheBustedPath,
              resubmit_count: draft.resubmit_count || 0
            }];
          }

          console.log('✅ Loaded draft for resubmission:', draft.id);
          console.log('📊 Resubmit count:', draft.resubmit_count || 0);

          // IMPORTANT: Return early to prevent overwriting with actual submission
          return;
        } else if (actualSubmissions.length === 0) {
          // Draft without last_resubmit_at and no actual submissions - this shouldn't happen
          // but handle it by treating as not submitted
          console.log('⚠️ Found orphan draft, treating as not submitted');
          hasSubmittedWork.value = false;
          existingSubmission.value = null;
        }
      }

      if (actualSubmissions.length > 0) {
        hasSubmittedWork.value = true;
        // Get the LATEST submission (most recent submitted_at)
        const latestSubmission = actualSubmissions.reduce((latest, current) => {
          const latestDate = new Date(latest.submitted_at || 0);
          const currentDate = new Date(current.submitted_at || 0);
          return currentDate > latestDate ? current : latest;
        });
        existingSubmission.value = latestSubmission;
        console.log('📌 Using LATEST submission:', latestSubmission.id, 'submitted at:', latestSubmission.submitted_at);

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
      } else {
        hasSubmittedWork.value = false;
        existingSubmission.value = null;
        hasScore.value = false;
        submissionScore.value = null;
        console.log('ℹ️ No actual submissions found');
      }
    } else {
      hasSubmittedWork.value = false;
      existingSubmission.value = null;
      hasScore.value = false;
      submissionScore.value = null;
      console.log('ℹ️ No submissions found');
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

      // Load user data including classroom
      const user = checkResponse.data.user;
      currentUser.value = {
        name: user.full_name || user.username || 'Student Name',
        email: user.email || 'student@example.com',
        role: user.role || 'student',
        classroom: user.classroom?.name || null,
        classroom_id: user.classroom?.id || null
      };

      console.log('✅ Loaded user classroom:', currentUser.value.classroom, 'ID:', currentUser.value.classroom_id);
      return true;
    }
  } catch (error) {
    // Not authenticated, try to create session
    try {
      const authResponse = await axios.post('/api/validate-session/', {
        role: 'student'
      });
      console.log('Authentication successful:', authResponse.data.user);

      // Load user data including classroom
      const user = authResponse.data.user;
      currentUser.value = {
        name: user.full_name || user.username || 'Student Name',
        email: user.email || 'student@example.com',
        role: user.role || 'student',
        classroom: user.classroom?.name || null,
        classroom_id: user.classroom?.id || null
      };

      console.log('✅ Loaded user classroom:', currentUser.value.classroom, 'ID:', currentUser.value.classroom_id);
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
  isLoadingCompilationStatus.value = true;
  try {
    // First, get the current user's classroom information
    let classroomId = null;

    // Try to get classroom ID from currentUser
    if (currentUser.value && currentUser.value.classroom_id) {
      classroomId = currentUser.value.classroom_id;
      console.log('📚 Using classroom ID from currentUser:', classroomId);
    }
    // Fallback to selectedClass
    else if (selectedClass.value && selectedClass.value.id) {
      classroomId = selectedClass.value.id;
      console.log('📚 Using classroom ID from selectedClass:', classroomId);
    }
    // Last resort: fetch user profile to get classroom
    else {
      try {
        const userResponse = await axios.get('/api/user/profile/');
        if (userResponse.data && userResponse.data.classroom_id) {
          classroomId = userResponse.data.classroom_id;
          currentUser.value.classroom_id = classroomId;
          console.log('📚 Fetched classroom ID from user profile:', classroomId);
        }
      } catch (profileError) {
        console.warn('Could not fetch user profile:', profileError);
      }
    }

    if (!classroomId) {
      console.log('⚠️ No classroom ID found, skipping portfolio compilation check');
      portfolioData.value.teacher_requested_compilation = false;
      return;
    }

    // Check for portfolio compilation notification using the unique classroom ID
    console.log(`🔍 Checking portfolio compilation status for classroom ID: ${classroomId}`);
    const response = await axios.get(`/api/notifications/portfolio-compilation/${classroomId}/`)
      .catch(error => {
        console.error('❌ API Error:', error.response?.status, error.response?.data);
        if (error.response && error.response.status === 404) {
          // Endpoint not found, treat as if compilation not requested
          console.log('Portfolio compilation endpoint not found, treating as not requested');
          return { data: { compilation_requested: false } };
        }
        // Re-throw other errors
        throw error;
      });

    console.log('📥 API Response:', response.data);
    portfolioData.value.teacher_requested_compilation = response.data?.compilation_requested || false;

    if (portfolioData.value.teacher_requested_compilation) {
      console.log('✅ Portfolio compilation has been requested by teacher');
      console.log('📊 Response data:', response.data);
    } else {
      console.log('ℹ️ Portfolio compilation not yet requested');
      console.log('📊 Response data:', response.data);
    }
  } catch (error) {
    console.error('❌ Error checking portfolio compilation status:', error);
    // Only show error if it's not a 404
    if (!error.response || error.response.status !== 404) {
      showError('Failed to check portfolio compilation status', 'Error');
    }
    portfolioData.value.teacher_requested_compilation = false;
  } finally {
    isLoadingCompilationStatus.value = false;
  }
};

// Load portfolio folders when component mounts
// Load classmates data
const loadClassmates = async () => {
    try {
        const response = await axios.get('/api/classrooms/');
        console.log('📊 Classroom API Response:', response.data);

        if (response.data && response.data.classrooms && response.data.classrooms.length > 0) {
            const currentClassroom = response.data.classrooms[0];

            // Filter out the current student from the list
            studentClassmates.value = (currentClassroom.students || []).filter(s => s.id !== currentUser.value.id);

            // Get teacher name - try multiple possible field names
            if (currentClassroom.teacher_name) {
                classTeacher.value = currentClassroom.teacher_name;
            } else if (currentClassroom.teacher && currentClassroom.teacher.name) {
                classTeacher.value = currentClassroom.teacher.name;
            } else if (currentClassroom.teacher && currentClassroom.teacher.username) {
                classTeacher.value = currentClassroom.teacher.username;
            } else {
                // Fallback: get from current user's classroom teacher
                classTeacher.value = currentUser.value.classroom?.teacher?.name || 'Teacher Name';
            }

            // Get teacher email
            if (currentClassroom.teacher_email) {
                classTeacherEmail.value = currentClassroom.teacher_email;
            } else if (currentClassroom.teacher && currentClassroom.teacher.email) {
                classTeacherEmail.value = currentClassroom.teacher.email;
            } else {
                classTeacherEmail.value = currentUser.value.classroom?.teacher?.email || '';
            }

            console.log('✅ Loaded classmates:', studentClassmates.value.length);
            console.log('👨‍🏫 Class Adviser:', classTeacher.value);
            console.log('📧 Adviser Email:', classTeacherEmail.value);
        }
    } catch (error) {
        console.error('❌ Error loading classmates:', error);
        studentClassmates.value = [];
    }
};

onMounted(async () => {
  console.log('Sroom.vue mounted. Initial className prop:', props.className);
  const authenticated = await authenticateWithBackend();
  if (authenticated) {
    await loadPortfolioFolders();
    await checkPortfolioCompilationStatus(); // Initial check
    await checkExistingEnvelope();
    await loadClassmates();

    // Restore previous view state if it exists
    const savedView = localStorage.getItem('student_current_view');
    if (savedView) {
      try {
        const viewState = JSON.parse(savedView);
        if (viewState.activeTab) activeTab.value = viewState.activeTab;
        if (viewState.selectedFolder) {
          selectedFolder.value = viewState.selectedFolder;
          await loadFolderActivities(viewState.selectedFolder.id);
          if (viewState.selectedActivity) {
            const activity = folderActivities.value.find(a => a.id === viewState.selectedActivity.id);
            if (activity) {
              selectedActivity.value = activity;
              await checkSubmissionStatus(activity.id);
              await loadActivitySubmissions(activity.id);
              await loadDraftSubmissions(activity.id);
            }
          }
        }
      } catch (error) {
        console.error('❌ Error restoring view state:', error);
        localStorage.removeItem('student_current_view');
      }
    }
  }

  // Add all event listeners
  document.addEventListener('click', handleDocumentClick, true);
  document.addEventListener('click', handleClickOutside);
  window.addEventListener('classChanged', handleClassChange);
  window.addEventListener('subjectChanged', handleSubjectChange);
  const folderEventHandler = () => { if (!selectedFolder.value) loadPortfolioFolders(); };
  window.addEventListener('folderCreated', folderEventHandler);
  window.addEventListener('folderDeleted', folderEventHandler);
  window.addEventListener('folderUpdated', folderEventHandler);
});

onUnmounted(() => {
  // Clear all event listeners
  document.removeEventListener('click', handleDocumentClick, true);
  document.removeEventListener('click', handleClickOutside);
  window.removeEventListener('classChanged', handleClassChange);
  window.removeEventListener('subjectChanged', handleSubjectChange);
  const folderEventHandler = () => { if (!selectedFolder.value) loadPortfolioFolders(); };
  window.removeEventListener('folderCreated', folderEventHandler);
  window.removeEventListener('folderDeleted', folderEventHandler);
  window.removeEventListener('folderUpdated', folderEventHandler);
});

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
const activeFolderMenuIndex = ref(null);
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

// Handle subject change from sidebar
const handleSubjectChange = async (event) => {
  const { classItem, subject } = event.detail;
  console.log('Subject changed event received in Sroom:', { classItem, subject });

  // Guard clause to prevent crash if classItem is undefined
  if (!classItem || typeof classItem.id === 'undefined') {
    console.error('Error: classItem is missing or invalid in subjectChanged event.', event.detail);
    return;
  }

  // Reload folders for the specific class to ensure the list is up-to-date
  await loadPortfolioFolders(classItem.id);

  // Now, find the corresponding folder in the updated portfolioFolders list
  const folder = portfolioFolders.value.find(f => f.title === subject);

  if (folder) {
    await openFolderContent(folder);
    console.log('✅ Successfully opened folder:', folder.title);
  } else {
    console.warn(`⚠️ Folder not found for subject: '${subject}' in class: '${classItem.name}'. This may be expected if the folder has just been created.`);
    // Clear the view as the folder isn't available
    folderActivities.value = []; // Corrected variable name
    currentFolder.value = null;
    isActivitiesView.value = false; // Go back to the main folder view
  }
};

onMounted(() => {
  document.addEventListener('click', handleDocumentClick, true);
  document.addEventListener('click', handleClickOutside);
  // Add event listener for subject changes from sidebar
  window.addEventListener('subjectChanged', handleSubjectChange);
});

onUnmounted(() => {
  document.removeEventListener('click', handleDocumentClick, true);
  document.removeEventListener('click', handleClickOutside);
  window.removeEventListener('classChanged', handleClassChange);
  // Remove event listener for subject changes
  window.removeEventListener('subjectChanged', handleSubjectChange);
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
const isReplacingFile = ref(false); // Flag to track if we're replacing a file
const uploadTabs = [
  { id: 'device', name: 'From Device', icon: 'pi pi-desktop' },
  { id: 'sketch', name: 'My Sketch', icon: 'pi pi-palette' },
  { id: 'collection', name: 'Submitted Collection', icon: 'pi pi-folder' }
];

// My Sketches state
const mySketches = ref([]);
const loadingSketches = ref(false);
const selectedSketchId = ref(null);
const selectedCollectionId = ref(null);
const activeSketchSubTab = ref('sketches');

// Watch for dialog opening to load sketches
watch(showUploadDialog, async (newValue) => {
  if (newValue) {
    if (activeUploadTab.value === 'sketch') {
      await loadMySketches();
    } else if (activeUploadTab.value === 'collection') {
      await loadSubmittedCollection();
    }
  }
});

// Watch for tab changes to load sketches when switching to sketch tab
watch(activeUploadTab, async (newValue) => {
  if (showUploadDialog.value) {
    if (newValue === 'sketch') {
      await loadMySketches();
    } else if (newValue === 'collection') {
      await loadSubmittedCollection();
    }
  }
  // Reset selected sketch when changing tabs
  selectedSketchId.value = null;
  selectedCollectionId.value = null;
  // Reset to sketches sub-tab
  activeSketchSubTab.value = 'sketches';
});

// Watch for main tab changes and save to localStorage
watch(activeTab, (newValue) => {
  const savedView = localStorage.getItem('student_current_view');
  if (savedView) {
    try {
      const viewState = JSON.parse(savedView);
      viewState.activeTab = newValue;
      localStorage.setItem('student_current_view', JSON.stringify(viewState));
      console.log('💾 Updated active tab in view state:', newValue);
    } catch (error) {
      console.error('Error updating tab in view state:', error);
    }
  }
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
    console.log('📤 Adding sketch to draft:', selectedSketch.title);

    // Convert base64 image to blob
    const base64Data = selectedSketch.image_data;
    const response = await fetch(base64Data);
    const blob = await response.blob();

    // Create a file from the blob
    const file = new File([blob], `${selectedSketch.title}.png`, { type: 'image/png' });

    // Create FormData for multi-file upload
    const formData = new FormData();
    formData.append('files', file);

    // Use the multi-file upload endpoint to ADD to existing files
    const uploadResponse = await axios.post(
      `/api/activities/${selectedActivity.value.id}/submissions/upload-files/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    console.log('✅ Sketch added to draft:', uploadResponse.data);

    // Store draft submission
    const submissionData = uploadResponse.data.submission;
    draftSubmission.value = submissionData;

    // Build draft files array from the submission's files
    if (submissionData.files && submissionData.files.length > 0) {
      draftFiles.value = submissionData.files.map(f => ({
        id: f.id,
        submissionId: submissionData.id,
        name: f.file_name,
        type: f.file_type,
        path: f.file_url ? `${f.file_url}?t=${Date.now()}` : f.file_path,
        size: f.file_size,
        order: f.order
      }));
    } else {
      // Fallback to main file
      const filePath = submissionData.file_url || submissionData.file_path || submissionData.file;
      const cacheBustedPath = filePath ? `${filePath}?t=${Date.now()}` : filePath;
      draftFiles.value = [{
        id: submissionData.id,
        name: selectedSketch.title,
        type: submissionData.file_type,
        path: cacheBustedPath,
        resubmit_count: submissionData.resubmit_count || 0
      }];
    }

    console.log('📋 Draft files:', draftFiles.value.length, 'file(s)');

    // Close dialog
    showUploadDialog.value = false;
    selectedSketchId.value = null;
    
    if (isReplacingFile.value) {
      isReplacingFile.value = false;
      showSuccess('Sketch added!', 'Updated');
    } else {
      showSuccess('Sketch added to draft!', 'Saved');
    }
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

// Select a collection item
const selectCollectionItem = (item) => {
  selectedCollectionId.value = item.id;
};

// Use selected collection item as submission
const useSelectedCollectionItem = async () => {
  if (!selectedCollectionId.value) return;

  const selectedItem = submittedCollection.value.find(i => i.id === selectedCollectionId.value);
  if (!selectedItem) return;

  isSubmitting.value = true;

  try {
    console.log('📤 Adding collection item to draft:', selectedItem.activity_title);

    // Fetch the file from the URL
    const response = await fetch(selectedItem.file_path);
    if (!response.ok) throw new Error('Failed to fetch file');

    const blob = await response.blob();

    // Determine mime type and extension
    let mimeType = blob.type;
    let extension = 'bin';
    if (selectedItem.file_type === 'image') {
      if (mimeType.includes('jpeg')) extension = 'jpg';
      else if (mimeType.includes('png')) extension = 'png';
      else if (mimeType.includes('gif')) extension = 'gif';
      else if (mimeType.includes('webp')) extension = 'webp';
      else extension = 'png';
    } else if (selectedItem.file_type === 'pdf') {
       mimeType = 'application/pdf';
       extension = 'pdf';
    }

    // Create a file from the blob
    const cleanTitle = (selectedItem.activity_title || 'submission').replace(/[^a-z0-9]/gi, '_').toLowerCase();
    const file = new File([blob], `${cleanTitle}.${extension}`, { type: mimeType });

    // Create FormData for multi-file upload
    const formData = new FormData();
    formData.append('files', file);

    // Use the multi-file upload endpoint to ADD to existing files
    const uploadResponse = await axios.post(
      `/api/activities/${selectedActivity.value.id}/submissions/upload-files/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    console.log('✅ Collection item added to draft:', uploadResponse.data);

    // Store draft submission
    const submissionData = uploadResponse.data.submission;
    draftSubmission.value = submissionData;

    // Build draft files array from the submission's files
    if (submissionData.files && submissionData.files.length > 0) {
      draftFiles.value = submissionData.files.map(f => ({
        id: f.id,
        submissionId: submissionData.id,
        name: f.file_name,
        type: f.file_type,
        path: f.file_url ? `${f.file_url}?t=${Date.now()}` : f.file_path,
        size: f.file_size,
        order: f.order
      }));
    } else {
      // Fallback to main file
      const filePath = submissionData.file_url || submissionData.file_path || submissionData.file;
      const cacheBustedPath = filePath ? `${filePath}?t=${Date.now()}` : filePath;
      draftFiles.value = [{
        id: submissionData.id,
        name: selectedItem.activity_title || 'Submitted work',
        type: submissionData.file_type,
        path: cacheBustedPath,
        resubmit_count: submissionData.resubmit_count || 0
      }];
    }

    console.log('📋 Draft files:', draftFiles.value.length, 'file(s)');

    // Close dialog
    showUploadDialog.value = false;
    selectedCollectionId.value = null;
    
    if (isReplacingFile.value) {
      isReplacingFile.value = false;
      showSuccess('Collection item added!', 'Updated');
    } else {
      showSuccess('Collection item added to draft!', 'Saved');
    }

  } catch (error) {
    console.error('❌ Error using collection item:', error);
    showError('Failed to use collection item', 'Error');
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
  const files = Array.from(event.target.files);
  if (!files || files.length === 0) return;

  isSubmitting.value = true;

  try {
    console.log(`📤 Uploading ${files.length} file(s) as draft submission...`);

    const formData = new FormData();
    
    // Append all files to FormData
    files.forEach((file, index) => {
      formData.append('files', file);
      console.log(`📎 File ${index + 1}: ${file.name}`);
    });

    // Use the new multi-file upload endpoint
    const response = await axios.post(
      `/api/activities/${selectedActivity.value.id}/submissions/upload-files/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    console.log('✅ Files uploaded successfully:', response.data);

    // Store the submission data
    const submissionData = response.data.submission;
    draftSubmission.value = submissionData;

    // Build draft files array from the submission's files
    if (submissionData.files && submissionData.files.length > 0) {
      draftFiles.value = submissionData.files.map(file => ({
        id: file.id,
        submissionId: submissionData.id,
        name: file.file_name,
        type: file.file_type,
        path: file.file_url ? `${file.file_url}?t=${Date.now()}` : file.file_path,
        size: file.file_size,
        order: file.order
      }));
    } else {
      // Fallback to main file if no files array
      const filePath = submissionData.file_url || submissionData.file_path || submissionData.file;
      const cacheBustedPath = filePath ? `${filePath}?t=${Date.now()}` : filePath;
      draftFiles.value = [{
        id: submissionData.id,
        name: files[0].name,
        type: submissionData.file_type,
        path: cacheBustedPath,
        resubmit_count: submissionData.resubmit_count || 0
      }];
    }

    console.log('📋 Draft files:', draftFiles.value);
    console.log('📊 Uploaded count:', response.data.uploaded_count);

    // Force Vue to update the DOM
    await nextTick();

    // Close upload dialog
    showUploadDialog.value = false;
    
    if (isReplacingFile.value) {
      isReplacingFile.value = false;
      showSuccess('Files replaced successfully!', 'Updated');
    } else {
      showSuccess(`${files.length} file(s) added as draft!`, 'Saved');
    }

    // Reset file input
    if (autoSaveFileInput.value) {
      autoSaveFileInput.value.value = '';
    }
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

// Open Turn In Dialog and pre-populate caption from draft
const openTurnInDialog = () => {
  // Always show the Turn In dialog (not the resubmission confirmation)
  // Pre-populate caption from draft submission if it exists
  if (draftSubmission.value && draftSubmission.value.caption) {
    submissionCaption.value = draftSubmission.value.caption;
    console.log('📝 Pre-populated caption from draft:', submissionCaption.value);
  } else {
    submissionCaption.value = '';
  }

  // Reset post to feed checkbox
  postToFeed.value = false;

  // Show the Turn In dialog
  showTurnInDialog.value = true;
  console.log('📤 Opening Turn In dialog');
};

// Confirm resubmission and turn in the work
const confirmResubmit = async () => {
  if (draftFiles.value.length === 0) {
    showWarning('Please add a file first', 'No File');
    return;
  }

  isSubmitting.value = true;
  showResubmitConfirmDialog.value = false;

  try {
    console.log('🔄 Confirming resubmission...');

    // Get the draft submission ID
    const draftId = draftFiles.value[0].id;

    // Turn in by changing status from draft to unscored
    const response = await axios.put(`/api/submissions/${draftId}/`, {
      status: 'unscored'
    });

    console.log('✅ Resubmission successful:', response.data);
    console.log('📊 New resubmit count:', response.data.resubmit_count);

    // Update state
    hasSubmittedWork.value = true;
    existingSubmission.value = response.data;
    draftSubmission.value = null;
    draftFiles.value = [];
    submissionCaption.value = '';
    postToFeed.value = false;

    // Reload submissions
    await loadActivitySubmissions(selectedActivity.value.id);

    showSuccess(
      `Work resubmitted successfully! (Resubmission #${response.data.resubmit_count})`,
      'Resubmitted'
    );
  } catch (error) {
    console.error('❌ Error resubmitting work:', error);
    showError(
      error.response?.data?.error || 'Failed to resubmit work',
      'Resubmit Failed'
    );
  } finally {
    isSubmitting.value = false;
  }
};

// Turn in the draft submission
const turnInDraft = async () => {
  if (draftFiles.value.length === 0) {
    showWarning('Please add a file first', 'No File');
    return;
  }

  isSubmitting.value = true;

  try {
    console.log(`📤 Turning in ${draftFiles.value.length} file(s)...`);

    // Get the submission ID from the first draft file
    // All files should belong to the same submission
    const submissionId = draftFiles.value[0].submissionId || draftFiles.value[0].id;
    
    console.log('📤 Turning in draft submission:', submissionId);

    // Turn in the draft submission (this will turn in all associated files)
    const response = await axios.put(
      `/api/submissions/${submissionId}/`,
      {
        status: 'unscored',
        is_draft: false,
        caption: submissionCaption.value || `${draftFiles.value.length} file(s) submitted`,
        post_to_feed: postToFeed.value
      }
    );

    console.log('✅ Submission turned in successfully with', draftFiles.value.length, 'file(s)');

    // Show success message
    showSuccess(`Work submitted successfully! (${draftFiles.value.length} file${draftFiles.value.length > 1 ? 's' : ''})`, 'Submitted');

    // Update state
    hasSubmittedWork.value = true;
    existingSubmission.value = response.data;
    draftSubmission.value = null;
    submissionCaption.value = '';
    postToFeed.value = false;
    showTurnInDialog.value = false;

    // Clear draft files since they're now submitted
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
      error.response?.data?.error || 'Failed to turn in submission',
      'Turn In Failed'
    );
  } finally {
    isSubmitting.value = false;
  }
};

// Handle resubmission - Show confirmation dialog
const handleResubmit = () => {
  // Show confirmation dialog instead of immediately converting
  showResubmitConfirmDialog.value = true;
  console.log('🔄 Showing resubmission confirmation dialog');
};

// Confirm resubmission - Enter resubmission mode OR Submit Turn In
const confirmResubmitAction = async () => {
  // If we are in Turn In dialog, proceed with final submission (spending a resubmit attempt)
  if (showTurnInDialog.value) {
      showResubmitConfirmDialog.value = false;
      await executeSubmission();
      return;
  }

  if (!selectedActivity.value || !existingSubmission.value) return;

  try {
    console.log('🔄 Entering resubmission mode...');

    // Close confirmation dialog
    showResubmitConfirmDialog.value = false;

    // Call backend API to convert submission to draft status
    // This will increment resubmit_count and set last_resubmit_at
    const response = await axios.put(`/api/submissions/${existingSubmission.value.id}/`, {
      status: 'draft'
    });

    console.log('✅ Backend response:', response.data);
    console.log('📊 New resubmit count:', response.data.resubmit_count);
    console.log('📅 Last resubmit at:', response.data.last_resubmit_at);

    // Update local state with backend response
    existingSubmission.value = response.data;

    // Load existing submission file into draft for editing
    const filePath = response.data.file_url || response.data.file_path;
    const cacheBustedPath = filePath ? `${filePath}?t=${Date.now()}` : filePath;

    draftFiles.value = [{
      id: response.data.id,
      name: response.data.caption || 'Submitted file',
      type: response.data.file_type,
      path: cacheBustedPath,
      resubmit_count: response.data.resubmit_count || 0
    }];

    console.log('✅ Loaded existing file for resubmission');
    console.log('✅ isResubmitting is now:', isResubmitting.value);

    // Show success message
    showSuccess('You can now edit and resubmit your work', 'Resubmission Mode');
  } catch (error) {
    console.error('❌ Error preparing resubmission:', error);
    showError(
      error.response?.data?.error || 'Failed to enter resubmission mode',
      'Error'
    );
  }
};

// Toggle file selection for post to feed (multiple selection)
const toggleFileSelection = (submission) => {
  const index = postToFeedSelectedFiles.value.findIndex(f => f.id === submission.id);
  if (index === -1) {
    postToFeedSelectedFiles.value.push(submission);
  } else {
    postToFeedSelectedFiles.value.splice(index, 1);
  }
};

// Check if a file is selected
const isFileSelected = (submission) => {
  return postToFeedSelectedFiles.value.some(f => f.id === submission.id);
};

// Select all files
const selectAllFiles = () => {
  postToFeedSelectedFiles.value = [...studentSubmissions.value];
};

// Deselect all files
const deselectAllFiles = () => {
  postToFeedSelectedFiles.value = [];
};

// Open Post to Feed dialog and pre-select all files if only one
const openPostToFeedDialog = () => {
  // Reset state
  postToFeedCaption.value = '';
  
  // Pre-select all files if there's only one, otherwise let user choose
  if (studentSubmissions.value.length === 1) {
    postToFeedSelectedFiles.value = [...studentSubmissions.value];
  } else {
    postToFeedSelectedFiles.value = [];
  }
  
  showPostToFeedConfirmDialog.value = true;
};

// Confirm and request to post existing submission to feed
const confirmPostToFeed = async () => {
  if (!existingSubmission.value) {
    showError('No submission found', 'Error');
    return;
  }

  if (postToFeedSelectedFiles.value.length === 0) {
    showError('Please select at least one file to post', 'Error');
    return;
  }

  try {
    isRequestingPost.value = true;
    console.log('📢 Requesting to post submission to feed:', existingSubmission.value.id);
    console.log('📁 Selected files:', postToFeedSelectedFiles.value.length);
    console.log('📝 Caption:', postToFeedCaption.value);

    // Get file IDs for the selected files
    const selectedFileIds = postToFeedSelectedFiles.value.map(f => f.id);

    // Update the submission to request posting to feed with selected files info
    const response = await axios.put(`/api/submissions/${existingSubmission.value.id}/`, {
      post_to_feed: true,
      post_file_ids: selectedFileIds,
      post_caption: postToFeedCaption.value || ''
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

      // Close confirmation dialog and reset state
      showPostToFeedConfirmDialog.value = false;
      postToFeedSelectedFiles.value = [];
      postToFeedCaption.value = '';

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
    console.log('🗑️ Removing draft file:', fileToRemove.value);

    // Check if this is a SubmissionFile (has submissionId) or the main submission
    const isSubmissionFile = fileToRemove.value.submissionId !== undefined;
    
    if (isSubmissionFile) {
      // Delete individual file from multi-file submission
      console.log('📎 Deleting individual file from submission');
      await axios.delete(`/api/submissions/${fileToRemove.value.submissionId}/files/${fileToRemove.value.id}/`);
      
      // Remove from local state
      draftFiles.value = draftFiles.value.filter(f => f.id !== fileToRemove.value.id);
      
      // Reorder remaining files
      draftFiles.value.forEach((f, index) => {
        f.order = index;
      });
      
      showSuccess('File removed successfully', 'Removed');
    } else {
      // Legacy: Handle single-file submission removal
      const isResubmittingMode = draftSubmission.value && draftSubmission.value.last_resubmit_at;

      if (isResubmittingMode) {
        // In resubmission mode: Just clear the UI, keep the submission record
        console.log('🔄 Resubmission mode: Clearing UI but keeping submission record');
        draftFiles.value = [];
        showSuccess('File removed. You can attach new files to resubmit.', 'Removed');
      } else {
        // Normal mode: Delete the entire submission
        console.log('📝 Normal mode: Deleting submission from database');
        await axios.delete(`/api/submissions/${fileToRemove.value.id}/`);
        
        draftFiles.value = draftFiles.value.filter(f => f.id !== fileToRemove.value.id);
        if (draftFiles.value.length === 0) {
          draftSubmission.value = null;
        }
        showSuccess('File removed successfully', 'Removed');
      }
    }

    console.log('✅ File removed. Remaining files:', draftFiles.value.length);

    // Close dialog and reset
    showRemoveConfirmDialog.value = false;
    fileToRemove.value = null;
  } catch (error) {
    console.error('❌ Error removing file:', error);
    const errorMsg = error.response?.data?.error || error.response?.data?.detail || 'Failed to remove file';
    showError(errorMsg, 'Error');
  }
};

// View draft file
const viewDraftFile = async (file) => {
  try {
    console.log('👁️ viewDraftFile called with:', file);
    
    // Check if this is a SubmissionFile (has submissionId) or main submission
    const isSubmissionFile = file.submissionId !== undefined;
    
    // Check if this is a studentSubmission object (has previewUrl and activityId)
    const isStudentSubmission = file.previewUrl !== undefined && file.activityId !== undefined;
    
    if (isStudentSubmission) {
      // For student submissions, use the previewUrl directly
      console.log('📎 StudentSubmission - using previewUrl:', file.previewUrl);
      previewFile.value = {
        ...file,
        path: file.previewUrl,
        type: file.isImage ? 'image' : 'pdf',
        name: file.caption || 'Submitted work',
        isSubmissionFile: false
      };
      previewFileCaption.value = file.caption || 'Submitted work';
    } else if (isSubmissionFile) {
      // For individual files, use the file path directly
      console.log('📎 SubmissionFile - using direct path:', file.path);
      previewFile.value = {
        ...file,
        path: file.path,
        isSubmissionFile: true
      };
      previewFileCaption.value = file.name;
    } else {
      // Legacy: Fetch full submission data
      const response = await axios.get(`/api/submissions/${file.id}/`);
      console.log('📥 Loaded submission data:', response.data);

      let filePath = response.data.file_url || response.data.file_path || response.data.file;
      console.log('📎 File path resolved:', filePath);

      previewFile.value = {
        ...file,
        path: filePath,
        fullData: response.data,
        isSubmissionFile: false
      };
      previewFileCaption.value = response.data.caption || file.name;
    }

    showFilePreview.value = true;
    console.log('👁️ Preview file set to:', previewFile.value);
  } catch (error) {
    console.error('❌ Error loading file:', error);
    showError('Failed to load file preview', 'Error');
  }
};

// Get absolute URL for a file path
const getAbsoluteFileUrl = (filePath) => {
  if (!filePath) return '';
  const cleanPath = filePath.split('?')[0];
  return cleanPath.startsWith('http') 
    ? cleanPath 
    : `${window.location.origin}${cleanPath}`;
};

// Open file in new tab (for viewing PDFs, documents, etc.)
const openFileInNewTab = (filePath, fileType = null) => {
  console.log('📂 Opening file:', filePath, 'Type:', fileType);
  if (!filePath) {
    showError('File path not available', 'Error');
    return;
  }
  
  // Remove cache busting parameter if present for cleaner URL
  const cleanPath = filePath.split('?')[0];
  console.log('📂 Clean path:', cleanPath);
  
  // Build absolute URL for the file
  const absoluteUrl = getAbsoluteFileUrl(filePath);
  
  console.log('📂 Opening URL:', absoluteUrl);
  
  // Check file extension to determine how to open
  const extension = cleanPath.split('.').pop().toLowerCase();
  console.log('📂 File extension:', extension);
  
  // Determine if this is a Word document by extension or file type
  const isWordDoc = extension === 'doc' || extension === 'docx' || fileType === 'document';
  const isPdf = extension === 'pdf' || fileType === 'pdf';
  
  if (isWordDoc) {
    // For Word documents, always use Google Docs Viewer
    // Note: On localhost, this won't work as Google can't access local files
    const googleViewerUrl = `https://docs.google.com/gview?url=${encodeURIComponent(absoluteUrl)}&embedded=false`;
    console.log('📂 Opening Word doc with Google Viewer:', googleViewerUrl);
    window.open(googleViewerUrl, '_blank');
  } else if (isPdf) {
    // For PDFs, open directly - browsers display PDFs inline
    console.log('📂 Opening PDF directly');
    window.open(absoluteUrl, '_blank');
  } else {
    // For images and other files, open directly
    console.log('📂 Opening file directly');
    window.open(absoluteUrl, '_blank');
  }
};

// fileToReplace ref for tracking which file is being replaced
const fileToReplace = ref(null);

// Replace current file - opens file picker to replace the specific file being previewed
const replaceCurrentFile = () => {
  if (!previewFile.value) return;
  
  fileToReplace.value = previewFile.value;
  
  // Create a temporary file input if it doesn't exist
  if (!replaceFileInput.value) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*,.pdf,.doc,.docx';
    input.onchange = handleReplaceFileUpload;
    replaceFileInput.value = input;
  }
  
  replaceFileInput.value.click();
};

// Handle the file replacement upload
const handleReplaceFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file || !fileToReplace.value) return;

  isSubmitting.value = true;

  try {
    console.log('🔄 Replacing file:', fileToReplace.value.name, 'with:', file.name);

    const formData = new FormData();
    formData.append('file', file);

    // Check if this is a SubmissionFile (has submissionId) or main submission
    const isSubmissionFile = fileToReplace.value.submissionId !== undefined;

    if (isSubmissionFile) {
      // Delete the old file and add new one
      await axios.delete(`/api/submissions/${fileToReplace.value.submissionId}/files/${fileToReplace.value.id}/`);
      
      // Add new file
      const uploadFormData = new FormData();
      uploadFormData.append('files', file);
      
      const response = await axios.post(
        `/api/activities/${selectedActivity.value.id}/submissions/upload-files/`,
        uploadFormData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );

      // Update draft files
      const submissionData = response.data.submission;
      draftSubmission.value = submissionData;
      
      if (submissionData.files && submissionData.files.length > 0) {
        draftFiles.value = submissionData.files.map(f => ({
          id: f.id,
          submissionId: submissionData.id,
          name: f.file_name,
          type: f.file_type,
          path: f.file_url ? `${f.file_url}?t=${Date.now()}` : f.file_path,
          size: f.file_size,
          order: f.order
        }));
      }
    } else {
      // Legacy: Update the main submission file
      const response = await axios.put(
        `/api/submissions/${fileToReplace.value.id}/`,
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );

      draftSubmission.value = response.data;
      
      const filePath = response.data.file_url || response.data.file_path || response.data.file;
      const cacheBustedPath = filePath ? `${filePath}?t=${Date.now()}` : filePath;
      
      // Update the file in draftFiles
      const fileIndex = draftFiles.value.findIndex(f => f.id === fileToReplace.value.id);
      if (fileIndex !== -1) {
        draftFiles.value[fileIndex] = {
          ...draftFiles.value[fileIndex],
          name: file.name,
          type: response.data.file_type,
          path: cacheBustedPath
        };
      }
    }

    // Close preview and show success
    showFilePreview.value = false;
    showSuccess('File replaced successfully!', 'Updated');
    
    // Reset
    fileToReplace.value = null;
    if (replaceFileInput.value) {
      replaceFileInput.value.value = '';
    }

  } catch (error) {
    console.error('❌ Error replacing file:', error);
    showError(error.response?.data?.error || 'Failed to replace file', 'Error');
  } finally {
    isSubmitting.value = false;
  }
};

// Open replace file dialog (legacy - opens upload dialog)
const openReplaceFileDialog = () => {
  isReplacingFile.value = true;
  showFilePreview.value = false; // Close preview dialog
  showUploadDialog.value = true; // Open upload dialog
  activeUploadTab.value = 'device'; // Default to device tab
  console.log('🔄 Opening replace file dialog');
};

// Save caption from preview dialog
const savePreviewCaption = async () => {
  if (!previewFile.value || !previewFileCaption.value) return;

  try {
    console.log('💾 Saving caption:', previewFileCaption.value);

    // Update the draft with new caption
    const response = await axios.put(
      `/api/submissions/${previewFile.value.id}/`,
      {
        caption: previewFileCaption.value,
        is_draft: true
      }
    );

    console.log('✅ Caption saved successfully');

    // Update draftSubmission (preserves resubmit_count)
    draftSubmission.value = response.data;

    // Update draftFiles array
    if (draftFiles.value.length > 0) {
      draftFiles.value[0].name = previewFileCaption.value;
    }

    // Update preview
    previewFile.value.name = previewFileCaption.value;
    previewFile.value.fullData = response.data;

    showSuccess('Caption saved successfully!', 'Saved');
    console.log('📊 Resubmit count preserved:', response.data.resubmit_count);
  } catch (error) {
    console.error('❌ Error saving caption:', error);
    showError('Failed to save caption', 'Error');
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
  // Use actualClassName which correctly prioritizes: selectedClass > currentUser.classroom > props.className
  envelopeDesign.value.className = actualClassName.value;

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
    // Save to backend - use actualClassName as fallback which correctly prioritizes student's classroom
    const response = await axios.post('/api/portfolio-envelope/create/', {
      title: envelopeDesign.value.title,
      student_name: envelopeDesign.value.studentName,
      class_name: envelopeDesign.value.className || actualClassName.value,
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
    // Fetch existing envelope data - use actualClassName which correctly prioritizes student's classroom
    const classNameValue = actualClassName.value;
    console.log('Checking for existing envelope in class (from fetch):', classNameValue); // Debugging line
    if (!classNameValue) {
      console.error('Class name is missing, cannot fetch portfolio envelope.');
      return;
    }
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
    envelopeDesign.value.className = actualClassName.value;
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
    // Use actualClassName which correctly prioritizes student's classroom
    const classNameValue = actualClassName.value;
    const response = await axios.get(`/api/portfolio-envelope/activities/${encodeURIComponent(classNameValue)}/`);

    if (response.data) {
      // Clone the data to prevent circular reference issues
      // Use submitted_activities which contains ONLY SCORED submissions
      const scoredActivities = JSON.parse(JSON.stringify(response.data.submitted_activities || []));
      const missingActivitiesData = JSON.parse(JSON.stringify(response.data.missing_activities || []));

      portfolioActivities.value = scoredActivities;
      missingActivities.value = missingActivitiesData;
      currentActivityIndex.value = 0;

      console.log(`✅ Loaded ${portfolioActivities.value.length} SCORED activities (${missingActivities.value.length} missing)`);
      console.log(`   - Submitted: ${response.data.submitted_count || 0}`);
      console.log(`   - Resubmitted: ${response.data.resubmitted_count || 0}`);
      console.log(`   - Late: ${response.data.late_count || 0}`);
      console.log(`   - Missing: ${response.data.missing_count || 0}`);
    }
  } catch (error) {
    console.error('❌ Error fetching portfolio activities:', error);
    console.error('Error details:', error.response?.data || error.message);
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
    // Use actualClassName which correctly prioritizes student's classroom
    const classNameValue = actualClassName.value;

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
  selectedMissingActivity.value = activity;

  // Check if there's an existing draft for this activity
  if (compilationDrafts.value[activity.id]) {
    const draft = compilationDrafts.value[activity.id];
    submissionCaption.value = draft.caption || '';
    draftFiles.value = draft.files || [];
  } else {
    submissionCaption.value = '';
    draftFiles.value = [];
  }

  // Open the Turn In Dialog
  showTurnInDialog.value = true;
};

// Edit existing compilation draft
const editCompilation = (activity) => {
  console.log('Editing compilation for:', activity.title);
  compileActivity(activity); // Reuse the same function
};



// Wrapper for Submit (handles confirmation)
const submitTurnInWork = () => {
  const activity = selectedActivity.value || selectedMissingActivity.value;

  if (!activity) {
    showWarning('No activity selected', 'Error');
    return;
  }

  if (draftFiles.length === 0) {
    showWarning('Please add a file first', 'No File');
    return;
  }

  const isCompilation = !!selectedMissingActivity.value;

  // Check if this is a resubmission (regular activity, existing submission, not draft)
  if (!isCompilation && existingSubmission.value && existingSubmission.value.status !== 'draft') {
      showResubmitConfirmDialog.value = true;
      return;
  }

  executeSubmission();
};

// Actual Submission Logic (renamed from submitTurnInWork)
const executeSubmission = async () => {
  // Check for either selectedActivity (regular) or selectedMissingActivity (compilation)
  const activity = selectedActivity.value || selectedMissingActivity.value;

  if (!activity) {
    showWarning('No activity selected', 'Error');
    return;
  }

  if (draftFiles.length === 0) {
    showWarning('Please add a file first', 'No File');
    return;
  }

  isSubmitting.value = true;

  try {
    console.log('📤 Submitting work for activity:', activity.id, activity.title);

    const file = draftFiles.value[0]; // Get the first file

    // Check if submission is late
    const isLateSubmission = isPastDue.value;

    // Determine if this is a compilation submission (from missing activities)
    const isCompilation = !!selectedMissingActivity.value;

    // If this is a compilation (missing activity), first mark it as compiled
    if (isCompilation) {
      try {
        console.log('⚡ Marking activity as compiled before submission...');
        await axios.post('/student/compile/', {
          activity_id: activity.id
        });
        console.log('✅ Activity marked as compiled');
      } catch (compileError) {
        console.error('⚠️ Error marking as compiled:', compileError);
        // Continue with submission even if compile fails
      }
    }

    // Submit to API
    const response = await axios.post(`/api/activities/${activity.id}/submissions/`, {
      caption: submissionCaption.value || '',
      file_path: file.path, // Base64 data
      file_type: file.type,
      post_to_feed: postOutputOption.value,
      is_late: isLateSubmission,
      is_draft: false, // ✅ CRITICAL: false = final submission
      is_compilation: isCompilation // Pass this explicitly to ensure backend treats it correctly
    });

    if (response.data) {
      console.log('✅ Work submitted successfully:', response.data);

      // Update submission status
      hasSubmittedWork.value = true;
      existingSubmission.value = response.data;

      // Close dialog and reset form
      showTurnInDialog.value = false;
      submissionCaption.value = '';
      postOutputOption.value = false;
      draftFiles.value = []; // Clearing this will automatically set isResubmitting = false

      // Clear selected missing activity if it was a compilation
      if (isCompilation) {
        selectedMissingActivity.value = null;
        // Reload portfolio activities to update missing list and compiled count
        await fetchPortfolioActivities();
        showSuccess('Activity compiled and submitted successfully!', 'Compiled');
      } else {
        // Reload submissions to update the UI for regular activities
        await checkSubmissionStatus(activity.id);
        await loadActivitySubmissions(activity.id);
        showSuccess('Work submitted successfully!', 'Submitted');
      }
    }
  } catch (error) {
    console.error('❌ Error submitting work:', error);
    showError(error.response?.data?.error || 'Failed to submit work. Please try again.', 'Submission Failed');
  } finally {
    isSubmitting.value = false;
  }
};

// Save as draft
const saveAsDraft = async () => {
  if (!selectedMissingActivity.value) {
    showWarning('No activity selected', 'Error');
    return;
  }

  if (draftFiles.length === 0 && !submissionCaption.value) {
    showWarning('Please add a file or caption', 'Missing Content');
    return;
  }

  isSubmitting.value = true;

  try {
    // Save draft locally (will be sent to backend when submitted)
    compilationDrafts.value[selectedMissingActivity.value.id] = {
      activityId: selectedMissingActivity.value.id,
      caption: submissionCaption.value,
      files: [...draftFiles.value],
      savedAt: new Date().toISOString()
    };

    console.log('✅ Draft saved for activity:', selectedMissingActivity.value.id);
    showSuccess('Compilation saved as draft', 'Draft Saved');

    // Close dialog
    showTurnInDialog.value = false;

    // Clear form
    submissionCaption.value = '';
    draftFiles.value = [];
    selectedMissingActivity.value = null;
  } catch (error) {
    console.error('❌ Error saving draft:', error);
    showError('Failed to save draft', 'Error');
  } finally {
    isSubmitting.value = false;
  }
};

// Open submit compilation confirmation dialog
const openSubmitCompilationDialog = (activity) => {
  selectedMissingActivity.value = activity;
  showSubmitCompilationDialog.value = true;
};

// Submit compilation
const submitCompilation = async () => {
  if (!selectedMissingActivity.value) {
    showError('No activity selected', 'Error');
    return;
  }

  const activityId = selectedMissingActivity.value.id;
  const draft = compilationDrafts.value[activityId];

  if (!draft || !draft.files || draft.files.length === 0) {
    showError('No draft found or no file attached', 'Error');
    return;
  }

  isSubmitting.value = true;

  try {
    console.log('📤 Submitting compilation for activity:', activityId);

    const file = draft.files[0]; // Get the first file

    // Submit to backend
    const response = await axios.post(
      `/api/portfolio-envelope/submit-compilation/${activityId}/`,
      {
        file: file.path, // Base64 data
        caption: draft.caption || ''
      }
    );

    console.log('✅ Compilation submitted successfully:', response.data);

    // Remove draft from local storage
    delete compilationDrafts.value[activityId];

    // Close dialog
    showSubmitCompilationDialog.value = false;

    // Show success message
    showSuccess('Compilation submitted successfully! It will appear in your Activity Compilation.', 'Success');

    // Refresh portfolio activities to show the new submission
    await fetchPortfolioActivities();

    // Clear selected activity
    selectedMissingActivity.value = null;
  } catch (error) {
    console.error('❌ Error submitting compilation:', error);
    showError(
      error.response?.data?.error || 'Failed to submit compilation',
      'Submission Failed'
    );
  } finally {
    isSubmitting.value = false;
  }
};

// Compile activity immediately (mark as compiled)
const compileActivityNow = async (activity) => {
  if (!activity) return;

  try {
    isSubmitting.value = true;
    console.log('⚡ Compiling activity now:', activity.id);

    const response = await axios.post('/student/compile/', {
      activity_id: activity.id
    });

    if (response.data.success) {
      console.log('✅ Activity compiled successfully');

      // Update local state immediately for better UX
      missingActivities.value = missingActivities.value.filter(a => a.id !== activity.id);

      // Refresh full list from server
      await fetchPortfolioActivities();

      showSuccess('Activity compiled successfully! It is now in your Activity Compilation.', 'Compiled');
    }
  } catch (error) {
    console.error('❌ Error compiling activity:', error);
    showError(error.response?.data?.error || 'Failed to compile activity', 'Error');
  } finally {
    isSubmitting.value = false;
  }
};

// Trigger file upload for compilation
const triggerCompilationFileUpload = () => {
  if (compilationFileInput.value) {
    compilationFileInput.value.click();
  }
};

// Handle file upload for compilation
const handleCompilationFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    // Convert file to base64
    const reader = new FileReader();
    const filePath = await new Promise((resolve, reject) => {
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });

    // Determine file type
    let fileType = 'file';
    if (file.type.startsWith('image/')) {
      fileType = 'image';
    } else if (file.type === 'application/pdf') {
      fileType = 'pdf';
    }

    // Add to draft files
    const fileData = {
      id: Date.now(),
      name: file.name,
      type: fileType,
      path: filePath,
      size: file.size
    };

    draftFiles.value = [fileData]; // Only one file allowed
    console.log('✅ File added to compilation:', fileData.name);
  } catch (error) {
    console.error('❌ Error uploading file:', error);
    showError('Failed to upload file', 'Upload Error');
  }

  // Reset input
  event.target.value = '';
};

// Unified submit function that handles both regular and missing activity submissions
const submitWork = async () => {
  if (isCompilingMissing.value) {
    // If compiling missing activity, use the missing activity submission
    await submitMissingActivity();
  } else {
    // Otherwise, use regular submission
    await submitNewProduct();
  }
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
    // Use actualClassName which correctly prioritizes student's classroom
    const classNameValue = actualClassName.value;
    console.log('Checking for existing envelope in class (from checkExistingEnvelope):', classNameValue); // Debugging line
    if (!classNameValue) {
      console.error('Class name is missing, cannot fetch portfolio envelope.');
      return;
    }
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
