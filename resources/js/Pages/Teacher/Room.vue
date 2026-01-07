<template>
    <div class="flex flex-col">
        <!-- Hidden file input for instruction attachments -->
        <input
            type="file"
            ref="instructionFileInput"
            @change="handleInstructionFileUpload"
            accept="image/*,.pdf,.doc,.docx"
            multiple
            class="hidden"
        />
        
        <!-- Class Header -->
        <div class="bg-white p-4 md:p-3 shadow-lg rounded-t-xl border-b border-gray-200">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                <div class="space-y-2">
                    <h1 class="text-xl md:text-2xl font-bold text-gray-900 px-4 py-2 md:px-5 md:py-2 rounded-lg inline-block bg-gray-100">
                        {{ actualClassName }}
                    </h1>
                    <p class="text-gray-600 ml-2 flex items-center gap-2 text-sm">
                        <i class="pi pi-user"></i>
                        Teacher: {{ currentUser.name }}
                    </p>
                </div>
            </div>

            <!-- Navigation Tabs -->
            <div class="flex flex-wrap gap-2 md:gap-4 mt-3 md:mt-4">
                <button
                    v-for="tab in tabs"
                    :key="tab.id"
                    @click="activeTab = tab.id"
                    class="flex items-center gap-2 text-gray-600 px-4 py-2 md:px-5 md:py-2.5 rounded-lg transition-all duration-300 relative overflow-hidden group"
                    :class="[
                        activeTab === tab.id
                            ? 'font-semibold text-indigo-700 bg-indigo-50'
                            : 'hover:text-indigo-600 hover:bg-gray-50'
                    ]"
                >
                    <span class="relative z-10 flex items-center gap-2">
                        <i :class="['pi', tab.icon]"></i>
                        <span>{{ tab.name }}</span>
                    </span>
                    <span
                        v-if="activeTab === tab.id"
                        class="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-600 rounded-full"
                    ></span>
                </button>
            </div>
        </div>

        <!-- Main Content Area -->
        <div class="w-full bg-white/80 flex-1">
            <!-- Content Area -->
            <div class="w-full px-4 sm:px-6 pt-1 pb-8 transition-all duration-300"
                 :style="{ 'padding-left': '1.5rem', 'padding-right': '1.5rem' }">
                <template v-if="activeTab === 'pupil'">
                    <div class="p-4 md:p-6 bg-transparent">
                        <!-- Show folders view when not in activities mode -->
                        <div v-if="!showingActivities" class="space-y-6">
                            <!-- Header with title and New Folder button -->
                            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                                <h2 class="text-xl md:text-2xl font-bold text-gray-900">Pupil's Activities</h2>
                                <button
                                    @click="showNewFolderDialog = true"
                                    class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                                >
                                    <i class="pi pi-plus"></i>
                                    <span>Create Class Activity</span>
                                </button>
                            </div>

                            <!-- Loading State -->
                            <div v-if="isLoadingFolders" class="flex justify-center items-center py-12">
                                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                                <span class="ml-3 text-gray-600">Loading folders...</span>
                            </div>

                            <!-- Empty State -->
                            <div v-else-if="subjectFolders.length === 0" class="text-center py-12">
                                <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-gray-100 mb-4">
                                    <i class="pi pi-folder text-gray-400 text-xl"></i>
                                </div>
                                <h3 class="text-lg font-medium text-gray-900 mb-2">No Activity Folders</h3>
                                <p class="text-gray-500">Click "Create Class Activity" to create your first folder.</p>
                            </div>

                            <!-- Folders Grid -->
                            <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
                                <!-- Subject Folders -->
                                <div v-for="folder in subjectFolders" :key="folder.id" class="group cursor-pointer">
                                    <div @click="showSubjectActivities(folder.name, folder.id)" class="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-lg transition-all duration-300 relative h-full flex flex-col group-hover:border-indigo-300">
                                        <!-- Header with Gradient Background -->
                                        <div class="relative h-32 bg-gradient-to-r from-indigo-600 to-blue-600 rounded-t-xl">
                                            <!-- Decorative Background Pattern -->
                                            <div class="absolute inset-0 opacity-10">
                                                <div class="absolute top-0 right-0 w-40 h-40 bg-white rounded-full transform translate-x-1/3 -translate-y-1/3"></div>
                                            </div>

                                            <!-- Content -->
                                            <div class="relative z-10 p-4 h-full flex flex-col justify-between text-white">
                                                <div>
                                                    <h3 class="text-lg font-bold truncate">{{ folder.name }}</h3>
                                                    <p class="text-sm text-white/80 truncate">Subject Folder</p>
                                                </div>
                                                <div class="text-xs text-white/70">{{ folder.items }} activities</div>
                                            </div>

                                            <!-- Teacher Avatar/Profile Picture -->
                                            <div class="absolute bottom-2 right-4 w-16 h-16 rounded-full bg-white shadow-lg border-4 border-white flex items-center justify-center overflow-hidden">
                                                <div v-if="currentUser?.profile_picture" class="w-full h-full">
                                                    <img :src="currentUser.profile_picture" :alt="currentUser?.name" class="w-full h-full object-cover">
                                                </div>
                                                <div v-else class="w-full h-full bg-gradient-to-br from-indigo-400 to-blue-500 flex items-center justify-center text-white font-bold text-lg">
                                                    {{ currentUser?.name?.charAt(0) || 'T' }}
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
                                                    :title="`Menu for ${folder.name}`"
                                                >
                                                    <i class="pi pi-ellipsis-v text-gray-500"></i>
                                                </button>

                                                <!-- Dropdown Menu -->
                                                <div v-if="activeFolderMenuIndex === folder.id" class="absolute right-0 bottom-full mb-2 w-48 bg-white rounded-md shadow-lg z-20 py-1">
                                                    <a @click.stop="openUpdateFolderModal(folder)" href="#" class="px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center">
                                                        <i class="pi pi-pencil mr-2"></i> Update
                                                    </a>
                                                    <div v-tooltip.left="folder.items > 0 ? 'Cannot drop a folder with activities' : 'Drop Folder'">
                                                        <a @click.stop="folder.items === 0 && dropfolder(folder)" href="#"
                                                           :class="['block w-full text-left px-4 py-2 text-sm', { 'text-red-500 hover:bg-red-50': folder.items === 0, 'text-gray-400 cursor-not-allowed': folder.items > 0 }]">
                                                            <i class="pi pi-trash mr-2"></i> Drop
                                                        </a>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Show activities list when a folder is selected -->
                        <div v-else>
                            <!-- List of Activities Header (Top) -->
                            <div class="mb-4">
                                <h2 class="text-2xl font-bold text-indigo-900">List of Activities - {{ selectedSubject }}</h2>
                            </div>

                            <!-- Back button and Action Buttons container -->
                            <div class="flex flex-col sm:flex-row justify-start sm:items-center gap-4 mb-4">
                                <!-- Back Button (Left Side) -->
                                <div class="flex flex-wrap gap-2 order-first">
                                    <!-- Back button -->
                                    <button
                                        @click="backToFolders"
                                        class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                                    >
                                        <i class="pi pi-arrow-left"></i>
                                        <span>Back to Folders</span>
                                    </button>
                                </div>

                                <!-- Action Buttons (Right Side) -->
                                <div class="flex flex-wrap gap-2 ml-auto">
                                    <!-- Add Activity button -->
                                    <button
                                        @click="showAddActivityDialog = true"
                                        class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                                    >
                                        <i class="pi pi-plus"></i>
                                        <span>Add Activity</span>
                                    </button>

                                    <!-- Track Progress button -->
                                    <button
                                        @click="navigateToProgress"
                                        class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                                    >
                                        <i class="pi pi-chart-line"></i>
                                        <span>Track Progress</span>
                                    </button>
                                </div>
                            </div>

                            <!-- Activities Table -->
                            <div class="bg-transparent rounded-xl shadow-sm overflow-visible border-0">
                                <!-- Loading State -->
                                <div v-if="isLoadingActivities" class="flex justify-center items-center py-12">
                                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                                </div>

                                <!-- Empty State -->
                                <div v-else-if="activities.length === 0" class="text-center py-12">
                                    <i class="pi pi-inbox text-4xl text-gray-400 mb-4"></i>
                                    <p class="text-gray-500">No activities yet. Click "Add Activity" to create one.</p>
                                </div>

                                <!-- Activities List -->
                                <template v-else>
                                    <div class="space-y-8">
                                        <!-- Draft Activities Table -->
                                        <div v-if="draftActivities.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                                            <!-- Section Header -->
                                            <div class="bg-white border-b border-gray-200 px-6 py-4">
                                                <div class="flex items-center justify-between">
                                                    <div class="flex items-center gap-3">
                                                        <div class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600">
                                                            <i class="pi pi-file-edit text-lg"></i>
                                                        </div>
                                                        <div>
                                                            <h3 class="text-lg font-bold text-gray-800">Draft Activities</h3>
                                                        </div>
                                                    </div>
                                                    <span class="px-3 py-1 bg-amber-100 text-amber-800 text-xs font-medium rounded-full border border-amber-200 shadow-sm">
                                                        {{ draftActivities.length }} Draft{{ draftActivities.length !== 1 ? 's' : '' }}
                                                    </span>
                                                </div>
                                            </div>

                                            <!-- Table Header -->
<div class="bg-gray-50 border-b border-gray-200">
  <div class="grid grid-cols-12 gap-4 px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider items-center">

    <div class="col-span-2 text-center">
      Activity ID#
    </div>

    <div class="col-span-2 text-center">
      Title
    </div>

    <div class="col-span-2 text-center">
      Type
    </div>

    <div class="col-span-2 text-center">
      Due Time
    </div>

    <div class="col-span-2 text-center">
      Due Date
    </div>

    <div class="col-span-2 text-center">
      Actions
    </div>

  </div>
</div>


                                            <!-- Table Body -->
                                            <div class="divide-y divide-gray-200">
                                                <div v-for="(activity, index) in draftActivities.slice(0, displayedDraftCount)" :key="activity.id"
                                                    class="group hover:bg-gray-50 transition-colors duration-150">

                                                    <div class="grid grid-cols-12 gap-4 px-6 py-4 items-center cursor-pointer"
                                                        @click="navigateToActivityOutputs(activity, index)">
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

                                                        <!-- Due Time -->
                                                        <div class="col-span-2 text-center">
                                                            <span v-if="activity.formattedTime" class="text-sm text-gray-700 font-medium">{{ activity.formattedTime }}</span>
                                                            <span v-else class="text-sm text-gray-400">--:--</span>
                                                        </div>

                                                        <!-- Due Date -->
                                                        <div class="col-span-2 text-center">
                                                            <div class="text-sm text-gray-700 font-medium">
                                                                {{ activity.date ? new Date(activity.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'No date' }}
                                                                <div v-if="activity.daysLeft" class="text-xs text-gray-500 mt-0.5">{{ activity.daysLeft }}</div>
                                                            </div>
                                                        </div>

                                                        <!-- Actions -->
                                                        <div class="col-span-2 flex items-center justify-center gap-2">
                                                            <!-- Publish Button -->
                                                            <button
                                                                @click.stop="submitActivity(activity, index)"
                                                                :disabled="activity.is_published"
                                                                :class="[
                                                                    'inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-all duration-150',
                                                                    activity.is_published
                                                                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                                                        : 'bg-green-600 text-white hover:bg-green-700 shadow-sm hover:shadow'
                                                                ]"
                                                                :title="activity.is_published ? 'Already published' : 'Publish to students'"
                                                            >
                                                                <i class="pi pi-send text-xs"></i>
                                                                <span>Publish</span>
                                                            </button>

                                                            <!-- Edit Button - Always enabled for teachers -->
                                                            <button
                                                                @click.stop="editActivity(activity, index)"
                                                                class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-all duration-150 bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm hover:shadow"
                                                                title="Edit activity"
                                                            >
                                                                <i class="pi pi-pencil text-xs"></i>
                                                                <span>Edit</span>
                                                            </button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <!-- Load More Button for Draft Activities -->
                                        <div v-if="displayedDraftCount < draftActivities.length" class="p-4 text-center border-t border-gray-200 bg-gray-50 rounded-b-xl">
                                            <button @click="displayedDraftCount += itemsPerPage" class="px-6 py-2.5 bg-amber-600 hover:bg-amber-700 text-white font-medium rounded-lg transition-colors duration-200 flex items-center gap-2 mx-auto">
                                                <i class="pi pi-chevron-down"></i>
                                                <span>Load More ({{ draftActivities.length - displayedDraftCount }} more)</span>
                                            </button>
                                        </div>

                                        <!-- Published Activities Table -->
                                        <div v-if="publishedActivities.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                                            <!-- Section Header -->
                                            <div class="bg-gray-50 border-b border-gray-200 px-6 py-4">
                                                <div class="flex items-center justify-between">
                                                    <div class="flex items-center gap-3">
                                                        <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center text-green-600">
                                                            <i class="pi pi-check-circle text-lg"></i>
                                                        </div>
                                                        <div>
                                                            <h3 class="text-lg font-bold text-gray-800">Published Activities</h3>
                                                        </div>
                                                    </div>
                                                    <span class="px-3 py-1 bg-emerald-100 text-emerald-800 text-xs font-medium rounded-full border border-emerald-200 shadow-sm">
                                                        {{ publishedActivities.length }} Published
                                                    </span>
                                                </div>
                                            </div>

                                            <!-- Table Header -->
<div class="bg-gray-50 border-b border-gray-200">
  <div class="grid grid-cols-12 gap-4 px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider items-center">

    <div class="col-span-2 text-center">
      Activity ID#
    </div>

    <div class="col-span-2 text-center">
      Title
    </div>

    <div class="col-span-2 text-center">
      Type
    </div>

    <div class="col-span-2 text-center">
      Due Time
    </div>

    <div class="col-span-2 text-center">
      Due Date
    </div>

    <div class="col-span-2 text-center">
      Actions
    </div>

  </div>
