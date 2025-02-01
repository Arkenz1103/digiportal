<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <!-- Create Lesson Plan Button -->
    <div class="flex justify-end mb-6">
      <button 
        @click="createLessonPlan" 
        class="bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg shadow hover:bg-blue-600 transition duration-300 ease-in-out flex items-center"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Create Lesson Plan
      </button>
    </div>

    <!-- Lesson Plan List -->
    <div class="grid grid-cols-1 gap-6 max-w-2xl mx-auto">
      <div 
        v-for="(lesson, index) in lessons" 
        :key="index" 
        class="bg-white rounded-xl shadow-md overflow-hidden transform transition hover:scale-102 hover:shadow-lg"
      >
        <div class="p-6">
          <div class="flex justify-between items-start mb-4">
            <div>
              <p class="text-xl font-bold text-gray-800 mb-2">{{ lesson.title }}</p>
              <span 
                :class="lesson.status === 'Draft' ? 'bg-blue-100 text-blue-600' : 'bg-green-100 text-green-600'" 
                class="text-xs px-2 py-1 rounded-full uppercase tracking-wider"
              >
                {{ lesson.status }}
              </span>
            </div>
          </div>
          
          <div class="mt-4 flex justify-between items-center">
            <div class="flex space-x-2">
              <button 
                @click="editLessonPlan(index)" 
                class="text-gray-500 hover:text-blue-600 transition"
                title="Edit"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>
              <button 
                @click="deleteLessonPlan(index)" 
                class="text-gray-500 hover:text-red-600 transition"
                title="Delete"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
            <div class="text-sm text-gray-500">
              {{ lesson.date }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const lessons = ref([
  { 
    title: 'Introduction to Mathematics', 
    status: 'Draft', 
    date: 'Jan 31, 2025'
  },
  { 
    title: 'Science Exploration', 
    status: 'Submitted', 
    date: 'Feb 1, 2025'
  }
])

const createLessonPlan = () => {
  lessons.value.push({
    title: 'New Lesson Plan',
    status: 'Draft',
    date: new Date().toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric' 
    })
  })
}

const editLessonPlan = (index) => {
  console.log('Edit lesson plan:', index)
}

const deleteLessonPlan = (index) => {
  lessons.value.splice(index, 1)
}
</script>

<style scoped>
/* Add any additional scoped styles if needed */
</style>
