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
                  <!-- List of Activities Header -->
                  <div class="rounded-lg py-2 px-4">
                    <span class="text-2xl font-bold text-indigo-900">List of Activities - {{ selectedFolder.title }}</span>
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
                          Due: {{ selectedActivity.date }}<span v-if="selectedActivity.formattedTime"> at {{ selectedActivity.formattedTime }}</span>
                          <span class="text-xs block mt-1 text-gray-900/70">You cannot submit after the due date</span>
                        </span>
                      </div>
                      <div class="flex items-center gap-4 w-full sm:w-auto justify-center sm:justify-end mt-4 sm:mt-0">
                        <!-- Turn In Button - Show when not submitted and not past due -->
                        <button
                          v-if="!hasSubmittedWork && !isPastDue"
                          @click="addSampleProduct"
                          class="group flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                        >
                          <i class="pi pi-plus"></i>
                          <span>Turn in</span>
                        </button>
                        
                        <!-- Missing Badge - Show when not submitted and past due -->
                        <span
                          v-if="!hasSubmittedWork && isPastDue"
                          class="px-4 py-2 rounded-lg bg-red-100 text-red-800 flex items-center gap-2 font-medium"
                        >
                          <i class="pi pi-times-circle"></i>
                          <span>Missing - Past Due</span>
                        </span>
                        
                        <!-- Submitted Section - Show when work has been submitted -->
                        <template v-if="hasSubmittedWork">
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
                      <div class="w-40 md:w-48">
                        <span class="text-sm font-semibold text-indigo-900">Activity Title</span>
                      </div>
                      <div class="flex-1">
                        <span class="text-sm font-semibold text-indigo-900">Description</span>
                      </div>
                      <div class="w-28">
                        <span class="text-sm font-semibold text-indigo-900">Status</span>
                      </div>
                      <div class="w-28 text-center">
                        <span class="text-sm font-semibold text-indigo-900">Due Time</span>
                      </div>
                      <div class="w-36 text-right">
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
                        <div class="w-40 md:w-48">
                          <span class="font-medium text-indigo-700 transition-colors duration-100">{{ activity.title }}</span>
                        </div>
                        <div class="flex-1">
                          <span class="text-indigo-700 group-hover:text-indigo-900 transition-colors duration-200 line-clamp-2">{{ activity.description }}</span>
                        </div>
                        <div class="w-28">
                          <span v-if="getActivityStatus(activity) === 'submitted'" 
                                class="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 flex items-center gap-1 w-fit">
                            <i class="pi pi-check-circle text-xs"></i>
                            Submitted
                          </span>
                          <span v-else-if="getActivityStatus(activity) === 'missing'" 
                                class="px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 flex items-center gap-1 w-fit">
                            <i class="pi pi-times-circle text-xs"></i>
                            Missing
                          </span>
                          <span v-else 
                                class="px-2 py-1 rounded-full text-xs font-medium bg-amber-100 text-amber-800 flex items-center gap-1 w-fit">
                            <i class="pi pi-clock text-xs"></i>
                            Pending
                          </span>
                        </div>
                        <div class="w-28 text-center">
                          <span v-if="activity.formattedTime" class="text-sm text-indigo-600 font-medium">{{ activity.formattedTime }}</span>
                          <span v-else class="text-xs text-gray-400 italic">No time</span>
                        </div>
                        <div class="w-36 text-right">
                          <span class="text-sm text-indigo-600">{{ activity.date }}</span>
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
          <div class="p-4 md:p-6">
            <!-- Show designed portfolio envelope if created -->
            <div v-if="portfolioEnvelopeCreated" class="max-w-3xl mx-auto">
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
              <div v-if="isEnvelopeOpen && portfolioActivities.length > 0" class="relative">
                <!-- Portfolio Tabs with Back Button -->
                <div class="flex justify-between items-center mb-6">
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
                <div v-if="activePortfolioTab === 'all'" class="rounded-2xl shadow-xl overflow-hidden min-h-[600px] relative"
                     :style="{ background: `linear-gradient(135deg, ${envelopeDesign.color} 0%, ${adjustBrightness(envelopeDesign.color, -20)} 100%)` }">
                  
                  <!-- Pattern Overlay (matching envelope) -->
                  <div v-if="envelopeDesign.pattern === 'dots'" 
                       class="absolute inset-0 opacity-10 pointer-events-none"
                       style="background-image: radial-gradient(circle, white 2px, transparent 2px); background-size: 20px 20px;">
                  </div>
                  <div v-else-if="envelopeDesign.pattern === 'lines'" 
                       class="absolute inset-0 opacity-10 pointer-events-none"
                       style="background-image: repeating-linear-gradient(45deg, white 0, white 2px, transparent 2px, transparent 10px);">
                  </div>
                  <div v-else-if="envelopeDesign.pattern === 'grid'" 
                       class="absolute inset-0 opacity-10 pointer-events-none"
                       style="background-image: linear-gradient(white 1px, transparent 1px), linear-gradient(90deg, white 1px, transparent 1px); background-size: 20px 20px;">
                  </div>

                  <!-- Activity Display -->
                  <div class="relative p-8">
                    <!-- Activity Counter -->
                    <div class="absolute top-4 right-4 z-10 text-white px-4 py-2 rounded-full text-sm font-semibold shadow-lg"
                         :style="{ backgroundColor: adjustBrightness(envelopeDesign.color, -30) }">
                      {{ currentActivityIndex + 1 }} / {{ portfolioActivities.length }}
                    </div>

                    <!-- Activity Content -->
                    <div v-if="portfolioActivities[currentActivityIndex]">
                      <!-- Content Card with Glass Effect -->
                      <div class="bg-white/95 backdrop-blur-sm rounded-2xl p-6 shadow-2xl relative">
                      <!-- Activity Image/Preview -->
                      <div class="aspect-video bg-gradient-to-br from-white/50 to-white/30 rounded-xl mb-6 flex items-center justify-center overflow-hidden relative border-2 border-white/50">
                        <img v-if="portfolioActivities[currentActivityIndex].submission_file" 
                             :src="portfolioActivities[currentActivityIndex].submission_file"
                             alt="Activity submission"
                             class="w-full h-full object-cover"
                             @error="(e) => { e.target.style.display = 'none'; }"
                        />
                        <div v-if="!portfolioActivities[currentActivityIndex].submission_file || portfolioActivities[currentActivityIndex].submission_status === 'missing'" 
                             class="text-center flex flex-col items-center">
                          <i class="pi pi-file text-6xl text-indigo-300 mb-4"></i>
                          <p class="text-indigo-600 font-medium">
                            {{ portfolioActivities[currentActivityIndex].submission_status === 'missing' ? 'No Submission' : 'Activity' }}
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
                        class="absolute left-2 top-[200px] w-14 h-14 bg-white/90 backdrop-blur-sm rounded-full shadow-2xl flex items-center justify-center hover:bg-white hover:scale-110 transition-all duration-200 disabled:opacity-20 disabled:cursor-not-allowed z-30"
                        :style="{ borderColor: envelopeDesign.color, borderWidth: '3px' }"
                      >
                        <i class="pi pi-chevron-left text-xl" :style="{ color: envelopeDesign.color }"></i>
                      </button>
                      <button
                        @click="nextActivity"
                        :disabled="currentActivityIndex >= portfolioActivities.length - 1"
                        class="absolute right-2 top-[200px] w-14 h-14 bg-white/90 backdrop-blur-sm rounded-full shadow-2xl flex items-center justify-center hover:bg-white hover:scale-110 transition-all duration-200 disabled:opacity-20 disabled:cursor-not-allowed z-30"
                        :style="{ borderColor: envelopeDesign.color, borderWidth: '3px' }"
                      >
                        <i class="pi pi-chevron-right text-xl" :style="{ color: envelopeDesign.color }"></i>
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
              <div v-if="!isEnvelopeOpen" class="flex flex-wrap gap-3 justify-center">
                <button
                  @click="editEnvelopeDesign"
                  class="px-6 py-3 bg-white text-gray-700 font-medium rounded-lg border-2 border-gray-300 hover:border-indigo-500 hover:text-indigo-600 transition-all flex items-center gap-2 shadow-md hover:shadow-lg"
                >
                  <i class="pi pi-pencil"></i>
                  Edit Design
                </button>
                <button
                  class="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl flex items-center gap-2"
                >
                  <i class="pi pi-download"></i>
                  Download Portfolio
                </button>
                <button
                  class="px-6 py-3 bg-gradient-to-r from-green-600 to-teal-600 text-white font-medium rounded-lg hover:from-green-700 hover:to-teal-700 transition-all shadow-lg hover:shadow-xl flex items-center gap-2"
                >
                  <i class="pi pi-share-alt"></i>
                  Share Portfolio
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