</div>


                                            <!-- Table Body -->
                                            <div class="divide-y divide-gray-200">
                                                <div v-for="(activity, index) in publishedActivities.slice(0, displayedPublishedCount)" :key="activity.id"
                                                    class="group hover:bg-gray-50 transition-colors duration-150">

                                                    <div class="grid grid-cols-12 gap-4 px-6 py-4 items-center cursor-pointer"
                                                        @click="navigateToActivityOutputs(activity, index)">
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
                                                            <span class="text-xs text-gray-700 capitalize font-medium">{{ activity.type }}</span>
                                                        </div>

                                                        <!-- Due Time -->
                                                        <div class="col-span-2 text-center">
                                                            <span v-if="activity.formattedTime" class="text-sm text-gray-700 font-medium">{{ activity.formattedTime }}</span>
                                                            <span v-else class="text-sm text-gray-400">--:--</span>
                                                        </div>

                                                        <!-- Due Date -->
                                                        <div class="col-span-2 text-center">
                                                            <div class="text-sm text-gray-700 font-medium">
                                                                {{ activity.date ? new Date(activity.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'No date' }}
                                                                <div v-if="activity.daysLeft" class="text-xs text-gray-500 mt-0.5">{{ activity.daysLeft }}</div>
                                                            </div>
                                                        </div>

                                                        <!-- Actions -->
                                                        <div class="col-span-2 flex items-center justify-center gap-2">
                                                            <!-- Retract Button -->
                                                            <button
                                                                @click.stop="retractActivity(activity, index)"
                                                                :disabled="!activity.is_published"
                                                                :class="[
                                                                    'inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-all duration-150',
                                                                    !activity.is_published
                                                                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                                                        : 'bg-orange-600 text-white hover:bg-orange-700 shadow-sm hover:shadow'
                                                                ]"
                                                                :title="!activity.is_published ? 'Not published' : 'Retract from students'"
                                                            >
                                                                <i class="pi pi-undo text-xs"></i>
                                                                <span>Retract</span>
                                                            </button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <!-- Load More Button for Published Activities -->
                                        <div v-if="displayedPublishedCount < publishedActivities.length" class="p-4 text-center border-t border-gray-200 bg-gray-50 rounded-b-xl">
                                            <button @click="displayedPublishedCount += itemsPerPage" class="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-medium rounded-lg transition-colors duration-200 flex items-center gap-2 mx-auto">
                                                <i class="pi pi-chevron-down"></i>
                                                <span>Load More ({{ publishedActivities.length - displayedPublishedCount }} more)</span>
                                            </button>
                                        </div>
                                    </div>
                                </template>
                            </div>
                        </div>
                    </div>
                </template>

                <template v-if="activeTab === 'portfolio'">
                    <div class="p-4 md:p-6 bg-transparent">
                        <!-- Portfolio Compilation Content -->
                        <div v-if="!portfolioCompilationActive" class="flex items-center justify-center min-h-[60vh]">
                            <div class="text-center">
                                <!-- Show Start button if not active -->
                                <button
                                    @click="showPortfolioCompilationDialog = true"
                                    class="px-8 py-4 bg-indigo-600 text-white text-lg font-semibold rounded-lg hover:bg-indigo-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
                                >
                                    <i class="pi pi-book mr-2"></i>
                                    Start Portfolio Compilation
                                </button>
                            </div>
                        </div>

                        <!-- Student Portfolio Compilation Table -->
                        <div v-else class="space-y-4">
                            <!-- Show selected envelope if viewing one -->
                            <div v-if="selectedEnvelope" class="rounded-2xl shadow-2xl overflow-hidden relative min-h-[600px] animate-scaleIn"
                                 :style="isEnvelopeOpen ? {
                                   background: `linear-gradient(135deg, ${selectedEnvelope.color} 0%, ${adjustBrightness(selectedEnvelope.color, -20)} 100%)`,
                                   animation: 'gradientShift 8s ease infinite'
                                 } : { background: 'white' }">

                                <!-- Animated Pattern Overlay (matching envelope) - Only when open -->
                                <div v-if="isEnvelopeOpen && selectedEnvelope.pattern === 'dots'"
                                     class="absolute inset-0 opacity-10 pointer-events-none animate-patternFloat"
                                     style="background-image: radial-gradient(circle, white 2px, transparent 2px); background-size: 20px 20px;">
                                </div>
                                <div v-else-if="isEnvelopeOpen && selectedEnvelope.pattern === 'lines'"
                                     class="absolute inset-0 opacity-10 pointer-events-none animate-patternSlide"
                                     style="background-image: repeating-linear-gradient(45deg, white 0, white 2px, transparent 2px, transparent 10px);">
                                </div>
                                <div v-else-if="isEnvelopeOpen && selectedEnvelope.pattern === 'grid'"
                                     class="absolute inset-0 opacity-10 pointer-events-none animate-patternPulse"
                                     style="background-image: linear-gradient(white 1px, transparent 1px), linear-gradient(90deg, white 1px, transparent 1px); background-size: 20px 20px;">
                                </div>

                                <!-- Floating Particles Effect - Reduced for performance -->
                                <div v-if="isEnvelopeOpen" class="absolute inset-0 pointer-events-none overflow-hidden">
                                    <div v-for="i in 5" :key="i"
                                         class="absolute w-2 h-2 bg-white/20 rounded-full animate-float"
                                         :style="{
                                           left: `${(i * 20)}%`,
                                           top: `${(i * 15) + 10}%`,
                                           animationDelay: `${i * 0.5}s`,
                                           animationDuration: `${8 + i}s`
                                         }">
                                    </div>
                                </div>

                                <div class="max-w-6xl mx-auto p-8 relative z-10">
                                    <!-- Show Closed Envelope (Front Cover) -->
                                    <div v-if="!isEnvelopeOpen" class="animate-fadeIn">
                                        <!-- Back Button - Aligned with envelope -->
                                        <button
                                            @click="selectedEnvelope = null; studentActivities = []; currentActivityIndex = 0"
                                            class="mb-4 px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-lg border-2 border-gray-300 hover:border-indigo-500 hover:text-indigo-600 hover:bg-indigo-50 transition-all duration-200 shadow-md hover:shadow-lg flex items-center gap-2"
                                        >
                                            <i class="pi pi-arrow-left text-sm"></i>
                                            Back to List
                                        </button>

                                        <!-- Envelope Front Cover - No white container, matching Student Design -->
                                        <div
                                            @click="openEnvelope"
                                            class="rounded-2xl overflow-hidden cursor-pointer transform transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl"
                                        >
                                            <!-- Envelope Preview -->
                                            <div class="relative w-full aspect-[21/9]"
                                                 :style="{ backgroundColor: selectedEnvelope.color }">

                                                <!-- Pattern Overlay -->
                                                <div v-if="selectedEnvelope.pattern === 'dots'"
                                                     class="absolute inset-0 opacity-20"
                                                     style="background-image: radial-gradient(circle, white 2px, transparent 2px); background-size: 20px 20px;">
                                                </div>
                                                <div v-else-if="selectedEnvelope.pattern === 'lines'"
                                                     class="absolute inset-0 opacity-20"
                                                     style="background-image: repeating-linear-gradient(45deg, white 0, white 2px, transparent 2px, transparent 10px);">
                                                </div>
                                                <div v-else-if="selectedEnvelope.pattern === 'grid'"
                                                     class="absolute inset-0 opacity-20"
                                                     style="background-image: linear-gradient(white 1px, transparent 1px), linear-gradient(90deg, white 1px, transparent 1px); background-size: 20px 20px;">
                                                </div>

                                                <!-- Envelope Flap -->
                                                <div
                                                    class="absolute top-0 left-0 right-0 h-1/4 border-b-4 border-white/30"
                                                    :style="{
                                                        background: `linear-gradient(180deg, ${selectedEnvelope.color} 0%, ${adjustBrightness(selectedEnvelope.color, -20)} 100%)`
                                                    }">
                                                    <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-0 h-0
                                                                border-l-[150px] border-r-[150px] border-t-[80px] border-l-transparent border-r-transparent"
                                                         :style="{ borderTopColor: adjustBrightness(selectedEnvelope.color, -20) }">
                                                    </div>
                                                </div>

                                                <!-- Content Area - Matching Student View with Grade/Section -->
                                                <div class="absolute inset-0 flex flex-col items-center justify-center p-4 text-center">
                                                    <div class="bg-white/20 backdrop-blur-md rounded-2xl p-6 shadow-xl border border-white/30 max-w-sm w-full">
                                                        <h1 class="text-2xl font-bold text-white mb-2"
                                                            style="text-shadow: 0 2px 8px rgba(0,0,0,0.3)">
                                                            {{ selectedEnvelope.name }}
                                                        </h1>
                                                        <p class="text-base text-white/90 font-medium mb-1"
                                                           style="text-shadow: 0 1px 4px rgba(0,0,0,0.2)">
                                                            {{ selectedEnvelope.className || selectedEnvelope.class_name || actualClassName }}
                                                        </p>

                                                        <!-- Click to Open Text -->
                                                        <div class="mt-4 text-white/60 text-xs animate-pulse">
                                                            <i class="pi pi-hand-pointer mr-1"></i>
                                                            Click to open
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Show Opened Envelope Content -->
                                    <div v-else>
                                        <!-- Tab Header with Back Button on Left -->
                                        <div class="flex justify-between items-center mb-6 animate-slideDown">
                                            <!-- Back Button on the left -->
                                            <button
                                                @click="selectedEnvelope = null; isEnvelopeOpen = false; studentActivities = []; currentActivityIndex = 0; activePortfolioTab = 'scored'"
                                                class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-lg border-2 border-gray-300 hover:border-indigo-500 hover:text-indigo-600 hover:bg-indigo-50 transition-all duration-200 shadow-md hover:shadow-lg flex items-center gap-2"
                                            >
                                                <i class="pi pi-arrow-left text-sm"></i>
                                                Back to List
                                            </button>

                                            <!-- Tabs on the right -->
                                            <div class="flex gap-2">
                                                <button
                                                    @click="activePortfolioTab = 'scored'"
                                                    :class="activePortfolioTab === 'scored'
                                                        ? 'bg-indigo-600 text-white shadow-lg'
                                                        : 'bg-white/30 text-white hover:bg-white/40'"
                                                    class="flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all duration-200"
                                                >
                                                    <i class="pi pi-check-circle"></i>
                                                    Student's Activitiy Compilation
                                                    <span class="px-2 py-0.5 rounded-full text-xs font-semibold"
                                                          :class="activePortfolioTab === 'scored' ? 'bg-white/20' : 'bg-white/30'">
                                                        {{ scoredActivities.length }}
                                                    </span>
                                                </button>
                                                                                            </div>
                                        </div>

                                        <!-- Display Student Activities (Carousel Style like Student View) -->
                                        <div class="relative min-h-[600px]">

                                    <!-- Loading state -->
                                    <div v-if="currentTabActivities.length === 0" class="text-center py-20 relative z-10">
                                        <div class="inline-block p-8 rounded-full mb-6 bg-white/30">
                                            <i class="pi pi-inbox text-6xl text-white"></i>
                                        </div>
                                        <p class="text-xl font-semibold text-white">
                                            No activities found
                                        </p>
                                        <p class="text-sm text-white/80 mt-2">
                                            This student hasn't submitted any activities yet
                                        </p>
                                    </div>

                                    <!-- Activity Carousel -->
                                    <div v-else class="relative">
                                        <!-- Activity Content -->
                                        <div v-if="currentTabActivities[currentActivityIndex]"
                                             :key="currentActivityIndex"
                                             @vue:mounted="currentPortfolioFileIndex = 0"
                                             class="animate-fadeIn">
                                          
                                          <!-- Top Navigation Bar -->
                                          <div class="flex items-center justify-between mb-4 bg-white/90 rounded-xl p-3 shadow-md">
                                            <button
                                              @click="previousActivity"
                                              :disabled="currentActivityIndex === 0"
                                              class="flex items-center gap-2 px-4 py-2 rounded-lg border-2 transition-all disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-50"
                                              :style="{ borderColor: selectedEnvelope.color, color: selectedEnvelope.color }"
                                            >
                                              <i class="pi pi-chevron-left"></i>
                                              <span class="font-medium">Previous</span>
                                            </button>
                                            
                                            <span class="px-4 py-2 rounded-lg font-bold text-white"
                                                  :style="{ backgroundColor: selectedEnvelope.color }">
                                              {{ currentActivityIndex + 1 }} / {{ currentTabActivities.length }}
                                            </span>
                                            
                                            <button
                                              @click="nextActivity"
                                              :disabled="currentActivityIndex >= currentTabActivities.length - 1"
                                              class="flex items-center gap-2 px-4 py-2 rounded-lg border-2 transition-all disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-50"
                                              :style="{ borderColor: selectedEnvelope.color, color: selectedEnvelope.color }"
                                            >
                                              <span class="font-medium">Next</span>
                                              <i class="pi pi-chevron-right"></i>
                                            </button>
                                          </div>

                                          <!-- Content Card - 75/25 Layout -->
                                          <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
                                            <div class="flex flex-col lg:flex-row">
                                              
                                              <!-- Left Column: File Preview (75%) -->
                                              <div class="lg:w-3/4 bg-gray-100 p-4 flex items-center justify-center min-h-[400px] relative">
                                                <!-- Multiple Files Navigation -->
                                                <template v-if="currentTabActivities[currentActivityIndex].submission_files && currentTabActivities[currentActivityIndex].submission_files.length > 0">
                                                  <!-- File Counter -->
                                                  <div v-if="currentTabActivities[currentActivityIndex].submission_files.length > 1" 
                                                       class="absolute top-3 right-3 z-20 bg-indigo-600 text-white px-3 py-1 rounded-full text-xs font-bold">
                                                    {{ currentPortfolioFileIndex + 1 }} / {{ currentTabActivities[currentActivityIndex].submission_files.length }}
                                                  </div>
                                                  
                                                  <!-- Previous File Button -->
                                                  <button v-if="currentTabActivities[currentActivityIndex].submission_files.length > 1"
                                                          @click.stop="currentPortfolioFileIndex = Math.max(0, currentPortfolioFileIndex - 1)"
                                                          :disabled="currentPortfolioFileIndex === 0"
                                                          class="absolute left-3 top-1/2 -translate-y-1/2 z-20 w-10 h-10 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-gray-100 transition-all disabled:opacity-30 disabled:cursor-not-allowed">
                                                    <i class="pi pi-chevron-left text-indigo-600 text-lg"></i>
                                                  </button>
                                                  
                                                  <!-- Next File Button -->
                                                  <button v-if="currentTabActivities[currentActivityIndex].submission_files.length > 1"
                                                          @click.stop="currentPortfolioFileIndex = Math.min(currentTabActivities[currentActivityIndex].submission_files.length - 1, currentPortfolioFileIndex + 1)"
                                                          :disabled="currentPortfolioFileIndex >= currentTabActivities[currentActivityIndex].submission_files.length - 1"
                                                          class="absolute right-3 top-1/2 -translate-y-1/2 z-20 w-10 h-10 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-gray-100 transition-all disabled:opacity-30 disabled:cursor-not-allowed">
                                                    <i class="pi pi-chevron-right text-indigo-600 text-lg"></i>
                                                  </button>
                                                  
                                                  <!-- File Display -->
                                                  <template v-if="isImageFileTeacher(currentTabActivities[currentActivityIndex].submission_files[currentPortfolioFileIndex])">
                                                    <img :src="getFileUrlTeacher(currentTabActivities[currentActivityIndex].submission_files[currentPortfolioFileIndex])"
                                                         alt="Activity submission"
                                                         class="max-w-full max-h-[380px] object-contain rounded-lg shadow-md cursor-pointer"
                                                         @click="openFileInNewTabTeacher(getFileUrlTeacher(currentTabActivities[currentActivityIndex].submission_files[currentPortfolioFileIndex]))"
                                                    />
                                                  </template>
                                                  <div v-else class="text-center p-6 bg-white rounded-xl shadow-md">
                                                    <i class="pi pi-file-pdf text-6xl text-red-500 mb-4" v-if="currentTabActivities[currentActivityIndex].submission_files[currentPortfolioFileIndex]?.type === 'pdf'"></i>
                                                    <i class="pi pi-file text-6xl text-gray-400 mb-4" v-else></i>
                                                    <p class="text-gray-600 font-medium mb-3">{{ currentTabActivities[currentActivityIndex].submission_files[currentPortfolioFileIndex]?.name || 'File Attached' }}</p>
                                                    <button @click="openFileInNewTabTeacher(getFileUrlTeacher(currentTabActivities[currentActivityIndex].submission_files[currentPortfolioFileIndex]))"
                                                       class="px-5 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors inline-block cursor-pointer">
                                                        <i class="pi pi-external-link mr-2"></i>View File
                                                    </button>
                                                  </div>
                                                </template>
                                                
                                                <!-- Single File (Legacy) -->
                                                <template v-else-if="currentTabActivities[currentActivityIndex].submission_file">
                                                  <template v-if="isImageUrlTeacher(currentTabActivities[currentActivityIndex].submission_file)">
                                                    <img :src="currentTabActivities[currentActivityIndex].submission_file"
                                                         alt="Activity submission"
                                                         class="max-w-full max-h-[380px] object-contain rounded-lg shadow-md cursor-pointer"
                                                         @click="openFileInNewTabTeacher(currentTabActivities[currentActivityIndex].submission_file)"
                                                    />
                                                  </template>
                                                  <div v-else class="text-center p-6 bg-white rounded-xl shadow-md">
                                                    <i class="pi pi-file-pdf text-6xl text-red-500 mb-4" v-if="currentTabActivities[currentActivityIndex].submission_file.includes('pdf')"></i>
                                                    <i class="pi pi-file text-6xl text-gray-400 mb-4" v-else></i>
                                                    <p class="text-gray-600 font-medium mb-3">File Attached</p>
                                                    <button @click="openFileInNewTabTeacher(currentTabActivities[currentActivityIndex].submission_file)"
                                                       class="px-5 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors inline-block cursor-pointer">
                                                        <i class="pi pi-external-link mr-2"></i>View File
                                                    </button>
                                                  </div>
                                                </template>
                                                
                                                <!-- No File -->
                                                <div v-else class="text-center p-6">
                                                  <i class="pi pi-image text-6xl text-gray-300 mb-4"></i>
                                                  <p class="text-gray-500 font-medium">No file attached</p>
                                                </div>
                                              </div>
                                              
                                              <!-- Right Column: Activity Details (25%) - Compact -->
                                              <div class="lg:w-1/4 p-4 bg-white border-l border-gray-200">
                                                <div class="space-y-3">
                                                  <!-- Activity Title -->
                                                  <div>
                                                    <span class="text-xs text-gray-400 uppercase">Title</span>
                                                    <p class="text-sm font-bold text-gray-800 leading-tight">{{ currentTabActivities[currentActivityIndex].title }}</p>
                                                  </div>
                                                  
                                                  <!-- Subject -->
                                                  <div>
                                                    <span class="text-xs text-gray-400 uppercase">Subject</span>
                                                    <p class="text-sm font-medium text-gray-700">{{ currentTabActivities[currentActivityIndex].folder_name || 'N/A' }}</p>
                                                  </div>
                                                  
                                                  <!-- Type -->
                                                  <div>
                                                    <span class="text-xs text-gray-400 uppercase">Type</span>
                                                    <p class="text-sm font-medium text-gray-700 capitalize">{{ currentTabActivities[currentActivityIndex].activity_type || 'Activity' }}</p>
                                                  </div>
                                                  
                                                  <!-- Date & Time -->
                                                  <div>
                                                    <span class="text-xs text-gray-400 uppercase">Submitted</span>
                                                    <p class="text-sm font-medium text-gray-700">
                                                      {{ currentTabActivities[currentActivityIndex].submitted_date || 'N/A' }}
                                                      <span v-if="currentTabActivities[currentActivityIndex].submitted_time" class="text-gray-500">
                                                        {{ currentTabActivities[currentActivityIndex].submitted_time }}
                                                      </span>
                                                    </p>
                                                  </div>
                                                  
                                                  <!-- Status -->
                                                  <div>
                                                    <span class="text-xs text-gray-400 uppercase">Status</span>
                                                    <p>
                                                      <span class="px-2 py-0.5 rounded text-xs font-medium"
                                                            :class="{
                                                              'bg-green-100 text-green-700': currentTabActivities[currentActivityIndex].submission_status === 'scored',
                                                              'bg-purple-100 text-purple-700': currentTabActivities[currentActivityIndex].submission_status === 'compiled' || currentTabActivities[currentActivityIndex].is_compilation,
                                                              'bg-blue-100 text-blue-700': currentTabActivities[currentActivityIndex].submission_status === 'scored_resubmitted',
                                                              'bg-orange-100 text-orange-700': currentTabActivities[currentActivityIndex].submission_status === 'scored_late'
                                                            }">
                                                        {{ getStatusLabelTeacher(currentTabActivities[currentActivityIndex]) }}
                                                      </span>
                                                    </p>
                                                  </div>
                                                  
                                                  <!-- Score -->
                                                  <div class="pt-2 border-t border-gray-100">
                                                    <span class="text-xs text-gray-400 uppercase">Score</span>
                                                    <p class="text-xl font-bold" :class="currentTabActivities[currentActivityIndex].submission_score !== null && !currentTabActivities[currentActivityIndex].is_compilation ? 'text-green-600' : 'text-gray-400'">
                                                      {{ getScoreDisplayTeacher(currentTabActivities[currentActivityIndex]) }}
                                                    </p>
                                                  </div>
                                                  
                                                  <!-- Feedback if exists -->
                                                  <div v-if="currentTabActivities[currentActivityIndex].submission_feedback" class="pt-2 border-t border-gray-100">
                                                    <span class="text-xs text-gray-400 uppercase">Feedback</span>
                                                    <p class="text-xs text-gray-600 mt-1">{{ currentTabActivities[currentActivityIndex].submission_feedback }}</p>
                                                  </div>
                                                </div>
                                              </div>
                                            </div>
                                          </div>
                                        </div>
                                    </div>
                                    </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Show table if not viewing an envelope -->
                            <div v-else>
                                <!-- Header with Buttons -->
                                <div class="flex justify-between items-center mb-6">
                                    <h2 class="text-2xl font-bold text-gray-900">Portfolio Compilation Status</h2>
                                    <div class="flex gap-3">
                                        <button
                                            @click="showNotStartedStudentsDialog = true"
                                            class="px-4 py-2 bg-orange-500 text-white font-semibold rounded-lg hover:bg-orange-600 transition-all duration-200 shadow-md hover:shadow-lg flex items-center gap-2"
                                        >
                                            <i class="pi pi-users"></i>
                                            Not Started
                                            <span v-if="notStartedStudents.length > 0" class="bg-white text-orange-600 px-2 py-0.5 rounded-full text-xs font-bold">
                                                {{ notStartedStudents.length }}
                                            </span>
                                        </button>
                                        <!-- Drop Portfolio Compilation button hidden -->
                                    </div>
                                </div>

                                <!-- Table Container -->
                            <div class="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
                                <!-- Table Header -->
                                <div class="bg-white border-b border-gray-200 px-6 py-4">
                                    <div class="grid grid-cols-5 gap-4 text-gray-700 font-semibold text-sm">
                                        <div class="flex items-center gap-2">
                                            <i class="pi pi-user"></i>
                                            Student Name
                                        </div>
                                        <div class="flex items-center gap-2">
                                            <i class="pi pi-id-card"></i>
                                            ID Number
                                        </div>
                                        <div class="flex items-center gap-2">
                                            <i class="pi pi-calendar"></i>
                                            Date Created
                                        </div>
                                        <div class="flex items-center gap-2">
                                            <i class="pi pi-clock"></i>
                                            Time Created
                                        </div>
                                        <div class="flex items-center gap-2">
                                            <i class="pi pi-check-circle"></i>
                                            Status
                                        </div>
                                    </div>
                                </div>

                                <!-- Table Body -->
                                <div class="divide-y divide-gray-200">
                                    <!-- Student Rows - Clickable when Done -->
                                    <div
                                        v-for="student in portfolioStudents"
                                        :key="student.id"
                                        @click="viewStudentEnvelope(student)"
                                        class="px-6 py-4 hover:bg-indigo-50 transition-colors duration-150 cursor-pointer"
                                        title="Click to view portfolio"
                                    >
                                        <div class="grid grid-cols-5 gap-4 items-center text-sm">
                                            <div class="flex items-center gap-3">
                                                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white font-semibold overflow-hidden">
                                                    <img v-if="student.profile_picture" :src="student.profile_picture" :alt="student.name" class="w-full h-full object-cover" />
                                                    <span v-else>{{ getInitials(student.name) }}</span>
                                                </div>
                                                <span class="font-medium text-gray-900">{{ student.name }}</span>
                                            </div>
                                            <div class="text-gray-700 font-mono">{{ student.idNumber }}</div>
                                            <div class="text-gray-700">{{ student.dateCreated }}</div>
                                            <div class="text-gray-700">{{ student.timeCreated }}</div>
                                            <div>
                                                <span v-if="student.isSubmitted || student.status === 'Done'" class="px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full">Done</span>
                                                <span v-else class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-semibold rounded-full">In Progress</span>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Empty State -->
                                    <div v-if="portfolioStudents.length === 0" class="px-6 py-12 text-center">
                                        <i class="pi pi-inbox text-5xl text-gray-300 mb-4"></i>
                                        <p class="text-gray-500 text-lg font-medium">No students have started yet</p>
                                        <p class="text-gray-400 text-sm mt-2">Students will appear here once they create their portfolio envelope</p>
                                    </div>
                                </div>

                                <!-- Table Footer -->
                                <div class="bg-gray-50 px-6 py-4 border-t border-gray-200">
                                    <div class="text-sm text-gray-600">
                                        <span>Total Students: <strong class="text-indigo-600">{{ portfolioStudents.length }}</strong></span>
                                    </div>
                                </div>
                            </div>
                            </div>
                        </div>
                    </div>
                </template>

                <template v-if="activeTab === 'schedule'">
                    <div class="p-4 md:p-6 bg-transparent">
                        <!-- Calendar Header -->
                        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                            <h2 class="text-xl font-bold text-indigo-900">NOVEMBER 2025</h2>
                            <div class="flex gap-4 items-center">
                                <span class="flex items-center gap-2">
                                    <div class="w-3 h-3 rounded-full bg-indigo-600"></div>
                                    <span class="text-sm text-indigo-700">Class Day</span>
                                </span>
                                <span class="flex items-center gap-2">
                                    <div class="w-3 h-3 rounded-full bg-indigo-100"></div>
                                    <span class="text-sm text-indigo-700">No Class</span>
                                </span>
                            </div>
                        </div>

                        <!-- Days of the Week -->
                        <div class="grid grid-cols-7 text-center font-semibold text-indigo-700 mb-2 bg-indigo-50 p-3 rounded-lg">
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
                                    isClassDay(date + 1) ? 'bg-indigo-100 border-indigo-200' : 'bg-white border-indigo-100'
                                ]"
                                @click="showScheduleDetails(date + 1)">
                                <div class="font-semibold text-indigo-900">{{ date + 1 }}</div>
                                <div v-if="isClassDay(date + 1)" class="text-xs md:text-sm mt-1 text-indigo-700">
                                    {{ day.time }}
                                </div>
                            </div>
                        </div>

                        <!-- Current Schedule Display -->
                        <div v-if="selectedDate" class="mt-4 p-4 rounded-lg bg-indigo-50">
                            <h3 class="font-semibold mb-2 text-indigo-900">
                                Selected Date: November {{ selectedDate }}
                            </h3>
                            <p v-if="isClassDay(selectedDate)" class="text-indigo-700">
                                Class Time: {{ schedule[selectedDate - 1].time }}
                            </p>
                            <p v-else class="text-indigo-700">
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
                                    <h1 class="text-2xl font-bold text-gray-900">My Classroom</h1>
                                </div>
                                <div class="flex items-center gap-2 bg-white px-3 py-1 rounded-full border border-gray-200">
                                    <span class="text-sm text-gray-500">School Year:</span>
                                    <span class="text-sm font-medium text-indigo-700">2024-2025</span>
                                </div>
                            </div>
                        </div>

                        <!-- Classroom Card -->
                        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                            <!-- Students List - Always visible like student view -->
                            <div class="p-6">
                                <div class="flex items-center justify-between mb-4">
                                    <h3 class="text-lg font-semibold text-gray-900">Class Member</h3>
                                    <span class="text-indigo-600 text-sm font-medium">{{ classroomStudents.length }} students</span>
                                </div>

                                <!-- Search Bar -->
                                <div class="mb-4">
                                    <div class="relative">
                                        <i class="pi pi-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                                        <input
                                            v-model="studentSearchQuery"
                                            type="text"
                                            placeholder="Search classmates by name..."
                                            class="w-full px-4 py-2.5 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
                                        />
                                    </div>
                                </div>

                                <!-- Student List - Always visible -->
                                <div class="space-y-3 max-h-96 overflow-y-auto">
                                    <div v-for="(student, index) in filteredStudents" :key="student.id"
                                        class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                                        <span class="text-sm text-gray-500 font-medium w-8">{{ index + 1 }}.</span>
                                        <div class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold overflow-hidden">
                                            <img v-if="student.profile_picture" :src="student.profile_picture" :alt="student.name" class="w-full h-full object-cover" />
                                            <span v-else>{{ getInitials(student.name) }}</span>
                                        </div>
                                        <div class="flex-1">
                                            <p class="font-medium text-gray-900">{{ student.name }}</p>
                                            <p class="text-xs text-gray-500">{{ student.email }}</p>
                                        </div>
                                    </div>

                                    <!-- No Results -->
                                    <div v-if="filteredStudents.length === 0 && studentSearchQuery" class="text-center py-8">
                                        <i class="pi pi-search text-gray-400 text-3xl mb-3"></i>
                                        <p class="text-gray-500">No students found matching "{{ studentSearchQuery }}"</p>
                                    </div>
                                </div>

                                <!-- Empty State -->
                                <div v-if="classroomStudents.length === 0" class="text-center py-8">
                                    <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                        <i class="pi pi-users text-gray-400 text-2xl"></i>
                                    </div>
                                    <h3 class="text-lg font-medium text-gray-900 mb-2">No Students Yet</h3>
                                    <p class="text-gray-500">Students will appear here once they join your classroom.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </div>
        </div>

        <!-- New Folder Dialog -->
        <Dialog v-model:visible="showNewFolderDialog"
            modal
            header="Create New Folder"
            :style="{ width: '90%', maxWidth: '45rem' }">
            <div class="p-4">
                <!-- Form Fields Section -->
                <div class="space-y-4 mb-6">
                    <div>
                        <label for="folderTitle" class="block text-sm font-medium text-gray-900 mb-2">Subject Title</label>
                        <input
                            id="folderTitle"
                            v-model="newFolder.title"
                            type="text"
                            class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
                            placeholder="Enter subject title"
                        >
                    </div>
                </div>

                <!-- Horizontal Divider -->
                <div class="relative my-6">
                    <div class="absolute inset-0 flex items-center">
                        <div class="w-full border-t border-gray-300"></div>
                    </div>
                    <div class="relative flex justify-center text-sm">
                        <span class="px-4 bg-white text-gray-500 font-medium">Preview</span>
                    </div>
                </div>

                <!-- Preview Section - Matching actual folder card design -->
                <div class="flex justify-center">
                    <div class="w-64 bg-white rounded-xl shadow-lg overflow-hidden">
                        <!-- Blue Gradient Header -->
                        <div class="relative bg-gradient-to-br from-indigo-500 to-blue-600 p-5 min-h-[140px]">
                            <!-- Decorative circle in background -->
                            <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/4"></div>
                            
                            <!-- Content -->
                            <div class="relative z-10">
                                <h3 class="text-xl font-bold text-white mb-1">
                                    {{ newFolder.title || 'Subject Title' }}
                                </h3>
                                <p class="text-white/80 text-sm mb-4">Subject Folder</p>
                                <p class="text-white/90 text-sm">0 activities</p>
                            </div>
                            
                            <!-- Teacher Initial Circle -->
                            <div class="absolute right-4 bottom-4 w-14 h-14 rounded-full border-2 border-white/50 bg-indigo-400/50 flex items-center justify-center">
                                <span class="text-white text-xl font-bold">T</span>
                            </div>
                        </div>
                        
                        <!-- White Footer -->
                        <div class="bg-white p-4 flex justify-end">
                            <i class="pi pi-ellipsis-v text-gray-400"></i>
                        </div>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-between items-center">
                    <p class="text-sm text-gray-500">* Preview updates as you type</p>
                    <div class="flex gap-2">
                        <button @click="showNewFolderDialog = false"
                            class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                            Cancel
                        </button>
                        <button
                            @click="createNewFolder"
                            :disabled="!newFolder.title"
                            :class="[
                                'px-4 py-2 rounded-lg transition-colors flex items-center gap-2',
                                newFolder.title ? 'bg-indigo-600 text-white hover:bg-indigo-700' : 'bg-indigo-100 text-indigo-300 cursor-not-allowed'
                            ]"
                        >
                            <i class="pi pi-check"></i>
                            Create Folder
                        </button>
                    </div>
                </div>
            </template>
        </Dialog>

        <!-- Update Folder Dialog -->
        <Dialog v-model:visible="showUpdateFolderDialog"
            modal
            header="Update Portfolio Folder"
            :style="{ width: '90%', maxWidth: '40rem' }">
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Folder Name</label>
                    <input
                        v-model="updateFolderData.title"
                        type="text"
                        placeholder="e.g., Portfolio A, Math Portfolio"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Description (Optional)</label>
                    <textarea
                        v-model="updateFolderData.description"
                        rows="3"
                        placeholder="Add a description for this portfolio folder..."
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    ></textarea>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-2">
                    <button @click="showUpdateFolderDialog = false"
                        class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                        Cancel
                    </button>
                    <button
                        @click="updateFolder"
                        :disabled="!updateFolderData.title"
                        :class="[
                            'px-4 py-2 rounded-lg transition-colors flex items-center gap-2',
                            updateFolderData.title ? 'bg-indigo-600 text-white hover:bg-indigo-700' : 'bg-indigo-100 text-indigo-300 cursor-not-allowed'
                        ]"
                    >
                        <i class="pi pi-check"></i>
                        Update Folder
                    </button>
                </div>
            </template>
        </Dialog>


        <!-- Delete Activity Dialog -->
        <Dialog v-model:visible="showDeleteActivityDialog"
            modal
            header="Delete Activity"
            :style="{ width: '90%', maxWidth: '35rem' }">
            <div class="space-y-4">
                <div class="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <i class="pi pi-exclamation-triangle text-red-600 text-xl mt-0.5"></i>
                    <div>
                        <h4 class="font-semibold text-red-900 mb-1">Warning: Permanent Action</h4>
                        <p class="text-sm text-red-700">
                            Deleting this activity will permanently remove it along with all student submissions and scores.
                        </p>
                        <p class="text-sm text-red-700 mt-2 font-medium">
                            This action cannot be undone!
                        </p>
                    </div>
                </div>

                <div class="space-y-2">
                    <div class="flex items-center justify-between py-2 border-b border-gray-200">
                        <span class="text-sm font-medium text-gray-700">Activity Title:</span>
                        <span class="text-sm text-gray-900 font-semibold">{{ deleteActivityData.title }}</span>
                    </div>
                    <div class="flex items-center justify-between py-2 border-b border-gray-200">
                        <span class="text-sm font-medium text-gray-700">Activity Type:</span>
                        <span class="text-sm text-gray-900 capitalize">{{ deleteActivityData.type }}</span>
                    </div>
                    <div class="flex items-center justify-between py-2">
                        <span class="text-sm font-medium text-gray-700">Status:</span>
                        <span :class="[
                            'text-sm font-medium px-2 py-1 rounded',
                            deleteActivityData.is_published
                                ? 'bg-green-100 text-green-800'
                                : 'bg-gray-100 text-gray-800'
                        ]">
                            {{ deleteActivityData.is_published ? 'Published' : 'Draft' }}
                        </span>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-2">
                    <button @click="showDeleteActivityDialog = false"
                        class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                        Cancel
                    </button>
                    <button
                        @click="confirmDeleteActivity"
                        :disabled="isDeletingActivity"
                        :class="[
                            'px-4 py-2 text-white rounded-lg transition-colors flex items-center gap-2',
                            isDeletingActivity
                                ? 'bg-gray-400 cursor-not-allowed'
                                : 'bg-red-600 hover:bg-red-700'
                        ]"
                    >
                        <i v-if="isDeletingActivity" class="pi pi-spin pi-spinner"></i>
                        <i v-else class="pi pi-trash"></i>
                        {{ isDeletingActivity ? 'Deleting...' : 'Delete Activity' }}
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
                    <button @click="archiveClass"
                        class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg flex items-center gap-2">
                        <i class="pi pi-archive"></i>
                        Archive Class
                    </button>
                </div>
            </div>
        </Dialog>

        <!-- Portfolio Compilation Confirmation Dialog -->
        <Dialog v-model:visible="showPortfolioCompilationDialog"
            modal
            header="Start Portfolio Compilation"
            :style="{ width: '90%', maxWidth: '30rem' }">
            <div class="p-6">
                <div class="mb-6 text-center">
                    <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 mb-4">
                        <i class="pi pi-book text-indigo-600 text-xl"></i>
                    </div>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">Notify Students?</h3>
                    <p class="text-sm text-gray-500">
                        This will notify all students in this class to start compiling their portfolios. Do you want to proceed?
                    </p>
                </div>
                <div class="flex justify-end gap-3">
                    <button @click="showPortfolioCompilationDialog = false"
                        class="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg">
                        Cancel
                    </button>
                    <button @click="confirmPortfolioCompilation"
                        class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg flex items-center gap-2">
                        <i class="pi pi-check"></i>
                        Confirm
                    </button>
                </div>
            </div>
        </Dialog>

        <!-- View Student Envelope Dialog -->
        <Dialog v-model:visible="showEnvelopeViewDialog"
            modal
            header="Student Portfolio Envelope"
            :style="{ width: '95%', maxWidth: '50rem' }">
            <div v-if="selectedEnvelope" class="p-6">
                <!-- Envelope Display -->
                <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                    <div class="relative w-full aspect-[21/9]"
                         :style="{ backgroundColor: selectedEnvelope.color }">

                        <!-- Pattern Overlay -->
                        <div v-if="selectedEnvelope.pattern === 'dots'"
                             class="absolute inset-0 opacity-20"
                             style="background-image: radial-gradient(circle, white 2px, transparent 2px); background-size: 20px 20px;">
                        </div>
                        <div v-else-if="selectedEnvelope.pattern === 'lines'"
                             class="absolute inset-0 opacity-20"
                             style="background-image: repeating-linear-gradient(45deg, white 0, white 2px, transparent 2px, transparent 10px);">
                        </div>
                        <div v-else-if="selectedEnvelope.pattern === 'grid'"
                             class="absolute inset-0 opacity-20"
                             style="background-image: linear-gradient(white 1px, transparent 1px), linear-gradient(90deg, white 1px, transparent 1px); background-size: 20px 20px;">
                        </div>

                        <!-- Envelope Flap -->
                        <div class="absolute top-0 left-0 right-0 h-1/4 border-b-4 border-white/30"
                             :style="{
                                 background: `linear-gradient(180deg, ${selectedEnvelope.color} 0%, ${adjustBrightness(selectedEnvelope.color, -20)} 100%)`
                             }">
                            <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-0 h-0
                                        border-l-[150px] border-r-[150px] border-t-[80px] border-l-transparent border-r-transparent"
                                 :style="{ borderTopColor: adjustBrightness(selectedEnvelope.color, -20) }">
                            </div>
                        </div>

                        <!-- Content Area -->
                        <div class="absolute inset-0 flex flex-col items-center justify-center p-4 text-center">
                            <div class="bg-white/20 backdrop-blur-md rounded-2xl p-6 shadow-xl border border-white/30 max-w-sm w-full">
                                <h1 class="text-2xl font-bold text-white mb-2" style="text-shadow: 0 2px 8px rgba(0,0,0,0.3)">
                                    {{ selectedEnvelope.title }}
                                </h1>
                                <p class="text-base text-white/90 font-medium mb-1" style="text-shadow: 0 1px 4px rgba(0,0,0,0.2)">
                                    {{ selectedEnvelope.name }}
                                </p>
                                <p class="text-sm text-white/80" style="text-shadow: 0 1px 4px rgba(0,0,0,0.2)">
                                    {{ selectedEnvelope.className }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Student Info -->
                <div class="mt-6 bg-gray-50 rounded-lg p-4">
                    <div class="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <span class="text-gray-600">Student Name:</span>
                            <span class="ml-2 font-medium text-gray-900">{{ selectedEnvelope.name }}</span>
                        </div>
                        <div>
                            <span class="text-gray-600">ID Number:</span>
                            <span class="ml-2 font-medium text-gray-900 font-mono">{{ selectedEnvelope.idNumber }}</span>
                        </div>
                        <div>
                            <span class="text-gray-600">Date Created:</span>
                            <span class="ml-2 font-medium text-gray-900">{{ selectedEnvelope.dateCreated }}</span>
                        </div>
                        <div>
                            <span class="text-gray-600">Time Created:</span>
                            <span class="ml-2 font-medium text-gray-900">{{ selectedEnvelope.timeCreated }}</span>
                        </div>
                    </div>
                </div>

                <!-- Close Button -->
                <div class="mt-6 flex justify-end">
                    <button
                        @click="showEnvelopeViewDialog = false"
                        class="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                    >
                        Close
                    </button>
                </div>
            </div>
        </Dialog>

        <!-- Delete Criteria Confirmation Dialog -->
        <Dialog v-model:visible="showDeleteCriteriaDialog"
                modal
                header="Delete Criterion"
                :style="{ width: '90%', maxWidth: '28rem' }">
            <div class="p-6">
                <div class="flex items-start gap-4">
                    <div class="mt-1 flex-shrink-0">
                        <div class="h-10 w-10 rounded-full bg-red-100 flex items-center justify-center">
                            <i class="pi pi-exclamation-triangle text-red-600 text-xl"></i>
                        </div>
                    </div>
                    <div>
                        <h3 class="text-lg font-medium text-gray-900">Delete Criterion</h3>
                        <p class="mt-1 text-gray-600">
                            Are you sure you want to delete this criterion? This action cannot be undone.
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <button @click="showDeleteCriteriaDialog = false"
                        class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500">
                        Cancel
                    </button>
                    <button @click="removeSavedCriterion"
                        class="px-4 py-2 text-white bg-red-600 rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                        <i class="pi pi-trash mr-2"></i>
                        Delete
                    </button>
                </div>
            </template>
        </Dialog>

        <!-- Drop Portfolio Compilation Confirmation Dialog -->
        <Dialog v-model:visible="showDropCompilationDialog"
            modal
            header="Drop Portfolio Compilation"
            :style="{ width: '90%', maxWidth: '30rem' }">
            <div class="p-6">
                <div class="mb-6 text-center">
                    <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
                        <i class="pi pi-exclamation-triangle text-red-600 text-xl"></i>
                    </div>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">Drop Portfolio Compilation?</h3>
                    <p class="text-sm text-gray-500">
                        This will delete the portfolio compilation and notify all students that the compilation has been cancelled. Do you want to proceed?
                    </p>
                </div>
                <div class="flex justify-end gap-3">
                    <button @click="showDropCompilationDialog = false"
                        class="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg">
                        Cancel
                    </button>
                    <button @click="confirmDropPortfolioCompilation"
                        class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg flex items-center gap-2">
                        <i class="pi pi-trash"></i>
                        Drop
                    </button>
                </div>
            </div>
        </Dialog>

        <!-- Not Started Students Dialog -->
        <Dialog v-model:visible="showNotStartedStudentsDialog"
            modal
            header="Students Who Haven't Started"
            :style="{ width: '90%', maxWidth: '40rem' }">
            <div class="p-4">
                <div v-if="notStartedStudents.length === 0" class="text-center py-8">
                    <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-green-100 mb-4">
                        <i class="pi pi-check-circle text-green-600 text-2xl"></i>
                    </div>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">All Students Have Started!</h3>
                    <p class="text-sm text-gray-500">Every student in this class has created their portfolio envelope.</p>
                </div>
                <div v-else>
                    <p class="text-sm text-gray-600 mb-4">
                        The following <strong class="text-orange-600">{{ notStartedStudents.length }}</strong> student(s) have not yet created their portfolio envelope:
                    </p>
                    <div class="max-h-80 overflow-y-auto border border-gray-200 rounded-lg">
                        <div class="divide-y divide-gray-200">
                            <div v-for="student in notStartedStudents" :key="student.id" class="px-4 py-3 flex items-center gap-3 hover:bg-gray-50">
                                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center text-white font-semibold overflow-hidden">
                                    <img v-if="student.profile_picture" :src="student.profile_picture" :alt="student.name" class="w-full h-full object-cover" />
                                    <span v-else>{{ getInitials(student.name) }}</span>
                                </div>
                                <div class="flex-1">
                                    <p class="font-medium text-gray-900">{{ student.name || student.username }}</p>
                                    <p class="text-xs text-gray-500 font-mono">{{ student.id_number || 'No ID' }}</p>
                                </div>
                                <span class="px-2 py-1 bg-orange-100 text-orange-700 text-xs font-semibold rounded-full">
                                    Not Started
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex justify-end mt-4">
                    <button @click="showNotStartedStudentsDialog = false"
                        class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg">
                        Close
                    </button>
                </div>
            </div>
        </Dialog>

        <!-- Add Activity Dialog -->
        <Dialog v-model:visible="showAddActivityDialog"
            modal
            header="Add New Activity"
            :style="{ width: '98%', maxWidth: '80rem' }"
            :contentStyle="{ maxHeight: '85vh', overflow: 'auto' }">
            <div class="p-6">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Left Column: Activity Area -->
                    <div class="space-y-2.5">
                        <h3 class="text-base font-semibold text-gray-900 mb-2">Activity Details</h3>

                        <div>
                            <label for="activityType" class="block text-xs font-medium text-gray-700 mb-0.5">Activity Type</label>
                            <Dropdown
                                id="activityType"
                                v-model="newActivity.type"
                                :options="activityTypes"
                                optionLabel="name"
                                placeholder="Select type"
                                class="w-full text-sm"
                                :class="{'p-invalid': !newActivity.type}"
                            >
                                <template #value="slotProps">
                                    <div v-if="slotProps.value" class="flex items-center">
                                        <span>{{ slotProps.value.name }}</span>
                                    </div>
                                    <span v-else>
                                        {{ slotProps.placeholder }}
                                    </span>
                                </template>
                                <template #option="slotProps">
                                    <div class="flex items-center">
                                        <span>{{ slotProps.option.name }}</span>
                                    </div>
                                </template>
                            </Dropdown>
                        </div>
                        <div>
                            <div class="flex items-center mb-0.5">
                                <label for="activityTitle" class="block text-xs font-medium text-gray-700">
                                    Activity Title <span class="text-red-500">*</span>
                                </label>
                            </div>
                            <input
                                id="activityTitle"
                                v-model="newActivity.title"
                                type="text"
                                required
                                class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                                placeholder="Enter title"
                            >
                        </div>
                        <div>
                            <div class="flex items-center justify-between mb-0.5">
                                <label for="activityDescription" class="block text-xs font-medium text-gray-700">Instruction</label>
                                <div class="flex items-center gap-1">
                                    <button
                                        @click="triggerInstructionFileUpload('new')"
                                        type="button"
                                        class="text-xs text-indigo-600 hover:text-indigo-800 flex items-center gap-1 px-2 py-1 hover:bg-indigo-50 rounded transition-colors"
                                        title="Attach file for instructions"
                                    >
                                        <i class="pi pi-paperclip text-sm"></i>
                                        <span>Attach</span>
                                    </button>
                                    <button
                                        @click="openPreviewDialog('instruction', newActivity.description)"
                                        type="button"
                                        class="text-xs text-indigo-600 hover:text-indigo-800 flex items-center gap-1 px-2 py-1 hover:bg-indigo-50 rounded transition-colors"
                                        title="Expand to edit in larger view"
                                    >
                                        <i class="pi pi-expand text-sm"></i>
                                        <span>Expand</span>
                                    </button>
                                </div>
                            </div>
                            <!-- Attached files display for new activity -->
                            <div v-if="newActivity.instructionFiles && newActivity.instructionFiles.length > 0" class="mb-2 flex flex-wrap gap-2">
                                <div v-for="(file, index) in newActivity.instructionFiles" :key="index" 
                                    class="flex items-center gap-1 px-2 py-1 bg-indigo-50 border border-indigo-200 rounded-lg text-xs">
                                    <i :class="getFileIcon(file.type)" class="text-indigo-600"></i>
                                    <span 
                                        class="text-gray-700 max-w-[120px] truncate cursor-pointer hover:text-indigo-600 hover:underline"
                                        @click="viewInstructionFile(file)"
                                        title="Click to view file"
                                    >{{ file.name }}</span>
                                    <button @click="removeInstructionFile('new', index)" type="button" class="text-red-500 hover:text-red-700 ml-1">
                                        <i class="pi pi-times text-xs"></i>
                                    </button>
                                </div>
                            </div>
                            <textarea
                                id="activityDescription"
                                v-model="newActivity.description"
                                rows="2"
                                class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
                                placeholder="Enter instruction for the activity"
                            ></textarea>
                        </div>
                        <div>
                            <label for="activityDate" class="block text-xs font-medium text-gray-700 mb-0.5">
                                Due Date <span class="text-red-500">*</span>
                            </label>
                            <input
                                id="activityDate"
                                v-model="newActivity.dueDate"
                                type="date"
                                required
                                :min="getTodayDate()"
                                class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            >
                        </div>
                        <div>
                            <label for="activityTime" class="block text-xs font-medium text-gray-700 mb-0.5">
                                Due Time <span class="text-red-500">*</span>
                            </label>
                            <input
                                id="activityTime"
                                v-model="newActivity.dueTime"
                                type="time"
                                required
                                :min="getMinTime()"
                                class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            >
                        </div>
                    </div>

                    <!-- Right Column: Scoring Criteria -->
                    <div class="space-y-4">
                        <div class="flex items-center justify-between">
                            <h3 class="text-lg font-semibold text-gray-900">
                                Scoring Criteria <span class="text-red-500">*</span>
                            </h3>
                            <button
                                @click="addCriterion"
                                type="button"
                                class="flex items-center gap-1 px-3 py-1.5 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                            >
                                <i class="pi pi-plus text-xs"></i>
                                Add Criterion
                            </button>
                        </div>

                        <!-- Criteria List -->
                        <div class="space-y-2.5 max-h-96 overflow-y-auto pr-2">
                            <div
                                v-for="(criterion, index) in savedCriteria"
                                :key="index"
                                class="p-3 bg-white border border-gray-200 rounded-lg hover:border-indigo-300 transition-colors"
                                :class="{ 'border-green-200 bg-green-50': criterion.isCreated }"
                            >
                                <div class="flex items-center gap-2">
                                    <div class="w-2 h-2 rounded-full flex-shrink-0"
                                         :class="criterion.isCreated ? 'bg-green-500' : 'bg-indigo-500'"></div>
                                    <div class="flex-1 flex items-center gap-1">
                                        <input
                                            v-model="criterion.name"
                                            type="text"
                                            placeholder="Enter Criteria"
                                            required
                                            :disabled="criterion.isCreated && !criterion.isEditing"
                                            class="flex-1 min-w-0 block w-full px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                                            :class="{
                                                'border-red-300': !criterion.name && !criterion.isCreated,
                                                'bg-gray-100': criterion.isEditing
                                            }"
                                            @input="updateCriteriaName($event, index)"
                                        />
                                        <button
                                            v-if="criterion.isEditing"
                                            @click="openPreviewDialog('criteria', criterion.name, index)"
                                            type="button"
                                            class="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                                            title="Expand to edit in larger view"
                                        >
                                            <i class="pi pi-window-maximize text-sm"></i>
                                        </button>
                                    </div>
                                    <input
                                        v-model.number="criterion.maxScore"
                                        type="number"
                                        min="0"
                                        max="100"
                                        placeholder="Score"
                                        required
                                        :disabled="criterion.isCreated && !criterion.isEditing"
                                        class="w-20 px-2 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-center"
                                        :class="{
                                            'border-red-300': (criterion.maxScore === '' || criterion.maxScore === null || criterion.maxScore === undefined) && !criterion.isCreated,
                                            'bg-gray-50 cursor-not-allowed': criterion.isCreated && !criterion.isEditing
                                        }"
                                    />
                                    <span class="text-xs text-gray-500 font-medium">pts</span>

                                    <!-- Create Button (only for new criteria) -->
                                    <button
                                        v-if="!criterion.isCreated"
                                        @click="createCriterion(index)"
                                        type="button"
                                        class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors"
                                    >
                                        Create
                                    </button>

                                    <!-- Remove Button (only for new criteria) -->
                                    <button
                                        v-if="!criterion.isCreated"
                                        @click="removeNewCriterion(index)"
                                        type="button"
                                        class="px-4 py-2 text-sm font-medium text-red-700 bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
                                    >
                                        Remove
                                    </button>

                                    <!-- Update Button (only for created criteria not being edited) -->
                                    <button
                                        v-if="criterion.isCreated && !criterion.isEditing"
                                        @click="enableEdit(index)"
                                        type="button"
                                        class="px-4 py-2 text-sm font-medium text-green-700 bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
                                    >
                                        Update
                                    </button>

                                    <!-- Confirm Button (only when editing) -->
                                    <button
                                        v-if="criterion.isCreated && criterion.isEditing"
                                        @click="confirmEdit(index)"
                                        type="button"
                                        class="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
                                    >
                                        Confirm
                                    </button>

                                    <!-- Cancel Button (only when editing) -->
                                    <button
                                        v-if="criterion.isCreated && criterion.isEditing"
                                        @click="cancelEdit(index)"
                                        type="button"
                                        class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                                    >
                                        Cancel
                                    </button>

                                    <!-- Delete Button (only for created criteria not being edited) -->
                                    <button
                                        v-if="criterion.isCreated && !criterion.isEditing"
                                        @click="confirmDeleteCriterion(index)"
                                        type="button"
                                        class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                        title="Delete criterion"
                                    >
                                        <i class="pi pi-trash text-sm"></i>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Total Score Display -->
                        <div class="p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                            <div class="flex items-center justify-between">
                                <span class="text-base font-semibold text-indigo-900">Total Points:</span>
                                <span class="text-2xl font-bold text-indigo-700">
                                    {{ savedCriteria.reduce((sum, c) => sum + (parseInt(c.maxScore) || 0), 0) }} pts
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end items-center">
                    <div class="flex gap-2">
                        <button @click="showAddActivityDialog = false"
                            class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                            Cancel
                        </button>
                        <button
                            @click="addNewActivity"
                            class="px-4 py-2 rounded-lg transition-colors flex items-center gap-2 bg-indigo-600 text-white hover:bg-indigo-700"
                        >
                            <i class="pi pi-check"></i>
                            Add Activity
                        </button>
                    </div>
                </div>
            </template>
        </Dialog>

        <!-- Preview/Review Dialog for Long Text Inputs -->
        <Dialog
            v-model:visible="showPreviewDialog"
            :header="previewDialogTitle"
            :style="{ width: '90vw', maxWidth: '700px' }"
            :modal="true"
            :closable="true"
            :dismissableMask="true"
            @keydown.escape="closePreviewDialog"
        >
            <div class="space-y-4">
                <!-- Preview Label -->
                <div class="text-sm text-gray-600 bg-blue-50 p-3 rounded-lg border border-blue-200">
                    <i class="pi pi-info-circle mr-2 text-blue-600"></i>
                    <span v-if="previewDialogType === 'title'">Edit your activity title with better readability and space.</span>
                    <span v-else-if="previewDialogType === 'instruction'">Edit your activity instructions with a larger text area for comfortable typing.</span>
                    <span v-else-if="previewDialogType === 'criteria'">Edit your scoring criteria with improved visibility.</span>
                </div>

                <!-- Text Area for Editing -->
                <div>
                    <label class="block text-sm font-medium text-gray-900 mb-2">Content</label>
                    <textarea
                        ref="previewTextareaRef"
                        v-model="previewTempContent"
                        :rows="previewDialogType === 'title' ? 3 : 8"
                        class="w-full px-4 py-3 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-vertical font-mono"
                        :placeholder="previewDialogType === 'title' ? 'Enter activity title...' : previewDialogType === 'instruction' ? 'Enter activity instructions...' : 'Enter scoring criteria...'"
                        @keydown.ctrl.enter="savePreviewContent"
                        @keydown.meta.enter="savePreviewContent"
                    ></textarea>
                </div>

            </div>
            <template #footer>
                <div class="flex justify-end gap-2">
                    <button
                        @click="closePreviewDialog"
                        class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium"
                    >
                        <i class="pi pi-times mr-2"></i>
                        Cancel
                    </button>
                    <button
                        @click="savePreviewContent"
                        class="px-4 py-2 text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium flex items-center gap-2"
                    >
                        <i class="pi pi-check"></i>
                        Save & Apply
                    </button>
                </div>
            </template>
        </Dialog>

        <!-- Edit Activity Dialog -->
        <Dialog v-model:visible="showEditDialog"
                modal
                header="Edit Activity"
                :style="{ width: '98%', maxWidth: '80rem' }"
                :contentStyle="{ maxHeight: '85vh', overflow: 'auto' }">
            <div class="p-6">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Left Column: Activity Details -->
                    <div class="space-y-2.5">
                        <h3 class="text-base font-semibold text-gray-900 mb-2">Activity Details</h3>

                        <div>
                            <label for="editActivityType" class="block text-xs font-medium text-gray-700 mb-0.5">
                                Activity Type <span class="text-red-500">*</span>
                            </label>
                            <Dropdown
                                id="editActivityType"
                                v-model="editActivityData.type"
                                :options="activityTypes"
                                optionLabel="name"
                                placeholder="Select type"
                                class="w-full text-sm"
                                :class="{'p-invalid': !editActivityData.type}"
                            >
                                <template #value="slotProps">
                                    <div v-if="slotProps.value" class="flex items-center">
                                        <span>{{ slotProps.value.name }}</span>
                                    </div>
                                    <span v-else>
                                        {{ slotProps.placeholder }}
                                    </span>
                                </template>
                                <template #option="slotProps">
                                    <div class="flex items-center">
                                        <span>{{ slotProps.option.name }}</span>
                                    </div>
                                </template>
                            </Dropdown>
                        </div>
                        <div>
                            <label for="editActivityTitle" class="block text-xs font-medium text-gray-700 mb-0.5">
                                Activity Title <span class="text-red-500">*</span>
                            </label>
                            <input
                                id="editActivityTitle"
                                v-model="editActivityData.title"
                                type="text"
                                class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                                placeholder="Enter title"
                            >
                        </div>
                        <div>
                            <div class="flex items-center justify-between mb-0.5">
                                <label for="editActivityDescription" class="block text-xs font-medium text-gray-700">Instruction</label>
                                <div class="flex items-center gap-1">
                                    <button
                                        @click="triggerInstructionFileUpload('edit')"
                                        type="button"
                                        class="text-xs text-indigo-600 hover:text-indigo-800 flex items-center gap-1 px-2 py-1 hover:bg-indigo-50 rounded transition-colors"
                                        title="Attach file for instructions"
                                    >
                                        <i class="pi pi-paperclip text-sm"></i>
                                        <span>Attach</span>
                                    </button>
                                    <button
                                        @click="openPreviewDialog('instruction', editActivityData.description)"
                                        type="button"
                                        class="text-xs text-indigo-600 hover:text-indigo-800 flex items-center gap-1 px-2 py-1 hover:bg-indigo-50 rounded transition-colors"
                                        title="Expand to edit in larger view"
                                    >
                                        <i class="pi pi-expand"></i>
                                        <span>Expand</span>
                                    </button>
                                </div>
                            </div>
                            <!-- Attached files display for edit activity -->
                            <div v-if="editActivityData.instructionFiles && editActivityData.instructionFiles.length > 0" class="mb-2 flex flex-wrap gap-2">
                                <div v-for="(file, index) in editActivityData.instructionFiles" :key="index" 
                                    class="flex items-center gap-1 px-2 py-1 bg-indigo-50 border border-indigo-200 rounded-lg text-xs">
                                    <i :class="getFileIcon(file.type)" class="text-indigo-600"></i>
                                    <span 
                                        class="text-gray-700 max-w-[120px] truncate cursor-pointer hover:text-indigo-600 hover:underline"
                                        @click="viewInstructionFile(file)"
                                        title="Click to view file"
                                    >{{ file.name }}</span>
                                    <button @click="removeInstructionFile('edit', index)" type="button" class="text-red-500 hover:text-red-700 ml-1">
                                        <i class="pi pi-times text-xs"></i>
                                    </button>
                                </div>
                            </div>
                            <textarea
                                id="editActivityDescription"
                                v-model="editActivityData.description"
                                rows="2"
                                class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
                                placeholder="Enter instruction"
                            ></textarea>
                        </div>
                        <div>
                            <label for="editActivityDate" class="block text-xs font-medium text-gray-700 mb-0.5">
                                Due Date <span class="text-red-500">*</span>
                            </label>
                            <input
                                id="editActivityDate"
                                v-model="editActivityData.dueDate"
                                type="date"
                                :min="getTodayDate()"
                                class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            >
                        </div>
                        <div>
                            <label for="editActivityTime" class="block text-xs font-medium text-gray-700 mb-0.5">
                                Due Time <span class="text-red-500">*</span>
                            </label>
                            <input
                                id="editActivityTime"
                                v-model="editActivityData.dueTime"
                                type="time"
                                :min="getMinTimeForEdit()"
                                class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            >
                        </div>
                    </div>

                    <!-- Right Column: Scoring Criteria -->
                    <div class="space-y-4">
                        <div class="flex items-center justify-between">
                            <h3 class="text-lg font-semibold text-gray-900">
                                Scoring Criteria <span class="text-red-500">*</span>
                            </h3>
                            <button
                                @click="editScoringCriteria.push({ name: '', maxScore: 0, isCreated: false, isEditing: false })"
                                type="button"
                                class="flex items-center gap-1 px-3 py-1.5 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                            >
                                <i class="pi pi-plus text-xs"></i>
                                Add Criterion
                            </button>
                        </div>

                        <!-- Criteria List -->
                        <div class="space-y-2.5 max-h-96 overflow-y-auto pr-2">
                            <div
                                v-for="(criterion, index) in editScoringCriteria"
                                :key="index"
                                class="p-3 bg-white border border-gray-200 rounded-lg hover:border-indigo-300 transition-colors"
                            >
                                <div class="flex items-center gap-2">
                                    <div class="w-2 h-2 rounded-full flex-shrink-0 bg-indigo-500"></div>
                                    <input
                                        v-model="criterion.name"
                                        type="text"
                                        placeholder="Name"
                                        class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                                    />
                                    <input
                                        v-model.number="criterion.maxScore"
                                        type="number"
                                        min="0"
                                        max="100"
                                        placeholder="Score"
                                        class="w-20 px-2 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-center"
                                    />
                                    <span class="text-xs text-gray-500 font-medium">pts</span>

                                    <!-- Remove Button -->
                                    <button
                                        @click="editScoringCriteria.splice(index, 1)"
                                        type="button"
                                        class="px-4 py-2 text-sm font-medium text-red-700 bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Total Points Display -->
                        <div v-if="editScoringCriteria.length > 0" class="p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                            <div class="flex items-center justify-between">
                                <span class="text-sm font-semibold text-indigo-900">Total Points:</span>
                                <span class="text-2xl font-bold text-indigo-700">
                                    {{ editScoringCriteria.reduce((sum, c) => sum + (parseInt(c.maxScore) || 0), 0) }}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end items-center">
                    <div class="flex gap-2">
                        <button @click="showEditDialog = false"
                            class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                            Cancel
                        </button>
                        <button
                            @click="updateActivity"
                            class="px-4 py-2 rounded-lg transition-colors flex items-center gap-2 bg-indigo-600 text-white hover:bg-indigo-700"
                        >
                            <i class="pi pi-check"></i>
                            Save Changes
                        </button>
                    </div>
                </div>
            </template>
        </Dialog>

        <!-- Submit Confirmation Dialog -->
        <Dialog v-model:visible="showSubmitDialog"
                modal
                header="Publish Activity"
                :style="{ width: '90%', maxWidth: '28rem' }">
            <div class="p-6">
                <div class="flex items-start gap-4">
                    <div class="mt-1 flex-shrink-0">
                        <div class="h-10 w-10 rounded-full bg-green-100 flex items-center justify-center">
                            <i class="pi pi-send text-green-600 text-xl"></i>
                        </div>
                    </div>
                    <div>
                        <h3 class="text-lg font-medium text-gray-900">Publish Activity to Students</h3>
                        <p class="mt-1 text-gray-600">
                            Are you sure you want to publish "<span class="font-medium">{{ activityToSubmit?.title }}</span>"?
                            Students will be notified and can start working on this activity.
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <button @click="showSubmitDialog = false"
                        class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Cancel
                    </button>
                    <button @click="confirmSubmitActivity"
                        class="px-4 py-2 text-white bg-green-600 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 flex items-center gap-2">
                        <i class="pi pi-check"></i>
                        Confirm & Publish
                    </button>
                </div>
            </template>
        </Dialog>

        <!-- Retract Confirmation Dialog -->
        <Dialog v-model:visible="showRetractDialog"
                modal
                header="Retract Activity"
                :style="{ width: '90%', maxWidth: '28rem' }">
            <div class="p-6">
                <div class="text-center">
                    <div class="mx-auto flex-shrink-0 h-12 w-12 rounded-full bg-orange-100 flex items-center justify-center">
                        <i class="pi pi-undo text-orange-600 text-2xl"></i>
                    </div>
                    <h3 class="mt-5 text-lg font-semibold text-gray-900">Retract Activity from Students</h3>
                    <div class="mt-2">
                        <p class="text-sm text-gray-500">
                            Are you sure you want to retract "<span class="font-bold text-gray-700 break-words">{{ activityToRetract?.title }}</span>"?
                            <br><br>
                            Students will no longer be able to see or submit this activity. You can publish it again later.
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <button @click="showRetractDialog = false"
                        class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Cancel
                    </button>
                    <button @click="confirmRetractActivity"
                        class="px-4 py-2 text-white bg-orange-600 rounded-lg hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 flex items-center gap-2">
                        <i class="pi pi-undo"></i>
                        Confirm & Retract
                    </button>
                </div>
            </template>
        </Dialog>

        <!-- Delete Confirmation Dialog -->
        <Dialog v-model:visible="showDeleteDialog"
                modal
                header="Confirm Deletion"
                :style="{ width: '90%', maxWidth: '28rem' }">
            <div class="p-6">
                <div class="flex items-start gap-4">
                    <div class="mt-1 flex-shrink-0">
                        <div class="h-10 w-10 rounded-full bg-red-100 flex items-center justify-center">
                            <i class="pi pi-exclamation-triangle text-red-600 text-xl"></i>
                        </div>
                    </div>
                    <div>
                        <h3 class="text-lg font-medium text-gray-900">Delete Activity Permanently</h3>
                        <p class="mt-1 text-gray-600">
                            Are you sure you want to delete "<span class="font-medium">{{ activityToDelete.activity?.title }}</span>"?
                            This will permanently delete the activity and all associated student submissions. This action cannot be undone.
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <button @click="showDeleteDialog = false"
                        class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Cancel
                    </button>
                    <button @click="handleDelete"
                        class="px-4 py-2 text-white bg-red-600 rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 flex items-center gap-2">
                        <i class="pi pi-trash"></i>
                        Confirm & Delete
                    </button>
                </div>
            </template>
        </Dialog>

        <!-- Archive Toast Notification -->
        <div v-if="showArchiveToast" class="fixed bottom-6 right-6 z-[9999] transition-all duration-300 transform"
             :class="{'translate-x-0 opacity-100': showArchiveToast, 'translate-x-full opacity-0': !showArchiveToast}">
            <div class="bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden w-96">
                <div class="p-4 flex items-start gap-3">
                    <div class="flex-shrink-0 mt-0.5">
                        <div class="w-9 h-9 rounded-full bg-emerald-100 flex items-center justify-center">
                            <i class="pi pi-archive text-emerald-600 text-sm"></i>
                        </div>
                    </div>
                    <div class="flex-1 min-w-0">
                        <div class="flex justify-between items-start">
                            <h4 class="text-[15px] font-semibold text-gray-900">Activity Archived</h4>
                            <button @click="showArchiveToast = false"
                                    class="text-gray-400 hover:text-gray-600 transition-colors"
                                    aria-label="Close notification">
                                <i class="pi pi-times text-sm"></i>
                            </button>
                        </div>
                        <p class="mt-1 text-sm text-gray-600">The activity has been moved to archives. You can restore it within 5 seconds.</p>
                        <div class="mt-3 flex items-center gap-2">
                            <button @click="undoArchive"
                                    class="px-3 py-1.5 text-xs font-medium rounded-lg bg-emerald-50 text-emerald-700 hover:bg-emerald-100 transition-colors border border-emerald-100">
                                Undo Archive
                            </button>
                            <span class="text-xs text-gray-500">5s</span>
                        </div>
                    </div>
                </div>
                <div class="h-1 bg-gray-100 w-full">
                    <div class="h-full bg-emerald-500 transition-all duration-5000 ease-linear"
                         :class="{'w-0': !showArchiveToast, 'w-full': showArchiveToast}"
                         style="transition-duration: 5s;">
                    </div>
                </div>
            </div>
        </div>

        <!-- Drop Folder Confirmation Dialog -->
        <Dialog header="Confirm Drop Folder" v-model:visible="showDropFolderDialog" :modal="true" :style="{ width: '400px' }">
            <div class="p-4">
                <div class="text-center">
                    <i class="pi pi-exclamation-triangle text-5xl text-amber-500"></i>
                    <p class="text-lg font-semibold mt-4">Are you sure you want to drop this folder?</p>
                    <p class="text-gray-600 mt-2">This action cannot be undone. All associated data will be permanently deleted.</p>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" @click="showDropFolderDialog = false" class="p-button-text" />
                <Button label="Drop Folder" icon="pi pi-trash" @click="confirmDropFolder" class="p-button-danger" />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, inject, nextTick } from 'vue';
