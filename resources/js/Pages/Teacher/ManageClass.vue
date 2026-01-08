<template>
    <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-blue-50 p-6">
        <!-- Header -->
        <div class="max-w-6xl mx-auto mb-8">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-3xl font-bold text-gray-800">Manage Classes</h1>
                </div>
                <button @click="showCreateFolderModal = true"
                    class="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg">
                    <i class="pi pi-plus"></i>
                    <span>Assign Subject</span>
                </button>
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
                    <p class="text-gray-600">Click "Create Subject Folder" to add your first subject folder.</p>
                </div>
            </div>

            <!-- Classes List -->
            <div v-else class="space-y-6">
                <div v-for="classItem in classesWithFolders" :key="classItem.id"
                    class="bg-white rounded-2xl shadow-lg border-2 border-indigo-100 overflow-hidden">
                    <!-- Class Header -->
                    <div class="p-6 bg-gradient-to-r from-indigo-600 to-purple-600">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-4">
                                <div class="w-14 h-14 bg-white/20 rounded-xl flex items-center justify-center">
                                    <span class="text-2xl font-bold text-white">{{ getClassSection(classItem.name) }}</span>
                                </div>
                                <div>
                                    <h2 class="text-xl font-bold text-white">{{ classItem.name }}</h2>
                                    <p class="text-indigo-100">{{ classItem.subjects?.length || 0 }} subject folders</p>
                                </div>
                            </div>
                            <button @click="openCreateFolderForClass(classItem)"
                                class="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-all">
                                <i class="pi pi-plus text-sm"></i>
                                <span>Add Subject</span>
                            </button>
                        </div>
                    </div>

                    <!-- Subject Folders -->
                    <div class="p-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
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
                                    <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-all">
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
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Create Subject Folder Modal -->
        <Dialog v-model:visible="showCreateFolderModal" modal header="Create Subject Folder" :style="{ width: '450px' }">
            <div class="space-y-4 p-2">
                <!-- Select Class -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Select Class</label>
                    <Dropdown v-model="newFolder.classId" :options="allClasses" optionLabel="name" optionValue="id"
                        placeholder="Choose a class" class="w-full" />
                </div>

                <!-- Subject Name -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Subject Name</label>
                    <InputText v-model="newFolder.name" placeholder="e.g., Mathematics, Science, English"
                        class="w-full" />
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
        <Dialog v-model:visible="showEditFolderModal" modal header="Edit Subject Folder" :style="{ width: '450px' }">
            <div class="space-y-4 p-2">
                <!-- Current Info -->
                <div class="p-3 bg-indigo-50 rounded-lg border border-indigo-100">
                    <p class="text-sm text-gray-600">Current folder: <strong class="text-indigo-700">{{ editFolder.originalName }}</strong></p>
                    <p class="text-sm text-gray-600">In class: <strong class="text-indigo-700">{{ editFolder.originalClassName }}</strong></p>
                </div>

                <!-- Select New Class -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Move to Class</label>
                    <Dropdown v-model="editFolder.newClassId" :options="allClasses" optionLabel="name" optionValue="id"
                        placeholder="Select class" class="w-full" />
                </div>

                <!-- Subject Name -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Subject Name</label>
                    <InputText v-model="editFolder.newName" placeholder="e.g., Mathematics, Science, English"
                        class="w-full" />
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
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import { useToast } from '../../composables/useToast';

const emit = defineEmits(['navigate']);
const { showSuccess, showError } = useToast();

// State
const isLoading = ref(true);
const isCreating = ref(false);
const isDeleting = ref(false);
const isUpdating = ref(false);
const allClasses = ref([]); // All available classes for dropdown
const showCreateFolderModal = ref(false);
const showEditFolderModal = ref(false);
const showDeleteDialog = ref(false);
const folderToDelete = ref(null);

// Computed: Only classes with folders for display
const classesWithFolders = computed(() => {
    return allClasses.value.filter(c => c.subjects && c.subjects.length > 0);
});

const newFolder = ref({
    classId: null,
    name: ''
});

const editFolder = ref({
    folderId: null,
    originalName: '',
    originalClassName: '',
    originalClassId: null,
    newClassId: null,
    newName: ''
});

// Helper to get CSRF token
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

// Get section letter from class name
const getClassSection = (className) => {
    if (!className || typeof className !== 'string') return '';
    const parts = className.split(' ');
    return parts.length > 1 ? parts[parts.length - 1] : className;
};

