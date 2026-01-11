<template>
  <div class="flex flex-col">
    <!-- Header -->
    <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 shadow-lg rounded-t-xl h-40 md:h-36 flex flex-col justify-center px-6 md:px-8">
      <div class="flex items-center gap-3">
        <h1 class="text-3xl md:text-4xl font-bold text-white flex items-center gap-3">
          <i class="pi pi-comments"></i>
          Remarks Management
        </h1>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="w-full bg-white/80 flex-1">
      <!-- Content Area -->
      <div class="w-full px-4 sm:px-6 pt-4 pb-6 transition-all duration-300"
           :style="{ 'padding-left': '1.5rem', 'padding-right': '1.5rem' }">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Pupil List -->
          <div class="lg:col-span-1">
            <div class="bg-white/95 rounded-xl border-2 border-indigo-100 overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300">
              <div class="bg-gradient-to-r from-indigo-50 to-violet-50 p-4 border-b-2 border-indigo-100">
                <div class="flex items-center justify-between gap-3">
                  <h3 class="text-lg font-bold text-indigo-900 flex items-center gap-2 whitespace-nowrap">
                    <i class="pi pi-users text-indigo-600"></i>
                    Pupils List
                  </h3>
                  <Dropdown
                    v-model="selectedClassroom"
                    :options="classrooms"
                    optionLabel="name"
                    placeholder="Select Class"
                    class="flex-1 max-w-[160px]"
                    @change="onClassroomChange"
                  >
                    <template #value="slotProps">
                      <div v-if="slotProps.value" class="flex items-center gap-1">
                        <span class="font-medium text-sm">{{ slotProps.value.name }}</span>
                      </div>
                      <span v-else class="text-gray-500 text-sm">Select Class</span>
                    </template>
                    <template #option="slotProps">
                      <div class="flex items-center justify-between w-full gap-2">
                        <span class="font-medium">{{ slotProps.option.name }}</span>
                        <span class="text-xs text-indigo-600 bg-indigo-100 px-2 py-0.5 rounded-full">{{ slotProps.option.student_count }}</span>
                      </div>
                    </template>
                  </Dropdown>
                </div>
                <!-- Selected Class Indicator -->
                <div v-if="selectedClassroom" class="mt-2 flex items-center gap-2">
                  <span class="text-xs font-semibold bg-indigo-600 text-white px-3 py-1 rounded-full flex items-center gap-1">
                    <i class="pi pi-bookmark-fill text-xs"></i>
                    {{ selectedClassroom.name }} • {{ selectedClassroom.student_count }} students
                  </span>
                </div>
              </div>
              <!-- Search Bar -->
              <div class="p-4 border-b border-indigo-100">
                <div class="relative">
                  <i class="pi pi-search absolute left-3 top-1/2 transform -translate-y-1/2 text-indigo-400"></i>
                  <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Search students..."
                    class="w-full pl-10 pr-4 py-2 border-2 border-indigo-200 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-300 focus:outline-none transition-all"
                  />
                </div>
              </div>
              <div class="p-4 max-h-[600px] overflow-y-auto">
                <div v-if="isLoadingStudents" class="flex justify-center items-center py-8">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                </div>
                <div v-else-if="filteredStudents.length === 0" class="text-center py-8">
                  <i class="pi pi-users text-4xl text-gray-300 mb-3"></i>
                  <p class="text-gray-500">No students found</p>
                  <p v-if="selectedClassroom" class="text-sm text-gray-400 mt-1">Try selecting a different class</p>
                </div>
                <ul v-else class="space-y-2">
                  <li v-for="student in filteredStudents"
                      :key="student.id"
                      @click="selectStudent(student)"
                      class="flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all duration-200 border-2"
                      :class="[
                        selectedStudent?.id === student.id
                          ? 'bg-gradient-to-r from-indigo-100 to-violet-100 border-indigo-400 shadow-md scale-105'
                          : 'hover:bg-indigo-50 border-transparent hover:border-indigo-200 hover:shadow-sm',
                      ]">
                    <div class="flex items-center gap-3">
                      <div class="bg-gradient-to-br from-indigo-600 to-violet-600 text-white font-bold w-10 h-10 flex items-center justify-center rounded-full shadow-md ring-2 ring-indigo-200 overflow-hidden">
                        <img v-if="student.profile_picture" :src="student.profile_picture" :alt="student.name" class="w-full h-full object-cover" />
                        <span v-else>{{ student.initial }}</span>
                      </div>
                      <div>
                        <span class="font-semibold text-indigo-900 block">{{ student.name }}</span>
                      </div>
                    </div>
                    <i class="pi pi-chevron-right text-indigo-400"></i>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Remarks Section -->
          <div class="lg:col-span-2 bg-white/95 rounded-xl border-2 border-indigo-100 overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300">
            <div class="bg-gradient-to-r from-indigo-50 to-violet-50 p-4 border-b-2 border-indigo-100">
              <div class="flex items-center justify-between">
                <h3 v-if="selectedStudent" class="text-lg font-bold text-indigo-900 flex items-center gap-2">
                  <i class="pi pi-comments text-indigo-600"></i>
                  Remarks for {{ selectedStudent.name }}
                </h3>
                <h3 v-else class="text-lg font-bold text-center text-indigo-600 w-full flex items-center justify-center gap-2">
                  <i class="pi pi-hand-pointer"></i>
                  Select a student to view remarks
                </h3>
                <div v-if="selectedStudent" class="flex gap-2">
                  <button
                    @click="showAddRemarkDialog = true"
                    class="flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200
                           bg-gradient-to-r from-indigo-600 to-blue-600 text-white shadow-sm hover:from-indigo-700 hover:to-blue-700
                           focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                    <i class="pi pi-plus"></i>
                    <span>Add Remark</span>
                  </button>
                </div>
              </div>
            </div>

            <div class="p-4">
              <div v-if="selectedStudent" class="space-y-4">
                <!-- Add Remark Section -->
                <div class="bg-gradient-to-br from-indigo-50 to-violet-50 p-4 rounded-xl border-2 border-indigo-200 shadow-sm">
                  <Textarea
                    v-model="newRemark"
                    rows="3"
                    placeholder="Enter new remark..."
                    class="w-full border-2 border-indigo-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-300 rounded-lg shadow-sm"/>
                </div>

                <!-- Remarks List -->
                <div class="space-y-3">
                  <div v-for="remark in selectedStudent.remarks"
                       :key="remark.id"
                       class="bg-white p-4 rounded-xl border-2 border-indigo-100 hover:shadow-md transition-all duration-200 hover:border-indigo-300 relative group hover:scale-[1.02]">
                    <div class="flex items-center justify-between mb-2">
                      <div class="flex flex-col">
                        <span class="text-sm text-indigo-700/80">{{ remark.date }}</span>
                        <span v-if="remark.time" class="text-xs text-indigo-600/60">{{ remark.time }}</span>
                      </div>
                      <Button
                        icon="pi pi-ellipsis-v"
                        class="p-button-text p-button-rounded p-button-plain h-8 w-8 flex items-center justify-center text-indigo-600 hover:bg-indigo-100 transition-colors duration-200"
                        @click="toggleRemarkMenu(remark.id)"
                        v-tooltip.top="'More options'"
                      />
                      <div v-if="activeMenu === remark.id" class="absolute right-2 bottom-10 bg-white shadow-lg rounded-md border border-gray-200 z-10 w-40 py-1">
                        <button @click="editRemark(remark)" class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-indigo-50">
                          Edit
                        </button>
                        <button @click="confirmDelete(remark)" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50">
                          Delete
                        </button>
                      </div>
                    </div>
                    <div v-if="editingRemarkId === remark.id" class="flex items-center gap-2 mt-2">
                      <Textarea
                        v-model="editText"
                        rows="2"
                        class="flex-1 text-sm"
                        autoResize
                      />
                      <div class="flex gap-1">
                        <Button
                          icon="pi pi-check"
                          class="p-button-sm"
                          @click="saveEdit(remark)"
                          :disabled="!editText.trim()"
                          style="background: linear-gradient(to right, #4f46e5, #6366f1); border: none;"
                        />
                        <Button
                          icon="pi pi-times"
                          class="p-button-sm p-button-text p-button-danger"
                          @click="cancelEdit()"
                        />
                      </div>
                    </div>
                    <p v-else class="text-indigo-900 pr-6 whitespace-pre-wrap">{{ remark.text }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Add Remark Confirmation Dialog -->
  <Dialog
    v-model:visible="showAddRemarkDialog"
    :style="{ width: '450px' }"
    header="Confirm Add Remark"
    :modal="true"
  >
    <div class="flex items-center gap-4">
      <i class="pi pi-question-circle text-indigo-500" style="font-size: 2rem" />
      <span>Are you sure you want to add this remark for {{ selectedStudent?.name }}?</span>
    </div>
    <template #footer>
      <Button
        label="Cancel"
        @click="showAddRemarkDialog = false"
        class="p-button-secondary"
      />
      <Button
        label="Add Remark"
        @click="confirmAddRemark"
        style="background: linear-gradient(to right, #4f46e5, #6366f1); border: none;"
        :disabled="!newRemark.trim()"
      />
    </template>
  </Dialog>

  <!-- Delete Confirmation Dialog -->
  <Dialog
    v-model:visible="showDeleteDialog"
    :style="{ width: '450px' }"
    header="Confirm Deletion"
    :modal="true"
  >
    <div class="flex items-center gap-4">
      <i class="pi pi-exclamation-triangle text-yellow-500" style="font-size: 2rem" />
      <span>Are you sure you want to delete this remark? This action cannot be undone.</span>
    </div>
    <template #footer>
      <Button
        label="Cancel"
        @click="showDeleteDialog = false"
        class="p-button-secondary"
        style="background: linear-gradient(to right, #4f46e5, #6366f1); border: none; color: white;"
      />
      <Button
        label="Delete"
        @click="deleteRemark"
        class="p-button-danger"
      />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import axios from 'axios';
import { useToast } from '../../composables/useToast';

// Define emits for navigation
const emit = defineEmits(['navigate']);

// Initialize toast
const { showSuccess, showError, showInfo, showWarning } = useToast();
import Button from "primevue/button";
import Textarea from "primevue/textarea";
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';

const students = ref([]);
const classrooms = ref([]);
const selectedClassroom = ref(null);
const isLoadingStudents = ref(false);
const searchQuery = ref('');
const showAddRemarkDialog = ref(false);

// Archived View Mode State
const isArchivedViewMode = ref(false);
const viewingArchivedSchoolYear = ref(null);

// Check if in archived view mode
const checkArchivedViewMode = () => {
    const savedArchivedView = localStorage.getItem('viewing_archived_school_year');
    if (savedArchivedView) {
        try {
            viewingArchivedSchoolYear.value = JSON.parse(savedArchivedView);
            isArchivedViewMode.value = true;
            console.log('📂 Remarks: Archived view mode:', viewingArchivedSchoolYear.value?.name);
        } catch (e) {
            isArchivedViewMode.value = false;
            viewingArchivedSchoolYear.value = null;
        }
    } else {
        isArchivedViewMode.value = false;
        viewingArchivedSchoolYear.value = null;
    }
};

// Handle archived view mode change event
const handleArchivedViewModeChange = (event) => {
    const { isViewing, schoolYear } = event.detail;
    isArchivedViewMode.value = isViewing;
    viewingArchivedSchoolYear.value = schoolYear;
    console.log('📂 Remarks: Archived view mode changed:', isViewing, schoolYear?.name);
    // Reload data with new filter
    loadClassrooms();
};

// Load classrooms for dropdown - includes assigned classroom + classrooms with folders
const loadClassrooms = async () => {
  try {
    // Build URL with school year filter if in archived view mode
    let classroomsUrl = '/api/classrooms/';
    let foldersUrl = '/api/portfolio/folders/?current_school_year=true';
    
    if (isArchivedViewMode.value && viewingArchivedSchoolYear.value?.name) {
        classroomsUrl += `?school_year=${encodeURIComponent(viewingArchivedSchoolYear.value.name)}`;
        foldersUrl = `/api/portfolio/folders/?school_year=${encodeURIComponent(viewingArchivedSchoolYear.value.name)}`;
        console.log('📂 Remarks: Loading archived classrooms for school year:', viewingArchivedSchoolYear.value.name);
    }
    
    // First, get teacher's assigned classrooms
    const assignedResponse = await axios.get(classroomsUrl);
    let assignedClassrooms = [];
    if (assignedResponse.data && assignedResponse.data.classrooms) {
      assignedClassrooms = assignedResponse.data.classrooms;
    }
    
    // Then, get classrooms where teacher has folders (from ManageClass)
    const foldersResponse = await axios.get(foldersUrl);
    let folderClassroomIds = new Set();
    if (foldersResponse.data) {
      foldersResponse.data.forEach(folder => {
        if (folder.classroom) {
          folderClassroomIds.add(folder.classroom);
        }
      });
    }
    
    // Build classroom map - assigned classrooms first
    const classroomMap = new Map();
    assignedClassrooms.forEach(c => {
      classroomMap.set(c.id, {
        id: c.id,
        name: c.name,
        student_count: c.students?.length || c.historical_student_count || 0,
        isAssigned: true,
        isArchived: c.is_archived || false
      });
    });
    
    // Add classrooms from folders that aren't already in the map
    for (const classroomId of folderClassroomIds) {
      if (!classroomMap.has(classroomId)) {
        try {
          const classroomResponse = await axios.get(`/api/classrooms/${classroomId}/`);
          // In archived view mode, include archived classrooms; otherwise exclude them
          const shouldInclude = isArchivedViewMode.value 
            ? classroomResponse.data.is_archived 
            : !classroomResponse.data.is_archived;
          
          if (classroomResponse.data && shouldInclude) {
            classroomMap.set(classroomId, {
              id: classroomResponse.data.id,
              name: classroomResponse.data.name,
              student_count: classroomResponse.data.students?.length || classroomResponse.data.historical_student_count || 0,
              isAssigned: false,
              isArchived: classroomResponse.data.is_archived || false
            });
          }
        } catch (err) {
          console.error(`Failed to fetch classroom ${classroomId}:`, err);
        }
      }
    }
    
    // Convert to array - assigned classrooms first, then others
    const allClassrooms = Array.from(classroomMap.values());
    allClassrooms.sort((a, b) => {
      // Assigned classrooms first
      if (a.isAssigned && !b.isAssigned) return -1;
      if (!a.isAssigned && b.isAssigned) return 1;
      // Then sort by name
      return a.name.localeCompare(b.name);
    });
    
    classrooms.value = allClassrooms;
    console.log('📚 Loaded classrooms for remarks:', classrooms.value);
    
    // Auto-select the first classroom (teacher's assigned classroom)
    if (classrooms.value.length > 0 && !selectedClassroom.value) {
      selectedClassroom.value = classrooms.value[0];
      await loadStudents();
    }
  } catch (error) {
    console.error('Error loading classrooms:', error);
  }
};

// Handle classroom change
const onClassroomChange = async () => {
  selectedStudent.value = null; // Clear selected student when changing class
  await loadStudents();
};

// Filtered students based on search query
const filteredStudents = computed(() => {
  if (!searchQuery.value.trim()) {
    return students.value;
  }
  const query = searchQuery.value.toLowerCase();
  return students.value.filter(student =>
    student.name.toLowerCase().includes(query) ||
    student.id.toString().includes(query) ||
    student.student_id?.toLowerCase().includes(query)
  );
});

// Load students from API
const loadStudents = async () => {
  isLoadingStudents.value = true;
  try {
    // Build URL with optional classroom filter
    let url = '/api/students/progress/';
    if (selectedClassroom.value) {
      url += `?classroom_id=${selectedClassroom.value.id}`;
    }
    
    const response = await axios.get(url);
    if (response.data) {
      // Map students without loading remarks initially (load on demand)
      students.value = response.data.map((student) => ({
        id: student.id,
        student_id: student.student_id,
        name: student.name,
        initial: student.name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2),
        username: student.username,
        email: student.email,
        profile_picture: student.profile_picture || null,
        remarks: [] // Will be loaded when student is selected
      }));
      console.log('Loaded students:', students.value.length, selectedClassroom.value ? `for ${selectedClassroom.value.name}` : 'all classes');
    }
  } catch (error) {
    console.error('Error loading students:', error);
    showError('Failed to load students', 'Error');
  } finally {
    isLoadingStudents.value = false;
  }
};