import axios from 'axios';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';
import { useToast } from '../../composables/useToast';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Calendar from 'primevue/calendar';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';

// Define emits for navigation
const emit = defineEmits(['navigate']);

// Initialize toast
const { showSuccess, showError, showInfo, showWarning } = useToast();

// Navigate to activity outputs
const navigateToActivityOutputs = (activity, index) => {
    console.log('🚀 Navigating to outputs with activity:', activity);
    console.log('📊 Scoring criteria:', activity.scoringCriteria);

    // Store the selected activity for the outputs page
    localStorage.setItem('selected_activity', JSON.stringify({
        id: activity.id, // Use the actual database ID
        title: activity.title,
        description: activity.description,
        type: activity.type,
        date: activity.date,
        dueDate: activity.due_date,
        class: className.value,
        subject: selectedSubject.value || 'General',
        scoringCriteria: activity.scoringCriteria, // Use camelCase
        instruction_files: activity.instruction_files || [] // Include instruction files
    }));

    // Navigate to outputs page
    emit('navigate', 'TeacherOutputs');
};

// Navigate to special progress page
const navigateToProgress = () => {
    // Store current class context for progress tracking
    localStorage.setItem('progress_class_context', JSON.stringify({
        className: className.value,
        classroomId: selectedClass.value?.id || null,
        subject: selectedSubject.value || 'General'
    }));

    // Navigate to special progress page
    emit('navigate', 'TeacherSprogress');
};

