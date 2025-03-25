<template>
  <Head title="Student Remarks" />
  
  <div class="p-6 max-w-7xl mx-auto">
    <div class="bg-white rounded-lg shadow-lg">
      <!-- Header -->
      <div class="border-b p-6">
        <h1 class="text-2xl font-bold text-gray-900">Pupil Remarks Management</h1>
      </div>

      <!-- Content -->
      <div class="p-6">
        <div class="grid grid-cols-3 gap-6">
          <!-- Pupil List -->
          <div class="col-span-1">
            <div class="bg-gray-50 rounded-xl border border-gray-200 overflow-hidden">
              <div class="bg-white p-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
                  <i class="pi pi-users text-blue-600"></i>
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
                          ? 'bg-blue-50 border-blue-200' 
                          : 'hover:bg-gray-50 border-transparent',
                        'border'
                      ]">
                    <div class="flex items-center gap-3">
                      <div class="bg-gradient-to-r from-blue-500 to-blue-700 text-white font-bold w-8 h-8 flex items-center justify-center rounded-full shadow-md">
                        {{ student.name.charAt(0) }}
                      </div>
                      <span class="font-medium text-gray-900">{{ student.name }}</span>
                    </div>
                    <span class="text-sm text-gray-500">{{ student.remarks.length }} remarks</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          
          <!-- Remarks Section -->
          <div class="col-span-2 bg-gray-50 rounded-xl border border-gray-200 overflow-hidden">
            <div class="bg-white p-4 border-b border-gray-200">
              <h3 v-if="selectedStudent" class="text-lg font-semibold text-gray-800 flex items-center gap-2">
                <i class="pi pi-comments text-blue-600"></i>
                Remarks for {{ selectedStudent.name }}
              </h3>
              <h3 v-else class="text-lg font-semibold text-gray-500">
                Select a student to view remarks
              </h3>
            </div>
            
            <div class="p-4">
              <div v-if="selectedStudent" class="space-y-4">
                <!-- Add Remark Section -->
                <div class="bg-white p-4 rounded-lg border border-gray-200">
                  <div class="flex gap-3 mb-3">
                    <Dropdown 
                      v-model="selectedCategory" 
                      :options="categories" 
                      placeholder="Select category" 
                      class="w-1/3" />
                    <Button 
                      label="Add Remark" 
                      icon="pi pi-plus"
                      @click="addRemark" 
                      class="p-button-primary" />
                  </div>
                  <Textarea 
                    v-model="newRemark" 
                    rows="3" 
                    placeholder="Enter new remark..." 
                    class="w-full"/>
                </div>

                <!-- Remarks List -->
                <div class="space-y-3">
                  <div v-for="remark in selectedStudent.remarks" 
                       :key="remark.id" 
                       class="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-all">
                    <div class="flex items-center justify-between mb-2">
                      <span class="text-sm font-medium text-blue-600">{{ remark.category }}</span>
                      <span class="text-sm text-gray-500">{{ remark.date }}</span>
                    </div>
                    <p class="text-gray-800">{{ remark.text }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { Head } from '@inertiajs/vue3';
import Dropdown from "primevue/dropdown";
import Button from "primevue/button";
import Textarea from "primevue/textarea";
import TeacherLayout from '@/Layouts/MainLayout.vue';

const students = ref([
  { id: 1, name: "Alice Smith", remarks: [
      { id: 1, category: "Academic", date: "2024-01-15", text: "Struggling with math concepts" },
      { id: 2, category: "Emotional", date: "2024-01-14", text: "Seems withdrawn in class" }
  ]},
  { id: 2, name: "Bob Johnson", remarks: [
      { id: 3, category: "Academic", date: "2024-01-16", text: "Needs help with reading comprehension" }
  ]},
  { id: 3, name: "Carrol Williams", remarks: [
      { id: 4, category: "Behavioral", date: "2024-01-17", text: "Talks excessively in class" }
  ]},
  { id: 4, name: "David Brown", remarks: [
      { id: 5, category: "Academic", date: "2024-01-18", text: "Excellent performance in science" }
  ]},
  { id: 5, name: "Emma Davies", remarks: [
      { id: 6, category: "Emotional", date: "2024-01-19", text: "Appears anxious before tests" }
  ]}
]);

const selectedStudent = ref(null);
const selectedCategory = ref(null);
const newRemark = ref("");
const categories = ref(["Academic", "Emotional", "Behavioral"]);

function selectStudent(student) {
  selectedStudent.value = student;
}

function addRemark() {
  if (selectedStudent.value && newRemark.value && selectedCategory.value) {
    selectedStudent.value.remarks.push({
      id: Date.now(),
      category: selectedCategory.value,
      date: new Date().toISOString().split("T")[0],
      text: newRemark.value
    });
    newRemark.value = "";
    selectedCategory.value = null;
  }
}
</script>

<script>
export default {
  layout: TeacherLayout
};
</script>

<style scoped>
.bg-gradient-to-r {
  background-size: 200% 200%;
  animation: gradient 15s ease infinite;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style> 