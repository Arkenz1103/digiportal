<template>
    <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-blue-50 p-6">
        <!-- Header with School Year Selector -->
        <div class="max-w-6xl mx-auto mb-8">
            <div class="flex items-center justify-between flex-wrap gap-4">
                <div>
                    <h1 class="text-3xl font-bold text-gray-800">Manage Classes</h1>
                    <div class="flex items-center gap-2 mt-2">
                        <span class="text-gray-600">School Year:</span>
                        <span class="px-3 py-1 rounded-full font-semibold"
                            :class="isViewingArchived ? 'bg-amber-100 text-amber-700' : 'bg-indigo-100 text-indigo-700'">
                            {{ isViewingArchived ? viewingArchivedSchoolYear?.name : (currentSchoolYear?.name || 'Not Set') }}
                        </span>
                        <span v-if="isViewingArchived" class="px-2 py-0.5 bg-amber-100 text-amber-700 text-xs rounded-full">
                            Archived
                        </span>
                        <span v-else-if="currentSchoolYear?.is_current" class="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">
                            Current
                        </span>
                        <button v-if="currentSchoolYear && !isViewingArchived" @click="openEditSchoolYearModal"
                            class="p-1.5 text-indigo-500 hover:bg-indigo-100 rounded-lg transition-all"
                            title="Edit school year name">
                            <i class="pi pi-pencil text-sm"></i>
                        </button>
                    </div>
                </div>
                <div v-if="!isViewingArchived" class="flex items-center gap-3">
                    <button @click="showArchiveListModal = true"
                        class="flex items-center gap-2 px-4 py-2.5 bg-indigo-100 text-indigo-700 rounded-xl font-medium hover:bg-indigo-200 transition-all">
                        <i class="pi pi-history"></i>
                        <span>Archives</span>
                    </button>
                    <button @click="showNewSchoolYearModal = true"
                        class="flex items-center gap-2 px-4 py-2.5 bg-indigo-600 text-white rounded-xl font-medium hover:bg-indigo-700 transition-all">
                        <i class="pi pi-calendar-plus"></i>
                        <span>New School Year</span>
                    </button>
                    <button @click="openCreateFolderModal"
                        class="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg">
                        <i class="pi pi-plus"></i>
                        <span>Assign Subject</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="flex justify-center items-center py-20">
            <div class="text-center">
                <div class="animate-spin rounded-full h-16 w-16 border-4 border-indigo-600 border-t-transparent mx-auto mb-4"></div>
                <p class="text-gray-600">Loading classes...</p>
            </div>
        </div>

        <!-- Classes Grid -->
        <div v-else class="max-w-6xl mx-auto">
            <!-- No Classes State -->
            <div v-if="classesWithFolders.length === 0" class="text-center py-20">
                <div class="bg-white rounded-2xl shadow-xl p-12 max-w-md mx-auto border-2 border-indigo-100">
                    <div class="w-20 h-20 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <i class="pi pi-folder-open text-4xl text-indigo-600"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-800 mb-2">No Subject Folders Yet</h3>
                    <p v-if="!isViewingArchived" class="text-gray-600">Click "Assign Subject" to add your first subject folder.</p>
                    <p v-else class="text-gray-600">This archived school year has no subject folders.</p>
                </div>
            </div>

            <!-- Classes List -->
            <div v-else class="space-y-6">
                <div v-for="classItem in classesWithFolders" :key="classItem.id"
                    class="bg-white rounded-2xl shadow-lg border-2 border-indigo-100 overflow-hidden">
                    <!-- Class Header -->
                    <div class="p-6 bg-gradient-to-r from-indigo-600 to-purple-600"
                        :class="{ 'from-amber-500 to-amber-600': isViewingArchived }">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-4">
                                <div class="w-14 h-14 bg-white/20 rounded-xl flex items-center justify-center">
                                    <span class="text-2xl font-bold text-white">{{ getClassSection(classItem.name) }}</span>
                                </div>
                                <div>
                                    <h2 class="text-xl font-bold text-white">{{ classItem.name }}</h2>
                                    <p class="text-indigo-100" :class="{ 'text-amber-100': isViewingArchived }">{{ classItem.subjects?.length || 0 }} subject folders</p>
                                </div>
                            </div>
                            <div class="flex items-center gap-3">
                                <!-- Class Code Display -->
                                <div v-if="classItem.class_code && !isViewingArchived" 
                                    class="flex items-center gap-2 px-3 py-2 bg-white/20 rounded-lg">
                                    <span class="text-white/80 text-sm">Code:</span>
                                    <span class="font-mono font-bold text-white tracking-wider">{{ classItem.class_code }}</span>
                                    <button @click.stop="copyClassCode(classItem.class_code, classItem.name)"
                                        class="p-1 hover:bg-white/20 rounded transition-all"
                                        title="Copy class code">
                                        <i class="pi pi-copy text-white text-sm"></i>
                                    </button>
                                </div>
                                <button v-if="!isViewingArchived" @click="openCreateFolderForClass(classItem)"
                                    class="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-all">
                                    <i class="pi pi-plus text-sm"></i>
                                    <span>Add Subject</span>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Subject Folders -->
                    <div class="p-6">
                        <!-- No Subject Folders Message -->
                        <div v-if="!classItem.subjects || classItem.subjects.length === 0" class="text-center py-8">
                            <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                <i class="pi pi-folder-open text-2xl text-gray-400"></i>
                            </div>
                            <p class="text-gray-500 mb-2">No subject folders yet</p>
                            <button v-if="!isViewingArchived" @click="openCreateFolderForClass(classItem)"
                                class="text-indigo-600 hover:text-indigo-700 font-medium text-sm">
                                <i class="pi pi-plus mr-1"></i>Add your first subject
                            </button>
                        </div>
                        <!-- Subject Folders Grid -->
                        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            <div v-for="(subject, index) in classItem.subjects" :key="index"
                                class="group relative bg-gradient-to-br from-gray-50 to-indigo-50 rounded-xl p-4 border border-indigo-100 hover:border-indigo-300 hover:shadow-md transition-all cursor-pointer"
                                @click="navigateToSubject(classItem, subject)">
                                <div class="flex items-center gap-3">
                                    <div class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center shadow-md">
                                        <i class="pi pi-folder text-white text-xl"></i>
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <h3 class="font-semibold text-gray-800 truncate">{{ subject }}</h3>
                                        <p class="text-sm text-gray-500">Subject Folder</p>
                                    </div>
                                    <div v-if="!isViewingArchived" class="flex gap-1 opacity-0 group-hover:opacity-100 transition-all">
                                        <button @click.stop="openEditFolderModal(classItem, subject)"
                                            class="p-2 text-indigo-500 hover:bg-indigo-50 rounded-lg transition-all"
                                            title="Edit folder">
                                            <i class="pi pi-pencil"></i>
                                        </button>
                                        <button @click.stop="confirmDeleteFolder(classItem, subject)"
                                            class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-all"
                                            title="Delete folder">
                                            <i class="pi pi-trash"></i>
                                        </button>
                                    </div>
                                    <div v-else class="text-gray-400">
                                        <i class="pi pi-eye"></i>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Create Subject Folder Modal -->
        <Dialog v-model:visible="showCreateFolderModal" modal header="Create Subject Folder" :style="{ width: '500px' }">
            <div class="space-y-4 p-2">
                <!-- School Year Selection -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Select School Year</label>
                    <Dropdown 
                        v-model="newFolder.schoolYearId" 
                        :options="allSchoolYearsForDropdown" 
                        optionLabel="displayName" 
                        optionValue="id"
                        placeholder="Choose a school year" 
                        class="w-full"
                        @change="onSchoolYearChange"
                    />
                </div>
                <!-- Class Selection (filtered by selected school year) -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Select Class</label>
                    <Dropdown 
                        v-model="newFolder.classId" 
                        :options="classesForSelectedSchoolYear" 
                        optionLabel="displayName" 
                        optionValue="id"
                        placeholder="Choose a class" 
                        class="w-full"
                        :disabled="!newFolder.schoolYearId"
                    />
                    <p v-if="!newFolder.schoolYearId" class="text-xs text-gray-500 mt-1">Please select a school year first</p>
                </div>
                <!-- Subject Name -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Subject Name</label>
                    <InputText v-model="newFolder.name" placeholder="e.g., Mathematics, Science, English" class="w-full" />
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <Button label="Cancel" severity="secondary" @click="showCreateFolderModal = false" />
                    <Button label="Create Folder" :disabled="!newFolder.classId || !newFolder.name.trim()"
                        @click="createSubjectFolder" :loading="isCreating"
                        class="bg-gradient-to-r from-indigo-600 to-purple-600" />
                </div>
            </template>
        </Dialog>

        <!-- Edit Subject Folder Modal -->
        <Dialog v-model:visible="showEditFolderModal" modal header="Edit Subject Folder" :style="{ width: '500px' }">
            <div class="space-y-4 p-2">
                <div class="p-3 bg-indigo-50 rounded-lg border border-indigo-100">
                    <p class="text-sm text-gray-600">Current folder: <strong class="text-indigo-700">{{ editFolder.originalName }}</strong></p>
                    <p class="text-sm text-gray-600">In class: <strong class="text-indigo-700">{{ editFolder.originalClassName }}</strong></p>
                </div>
                <!-- School Year Selection -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Move to School Year</label>
                    <Dropdown 
                        v-model="editFolder.schoolYearId" 
                        :options="allSchoolYearsForDropdown" 
                        optionLabel="displayName" 
                        optionValue="id"
                        placeholder="Choose a school year" 
                        class="w-full"
                        @change="onEditSchoolYearChange"
                    />
                </div>
                <!-- Class Selection -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Move to Class</label>
                    <Dropdown 
                        v-model="editFolder.newClassId" 
                        :options="classesForEditSchoolYear" 
                        optionLabel="displayName" 
                        optionValue="id"
                        placeholder="Select class" 
                        class="w-full"
                        :disabled="!editFolder.schoolYearId"
                    />
                </div>
                <!-- Subject Name -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Subject Name</label>
                    <InputText v-model="editFolder.newName" placeholder="e.g., Mathematics, Science, English" class="w-full" />
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <Button label="Cancel" severity="secondary" @click="showEditFolderModal = false" />
                    <Button label="Save Changes" :disabled="!editFolder.newClassId || !editFolder.newName.trim()"
                        @click="updateFolder" :loading="isUpdating"
                        class="bg-gradient-to-r from-indigo-600 to-purple-600" />
                </div>
            </template>
        </Dialog>

        <!-- Delete Confirmation Dialog -->
        <Dialog v-model:visible="showDeleteDialog" modal header="Delete Subject Folder" :style="{ width: '400px' }">
            <div class="p-4">
                <div class="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <i class="pi pi-exclamation-triangle text-2xl text-red-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">Are you sure you want to delete this folder?</p>
                        <p class="text-gray-600 text-sm mt-1">
                            Folder: <strong>{{ folderToDelete?.subject }}</strong><br>
                            Class: <strong>{{ folderToDelete?.classItem?.name }}</strong>
                        </p>
                        <p class="text-red-600 text-sm mt-2">This action cannot be undone.</p>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <Button label="Cancel" severity="secondary" @click="showDeleteDialog = false" />
                    <Button label="Delete" severity="danger" @click="deleteFolder" :loading="isDeleting" />
                </div>
            </template>
        </Dialog>

        <!-- New School Year Modal -->
        <Dialog v-model:visible="showNewSchoolYearModal" modal header="Start New School Year" :style="{ width: '550px' }">
            <div class="space-y-4 p-2">
                <div class="p-4 bg-amber-50 border border-amber-200 rounded-lg">
                    <div class="flex items-start gap-3">
                        <i class="pi pi-info-circle text-amber-600 text-xl mt-0.5"></i>
                        <div>
                            <p class="text-amber-800 font-medium">Starting a new school year will:</p>
                            <ul class="text-amber-700 text-sm mt-2 space-y-1">
                                <li>• Archive the current school year data</li>
                                <li>• Create fresh classrooms (copy your assigned classrooms)</li>
                                <li>• Generate class codes for students to join</li>
                                <li>• Students will use class codes to enroll themselves</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">School Year Name</label>
                    <InputText v-model="newSchoolYear.name" placeholder="e.g., 2025-2026" class="w-full" />
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
                        <Calendar v-model="newSchoolYear.start_date" dateFormat="yy-mm-dd" class="w-full" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">End Date</label>
                        <Calendar v-model="newSchoolYear.end_date" dateFormat="yy-mm-dd" class="w-full" />
                    </div>
                </div>
                <div class="space-y-3">
                    <div class="flex items-center gap-3">
                        <Checkbox v-model="newSchoolYear.copy_classrooms" :binary="true" inputId="copyClassrooms" />
                        <label for="copyClassrooms" class="text-sm text-gray-700">Copy classroom structure from current year</label>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <Button label="Cancel" severity="secondary" @click="showNewSchoolYearModal = false" />
                    <Button label="Start New Year" :disabled="!newSchoolYear.name || !newSchoolYear.start_date || !newSchoolYear.end_date"
                        @click="startNewSchoolYear" :loading="isStartingNewYear"
                        class="bg-amber-500 hover:bg-amber-600" />
                </div>
            </template>
        </Dialog>

        <!-- Edit School Year Modal -->
        <Dialog v-model:visible="showEditSchoolYearModal" modal header="Edit School Year" :style="{ width: '450px' }">
            <div class="space-y-4 p-2">
                <div class="p-3 bg-indigo-50 border border-indigo-100 rounded-lg">
                    <p class="text-sm text-indigo-700">
                        <i class="pi pi-info-circle mr-2"></i>
                        Changing the school year name will update all associated classrooms.
                    </p>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">School Year Name</label>
                    <InputText v-model="editSchoolYear.name" placeholder="e.g., 2024-2025" class="w-full" />
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <Button label="Cancel" severity="secondary" @click="showEditSchoolYearModal = false" />
                    <Button label="Save Changes" :disabled="!editSchoolYear.name?.trim() || editSchoolYear.name === editSchoolYear.originalName"
                        @click="updateSchoolYearName" :loading="isUpdatingSchoolYear"
                        class="bg-gradient-to-r from-indigo-600 to-purple-600" />
                </div>
            </template>
        </Dialog>

        <!-- Promotion Result Modal -->
        <Dialog v-model:visible="showPromotionResultModal" modal header="Promotion Complete" :style="{ width: '500px' }">
            <div class="space-y-4 p-2">
                <div class="p-4 bg-green-50 border border-green-200 rounded-lg">
                    <div class="flex items-center gap-3 mb-3">
                        <i class="pi pi-check-circle text-green-600 text-2xl"></i>
                        <p class="text-green-800 font-semibold">Students have been promoted!</p>
                    </div>
                    <div class="grid grid-cols-2 gap-4 text-sm">
                        <div class="p-3 bg-white rounded-lg border">
                            <p class="text-2xl font-bold text-indigo-600">{{ promotionResult.promoted }}</p>
                            <p class="text-gray-600">Promoted to next grade</p>
                        </div>
                        <div class="p-3 bg-white rounded-lg border">
                            <p class="text-2xl font-bold text-amber-600">{{ promotionResult.graduated }}</p>
                            <p class="text-gray-600">Graduated (Grade 6)</p>
                        </div>
                        <div class="p-3 bg-white rounded-lg border">
                            <p class="text-2xl font-bold text-green-600">{{ promotionResult.new_grade1 }}</p>
                            <p class="text-gray-600">New Grade 1 students</p>
                        </div>
                        <div class="p-3 bg-white rounded-lg border">
                            <p class="text-2xl font-bold text-gray-600">{{ promotionResult.unassigned }}</p>
                            <p class="text-gray-600">Unassigned</p>
                        </div>
                    </div>
                </div>
                <div class="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                    <p class="text-sm text-blue-800">
                        <i class="pi pi-info-circle mr-2"></i>
                        You can undo this promotion from the school year settings if needed.
                    </p>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-between">
                    <Button label="Undo Promotion" severity="warning" @click="undoPromotion" :loading="isUndoing" />
                    <Button label="Done" @click="showPromotionResultModal = false" class="bg-indigo-600" />
                </div>
            </template>
        </Dialog>

        <!-- Undo Promotion Confirmation Modal -->
        <Dialog v-model:visible="showUndoConfirmModal" modal header="Undo Student Promotion" :style="{ width: '450px' }">
            <div class="p-4">
                <div class="flex items-start gap-3 p-4 bg-orange-50 border border-orange-200 rounded-lg">
                    <i class="pi pi-exclamation-triangle text-2xl text-orange-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">Are you sure you want to undo the student promotion?</p>
                        <p class="text-gray-600 text-sm mt-2">This will:</p>
                        <ul class="text-gray-600 text-sm mt-1 space-y-1">
                            <li>• Revert all students to their previous grade & section</li>
                            <li>• Restore graduated students back to Grade 6</li>
                            <li>• Remove new Grade 1 assignments</li>
                        </ul>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <Button label="Cancel" severity="secondary" @click="showUndoConfirmModal = false" />
                    <Button label="Undo Promotion" severity="warning" @click="undoPromotion" :loading="isUndoing" />
                </div>
            </template>
        </Dialog>

        <!-- Archive List Modal -->
        <Dialog v-model:visible="showArchiveListModal" modal header="Archived School Years" :style="{ width: '700px' }">
            <div class="space-y-4">
                <div v-if="archivedSchoolYears.length === 0" class="text-center py-8">
                    <i class="pi pi-inbox text-4xl text-gray-300 mb-3"></i>
                    <p class="text-gray-500">No archived school years yet</p>
                </div>
                <div v-else class="space-y-3">
                    <div v-for="archive in archivedSchoolYears" :key="archive.id"
                        class="p-4 bg-gray-50 rounded-xl border border-gray-200 hover:border-indigo-300 transition-all">
                        <div class="flex items-center justify-between">
                            <div>
                                <h3 class="font-semibold text-gray-800">{{ archive.name }}</h3>
                                <p class="text-sm text-gray-500">Archived: {{ formatDate(archive.archived_at) }}</p>
                            </div>
                            <div class="flex items-center gap-4 text-sm">
                                <div class="text-center">
                                    <p class="font-semibold text-indigo-600">{{ archive.stats?.classrooms || 0 }}</p>
                                    <p class="text-gray-500">Classes</p>
                                </div>
                                <div class="text-center">
                                    <p class="font-semibold text-green-600">{{ archive.stats?.students || 0 }}</p>
                                    <p class="text-gray-500">Students</p>
                                </div>
                                <div class="text-center">
                                    <p class="font-semibold text-purple-600">{{ archive.stats?.submissions || 0 }}</p>
                                    <p class="text-gray-500">Submissions</p>
                                </div>
                                <div class="flex gap-2">
                                    <button @click="viewArchivedSchoolYear(archive)"
                                        class="p-2 text-gray-500 hover:bg-gray-200 rounded-lg transition-all"
                                        title="View details">
                                        <i class="pi pi-info-circle"></i>
                                    </button>
                                    <button @click="confirmViewArchivedMode(archive)"
                                        class="flex items-center gap-1 px-3 py-1.5 bg-indigo-100 text-indigo-700 hover:bg-indigo-200 rounded-lg transition-all text-sm font-medium"
                                        title="View full archived data">
                                        <i class="pi pi-eye text-xs"></i>
                                        <span>View</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Dialog>

        <!-- Confirm View Archived Mode Dialog -->
        <Dialog v-model:visible="showConfirmViewArchivedModal" modal header="View Archived School Year" :style="{ width: '450px' }">
            <div class="p-4">
                <div class="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                    <i class="pi pi-eye text-2xl text-amber-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">You are about to view archived data</p>
                        <p class="text-gray-600 text-sm mt-2">
                            School Year: <strong class="text-amber-700">{{ archiveToView?.name }}</strong>
                        </p>
                        <p class="text-gray-600 text-sm mt-2">This will switch to read-only mode where you can browse the archived school year's data without making any changes.</p>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <Button label="Cancel" severity="secondary" @click="showConfirmViewArchivedModal = false" />
                    <Button label="View Archived Data" @click="proceedToArchivedViewMode" class="bg-amber-500 hover:bg-amber-600" />
                </div>
            </template>
        </Dialog>

        <!-- View Archived School Year Modal -->
        <Dialog v-model:visible="showArchivedDetailModal" modal :header="'Archive: ' + (selectedArchive?.name || '')" :style="{ width: '900px' }">
            <div v-if="isLoadingArchive" class="flex justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-4 border-indigo-600 border-t-transparent"></div>
            </div>
            <div v-else-if="archivedDetail" class="space-y-4">
                <!-- Classrooms List -->
                <div class="space-y-3">
                    <h4 class="font-semibold text-gray-700">Classrooms</h4>
                    <div class="grid grid-cols-2 gap-3">
                        <div v-for="classroom in archivedDetail.classrooms" :key="classroom.id"
                            class="p-3 bg-indigo-50 rounded-lg border border-indigo-100 cursor-pointer hover:bg-indigo-100 transition-all"
                            @click="viewArchivedClassroom(classroom)">
                            <div class="flex items-center justify-between">
                                <div>
                                    <p class="font-medium text-indigo-700">{{ classroom.name }}</p>
                                    <p class="text-sm text-gray-500">{{ classroom.student_count }} students • {{ classroom.folder_count }} folders</p>
                                </div>
                                <i class="pi pi-eye text-indigo-500"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Dialog>

        <!-- View Archived Classroom Detail Modal -->
        <Dialog v-model:visible="showArchivedClassroomModal" modal :header="'Classroom: ' + (selectedArchivedClassroom?.name || '')" :style="{ width: '900px' }">
            <div v-if="isLoadingClassroomDetail" class="flex justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-4 border-indigo-600 border-t-transparent"></div>
            </div>
            <div v-else-if="archivedClassroomDetail" class="space-y-6">
                <!-- Tabs -->
                <TabView>
                    <TabPanel header="Home (Folders)">
                        <div class="space-y-3">
                            <div v-for="folder in archivedClassroomDetail.folders" :key="folder.id" class="p-4 bg-gray-50 rounded-lg">
                                <h5 class="font-semibold text-gray-800 mb-2">{{ folder.name }}</h5>
                                <div class="space-y-2">
                                    <div v-for="activity in folder.activities" :key="activity.id" class="p-2 bg-white rounded border">
                                        <div class="flex justify-between items-center">
                                            <span class="text-sm">{{ activity.title }}</span>
                                            <span class="text-xs text-gray-500">{{ activity.submissions?.length || 0 }} submissions</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </TabPanel>
                    <TabPanel header="Remarks">
                        <div class="space-y-2 max-h-96 overflow-y-auto">
                            <div v-for="remark in archivedClassroomDetail.remarks" :key="remark.id" class="p-3 bg-yellow-50 rounded-lg border border-yellow-100">
                                <div class="flex justify-between items-start">
                                    <div>
                                        <p class="text-sm font-medium text-gray-800">To: {{ remark.student }}</p>
                                        <p class="text-sm text-gray-600 mt-1">{{ remark.text }}</p>
                                    </div>
                                    <span class="text-xs text-gray-400">{{ formatDate(remark.created_at) }}</span>
                                </div>
                            </div>
                            <p v-if="!archivedClassroomDetail.remarks?.length" class="text-gray-500 text-center py-4">No remarks</p>
                        </div>
                    </TabPanel>
                    <TabPanel header="Notifications">
                        <div class="space-y-2 max-h-96 overflow-y-auto">
                            <div v-for="notif in archivedClassroomDetail.notifications" :key="notif.id" class="p-3 bg-blue-50 rounded-lg border border-blue-100">
                                <div class="flex justify-between items-start">
                                    <div>
                                        <p class="text-sm font-medium text-gray-800">{{ notif.title }}</p>
                                        <p class="text-sm text-gray-600">{{ notif.message }}</p>
                                    </div>
                                    <span class="text-xs text-gray-400">{{ formatDate(notif.created_at) }}</span>
                                </div>
                            </div>
                            <p v-if="!archivedClassroomDetail.notifications?.length" class="text-gray-500 text-center py-4">No notifications</p>
                        </div>
                    </TabPanel>
                    <TabPanel header="Students">
                        <div class="grid grid-cols-2 gap-2">
                            <div v-for="student in archivedClassroomDetail.students" :key="student.id" class="p-2 bg-gray-50 rounded flex items-center gap-2">
                                <i class="pi pi-user text-gray-400"></i>
                                <span class="text-sm">{{ student.name }}</span>
                            </div>
                        </div>
                        <p v-if="!archivedClassroomDetail.students?.length" class="text-gray-500 text-center py-4">No students</p>
                    </TabPanel>
                </TabView>
            </div>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import Calendar from 'primevue/calendar';