// Activity types (must match backend model choices)
const activityTypes = ref([
    { name: 'Quiz', value: 'Quiz' },
    { name: 'Assignment', value: 'Assignment' },
    { name: 'Project', value: 'Project' },
    { name: 'Exam', value: 'Exam' },
    { name: 'Presentation', value: 'Presentation' },
    { name: 'Contest', value: 'Contest' }
]);

// Subject folders data
const subjectFolders = ref([]);
const isLoadingFolders = ref(false);

// New Folder Dialog State
const showNewFolderDialog = ref(false);
const newFolder = ref({ title: '', description: '' });

// Update Folder Dialog State
const showUpdateFolderDialog = ref(false);
const showDropFolderDialog = ref(false);
const folderToDrop = ref(null);
const updateFolderData = ref({ id: null, title: '', description: '' });

// Archive Folder Dialog State
const showArchiveFolderDialog = ref(false);
const archiveFolderData = ref({ id: null, name: '', items: 0 });

// Delete Activity Dialog State
const showDeleteActivityDialog = ref(false);
const deleteActivityData = ref({ id: null, title: '', type: '', is_published: false, index: null });
const isDeletingActivity = ref(false);

// Folder Menu State
const activeFolderMenuIndex = ref(null);

// Add Activity Dialog State
const showAddActivityDialog = ref(false);
const newActivity = ref({
    title: '',
    type: '',
    description: '',
    dueDate: '',
    dueTime: '',
    instructionFiles: [],
    scoringCriteria: [
        { name: '', maxScore: 10 }
    ]
});

