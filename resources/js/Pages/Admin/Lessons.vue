<script setup>
import { ref, computed } from "vue";
import { Link, usePage } from "@inertiajs/vue3";

// Lesson Status Types
const LESSON_STATUS = {
  PENDING_REVIEW: 'Pending Review',
  APPROVED: 'Approved',
  NEEDS_REVISION: 'Needs Revision'
};

// Lesson Priority Levels
const LESSON_PRIORITY = {
  HIGH: 'High',
  MEDIUM: 'Medium',
  LOW: 'Low'
};

// Dummy data structure to represent lesson plans
const lessonPlans = ref([
  // Urgent Review Lessons (within 7 days)
  {
    id: 1,
    title: 'Math Algebra Fundamentals',
    teacher: 'John Smith',
    subject: 'Mathematics',
    grade: '10A',
    dueDate: new Date(new Date().setDate(new Date().getDate() + 3)).toISOString().split('T')[0],
    status: LESSON_STATUS.PENDING_REVIEW,
    priority: LESSON_PRIORITY.HIGH
  },
  {
    id: 2,
    title: 'Physics Mechanics',
    teacher: 'Emily Rodriguez',
    subject: 'Physics',
    grade: '11B',
    dueDate: new Date(new Date().setDate(new Date().getDate() + 5)).toISOString().split('T')[0],
    status: LESSON_STATUS.PENDING_REVIEW,
    priority: LESSON_PRIORITY.MEDIUM
  },
  
  // Upcoming Review Lessons (more than 7 days)
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
  },
  {
    id: 5,
    title: 'Spanish Language and Culture',
    teacher: 'Carlos Ramirez',
    subject: 'Foreign Language',
    grade: '10B',
    dueDate: new Date(new Date().setDate(new Date().getDate() + 30)).toISOString().split('T')[0],
    status: LESSON_STATUS.PENDING_REVIEW,
    priority: LESSON_PRIORITY.LOW
  },
  
  // Approved Lessons
  {
    id: 6,
    title: 'English Literature: Shakespeare',
    teacher: 'Elizabeth Brown',
    subject: 'English',
    grade: '11A',
    dueDate: '2024-02-01',
    status: LESSON_STATUS.APPROVED,
    priority: LESSON_PRIORITY.HIGH
  }
]);

// Search and Filter State
const searchQuery = ref("");
const filters = ref({
  teacher: "",
  subject: "",
  status: "",
  priority: ""
});

// Pagination State
const currentPage = ref(1);
const itemsPerPage = 5;

const page = usePage();
const initialView = page.props.view || 'urgent_and_upcoming';

// Modify the initial state to use the route parameter
const activeView = ref(initialView);

