<template>
    <div class="flex flex-col">
        <!-- Class Header -->
        <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-6 md:p-4 shadow-lg rounded-t-xl">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div class="space-y-3">
                    <h1 class="text-xl md:text-2xl font-bold text-white px-4 py-2 md:px-6 md:py-3 rounded-lg inline-block bg-white/20">
                        {{ className }}
                    </h1>
                    <p class="text-white/90 ml-2 flex items-center gap-2">
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
                <template v-if="activeTab === 'pupil'">
                    <div class="p-4 md:p-6 bg-transparent">
                        <!-- Show folders view when not in activities mode -->
                        <div v-if="!showingActivities" class="space-y-6">
                            <!-- Header with title and New Folder button -->
                            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                                <h2 class="text-xl md:text-2xl font-bold text-gray-900">Pupils Portfolio</h2>
                                <button
                                    @click="showNewFolderDialog = true"
                                    class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                                >
                                    <i class="pi pi-plus"></i>
                                    <span>Create Class Portfolio</span>
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
                                <h3 class="text-lg font-medium text-gray-900 mb-2">No Portfolio Folders</h3>
                                <p class="text-gray-500">Click "Create Class Portfolio" to create your first folder.</p>
                            </div>
                            
                            <!-- Folders Grid -->
                            <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
                                <!-- Subject Folders -->
                                <div v-for="folder in subjectFolders"
                                    :key="folder.id"
                                    @click="showSubjectActivities(folder.name, folder.id)"
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
                                    <span class="text-2xl font-bold text-indigo-900">List of Activities - Portfolio {{ selectedSubject }}</span>
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
                                        @click="showingActivities = false"
                                        class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200"
                                    >
                                        <i class="pi pi-arrow-left"></i>
                                        <span>Back to Folders</span>
                                    </button>
                                </div>
                            </div>

                            <!-- Activities Table -->
                            <div class="bg-transparent rounded-xl shadow-sm overflow-hidden border-0">
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
                                    <!-- Table Header -->
                                    <div class="flex items-center px-4 md:px-6 py-4 bg-indigo-100/80 border-b border-indigo-200/50 rounded-t-xl">
                                        <div class="w-32">
                                            <span class="text-sm font-semibold text-indigo-900">Activity Type</span>
                                        </div>
                                        <div class="w-32 md:w-48">
                                            <span class="text-sm font-semibold text-indigo-900">Activity Tittle</span>
                                        </div>
                                        <div class="flex-1">
                                            <span class="text-sm font-semibold text-indigo-900">Description</span>
                                        </div>
                                        <div class="w-24 md:w-48 text-right">
                                            <span class="text-sm font-semibold text-indigo-900">Due Date</span>
                                        </div>
                                        <div class="w-8"></div>
                                    </div>

                                    <!-- Activity Items -->
                                    <div v-for="(activity, index) in activities" :key="activity.id"
                                    class="group flex items-center px-4 md:px-6 py-4 hover:bg-indigo-50 border-b border-indigo-100 cursor-pointer transition-colors duration-200"
                                    @click="navigateToActivityOutputs(activity, index)">
                                    <div class="w-32 flex items-center gap-2">
                                        <span class="text-sm text-indigo-700 capitalize">{{ activity.type }}</span>
                                        <span v-if="activity.archived" class="text-amber-500" title="Archived">
                                            <i class="pi pi-archive text-xs"></i>
                                        </span>
                                    </div>
                                    <div class="w-32 md:w-48">
                                        <span class="font-medium text-indigo-700 transition-colors duration-100">{{ activity.title }}</span>
                                    </div>
                                    <div class="flex-1">
                                        <span class="text-indigo-700 group-hover:text-indigo-900 transition-colors duration-200 line-clamp-2">{{ activity.description }}</span>
                                    </div>
                                    <div class="w-24 md:w-48 text-right">
                                        <span class="text-sm text-indigo-600">{{ activity.date }}</span>
                                    </div>
                                    <div class="w-12 flex justify-end opacity-100 relative" style="z-index: 50;">
                                        <button 
                                            class="p-1.5 rounded-full hover:bg-indigo-100 text-indigo-700 hover:text-indigo-900 focus:outline-none" 
                                            @click.stop="toggleActivityMenu($event, activity, index)"
                                            :ref="'menuButton' + index"
                                            :aria-expanded="activeMenuIndex === index"
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
                                                v-if="activeMenuIndex === index"
                                                class="activity-menu-dropdown fixed z-[9999] w-48 bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden py-1"
                                                :style="{
                                                    top: `${menuPosition.y}px`,
                                                    left: `${menuPosition.x - 180}px`
                                                }"
                                            >
                                                <button
                                                    @click.stop="editActivity(activity, index)"
                                                    class="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700 flex items-center gap-2"
                                                >
                                                    <i class="pi pi-pencil text-sm"></i>
                                                    <span>Edit Activity</span>
                                                </button>
                                                <button
                                                    @click.stop="confirmDelete(activity, index)"
                                                    class="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-red-50 hover:text-red-600 flex items-center gap-2"
                                                >
                                                    <i class="pi pi-trash text-sm"></i>
                                                    <span>Delete</span>
                                                </button>
                                                <button
                                                    @click.stop="archiveActivity(activity, index)"
                                                    class="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-amber-50 hover:text-amber-600 flex items-center gap-2"
                                                >
                                                    <i class="pi pi-archive text-sm"></i>
                                                    <span>Archive</span>
                                                </button>
                                            </div>
                                        </transition>
                                    </div>
                                </div>
                                </template>
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
            header="Create New - Portfolio Folder"
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
                        <div class="bg-white rounded-xl shadow-sm border border-indigo-100 p-6 group">
                            <!-- Folder Preview -->
                            <div class="relative h-32 mb-4">
                                <!-- Stacked Preview Images -->
                                <div class="absolute top-0 right-0 w-24 h-28 flex items-center justify-center">
                                    <div class="absolute w-20 h-24 rounded-md transform rotate-[-15deg] transition-transform duration-300 group-hover:rotate-[-20deg] group-hover:scale-105 bg-gradient-to-br from-violet-500 to-blue-600 shadow-md ring-1 ring-white/40"></div>
                                    <div class="absolute w-20 h-24 rounded-md transform rotate-[-5deg] transition-transform duration-300 group-hover:rotate-[-10deg] group-hover:scale-105 bg-gradient-to-br from-violet-400 to-blue-500 shadow-sm ring-1 ring-white/30"></div>
                                    <div class="absolute w-20 h-24 rounded-md transform rotate-[5deg] transition-transform duration-300 group-hover:rotate-[10deg] group-hover:scale-105 bg-gradient-to-br from-violet-300 to-blue-400 ring-1 ring-white/20"></div>
                                </div>
                                <!-- Folder Title -->
                                <h3 class="text-xl font-semibold text-gray-900 mb-1 relative z-10">{{ newFolder.title || 'Folder Title' }}</h3>
                                <span class="text-sm text-gray-600 relative z-10">0 items</span>
                            </div>
                            <!-- Folder Description -->
                            <p class="text-gray-600 text-sm">{{ newFolder.description || 'Your folder description will appear here' }}</p>
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

        <!-- Add Activity Dialog -->
        <Dialog v-model:visible="showAddActivityDialog"
            modal
            header="Add New Activity"
            :style="{ width: '90%', maxWidth: '40rem' }">
            <div class="p-6">
                <div class="space-y-4">
                    <div>
                        <label for="activityType" class="block text-sm font-medium text-gray-900 mb-1">Activity Type</label>
                        <Dropdown
                            id="activityType"
                            v-model="newActivity.type"
                            :options="activityTypes"
                            optionLabel="name"
                            placeholder="Select Activity Type"
                            class="w-full"
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
                        <label for="activityTitle" class="block text-sm font-medium text-gray-900 mb-1">Activity Title</label>
                        <input
                            id="activityTitle"
                            v-model="newActivity.title"
                            type="text"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            placeholder="Enter activity title"
                        >
                    </div>
                    <div>
                        <label for="activityDescription" class="block text-sm font-medium text-gray-900 mb-1">Description</label>
                        <textarea
                            id="activityDescription"
                            v-model="newActivity.description"
                            rows="3"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            placeholder="Enter activity description"
                        ></textarea>
                    </div>
                    <div>
                        <label for="activityDate" class="block text-sm font-medium text-gray-900 mb-1">Due Date</label>
                        <input
                            id="activityDate"
                            v-model="newActivity.dueDate"
                            type="date"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                        >
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-between items-center">
                    <p class="text-sm text-gray-500">* All fields are required</p>
                    <div class="flex gap-2">
                        <button @click="showAddActivityDialog = false"
                            class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                            Cancel
                        </button>
                        <button
                            @click="addNewActivity"
                            :disabled="!newActivity.type || !newActivity.title || !newActivity.description || !newActivity.dueDate"
                            :class="[
                                'px-4 py-2 rounded-lg transition-colors flex items-center gap-2',
                                newActivity.type && newActivity.title && newActivity.description && newActivity.dueDate
                                    ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                                    : 'bg-indigo-100 text-indigo-300 cursor-not-allowed'
                            ]"
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
                :style="{ width: '90%', maxWidth: '40rem' }">
            <div class="p-6">
                <div class="space-y-4">
                    <div>
                        <label for="editActivityType" class="block text-sm font-medium text-gray-900 mb-1">Activity Type</label>
                        <Dropdown
                            id="editActivityType"
                            v-model="editActivityData.type"
                            :options="activityTypes"
                            optionLabel="name"
                            placeholder="Select Activity Type"
                            class="w-full"
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
                        <label for="editActivityTitle" class="block text-sm font-medium text-gray-900 mb-1">Activity Title</label>
                        <input
                            id="editActivityTitle"
                            v-model="editActivityData.title"
                            type="text"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            placeholder="Enter activity title"
                        >
                    </div>
                    <div>
                        <label for="editActivityDescription" class="block text-sm font-medium text-gray-900 mb-1">Description</label>
                        <textarea
                            id="editActivityDescription"
                            v-model="editActivityData.description"
                            rows="3"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            placeholder="Enter activity description"
                        ></textarea>
                    </div>
                    <div>
                        <label for="editActivityDate" class="block text-sm font-medium text-gray-900 mb-1">Due Date</label>
                        <input
                            id="editActivityDate"
                            v-model="editActivityData.dueDate"
                            type="date"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                        >
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-between items-center">
                    <p class="text-sm text-gray-500">* All fields are required</p>
                    <div class="flex gap-2">
                        <button @click="showEditDialog = false"
                            class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                            Cancel
                        </button>
                        <button
                            @click="updateActivity"
                            :disabled="!editActivityData.type || !editActivityData.title || !editActivityData.description || !editActivityData.dueDate"
                            :class="[
                                'px-4 py-2 rounded-lg transition-colors flex items-center gap-2',
                                editActivityData.type && editActivityData.title && editActivityData.description && editActivityData.dueDate
                                    ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                                    : 'bg-indigo-100 text-indigo-300 cursor-not-allowed'
                            ]"
                        >
                            <i class="pi pi-check"></i>
                            Save Changes
                        </button>
                    </div>
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
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Calendar from 'primevue/calendar';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';