// Saved criteria list (displayed on the right side)
const savedCriteria = ref([
    { name: '', maxScore: 0, isCreated: false, isEditing: false, originalName: '', originalScore: 0 }
]);

// Preview/Review Dialog State
const showPreviewDialog = ref(false);
const previewDialogType = ref(null); // 'title', 'instruction', or 'criteria'
const previewDialogTitle = ref('');
const previewContent = ref('');
const previewCriteriaIndex = ref(null);
const previewTempContent = ref('');
const previewTextareaRef = ref(null);

// Instruction file upload ref
const instructionFileInput = ref(null);
const currentFileUploadMode = ref('new'); // 'new' or 'edit'

const editActivityData = ref({
    id: null,
    title: '',
    type: '',
    description: '',
    dueDate: '',
    dueTime: '',
    instructionFiles: []
});

const editScoringCriteria = ref([]);


// Classroom Management Data
const classroomStudents = ref([]);
const showStudentList = ref(false);
const studentSearchQuery = ref('');
const totalStudents = computed(() => classroomStudents.value.length);
const presentToday = computed(() => classroomStudents.value.filter(s => s.is_active).length);
const absentToday = computed(() => totalStudents.value - presentToday.value);
const attendanceRate = computed(() => {
    if (totalStudents.value === 0) return 0;
    return Math.round((presentToday.value / totalStudents.value) * 100);
});
const totalActivities = computed(() => {
    // Count total activities from all folders
    return subjectFolders.value.reduce((total, folder) => total + (folder.items || 0), 0);
});

// Filtered students based on search query
const filteredStudents = computed(() => {
    if (!studentSearchQuery.value.trim()) {
        return classroomStudents.value;
    }

    const query = studentSearchQuery.value.toLowerCase().trim();
    return classroomStudents.value.filter(student => {
        const name = (student.name || '').toLowerCase();
        const email = (student.email || '').toLowerCase();
        return name.includes(query) || email.includes(query);
    });
});

// Helper function to get initials
const getInitials = (name) => {
    if (!name) return '?';
    const parts = name.split(' ');
    if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
};
const showEditDialog = ref(false);

// Computed property to validate activity form
const isActivityFormValid = computed(() => {
    // Check if required fields are filled
    const hasTitle = newActivity.value.title && newActivity.value.title.trim() !== '';
    const hasDueDate = newActivity.value.dueDate && newActivity.value.dueDate.trim() !== '';
    const hasDueTime = newActivity.value.dueTime && newActivity.value.dueTime.trim() !== '';

    // Check if at least one criterion is created with valid points
    const hasValidCriteria = savedCriteria.value.some(c =>
        c.isCreated &&
        c.name &&
        c.name.trim() !== '' &&
        c.maxScore > 0
    );

    return hasTitle && hasDueDate && hasDueTime && hasValidCriteria;
});

// Instruction File Handling Functions
const triggerInstructionFileUpload = (mode) => {
    currentFileUploadMode.value = mode;
    if (instructionFileInput.value) {
        instructionFileInput.value.click();
    }
};

const handleInstructionFileUpload = (event) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    const mode = currentFileUploadMode.value;
    const targetData = mode === 'new' ? newActivity.value : editActivityData.value;

    if (!targetData.instructionFiles) {
        targetData.instructionFiles = [];
    }

    for (const file of files) {
        // Determine file type
        let fileType = 'file';
        if (file.type.startsWith('image/')) {
            fileType = 'image';
        } else if (file.type === 'application/pdf') {
            fileType = 'pdf';
        } else if (file.type.includes('word') || file.type.includes('document')) {
            fileType = 'document';
        }

        // Create file object with preview URL
        const fileObj = {
            file: file,
            name: file.name,
            type: fileType,
            size: file.size,
            url: URL.createObjectURL(file)
        };

        targetData.instructionFiles.push(fileObj);
    }

    // Reset the input
    event.target.value = '';
};

const removeInstructionFile = (mode, index) => {
    const targetData = mode === 'new' ? newActivity.value : editActivityData.value;
    if (targetData.instructionFiles && targetData.instructionFiles[index]) {
        const fileToRemove = targetData.instructionFiles[index];
        
        // If it's an existing file from the server, mark it for deletion
        if (fileToRemove.isExisting && fileToRemove.id) {
            if (!targetData.deleteInstructionFileIds) {
                targetData.deleteInstructionFileIds = [];
            }
            targetData.deleteInstructionFileIds.push(fileToRemove.id);
            console.log('Marking file for deletion:', fileToRemove.id);
        } else {
            // Revoke the object URL to free memory for new files
            if (fileToRemove.url) {
                URL.revokeObjectURL(fileToRemove.url);
            }
        }
        
        targetData.instructionFiles.splice(index, 1);
    }
};

// View instruction file - opens in new tab or shows preview
const viewInstructionFile = (file) => {
    if (file.url) {
        // Open the file URL in a new tab
        window.open(file.url, '_blank');
    } else if (file.file) {
        // For newly attached files that haven't been uploaded yet, create a temporary URL
        const tempUrl = URL.createObjectURL(file.file);
        window.open(tempUrl, '_blank');
        // Note: We don't revoke immediately as the new tab needs time to load
        // The URL will be cleaned up when the page is closed
    }
};

const getFileIcon = (fileType) => {
    switch (fileType) {
        case 'image':
            return 'pi pi-image';
        case 'pdf':
            return 'pi pi-file-pdf';
        case 'document':
            return 'pi pi-file-word';
        default:
            return 'pi pi-file';
    }
};

// Preview/Review Dialog Functions
const openPreviewDialog = (type, content, index = null) => {
    previewDialogType.value = type;
    previewContent.value = content;
    previewTempContent.value = content;
    previewCriteriaIndex.value = index;

    if (type === 'title') {
        previewDialogTitle.value = 'Edit Activity Title';
    } else if (type === 'instruction') {
        previewDialogTitle.value = 'Edit Activity Instruction';
    } else if (type === 'criteria') {
        previewDialogTitle.value = 'Edit Scoring Criteria';
    }

    showPreviewDialog.value = true;

    // Focus textarea after dialog opens
    nextTick(() => {
        if (previewTextareaRef.value) {
            previewTextareaRef.value.focus();
        }
    });
};

const savePreviewContent = () => {
    try {
        // Get the content (preserve original formatting for instruction)
        const content = previewTempContent.value || '';

        // Validate input based on type
        if (previewDialogType.value === 'title') {
            const trimmedContent = content.trim();
            if (!trimmedContent) {
                showError('Title cannot be empty');
                return;
            }
            // Update both new and edit activity data
            if (showEditDialog.value) {
                editActivityData.value.title = trimmedContent;
            } else {
                newActivity.value.title = trimmedContent;
            }
        } else if (previewDialogType.value === 'instruction') {
            // Preserve original formatting (don't trim) for instruction
            // Update both new and edit activity data
            if (showEditDialog.value) {
                editActivityData.value.description = content;
            } else {
                newActivity.value.description = content;
            }
        } else if (previewDialogType.value === 'criteria') {
            const trimmedContent = content.trim();
            if (previewCriteriaIndex.value !== null) {
                if (!trimmedContent) {
                    showError('Criteria name cannot be empty');
                    return;
                }
                // Update the appropriate criteria array
                if (showEditDialog.value) {
                    editScoringCriteria.value[previewCriteriaIndex.value].name = trimmedContent;
                } else {
                    savedCriteria.value[previewCriteriaIndex.value].name = trimmedContent;
                }
            }
        }

        // Show success feedback
        showSuccess('Changes saved successfully');

        // Close the dialog
        closePreviewDialog();
    } catch (error) {
        console.error('Error saving content:', error);
        showError('Failed to save changes');
    }
};

const closePreviewDialog = () => {
    showPreviewDialog.value = false;
    previewDialogType.value = null;
    previewContent.value = '';
    previewTempContent.value = '';
    previewCriteriaIndex.value = null;
};

// Function to create new folder
const createNewFolder = async () => {
    if (!newFolder.value.title) return;

    try {
        console.log('Creating folder:', newFolder.value);
        console.log('Class name:', className.value);
        const response = await axios.post('/api/portfolio/folders/', {
            name: newFolder.value.title,
            description: newFolder.value.description || '',
            class_name: className.value || 'Grade 1 - A'
        });

        if (response.data) {
            console.log('Folder created successfully:', response.data);
            // Add the new folder to the list
            subjectFolders.value.unshift({
                id: response.data.id,
                name: response.data.name,
                items: 0,
                description: response.data.description || ''
            });

            showNewFolderDialog.value = false;
            newFolder.value = { title: '', description: '' };

            // Broadcast folder creation event to other tabs/windows
            const folderEvent = new CustomEvent('folderCreated', {
                detail: {
                    folderId: response.data.id,
                    folderName: response.data.name,
                    timestamp: Date.now()
                }
            });
            window.dispatchEvent(folderEvent);

            // Also use localStorage for cross-tab communication
            localStorage.setItem('folder_created_trigger', JSON.stringify({
                folderId: response.data.id,
                folderName: response.data.name,
                timestamp: Date.now()
            }));

            console.log('📢 Broadcasted folder creation event');

            // Show success message
            showSuccess('Portfolio folder created successfully!', 'Folder Created');
        }
    } catch (error) {
        console.error('Error creating folder:', error);
        console.error('Error response:', error.response?.data);

        // Show detailed error message
        const errorMsg = error.response?.data?.error || error.message || 'Failed to create folder';
        const errorDetail = error.response?.data?.detail || '';

        if (errorDetail) {
            showError(`${errorMsg}\n\n${errorDetail}`, 'Failed to Create Folder');
        } else {
            showError(errorMsg, 'Failed to Create Folder');
        }

        // If authentication failed, try to re-authenticate
        if (error.response?.status === 401) {
            console.log('Authentication failed, attempting to re-authenticate...');
            const authenticated = await authenticateWithBackend();
            if (authenticated) {
                showInfo('Please try creating the folder again.', 'Re-authenticated');
            }
        }
    }
};

// Toggle folder menu
const toggleFolderMenu = (event, folder, index) => {
    event.stopPropagation();
    activeFolderMenuIndex.value = activeFolderMenuIndex.value === index ? null : index;
};

// Open update folder dialog
const openUpdateFolderModal = (folder) => {
    updateFolderData.value = {
        id: folder.id,
        title: folder.name,
        description: folder.description
    };
    showUpdateFolderDialog.value = true;
};

const dropfolder = (folder) => {
    folderToDrop.value = folder;
    showDropFolderDialog.value = true;
};

const confirmDropFolder = async () => {
    if (!folderToDrop.value) return;

    try {
        await axios.delete(`/api/folders/${folderToDrop.value.id}/delete/`);
        showDropFolderDialog.value = false;
        showSuccess('Folder dropped successfully!', 'The folder has been permanently deleted.');

        // Refresh the folder list
        loadPortfolioFolders();

    } catch (error) {
        console.error('Error dropping folder:', error);
        showError('Failed to drop folder', error.response?.data?.error || 'Please try again.');
        showDropFolderDialog.value = false;
    } finally {
        folderToDrop.value = null;
    }
};

// Update folder
const updateFolder = async () => {
    if (!updateFolderData.value.title) return;

    try {
        console.log('Updating folder:', updateFolderData.value);

        const response = await axios.put(`/api/portfolio/folders/${updateFolderData.value.id}/`, {
            name: updateFolderData.value.title,
            description: updateFolderData.value.description || ''
        });

        if (response.data) {
            console.log('Folder updated successfully:', response.data);

            // Update the folder in the list
            const folderIndex = subjectFolders.value.findIndex(f => f.id === updateFolderData.value.id);
            if (folderIndex !== -1) {
                subjectFolders.value[folderIndex].name = response.data.name;
                subjectFolders.value[folderIndex].description = response.data.description || '';
            }

            // If we're currently viewing this folder's activities, update the selected subject name
            if (selectedFolderId.value === updateFolderData.value.id) {
                selectedSubject.value = response.data.name;
            }

            // Broadcast folder update event to other tabs/windows
            const folderEvent = new CustomEvent('folderUpdated', {
                detail: {
                    folderId: updateFolderData.value.id,
                    folderName: response.data.name,
                    timestamp: Date.now()
                }
            });
            window.dispatchEvent(folderEvent);

            // Also use localStorage for cross-tab communication
            localStorage.setItem('folder_updated_trigger', JSON.stringify({
                folderId: updateFolderData.value.id,
                folderName: response.data.name,
                timestamp: Date.now()
            }));

            console.log('📢 Broadcasted folder update event');

            showUpdateFolderDialog.value = false;
            updateFolderData.value = { id: null, title: '', description: '' };
            showSuccess('The change is reflected in the database and for all students.', 'Folder Updated');
        }
    } catch (error) {
        console.error('Error updating folder:', error);
        console.error('Error details:', error.response?.data);

        const errorMsg = error.response?.data?.error || error.message;
        const errorDetail = error.response?.data?.detail || '';

        if (errorDetail) {
            showError(`${errorMsg}\n\n${errorDetail}`, 'Failed to Update Folder');
        } else {
            showError(errorMsg, 'Failed to Update Folder');
        }
    }
};

// Open archive folder dialog
const openArchiveFolderDialog = (folder) => {
    archiveFolderData.value = {
        id: folder.id,
        name: folder.name,
        items: folder.items || 0
    };
    showArchiveFolderDialog.value = true;
    activeFolderMenuIndex.value = null;
    console.log('📦 Archive folder dialog opened for:', folder.name);
};

// Archive folder
const archiveFolder = async () => {
    try {
        console.log('📦 Archiving folder:', archiveFolderData.value);

        // Update folder status to archived in database
        const response = await axios.patch(`/api/portfolio/folders/${archiveFolderData.value.id}/`, {
            is_archived: true
        });

        console.log('✅ Folder archived successfully:', response.data);

        // Remove the folder from the active list
        subjectFolders.value = subjectFolders.value.filter(f => f.id !== archiveFolderData.value.id);

        // If we're currently viewing this folder's activities, go back to folder view
        if (selectedFolderId.value === archiveFolderData.value.id) {
            showingActivities.value = false;
            selectedSubject.value = '';
            selectedFolderId.value = null;
            activities.value = [];
        }

        // Close the dialog
        showArchiveFolderDialog.value = false;
        archiveFolderData.value = { id: null, name: '', items: 0 };

        showSuccess('Subject folder has been archived.', 'Folder Archived');
    } catch (error) {
        console.error('❌ Error archiving folder:', error);
        const errorMsg = error.response?.data?.message || 'Failed to archive folder';
        showError(errorMsg, 'Archive Failed');
    }
};



