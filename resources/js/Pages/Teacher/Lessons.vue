<template>
  <div class="flex flex-col space-y-4 p-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">Lesson Plans</h1>
      <input 
        type="file" 
        ref="fileInput" 
        @change="handleFileUpload" 
        accept=".pdf,.doc,.docx" 
        class="hidden"
      />
      <button 
        @click="triggerFileUpload"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Upload Lesson Plan
      </button>
    </div>

    <!-- Empty State -->
    <div 
      v-if="lessonPlans.length === 0" 
      class="bg-white shadow rounded-lg p-6 text-center"
    >
      <p class="text-gray-500">No lesson plans uploaded yet</p>
      <p class="text-sm text-gray-400 mt-2">
        Click "Upload Lesson Plan" to get started
      </p>
    </div>

    <!-- Lesson Plans Table -->
    <div 
      v-else 
      class="bg-white shadow rounded-lg"
    >
      <table class="w-full">
        <thead class="bg-gray-100 border-b">
          <tr>
            <th class="p-3 text-left">Title</th>
            <th class="p-3 text-left">Status</th>
            <th class="p-3 text-left">Date Uploaded</th>
            <th class="p-3 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="lesson in lessonPlans" 
            :key="lesson.id" 
            class="border-b hover:bg-gray-50"
          >
            <td class="p-3">{{ lesson.title }}</td>
            <td class="p-3">
              <span 
                :class="{
                  'text-yellow-600': lesson.status === 'Pending',
                  'text-green-600': lesson.status === 'Approved',
                  'text-red-600': lesson.status === 'Rejected'
                }"
              >
                {{ lesson.status }}
              </span>
            </td>
            <td class="p-3">{{ lesson.uploaded_at }}</td>
            <td class="p-3">
              <button 
                @click="viewLessonPlan(lesson)"
                class="text-blue-500 hover:underline mr-2"
              >
                View
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { router } from '@inertiajs/vue3';
import axios from 'axios';

export default {
  setup() {
    const fileInput = ref(null);
    const lessonPlans = ref([]);

    const triggerFileUpload = () => {
      fileInput.value.click();
    };

    const handleFileUpload = async (event) => {
      const file = event.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('lesson_plan', file);

        try {
          const response = await axios.post('/teacher/lesson-plans/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });

          // Update lesson plans list
          lessonPlans.value = response.data.lesson_plans;
          
          // Reset file input
          if (fileInput.value) {
            fileInput.value.value = '';
          }
        } catch (error) {
          console.error('Upload failed:', error);
          alert('File upload failed. Please try again.');
        }
      }
    };

    const fetchLessonPlans = async () => {
      try {
        const response = await axios.get('/teacher/lesson-plans');
        lessonPlans.value = response.data.lesson_plans;
      } catch (error) {
        console.error('Failed to fetch lesson plans:', error);
      }
    };

    const viewLessonPlan = (lesson) => {
      // Implement view logic, e.g., open file in new tab
      window.open(`/storage/${lesson.path}`, '_blank');
    };

    onMounted(() => {
      fetchLessonPlans();
    });

    return {
      fileInput,
      lessonPlans,
      triggerFileUpload,
      handleFileUpload,
      viewLessonPlan
    };
  }
};
</script>