// Define emits for navigation
const emit = defineEmits(['navigate']);

// Navigate to activity outputs
const navigateToActivityOutputs = (activity, index) => {
    // Store the selected activity for the outputs page
    localStorage.setItem('selected_activity', JSON.stringify({
        id: activity.type + '-' + index,
        title: activity.title,
        description: activity.description,
        type: activity.type,
        date: activity.date,
        class: className.value,
        subject: selectedSubject.value || 'General'
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
    { name: 'Other', value: 'Other' }
]);

// Subject folders data
const subjectFolders = ref([]);
const isLoadingFolders = ref(false);

// New Folder Dialog State
const showNewFolderDialog = ref(false);
const newFolder = ref({ title: '', description: '' });

// Add Activity Dialog State
const showAddActivityDialog = ref(false);
const newActivity = ref({
    title: '',
    type: '',
    description: '',
    dueDate: ''
});

const editActivityData = ref({
    id: null,
    title: '',
    type: '',
    description: '',
    dueDate: ''
});

const showEditDialog = ref(false);

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
            alert('Portfolio folder created successfully!');
        }
    } catch (error) {
        console.error('Error creating folder:', error);
        console.error('Error response:', error.response?.data);
        
        // Show detailed error message
        const errorMsg = error.response?.data?.error || error.response?.data?.detail || error.message || 'Failed to create folder';
        alert(`Error: ${errorMsg}\n\nPlease check the console for more details.`);
        
        // If authentication failed, try to re-authenticate
        if (error.response?.status === 401) {
            console.log('Authentication failed, attempting to re-authenticate...');
            const authenticated = await authenticateWithBackend();
            if (authenticated) {
                alert('Re-authenticated successfully. Please try creating the folder again.');
            }
        }
    }
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

