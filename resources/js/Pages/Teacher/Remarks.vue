<template>
  
  <div class="p-4 md:p-6">
    <div class="rounded-2xl shadow-lg bg-white/90 backdrop-blur-sm border border-indigo-100 overflow-hidden">
      <!-- Header -->
      <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-6">
        <h1 class="text-2xl font-bold text-white">Pupil Remarks Management</h1>
      </div>

      <!-- Content -->
      <div class="p-6">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Pupil List -->
          <div class="lg:col-span-1">
            <div class="bg-white/90 rounded-xl border border-indigo-100 overflow-hidden shadow-sm">
              <div class="bg-indigo-50 p-4 border-b border-indigo-100">
                <h3 class="text-lg font-semibold text-indigo-900 flex items-center gap-2">
                  <i class="pi pi-users text-indigo-600"></i>
                  Pupils List
                </h3>
              </div>
              <div class="p-4">
                <ul class="space-y-2">
                  <li v-for="student in students" 
                      :key="student.id" 
                      @click="selectStudent(student)"
                      class="flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all"
                      :class="[
                        selectedStudent?.id === student.id 
                          ? 'bg-indigo-100 border-indigo-300' 
                          : 'hover:bg-indigo-50 border-transparent',
                        'border transition-colors duration-200'
                      ]">
                    <div class="flex items-center gap-3">
                      <div class="bg-indigo-600 text-white font-bold w-8 h-8 flex items-center justify-center rounded-full shadow-sm">
                        {{ student.name.charAt(0) }}
                      </div>
                      <span class="font-medium text-indigo-900">{{ student.name }}</span>
                    </div>
                    <span class="text-sm text-indigo-700/80">{{ student.remarks.length }} remarks</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          
          <!-- Remarks Section -->
          <div class="lg:col-span-2 bg-white/90 rounded-xl border border-indigo-100 overflow-hidden shadow-sm">
            <div class="bg-indigo-50 p-4 border-b border-indigo-100">
              <div class="flex items-center justify-between">
                <h3 v-if="selectedStudent" class="text-lg font-semibold text-indigo-900 flex items-center gap-2">
                  <i class="pi pi-comments text-indigo-600"></i>
                  Remarks for {{ selectedStudent.name }}
                </h3>
                <h3 v-else class="text-lg font-semibold text-center text-indigo-900 w-full">
                  Select a student to view remarks
                </h3>
                <div v-if="selectedStudent" class="flex gap-2">
                  <button 
                    @click="addRemark" 
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
                <div class="bg-white p-4 rounded-lg border border-indigo-100">
                  <Textarea 
                    v-model="newRemark" 
                    rows="3" 
                    placeholder="Enter new remark..." 
                    class="w-full border-indigo-200 focus:border-indigo-500 focus:ring-indigo-500 rounded-md shadow-sm"/>
                </div>

                <!-- Remarks List -->
                <div class="space-y-3">
                  <div v-for="remark in selectedStudent.remarks" 
                       :key="remark.id" 
                       class="bg-white p-4 rounded-lg border border-indigo-100 hover:shadow-sm transition-all hover:border-indigo-200 relative group">
                    <div class="flex items-center justify-between mb-2">
                      <span class="text-sm text-indigo-700/80">{{ remark.date }}</span>
                      <Button 
                        icon="pi pi-ellipsis-v" 
                        class="p-button-text p-button-rounded p-button-plain h-8 w-8 flex items-center justify-center text-indigo-600 hover:bg-indigo-100 transition-colors duration-200"
                        @click="toggleRemarkMenu(remark.id)"
                        v-tooltip.top="'More options'"
                      />
                      <div v-if="activeMenu === remark.id" class="absolute right-2 top-10 bg-white shadow-lg rounded-md border border-gray-200 z-10 w-40 py-1">
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
import { ref, onMounted, onUnmounted } from "vue";
import Button from "primevue/button";
import Textarea from "primevue/textarea";
import Dialog from 'primevue/dialog';

const students = ref([
  { id: 1, name: "Alice Smith", remarks: [
      { id: 1, date: "2024-01-15", text: "Struggling with math concepts" },
      { id: 2, date: "2024-01-14", text: "Seems withdrawn in class" }
  ]},
  { id: 2, name: "Bob Johnson", remarks: [
      { id: 3, date: "2024-01-16", text: "Needs help with reading comprehension" }
  ]},
  { id: 3, name: "Carrol Williams", remarks: [
      { id: 4, date: "2024-01-17", text: "Talks excessively in class" }
  ]},
  { id: 4, name: "David Brown", remarks: [
      { id: 5, date: "2024-01-18", text: "Excellent performance in science" }
  ]},
  { id: 5, name: "Emma Davies", remarks: [
      { id: 6, date: "2024-01-19", text: "Appears anxious before tests" }
  ]}
]);

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
});

onUnmounted(() => {
  document.removeEventListener('click', closeMenu);
});

function selectStudent(student) {
  selectedStudent.value = student;
}

function toggleRemarkMenu(remarkId) {
  activeMenu.value = activeMenu.value === remarkId ? null : remarkId;
}

function editRemark(remark) {
  editingRemarkId.value = remark.id;
  editText.value = remark.text;
  activeMenu.value = null;
}

function saveEdit(remark) {
  const remarkToUpdate = selectedStudent.value.remarks.find(r => r.id === remark.id);
  if (remarkToUpdate) {
    remarkToUpdate.text = editText.value.trim();
    remarkToUpdate.date = new Date().toISOString().split("T")[0];
  }
  cancelEdit();
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

function deleteRemark() {
  if (remarkToDelete.value) {
    selectedStudent.value.remarks = selectedStudent.value.remarks.filter(
      r => r.id !== remarkToDelete.value.id
    );
    showDeleteDialog.value = false;
    remarkToDelete.value = null;
  }
}

function addRemark() {
  if (selectedStudent.value && newRemark.value) {
    selectedStudent.value.remarks.unshift({
      id: Date.now(),
      date: new Date().toISOString().split("T")[0],
      text: newRemark.value
    });
    newRemark.value = "";
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