// Open delete activity dialog
const openDeleteActivityDialog = (activity, index) => {
    deleteActivityData.value = {
        id: activity.id,
        title: activity.title,
        type: activity.type,
        is_published: activity.is_published,
        index: index
    };
    showDeleteActivityDialog.value = true;
};

// Confirm delete activity
const confirmDeleteActivity = async () => {
    try {
        isDeletingActivity.value = true;
        console.log('Deleting activity:', deleteActivityData.value);

        // Delete activity from database
        const response = await axios.delete(`/api/activities/${deleteActivityData.value.id}/`);

        console.log('Activity deleted successfully:', response.data);

        // Remove the activity from the list
        activities.value = activities.value.filter(a => a.id !== deleteActivityData.value.id);

        // Close dialog and reset data
        showDeleteActivityDialog.value = false;
        deleteActivityData.value = { id: null, title: '', type: '', is_published: false, index: null };

        showSuccess('Activity and all related submissions have been permanently deleted.', 'Activity Deleted');
    } catch (error) {
        console.error('Error deleting activity:', error);
        console.error('Error details:', error.response?.data);

        // Get error message from backend
        const errorMsg = error.response?.data?.error || error.response?.data?.detail || error.message;

        showError(errorMsg, 'Failed to Delete Activity');
    } finally {
        isDeletingActivity.value = false;
    }
};

// Close folder menu when clicking outside
const closeFolderMenu = () => {
    activeFolderMenuIndex.value = null;
};

// Function to load portfolio folders
const loadPortfolioFolders = async () => {
    isLoadingFolders.value = true;
    try {
        const selectedClass = JSON.parse(localStorage.getItem('digiportal_selected_class'));
        if (!selectedClass || !selectedClass.id) {
            showError('No class selected. Please go back and select a class.', 'Error');
            isLoadingFolders.value = false;
            return;
        }

        const response = await axios.get(`/api/portfolio/folders/?classroom_id=${selectedClass.id}`);

        console.log('API Response:', response.data); // Debug log

        if (response.data && Array.isArray(response.data)) {
            subjectFolders.value = response.data.map(folder => ({
                id: folder.id,
                name: folder.name,
                items: folder.activities ? folder.activities.length : 0,
                description: folder.description || ''
            }));
        } else {
            console.warn('API did not return an array:', response.data);
            subjectFolders.value = [];
        }
    } catch (error) {
        console.error('Error loading folders:', error);
        showError('Failed to load portfolio folders', 'Error');
        subjectFolders.value = [];
    } finally {
        isLoadingFolders.value = false;
    }
};

// Add a new criterion
const addCriterion = () => {
    savedCriteria.value.push({ name: '', maxScore: 0, isCreated: false, isEditing: false, originalName: '', originalScore: 0 });
};

// Create a criterion (validates and marks as created)
const createCriterion = (index) => {
    const criterion = savedCriteria.value[index];

    // Validate name
    if (!criterion.name || !criterion.name.trim()) {
        showWarning('Criterion name is required', 'Invalid Criterion');
        return;
    }

    // Validate score - must be a number and required
    if (criterion.maxScore === '' || criterion.maxScore === null || criterion.maxScore === undefined || isNaN(criterion.maxScore)) {
        showWarning('Score level is required', 'Invalid Score');
        return;
    }

    if (criterion.maxScore <= 0) {
        showWarning('Score must be greater than 0', 'Invalid Score');
        return;
    }

    // Mark as created
    criterion.isCreated = true;

    console.log('Criterion created:', criterion);
};

// Enable editing for a created criterion
const enableEdit = (index) => {
    const criterion = savedCriteria.value[index];

    // Save original values for cancel
    criterion.originalName = criterion.name;
    criterion.originalScore = criterion.maxScore;

    // Enable editing mode
    criterion.isEditing = true;

    console.log('Criterion edit enabled:', criterion);
};

// Confirm edit changes
const confirmEdit = (index) => {
    const criterion = savedCriteria.value[index];

    // Validate name
    if (!criterion.name || !criterion.name.trim()) {
        showWarning('Criterion name is required', 'Invalid Criterion');
        return;
    }

    // Validate score - must be a number and required
    if (criterion.maxScore === '' || criterion.maxScore === null || criterion.maxScore === undefined || isNaN(criterion.maxScore)) {
        showWarning('Score level is required', 'Invalid Score');
        return;
    }

    if (criterion.maxScore <= 0) {
        showWarning('Score must be greater than 0', 'Invalid Score');
        return;
    }

    // Disable editing mode
    criterion.isEditing = false;

    console.log('Criterion updated:', criterion);
};

// Cancel edit changes
const cancelEdit = (index) => {
    const criterion = savedCriteria.value[index];

    // Restore original values
    criterion.name = criterion.originalName;
    criterion.maxScore = criterion.originalScore;

    // Disable editing mode
    criterion.isEditing = false;

    console.log('Edit cancelled:', criterion);
};

// Remove a new criterion (before it's created)
const removeNewCriterion = (index) => {
    // Prevent removing the last criterion
    if (savedCriteria.value.length === 1) {
        showWarning('You must have at least one criterion', 'Cannot Remove');
        return;
    }
    savedCriteria.value.splice(index, 1);
};

// State for delete confirmation dialog
const showDeleteCriteriaDialog = ref(false);
const criteriaToDelete = ref(null);

// Open delete confirmation dialog
const confirmDeleteCriterion = (index) => {
    criteriaToDelete.value = index;
    showDeleteCriteriaDialog.value = true;
};

// Remove a saved criterion (after it's created)
const removeSavedCriterion = () => {
    if (criteriaToDelete.value !== null) {
        savedCriteria.value.splice(criteriaToDelete.value, 1);
        showDeleteCriteriaDialog.value = false;
        criteriaToDelete.value = null;
        showSuccess('Criterion deleted successfully');
    }
};

// Helper function to get today's date in YYYY-MM-DD format
const getTodayDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
};

// Helper function to get current time in HH:MM format
const getCurrentTime = () => {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
};

// Helper function to check if activity is past due or too close to deadline
const isActivityPastDue = (activity) => {
    if (!activity.due_date) return false;

    // Configuration: Minimum hours before due date/time to allow editing (must match backend)
    const EDIT_CUTOFF_HOURS = 3;

    // Parse due date
    const dueDate = new Date(activity.due_date);

    // Combine date and time
    let dueDatetime;
    if (activity.due_time) {
        const [hours, minutes] = activity.due_time.split(':');
        dueDatetime = new Date(dueDate);
        dueDatetime.setHours(parseInt(hours), parseInt(minutes), 0, 0);
    } else {
        // If no time specified, use end of day
        dueDatetime = new Date(dueDate);
        dueDatetime.setHours(23, 59, 59, 999);
    }

    // Get current time
    const now = new Date();

    // Calculate time remaining in milliseconds
    const timeRemaining = dueDatetime - now;

    // If deadline has passed
    if (timeRemaining <= 0) {
        return true;
    }

    // If less than EDIT_CUTOFF_HOURS remaining
    const cutoffMilliseconds = EDIT_CUTOFF_HOURS * 60 * 60 * 1000;
    if (timeRemaining < cutoffMilliseconds) {
        return true;
    }

    return false;
};

// Helper function to get minimum time for time input (only if date is today)
const getMinTime = () => {
    if (!newActivity.value.dueDate) return '';

    const selectedDate = new Date(newActivity.value.dueDate);
    const today = new Date();
    selectedDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    // If selected date is today, return current time as minimum
    if (selectedDate.getTime() === today.getTime()) {
        return getCurrentTime();
    }

    // If future date, no minimum time restriction
    return '';
};

// Helper function to get minimum time for edit dialog
const getMinTimeForEdit = () => {
    if (!editActivityData.value.dueDate) return '';

    const selectedDate = new Date(editActivityData.value.dueDate);
    const today = new Date();
    selectedDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    // If selected date is today, return current time as minimum
    if (selectedDate.getTime() === today.getTime()) {
        return getCurrentTime();
    }

    // If future date, no minimum time restriction
    return '';
};