// Function to add new activity
const addNewActivity = async () => {
    if (!newActivity.value.type || !newActivity.value.title || !newActivity.value.description || !newActivity.value.dueDate) return;

    try {
        // Get the current folder ID
        const currentFolder = subjectFolders.value.find(f => f.name === selectedSubject.value);
        if (!currentFolder) {
            alert('Please select a folder first');
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
        }

        console.log('Creating activity:', {
            folder_id: currentFolder.id,
            activity_type: newActivity.value.type?.value || newActivity.value.type,
            title: newActivity.value.title,
            description: newActivity.value.description,
            due_date: formattedDueDate
        });

        // Save to database via API
        const response = await axios.post(`/api/portfolio/folders/${currentFolder.id}/activities/`, {
            activity_type: newActivity.value.type?.value || newActivity.value.type,
            title: newActivity.value.title,
            description: newActivity.value.description,
            due_date: formattedDueDate
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
                dueDate: ''
            };

            alert('Activity added successfully!');
        }
    } catch (error) {
        console.error('Error creating activity:', error);
        alert('Failed to create activity: ' + (error.response?.data?.message || error.message));
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

// Load selected class on mount
onMounted(() => {
    const savedClass = localStorage.getItem('digiportal_selected_class');
    if (savedClass) {
        selectedClass.value = JSON.parse(savedClass);
        className.value = selectedClass.value.name;
    }
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
    { id: 'pupil', name: 'Pupils Portfolio', icon: 'pi-users' },
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
const isSidebarCollapsed = inject('isSidebarCollapsed', ref(false));
const activeMenuIndex = ref(null);
const menuButtonRefs = ref({});
const menuPosition = ref({ x: 0, y: 0 });
const settingsRef = ref(null);

// Watch for sidebar state changes
watch(isSidebarCollapsed, (newValue) => {
    // This will trigger a re-render when the sidebar state changes
    console.log('Sidebar collapsed state changed to:', newValue);
});

// Toggle activity action menu
const toggleActivityMenu = (event, activity, index) => {
    event.stopPropagation();
    
    if (activeMenuIndex.value === index) {
        activeMenuIndex.value = null;
    } else {
        // Get the button's position
        const buttonRect = event.currentTarget.getBoundingClientRect();
        menuPosition.value = {
            x: buttonRect.right,
            y: buttonRect.bottom + window.scrollY
        };
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
                role: 'teacher'
            });
            console.log('Authentication successful:', authResponse.data.user);
            return true;
        } catch (authError) {
            console.error('Authentication failed:', authError);
            return false;
        }
    }
};

onMounted(async () => {
    document.addEventListener('click', handleDocumentClick, true);
    document.addEventListener('click', handleClickOutside);
    
    // Authenticate with backend first, then load folders
    const authenticated = await authenticateWithBackend();
    if (authenticated) {
        loadPortfolioFolders();
    } else {
        console.error('Failed to authenticate with backend');
    }
});

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
    if (toastTimeout) clearTimeout(toastTimeout);
});