import Checkbox from 'primevue/checkbox';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import { useToast } from '../../composables/useToast';

const emit = defineEmits(['navigate']);
const { showSuccess, showError } = useToast();

// State
const isLoading = ref(true);
const isCreating = ref(false);
const isDeleting = ref(false);
const isUpdating = ref(false);
const isStartingNewYear = ref(false);
const isUndoing = ref(false);
const isLoadingArchive = ref(false);
const isLoadingClassroomDetail = ref(false);
const allClasses = ref([]);
const currentSchoolYear = ref(null);
const archivedSchoolYears = ref([]);
const archivedDetail = ref(null);
const archivedClassroomDetail = ref(null);
const currentUserId = ref(null); // Store current user ID to filter out assigned classroom
const selectedArchive = ref(null);
const selectedArchivedClassroom = ref(null);
const promotionResult = ref({ promoted: 0, graduated: 0, new_grade1: 0, unassigned: 0 });

// Archived View Mode State
const isViewingArchived = ref(false);
const viewingArchivedSchoolYear = ref(null);

// Modals
const showCreateFolderModal = ref(false);
const showEditFolderModal = ref(false);
const showDeleteDialog = ref(false);
const showNewSchoolYearModal = ref(false);
const showEditSchoolYearModal = ref(false);
const showPromotionResultModal = ref(false);
const showUndoConfirmModal = ref(false);
const showArchiveListModal = ref(false);
const showArchivedDetailModal = ref(false);
const showArchivedClassroomModal = ref(false);
const showConfirmViewArchivedModal = ref(false);
const archiveToView = ref(null);
const folderToDelete = ref(null);
const isUpdatingSchoolYear = ref(false);
const editSchoolYear = ref({ id: null, name: '', originalName: '' });

