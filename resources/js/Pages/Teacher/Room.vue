<template>
    <div class="flex flex-col">
        <!-- Class Header -->
        <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-4 md:p-3 shadow-lg rounded-t-xl">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                <div class="space-y-2">
                    <h1 class="text-xl md:text-2xl font-bold text-white px-4 py-2 md:px-5 md:py-2 rounded-lg inline-block bg-white/20">
                        {{ className }}
                    </h1>
                    <p class="text-white/90 ml-2 flex items-center gap-2 text-sm">
                        <i class="pi pi-user"></i>
                        Teacher: {{ currentUser.name }}
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
                                <div v-for="(folder, index) in subjectFolders"
                                    :key="folder.id"
                                    @click="showSubjectActivities(folder.name, folder.id)"
                                    class="group bg-white rounded-xl shadow-sm border border-indigo-100 overflow-hidden hover:shadow-lg transition-all cursor-pointer transform hover:-translate-y-1 duration-200"
                                >
                                    <!-- Folder Preview -->
                                    <div class="relative h-36 mb-4 p-4 md:p-6">
                                        <!-- 3-Dot Menu Button -->
                                        <div class="absolute top-2 right-2 z-20">
                                            <button
                                                @click.stop="toggleFolderMenu($event, folder, index)"
                                                class="p-2 rounded-full hover:bg-indigo-100 text-gray-600 hover:text-indigo-700 transition-colors"
                                                :ref="'folderMenuButton' + index"
                                            >
                                                <i class="pi pi-ellipsis-v"></i>
                                            </button>
                                            
                                            <!-- Dropdown Menu -->
                                            <div
                                                v-if="activeFolderMenuIndex === index"
                                                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50"
                                            >
                                                <button
                                                    @click.stop="openUpdateFolderDialog(folder)"
                                                    class="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700 flex items-center gap-2"
                                                >
                                                    <i class="pi pi-pencil text-sm"></i>
                                                    <span>Update</span>
                                                </button>
                                                <button
                                                    @click.stop="openDropFolderDialog(folder)"
                                                    :disabled="folder.items > 0"
                                                    :class="[
                                                        'w-full text-left px-4 py-2.5 text-sm flex items-center gap-2',
                                                        folder.items > 0 
                                                            ? 'text-gray-400 cursor-not-allowed bg-gray-50' 
                                                            : 'text-gray-700 hover:bg-red-50 hover:text-red-600'
                                                    ]"
                                                    :title="folder.items > 0 ? 'Cannot drop folder with activities. Please delete all activities first.' : 'Drop this folder'"
                                                >
                                                    <i class="pi pi-trash text-sm"></i>
                                                    <span>Drop</span>
                                                </button>
                                            </div>
                                        </div>
                                        
                                        <!-- Stacked Preview Images with Dynamic Animation -->
                                        <div class="absolute top-5 right-12 w-28 h-32 flex items-center justify-center">
                                            <div class="absolute w-24 h-28 rounded-md transform rotate-[-15deg] transition-all duration-300 group-hover:rotate-[-20deg] group-hover:scale-105 bg-gradient-to-br from-violet-500 to-blue-600 shadow-md ring-1 ring-white/40"></div>
                                            <div class="absolute w-24 h-28 rounded-md transform rotate-[-5deg] transition-all duration-300 group-hover:rotate-[-10deg] group-hover:scale-105 bg-gradient-to-br from-violet-400 to-blue-500 shadow-sm ring-1 ring-white/30"></div>
                                            <div class="absolute w-24 h-28 rounded-md transform rotate-[5deg] transition-all duration-300 group-hover:rotate-[10deg] group-hover:scale-105 bg-gradient-to-br from-violet-300 to-blue-400 ring-1 ring-white/20"></div>
                                        </div>
                                        <!-- Folder Title -->
                                        <div class="relative z-10">
                                            <h3 class="text-xl md:text-2xl font-bold mb-1 text-gray-900 group-hover:text-indigo-700 transition-colors">
                                                {{ folder.name }}
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

                        <!-- Show activities list when a folder is selected -->
                        <div v-else>
                            <!-- Back button and List Header container -->
                            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
                                <!-- List of Activities Header -->
                                <div class="rounded-lg py-2 px-4">
                                    <span class="text-2xl font-bold text-indigo-900">List of Activities - {{ selectedSubject }}</span>
                                </div>

                                <div class="flex flex-wrap gap-2">
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

                                    <!-- Back button -->
                                    <button
                                        @click="backToFolders"
                                        class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                                    >
                                        <i class="pi pi-arrow-left"></i>
                                        <span>Back to Folders</span>
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
                                    <!-- DRAFT ACTIVITIES TABLE -->
                                    <div v-if="draftActivities.length > 0" class="mb-8">
                                        <div class="mb-3 px-2">
                                            <h3 class="text-lg font-bold text-gray-700 flex items-center gap-2">
                                                <i class="pi pi-file-edit text-indigo-600"></i>
                                                Draft Activities
                                            </h3>
                                        </div>
                                        
                                        <!-- Table Header -->
                                        <div class="flex items-center px-4 md:px-6 py-4 bg-indigo-100/80 border-b border-indigo-200/50 rounded-t-xl">
                                            <div class="w-32">
                                                <span class="text-sm font-semibold text-indigo-900">Activity Type</span>
                                            </div>
                                            <div class="w-40 md:w-48">
                                                <span class="text-sm font-semibold text-indigo-900">Activity Title</span>
                                            </div>
                                            <div class="flex-1">
                                                <span class="text-sm font-semibold text-indigo-900">Instruction</span>
                                            </div>
                                            <div class="w-28 text-center">
                                                <span class="text-sm font-semibold text-indigo-900">Due Time</span>
                                            </div>
                                            <div class="w-36 text-right">
                                                <span class="text-sm font-semibold text-indigo-900">Due Date</span>
                                            </div>
                                            <div class="w-12"></div>
                                        </div>

                                        <!-- Draft Activity Items -->
                                        <div v-for="(activity, index) in draftActivities" :key="activity.id"
                                    class="group flex items-center px-4 md:px-6 py-4 hover:bg-indigo-50 border-b border-indigo-100 cursor-pointer transition-colors duration-200"
                                    @click="navigateToActivityOutputs(activity, index)">
                                    <div class="w-32 flex items-center gap-2">
                                        <span class="text-sm text-indigo-700 capitalize">{{ activity.type }}</span>
                                        <span v-if="activity.archived" class="text-amber-500" title="Archived">
                                            <i class="pi pi-archive text-xs"></i>
                                        </span>
                                    </div>
                                    <div class="w-40 md:w-48">
                                        <span class="font-medium text-indigo-700 transition-colors duration-100">{{ activity.title }}</span>
                                    </div>
                                    <div class="flex-1 relative">
                                        <div class="instruction-cell group/tooltip">
                                            <span class="instruction-text">{{ activity.description }}</span>
                                            <div class="instruction-tooltip">
                                                {{ activity.description }}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="w-28 text-center">
                                        <span v-if="activity.formattedTime" class="text-sm text-indigo-600 font-medium">{{ activity.formattedTime }}</span>
                                        <span v-else class="text-xs text-gray-400 italic">No time</span>
                                    </div>
                                    <div class="w-36 text-right">
                                        <span class="text-sm text-indigo-600">{{ activity.date }}</span>
                                    </div>
                                    <div class="w-12 flex justify-end opacity-100 relative" style="z-index: 50;">
                                        <button 
                                            class="p-1.5 rounded-full hover:bg-indigo-100 text-indigo-700 hover:text-indigo-900 focus:outline-none" 
                                            @click.stop="toggleActivityMenu($event, activity, 'draft-' + index)"
                                            :ref="'menuButton-draft-' + index"
                                            :aria-expanded="activeMenuIndex === 'draft-' + index"
                                            aria-haspopup="true"
                                        >
                                            <i class="pi pi-ellipsis-v"></i>
                                        </button>
                                        
                                        <!-- Activity Actions Menu -->
                                        <transition
                                            enter-active-class="transition ease-out duration-100"
                                            enter-from-class="transform opacity-0 scale-95"
                                            enter-to-class="transform opacity-100 scale-100"
                                            leave-active-class="transition ease-in duration-75"
                                            leave-from-class="transform opacity-100 scale-100"
                                            leave-to-class="transform opacity-0 scale-95"
                                        >
                                            <div 
                                                v-if="activeMenuIndex === 'draft-' + index"
                                                class="activity-menu-dropdown absolute z-[9999] w-48 bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden py-1"
                                                style="bottom: 100%; margin-bottom: 0.5rem; right: 0;"
                                            >
                                                <button
                                                    @click.stop="submitActivity(activity, index)"
                                                    :disabled="activity.is_published"
                                                    :class="[
                                                        'w-full text-left px-4 py-2.5 text-sm flex items-center gap-2 transition-colors',
                                                        activity.is_published 
                                                            ? 'text-gray-400 cursor-not-allowed bg-gray-50' 
                                                            : 'text-gray-700 hover:bg-green-50 hover:text-green-700'
                                                    ]"
                                                    :title="activity.is_published ? 'Activity is already published. Use Retract to unpublish.' : 'Publish activity to students'"
                                                >
                                                    <i class="pi pi-send text-sm"></i>
                                                    <span>{{ activity.is_published ? 'Published' : 'Submit' }}</span>
                                                </button>
                                                <button
                                                    @click.stop="editActivity(activity, index)"
                                                    :disabled="isActivityPastDue(activity)"
                                                    :class="[
                                                        'w-full text-left px-4 py-2.5 text-sm flex items-center gap-2 transition-colors',
                                                        isActivityPastDue(activity)
                                                            ? 'text-gray-400 cursor-not-allowed bg-gray-50'
                                                            : 'text-gray-700 hover:bg-indigo-50 hover:text-indigo-700'
                                                    ]"
                                                    :title="isActivityPastDue(activity) ? 'Cannot edit activity within 3 hours of deadline or after it has passed' : 'Edit activity details'"
                                                >
                                                    <i class="pi pi-pencil text-sm"></i>
                                                    <span>Edit Activity</span>
                                                </button>
                                                <button
                                                    @click.stop="retractActivity(activity, index)"
                                                    :disabled="!activity.is_published"
                                                    :class="[
                                                        'w-full text-left px-4 py-2.5 text-sm flex items-center gap-2 transition-colors',
                                                        !activity.is_published 
                                                            ? 'text-gray-400 cursor-not-allowed bg-gray-50' 
                                                            : 'text-gray-700 hover:bg-orange-50 hover:text-orange-600'
                                                    ]"
                                                    :title="!activity.is_published ? 'Activity must be published first before retracting' : 'Retract activity from students'"
                                                >
                                                    <i class="pi pi-undo text-sm"></i>
                                                    <span>Retract</span>
                                                </button>
                                            </div>
                                        </transition>
                                    </div>
                                </div>
                                    </div>

                                    <!-- PUBLISHED ACTIVITIES TABLE -->
                                    <div v-if="publishedActivities.length > 0">
                                        <div class="mb-3 px-2">
                                            <h3 class="text-lg font-bold text-gray-700 flex items-center gap-2">
                                                <i class="pi pi-check-circle text-green-600"></i>
                                                Published Activities
                                            </h3>
                                        </div>
                                        
                                        <!-- Table Header -->
                                        <div class="flex items-center px-4 md:px-6 py-4 bg-green-100/80 border-b border-green-200/50 rounded-t-xl">
                                            <div class="w-32">
                                                <span class="text-sm font-semibold text-green-900">Activity Type</span>
                                            </div>
                                            <div class="w-40 md:w-48">
                                                <span class="text-sm font-semibold text-green-900">Activity Title</span>
                                            </div>
                                            <div class="flex-1">
                                                <span class="text-sm font-semibold text-green-900">Instruction</span>
                                            </div>
                                            <div class="w-28 text-center">
                                                <span class="text-sm font-semibold text-green-900">Due Time</span>
                                            </div>
                                            <div class="w-36 text-right">
                                                <span class="text-sm font-semibold text-green-900">Due Date</span>
                                            </div>
                                            <div class="w-12"></div>
                                        </div>

                                        <!-- Published Activity Items -->
                                        <div v-for="(activity, index) in publishedActivities" :key="activity.id"
                                        class="group flex items-center px-4 md:px-6 py-4 hover:bg-green-50 border-b border-green-100 cursor-pointer transition-colors duration-200"
                                        @click="navigateToActivityOutputs(activity, index)">
                                        <div class="w-32 flex items-center gap-2">
                                            <span class="text-sm text-green-700 capitalize">{{ activity.type }}</span>
                                            <span v-if="activity.archived" class="text-amber-500" title="Archived">
                                                <i class="pi pi-archive text-xs"></i>
                                            </span>
                                        </div>
                                        <div class="w-40 md:w-48">
                                            <span class="font-medium text-green-700 transition-colors duration-100">{{ activity.title }}</span>
                                        </div>
                                        <div class="flex-1 relative">
                                            <div class="instruction-cell group/tooltip">
                                                <span class="instruction-text text-green-700 group-hover:text-green-900">{{ activity.description }}</span>
                                                <div class="instruction-tooltip">
                                                    {{ activity.description }}
                                                </div>
                                            </div>
                                        </div>
                                        <div class="w-28 text-center">
                                            <span v-if="activity.formattedTime" class="text-sm text-green-600 font-medium">{{ activity.formattedTime }}</span>
                                            <span v-else class="text-xs text-gray-400 italic">No time</span>
                                        </div>
                                        <div class="w-36 text-right">
                                            <span class="text-sm text-green-600">{{ activity.date }}</span>
                                        </div>
                                        <div class="w-12 flex justify-end opacity-100 relative" style="z-index: 50;">
                                            <button 
                                                class="p-1.5 rounded-full hover:bg-green-100 text-green-700 hover:text-green-900 focus:outline-none" 
                                                @click.stop="toggleActivityMenu($event, activity, 'published-' + index)"
                                                :ref="'menuButton-published-' + index"
                                                :aria-expanded="activeMenuIndex === 'published-' + index"
                                                aria-haspopup="true"
                                            >
                                                <i class="pi pi-ellipsis-v"></i>
                                            </button>
                                            
                                            <!-- Activity Actions Menu -->
                                            <transition
                                                enter-active-class="transition ease-out duration-100"
                                                enter-from-class="transform opacity-0 scale-95"
                                                enter-to-class="transform opacity-100 scale-100"
                                                leave-active-class="transition ease-in duration-75"
                                                leave-from-class="transform opacity-100 scale-100"
                                                leave-to-class="transform opacity-0 scale-95"
                                            >
                                                <div 
                                                    v-if="activeMenuIndex === 'published-' + index"
                                                    class="activity-menu-dropdown absolute z-[9999] w-48 bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden py-1"
                                                    style="bottom: 100%; margin-bottom: 0.5rem; right: 0;"
                                                >
                                                    <button
                                                        @click.stop="submitActivity(activity, index)"
                                                        :disabled="activity.is_published"
                                                        :class="[
                                                            'w-full text-left px-4 py-2.5 text-sm flex items-center gap-2 transition-colors',
                                                            activity.is_published 
                                                                ? 'text-gray-400 cursor-not-allowed bg-gray-50' 
                                                                : 'text-gray-700 hover:bg-green-50 hover:text-green-700'
                                                        ]"
                                                        :title="activity.is_published ? 'Activity is already published. Use Retract to unpublish.' : 'Publish activity to students'"
                                                    >
                                                        <i class="pi pi-send text-sm"></i>
                                                        <span>{{ activity.is_published ? 'Published' : 'Submit' }}</span>
                                                    </button>
                                                    <button
                                                        @click.stop="editActivity(activity, index)"
                                                        :disabled="isActivityPastDue(activity)"
                                                        :class="[
                                                            'w-full text-left px-4 py-2.5 text-sm flex items-center gap-2 transition-colors',
                                                            isActivityPastDue(activity)
                                                                ? 'text-gray-400 cursor-not-allowed bg-gray-50'
                                                                : 'text-gray-700 hover:bg-indigo-50 hover:text-indigo-700'
                                                        ]"
                                                        :title="isActivityPastDue(activity) ? 'Cannot edit activity within 3 hours of deadline or after it has passed' : 'Edit activity details'"
                                                    >
                                                        <i class="pi pi-pencil text-sm"></i>
                                                        <span>Edit Activity</span>
                                                    </button>
                                                    <button
                                                        @click.stop="retractActivity(activity, index)"
                                                        :disabled="!activity.is_published"
                                                        :class="[
                                                            'w-full text-left px-4 py-2.5 text-sm flex items-center gap-2 transition-colors',
                                                            !activity.is_published 
                                                                ? 'text-gray-400 cursor-not-allowed bg-gray-50' 
                                                                : 'text-gray-700 hover:bg-orange-50 hover:text-orange-600'
                                                        ]"
                                                        :title="!activity.is_published ? 'Activity must be published first before retracting' : 'Retract activity from students'"
                                                    >
                                                        <i class="pi pi-undo text-sm"></i>
                                                        <span>Retract</span>
                                                    </button>
                                                </div>
                                            </transition>
                                        </div>
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
                                 :style="{ 
                                   background: `linear-gradient(135deg, ${selectedEnvelope.color} 0%, ${adjustBrightness(selectedEnvelope.color, -20)} 100%)`,
                                   animation: 'gradientShift 8s ease infinite'
                                 }">
                                
                                <!-- Animated Pattern Overlay (matching envelope) -->
                                <div v-if="selectedEnvelope.pattern === 'dots'" 
                                     class="absolute inset-0 opacity-10 pointer-events-none animate-patternFloat"
                                     style="background-image: radial-gradient(circle, white 2px, transparent 2px); background-size: 20px 20px;">
                                </div>
                                <div v-else-if="selectedEnvelope.pattern === 'lines'" 
                                     class="absolute inset-0 opacity-10 pointer-events-none animate-patternSlide"
                                     style="background-image: repeating-linear-gradient(45deg, white 0, white 2px, transparent 2px, transparent 10px);">
                                </div>
                                <div v-else-if="selectedEnvelope.pattern === 'grid'" 
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

                                <div class="max-w-5xl mx-auto p-8 relative z-10">
                                    <!-- Tab Header with Back Button -->
                                    <div class="flex justify-between items-center mb-6 animate-slideDown">
                                        <!-- Tab on the left -->
                                        <div class="flex gap-2">
                                            <button
                                                class="flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all duration-200 bg-indigo-600 text-white shadow-lg"
                                            >
                                                <i class="pi pi-list"></i>
                                                Student Activity Compilation
                                                <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-white/20">
                                                    {{ studentActivities.length }}
                                                </span>
                                            </button>
                                        </div>

                                        <!-- Back Button on the right -->
                                        <button
                                            @click="selectedEnvelope = null; isEnvelopeOpen = false; studentActivities = []; currentActivityIndex = 0"
                                            class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-lg border-2 border-gray-300 hover:border-indigo-500 hover:text-indigo-600 hover:bg-indigo-50 transition-all duration-200 shadow-md hover:shadow-lg flex items-center gap-2"
                                        >
                                            <i class="pi pi-arrow-left text-sm"></i>
                                            Back to List
                                        </button>
                                    </div>

                                    <!-- Display Student Activities (Carousel Style like Student View) -->
                                    <div class="relative min-h-[600px]">
                                    
                                    <!-- Loading state -->
                                    <div v-if="studentActivities.length === 0" class="text-center py-20 relative z-10">
                                        <div class="inline-block p-8 rounded-full mb-6 bg-white/30">
                                            <i class="pi pi-inbox text-6xl text-white"></i>
                                        </div>
                                        <p class="text-xl font-semibold text-white">No submitted activities found</p>
                                        <p class="text-sm text-white/80 mt-2">This student hasn't submitted any activities yet</p>
                                    </div>
                                    
                                    <!-- Activity Carousel -->
                                    <div v-else class="relative">
                                        <!-- Activity Counter with Enhanced Design -->
                                        <div class="absolute top-4 right-4 z-10 text-white px-6 py-3 rounded-full text-base font-bold shadow-2xl animate-pulse-slow transform transition-all duration-300 hover:scale-110"
                                             :style="{ 
                                               background: `linear-gradient(135deg, ${adjustBrightness(selectedEnvelope.color, -20)} 0%, ${adjustBrightness(selectedEnvelope.color, -40)} 100%)`,
                                               boxShadow: `0 0 30px ${selectedEnvelope.color}60, 0 8px 16px rgba(0,0,0,0.2)`
                                             }">
                                          <span class="relative z-10 flex items-center gap-2">
                                            <i class="pi pi-book"></i>
                                            {{ currentActivityIndex + 1 }} / {{ studentActivities.length }}
                                          </span>
                                          <div class="absolute inset-0 rounded-full animate-ping opacity-20"
                                               :style="{ backgroundColor: selectedEnvelope.color }">
                                          </div>
                                        </div>

                                        <!-- Activity Content -->
                                        <div v-if="studentActivities[currentActivityIndex]" 
                                             :key="currentActivityIndex"
                                             class="animate-fadeIn">
                                          <!-- Content Card with Glass Effect -->
                                          <div class="bg-white/95 backdrop-blur-sm rounded-2xl p-6 shadow-2xl relative transform transition-all duration-500 hover:shadow-3xl hover:scale-[1.01]">
                                            <!-- Activity Image/Preview -->
                                            <div class="aspect-video bg-gradient-to-br from-white/50 to-white/30 rounded-xl mb-6 flex items-center justify-center overflow-hidden relative border-2 border-white/50 shadow-lg transform transition-all duration-300 hover:shadow-2xl"
                                                 :style="{ borderColor: `${selectedEnvelope.color}40` }">
                                              <img v-if="studentActivities[currentActivityIndex].submission_file" 
                                                   :src="studentActivities[currentActivityIndex].submission_file"
                                                   alt="Activity submission"
                                                   class="w-full h-full object-contain"
                                                   @error="(e) => { e.target.style.display = 'none'; }"
                                              />
                                              <div v-else class="text-center flex flex-col items-center">
                                                <i class="pi pi-file text-6xl text-gray-300 mb-4"></i>
                                                <p class="text-gray-500 font-medium">No File</p>
                                              </div>
                                            </div>

                                            <!-- Submission Caption -->
                                            <div v-if="studentActivities[currentActivityIndex].submission_caption" class="mb-4 p-4 bg-gray-50 rounded-lg">
                                              <p class="text-sm text-gray-700 italic">
                                                "{{ studentActivities[currentActivityIndex].submission_caption }}"
                                              </p>
                                            </div>

                                            <!-- Score and Feedback -->
                                            <div v-if="studentActivities[currentActivityIndex].submission_score !== null" 
                                                 class="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                                              <div class="flex items-center justify-between mb-2">
                                                <span class="text-sm font-medium text-gray-700">Score:</span>
                                                <span class="text-2xl font-bold text-green-700">{{ studentActivities[currentActivityIndex].submission_score }}</span>
                                              </div>
                                              <div v-if="studentActivities[currentActivityIndex].submission_feedback" class="mt-2 pt-2 border-t border-green-200">
                                                <p class="text-sm text-gray-600">
                                                  <span class="font-medium">Feedback:</span> {{ studentActivities[currentActivityIndex].submission_feedback }}
                                                </p>
                                              </div>
                                            </div>

                                            <!-- Activity Details -->
                                            <div class="space-y-4">
                                              <div>
                                                <div class="flex items-center gap-3 mb-3">
                                                  <span class="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-xs font-semibold uppercase">
                                                    {{ studentActivities[currentActivityIndex].activity_type || 'Activity' }}
                                                  </span>
                                                  <span class="text-sm text-gray-500">
                                                    {{ studentActivities[currentActivityIndex].folder_name }}
                                                  </span>
                                                </div>
                                                <h3 class="text-2xl font-bold text-gray-900 mb-2">
                                                  {{ studentActivities[currentActivityIndex].title }}
                                                </h3>
                                                <p class="text-gray-600">
                                                  {{ studentActivities[currentActivityIndex].description }}
                                                </p>
                                              </div>

                                              <div class="grid grid-cols-2 md:grid-cols-3 gap-4 pt-4 border-t border-gray-200">
                                                <div>
                                                  <span class="text-sm text-gray-500 block mb-1">Status:</span>
                                                  <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium inline-block">
                                                    Submitted
                                                  </span>
                                                </div>
                                                <div v-if="studentActivities[currentActivityIndex].submitted_date">
                                                  <span class="text-sm text-gray-500 block mb-1">Submitted:</span>
                                                  <span class="text-sm font-medium text-gray-900">
                                                    {{ studentActivities[currentActivityIndex].submitted_date }}
                                                  </span>
                                                </div>
                                                <div v-if="studentActivities[currentActivityIndex].submitted_time">
                                                  <span class="text-sm text-gray-500 block mb-1">Time:</span>
                                                  <span class="text-sm font-medium text-gray-900">
                                                    {{ studentActivities[currentActivityIndex].submitted_time }}
                                                  </span>
                                                </div>
                                              </div>
                                            </div>
                                          </div>
                                        </div>
                                        
                                        <!-- Navigation Arrows with Enhanced Design -->
                                        <button
                                          @click="previousActivity"
                                          :disabled="currentActivityIndex === 0"
                                          class="absolute left-2 top-[200px] w-16 h-16 bg-white/95 backdrop-blur-md rounded-full shadow-2xl flex items-center justify-center hover:bg-white hover:scale-125 transition-all duration-300 disabled:opacity-20 disabled:cursor-not-allowed z-30 group"
                                          :style="{ 
                                            borderColor: selectedEnvelope.color, 
                                            borderWidth: '3px',
                                            boxShadow: `0 8px 32px ${selectedEnvelope.color}40, 0 0 0 0 ${selectedEnvelope.color}20`
                                          }"
                                        >
                                          <i class="pi pi-chevron-left text-2xl transition-all duration-300 group-hover:scale-110" 
                                             :style="{ color: selectedEnvelope.color }"></i>
                                          <div class="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                                               :style="{ 
                                                 background: `radial-gradient(circle, ${selectedEnvelope.color}20 0%, transparent 70%)`,
                                                 animation: 'pulse 2s infinite'
                                               }">
                                          </div>
                                        </button>
                                        <button
                                          @click="nextActivity"
                                          :disabled="currentActivityIndex >= studentActivities.length - 1"
                                          class="absolute right-2 top-[200px] w-16 h-16 bg-white/95 backdrop-blur-md rounded-full shadow-2xl flex items-center justify-center hover:bg-white hover:scale-125 transition-all duration-300 disabled:opacity-20 disabled:cursor-not-allowed z-30 group"
                                          :style="{ 
                                            borderColor: selectedEnvelope.color, 
                                            borderWidth: '3px',
                                            boxShadow: `0 8px 32px ${selectedEnvelope.color}40, 0 0 0 0 ${selectedEnvelope.color}20`
                                          }"
                                        >
                                          <i class="pi pi-chevron-right text-2xl transition-all duration-300 group-hover:scale-110" 
                                             :style="{ color: selectedEnvelope.color }"></i>
                                          <div class="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                                               :style="{ 
                                                 background: `radial-gradient(circle, ${selectedEnvelope.color}20 0%, transparent 70%)`,
                                                 animation: 'pulse 2s infinite'
                                               }">
                                          </div>
                                        </button>
                                    </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Show table if not viewing an envelope -->
                            <div v-else>
                                <!-- Header with Drop Button -->
                                <div class="flex justify-between items-center mb-6">
                                    <h2 class="text-2xl font-bold text-gray-900">Portfolio Compilation Status</h2>
                                    <button
                                        @click="showDropCompilationDialog = true"
                                        class="px-6 py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-all duration-200 shadow-lg hover:shadow-xl flex items-center gap-2"
                                    >
                                        <i class="pi pi-trash"></i>
                                        Drop Portfolio Compilation
                                    </button>
                                </div>

                                <!-- Table Container -->
                            <div class="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
                                <!-- Table Header -->
                                <div class="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-4">
                                    <div class="grid grid-cols-4 gap-4 text-white font-semibold text-sm">
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
                                    </div>
                                </div>

                                <!-- Table Body -->
                                <div class="divide-y divide-gray-200">
                                    <!-- Student Rows - Clickable -->
                                    <div 
                                        v-for="student in portfolioStudents" 
                                        :key="student.id"
                                        @click="viewStudentEnvelope(student)"
                                        class="px-6 py-4 hover:bg-indigo-50 transition-colors duration-150 cursor-pointer"
                                    >
                                        <div class="grid grid-cols-4 gap-4 items-center text-sm">
                                            <div class="flex items-center gap-3">
                                                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white font-semibold">
                                                    {{ student.name.charAt(0) }}
                                                </div>
                                                <span class="font-medium text-gray-900">{{ student.name }}</span>
                                            </div>
                                            <div class="text-gray-700 font-mono">{{ student.idNumber }}</div>
                                            <div class="text-gray-700">{{ student.dateCreated }}</div>
                                            <div class="text-gray-700">{{ student.timeCreated }}</div>
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
            </div>
        </div>

        <!-- New Folder Dialog -->
        <Dialog v-model:visible="showNewFolderDialog"
            modal
            header="Create New Folder"
            :style="{ width: '90%', maxWidth: '40rem' }">
            <div class="p-6">
                <div class="grid grid-cols-2 gap-6">
                    <!-- Form Fields -->
                    <div class="space-y-4">
                        <div>
                            <label for="folderTitle" class="block text-sm font-medium text-gray-900 mb-1">Title</label>
                            <input
                                id="folderTitle"
                                v-model="newFolder.title"
                                type="text"
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                                placeholder="Enter folder title"
                            >
                        </div>
                        <div>
                            <label for="folderDescription" class="block text-sm font-medium text-gray-900 mb-1">Description</label>
                            <textarea
                                id="folderDescription"
                                v-model="newFolder.description"
                                rows="3"
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                                placeholder="Enter folder description"
                            ></textarea>
                        </div>
                    </div>

                    <!-- Preview -->
                    <div>
                        <label class="block text-sm font-medium text-gray-900 mb-3">Preview</label>
                        <div class="bg-white rounded-xl shadow-sm border border-indigo-100 overflow-hidden group">
                            <!-- Folder Preview -->
                            <div class="relative h-36 mb-4 p-4 md:p-6">
                                <!-- Stacked Preview Images with Dynamic Animation -->
                                <div class="absolute top-5 right-5 w-28 h-32 flex items-center justify-center">
                                    <div class="absolute w-24 h-28 rounded-md transform rotate-[-15deg] transition-all duration-300 group-hover:rotate-[-20deg] group-hover:scale-105 bg-gradient-to-br from-violet-500 to-blue-600 shadow-md ring-1 ring-white/40"></div>
                                    <div class="absolute w-24 h-28 rounded-md transform rotate-[-5deg] transition-all duration-300 group-hover:rotate-[-10deg] group-hover:scale-105 bg-gradient-to-br from-violet-400 to-blue-500 shadow-sm ring-1 ring-white/30"></div>
                                    <div class="absolute w-24 h-28 rounded-md transform rotate-[5deg] transition-all duration-300 group-hover:rotate-[10deg] group-hover:scale-105 bg-gradient-to-br from-violet-300 to-blue-400 ring-1 ring-white/20"></div>
                                </div>
                                <!-- Folder Title -->
                                <div class="relative z-10 pr-32">
                                    <h3 class="text-xl md:text-2xl font-bold mb-1 text-gray-900 group-hover:text-indigo-700 transition-colors break-words overflow-hidden">
                                        {{ newFolder.title || 'Folder Title' }}
                                    </h3>
                                    <div class="flex items-center space-x-2">
                                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                                            0 items
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

        <!-- Drop Folder Dialog -->
        <Dialog v-model:visible="showDropFolderDialog"
            modal
            header="Drop Portfolio Folder"
            :style="{ width: '90%', maxWidth: '35rem' }">
            <div class="space-y-4">
                <div class="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <i class="pi pi-exclamation-triangle text-red-600 text-xl mt-0.5"></i>
                    <div>
                        <h4 class="font-semibold text-red-900 mb-1">Warning: Permanent Action</h4>
                        <p class="text-sm text-red-700">
                            Dropping this portfolio folder will permanently delete the folder.
                        </p>
                        <p class="text-sm text-red-700 mt-2 font-medium">
                            This action cannot be undone!
                        </p>
                    </div>
                </div>
                <div class="p-4 bg-gray-50 rounded-lg">
                    <p class="text-sm text-gray-700">
                        <strong>Folder:</strong> {{ dropFolderData.name }}
                    </p>
                    <p class="text-sm text-gray-700 mt-1">
                        <strong>Items:</strong> {{ dropFolderData.items }} activities
                    </p>
                </div>
                <div v-if="dropFolderData.items > 0" class="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                    <i class="pi pi-info-circle text-amber-600 text-xl mt-0.5"></i>
                    <div>
                        <p class="text-sm text-amber-700">
                            <strong>Note:</strong> This folder contains activities. You must delete all activities before you can drop this folder.
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-2">
                    <button @click="showDropFolderDialog = false"
                        class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                        Cancel
                    </button>
                    <button
                        @click="dropFolder"
                        :disabled="dropFolderData.items > 0"
                        :class="[
                            'px-4 py-2 rounded-lg transition-colors flex items-center gap-2',
                            dropFolderData.items > 0
                                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                                : 'bg-red-600 text-white hover:bg-red-700'
                        ]"
                    >
                        <i class="pi pi-trash"></i>
                        Drop Folder
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
                        Drop Request
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
                            <label for="activityTitle" class="block text-xs font-medium text-gray-700 mb-0.5">
                                Activity Title <span class="text-red-500">*</span>
                            </label>
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
                            <label for="activityDescription" class="block text-xs font-medium text-gray-700 mb-0.5">Instruction</label>
                            <textarea
                                id="activityDescription"
                                v-model="newActivity.description"
                                rows="2"
                                class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
                                placeholder="Enter instruction"
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
                                    <input
                                        v-model="criterion.name"
                                        type="text"
                                        placeholder="Name"
                                        required
                                        :disabled="criterion.isCreated && !criterion.isEditing"
                                        class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                                        :class="{ 
                                            'border-red-300': !criterion.name && !criterion.isCreated,
                                            'bg-gray-50 cursor-not-allowed': criterion.isCreated && !criterion.isEditing
                                        }"
                                    />
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
                                        @click="removeSavedCriterion(index)"
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
                            <label for="editActivityDescription" class="block text-xs font-medium text-gray-700 mb-0.5">Instruction</label>
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
                <div class="flex items-start gap-4">
                    <div class="mt-1 flex-shrink-0">
                        <div class="h-10 w-10 rounded-full bg-orange-100 flex items-center justify-center">
                            <i class="pi pi-undo text-orange-600 text-xl"></i>
                        </div>
                    </div>
                    <div>
                        <h3 class="text-lg font-medium text-gray-900">Retract Activity from Students</h3>
                        <p class="mt-1 text-gray-600">
                            Are you sure you want to retract "<span class="font-medium">{{ activityToRetract?.title }}</span>"? 
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
                        <h3 class="text-lg font-medium text-gray-900">Delete Activity</h3>
                        <p class="mt-1 text-gray-600">
                            Are you sure you want to delete "<span class="font-medium">{{ activityToDelete.activity?.title }}</span>"? 
                            This action cannot be undone.
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
                        Delete
                    </button>
                </div>
            </template>
        </Dialog>
        
        <!-- Archive Toast -->
        <div v-if="showArchiveToast" class="fixed bottom-4 right-4 z-[9999]">
            <div class="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden w-80">
                <div class="p-4 flex items-start">
                    <div class="flex-shrink-0">
                        <div class="h-10 w-10 rounded-full bg-amber-100 flex items-center justify-center">
                            <i class="pi pi-archive text-amber-600"></i>
                        </div>
                    </div>
                    <div class="ml-3 flex-1">
                        <p class="text-sm font-medium text-gray-900">Activity Archived</p>
                        <p class="mt-1 text-sm text-gray-500">
                            {{ archivedActivity?.title || 'Activity' }} has been moved to archive.
                        </p>
                    </div>
                    <div class="ml-4 flex-shrink-0 flex">
                        <button @click="undoArchive" class="text-sm font-medium text-indigo-600 hover:text-indigo-500">
                            Undo
                        </button>
                        <button @click="showArchiveToast = false" class="ml-4 text-gray-400 hover:text-gray-500">
                            <span class="sr-only">Close</span>
                            <i class="pi pi-times"></i>
                        </button>
                    </div>
                </div>
                <div class="bg-gray-100 h-1 w-full">
                    <div class="bg-amber-500 h-full transition-all duration-5000 ease-linear" 
                         :class="{'w-0': !showArchiveToast, 'w-full': showArchiveToast}"
                         style="transition-duration: 5s;"></div>
                </div>
            </div>
        </div>
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
        scoringCriteria: activity.scoringCriteria // Use camelCase
    }));
    
    // Navigate to outputs page
    emit('navigate', 'TeacherOutputs');
};