// Function to add new activity
const addNewActivity = async () => {
    // Validate Activity Type
    if (!newActivity.value.type) {
        showWarning('Please select an activity type.', 'Activity Type Required');
        return;
    }

    // Validate Activity Title
    if (!newActivity.value.title || !newActivity.value.title.trim()) {
        showWarning('Please enter a title for the activity.', 'Activity Title Required');
        return;
    }

    // Validate Due Date
    if (!newActivity.value.dueDate) {
        showWarning('Please select a due date.', 'Due Date Required');
        return;
    }

    // Validate Due Time
    if (!newActivity.value.dueTime || !newActivity.value.dueTime.trim()) {
        showWarning('Please select a due time.', 'Due Time Required');
        return;
    }

    // Validate Scoring Criteria
    const createdCriteria = savedCriteria.value.filter(c => c.isCreated);
    if (createdCriteria.length === 0) {
        showWarning('Please add and create at least one scoring criterion with points greater than 0.', 'Scoring Criteria Required');
        return;
    }

    try {
        // Get the current folder ID
        const currentFolder = subjectFolders.value.find(f => f.name === selectedSubject.value);
        if (!currentFolder) {
            showWarning('Please select a folder first', 'No Folder Selected');
            return;
        }

        // Validate and format the date properly
        let formattedDueDate = newActivity.value.dueDate;
        if (formattedDueDate) {
            // Ensure date is in YYYY-MM-DD format
            const dateObj = new Date(formattedDueDate);
            if (!isNaN(dateObj.getTime())) {
                formattedDueDate = dateObj.toISOString().split('T')[0];
            }

            // Validate that the date is not in the past
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const selectedDate = new Date(formattedDueDate);
            selectedDate.setHours(0, 0, 0, 0);

            if (selectedDate < today) {
                showWarning('Please select today or a future date.', 'Invalid Due Date');
                return;
            }

            // If the date is today, validate the time is not in the past
            if (selectedDate.getTime() === today.getTime()) {
                const currentTime = getCurrentTime();
                if (newActivity.value.dueTime < currentTime) {
                    showWarning('Please select a future time.', 'Invalid Due Time');
                    return;
                }
            }
        }

        // Map created criteria for submission
        const criteriaForSubmission = createdCriteria.map(c => ({
            name: c.name,
            maxScore: c.maxScore
        }));

        console.log('Creating activity with criteria:', {
            folder_id: currentFolder.id,
            activity_type: newActivity.value.type?.value || newActivity.value.type,
            title: newActivity.value.title,
            description: newActivity.value.description,
            due_date: formattedDueDate,
            due_time: newActivity.value.dueTime || null,
            scoring_criteria: criteriaForSubmission
        });

        // Create FormData to support file uploads
        const formData = new FormData();
        formData.append('activity_type', newActivity.value.type?.value || newActivity.value.type);
        formData.append('title', newActivity.value.title);
        formData.append('description', newActivity.value.description || '');
        formData.append('due_date', formattedDueDate);
        formData.append('due_time', newActivity.value.dueTime || '');
        formData.append('scoring_criteria', JSON.stringify(criteriaForSubmission));

        // Add instruction files if any
        if (newActivity.value.instructionFiles && newActivity.value.instructionFiles.length > 0) {
            for (const fileObj of newActivity.value.instructionFiles) {
                formData.append('instruction_files', fileObj.file);
            }
            console.log(`Adding ${newActivity.value.instructionFiles.length} instruction files`);
        }

        // Save to database via API
        const response = await axios.post(`/api/portfolio/folders/${currentFolder.id}/activities/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        if (response.data) {
            console.log('Activity created successfully:', response.data);

            // Update the items count
            currentFolder.items += 1;

            // Reload activities from database to ensure sync
            await loadActivities(currentFolder.id);

            showAddActivityDialog.value = false;
            newActivity.value = {
                type: null,
                title: '',
                description: '',
                dueDate: '',
                dueTime: '',
                instructionFiles: [],
                scoringCriteria: [
                    { name: '', maxScore: 10 }
                ]
            };
            savedCriteria.value = [
                { name: '', maxScore: 0, isCreated: false, isEditing: false, originalName: '', originalScore: 0 }
            ];

            showSuccess('Activity added successfully!', 'Activity Created');
        }
    } catch (error) {
        console.error('Error creating activity:', error);
        showError(error.response?.data?.message || error.message, 'Failed to Create Activity');
    }
};

// Get selected class from localStorage
const selectedClass = ref(null);
const className = ref('Grade 1 - A'); // Default class name
const currentUser = ref({
    name: 'Teacher Name',
    email: 'teacher@example.com',
    role: 'teacher'
});

// Computed property for actual classroom name (similar to student view)
const actualClassName = computed(() => {
    // Priority: selectedClass > className default
    if (selectedClass.value && selectedClass.value.name) {
        return selectedClass.value.name;
    }
    return className.value;
});

// Function to handle class change event
const handleClassChange = async (event) => {
    console.log('🔄 Class changed in Room, reloading data...', event.detail);

    // Extract class from event detail (can be event.detail.classItem or event.detail directly)
    const classData = event.detail.classItem || event.detail;

    // Update selected class in localStorage (already done by MainLayout, but ensure it's set)
    localStorage.setItem('digiportal_selected_class', JSON.stringify(classData));

    // Update local state
    selectedClass.value = classData;
    className.value = classData.name;

    // Clear current view state - go back to folders view
    showingActivities.value = false;
    selectedSubject.value = '';
    selectedFolderId.value = null;
    activities.value = [];
    selectedActivity.value = null;

    // Clear saved view state - this ensures clicking a class always shows folders
    localStorage.removeItem('teacher_current_view');

    console.log('📂 Clearing activities view, returning to folders');

    // Reload folders for the new class
    await loadPortfolioFolders();

    // Check if we need to navigate to a specific tab (from notification)
    const navigateToTab = localStorage.getItem('teacher_navigate_to_tab');
    if (navigateToTab) {
        console.log('📂 Navigating to tab from notification:', navigateToTab);
        if (navigateToTab === 'compilation') {
            activeTab.value = 'portfolio';
            // Refresh portfolio compilation status
            await checkPortfolioCompilationStatus();
            // Load portfolio students
            await fetchPortfolioEnvelopes();
        }
        localStorage.removeItem('teacher_navigate_to_tab');
    }

    console.log('✅ Folders reloaded for class:', classData.name);
};

// Load selected class on mount
onMounted(() => {
    const savedClass = localStorage.getItem('digiportal_selected_class');
    if (savedClass) {
        selectedClass.value = JSON.parse(savedClass);
        className.value = selectedClass.value.name;
    }

    // Listen for class change events
    window.addEventListener('classChanged', handleClassChange);
});

const props = defineProps({
    theme: {
        type: String,
        default: 'neutral'
    }
});

// Check if returning from Outputs/Sprogress to set initial state
const isReturningFromOutputs = () => {
    const returnContext = localStorage.getItem('return_to_activities');
    if (returnContext) {
        try {
            const context = JSON.parse(returnContext);
            const isRecent = context.timestamp && (Date.now() - context.timestamp < 5000);
            return isRecent && context.showActivities;
        } catch (error) {
            console.error('Error checking return context:', error);
        }
    }
    return false;
};

// Get saved tab from localStorage or use default
const getSavedTab = () => {
    const savedTab = localStorage.getItem('teacher_room_active_tab');
    if (savedTab && ['classroom', 'pupil', 'portfolio'].includes(savedTab)) {
        return savedTab;
    }
    return isReturningFromOutputs() ? 'pupil' : 'classroom';
};

const activeTab = ref(getSavedTab());

// Watch for tab changes and save to localStorage
watch(activeTab, (newTab) => {
    localStorage.setItem('teacher_room_active_tab', newTab);
});

// Tab configurations
const tabs = [
    { id: 'classroom', name: "Student's Classroom", icon: 'pi-building' },
    { id: 'pupil', name: "Student's Activities", icon: 'pi-users' },
    { id: 'portfolio', name: "Student's Portfolio Compilation", icon: 'pi-folder' }
];

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

// Settings Dropdown State
const showSettingsDropdown = ref(false);
const showArchiveDialog = ref(false);
const showPortfolioCompilationDialog = ref(false);
const showDropCompilationDialog = ref(false);
const showNotStartedStudentsDialog = ref(false);
const portfolioCompilationActive = ref(false); // Track if compilation is already requested

// Portfolio students data
const portfolioStudents = ref([]);
const showEnvelopeViewDialog = ref(false);
const selectedEnvelope = ref(null);
const isEnvelopeOpen = ref(false);
const studentActivities = ref([]); // Store student's submitted activities
const currentActivityIndex = ref(0); // Current activity index for carousel
const currentPortfolioFileIndex = ref(0); // For navigating multiple files in portfolio
const activePortfolioTab = ref('scored'); // 'scored' or 'missing'

// Computed property for students who haven't started portfolio compilation
const notStartedStudents = computed(() => {
    // Get IDs of students who have started (in portfolioStudents)
    const startedStudentIds = new Set(portfolioStudents.value.map(s => s.student_id));
    
    // Filter classroom students who haven't started
    return classroomStudents.value.filter(student => !startedStudentIds.has(student.id));
});

// Computed properties for filtered activities
const scoredActivities = computed(() => {
    return studentActivities.value.filter(activity =>
        activity.submission_status === 'scored' ||
        activity.submission_status === 'scored_late' ||
        activity.submission_status === 'scored_resubmitted' ||
        activity.submission_status === 'compiled'  // Include compiled activities
    );
});

const missingCompiledActivities = computed(() => {
    return studentActivities.value.filter(activity =>
        activity.submission_status === 'submitted_compilation' ||
        activity.submission_status === 'compiled'  // Include compiled activities
    );
});

const currentTabActivities = computed(() => {
    return activePortfolioTab.value === 'scored' ? scoredActivities.value : missingCompiledActivities.value;
});

const isSidebarCollapsed = inject('isSidebarCollapsed', ref(false));
const activeMenuIndex = ref(null);
const menuButtonRefs = ref({});
const menuPosition = ref({ x: 0, y: 0 });
const settingsRef = ref(null);

// Watch for portfolio tab changes
watch(activePortfolioTab, () => {
    currentActivityIndex.value = 0; // Reset to first activity when switching tabs
});

// Watch for sidebar state changes
watch(isSidebarCollapsed, (newValue) => {
    // This will trigger a re-render when the sidebar state changes
    // console.log('Sidebar collapsed state changed to:', newValue);
});

// Watch for active tab changes to manage folder selection
watch(activeTab, (newTab) => {
    if (newTab === 'portfolio') {
        // Save current folder selection before clearing (when switching to portfolio tab)
        lastSelectedSubject.value = selectedSubject.value;
        lastSelectedFolderId.value = selectedFolderId.value;

        // Clear folder selection when switching to Portfolio Compilation tab
        selectedSubject.value = '';
        selectedFolderId.value = null;
        showingActivities.value = false;

        // Dispatch event to clear sidebar folder active state
        window.dispatchEvent(new CustomEvent('folderSelected', {
            detail: {
                subject: null,
                classItem: selectedClass.value
            }
        }));
        console.log('📂 Cleared folder selection when switching to portfolio tab');
    } else if (newTab === 'pupil') {
        // Returning to Student's Activities tab
        if (lastSelectedSubject.value && lastSelectedFolderId.value) {
            // Restore from portfolio tab
            selectedSubject.value = lastSelectedSubject.value;
            selectedFolderId.value = lastSelectedFolderId.value;
            showingActivities.value = true;

            // Dispatch event to restore sidebar folder active state
            window.dispatchEvent(new CustomEvent('folderSelected', {
                detail: {
                    subject: lastSelectedSubject.value,
                    classItem: selectedClass.value
                }
            }));
            console.log('📂 Restored folder selection when returning from portfolio tab');
        } else if (activitiesTabSelectedSubject.value && activitiesTabSelectedFolderId.value) {
            // Restore from classroom tab
            selectedSubject.value = activitiesTabSelectedSubject.value;
            selectedFolderId.value = activitiesTabSelectedFolderId.value;
            showingActivities.value = true;

            // Dispatch event to restore sidebar folder active state
            window.dispatchEvent(new CustomEvent('folderSelected', {
                detail: {
                    subject: activitiesTabSelectedSubject.value,
                    classItem: selectedClass.value
                }
            }));
            console.log('📂 Restored Activities tab folder selection when returning from Classroom');
        }
    } else if (newTab === 'classroom') {
        // Switching to Student's Classroom tab - save Activities folder selection
        activitiesTabSelectedSubject.value = selectedSubject.value;
        activitiesTabSelectedFolderId.value = selectedFolderId.value;

        // Clear folder selection when switching to Classroom tab
        selectedSubject.value = '';
        selectedFolderId.value = null;
        showingActivities.value = false;

        // Dispatch event to clear sidebar folder active state
        window.dispatchEvent(new CustomEvent('folderSelected', {
            detail: {
                subject: null,
                classItem: selectedClass.value
            }
        }));
        console.log('📂 Cleared folder selection when switching to Classroom tab');
    }
});

// Toggle activity action menu
const toggleActivityMenu = (event, activity, index) => {
    event.stopPropagation();

    if (activeMenuIndex.value === index) {
        activeMenuIndex.value = null;
    } else {
        activeMenuIndex.value = index;
    }
};

// Close the currently active menu
const closeMenu = () => {
    activeMenuIndex.value = null;
};

// Close menu when scrolling
onMounted(() => {
    window.addEventListener('scroll', closeMenu, true);
});

onUnmounted(() => {
    window.removeEventListener('scroll', closeMenu, true);
});

// Toggle settings dropdown
const toggleSettingsDropdown = () => {
    showSettingsDropdown.value = !showSettingsDropdown.value;
};

// Close settings dropdown when clicking outside (robust)
const handleDocumentClick = (event) => {
    const root = settingsRef.value;
    if (!root) return;
    if (!root.contains(event.target)) {
        showSettingsDropdown.value = false;
    }
};

// Close menu when clicking outside
const handleClickOutside = (event) => {
    if (activeMenuIndex.value !== null) {
        closeMenu();
    }
};

// Helper to get CSRF token
const getCsrfToken = () => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
};

// Function to authenticate with backend
const authenticateWithBackend = async () => {
    try {
        // First check if already authenticated
        const checkResponse = await axios.get('/api/validate-session/');
        if (checkResponse.data.authenticated) {
            console.log('Already authenticated:', checkResponse.data.user);
            
            // Load user data
            const user = checkResponse.data.user;
            currentUser.value = {
                name: user.full_name || user.username || 'Teacher Name',
                email: user.email || 'teacher@example.com',
                role: user.role || 'teacher',
                profile_picture: user.profile_picture || null
            };
            
            // Check if role is teacher - if not, logout and re-authenticate as teacher
            if (checkResponse.data.user?.role !== 'teacher') {
                console.warn('⚠️ User is authenticated as', checkResponse.data.user?.role, '- need to switch to teacher');
                try {
                    // Logout first
                    await axios.post('/logout/');
                    console.log('Logged out from', checkResponse.data.user?.role);

                    // Refresh CSRF token after logout
                    const csrfToken = getCsrfToken();
                    if (csrfToken) {
                        axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
                    }

                    // Then login as teacher
                    const authResponse = await axios.post('/api/validate-session/', {
                        role: 'teacher'
                    });
                    console.log('✅ Re-authenticated as teacher:', authResponse.data.user);
                    
                    // Update currentUser with new data
                    const newUser = authResponse.data.user;
                    currentUser.value = {
                        name: newUser.full_name || newUser.username || 'Teacher Name',
                        email: newUser.email || 'teacher@example.com',
                        role: newUser.role || 'teacher',
                        profile_picture: newUser.profile_picture || null
                    };
                    
                    return true;
                } catch (switchError) {
                    console.error('❌ Failed to switch to teacher role:', switchError);
                    console.error('Error details:', switchError.response?.data);
                    // Try direct auth without logout
                    try {
                        const authResponse = await axios.post('/api/validate-session/', {
                            role: 'teacher'
                        });
                        console.log('✅ Authenticated as teacher (direct):', authResponse.data.user);
                        
                        // Update currentUser with new data
                        const newUser = authResponse.data.user;
                        currentUser.value = {
                            name: newUser.full_name || newUser.username || 'Teacher Name',
                            email: newUser.email || 'teacher@example.com',
                            role: newUser.role || 'teacher',
                            profile_picture: newUser.profile_picture || null
                        };
                        
                        return true;
                    } catch (directError) {
                        console.error('❌ Direct auth also failed:', directError);
                        console.error('Direct error details:', directError.response?.data);
                        return false;
                    }
                }
            }
            return true;
        }
    } catch (error) {
        // Not authenticated, try to create session
        try {
            const authResponse = await axios.post('/api/validate-session/', {
                role: 'teacher'
            });
            console.log('Authentication successful:', authResponse.data.user);
            
            // Load user data
            const user = authResponse.data.user;
            currentUser.value = {
                name: user.full_name || user.username || 'Teacher Name',
                email: user.email || 'teacher@example.com',
                role: user.role || 'teacher',
                profile_picture: user.profile_picture || null
            };
            
            return true;
        } catch (authError) {
            console.error('Authentication failed:', authError);
            console.error('Auth error details:', authError.response?.data);
            return false;
        }
    }
};

// Check if portfolio compilation is already active for this class
const checkPortfolioCompilationStatus = async () => {
    try {
        const classroomId = selectedClass.value?.id;

        if (!classroomId) {
            console.log('No class selected, skipping portfolio compilation check');
            return;
        }

        const response = await axios.get(`/api/notifications/portfolio-compilation/${classroomId}/`);

        if (response.data && response.data.compilation_requested) {
            portfolioCompilationActive.value = true;
            console.log('✅ Portfolio compilation is active for this class');

            // Fetch portfolio envelopes if compilation is active
            await fetchPortfolioEnvelopes();
        } else {
            portfolioCompilationActive.value = false;
        }
    } catch (error) {
        console.error('❌ Error checking portfolio compilation status:', error);
        showError('Failed to check portfolio compilation status', 'Error');
        portfolioCompilationActive.value = false;
    }
};

// Check for activities approaching edit deadline
const checkEditDeadlines = async () => {
    try {
        console.log('🔔 Checking for activities approaching edit deadline...');
        const response = await axios.get('/api/notifications/check-edit-deadlines/');

        if (response.data && response.data.warnings_sent > 0) {
            console.log(`✅ ${response.data.warnings_sent} edit deadline warning(s) sent:`, response.data.activities_warned);
        } else {
            console.log('✅ No activities approaching edit deadline');
        }
    } catch (error) {
        console.error('❌ Error checking edit deadlines:', error);
        showError('Failed to check edit deadlines', 'Error');
    }
};

// View student envelope
const viewStudentEnvelope = async (student) => {
    selectedEnvelope.value = student;
    isEnvelopeOpen.value = false; // Show closed envelope first
    currentActivityIndex.value = 0; // Reset to first activity
    activePortfolioTab.value = 'scored'; // Reset to scored tab
    console.log('Viewing envelope for:', student.name);

    // Fetch student activities immediately
    await fetchStudentActivities(student.student_id);
};

// Open envelope and show activities
const openEnvelope = () => {
    isEnvelopeOpen.value = true;
    currentActivityIndex.value = 0;
    console.log('Opening envelope, showing activities');
};

// Navigate activities
const nextActivity = () => {
    const maxIndex = activePortfolioTab.value === 'scored'
        ? scoredActivities.value.length - 1
        : missingCompiledActivities.value.length - 1;

    if (currentActivityIndex.value < maxIndex) {
        currentActivityIndex.value++;
    }
};

const previousActivity = () => {
    if (currentActivityIndex.value > 0) {
        currentActivityIndex.value--;
    }
};

// Fetch student's submitted activities
const fetchStudentActivities = async (studentId) => {
    try {
        const classNameValue = props.className || className.value;

        if (!classNameValue || !studentId) {
            return;
        }

        console.log(`📚 Fetching activities for student ID: ${studentId}`);

        // Fetch activities for specific student (teacher view)
        const response = await axios.get(`/api/portfolio-envelope/teacher-activities/${encodeURIComponent(classNameValue)}/${studentId}/`);

        if (response.data) {
            // Use submitted_activities to show only submitted work
            studentActivities.value = response.data.submitted_activities || [];
            console.log(`✅ Loaded ${studentActivities.value.length} submitted activities for student (${response.data.total_count} total)`);
        }
    } catch (error) {
        console.error('❌ Error fetching student activities:', error);
        showError('Failed to load student activities', 'Error');
        studentActivities.value = [];
    }
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

// Helper function to check if file is an image
const isImageFile = (filename) => {
    if (!filename) return false;
    const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg'];
    const extension = filename.split('.').pop().toLowerCase();
    return imageExtensions.includes(extension);
};

// Helper function to check if file object is an image (for portfolio)
const isImageFileTeacher = (file) => {
  if (!file) return false;
  // Check type property
  if (file.type === 'image') return true;
  // Check path for base64 image
  const path = file.path || file.file_url || '';
  if (path.startsWith('data:image')) return true;
  // Check file extension
  if (path.match(/\.(jpeg|jpg|gif|png|webp|bmp|svg)$/i)) return true;
  return false;
};

// Helper function to check if URL is an image (for portfolio)
const isImageUrlTeacher = (url) => {
  if (!url) return false;
  if (url.startsWith('data:image')) return true;
  if (url.match(/\.(jpeg|jpg|gif|png|webp|bmp|svg)$/i)) return true;
  return false;
};

// Helper function to get file URL (for portfolio)
const getFileUrlTeacher = (file) => {
  if (!file) return '';
  return file.path || file.file_url || '';
};

// Helper function to open file in new tab (handles base64 data URLs)
const openFileInNewTabTeacher = (fileUrl) => {
  if (!fileUrl) return;
  
  // For base64 data URLs, create a blob and open it
  if (fileUrl.startsWith('data:')) {
    try {
      // Convert base64 to blob
      const byteString = atob(fileUrl.split(',')[1]);
      const mimeString = fileUrl.split(',')[0].split(':')[1].split(';')[0];
      const ab = new ArrayBuffer(byteString.length);
      const ia = new Uint8Array(ab);
      for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
      }
      const blob = new Blob([ab], { type: mimeString });
      const blobUrl = URL.createObjectURL(blob);
      window.open(blobUrl, '_blank');
    } catch (error) {
      console.error('Error opening base64 file:', error);
      // Fallback: try to open directly
      window.open(fileUrl, '_blank');
    }
  } else {
    // Regular URL, open directly
    window.open(fileUrl, '_blank');
  }
};

// Helper function to get status label for portfolio activities (Teacher view)
const getStatusLabelTeacher = (activity) => {
  if (!activity) return 'N/A';
  
  const status = activity.submission_status;
  const isCompilation = activity.is_compilation;
  const resubmitCount = activity.resubmit_count || 0;
  
  // If it's a compilation submission (from missing activity)
  if (isCompilation || status === 'compiled') {
    return 'Compiled';
  }
  
  // If it's a resubmission
  if (status === 'scored_resubmitted' || resubmitCount > 0) {
    return `Resubmitted (${resubmitCount}x)`;
  }
  
  // If submitted late
  if (status === 'scored_late' || activity.is_late) {
    return 'Submitted Late';
  }
  
  // Regular scored submission
  if (status === 'scored') {
    return 'Submitted';
  }
  
  return status?.replace(/_/g, ' ') || 'N/A';
};

// Helper function to get score display for portfolio activities (Teacher view)
const getScoreDisplayTeacher = (activity) => {
  if (!activity) return 'None';
  
  // If it's a compilation submission, don't show score
  if (activity.is_compilation || activity.submission_status === 'compiled') {
    return 'None';
  }
  
  // If no score yet
  if (activity.submission_score === null || activity.submission_score === undefined) {
    return 'None';
  }
  
  // Show score with max score if available
  const score = activity.submission_score;
  const maxScore = activity.max_score;
  
  if (maxScore) {
    return `${score}/${maxScore}`;
  }
  
  return `${score}`;
};

// Fetch portfolio envelopes for the class
const fetchPortfolioEnvelopes = async () => {
    try {
        const classNameValue = props.className || className.value;

        if (!classNameValue) {
            return;
        }

        console.log('📋 Fetching portfolio envelopes for:', classNameValue);

        const response = await axios.get(`/api/portfolio-envelope/${encodeURIComponent(classNameValue)}/`);

        if (response.data && response.data.envelopes) {
            portfolioStudents.value = response.data.envelopes.map(env => ({
                id: env.id,
                student_id: env.student_id, // Add student_id for fetching activities
                name: env.student_name || env.name,
                idNumber: env.id_number,
                profile_picture: env.profile_picture || null,
                dateCreated: env.date_created,
                timeCreated: env.time_created,
                // Store full envelope data for viewing
                title: env.title,
                color: env.color,
                pattern: env.pattern,
                className: env.class_name || props.className || className.value,
                isSubmitted: env.is_submitted,
                status: env.status || (env.is_submitted ? 'Done' : 'In Progress'),
                submittedAt: env.submitted_at,
                compiled_count: env.compiled_count || 0,
                total_activities: env.total_activities || 0
            }));

            console.log(`✅ Loaded ${portfolioStudents.value.length} portfolio envelopes`);
        }
    } catch (error) {
        console.error('❌ Error fetching portfolio envelopes:', error);
        showError('Failed to load portfolio envelopes', 'Error');
        portfolioStudents.value = [];
    }
};

// Load classroom students
const loadClassroomStudents = async () => {
    try {
        const response = await axios.get('/api/classrooms/');
        if (response.data && response.data.classrooms && response.data.classrooms.length > 0) {
            // Get the first classroom (current class)
            const currentClassroom = response.data.classrooms[0];
            classroomStudents.value = currentClassroom.students || [];
            console.log('✅ Loaded classroom students:', classroomStudents.value.length);
            console.log('📊 Classroom data:', currentClassroom);
        } else {
            console.warn('⚠️ No classroom data found');
            classroomStudents.value = [];
        }
    } catch (error) {
        console.error('❌ Error loading classroom students:', error);
        classroomStudents.value = [];
    }
};

onMounted(async () => {
    document.addEventListener('click', handleDocumentClick, true);
    document.addEventListener('click', handleClickOutside);
    document.addEventListener('click', closeFolderMenu);

    // Check if we're coming from a notification that needs to navigate to a specific tab
    // Do this BEFORE loading folders to ensure class is set correctly
    const navigateToTab = localStorage.getItem('teacher_navigate_to_tab');
    if (navigateToTab === 'compilation') {
        console.log('📂 Coming from notification, will navigate to compilation tab');
        // Ensure the class is loaded from localStorage first
        const savedClass = localStorage.getItem('digiportal_selected_class');
        if (savedClass) {
            const classData = JSON.parse(savedClass);
            selectedClass.value = classData;
            className.value = classData.name;
            console.log('✅ Class loaded from notification context:', classData.name);
        }
    }

    // Authenticate with backend first, then load folders
    const authenticated = await authenticateWithBackend();
    if (authenticated) {
        await loadPortfolioFolders();
        await loadClassroomStudents();

        // Check portfolio compilation status
        await checkPortfolioCompilationStatus();

        // Check for activities approaching edit deadline
        await checkEditDeadlines();

        // Check if returning from Outputs/Sprogress page to show activities list
        const returnContext = localStorage.getItem('return_to_activities');
        if (returnContext) {
            try {
                const context = JSON.parse(returnContext);
                console.log('Return context:', context);

                // Check if timestamp exists and is within 5 seconds (to prevent showing on refresh)
                const isRecent = context.timestamp && (Date.now() - context.timestamp < 5000);

                if (!isRecent) {
                    console.log('⏰ Return context expired, clearing...');
                    localStorage.removeItem('return_to_activities');
                } else {
                    console.log('Available folders:', subjectFolders.value);

                    if (context.showActivities && context.subject) {
                        // Find the folder for this subject
                        // First try exact match by folder name (for Outputs.vue)
                        let folder = subjectFolders.value.find(f => f.name === context.subject);

                        // If not found, try matching by class_name (for Sprogress.vue)
                        if (!folder) {
                            folder = subjectFolders.value.find(f => f.class_name === context.subject);
                        }

                        // If still not found, just use the first folder for this class
                        if (!folder && subjectFolders.value.length > 0) {
                            console.log('⚠️ No exact match, using first folder');
                            folder = subjectFolders.value[0];
                        }

                        console.log('✅ Found folder:', folder);

                        if (folder) {
                            console.log('🎯 Showing activities for folder:', folder.name, 'ID:', folder.id);
                            // Use folder.name (not context.subject) as the first parameter
                            await showSubjectActivities(folder.name, folder.id);
                        } else {
                            console.error('❌ Folder not found for subject:', context.subject);
                            console.log('🔎 Tried matching:', context.subject);
                            console.log('📋 Against folders:', subjectFolders.value.map(f => ({ name: f.name, class_name: f.class_name })));
                        }
                    }
                    localStorage.removeItem('return_to_activities');
                }
            } catch (error) {
                console.error('Error restoring activities view:', error);
                localStorage.removeItem('return_to_activities');
            }
        }

        // Check for regular view state restoration (for page refresh)
        const savedView = localStorage.getItem('teacher_current_view');
        if (savedView && !returnContext) {
            try {
                const viewState = JSON.parse(savedView);
                console.log('🔄 Restoring teacher view state:', viewState);

                if (viewState.showingActivities && viewState.selectedFolderId) {
                    // Find the folder by ID
                    const folder = subjectFolders.value.find(f => f.id === viewState.selectedFolderId);

                    if (folder) {
                        console.log('✅ Restoring activities view for folder:', folder.name);
                        // Restore the activities view
                        selectedSubject.value = viewState.selectedSubject;
                        selectedFolderId.value = viewState.selectedFolderId;
                        showingActivities.value = true;

                        // Load activities
                        await loadActivities(viewState.selectedFolderId);
                        console.log('✅ Activities view restored');
                    } else {
                        console.warn('⚠️ Folder not found, clearing view state');
                        localStorage.removeItem('teacher_current_view');
                    }
                }
            } catch (error) {
                console.error('❌ Error restoring teacher view state:', error);
                localStorage.removeItem('teacher_current_view');
            }
        }

        // Check if we need to navigate to a specific tab (from notification)
        const navigateToTab = localStorage.getItem('teacher_navigate_to_tab');
        if (navigateToTab) {
            console.log('📂 Navigating to tab from notification:', navigateToTab);
            if (navigateToTab === 'compilation') {
                activeTab.value = 'portfolio';
                // Refresh portfolio compilation status
                await checkPortfolioCompilationStatus();
                // Load portfolio students
                await fetchPortfolioEnvelopes();
            }
            localStorage.removeItem('teacher_navigate_to_tab');
        }
    } else {
        console.error('Failed to authenticate with backend');
    }

    // Listen for folder created events (same tab)
    window.addEventListener('folderCreated', async (event) => {
        console.log('📢 Received folderCreated event in teacher view:', event.detail);
    });

    // Listen for folder deleted events (same tab)
    window.addEventListener('folderDeleted', async (event) => {
        console.log('📢 Received folderDeleted event in teacher view:', event.detail);
    });

    // Listen for folder updated events (same tab)
    window.addEventListener('folderUpdated', async (event) => {
        console.log('📢 Received folderUpdated event in teacher view:', event.detail);
    });

    // Listen for storage events (cross-tab communication)
    window.addEventListener('storage', async (event) => {
        if (event.key === 'folder_created_trigger') {
            console.log('📢 Folder created in another tab/window (teacher view)');
            if (!showingActivities.value) {
                await loadPortfolioFolders();
            }
            // Clear the trigger
            localStorage.removeItem('folder_created_trigger');
        } else if (event.key === 'folder_deleted_trigger') {
            console.log('📢 Folder deleted in another tab/window (teacher view)');
            if (!showingActivities.value) {
                await loadPortfolioFolders();
            }
            // Clear the trigger
            localStorage.removeItem('folder_deleted_trigger');
        } else if (event.key === 'folder_updated_trigger') {
            console.log('📢 Folder updated in another tab/window (teacher view)');
            if (!showingActivities.value) {
                await loadPortfolioFolders();
            }
            // Clear the trigger
            localStorage.removeItem('folder_updated_trigger');
        }
    });

    // Watch for class changes to update AI grade level lock status
    watch(className, (newClassName) => {
        if (showAIGenerationDialog.value) {
            setGradeLevelFromClass();
        }
    });

    // Listen for subject change events from sidebar
    window.addEventListener('subjectChanged', handleSubjectChange);

    // Listen for class change events
    window.addEventListener('classChanged', handleClassChange);
});

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
    document.removeEventListener('click', closeFolderMenu);
    if (toastTimeout) clearTimeout(toastTimeout);
});

onUnmounted(() => {
    document.removeEventListener('click', handleDocumentClick, true);
    window.removeEventListener('classChanged', handleClassChange);
    window.removeEventListener('subjectChanged', handleSubjectChange);
});

const handleSubjectChange = async (event) => {
    const { classItem, subject } = event.detail;

    // Guard against undefined classItem
    if (!classItem) {
        console.error('❌ Error: classItem is undefined in subjectChanged event.');
        return;
    }

    console.log('📂 Subject clicked from sidebar:', subject, 'in class:', classItem.name);

    try {
        // Wait for folders to load if they're not loaded yet
        if (!subjectFolders.value || subjectFolders.value.length === 0) {
            console.log('⏳ Folders not loaded yet, loading now...');
            await loadPortfolioFolders();
        }

        console.log('📋 Available folders:', subjectFolders.value.map(f => ({ name: f.name, id: f.id })));

        // Find the folder ID for this subject - try exact match first, then case-insensitive
        let folder = subjectFolders.value.find(f => f.name === subject);

        if (!folder) {
            // Try case-insensitive match
            folder = subjectFolders.value.find(f => f.name.toLowerCase() === subject.toLowerCase());
        }

        if (!folder) {
            // Try partial match (in case folder name has extra text)
            folder = subjectFolders.value.find(f => f.name.includes(subject) || subject.includes(f.name));
        }

        if (folder) {
            console.log('✅ Found folder:', folder.name, 'with ID:', folder.id);
            // Show activities for this subject
            await showSubjectActivities(subject, folder.id);
        } else {
            console.log('❌ Folder not found for subject:', subject);
            console.log('📌 Creating new folder for subject:', subject);

            // Create the folder if it doesn't exist
            try {
                const response = await axios.post('/api/portfolio/folders/', {
                    name: subject,
                    description: `Activities for ${subject}`,
                    classroom: selectedClass.id
                });

                console.log('✅ Created new folder:', response.data);

                // Reload folders and show activities
                await loadPortfolioFolders();
                const newFolder = subjectFolders.value.find(f => f.name === subject);

                if (newFolder) {
                    await showSubjectActivities(subject, newFolder.id);
                }
            } catch (error) {
                console.error('❌ Error creating folder:', error);
                // If folder creation fails, just show empty activities view
                await showSubjectActivities(subject, null);
            }
        }
    } catch (error) {
        console.error('❌ Error in handleSubjectChange:', error);
    }
};

// Subject activities state
const showingActivities = ref(isReturningFromOutputs());
const selectedSubject = ref('');
const selectedFolderId = ref(null);
const activities = ref([]);
const isLoadingActivities = ref(false);
const itemsPerPage = 5;
const displayedDraftCount = ref(itemsPerPage);
const displayedPublishedCount = ref(itemsPerPage);

// Store last selected folder to restore when returning from Portfolio tab
const lastSelectedSubject = ref('');
const lastSelectedFolderId = ref(null);

// Store Activities tab folder selection separately to persist when switching to Classroom
const activitiesTabSelectedSubject = ref('');
const activitiesTabSelectedFolderId = ref(null);

// Computed properties to separate draft and published activities
const draftActivities = computed(() => {
    return activities.value.filter(activity => !activity.is_published);
});

const publishedActivities = computed(() => {
    return activities.value.filter(activity => activity.is_published);
});

// Function to go back to folders view
const backToFolders = () => {
    showingActivities.value = false;
    selectedSubject.value = '';
    selectedFolderId.value = null;
    activities.value = [];

    // Dispatch event to clear sidebar folder active state
    window.dispatchEvent(new CustomEvent('folderSelected', {
        detail: {
            subject: null,
            classItem: selectedClass.value
        }
    }));
    console.log('📂 Cleared folder selection when clicking Back to Folders');

    // Clear saved view state
    localStorage.removeItem('teacher_current_view');
    console.log('🗑️ Cleared teacher view state');
};

// Function to show activities for a subject
const showSubjectActivities = async (subjectName, folderId) => {
    selectedSubject.value = subjectName;
    selectedFolderId.value = folderId;
    showingActivities.value = true;

    // Automatically switch to the Student's Activities tab
    activeTab.value = 'pupil';

    // Save view state to localStorage
    localStorage.setItem('teacher_current_view', JSON.stringify({
        showingActivities: true,
        selectedSubject: subjectName, // Use the correct variable
        selectedFolderId: folderId
    }));
    console.log('💾 Saved teacher view state: Activities for', subjectName);

    // Dispatch event to update MainLayout sidebar active state
    window.dispatchEvent(new CustomEvent('folderSelected', {
        detail: {
            subject: subjectName,
            classItem: selectedClass.value
        }
    }));
    console.log('📂 Dispatched folderSelected event for sidebar sync');

    // Load activities from database
    await loadActivities(folderId);
};

// Function to load activities from database
const loadActivities = async (folderId) => {
    isLoadingActivities.value = true;
    try {
        const response = await axios.get(`/api/portfolio/folders/${folderId}/activities/`);
        console.log('🔥 API Response for activities:', response.data);

        if (response.data) {
            // Format activities for display
            activities.value = response.data.map(activity => {
                console.log('🔍 Processing activity:', activity.title);
                console.log('📊 Raw scoring_criteria from API:', activity.scoring_criteria);
                console.log('📊 Type:', typeof activity.scoring_criteria);
                console.log('📊 Is Array:', Array.isArray(activity.scoring_criteria));

                // Parse scoring criteria if it exists
                let scoringCriteria = [];
                if (activity.scoring_criteria) {
                    try {
                        scoringCriteria = typeof activity.scoring_criteria === 'string'
                            ? JSON.parse(activity.scoring_criteria)
                            : activity.scoring_criteria;
                        console.log('✅ Parsed scoring criteria:', scoringCriteria);
                    } catch (error) {
                        console.error('❌ Error parsing scoring criteria:', error);
                    }
                } else {
                    console.log('⚠️ No scoring criteria found for activity:', activity.title);
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

                console.log(`📌 Activity "${activity.title}" - is_published:`, activity.is_published, 'published_at:', activity.published_at);

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
                    archived: false,
                    scoringCriteria: scoringCriteria,  // Use camelCase for consistency
                    is_published: activity.is_published || false,  // Include publish status
                    published_at: activity.published_at || null,    // Include publish timestamp
                    instruction_files: activity.instruction_files || []  // Include instruction files
                };
            });
            console.log('✅ Final loaded activities:', activities.value);
        }
    } catch (error) {
        console.error('Error loading activities:', error);
        showError('Failed to load activities', 'Error');
        activities.value = [];
    } finally {
        isLoadingActivities.value = false;
    }
};

// Handle edit activity
const editActivity = (activity, index) => {
    closeMenu();

    // Teachers can edit activities at any time (removed past due restriction)

    console.log('📝 Editing activity:', activity);
    console.log('📊 Activity scoring criteria:', activity.scoringCriteria);
    console.log('📎 Activity instruction files:', activity.instruction_files);

    // Find the activity type object that matches the current activity's type
    const activityType = activityTypes.value.find(type => type.value === activity.type) || null;

    // Load existing instruction files from the activity
    const existingFiles = (activity.instruction_files || []).map(f => ({
        id: f.id,
        name: f.file_name,
        type: f.file_type,
        size: f.file_size,
        url: f.file_url,
        isExisting: true  // Mark as existing file from server
    }));

    editActivityData.value = {
        id: activity.id,
        title: activity.title,
        type: activityType,
        description: activity.description,
        dueDate: activity.due_date,
        dueTime: activity.due_time || '',
        instructionFiles: existingFiles,
        deleteInstructionFileIds: []  // Track files to delete
    };

    // Load scoring criteria if exists
    if (activity.scoringCriteria && activity.scoringCriteria.length > 0) {
        editScoringCriteria.value = activity.scoringCriteria.map(c => ({
            name: c.name,
            maxScore: c.maxScore,
            isCreated: false,
            isEditing: false,
            originalName: c.name,
            originalScore: c.maxScore
        }));
        console.log('✅ Loaded criteria for editing:', editScoringCriteria.value);
    } else {
        editScoringCriteria.value = [];
        console.log('⚠️ No criteria found for this activity');
    }

    showEditDialog.value = true;
};

// Delete confirmation dialog state
const showDeleteDialog = ref(false);
const activityToDelete = ref({ activity: null, index: null });

// Handle delete confirmation
const confirmDelete = (activity, index) => {
    closeMenu();
    activityToDelete.value = { activity, index };
    showDeleteDialog.value = true;
};

// Handle actual deletion
const handleDelete = async () => {
    if (activityToDelete.value.activity && activityToDelete.value.index !== null) {
        await deleteActivity(activityToDelete.value.activity, activityToDelete.value.index);
        showDeleteDialog.value = false;
        activityToDelete.value = { activity: null, index: null };
    }
};

// Handle delete activity
const deleteActivity = async (activity, index) => {
    try {
        console.log('Deleting activity:', activity.id);

        // Make API call to delete the activity
        const response = await axios.delete(`/api/activities/${activity.id}/`);

        console.log('✅ Activity deleted:', response.data);

        // Reload activities for the current folder
        if (selectedFolderId.value) {
            await loadActivities(selectedFolderId.value);
        }

        showSuccess('Activity deleted successfully!', 'Activity Deleted');

        // For now, just remove from local state
        activities.value.splice(index, 1);

    } catch (error) {
        console.error('Error deleting activity:', error);
        showError('Failed to delete activity', 'Error');
    }
};

// Submit activity state
const showSubmitDialog = ref(false);
const activityToSubmit = ref(null);

// Submit activity (show confirmation dialog)
const submitActivity = (activity, index) => {
    closeMenu();
    activityToSubmit.value = activity;
    showSubmitDialog.value = true;
};

// Confirm submit activity
const confirmSubmitActivity = async () => {
    if (!activityToSubmit.value) return;

    try {
        const wasRetracted = activityToSubmit.value.is_published === false && activityToSubmit.value.published_at === null;
        console.log('Publishing activity:', activityToSubmit.value.id, wasRetracted ? '(Re-publishing retracted activity)' : '');

        const response = await axios.post(`/api/activities/${activityToSubmit.value.id}/publish/`);

        if (response.data) {
            console.log('✅ Activity published successfully:', response.data);

            // Update the activity in the local list
            const activityIndex = activities.value.findIndex(a => a.id === activityToSubmit.value.id);
            if (activityIndex !== -1) {
                activities.value[activityIndex].is_published = true;
                activities.value[activityIndex].published_at = response.data.activity.published_at;
            }

            showSubmitDialog.value = false;
            activityToSubmit.value = null;

            if (wasRetracted) {
                showSuccess('Students can now see this activity again.', 'Activity Re-Published');
            } else {
                showSuccess('Students can now see this activity.', 'Activity Published');
            }
        }
    } catch (error) {
        console.error('❌ Error publishing activity:', error);
        showError(error.response?.data?.error || error.message, 'Failed to Publish Activity');
    }
};

// Retract activity state
const showRetractDialog = ref(false);
const activityToRetract = ref(null);

// Retract activity (show confirmation dialog)
const retractActivity = (activity, index) => {
    closeMenu();

    // Check if activity is published
    if (!activity.is_published) {
        alert('This activity is not published yet.');
        return;
    }

    activityToRetract.value = activity;
    showRetractDialog.value = true;
};

// Confirm retract activity
const confirmRetractActivity = async () => {
    if (!activityToRetract.value) return;

    try {
        console.log('Retracting activity:', activityToRetract.value.id);

        const response = await axios.post(`/api/activities/${activityToRetract.value.id}/retract/`);

        if (response.data) {
            console.log('✅ Activity retracted successfully:', response.data);

            // Update the activity in the local list
            const activityIndex = activities.value.findIndex(a => a.id === activityToRetract.value.id);
            if (activityIndex !== -1) {
                activities.value[activityIndex].is_published = false;
                activities.value[activityIndex].published_at = null;
            }

            showRetractDialog.value = false;
            activityToRetract.value = null;
            showSuccess('Students can no longer see this activity.', 'Activity Retracted');
        }
    } catch (error) {
        console.error('❌ Error retracting activity:', error);
        showError(error.response?.data?.error || error.message, 'Failed to Retract Activity');
    }
};

// Update activity
const updateActivity = async () => {
    // Validate Activity Type
    if (!editActivityData.value.type) {
        alert('Activity Type is required. Please select an activity type.');
        return;
    }

    // Validate Activity Title
    if (!editActivityData.value.title || !editActivityData.value.title.trim()) {
        alert('Activity Title is required. Please enter a title for the activity.');
        return;
    }

    // Validate Due Date
    if (!editActivityData.value.dueDate) {
        alert('Due Date is required. Please select a due date.');
        return;
    }

    // Validate Due Time
    if (!editActivityData.value.dueTime || !editActivityData.value.dueTime.trim()) {
        alert('Due Time is required. Please select a due time.');
        return;
    }

    // Validate Scoring Criteria
    const validCriteria = editScoringCriteria.value.filter(c => c.name && c.name.trim() && c.maxScore > 0);
    if (validCriteria.length === 0) {
        alert('Scoring Criteria is required. Please add at least one criterion with a name and points greater than 0.');
        return;
    }

    try {
        const activityId = editActivityData.value.id;

        console.log('Updating activity:', activityId);

        // Validate date and time
        if (editActivityData.value.dueDate) {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const selectedDate = new Date(editActivityData.value.dueDate);
            selectedDate.setHours(0, 0, 0, 0);

            if (selectedDate < today) {
                alert('Due date cannot be in the past. Please select today or a future date.');
                return;
            }

            // If the date is today, validate the time is not in the past
            if (selectedDate.getTime() === today.getTime()) {
                const currentTime = getCurrentTime();
                if (editActivityData.value.dueTime < currentTime) {
                    alert('Due time cannot be in the past. Please select a future time.');
                    return;
                }
            }
        }

        // Prepare scoring criteria
        const scoringCriteria = validCriteria.map(c => ({
            name: c.name,
            maxScore: parseInt(c.maxScore)
        }));

        // Create FormData to support file uploads
        const formData = new FormData();
        formData.append('title', editActivityData.value.title);
        formData.append('activity_type', editActivityData.value.type.value);
        formData.append('description', editActivityData.value.description || '');
        formData.append('due_date', editActivityData.value.dueDate);
        formData.append('due_time', editActivityData.value.dueTime || '');
        formData.append('scoring_criteria', JSON.stringify(scoringCriteria));

        // Add new instruction files if any
        if (editActivityData.value.instructionFiles && editActivityData.value.instructionFiles.length > 0) {
            for (const fileObj of editActivityData.value.instructionFiles) {
                // Only add new files (those with a file property, not existing ones from server)
                if (fileObj.file && !fileObj.id) {
                    formData.append('instruction_files', fileObj.file);
                }
            }
        }

        // Add IDs of files to delete
        if (editActivityData.value.deleteInstructionFileIds && editActivityData.value.deleteInstructionFileIds.length > 0) {
            formData.append('delete_instruction_file_ids', JSON.stringify(editActivityData.value.deleteInstructionFileIds));
        }

        // Make API call to update the activity
        const response = await axios.put(`/api/activities/${editActivityData.value.id}/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        console.log('✅ Activity updated:', response.data);

        // Reload activities for the current folder
        if (selectedFolderId.value) {
            await loadActivities(selectedFolderId.value);
        }

        showEditDialog.value = false;
        showSuccess('Activity updated successfully!', 'Activity Updated');
    } catch (error) {
        console.error('❌ Error updating activity:', error);
        showError(error.response?.data?.error || error.message, 'Failed to Update Activity');
    }
};

// Archive state
const archivedActivity = ref(null);
const showArchiveToast = ref(false);
let toastTimeout = null;

// Handle archive activity
const archiveActivity = (activity, index) => {
    closeMenu();

    // Store the activity and its index for potential undo
    archivedActivity.value = { ...activity, originalIndex: index };

    // Remove from the current list
    activities.value.splice(index, 1);

    // Show toast with undo option
    showArchiveToast.value = true;

    // Hide toast after 5 seconds
    if (toastTimeout) clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        showArchiveToast.value = false;
        // After timeout, you might want to make the archive permanent
        // by calling an API endpoint
        if (archivedActivity.value) {
            // makeArchivePermanent(archivedActivity.value);
            archivedActivity.value = null;
        }
    }, 5000);
};