const selectedStudent = ref(null);
const newRemark = ref("");
const activeMenu = ref(null);
const editingRemarkId = ref(null);
const editText = ref("");
const showDeleteDialog = ref(false);
const remarkToDelete = ref(null);

// Close menu when clicking outside
const closeMenu = (event) => {
  if (!event.target.closest('.relative')) {
    activeMenu.value = null;
  }
};

onMounted(() => {
  document.addEventListener('click', closeMenu);
  checkArchivedViewMode();
  loadClassrooms(); // This will auto-select first classroom and load students
  
  // Listen for archived view mode changes
  window.addEventListener('archivedViewModeChanged', handleArchivedViewModeChange);
});

onUnmounted(() => {
  document.removeEventListener('click', closeMenu);
  window.removeEventListener('archivedViewModeChanged', handleArchivedViewModeChange);
});

async function selectStudent(student) {
  selectedStudent.value = student;
  // Load remarks for this student
  await loadStudentRemarks(student.id);
}

const loadStudentRemarks = async (studentId) => {
  try {
    const response = await axios.get(`/api/remarks/?student_id=${studentId}`);
    if (response.data) {
      selectedStudent.value.remarks = response.data.map(remark => {
        const remarkDate = new Date(remark.created_at);
        return {
          id: remark.id,
          date: remarkDate.toLocaleDateString(),
          time: remarkDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          text: remark.text
        };
      });
    }
  } catch (error) {
    console.error('Error loading student remarks:', error);
  }
};