// Navigate to special progress page
const navigateToProgress = () => {
    // Store current class context for progress tracking
    localStorage.setItem('progress_class_context', JSON.stringify({
        className: className.value,
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
const updateFolderData = ref({ id: null, title: '', description: '' });

// Drop Folder Dialog State
const showDropFolderDialog = ref(false);
const dropFolderData = ref({ id: null, name: '', items: 0 });

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
    scoringCriteria: [
        { name: '', maxScore: 10 }
    ]
});

// Saved criteria list (displayed on the right side)
const savedCriteria = ref([
    { name: '', maxScore: 0, isCreated: false, isEditing: false, originalName: '', originalScore: 0 }
]);

const editActivityData = ref({
    id: null,
    title: '',
    type: '',
    description: '',
    dueDate: '',
    dueTime: ''
});

const editScoringCriteria = ref([]);
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
const openUpdateFolderDialog = (folder) => {
    updateFolderData.value = {
        id: folder.id,
        title: folder.name,
        description: folder.description || ''
    };
    showUpdateFolderDialog.value = true;
    activeFolderMenuIndex.value = null;
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

// Open drop folder dialog
const openDropFolderDialog = (folder) => {
    // Prevent opening dialog if folder has activities
    if (folder.items > 0) {
        showWarning(`This folder contains ${folder.items} activity/activities. Please delete all activities first before deleting the folder.`, 'Cannot Delete Folder');
        activeFolderMenuIndex.value = null;
        return;
    }
    
    dropFolderData.value = {
        id: folder.id,
        name: folder.name,
        items: folder.items || 0
    };
    showDropFolderDialog.value = true;
    activeFolderMenuIndex.value = null;
};

// Drop folder
const dropFolder = async () => {
    try {
        console.log('Dropping folder:', dropFolderData.value);
        
        // Delete folder from database (only if it has no activities)
        const response = await axios.delete(`/api/portfolio/folders/${dropFolderData.value.id}/`);
        
        console.log('Folder dropped successfully:', response.data);
        
        // Remove the folder from the list
        subjectFolders.value = subjectFolders.value.filter(f => f.id !== dropFolderData.value.id);
        
        // If we're currently viewing this folder's activities, go back to folder view
        if (selectedFolderId.value === dropFolderData.value.id) {
            showingActivities.value = false;
            selectedSubject.value = '';
            selectedFolderId.value = null;
            activities.value = [];
        }
        
        showDropFolderDialog.value = false;
        dropFolderData.value = { id: null, name: '', items: 0 };
        
        showSuccess('Portfolio folder has been permanently deleted.', 'Folder Deleted');
    } catch (error) {
        console.error('Error dropping folder:', error);
        console.error('Error details:', error.response?.data);
        
        // Get error message from backend
        const errorMsg = error.response?.data?.error || error.response?.data?.detail || error.message;
        const errorDetail = error.response?.data?.detail || '';
        
        // Show detailed error message
        if (errorDetail) {
            showError(`${errorMsg}\n\n${errorDetail}`, 'Failed to Delete Folder');
        } else {
            showError(errorMsg, 'Failed to Delete Folder');
        }
        
        // Close the dialog
        showDropFolderDialog.value = false;
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
        const response = await axios.get('/api/portfolio/folders/');
        
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

// Remove a saved criterion (after it's created)
const removeSavedCriterion = (index) => {
    if (confirm('Are you sure you want to delete this criterion?')) {
        savedCriteria.value.splice(index, 1);
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

        // Save to database via API
        const response = await axios.post(`/api/portfolio/folders/${currentFolder.id}/activities/`, {
            activity_type: newActivity.value.type?.value || newActivity.value.type,
            title: newActivity.value.title,
            description: newActivity.value.description,
            due_date: formattedDueDate,
            due_time: newActivity.value.dueTime || null,
            scoring_criteria: JSON.stringify(criteriaForSubmission)
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

// Function to handle class change event
const handleClassChange = async (event) => {
    console.log('🔄 Class changed in Room, reloading data...', event.detail);
    
    // Update selected class in localStorage (already done by MainLayout, but ensure it's set)
    localStorage.setItem('digiportal_selected_class', JSON.stringify(event.detail));
    
    // Update local state
    selectedClass.value = event.detail;
    className.value = event.detail.name;
    
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
    
    console.log('✅ Folders reloaded for class:', event.detail.name);
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

const activeTab = ref('pupil');

// Tab configurations
const tabs = [
    { id: 'pupil', name: "Pupil's Activities", icon: 'pi-users' },
    { id: 'portfolio', name: "Pupil's Portfolio Compilation", icon: 'pi-folder' },
    { id: 'schedule', name: 'Schedule', icon: 'pi-calendar' }
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
const portfolioCompilationActive = ref(false); // Track if compilation is already requested

// Portfolio students data
const portfolioStudents = ref([]);
const showEnvelopeViewDialog = ref(false);
const selectedEnvelope = ref(null);
const isEnvelopeOpen = ref(false);
const studentActivities = ref([]); // Store student's submitted activities
const currentActivityIndex = ref(0); // Current activity index for carousel

const isSidebarCollapsed = inject('isSidebarCollapsed', ref(false));
const activeMenuIndex = ref(null);
const menuButtonRefs = ref({});
const menuPosition = ref({ x: 0, y: 0 });
const settingsRef = ref(null);

// Watch for sidebar state changes
watch(isSidebarCollapsed, (newValue) => {
    // This will trigger a re-render when the sidebar state changes
    // console.log('Sidebar collapsed state changed to:', newValue);
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
        const classNameValue = props.className || className.value;
        
        if (!classNameValue) {
            return;
        }
        
        const response = await axios.get(`/api/notifications/portfolio-compilation/${encodeURIComponent(classNameValue)}/`);
        
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
    }
};

// View student envelope
const viewStudentEnvelope = async (student) => {
    selectedEnvelope.value = student;
    isEnvelopeOpen.value = true; // Automatically open and show activities
    currentActivityIndex.value = 0; // Reset to first activity
    console.log('Viewing activities for:', student.name);
    
    // Fetch student activities immediately
    await fetchStudentActivities(student.student_id);
};

// Navigate activities
const nextActivity = () => {
    if (currentActivityIndex.value < studentActivities.value.length - 1) {
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
                name: env.student_name,
                idNumber: env.id_number,
                dateCreated: env.date_created,
                timeCreated: env.time_created,
                // Store full envelope data for viewing
                title: env.title,
                color: env.color,
                pattern: env.pattern,
                className: env.class_name || props.className || className.value
            }));
            
            console.log(`✅ Loaded ${portfolioStudents.value.length} portfolio envelopes`);
        }
    } catch (error) {
        console.error('❌ Error fetching portfolio envelopes:', error);
        portfolioStudents.value = [];
    }
};

onMounted(async () => {
    document.addEventListener('click', handleDocumentClick, true);
    document.addEventListener('click', handleClickOutside);
    document.addEventListener('click', closeFolderMenu);
    
    // Authenticate with backend first, then load folders
    const authenticated = await authenticateWithBackend();
    if (authenticated) {
        await loadPortfolioFolders();
        
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
    } else {
        console.error('Failed to authenticate with backend');
    }
});

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
    document.removeEventListener('click', closeFolderMenu);
    if (toastTimeout) clearTimeout(toastTimeout);
});

onUnmounted(() => {
    document.removeEventListener('click', handleDocumentClick, true);
    window.removeEventListener('classChanged', handleClassChange);
});

// Subject activities state
const showingActivities = ref(false);
const selectedSubject = ref('');
const selectedFolderId = ref(null);
const activities = ref([]);
const isLoadingActivities = ref(false);

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
    
    // Clear saved view state
    localStorage.removeItem('teacher_current_view');
    console.log('🗑️ Cleared teacher view state');
};

// Function to show activities for a subject
const showSubjectActivities = async (subject, folderId) => {
    selectedSubject.value = subject;
    selectedFolderId.value = folderId;
    showingActivities.value = true;
    
    // Save view state to localStorage
    localStorage.setItem('teacher_current_view', JSON.stringify({
        showingActivities: true,
        selectedSubject: subject,
        selectedFolderId: folderId
    }));
    console.log('💾 Saved teacher view state: Activities for', subject);
    
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
                    published_at: activity.published_at || null    // Include publish timestamp
                };
            });
            console.log('✅ Final loaded activities:', activities.value);
        }
    } catch (error) {
        console.error('Error loading activities:', error);
        activities.value = [];
    } finally {
        isLoadingActivities.value = false;
    }
};