// Handle undo archive
const undoArchive = () => {
    if (archivedActivity.value) {
        // Add the activity back to its original position
        activities.value.splice(
            archivedActivity.value.originalIndex,
            0,
            archivedActivity.value
        );

        // Hide toast and clear the archived activity
        showArchiveToast.value = false;
        archivedActivity.value = null;

        if (toastTimeout) {
            clearTimeout(toastTimeout);
            toastTimeout = null;
        }
    }
};

// Handle portfolio compilation confirmation
const confirmPortfolioCompilation = async () => {
    try {
        // Close the dialog
        showPortfolioCompilationDialog.value = false;

        // Get the class name from props
        const classNameValue = props.className || className.value;

        if (!classNameValue) {
            alert('Class name not found');
            return;
        }

        // Send notification to all students in this class
        const response = await axios.post('/api/notifications/portfolio-compilation/', {
            class_name: classNameValue
        });

        console.log('✅ Portfolio compilation notification sent:', response.data);

        // Set compilation as active
        portfolioCompilationActive.value = true;

        // Show success message with details
        const studentsNotified = response.data.students_notified || 0;
        showSuccess(`Portfolio compilation request sent successfully! ${studentsNotified} student(s) have been notified.`, 'Notification Sent');

    } catch (error) {
        console.error('❌ Error sending portfolio compilation notification:', error);
        const errorMsg = error.response?.data?.error || error.message;
        showError('Failed to send notification: ' + errorMsg, 'Error');
    }
};

// Handle confirm drop portfolio compilation
const confirmDropPortfolioCompilation = async () => {
    try {
        // Close the dialog
        showDropCompilationDialog.value = false;

        const classroomId = selectedClass.value?.id;

        if (!classroomId) {
            showError('No class selected or class ID is missing.', 'Error');
            return;
        }

        // Delete the compilation request and notify students
        const response = await axios.delete(`/api/notifications/portfolio-compilation/${classroomId}/`);

        console.log('✅ Portfolio compilation dropped:', response.data);

        // Set compilation as inactive and clear students list
        portfolioCompilationActive.value = false;
        portfolioStudents.value = [];

        // Show success message
        const envelopesDeleted = response.data.envelopes_deleted || 0;
        const notificationsDeleted = response.data.notifications_deleted || 0;
        const studentsNotified = response.data.students_notified || 0;
        showSuccess(`Portfolio compilation deleted successfully. ${envelopesDeleted} envelope(s) deleted, ${notificationsDeleted} notification(s) removed, ${studentsNotified} student(s) notified.`, 'Compilation Deleted');

    } catch (error) {
        console.error('❌ Error dropping portfolio compilation:', error);
        const errorMsg = error.response?.data?.error || error.message;
        showError('Failed to drop compilation request: ' + errorMsg, 'Error');
    }
};

onMounted(() => {
    // If the pupil's activities tab is active and no folder is selected, auto-select the first one.
    if (activeTab.value === 'pupil' && subjectFolders.value.length > 0 && !selectedFolderId.value) {
        const firstFolder = subjectFolders.value[0];
        showSubjectActivities(firstFolder.name, firstFolder.id);
        console.log('Automatically selected the first folder:', firstFolder.name);
    }
});

</script>

<style scoped>
.aspect-video {
    aspect-ratio: 16 / 9;
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
    color: #374151;
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
::deep(.p-dialog-header) {
    background: linear-gradient(90deg, #4338ca, #6d28d9, #2563eb);
    color: white;
}

::deep(.p-dialog-content) {
    background-color: white;
}

/* Dropdown styles */
::deep(.p-dropdown) {
    width: 100%;
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    transition: all 0.2s;
}

::deep(.p-dropdown:not(.p-disabled).p-focus) {
    box-shadow: 0 0 0 0.2rem rgba(99, 102, 241, 0.35);
    border-color: #6366f1;
}

::deep(.p-dropdown-panel .p-dropdown-items .p-dropdown-item) {
    padding: 0.5rem 1rem;
}

::deep(.p-dropdown-panel .p-dropdown-items .p-dropdown-item.p-highlight) {
    background-color: #4338ca;
    color: white;
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
</style>
