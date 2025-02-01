<script setup>
import { ref, computed } from "vue";
import { Link } from "@inertiajs/vue3";
import Dropdown from 'primevue/dropdown';

// Lesson Status Types
const LESSON_STATUS = {
  PENDING_REVIEW: 'Pending Review'
};

// Lesson Priority Levels
const LESSON_PRIORITY = {
  HIGH: 'High',
  MEDIUM: 'Medium',
  LOW: 'Low'
};

// Dummy data structure to represent upcoming review lesson plans
const lessonPlans = ref([
  {
    id: 3,
    title: 'World History: Industrial Revolution',
    teacher: 'Michael Chen',
    subject: 'History',
    grade: '9C',
    dueDate: new Date(new Date().setDate(new Date().getDate() + 14)).toISOString().split('T')[0],
    status: LESSON_STATUS.PENDING_REVIEW,
    priority: LESSON_PRIORITY.LOW
  },
  {
    id: 4,
    title: 'Advanced Biology: Genetics',
    teacher: 'Sarah Williams',
    subject: 'Biology',
    grade: '12A',
    dueDate: new Date(new Date().setDate(new Date().getDate() + 21)).toISOString().split('T')[0],
    status: LESSON_STATUS.PENDING_REVIEW,
    priority: LESSON_PRIORITY.MEDIUM
  }
]);

// Search and Filter State
const searchQuery = ref("");
const filters = ref({
  teacher: "",
  subject: "",
  priority: ""
});

// Pagination State
const currentPage = ref(1);
const itemsPerPage = 5;

// Computed Filtered Lesson Plans
const filteredLessonPlans = computed(() => {
  return lessonPlans.value.filter((lesson) => {
    const isUpcoming = new Date(lesson.dueDate) > new Date(new Date().setDate(new Date().getDate() + 7));
    
    return isUpcoming && (
      (!filters.value.teacher || lesson.teacher.includes(filters.value.teacher)) &&
      (!filters.value.subject || lesson.subject.includes(filters.value.subject)) &&
      (!filters.value.priority || lesson.priority === filters.value.priority) &&
      (!searchQuery.value || 
        lesson.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        lesson.teacher.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    );
  }).sort((a, b) => {
    // Sort by priority and due date
    const priorityOrder = { 
      [LESSON_PRIORITY.HIGH]: 1, 
      [LESSON_PRIORITY.MEDIUM]: 2, 
      [LESSON_PRIORITY.LOW]: 3 
    };
    return priorityOrder[a.priority] - priorityOrder[b.priority] || 
           new Date(a.dueDate) - new Date(b.dueDate);
  });
});

const paginatedLessonPlans = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredLessonPlans.value.slice(start, start + itemsPerPage);
});

const totalPages = computed(() => Math.ceil(filteredLessonPlans.value.length / itemsPerPage));

// Pagination Handlers
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) currentPage.value = page;
};

// Action Methods
const reviewLessonPlan = (lesson) => {
  console.log(`Reviewing upcoming lesson plan: ${lesson.title}`);
};
</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <header class="mb-4">
      <h1 class="text-2xl font-bold">Upcoming Review Lessons</h1>
      <div class="text-sm text-gray-600 mt-2">
        Lesson plans for future weeks
      </div>
    </header>

    <div class="mb-4 px-6">
      <div class="relative w-2/3">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search lessons..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-full bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm transition duration-300 ease-in-out"
        />
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>
      </div>
    </div>

    <!-- Lesson Plans Table -->
    <table class="w-full border-collapse border border-gray-300">
      <thead class="bg-gray-100">
        <tr>
          <th class="border border-gray-300 px-4 py-2">Teacher</th>
          <th class="border border-gray-300 px-4 py-2">Subject</th>
          <th class="border border-gray-300 px-4 py-2">Grade</th>
          <th class="border border-gray-300 px-4 py-2">Title</th>
          <th class="border border-gray-300 px-4 py-2">Due Date</th>
          <th class="border border-gray-300 px-4 py-2">Priority</th>
          <th class="border border-gray-300 px-4 py-2">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="lesson in paginatedLessonPlans" :key="lesson.id" class="hover:bg-gray-50">
          <td class="border border-gray-300 px-4 py-2">{{ lesson.teacher }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ lesson.subject }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ lesson.grade }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ lesson.title }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ lesson.dueDate }}</td>
          <td class="border border-gray-300 px-4 py-2">
            <span :class="{
              'text-green-600': lesson.priority === LESSON_PRIORITY.HIGH,
              'text-yellow-600': lesson.priority === LESSON_PRIORITY.MEDIUM,
              'text-gray-600': lesson.priority === LESSON_PRIORITY.LOW
            }">
              {{ lesson.priority }}
            </span>
          </td>
          <td class="border border-gray-300 px-4 py-2 text-center">
            <button 
              @click="reviewLessonPlan(lesson)"
              class="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600 transition duration-300"
            >
              Upcoming Review
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div class="flex justify-between items-center mt-4 px-6">
      <div>
        Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to 
        {{ Math.min(currentPage * itemsPerPage, filteredLessonPlans.length) }} 
        of {{ filteredLessonPlans.length }} lessons
      </div>
      <div class="flex space-x-2">
        <button 
          @click="goToPage(currentPage - 1)" 
          :disabled="currentPage === 1"
          class="px-3 py-1 border rounded bg-gray-200 disabled:opacity-50"
        >
          Previous
        </button>
        <button 
          @click="goToPage(currentPage + 1)" 
          :disabled="currentPage === totalPages"
          class="px-3 py-1 border rounded bg-gray-200 disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Additional custom styles can be added here */
</style>