// Handle edit activity
const editActivity = (activity, index) => {
    closeMenu();
    
    // Check if activity is past due or too close to deadline
    if (isActivityPastDue(activity)) {
        alert('Cannot edit activity within 3 hours of the deadline or after it has passed.');
        return;
    }
    
    console.log('📝 Editing activity:', activity);
    console.log('📊 Activity scoring criteria:', activity.scoringCriteria);
    
    // Find the activity type object that matches the current activity's type
    const activityType = activityTypes.value.find(type => type.value === activity.type) || null;
    
    editActivityData.value = {
        id: activity.id,
        title: activity.title,
        type: activityType,
        description: activity.description,
        dueDate: activity.due_date,
        dueTime: activity.due_time || ''
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
        // Show error message
        // toast.error('Failed to delete activity');
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
        
        // Make API call to update the activity
        const response = await axios.put(`/api/activities/${editActivityData.value.id}/`, {
            title: editActivityData.value.title,
            activity_type: editActivityData.value.type.value,
            description: editActivityData.value.description,
            due_date: editActivityData.value.dueDate,
            due_time: editActivityData.value.dueTime || null,
            scoring_criteria: JSON.stringify(scoringCriteria)
        });
        
        console.log('✅ Activity updated:', response.data);
        
        // Reload activities for the current folder
        if (selectedFolderId.value) {
            await loadActivities(selectedFolderId.value);
        }
        
        showEditDialog.value = false;
        showSuccess('Activity has been updated successfully!', 'Activity Updated');
    } catch (error) {
        console.error('❌ Error updating activity:', error);
        const errorMessage = error.response?.data?.error || error.message || 'Unknown error occurred';
        showError(`Failed to update activity: ${errorMessage}`, 'Update Failed');
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
        const successMessage = `Portfolio compilation request sent successfully! ${studentsNotified} student(s) have been notified.`;
        showSuccess(successMessage, 'Request Sent');
        
    } catch (error) {
        console.error('❌ Error sending portfolio compilation notification:', error);
        const errorMsg = error.response?.data?.error || error.message || 'Unknown error occurred';
        showError(`Failed to send notification: ${errorMsg}`, 'Request Failed');
    }
};