function toggleRemarkMenu(remarkId) {
  activeMenu.value = activeMenu.value === remarkId ? null : remarkId;
}

function editRemark(remark) {
  editingRemarkId.value = remark.id;
  editText.value = remark.text;
  activeMenu.value = null;
}

async function saveEdit(remark) {
  if (!editText.value.trim()) return;

  try {
    const response = await axios.put(`/api/remarks/${remark.id}/`, {
      text: editText.value.trim()
    });

    if (response.data) {
      const remarkDate = new Date(response.data.updated_at);
      const remarkToUpdate = selectedStudent.value.remarks.find(r => r.id === remark.id);
      if (remarkToUpdate) {
        remarkToUpdate.text = response.data.text;
        remarkToUpdate.date = remarkDate.toLocaleDateString();
        remarkToUpdate.time = remarkDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      }

      // Also update in students list
      const studentInList = students.value.find(s => s.id === selectedStudent.value.id);
      if (studentInList && studentInList.remarks) {
        const remarkInList = studentInList.remarks.find(r => r.id === remark.id);
        if (remarkInList) {
          remarkInList.text = response.data.text;
          remarkInList.date = remarkDate.toLocaleDateString();
          remarkInList.time = remarkDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }
      }

      cancelEdit();
      console.log('Remark updated successfully');
    }
  } catch (error) {
    console.error('Error updating remark:', error);
    alert('Failed to update remark. Please try again.');
  }
}