// Computed
// Classes for current school year - shows teacher's assigned classrooms AND classrooms where they have folders
const classesWithFolders = computed(() => {
    // If viewing archived school year, show teacher's classes from that year
    if (isViewingArchived.value && viewingArchivedSchoolYear.value) {
        return allClasses.value.filter(c => 
            c.school_year === viewingArchivedSchoolYear.value.name &&
            (c.teacher_id === currentUserId.value || (c.subjects && c.subjects.length > 0))
        );
    }
    
    // Normal mode: show teacher's assigned classrooms AND classrooms where they have folders
    if (!currentSchoolYear.value || !currentSchoolYear.value.name) {
        return allClasses.value.filter(c => 
            c.teacher_id === currentUserId.value || (c.subjects && c.subjects.length > 0)
        );
    }
    // Filter by current school year AND (teacher's assigned classrooms OR classrooms with folders)
    return allClasses.value.filter(c => 
        c.school_year === currentSchoolYear.value.name &&
        !c.is_archived &&
        (c.teacher_id === currentUserId.value || (c.subjects && c.subjects.length > 0))
    );
});

// Filter classes to only show those from the current school year
const currentSchoolYearClasses = computed(() => {
    if (!currentSchoolYear.value || !currentSchoolYear.value.name) {
        return allClasses.value;
    }
    return allClasses.value.filter(c => c.school_year === currentSchoolYear.value.name);
});