// Handle confirm drop portfolio compilation
const confirmDropPortfolioCompilation = async () => {
    try {
        // Close the dialog
        showDropCompilationDialog.value = false;
        
        const classNameValue = props.className || className.value;
        
        if (!classNameValue) {
            alert('Class name not found');
            return;
        }
        
        // Delete the compilation request and notify students
        const response = await axios.delete(`/api/notifications/portfolio-compilation/${encodeURIComponent(classNameValue)}/`);
        
        console.log('✅ Portfolio compilation dropped:', response.data);
        
        // Set compilation as inactive and clear students list
        portfolioCompilationActive.value = false;
        portfolioStudents.value = [];
        
        // Show success message with details
        const envelopesDeleted = response.data.envelopes_deleted || 0;
        const notificationsDeleted = response.data.notifications_deleted || 0;
        const studentsNotified = response.data.students_notified || 0;
        
        const successMessage = `${envelopesDeleted} portfolio envelope(s) deleted, ${notificationsDeleted} notification(s) removed, ${studentsNotified} student(s) notified about cancellation.`;
        showSuccess(successMessage, 'Portfolio Compilation Deleted');
        
    } catch (error) {
        console.error('❌ Error dropping portfolio compilation:', error);
        const errorMsg = error.response?.data?.error || error.message || 'Unknown error occurred';
        showError(`Failed to drop compilation request: ${errorMsg}`, 'Delete Failed');
    }
};

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

