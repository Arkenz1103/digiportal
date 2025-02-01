
<template>
  <div class="min-h-screen bg-gray-100 p-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-800 mb-2">Admin Dashboard</h1>
      <p class="text-gray-600">Welcome back, {{ user?.name }}! </p>
    </div>

    <!-- Quick Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- Lesson Plans Card -->
      <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-blue-500 hover:shadow-lg transition">
        <div class="flex justify-between items-center">
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-2">Lesson Plans</h3>
            <p class="text-3xl font-bold text-blue-600">{{ stats.lessonPlans }}</p>
          </div>
          <div class="bg-blue-100 rounded-full p-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
        </div>
        <div class="mt-4 text-sm text-gray-500">
          <span class="text-green-500">+{{ stats.newLessonPlans }} new this week</span>
        </div>
      </div>

      <!-- Teachers Card -->
      <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-green-500 hover:shadow-lg transition">
        <div class="flex justify-between items-center">
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-2">Teachers</h3>
            <p class="text-3xl font-bold text-green-600">{{ stats.teachers }}</p>
          </div>
          <div class="bg-green-100 rounded-full p-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
        </div>
        <div class="mt-4 text-sm text-gray-500">
          <span class="text-blue-500">{{ stats.newTeachers }} new teachers</span>
        </div>
      </div>

      <!-- Students Card -->
      <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-purple-500 hover:shadow-lg transition">
        <div class="flex justify-between items-center">
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-2">Students</h3>
            <p class="text-3xl font-bold text-purple-600">{{ stats.students }}</p>
          </div>
          <div class="bg-purple-100 rounded-full p-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
        </div>
        <div class="mt-4 text-sm text-gray-500">
          <span class="text-red-500">{{ stats.newStudents }} new enrollments</span>
        </div>
      </div>

      <!-- Classes Card -->
      <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-red-500 hover:shadow-lg transition">
        <div class="flex justify-between items-center">
          <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-2">Classes</h3>
            <p class="text-3xl font-bold text-red-600">{{ stats.classes }}</p>
          </div>
          <div class="bg-red-100 rounded-full p-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z" />
            </svg>
          </div>
        </div>
        <div class="mt-4 text-sm text-gray-500">
          <span class="text-green-500">+{{ stats.newClasses }} new this month</span>
        </div>
      </div>
    </div>

    <!-- Recent Activities -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Lesson Plans -->
      <div class="bg-white rounded-xl shadow-md p-6">
        <h3 class="text-xl font-semibold mb-4 text-gray-800">Pending Review</h3>
        <div class="space-y-4">
          <div
            v-for="(plan, index) in recentLessonPlans"
            :key="index"
            class="flex justify-between items-center border-b pb-2 last:border-b-0"
          >
            <div>
              <p class="font-medium text-gray-700">{{ plan.title }}</p>
              <p class="text-sm text-gray-500">{{ plan.teacher }}</p>
            </div>
            <span
              :class="plan.status === 'Draft' ? 'bg-blue-100 text-blue-600' : 'bg-green-100 text-green-600'"
              class="text-xs px-2 py-1 rounded-full uppercase"
            >
              {{ plan.status }}
            </span>
          </div>
        </div>
      </div>

      <!-- Recently Monitored Classes -->
      <div class="bg-white rounded-xl shadow-md p-6">
        <h3 class="text-xl font-semibold mb-4 text-gray-800">Recently Monitored Classes</h3>
        <div class="space-y-4">
          <div
            v-for="(classItem, index) in recentlyMonitoredClasses"
            :key="index"
            class="flex justify-between items-center border-b pb-2 last:border-b-0"
          >
            <div>
              <p class="font-medium text-gray-700">{{ classItem.name }}</p>
              <p class="text-sm text-gray-500">{{ classItem.teacher }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  user: {
    type: Object,
    required: true
  }
})

// Mock data for demonstration
const stats = ref({
  lessonPlans: 45,
  newLessonPlans: 7,
  teachers: 12,
  newTeachers: 2,
  students: 250,
  newStudents: 15,
  classes: 20,
  newClasses: 3
})

const recentLessonPlans = ref([
  { title: 'Introduction to Mathematics', teacher: 'John Doe', status: 'Review' },
  { title: 'Science Exploration', teacher: 'Jane Smith', status: 'Review' },
  { title: 'History Basics', teacher: 'Mike Johnson', status: 'Review' }
])

const recentlyMonitoredClasses = ref([
  { name: 'Class 1', teacher: 'John Doe', status: 'Active' },
  { name: 'Class 2', teacher: 'Jane Smith', status: 'In Progress' },
  { name: 'Class 3', teacher: 'Mike Johnson', status: 'Monitoring' }
])

// Quick Action Methods
const createNewTeacher = () => {
  console.log('Creating new teacher')
  // Implement teacher creation logic
}

const createNewClass = () => {
  console.log('Creating new class')
  // Implement class creation logic
}

const addNewStudent = () => {
  console.log('Adding new student')
  // Implement student addition logic
}

const createLessonPlan = () => {
  console.log('Creating lesson plan')
  // Implement lesson plan creation logic
}
</script>

<style scoped>
/* Additional custom styles can be added here */
</style>