// All school years for dropdown (only current, not archived)
const allSchoolYearsForDropdown = computed(() => {
    const schoolYears = [];
    
    // Add current school year only (not archived)
    if (currentSchoolYear.value) {
        schoolYears.push({
            id: currentSchoolYear.value.id,
            name: currentSchoolYear.value.name,
            displayName: `${currentSchoolYear.value.name} (Current)`,
            isCurrent: true
        });
    }
    
    // Don't add archived school years to the dropdown
    // They can still be viewed in the Archives modal
    
    return schoolYears;
});

// Classes filtered by selected school year for create modal
// Excludes the teacher's assigned classroom (where teacher_id matches current user)
const classesForSelectedSchoolYear = computed(() => {
    if (!newFolder.value.schoolYearId) {
        return [];
    }
    
    const selectedSY = allSchoolYearsForDropdown.value.find(sy => sy.id === newFolder.value.schoolYearId);
    if (!selectedSY) return [];
    
    return allClasses.value
        .filter(c => c.school_year === selectedSY.name)
        .filter(c => c.teacher_id !== currentUserId.value) // Exclude teacher's assigned classroom
        .map(c => ({
            ...c,
            displayName: `${c.name} (${c.school_year})`
        }));
});

// Classes filtered by selected school year for edit modal
// Excludes the teacher's assigned classroom (where teacher_id matches current user)
const classesForEditSchoolYear = computed(() => {
    if (!editFolder.value.schoolYearId) {
        return [];
    }
    
    const selectedSY = allSchoolYearsForDropdown.value.find(sy => sy.id === editFolder.value.schoolYearId);
    if (!selectedSY) return [];
    
    return allClasses.value
        .filter(c => c.school_year === selectedSY.name)
        .filter(c => c.teacher_id !== currentUserId.value) // Exclude teacher's assigned classroom
        .map(c => ({
            ...c,
            displayName: `${c.name} (${c.school_year})`
        }));
});