// Check if student has already submitted (reactive state)
const hasSubmittedWork = ref(false);
const existingSubmission = ref(null);
const hasScore = ref(false);
const showScoreDialog = ref(false);
const submissionScore = ref(null);

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

// Function to get activity status
const getActivityStatus = (activity) => {
  // If already submitted, return 'submitted'
  if (activity.hasSubmitted) {
    return 'submitted';
  }
  
  // Check if past due date and time
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
    
    // If past due date/time and not submitted, return 'missing'
    if (now > dueDateTime) {
      return 'missing';
    }
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
          id: submission.id,
          caption: submission.caption,
          file_type: submission.file_type,
          has_file_path: !!submission.file_path,
          file_path_length: submission.file_path?.length,
          file_path_starts_with: submission.file_path?.substring(0, 50),
          file_path_value: submission.file_path,
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
              
              console.log('✅ Restored activity view:', activity.title);
              console.log('✅ Submissions loaded:', studentSubmissions.value.length);
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
    alert('Please fill in all required fields (Title and Student Name)');
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
    
    alert('Portfolio envelope created successfully!');
  } catch (error) {
    console.error('❌ Error creating portfolio envelope:', error);
    alert('Failed to create portfolio envelope: ' + (error.response?.data?.error || error.message));
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
    }
  } catch (error) {
    console.error('❌ Error fetching portfolio activities:', error);
  }
};

// Navigate activities
const nextActivity = () => {
  if (currentActivityIndex.value < portfolioActivities.value.length - 1) {
    currentActivityIndex.value++;
  }
};

const previousActivity = () => {
  if (currentActivityIndex.value > 0) {
    currentActivityIndex.value--;
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
  // Open the activity for submission
  openActivity(activity);
};

// Check if student has existing envelope
const checkExistingEnvelope = async () => {
  try {
    const classNameValue = props.className;
    const response = await axios.get(`/api/portfolio-envelope/student/${encodeURIComponent(classNameValue)}/`);
    
    if (response.data && response.data.envelope) {
      // Load existing envelope data
      envelopeDesign.value = {
        title: response.data.envelope.title,
        studentName: response.data.envelope.student_name,
        className: response.data.envelope.class_name,
        color: response.data.envelope.color,
        pattern: response.data.envelope.pattern
      };
      portfolioEnvelopeCreated.value = true;
      console.log('✅ Existing envelope found and loaded');
    } else {
      portfolioEnvelopeCreated.value = false;
    }
  } catch (error) {
    console.log('ℹ️ No existing envelope found:', error.response?.status);
    portfolioEnvelopeCreated.value = false;
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
    alert('Please select a file and activity');
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