onUnmounted(() => {
    document.removeEventListener('click', handleDocumentClick, true);
});

// Subject activities state
const showingActivities = ref(false);
const selectedSubject = ref('');
const selectedFolderId = ref(null);
const activities = ref([]);
const isLoadingActivities = ref(false);

// Function to show activities for a subject
const showSubjectActivities = async (subject, folderId) => {
    selectedSubject.value = subject;
    selectedFolderId.value = folderId;
    showingActivities.value = true;
    
    // Load activities from database
    await loadActivities(folderId);
};

// Function to load activities from database
const loadActivities = async (folderId) => {
    isLoadingActivities.value = true;
    try {
        const response = await axios.get(`/api/portfolio/folders/${folderId}/activities/`);
        if (response.data) {
            // Format activities for display
            activities.value = response.data.map(activity => ({
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
                archived: false
            }));
            console.log('Loaded activities:', activities.value);
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
    // Find the activity type object that matches the current activity's type
    const activityType = activityTypes.value.find(type => type.value === activity.type) || null;
    
    editActivityData.value = {
        id: index,
        title: activity.title,
        type: activityType, // Store the full type object for the dropdown
        description: activity.description,
        dueDate: activity.date
    };
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
        // Here you would typically make an API call to delete the activity
        console.log('Deleting activity:', activity, 'at index:', index);
        
        // Example API call (uncomment and modify as needed):
        // const response = await axios.delete(`/api/activities/${activity.id}`);
        // if (response.data.success) {
        //     // Remove the activity from the local state
        //     activities.value.splice(index, 1);
        //     // Show success message
        //     toast.success('Activity deleted successfully');
        // }
        
        // For now, just remove from local state
        activities.value.splice(index, 1);
        
    } catch (error) {
        console.error('Error deleting activity:', error);
        // Show error message
        // toast.error('Failed to delete activity');
    }
};

// Update activity
const updateActivity = async () => {
    try {
        // Update the activity in the local state
        const index = editActivityData.value.id;
        if (index !== null && activities.value[index]) {
            activities.value[index] = {
                ...activities.value[index],
                title: editActivityData.value.title,
                type: editActivityData.value.type.value, // Store just the value
                description: editActivityData.value.description,
                date: editActivityData.value.dueDate
            };
            
            // Here you would typically make an API call to update the activity
            // Example:
            // await axios.put(`/api/activities/${editActivityData.value.id}`, {
            //     title: editActivityData.value.title,
            //     type: editActivityData.value.type.value,
            //     description: editActivityData.value.description,
            //     due_date: editActivityData.value.dueDate
            // });
            
            showEditDialog.value = false;
            // Show success message
            // Example: toast.success('Activity updated successfully');
        }
    } catch (error) {
        console.error('Error updating activity:', error);
        // Show error message
        // Example: toast.error('Failed to update activity');
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