// Handle school year change in create modal
const onSchoolYearChange = () => {
    // Reset class selection when school year changes
    newFolder.value.classId = null;
};

// Handle school year change in edit modal
const onEditSchoolYearChange = () => {
    // Reset class selection when school year changes
    editFolder.value.newClassId = null;
};

const newFolder = ref({ classId: null, name: '', schoolYearId: null });
const editFolder = ref({
    folderId: null, originalName: '', originalClassName: '',
    originalClassId: null, newClassId: null, newName: '', schoolYearId: null
});
const newSchoolYear = ref({
    name: '', start_date: null, end_date: null,
    copy_classrooms: true
});

// Helper functions
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

const getClassSection = (className) => {
    if (!className || typeof className !== 'string') return '';
    const parts = className.split(' ');
    return parts.length > 1 ? parts[parts.length - 1] : className;
};

const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};

// Copy class code to clipboard
const copyClassCode = async (code, className) => {
    try {
        await navigator.clipboard.writeText(code);
        showSuccess(`Class code "${code}" copied! Share this with students to join ${className}.`);
    } catch (err) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = code;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showSuccess(`Class code "${code}" copied!`);
    }
};

// Load school years
const loadSchoolYears = async () => {
    try {
        const response = await fetch('/api/school-years/', {
            credentials: 'include',
            headers: { 'Accept': 'application/json' }
        });
        if (response.ok) {
            const data = await response.json();
            currentSchoolYear.value = data.current;
        }
    } catch (error) {
        console.error('Error loading school years:', error);
    }
};