// Load classrooms
const loadClassrooms = async () => {
    isLoading.value = true;
    try {
        // Use ?all=true to get all available classrooms for folder management
        const response = await fetch('/api/classrooms/?all=true', {
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
                    subjects: []
                }));
                await loadSubjectsForClasses();
            }
        }
    } catch (error) {
        console.error('Error loading classrooms:', error);
        showError('Failed to load classrooms');
    } finally {
        isLoading.value = false;
    }
};

// Load subjects (portfolio folders) for all classes
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

// Open create folder modal for specific class
const openCreateFolderForClass = (classItem) => {
    newFolder.value = {
        classId: classItem.id,
        name: ''
    };
    showCreateFolderModal.value = true;
};

// Create subject folder
const createSubjectFolder = async () => {
    if (!newFolder.value.classId || !newFolder.value.name.trim()) return;

    isCreating.value = true;
    try {
        const selectedClass = allClasses.value.find(c => c.id === newFolder.value.classId);
        
        const response = await fetch('/api/portfolio/folders/', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                name: newFolder.value.name.trim(),
                class_name: selectedClass?.name || 'General'
            })
        });

        if (response.ok) {
            showSuccess('Subject folder created successfully');
            showCreateFolderModal.value = false;
            newFolder.value = { classId: null, name: '' };
            await loadSubjectsForClasses();
            
            // Dispatch event to update sidebar
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

// Open edit folder modal
const openEditFolderModal = async (classItem, subject) => {
    try {
        // Find the folder ID
        const response = await fetch('/api/portfolio/folders/', {
            credentials: 'include',
            headers: { 'Accept': 'application/json' }
        });

        if (response.ok) {
            const folders = await response.json();
            const folder = folders.find(f => 
                f.classroom === classItem.id && 
                f.name === subject
            );

            if (folder) {
                editFolder.value = {
                    folderId: folder.id,
                    originalName: subject,
                    originalClassName: classItem.name,
                    originalClassId: classItem.id,
                    newClassId: classItem.id,
                    newName: subject
                };
                showEditFolderModal.value = true;
            }
        }
    } catch (error) {
        console.error('Error finding folder:', error);
        showError('Failed to load folder details');
    }
};

// Update folder
const updateFolder = async () => {
    if (!editFolder.value.folderId || !editFolder.value.newClassId || !editFolder.value.newName.trim()) return;

    isUpdating.value = true;
    try {
        const selectedClass = allClasses.value.find(c => c.id === editFolder.value.newClassId);
        
        const response = await fetch(`/api/portfolio/folders/${editFolder.value.folderId}/`, {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                name: editFolder.value.newName.trim(),
                class_name: selectedClass?.name || 'General'
            })
        });

        if (response.ok) {
            showSuccess('Folder updated successfully');
            showEditFolderModal.value = false;
            await loadSubjectsForClasses();
            
            // Dispatch event to update sidebar
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

// Confirm delete folder
const confirmDeleteFolder = (classItem, subject) => {
    folderToDelete.value = { classItem, subject };
    showDeleteDialog.value = true;
};

// Delete folder
const deleteFolder = async () => {
    if (!folderToDelete.value) return;

    isDeleting.value = true;
    try {
        // Find the folder ID
        const response = await fetch('/api/portfolio/folders/', {
            credentials: 'include',
            headers: { 'Accept': 'application/json' }
        });

        if (response.ok) {
            const folders = await response.json();
            const folder = folders.find(f => 
                f.classroom === folderToDelete.value.classItem.id && 
                f.name === folderToDelete.value.subject
            );

            if (folder) {
                const deleteResponse = await fetch(`/api/portfolio/folders/${folder.id}/`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken': getCsrfToken()
                    }
                });

                if (deleteResponse.ok) {
                    showSuccess('Folder deleted successfully');
                    showDeleteDialog.value = false;
                    folderToDelete.value = null;
                    await loadSubjectsForClasses();
                    
                    // Dispatch event to update sidebar
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

// Navigate to subject
const navigateToSubject = (classItem, subject) => {
    localStorage.setItem('digiportal_selected_class', JSON.stringify(classItem));
    localStorage.setItem('digiportal_selected_subject', subject);
    
    window.dispatchEvent(new CustomEvent('subjectChanged', {
        detail: { classItem, subject }
    }));
    
    emit('navigate', 'TeacherRoom');
};

onMounted(() => {
    loadClassrooms();
});
</script>
