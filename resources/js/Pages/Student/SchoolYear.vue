<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6">
        <!-- Header -->
        <div class="max-w-4xl mx-auto mb-8">
            <h1 class="text-3xl font-bold text-gray-800">School Year</h1>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="flex justify-center items-center py-20">
            <div class="text-center">
                <div class="animate-spin rounded-full h-16 w-16 border-4 border-indigo-600 border-t-transparent mx-auto mb-4"></div>
                <p class="text-gray-600">Loading...</p>
            </div>
        </div>

        <div v-else class="max-w-4xl mx-auto space-y-6">
            <!-- Current Classroom Section -->
            <div v-if="hasClassroom" class="bg-white rounded-2xl shadow-lg overflow-hidden">
                <div class="bg-gradient-to-r from-indigo-600 to-purple-600 p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-indigo-100 text-sm">Current Classroom</p>
                            <h2 class="text-2xl font-bold text-white">{{ currentClassroom?.name }}</h2>
                        </div>
                        <div class="text-right">
                            <p class="text-indigo-100 text-sm">School Year</p>
                            <p class="text-xl font-semibold text-white">{{ currentClassroom?.school_year }}</p>
                        </div>
                    </div>
                </div>
                
                <div class="p-6">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                        <div class="text-center p-4 bg-gray-50 rounded-lg">
                            <p class="text-2xl font-bold text-indigo-600">{{ currentClassroom?.grade_level }}</p>
                            <p class="text-sm text-gray-600">Grade Level</p>
                        </div>
                        <div class="text-center p-4 bg-gray-50 rounded-lg">
                            <p class="text-2xl font-bold text-purple-600">{{ currentClassroom?.section }}</p>
                            <p class="text-sm text-gray-600">Section</p>
                        </div>
                        <div class="text-center p-4 bg-gray-50 rounded-lg col-span-2">
                            <p class="text-lg font-semibold text-gray-800">{{ currentClassroom?.teacher_name || 'Not assigned' }}</p>
                            <p class="text-sm text-gray-600">Class Teacher</p>
                        </div>
                    </div>

                    <!-- Archive Button -->
                    <div class="border-t pt-6">
                        <div class="flex items-start gap-4 p-4 bg-amber-50 border border-amber-200 rounded-lg mb-4">
                            <i class="pi pi-info-circle text-amber-600 text-xl mt-0.5"></i>
                            <div>
                                <p class="font-medium text-amber-800">Ready for a new school year?</p>
                                <p class="text-sm text-amber-700 mt-1">Archive your current school year to join a new classroom. Your history will be saved.</p>
                            </div>
                        </div>
                        <button @click="showArchiveConfirm = true"
                            class="w-full flex items-center justify-center gap-2 px-6 py-3 bg-amber-500 text-white rounded-xl font-semibold hover:bg-amber-600 transition-all">
                            <i class="pi pi-history"></i>
                            <span>Archive School Year</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- No Classroom - Join Section -->
            <div v-else class="bg-white rounded-2xl shadow-lg overflow-hidden">
                <div class="bg-gradient-to-r from-indigo-600 to-purple-600 p-6">
                    <div class="flex items-center gap-4">
                        <div class="w-14 h-14 bg-white/20 rounded-xl flex items-center justify-center">
                            <i class="pi pi-sign-in text-2xl text-white"></i>
                        </div>
                        <div>
                            <h2 class="text-2xl font-bold text-white">Join a Classroom</h2>
                            <p class="text-indigo-100">Enter the class code provided by your teacher</p>
                        </div>
                    </div>
                </div>
                
                <div class="p-6">
                    <!-- Class Code Input -->
                    <div class="mb-6">
                        <label class="block text-sm font-medium text-gray-700 mb-2">Class Code</label>
                        <div class="flex gap-3">
                            <InputText 
                                v-model="classCode" 
                                placeholder="Enter 6-character code (e.g., AbC123)"
                                class="flex-1 text-lg tracking-widest"
                                :class="{ 'p-invalid': codeError }"
                                maxlength="6"
                                @input="validateCode"
                            />
                            <Button 
                                label="Validate" 
                                icon="pi pi-search"
                                @click="validateClassCode"
                                :loading="isValidating"
                                :disabled="classCode.length !== 6"
                                class="bg-indigo-600 hover:bg-indigo-700"
                            />
                        </div>
                        <p v-if="codeError" class="text-red-500 text-sm mt-2">
                            <i class="pi pi-exclamation-circle mr-1"></i>{{ codeError }}
                        </p>
                    </div>

                    <!-- Validated Classroom Preview -->
                    <div v-if="validatedClassroom" class="p-4 bg-indigo-50 border-2 border-indigo-200 rounded-xl">
                        <div class="flex items-center gap-2 mb-3">
                            <i class="pi pi-check-circle text-indigo-600"></i>
                            <span class="font-semibold text-indigo-800">Classroom Found!</span>
                        </div>
                        <div class="grid grid-cols-2 gap-4 text-sm">
                            <div>
                                <p class="text-gray-600">Classroom</p>
                                <p class="font-semibold text-gray-800">{{ validatedClassroom.name }}</p>
                            </div>
                            <div>
                                <p class="text-gray-600">School Year</p>
                                <p class="font-semibold text-gray-800">{{ validatedClassroom.school_year }}</p>
                            </div>
                            <div>
                                <p class="text-gray-600">Teacher</p>
                                <p class="font-semibold text-gray-800">{{ validatedClassroom.teacher_name || 'Not assigned' }}</p>
                            </div>
                            <div>
                                <p class="text-gray-600">Students</p>
                                <p class="font-semibold text-gray-800">{{ validatedClassroom.student_count }} enrolled</p>
                            </div>
                        </div>
                        
                        <button @click="showJoinConfirm = true"
                            class="w-full mt-4 flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition-all">
                            <i class="pi pi-check"></i>
                            <span>Join This Classroom</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- School Year History -->
            <div v-if="history.length > 0" class="bg-white rounded-2xl shadow-lg overflow-hidden">
                <div class="p-6 border-b border-gray-200">
                    <div class="flex items-center gap-3">
                        <i class="pi pi-history text-gray-600"></i>
                        <h3 class="text-lg font-semibold text-gray-800">School Year History</h3>
                        <span class="px-2 py-0.5 bg-gray-100 text-gray-600 text-sm rounded-full">{{ history.length }}</span>
                    </div>
                </div>
                <div class="divide-y divide-gray-100">
                    <div v-for="item in history" :key="item.id" class="p-4 hover:bg-gray-50 transition-all">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-4">
                                <div class="w-12 h-12 bg-gradient-to-br from-gray-400 to-gray-500 rounded-lg flex items-center justify-center text-white font-bold">
                                    {{ item.section }}
                                </div>
                                <div>
                                    <p class="font-semibold text-gray-800">{{ item.classroom_name }}</p>
                                    <p class="text-sm text-gray-600">{{ item.teacher_name || 'Teacher not recorded' }}</p>
                                </div>
                            </div>
                            <div class="flex items-center gap-4">
                                <div class="text-right">
                                    <p class="font-medium text-indigo-600">{{ item.school_year }}</p>
                                    <p class="text-xs text-gray-500">Archived {{ formatDate(item.archived_at) }}</p>
                                </div>
                                <button @click="confirmViewArchived(item)"
                                    class="flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all"
                                    :class="item.classroom_id 
                                        ? 'bg-indigo-100 text-indigo-700 hover:bg-indigo-200' 
                                        : 'bg-gray-100 text-gray-400 cursor-not-allowed'"
                                    :disabled="!item.classroom_id"
                                    :title="item.classroom_id ? 'View archived data' : 'Classroom no longer exists'">
                                    <i class="pi pi-eye text-sm"></i>
                                    <span>View</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Archive Confirmation Dialog -->
        <Dialog v-model:visible="showArchiveConfirm" modal header="Archive School Year" :style="{ width: '450px' }">
            <div class="p-4">
                <div class="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                    <i class="pi pi-exclamation-triangle text-2xl text-amber-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">Are you sure you want to archive this school year?</p>
                        <p class="text-gray-600 text-sm mt-2">
                            You will leave <strong>{{ currentClassroom?.name }}</strong> and need to join a new classroom using a class code.
                        </p>
                        <p class="text-amber-700 text-sm mt-2">Your school year history will be saved.</p>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <Button label="Cancel" severity="secondary" @click="showArchiveConfirm = false" />
                    <Button label="Archive & Leave" severity="warning" @click="archiveSchoolYear" :loading="isArchiving" />
                </div>
            </template>
        </Dialog>

        <!-- Join Confirmation Dialog -->
        <Dialog v-model:visible="showJoinConfirm" modal header="Join Classroom" :style="{ width: '450px' }">
            <div class="p-4">
                <div class="flex items-start gap-3 p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
                    <i class="pi pi-check-circle text-2xl text-indigo-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">Confirm joining this classroom?</p>
                        <p class="text-gray-600 text-sm mt-2">
                            You will be enrolled in <strong>{{ validatedClassroom?.name }}</strong> for school year <strong>{{ validatedClassroom?.school_year }}</strong>.
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <Button label="Cancel" severity="secondary" @click="showJoinConfirm = false" />
                    <Button label="Join Classroom" @click="joinClassroom" :loading="isJoining" class="bg-indigo-600 hover:bg-indigo-700" />
                </div>
            </template>
        </Dialog>

        <!-- View Archived History Modal -->
        <Dialog v-model:visible="showArchivedModal" modal :header="archivedModalTitle" :style="{ width: '800px' }">
            <div class="p-2">
                <!-- Archived Info Banner -->
                <div class="mb-4 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                    <div class="flex items-center gap-3">
                        <i class="pi pi-history text-amber-600 text-xl"></i>
                        <div>
                            <p class="font-semibold text-amber-800">Viewing Archived School Year</p>
                            <p class="text-sm text-amber-700">{{ selectedArchivedItem?.classroom_name }} • {{ selectedArchivedItem?.school_year }}</p>
                        </div>
                    </div>
                </div>

                <!-- Loading State -->
                <div v-if="isLoadingArchived" class="flex justify-center items-center py-12">
                    <div class="text-center">
                        <div class="animate-spin rounded-full h-10 w-10 border-4 border-indigo-600 border-t-transparent mx-auto mb-3"></div>
                        <p class="text-gray-600">Loading archived data...</p>
                    </div>
                </div>

                <!-- Archived Content -->
                <div v-else>
                    <!-- Stats Summary -->
                    <div class="grid grid-cols-3 gap-4 mb-6">
                        <div class="text-center p-4 bg-indigo-50 rounded-lg">
                            <p class="text-2xl font-bold text-indigo-600">{{ archivedSubmissions.length }}</p>
                            <p class="text-sm text-gray-600">Submissions</p>
                        </div>
                        <div class="text-center p-4 bg-green-50 rounded-lg">
                            <p class="text-2xl font-bold text-green-600">{{ archivedStats.graded }}</p>
                            <p class="text-sm text-gray-600">Graded</p>
                        </div>
                        <div class="text-center p-4 bg-purple-50 rounded-lg">
                            <p class="text-2xl font-bold text-purple-600">{{ archivedStats.averageScore }}</p>
                            <p class="text-sm text-gray-600">Avg Score</p>
                        </div>
                    </div>

                    <!-- No Submissions -->
                    <div v-if="archivedSubmissions.length === 0" class="text-center py-12">
                        <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <i class="pi pi-inbox text-2xl text-gray-400"></i>
                        </div>
                        <p class="text-gray-500">No submissions found for this school year</p>
                    </div>

                    <!-- Submissions List -->
                    <div v-else class="space-y-3 max-h-96 overflow-y-auto">
                        <div v-for="submission in archivedSubmissions" :key="submission.id"
                            class="p-4 bg-gray-50 rounded-lg border border-gray-200 hover:border-indigo-300 transition-all">
                            <div class="flex items-start justify-between">
                                <div class="flex-1">
                                    <p class="font-semibold text-gray-800">{{ submission.activity_title }}</p>
                                    <p class="text-sm text-gray-600">{{ submission.folder_name }}</p>
                                    <p class="text-xs text-gray-500 mt-1">Submitted: {{ formatDate(submission.submitted_at) }}</p>
                                </div>
                                <div class="text-right">
                                    <span v-if="submission.score !== null" 
                                        class="inline-block px-3 py-1 rounded-full text-sm font-semibold"
                                        :class="submission.score >= 80 ? 'bg-green-100 text-green-700' : submission.score >= 60 ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'">
                                        {{ submission.score }}%
                                    </span>
                                    <span v-else class="inline-block px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm">
                                        Not graded
                                    </span>
                                    <p class="text-xs text-gray-500 mt-1 capitalize">{{ submission.status }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end">
                    <Button label="Close" severity="secondary" @click="showArchivedModal = false" />
                </div>
            </template>
        </Dialog>

        <!-- View Archived Confirmation Dialog -->
        <Dialog v-model:visible="showViewArchivedConfirm" modal header="View Archived School Year" :style="{ width: '450px' }">
            <div class="p-4">
                <div class="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                    <i class="pi pi-eye text-2xl text-amber-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">You are about to view archived data</p>
                        <p class="text-gray-600 text-sm mt-2">
                            School Year: <strong class="text-amber-700">{{ selectedArchivedForView?.school_year }}</strong>
                        </p>
                        <p class="text-gray-600 text-sm">
                            Classroom: <strong class="text-amber-700">{{ selectedArchivedForView?.classroom_name }}</strong>
                        </p>
                        <p class="text-gray-600 text-sm mt-2">This will switch to read-only mode where you can browse your archived activities and submissions.</p>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-3">
                    <Button label="Cancel" severity="secondary" @click="showViewArchivedConfirm = false" />
                    <Button label="View Archived" @click="enterArchivedViewMode(selectedArchivedForView)" class="bg-amber-500 hover:bg-amber-600" />
                </div>
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import { useToast } from '../../composables/useToast';

const { showSuccess, showError } = useToast();

// State
const isLoading = ref(true);
const hasClassroom = ref(false);
const currentClassroom = ref(null);
const history = ref([]);
const classCode = ref('');
const codeError = ref('');
const validatedClassroom = ref(null);
const isValidating = ref(false);
const isArchiving = ref(false);
const isJoining = ref(false);
const showArchiveConfirm = ref(false);
const showJoinConfirm = ref(false);

// Archived view state
const showArchivedModal = ref(false);
const selectedArchivedItem = ref(null);
const archivedSubmissions = ref([]);
const isLoadingArchived = ref(false);
const archivedModalTitle = ref('Archived School Year');
const showViewArchivedConfirm = ref(false);
const selectedArchivedForView = ref(null);
const archivedStats = ref({
    graded: 0,
    averageScore: 'N/A'
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

const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
};

// Load school year info
const loadSchoolYearInfo = async () => {
    isLoading.value = true;
    try {
        const response = await fetch('/api/student/school-year/', {
            credentials: 'include',
            headers: { 'Accept': 'application/json' }
        });
        
        if (response.ok) {
            const data = await response.json();
            hasClassroom.value = data.has_classroom;
            currentClassroom.value = data.current_classroom;
            history.value = data.history || [];
            console.log('✅ School year info loaded:', data);
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to load school year info');
        }
    } catch (error) {
        console.error('Error loading school year info:', error);
        showError('Failed to load school year info');
    } finally {
        isLoading.value = false;
    }
};

// Validate input
const validateCode = () => {
    classCode.value = classCode.value.replace(/[^a-zA-Z0-9]/g, '');
    codeError.value = '';
    validatedClassroom.value = null;
};

// Validate class code
const validateClassCode = async () => {
    if (classCode.value.length !== 6) {
        codeError.value = 'Class code must be 6 characters';
        return;
    }
    
    isValidating.value = true;
    codeError.value = '';
    validatedClassroom.value = null;
    
    try {
        const response = await fetch(`/api/classroom/validate-code/?code=${classCode.value}`, {
            credentials: 'include',
            headers: { 'Accept': 'application/json' }
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.valid) {
                if (data.classroom.is_archived) {
                    codeError.value = 'This classroom is archived and no longer accepting students.';
                } else {
                    validatedClassroom.value = data.classroom;
                }
            }
        } else {
            const error = await response.json();
            codeError.value = error.error || 'Invalid class code. Please check and try again.';
        }
    } catch (error) {
        console.error('Error validating code:', error);
        codeError.value = 'Failed to validate code. Please try again.';
    } finally {
        isValidating.value = false;
    }
};

// Archive school year
const archiveSchoolYear = async () => {
    isArchiving.value = true;
    try {
        const response = await fetch('/api/student/school-year/archive/', {
            method: 'POST',
            credentials: 'include',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() 
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            showSuccess(data.message || 'School year archived successfully');
            showArchiveConfirm.value = false;
            
            // Reload data
            await loadSchoolYearInfo();
            
            // Dispatch event to update sidebar
            window.dispatchEvent(new CustomEvent('studentClassroomChanged', { 
                detail: { hasClassroom: false } 
            }));
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to archive school year');
        }
    } catch (error) {
        console.error('Error archiving school year:', error);
        showError('Failed to archive school year');
    } finally {
        isArchiving.value = false;
    }
};

// Join classroom
const joinClassroom = async () => {
    if (!validatedClassroom.value) return;
    
    isJoining.value = true;
    try {
        const response = await fetch('/api/student/classroom/join/', {
            method: 'POST',
            credentials: 'include',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() 
            },
            body: JSON.stringify({ class_code: classCode.value })
        });
        
        if (response.ok) {
            const data = await response.json();
            showSuccess(data.message || 'Successfully joined classroom');
            showJoinConfirm.value = false;
            classCode.value = '';
            validatedClassroom.value = null;
            
            // Reload data
            await loadSchoolYearInfo();
            
            // Dispatch event to update sidebar
            window.dispatchEvent(new CustomEvent('studentClassroomChanged', { 
                detail: { hasClassroom: true, classroom: data.classroom } 
            }));
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to join classroom');
        }
    } catch (error) {
        console.error('Error joining classroom:', error);
        showError('Failed to join classroom');
    } finally {
        isJoining.value = false;
    }
};

// View archived history
const viewArchivedHistory = async (item) => {
    selectedArchivedItem.value = item;
    archivedModalTitle.value = `${item.classroom_name} - ${item.school_year}`;
    showArchivedModal.value = true;
    isLoadingArchived.value = true;
    archivedSubmissions.value = [];
    archivedStats.value = { graded: 0, averageScore: 'N/A' };
    
    try {
        const response = await fetch(`/api/student/archived-submissions/?school_year=${encodeURIComponent(item.school_year)}&classroom_id=${item.classroom_id}`, {
            credentials: 'include',
            headers: { 'Accept': 'application/json' }
        });
        
        if (response.ok) {
            const data = await response.json();
            archivedSubmissions.value = data.submissions || [];
            
            // Calculate stats
            const graded = archivedSubmissions.value.filter(s => s.score !== null);
            archivedStats.value.graded = graded.length;
            
            if (graded.length > 0) {
                const totalScore = graded.reduce((sum, s) => sum + s.score, 0);
                archivedStats.value.averageScore = Math.round(totalScore / graded.length) + '%';
            }
            
            console.log('✅ Loaded archived submissions:', data);
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to load archived data');
        }
    } catch (error) {
        console.error('Error loading archived data:', error);
        showError('Failed to load archived data');
    } finally {
        isLoadingArchived.value = false;
    }
};

// Show confirmation dialog before entering archived view mode
const confirmViewArchived = (item) => {
    selectedArchivedForView.value = item;
    showViewArchivedConfirm.value = true;
};

// Enter archived view mode (like teacher's archived view)
const enterArchivedViewMode = (item) => {
    showViewArchivedConfirm.value = false;
    console.log('📂 Entering student archived view mode:', item);
    
    // Check if classroom_id exists
    if (!item.classroom_id) {
        showError('Cannot view archived data: The classroom no longer exists.');
        return;
    }
    
    // Store archived school year info in localStorage
    const archivedData = {
        id: item.id,
        name: item.school_year,
        classroom_id: item.classroom_id,
        classroom_name: item.classroom_name,
        section: item.section,
        grade_level: item.grade_level,
        teacher_name: item.teacher_name,
        archived_at: item.archived_at
    };
    localStorage.setItem('student_viewing_archived_school_year', JSON.stringify(archivedData));
    
    // Save the target page to localStorage so App.vue can navigate
    localStorage.setItem('digiportal_current_page', 'StudentRoom');
    
    // Dispatch event to MainLayout to enter archived view mode
    window.dispatchEvent(new CustomEvent('studentArchivedViewModeChanged', { 
        detail: { 
            isViewing: true, 
            schoolYear: archivedData,
            classroom: {
                id: item.classroom_id,
                name: item.classroom_name,
                section: item.section,
                grade_level: item.grade_level
            }
        } 
    }));
    
    showSuccess(`Viewing archived data for ${item.school_year}`);
    
    // Reload the page to navigate to StudentRoom with archived view mode
    window.location.reload();
};

onMounted(() => {
    loadSchoolYearInfo();
});
</script>