// Load archived school years
const loadArchivedSchoolYears = async () => {
    try {
        console.log('📦 Loading archived school years...');
        const response = await fetch('/api/school-years/archived/', {
            credentials: 'include',
            headers: { 'Accept': 'application/json' }
        });
        console.log('📦 Response status:', response.status);
        if (response.ok) {
            const data = await response.json();
            console.log('📦 Archived school years data:', data);
            archivedSchoolYears.value = data.archived_school_years || [];
            console.log('📦 Archived school years loaded:', archivedSchoolYears.value.length);
        } else {
            const errorData = await response.text();
            console.error('📦 Error response:', errorData);
        }
    } catch (error) {
        console.error('Error loading archived school years:', error);
    }
};

// Load classrooms
const loadClassrooms = async () => {
    isLoading.value = true;
    try {
        // Load ALL classrooms including from archived school years for folder creation
        const response = await fetch('/api/classrooms/?all=true&include_archived=true', {
            credentials: 'include',
            headers: { 'Accept': 'application/json' }
        });
        if (response.ok) {
            const data = await response.json();
            if (data.classrooms && data.classrooms.length > 0) {
                allClasses.value = data.classrooms.map(classroom => ({
                    id: classroom.id,
                    name: classroom.name,
                    grade_level: classroom.grade_level,
                    section: classroom.section,
                    school_year: classroom.school_year,
                    is_archived: classroom.is_archived,
                    teacher_id: classroom.teacher?.id || null, // Store teacher ID to identify assigned classroom
                    class_code: classroom.class_code, // Class code for student enrollment
                    subjects: []
                }));
                await loadSubjectsForClasses();
                console.log(`📚 Loaded ${allClasses.value.length} classrooms from all school years`);
            }
        }
    } catch (error) {
        console.error('Error loading classrooms:', error);
        showError('Failed to load classrooms');
    } finally {
        isLoading.value = false;
    }
};

const loadSubjectsForClasses = async () => {
    try {
        const response = await fetch('/api/portfolio/folders/', {
            credentials: 'include',
            headers: { 'Accept': 'application/json' }
        });
        if (response.ok) {
            const folders = await response.json();
            const foldersByClass = {};
            folders.forEach(folder => {
                if (folder.classroom) {
                    if (!foldersByClass[folder.classroom]) {
                        foldersByClass[folder.classroom] = [];
                    }
                    foldersByClass[folder.classroom].push(folder.name);
                }
            });
            allClasses.value = allClasses.value.map(classItem => ({
                ...classItem,
                subjects: [...new Set(foldersByClass[classItem.id] || [])]
            }));
        }
    } catch (error) {
        console.error('Error loading subjects:', error);
    }
};

// Folder operations
const openCreateFolderForClass = (classItem) => {
    // Find the school year for this class
    const schoolYear = allSchoolYearsForDropdown.value.find(sy => sy.name === classItem.school_year);
    newFolder.value = { 
        classId: classItem.id, 
        name: '',
        schoolYearId: schoolYear?.id || currentSchoolYear.value?.id || null
    };
    showCreateFolderModal.value = true;
};

// Open create folder modal without pre-selecting a class (from Assign Subject button)
const openCreateFolderModal = () => {
    newFolder.value = { 
        classId: null, 
        name: '',
        schoolYearId: currentSchoolYear.value?.id || null  // Default to current school year
    };
    showCreateFolderModal.value = true;
};

const createSubjectFolder = async () => {
    if (!newFolder.value.classId || !newFolder.value.name.trim()) return;
    isCreating.value = true;
    try {
        const selectedClass = allClasses.value.find(c => c.id === newFolder.value.classId);
        const response = await fetch('/api/portfolio/folders/', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
            body: JSON.stringify({ name: newFolder.value.name.trim(), class_name: selectedClass?.name || 'General' })
        });
        if (response.ok) {
            showSuccess('Subject folder created successfully');
            showCreateFolderModal.value = false;
            newFolder.value = { classId: null, name: '', schoolYearId: null };
            await loadSubjectsForClasses();
            window.dispatchEvent(new CustomEvent('folderCreated'));
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to create folder');
        }
    } catch (error) {
        console.error('Error creating folder:', error);
        showError('Failed to create folder');
    } finally {
        isCreating.value = false;
    }
};