function cancelEdit() {
  editingRemarkId.value = null;
  editText.value = "";
}

function confirmDelete(remark) {
  remarkToDelete.value = remark;
  showDeleteDialog.value = true;
  activeMenu.value = null;
}

async function deleteRemark() {
  if (remarkToDelete.value) {
    try {
      await axios.delete(`/api/remarks/${remarkToDelete.value.id}/`);

      // Remove from selected student's remarks
      selectedStudent.value.remarks = selectedStudent.value.remarks.filter(
        r => r.id !== remarkToDelete.value.id
      );

      // Update the student in the students list to reflect the new count
      const studentInList = students.value.find(s => s.id === selectedStudent.value.id);
      if (studentInList && studentInList.remarks) {
        studentInList.remarks = studentInList.remarks.filter(
          r => r.id !== remarkToDelete.value.id
        );
      }

      showDeleteDialog.value = false;
      remarkToDelete.value = null;
      console.log('Remark deleted successfully');
    } catch (error) {
      console.error('Error deleting remark:', error);
      alert('Failed to delete remark. Please try again.');
      showDeleteDialog.value = false;
    }
  }
}

async function confirmAddRemark() {
  if (selectedStudent.value && newRemark.value.trim()) {
    try {
      const response = await axios.post('/api/remarks/', {
        student: selectedStudent.value.id,
        text: newRemark.value.trim()
      });

      if (response.data) {
        const remarkDate = new Date(response.data.created_at);
        const newRemarkData = {
          id: response.data.id,
          date: remarkDate.toLocaleDateString(),
          time: remarkDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          text: response.data.text
        };

        // Reload remarks for the selected student to get fresh data from server
        await loadStudentRemarks(selectedStudent.value.id);

        newRemark.value = "";
        showAddRemarkDialog.value = false;
        showSuccess('Remark saved successfully!', 'Saved');
      }
    } catch (error) {
      console.error('Error adding remark:', error);
      showError(error.response?.data?.error || error.message, 'Save Failed');
      showAddRemarkDialog.value = false;
    }
  }
}
</script>


<style scoped>
/* Theme variables */
:root {
  --theme-indigo: #4f46e5;
  --theme-violet: #7c3aed;
  --theme-blue: #3b82f6;
  --theme-light: #f5f3ff;
  --theme-dark: #1e1b4b;
}
</style>