/* ===== Instruction Cell with Tooltip Styles ===== */
.instruction-cell {
    position: relative;
    width: 100%;
    cursor: help;
}

.instruction-text {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.5;
    color: #4338ca;
    transition: color 0.2s ease;
    word-break: break-word;
    max-width: 100%;
}

/* Hover effect on text */
.instruction-cell:hover .instruction-text {
    color: #312e81;
}

/* Tooltip styling */
.instruction-tooltip {
    position: absolute;
    left: 0;
    top: 100%;
    margin-top: 0.5rem;
    padding: 0.75rem 1rem;
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
    color: white;
    border-radius: 0.5rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.2);
    font-size: 0.875rem;
    line-height: 1.6;
    max-width: 400px;
    min-width: 250px;
    z-index: 1000;
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    pointer-events: none;
    word-wrap: break-word;
    white-space: normal;
}

/* Tooltip arrow */
.instruction-tooltip::before {
    content: '';
    position: absolute;
    bottom: 100%;
    left: 1.5rem;
    border: 6px solid transparent;
    border-bottom-color: #1e1b4b;
}

/* Show tooltip on hover */
.instruction-cell:hover .instruction-tooltip {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

/* Responsive adjustments for mobile */
@media (max-width: 768px) {
    .instruction-text {
        -webkit-line-clamp: 3;
        font-size: 0.875rem;
    }
    
    .instruction-tooltip {
        max-width: 280px;
        min-width: 200px;
        font-size: 0.8125rem;
        left: 50%;
        transform: translateX(-50%) translateY(-10px);
    }
    
    .instruction-cell:hover .instruction-tooltip {
        transform: translateX(-50%) translateY(0);
    }
    
    .instruction-tooltip::before {
        left: 50%;
        transform: translateX(-50%);
    }
}

/* Ensure tooltip doesn't overflow on right side */
@media (min-width: 769px) {
    .instruction-tooltip {
        max-width: min(400px, 90vw);
    }
}

/* Alternative: Right-aligned tooltip for cells near the end */
.instruction-cell.tooltip-right .instruction-tooltip {
    left: auto;
    right: 0;
}

.instruction-cell.tooltip-right .instruction-tooltip::before {
    left: auto;
    right: 1.5rem;
}
</style>