const openEditFolderModal = async (classItem, subject) => {
    try {
        const response = await fetch('/api/portfolio/folders/', { credentials: 'include', headers: { 'Accept': 'application/json' } });
        if (response.ok) {
            const folders = await response.json();
            const folder = folders.find(f => f.classroom === classItem.id && f.name === subject);
            if (folder) {
                // Find the school year for this class
                const schoolYear = allSchoolYearsForDropdown.value.find(sy => sy.name === classItem.school_year);
                editFolder.value = {
                    folderId: folder.id, originalName: subject, originalClassName: classItem.name,
                    originalClassId: classItem.id, newClassId: classItem.id, newName: subject,
                    schoolYearId: schoolYear?.id || currentSchoolYear.value?.id || null
                };
                showEditFolderModal.value = true;
            }
        }
    } catch (error) {
        console.error('Error finding folder:', error);
        showError('Failed to load folder details');
    }
};

const updateFolder = async () => {
    if (!editFolder.value.folderId || !editFolder.value.newClassId || !editFolder.value.newName.trim()) return;
    isUpdating.value = true;
    try {
        const selectedClass = allClasses.value.find(c => c.id === editFolder.value.newClassId);
        const response = await fetch(`/api/portfolio/folders/${editFolder.value.folderId}/`, {
            method: 'PUT',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
            body: JSON.stringify({ name: editFolder.value.newName.trim(), class_name: selectedClass?.name || 'General' })
        });
        if (response.ok) {
            showSuccess('Folder updated successfully');
            showEditFolderModal.value = false;
            await loadSubjectsForClasses();
            window.dispatchEvent(new CustomEvent('folderUpdated'));
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to update folder');
        }
    } catch (error) {
        console.error('Error updating folder:', error);
        showError('Failed to update folder');
    } finally {
        isUpdating.value = false;
    }
};

const confirmDeleteFolder = (classItem, subject) => {
    folderToDelete.value = { classItem, subject };
    showDeleteDialog.value = true;
};

const deleteFolder = async () => {
    if (!folderToDelete.value) return;
    isDeleting.value = true;
    try {
        const response = await fetch('/api/portfolio/folders/', { credentials: 'include', headers: { 'Accept': 'application/json' } });
        if (response.ok) {
            const folders = await response.json();
            const folder = folders.find(f => f.classroom === folderToDelete.value.classItem.id && f.name === folderToDelete.value.subject);
            if (folder) {
                const deleteResponse = await fetch(`/api/portfolio/folders/${folder.id}/`, {
                    method: 'DELETE', credentials: 'include', headers: { 'X-CSRFToken': getCsrfToken() }
                });
                if (deleteResponse.ok) {
                    showSuccess('Folder deleted successfully');
                    showDeleteDialog.value = false;
                    folderToDelete.value = null;
                    await loadSubjectsForClasses();
                    window.dispatchEvent(new CustomEvent('folderDeleted'));
                } else {
                    showError('Failed to delete folder');
                }
            }
        }
    } catch (error) {
        console.error('Error deleting folder:', error);
        showError('Failed to delete folder');
    } finally {
        isDeleting.value = false;
    }
};

// School year operations
const startNewSchoolYear = async () => {
    if (!newSchoolYear.value.name || !newSchoolYear.value.start_date || !newSchoolYear.value.end_date) return;
    isStartingNewYear.value = true;
    try {
        const formatDateForApi = (date) => {
            if (!date) return null;
            const d = new Date(date);
            return d.toISOString().split('T')[0];
        };
        
        const response = await fetch('/api/school-years/start-new/', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
            body: JSON.stringify({
                name: newSchoolYear.value.name,
                start_date: formatDateForApi(newSchoolYear.value.start_date),
                end_date: formatDateForApi(newSchoolYear.value.end_date),
                copy_classrooms: newSchoolYear.value.copy_classrooms
            })
        });
        if (response.ok) {
            const data = await response.json();
            
            // Build success message with class codes info
            let message = `School year ${data.school_year.name} started successfully!`;
            if (data.class_codes && data.class_codes.length > 0) {
                message += ` ${data.class_codes.length} classroom(s) created. Share the class codes with students to let them join.`;
            }
            showSuccess(message);
            showNewSchoolYearModal.value = false;
            
            newSchoolYear.value = { name: '', start_date: null, end_date: null, copy_classrooms: true };
            await loadSchoolYears();
            await loadClassrooms();
            await loadArchivedSchoolYears();
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to start new school year');
        }
    } catch (error) {
        console.error('Error starting new school year:', error);
        showError('Failed to start new school year');
    } finally {
        isStartingNewYear.value = false;
    }
};

// Open edit school year modal
const openEditSchoolYearModal = () => {
    if (!currentSchoolYear.value) return;
    editSchoolYear.value = {
        id: currentSchoolYear.value.id,
        name: currentSchoolYear.value.name,
        originalName: currentSchoolYear.value.name
    };
    showEditSchoolYearModal.value = true;
};