// Computed Filtered Lesson Plans
const filteredLessonPlans = computed(() => {
  return lessonPlans.value.filter((lesson) => {
    let isMatchingView = true;
    
    switch(activeView.value) {
      case 'urgent':
        isMatchingView = lesson.status === LESSON_STATUS.PENDING_REVIEW && 
                         new Date(lesson.dueDate) <= new Date(new Date().setDate(new Date().getDate() + 7));
        break;
      case 'upcoming':
        isMatchingView = lesson.status === LESSON_STATUS.PENDING_REVIEW && 
                         new Date(lesson.dueDate) > new Date(new Date().setDate(new Date().getDate() + 7));
        break;
      case 'urgent_and_upcoming':
        isMatchingView = lesson.status === LESSON_STATUS.PENDING_REVIEW;
        break;
      case 'approved':
        isMatchingView = lesson.status === LESSON_STATUS.APPROVED;
        break;
    }

    return isMatchingView && (
      (!filters.value.teacher || lesson.teacher.includes(filters.value.teacher)) &&
      (!filters.value.subject || lesson.subject.includes(filters.value.subject)) &&
      (!filters.value.status || lesson.status === filters.value.status) &&
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

// Modify header text based on active view
const pageTitle = computed(() => {
  switch(activeView.value) {
    case 'urgent_and_upcoming':
      return 'Pending Lesson Plans';
    case 'urgent':
      return 'Urgent Review Needed';
    case 'upcoming':
      return 'Upcoming Lesson Plans';
    case 'approved':
      return 'Approved Lesson Plans';
    default:
      return 'Lesson Plans';
  }
});

const pageDescription = computed(() => {
  switch(activeView.value) {
    case 'urgent_and_upcoming':
      return 'All lesson plans that require review, sorted by priority and date';
    case 'urgent':
      return 'Lesson plans that need immediate review (due within 7 days)';
    case 'upcoming':
      return 'Lesson plans for future weeks';
    case 'approved':
      return 'Lesson plans that have been approved';
    default:
      return 'Review and manage lesson plans';
  }
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
  // TODO: Implement lesson plan review modal/navigation
  console.log(`Reviewing lesson plan: ${lesson.title}`);
};
</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <header class="mb-4">
      <h1 class="text-2xl font-bold">{{ pageTitle }}</h1>
      <div class="text-sm text-gray-600 mt-2">
        {{ pageDescription }}
      </div>
    </header>

    <!-- Search and Filters -->
    <div class="mb-4 grid grid-cols-4 gap-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search by title or teacher"
        class="border rounded px-4 py-2"
      />
      <select v-model="filters.teacher" class="border rounded px-4 py-2">
        <option value="">[All Teachers]</option>
        <option value="John Smith">John Smith</option>
        <option value="Emily Rodriguez">Emily Rodriguez</option>
        <option value="Michael Chen">Michael Chen</option>
        <option value="Sarah Williams">Sarah Williams</option>
        <option value="Carlos Ramirez">Carlos Ramirez</option>
        <option value="Elizabeth Brown">Elizabeth Brown</option>
      </select>
      <select v-model="filters.status" class="border rounded px-4 py-2">
        <option value="">[All Statuses]</option>
        <option :value="LESSON_STATUS.PENDING_REVIEW">Pending Review</option>
        <option :value="LESSON_STATUS.APPROVED">Approved</option>
        <option :value="LESSON_STATUS.NEEDS_REVISION">Needs Revision</option>
      </select>
      <select v-model="filters.priority" class="border rounded px-4 py-2">
        <option value="">[All Priorities]</option>
        <option :value="LESSON_PRIORITY.HIGH">High Priority</option>
        <option :value="LESSON_PRIORITY.MEDIUM">Medium Priority</option>
        <option :value="LESSON_PRIORITY.LOW">Low Priority</option>
      </select>
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
          <th class="border border-gray-300 px-4 py-2">Status</th>
          <th class="border border-gray-300 px-4 py-2">Priority</th>
          <th class="border border-gray-300 px-4 py-2">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="lesson in paginatedLessonPlans"
          :key="lesson.id"
          :class="{
            'bg-red-50': lesson.priority === LESSON_PRIORITY.HIGH,
            'bg-yellow-50': lesson.priority === LESSON_PRIORITY.MEDIUM
          }"
          class="text-center hover:bg-blue-50 transition"
        >
          <td class="border border-gray-300 px-4 py-2">{{ lesson.teacher }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ lesson.subject }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ lesson.grade }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ lesson.title }}</td>
          <td class="border border-gray-300 px-4 py-2 font-bold text-red-600">{{ lesson.dueDate }}</td>
          <td class="border border-gray-300 px-4 py-2">
            <span
              :class="{
                'text-yellow-600': lesson.status === LESSON_STATUS.PENDING_REVIEW,
                'text-green-600': lesson.status === LESSON_STATUS.APPROVED,
                'text-red-600': lesson.status === LESSON_STATUS.NEEDS_REVISION
              }"
            >
              {{ lesson.status }}
            </span>
          </td>
          <td class="border border-gray-300 px-4 py-2">
            <span
              :class="{
                'text-red-600': lesson.priority === LESSON_PRIORITY.HIGH,
                'text-yellow-600': lesson.priority === LESSON_PRIORITY.MEDIUM,
                'text-green-600': lesson.priority === LESSON_PRIORITY.LOW
              }"
            >
              {{ lesson.priority }}
            </span>
          </td>
          <td class="border border-gray-300 px-4 py-2">
            <button
              @click="reviewLessonPlan(lesson)"
              class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition"
            >
              Review
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- No Results Message -->
    <div
      v-if="paginatedLessonPlans.length === 0"
      class="text-center py-8 text-gray-500"
    >
      No lesson plans found.
    </div>

    <!-- Pagination -->
    <div
      v-if="paginatedLessonPlans.length > 0"
      class="mt-4 flex justify-center items-center space-x-2"
    >
      <button
        @click="goToPage(currentPage - 1)"
        class="px-3 py-1 border rounded bg-gray-200"
        :disabled="currentPage === 1"
      >
        ‹ Prev
      </button>
      <span v-for="page in totalPages" :key="page">
        <button
          @click="goToPage(page)"
          class="px-3 py-1 border rounded"
          :class="{
            'bg-blue-500 text-white': page === currentPage,
            'bg-gray-200': page !== currentPage,
          }"
        >
          {{ page }}
        </button>
      </span>
      <button
        @click="goToPage(currentPage + 1)"
        class="px-3 py-1 border rounded bg-gray-200"
        :disabled="currentPage === totalPages"
      >
        Next ›
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Additional custom styles can be added here */
</style>
