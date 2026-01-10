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
              <div class="w-14 h-14 bg-white rounded-full flex items-center justify-center shadow-lg ring-2 ring-white/30 overflow-hidden">
                <img 
                  v-if="studentInfo.profilePicture && !profileImageFailed" 
                  :src="studentInfo.profilePicture" 
                  :alt="studentInfo.name" 
                  class="w-full h-full object-cover"
                  @error="handleProfileImageError"
                />
                <span v-else class="text-indigo-600 text-2xl font-bold">{{ studentInfo.initial }}</span>
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
          </div>

          <!-- Teacher's Remarks Section - White Background -->
          <div class="mt-4 bg-white p-4 rounded-lg shadow-sm">
            <div class="flex justify-between items-center mb-2">
              <div class="flex items-center gap-2">
                <div class="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
                  <i class="pi pi-comments text-indigo-600 text-sm"></i>
                </div>
                <div>
                  <h3 class="text-base font-bold text-gray-800">Recent Remarks</h3>
                  <span class="text-xs text-gray-500">{{ remarksDate }} • {{ remarksTime }}</span>
                </div>
              </div>
              <button
                @click="openRemarksDialog"
                class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-all duration-200 shadow-sm hover:shadow-md">

                <span>View All</span>
              </button>
            </div>
            <p v-if="latestRemark" class="text-gray-700 leading-relaxed">
              {{ latestRemark.text }}
            </p>
            <p v-else class="text-gray-400 italic text-sm">
              No remarks yet for this student.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Table Section -->
    <div class="bg-white/80 backdrop-blur-sm p-6 rounded-xl shadow-sm border border-indigo-100">
      <div class="flex flex-col space-y-6">
        <!-- Search Bar and Statistics Row - Aligned Horizontally -->
        <div class="flex items-center gap-2">
            <!-- Back Button - Left side of Search -->
            <button @click="goBack"
              class="flex items-center gap-2 px-3 py-2 bg-indigo-600 text-white hover:bg-indigo-700 rounded-lg transition-all shadow-sm hover:shadow-md text-sm font-medium flex-shrink-0">
              <i class="pi pi-arrow-left text-sm"></i>
              <span>Back to Student Progress</span>
            </button>

            <!-- Search Bar - Moderate width -->
            <div class="relative" style="min-width: 400px; max-width: 280px;">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by subject or activity..."
                class="w-full pl-9 pr-8 py-2 rounded-lg border border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-200 transition-all text-gray-700 placeholder-gray-400 text-sm"
              />
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="pi pi-search text-indigo-500 text-xs"></i>
              </div>
              <button
                v-if="searchQuery"
                @click="searchQuery = ''"
                class="absolute inset-y-0 right-0 pr-2 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
              >
                <i class="pi pi-times text-xs"></i>
              </button>
            </div>

            <!-- Spacer to push stats to the right -->
            <div class="flex-1"></div>

            <!-- Total Activities - Compact -->
            <div
                @click="setFilter('all')"
                class="bg-gradient-to-r from-indigo-50 to-white px-3 py-2 rounded-lg border cursor-pointer transition-all duration-200 hover:shadow-sm flex-shrink-0"
                :class="activeFilter === 'all' ? 'border-indigo-500 border-2 ring-1 ring-indigo-200' : 'border-indigo-100'"
                style="min-width: 150px;">
                <div class="flex items-center gap-2">
                    <div class="w-7 h-7 bg-indigo-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <i class="pi pi-book text-xs text-indigo-600"></i>
                    </div>
                    <div class="min-w-0">
                        <p class="text-xs text-indigo-600 font-semibold leading-tight">Total Activities</p>
                        <p class="text-base font-bold text-indigo-900 leading-tight">{{ records.length }}</p>
                    </div>
                </div>
            </div>

            <!-- Completed - Compact -->
            <div
                @click="setFilter('completed')"
                class="bg-gradient-to-r from-green-50 to-white px-3 py-2 rounded-lg border cursor-pointer transition-all duration-200 hover:shadow-sm flex-shrink-0"
                :class="activeFilter === 'completed' ? 'border-green-500 border-2 ring-1 ring-green-200' : 'border-green-100'"
                style="min-width: 150px;">
                <div class="flex items-center gap-2">
                    <div class="w-7 h-7 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <i class="pi pi-check text-xs text-green-600"></i>
                    </div>
                    <div class="min-w-0">
                        <p class="text-xs text-green-600 font-semibold leading-tight">Completed</p>
                        <p class="text-base font-bold text-green-700 leading-tight">{{ completedCount }}</p>
                    </div>
                </div>
            </div>

            <!-- Incomplete - Compact -->
            <div
                @click="setFilter('incomplete')"
                class="bg-gradient-to-r from-red-50 to-white px-3 py-2 rounded-lg border cursor-pointer transition-all duration-200 hover:shadow-sm flex-shrink-0"
                :class="activeFilter === 'incomplete' ? 'border-red-500 border-2 ring-1 ring-red-200' : 'border-red-100'"
                style="min-width: 150px;">
                <div class="flex items-center gap-2">
                    <div class="w-7 h-7 bg-red-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <i class="pi pi-times-circle text-xs text-red-600"></i>
                    </div>
                    <div class="min-w-0">
                        <p class="text-xs text-red-600 font-semibold leading-tight">Incomplete</p>
                        <p class="text-base font-bold text-red-700 leading-tight">{{ incompleteCount }}</p>
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
          :value="paginatedRecords"
          :scrollable="true"
          scrollHeight="400px"
          class="p-datatable-rounded"
          stripedRows
          showGridlines>
          <Column field="subject" header="Subject" class="font-semibold">
            <template #body="slotProps">
              <div class="flex items-center gap-2">
                <i class="pi pi-book text-indigo-600"></i>
                <span class="font-medium text-indigo-900">{{ slotProps.data.subject }}</span>
              </div>
            </template>
          </Column>
          <Column field="output" header="Activity" style="min-width: 200px">
            <template #body="slotProps">
              <button @click="openActivityDetails(slotProps.data)" class="text-left hover:bg-indigo-50 p-1 rounded transition-colors w-full">
                <div class="font-medium text-indigo-700 hover:text-indigo-900">{{ slotProps.data.output }}</div>
                <div class="text-xs text-gray-500">{{ slotProps.data.activityType }}</div>
              </button>
            </template>
          </Column>
          <Column field="dueDate" header="Due Date & Time">
            <template #body="slotProps">
              <div class="text-sm text-gray-700">
                <div>{{ slotProps.data.dueDate }}</div>
                <div v-if="slotProps.data.dueTime" class="text-xs text-gray-500">{{ slotProps.data.dueTime }}</div>
              </div>
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
        <div v-if="!isLoading && hasMoreRecords" class="p-3 text-center border-t border-gray-100 bg-gradient-to-r from-indigo-50 to-violet-50 rounded-b-lg">
          <button
            @click="loadMore"
            class="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors duration-200 flex items-center gap-2 mx-auto text-sm"
          >
            <i class="pi pi-chevron-down text-xs"></i>
            <span>Load More ({{ remainingRecords }} more)</span>
          </button>
        </div>

        <!-- End of Records Message -->
        <div v-if="!isLoading && !hasMoreRecords && filteredRecords.length > 0" class="flex justify-center mt-4">
          <div class="text-sm text-gray-500 flex items-center gap-2">
            <i class="pi pi-check-circle text-indigo-600"></i>
            <span>All activities loaded</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- View Output Dialog -->
  <Dialog v-model:visible="showOutputDialog" modal header="View Student Output" :style="{width: '650px', maxWidth: '90vw'}" class="p-fluid">
    <div v-if="selectedOutput" class="space-y-4">
      <!-- Activity Info Grid -->
      <div class="grid grid-cols-2 gap-x-6 gap-y-3 p-4 bg-gray-50 rounded-lg border border-gray-200">
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium">Subject</p>
          <p class="text-gray-900 font-medium">{{ selectedOutput.subject }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium">Activity Type</p>
          <p class="text-gray-900 font-medium capitalize">{{ selectedOutput.activityType }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium">Activity Title</p>
          <p class="text-gray-900 font-medium">{{ selectedOutput.output }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium">Date & Time Submitted</p>
          <p class="text-gray-900 font-medium">{{ selectedOutput.submittedDate }} <span class="text-gray-500">{{ selectedOutput.time }}</span></p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium">Status</p>
          <span
            class="px-2 py-1 text-xs rounded font-medium inline-block mt-1"
            :class="{
              'bg-green-100 text-green-800': selectedOutput.status === 'Scored',
              'bg-blue-100 text-blue-800': selectedOutput.status === 'Submitted',
              'bg-amber-100 text-amber-700': selectedOutput.status === 'Pending',
              'bg-red-100 text-red-800': selectedOutput.status === 'Missing'
            }">
            {{ selectedOutput.status }}
          </span>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium">Score</p>
          <p class="font-bold" :class="selectedOutput.score === 'N/A' ? 'text-gray-400' : 'text-green-600'">
            {{ selectedOutput.score }}
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
                :alt="selectedOutput.output"
                class="max-w-full max-h-72 rounded shadow-lg object-contain"
                @error="handleImageError"
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
            <template v-else>
              <div class="text-center text-gray-400">
                <i class="pi pi-image text-5xl mb-2"></i>
                <p>No file available</p>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Caption (if any) -->
      <div v-if="selectedOutput.caption" class="p-3 bg-gray-50 rounded-lg border border-gray-200">
        <p class="text-xs text-gray-500 uppercase font-medium mb-1">Caption</p>
        <p class="text-gray-700">{{ selectedOutput.caption }}</p>
      </div>
    </div>

    <template #footer>
      <button @click="showOutputDialog = false" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors">
        Close
      </button>
    </template>
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

  <!-- Activity Details Dialog -->
  <Dialog v-model:visible="showActivityDetailsDialog" modal header="Activity Details" :style="{width: '550px', maxWidth: '90vw'}" class="p-fluid">
    <div v-if="selectedActivityDetail" class="space-y-4">
      <!-- Title and Subject -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium mb-1">Title</p>
          <p class="font-semibold text-gray-900">{{ selectedActivityDetail.output }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium mb-1">Subject</p>
          <p class="font-medium text-gray-700">{{ selectedActivityDetail.subject }}</p>
        </div>
      </div>

      <!-- Type and Due Date -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium mb-1">Type</p>
          <p class="font-medium text-gray-700 capitalize">{{ selectedActivityDetail.activityType }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 uppercase font-medium mb-1">Due Date</p>
          <p class="font-medium text-gray-700">
            {{ selectedActivityDetail.dueDate }}
            <span v-if="selectedActivityDetail.dueTime" class="text-gray-500"> {{ selectedActivityDetail.dueTime }}</span>
          </p>
        </div>
      </div>

      <!-- Status -->
      <div>
        <p class="text-xs text-gray-500 uppercase font-medium mb-1">Status</p>
        <span
          class="px-3 py-1.5 text-sm rounded-lg font-medium inline-block"
          :class="{
            'bg-green-100 text-green-800 border border-green-200': selectedActivityDetail.status === 'Scored',
            'bg-blue-100 text-blue-800 border border-blue-200': selectedActivityDetail.status === 'Submitted',
            'bg-amber-100 text-amber-700 border border-amber-300': selectedActivityDetail.status === 'Pending',
            'bg-red-100 text-red-800 border border-red-200': selectedActivityDetail.status === 'Missing'
          }">
          {{ selectedActivityDetail.status }}
        </span>
      </div>

      <!-- Instructions (if available) -->
      <div v-if="selectedActivityDetail.instructions">
        <div class="flex items-center justify-between mb-1">
          <p class="text-xs text-gray-500 uppercase font-medium">Instructions</p>
          <button @click="expandInstructions = !expandInstructions" class="text-xs text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
            <i :class="expandInstructions ? 'pi pi-compress' : 'pi pi-expand'" class="text-xs"></i>
            {{ expandInstructions ? 'Collapse' : 'Expand' }}
          </button>
        </div>
        <div class="bg-gray-50 p-3 rounded-lg border border-gray-200 text-sm text-gray-700 whitespace-pre-wrap" :class="expandInstructions ? '' : 'max-h-24 overflow-y-auto'">
          {{ selectedActivityDetail.instructions }}
        </div>
      </div>

      <!-- Scoring Criteria (if available) -->
      <div v-if="selectedActivityDetail.scoringCriteria && selectedActivityDetail.scoringCriteria.length > 0">
        <p class="text-xs text-gray-500 uppercase font-medium mb-2">Scoring Criteria</p>
        <div class="space-y-1">
          <div v-for="(criterion, index) in selectedActivityDetail.scoringCriteria" :key="index" class="flex justify-between text-sm bg-gray-50 px-3 py-2 rounded">
            <span class="text-gray-700">{{ criterion.name }}</span>
            <span class="font-medium text-indigo-600">{{ criterion.maxScore }} pts</span>
          </div>
        </div>
      </div>

      <!-- Score (if scored) -->
      <div v-if="selectedActivityDetail.score && selectedActivityDetail.score !== 'N/A'">
        <p class="text-xs text-gray-500 uppercase font-medium mb-1">Score</p>
        <p class="text-lg font-bold text-green-700">{{ selectedActivityDetail.score }}</p>
      </div>
    </div>

    <template #footer>
      <button @click="showActivityDetailsDialog = false" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors">
        Close
      </button>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
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
    console.log('   Full studentData:', JSON.stringify(studentData.value));

    // Get student's classroom info
    const studentGradeLevel = studentData.value?.gradeLevel || studentData.value?.grade_level || '';
    const studentSection = studentData.value?.section || '';
    const studentClassroom = studentData.value?.classroom || '';
    // Build expected classroom name format: "Grade 1 - A"
    const expectedClassroom = studentGradeLevel && studentSection 
        ? `${studentGradeLevel} - ${studentSection}` 
        : studentClassroom;
    
    console.log('   Student gradeLevel:', studentGradeLevel);
    console.log('   Student section:', studentSection);
    console.log('   Student classroom:', studentClassroom);
    console.log('   Expected classroom match:', expectedClassroom);

    try {
        // Load portfolio folders - only from current school year
        const foldersResponse = await axios.get('/api/portfolio/folders/?current_school_year=true');
        portfolioFolders.value = foldersResponse.data || [];
        console.log('📁 Loaded portfolio folders (current school year only):', portfolioFolders.value.length);

        const allRecords = [];

        // Load submissions for each folder
        for (const folder of portfolioFolders.value) {
            // Check if folder belongs to student's classroom
            const folderClassroom = folder.classroom_name || folder.class_name || '';
            console.log(`\n📂 Processing folder: ${folder.name} (ID: ${folder.id}, Classroom: ${folderClassroom})`);
            
            // Skip folders not in student's classroom
            if (expectedClassroom && folderClassroom && 
                folderClassroom !== 'General' && 
                folderClassroom !== expectedClassroom) {
                console.log(`   ⏭️ Skipping folder "${folder.name}" - classroom mismatch (${folderClassroom} vs ${expectedClassroom})`);
                continue;
            }

            try {
                const activitiesResponse = await axios.get(`/api/portfolio/folders/${folder.id}/activities/`);
                const activities = activitiesResponse.data || [];

                for (const activity of activities) {
                    // Skip unpublished/retracted activities - only show published ones
                    if (!activity.is_published) {
                        console.log(`   ⏭️ Skipping activity "${activity.title}" - not published`);
                        continue;
                    }

                    // Filter activities by student's classroom
                    const activityClassroom = activity.classroom_name || '';
                    
                    // Skip activities not assigned to this student's classroom
                    // Only filter if both have valid classroom info and they don't match
                    if (expectedClassroom && activityClassroom && 
                        activityClassroom !== 'General' && 
                        activityClassroom !== expectedClassroom) {
                        console.log(`   ⏭️ Skipping activity "${activity.title}" - classroom mismatch (${activityClassroom} vs ${expectedClassroom})`);
                        continue;
                    }

                    console.log(`   📝 Activity: ${activity.title} (ID: ${activity.id}, Classroom: ${activityClassroom}, Published: ${activity.is_published})`);

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

                                // Determine proper status based on submission data
                                // Status is "Scored" only if there's an actual score value
                                let displayStatus = 'Submitted';
                                const hasScore = (totalScore !== null && totalScore !== undefined) || 
                                                 (submission.score !== null && submission.score !== undefined);
                                
                                if (submission.status === 'scored' && hasScore) {
                                    displayStatus = 'Scored';
                                } else if (submission.status === 'unscored' || submission.status === 'scored') {
                                    // Unscored or scored without actual score value
                                    displayStatus = 'Submitted';
                                }

                                allRecords.push({
                                    activityId: activity.id,
                                    submissionId: submission.id,
                                    subject: folder.name,
                                    output: activity.title,
                                    activityType: activity.activity_type,
                                    dueDate: activity.due_date ? new Date(activity.due_date).toLocaleDateString() : 'N/A',
                                    dueTime: activity.due_time ? formatDueTime(activity.due_time) : null,
                                    dueDateRaw: activity.due_date,
                                    submittedDate: new Date(submission.submitted_at).toLocaleDateString(),
                                    time: new Date(submission.submitted_at).toLocaleTimeString(),
                                    status: displayStatus,
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
                                activityId: activity.id,
                                subject: folder.name,
                                output: activity.title,
                                activityType: activity.activity_type,
                                dueDate: activity.due_date ? new Date(activity.due_date).toLocaleDateString() : 'N/A',
                                dueTime: activity.due_time ? formatDueTime(activity.due_time) : null,
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

// Helper function to format due time (HH:MM:SS to 12-hour format)
const formatDueTime = (timeString) => {
    if (!timeString) return null;
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
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
                record.status === 'Scored' || 
                record.status === 'Submitted' || 
                record.status === 'Submitted Late' || 
                record.status === 'Resubmitted'
            );
        } else if (activeFilter.value === 'incomplete') {
            filtered = filtered.filter(record => 
                record.status === 'Pending' || 
                record.status === 'Missing'
            );
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

const remainingRecords = computed(() => {
    return filteredRecords.value.length - displayLimit.value;
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

// Activity details dialog
const showActivityDetailsDialog = ref(false);
const selectedActivityDetail = ref(null);
const expandInstructions = ref(false);

const openActivityDetails = async (activity) => {
    // Set basic info from the record
    selectedActivityDetail.value = {
        ...activity,
        instructions: null,
        scoringCriteria: null
    };
    showActivityDetailsDialog.value = true;
    expandInstructions.value = false;

    // Try to fetch additional details from API
    try {
        if (activity.activityId) {
            const response = await axios.get(`/api/activities/${activity.activityId}/`);
            if (response.data) {
                selectedActivityDetail.value.instructions = response.data.description || null;
                
                // Parse scoring criteria
                if (response.data.scoring_criteria) {
                    try {
                        selectedActivityDetail.value.scoringCriteria = typeof response.data.scoring_criteria === 'string'
                            ? JSON.parse(response.data.scoring_criteria)
                            : response.data.scoring_criteria;
                    } catch (e) {
                        console.error('Error parsing scoring criteria:', e);
                    }
                }
            }
        }
    } catch (error) {
        console.error('Error fetching activity details:', error);
    }
};

const viewOutput = async (output) => {
    selectedOutput.value = output;
    outputFiles.value = [];
    currentOutputFileIndex.value = 0;
    showOutputDialog.value = true;

    // Try to fetch submission files from API
    try {
        if (output.submissionId) {
            const response = await axios.get(`/api/submissions/${output.submissionId}/`);
            if (response.data) {
                // Check if there are multiple files
                if (response.data.files && response.data.files.length > 0) {
                    // Map files to use file_url if available
                    outputFiles.value = response.data.files.map(f => ({
                        file_path: f.file_url || f.file_path,
                        file_type: f.file_type,
                        file_name: f.file_name || 'Submission'
                    }));
                } else if (response.data.file_url || response.data.file_path) {
                    // Single file - prefer file_url
                    outputFiles.value = [{
                        file_path: response.data.file_url || response.data.file_path,
                        file_type: response.data.file_type,
                        file_name: response.data.caption || 'Submission'
                    }];
                }
            }
        } else if (output.filePath) {
            // Fallback to single file from record
            outputFiles.value = [{
                file_path: output.filePath,
                file_type: output.fileType,
                file_name: output.caption || 'Submission'
            }];
        }
    } catch (error) {
        console.error('Error fetching submission files:', error);
        // Fallback to single file from record
        if (output.filePath) {
            outputFiles.value = [{
                file_path: output.filePath,
                file_type: output.fileType,
                file_name: output.caption || 'Submission'
            }];
        }
    }
};

// Multiple files navigation for output dialog
const outputFiles = ref([]);
const currentOutputFileIndex = ref(0);

const currentOutputFile = computed(() => {
    if (outputFiles.value.length > 0) {
        return outputFiles.value[currentOutputFileIndex.value];
    }
    // Fallback to selectedOutput
    if (selectedOutput.value?.filePath) {
        return {
            file_path: selectedOutput.value.filePath,
            file_type: selectedOutput.value.fileType,
            file_name: selectedOutput.value.caption || 'Submission'
        };
    }
    return null;
});

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

// Helper function to check if file is an image
const isImageFile = (file) => {
    if (!file) return false;
    // Check file_type first
    if (file.file_type === 'image') return true;
    // Check if file_path is a data URI for image
    if (file.file_path && file.file_path.startsWith('data:image')) return true;
    // Check if file_path is a URL ending with image extension
    if (file.file_path) {
        const path = file.file_path.toLowerCase();
        if (path.match(/\.(jpg|jpeg|png|gif|webp|bmp)(\?.*)?$/)) return true;
    }
    // Check file_name extension
    if (file.file_name) {
        const ext = file.file_name.toLowerCase().split('.').pop();
        return ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'].includes(ext);
    }
    return false;
};

// Helper function to get proper file URL
const getFileUrl = (filePath) => {
    if (!filePath) return '';
    // Already a proper URL or data URI
    if (filePath.startsWith('data:') || filePath.startsWith('http') || filePath.startsWith('/media')) {
        return filePath;
    }
    // Assume it's base64 encoded image data
    return `data:image/png;base64,${filePath}`;
};

// Handle image load error
const handleImageError = (event) => {
    console.error('Image failed to load:', event.target.src?.substring(0, 100));
};

// Handle profile image load error - hide the image and show initials
const profileImageFailed = ref(false);
const handleProfileImageError = (event) => {
    console.error('Profile image failed to load:', event.target.src?.substring(0, 100));
    profileImageFailed.value = true;
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

// Helper to get proper profile picture URL
const getProfilePictureUrl = (profilePic) => {
    if (!profilePic) return null;
    // If it's already a full URL or data URI, return as is
    if (profilePic.startsWith('http') || profilePic.startsWith('data:') || profilePic.startsWith('/media')) {
        return profilePic;
    }
    // If it's a relative path, prepend the base URL
    return profilePic;
};

const studentInfo = computed(() => {
    const name = studentData.value?.name || props.selectedStudent?.name || 'Unknown Student';
    // Get initials from first and last name (e.g., "Catalina San" -> "CS")
    const nameParts = name.trim().split(' ').filter(p => p.length > 0);
    const initials = nameParts.length >= 2 
        ? (nameParts[0].charAt(0) + nameParts[nameParts.length - 1].charAt(0)).toUpperCase()
        : name.charAt(0).toUpperCase();
    
    const rawProfilePic = studentData.value?.profile_picture || studentData.value?.profilePicture || props.selectedStudent?.profile_picture || null;
    
    return {
        name: name,
        id: studentData.value?.id || props.selectedStudent?.id || 'N/A',
        initial: initials,
        profilePicture: getProfilePictureUrl(rawProfilePic)
    };
});

// Function to handle class change event
const handleClassChange = (event) => {
    console.log('🔄 Class changed in Progress, clearing view state and navigating...', event.detail);

    // Clear the teacher view state so Room shows folders view
    localStorage.removeItem('teacher_current_view');

    // Navigate directly to TeacherRoom to show folders view
    emit('navigate', 'TeacherRoom');
};

onMounted(() => {
    console.log('Progress.vue mounted');
    
    // Reset profile image failed state
    profileImageFailed.value = false;

    // Get student data from localStorage (set by Sprogress.vue)
    const stored = localStorage.getItem('selected_student_progress');
    if (stored) {
        try {
            const data = JSON.parse(stored);
            studentData.value = data.student;
            console.log('Loaded student from localStorage:', studentData.value);
            console.log('Student display ID:', studentData.value?.id);
            console.log('Student database ID:', studentData.value?.dbId);
            console.log('Student profile_picture:', studentData.value?.profile_picture);

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

    // Listen for class change events
    window.addEventListener('classChanged', handleClassChange);
});

onUnmounted(() => {
    // Clean up event listener
    window.removeEventListener('classChanged', handleClassChange);
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
    return records.value.filter(record => 
        record.status === "Scored" || 
        record.status === "Submitted" || 
        record.status === "Submitted Late" || 
        record.status === "Resubmitted"
    ).length;
});

const incompleteCount = computed(() => {
    return records.value.filter(record => 
        record.status === "Pending" || 
        record.status === "Missing"
    ).length;
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
    layout: TeacherLayout,
    inheritAttrs: false
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