// Update school year name
const updateSchoolYearName = async () => {
    if (!editSchoolYear.value.name?.trim() || editSchoolYear.value.name === editSchoolYear.value.originalName) return;
    
    isUpdatingSchoolYear.value = true;
    try {
        const response = await fetch(`/api/school-years/${editSchoolYear.value.id}/`, {
            method: 'PUT',
            credentials: 'include',
            headers: { 
                'Content-Type': 'application/json', 
                'X-CSRFToken': getCsrfToken() 
            },
            body: JSON.stringify({
                name: editSchoolYear.value.name.trim()
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            showSuccess(`School year renamed to "${data.name}" successfully!`);
            showEditSchoolYearModal.value = false;
            
            // Reload data to reflect changes
            await loadSchoolYears();
            await loadClassrooms();
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to update school year name');
        }
    } catch (error) {
        console.error('Error updating school year:', error);
        showError('Failed to update school year name');
    } finally {
        isUpdatingSchoolYear.value = false;
    }
};

// Undo promotion
const undoPromotion = async () => {
    if (!currentSchoolYear.value) return;
    isUndoing.value = true;
    try {
        const response = await fetch(`/api/school-years/${currentSchoolYear.value.id}/undo-promotion/`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'X-CSRFToken': getCsrfToken() }
        });
        if (response.ok) {
            const data = await response.json();
            showSuccess(`Promotion undone! ${data.stats.reverted} students reverted, ${data.stats.graduated_restored} graduates restored.`);
            showPromotionResultModal.value = false;
            showUndoConfirmModal.value = false;
            await loadSchoolYears();
            await loadClassrooms();
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to undo promotion');
        }
    } catch (error) {
        console.error('Error undoing promotion:', error);
        showError('Failed to undo promotion');
    } finally {
        isUndoing.value = false;
    }
};

// Confirm undo promotion from header button
const confirmUndoPromotion = () => {
    showUndoConfirmModal.value = true;
};

// Show confirmation dialog before entering archived view mode
const confirmViewArchivedMode = (archive) => {
    archiveToView.value = archive;
    showConfirmViewArchivedModal.value = true;
};

// Proceed to archived view mode after confirmation
const proceedToArchivedViewMode = () => {
    showConfirmViewArchivedModal.value = false;
    if (archiveToView.value) {
        enterArchivedViewMode(archiveToView.value);
        archiveToView.value = null;
    }
};

// Enter archived view mode - shows archived school year data across the app
const enterArchivedViewMode = (archive) => {
    viewingArchivedSchoolYear.value = archive;
    isViewingArchived.value = true;
    showArchiveListModal.value = false;
    
    // Store in localStorage so other pages can access it
    localStorage.setItem('viewing_archived_school_year', JSON.stringify(archive));
    
    // Dispatch event so other components (sidebar, etc.) can react
    window.dispatchEvent(new CustomEvent('archivedViewModeChanged', { 
        detail: { isViewing: true, schoolYear: archive } 
    }));
    
    console.log(`📂 Entered archived view mode: ${archive.name}`);
    showSuccess(`Now viewing archived school year: ${archive.name}`);
};

// Exit archived view mode - returns to current school year
const exitArchivedViewMode = () => {
    viewingArchivedSchoolYear.value = null;
    isViewingArchived.value = false;
    
    // Clear from localStorage
    localStorage.removeItem('viewing_archived_school_year');
    
    // Dispatch event so other components can react
    window.dispatchEvent(new CustomEvent('archivedViewModeChanged', { 
        detail: { isViewing: false, schoolYear: null } 
    }));
    
    console.log('📂 Exited archived view mode, back to current school year');
    showSuccess('Returned to current school year');
};

const viewArchivedSchoolYear = async (archive) => {
    selectedArchive.value = archive;
    showArchivedDetailModal.value = true;
    isLoadingArchive.value = true;
    try {
        const response = await fetch(`/api/school-years/${archive.id}/`, {
            credentials: 'include', headers: { 'Accept': 'application/json' }
        });
        if (response.ok) {
            archivedDetail.value = await response.json();
        }
    } catch (error) {
        console.error('Error loading archive details:', error);
        showError('Failed to load archive details');
    } finally {
        isLoadingArchive.value = false;
    }
};

const viewArchivedClassroom = async (classroom) => {
    selectedArchivedClassroom.value = classroom;
    showArchivedClassroomModal.value = true;
    isLoadingClassroomDetail.value = true;
    try {
        const response = await fetch(`/api/school-years/${selectedArchive.value.id}/classrooms/${classroom.id}/`, {
            credentials: 'include', headers: { 'Accept': 'application/json' }
        });
        if (response.ok) {
            archivedClassroomDetail.value = await response.json();
        }
    } catch (error) {
        console.error('Error loading classroom details:', error);
        showError('Failed to load classroom details');
    } finally {
        isLoadingClassroomDetail.value = false;
    }
};

const navigateToSubject = (classItem, subject) => {
    // In archived view mode, allow navigation but mark as read-only
    const isReadOnly = isViewingArchived.value;
    
    localStorage.setItem('digiportal_selected_class', JSON.stringify(classItem));
    localStorage.setItem('digiportal_selected_subject', subject);
    
    // Store read-only flag for archived view
    if (isReadOnly) {
        localStorage.setItem('digiportal_archived_view_readonly', 'true');
    } else {
        localStorage.removeItem('digiportal_archived_view_readonly');
    }
    
    window.dispatchEvent(new CustomEvent('subjectChanged', { detail: { classItem, subject, isReadOnly } }));
    emit('navigate', 'TeacherRoom');
};

// Load current user ID
const loadCurrentUser = async () => {
    try {
        const response = await fetch('/api/user/profile/', {
            credentials: 'include',
            headers: { 'Accept': 'application/json' }
        });
        if (response.ok) {
            const data = await response.json();
            currentUserId.value = data.id;
            console.log('👤 Current user ID:', currentUserId.value);
        }
    } catch (error) {
        console.error('Error loading user profile:', error);
    }
};

// Handle archived view mode change from MainLayout banner
const handleArchivedViewModeChange = (event) => {
    const { isViewing, schoolYear } = event.detail;
    isViewingArchived.value = isViewing;
    viewingArchivedSchoolYear.value = schoolYear;
    console.log('📂 ManageClass: Archived view mode changed:', isViewing, schoolYear?.name);
};

onMounted(async () => {
    // Listen for archived view mode changes from MainLayout banner
    window.addEventListener('archivedViewModeChanged', handleArchivedViewModeChange);
    
    // Check if we're already in archived view mode (from localStorage)
    const savedArchivedView = localStorage.getItem('viewing_archived_school_year');
    if (savedArchivedView) {
        try {
            const archivedData = JSON.parse(savedArchivedView);
            isViewingArchived.value = true;
            viewingArchivedSchoolYear.value = archivedData;
            console.log('📂 ManageClass: Restored archived view mode:', archivedData.name);
        } catch (e) {
            console.error('Error parsing archived view data:', e);
        }
    }
    
    await loadCurrentUser(); // Load user ID first
    await loadSchoolYears();
    await loadClassrooms();
    await loadArchivedSchoolYears();
});

onUnmounted(() => {
    // Clean up event listener
    window.removeEventListener('archivedViewModeChanged', handleArchivedViewModeChange);
});
</script>
