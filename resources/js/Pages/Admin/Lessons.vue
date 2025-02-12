<script setup>
import { ref, computed } from "vue";
import { Link, usePage } from "@inertiajs/vue3";
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';

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

// Unique values for filters
const teacherOptions = computed(() =>
  [...new Set(lessonPlans.value.map(lesson => lesson.teacher))]
);

const subjectOptions = computed(() =>
  [...new Set(lessonPlans.value.map(lesson => lesson.subject))]
);

const gradeOptions = computed(() =>
  [...new Set(lessonPlans.value.map(lesson => lesson.grade))]
);

// Search and Filter State
const searchQuery = ref("");
const filters = ref({
  teacher: "",
  subject: "",
  grade: "",
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
      (!filters.value.grade || lesson.grade.includes(filters.value.grade)) &&
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

    <!-- Filters Section -->
    <div class="mb-4 grid grid-cols-4 gap-4">
      <!-- Search Input -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <i class="pi pi-search text-gray-400"></i>
          </div>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by title or teacher"
            class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>
      <Dropdown
        v-model="filters.teacher"
        :options="[
          { label: '[All Teachers]', value: '' },
          { label: 'John Smith', value: 'John Smith' },
          { label: 'Emily Rodriguez', value: 'Emily Rodriguez' },
          { label: 'Michael Chen', value: 'Michael Chen' },
          { label: 'Sarah Williams', value: 'Sarah Williams' },
          { label: 'Carlos Ramirez', value: 'Carlos Ramirez' },
          { label: 'Elizabeth Brown', value: 'Elizabeth Brown' }
        ]"
        optionLabel="label"
        optionValue="value"
        placeholder="Select a Teacher"
        class="w-full"
      />
      <Dropdown
        v-model="filters.status"
        :options="[
          { label: '[All Statuses]', value: '' },
          { label: 'Pending Review', value: LESSON_STATUS.PENDING_REVIEW },
          { label: 'Approved', value: LESSON_STATUS.APPROVED },
          { label: 'Needs Revision', value: LESSON_STATUS.NEEDS_REVISION }
        ]"
        optionLabel="label"
        optionValue="value"
        placeholder="Select a Status"
        class="w-full"
      />
      <Dropdown
        v-model="filters.priority"
        :options="[
          { label: '[All Priorities]', value: '' },
          { label: 'High Priority', value: LESSON_PRIORITY.HIGH },
          { label: 'Medium Priority', value: LESSON_PRIORITY.MEDIUM },
          { label: 'Low Priority', value: LESSON_PRIORITY.LOW }
        ]"
        optionLabel="label"
        optionValue="value"
        placeholder="Select a Priority"
        class="w-full"
      />
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
        <tr
          v-for="lesson in paginatedLessonPlans"
          :key="lesson.id"
          class="border-b hover:bg-gray-50"
        >
          <td class="border border-gray-300 px-4 py-2">{{ lesson.teacher }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ lesson.subject }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ lesson.grade }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ lesson.title }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ lesson.dueDate }}</td>
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
          <td class="border border-gray-300 px-4 py-2 text-center">
            <button
              @click="reviewLessonPlan(lesson)"
              class="text-blue-600 hover:text-blue-800"
            >
              Review
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div class="flex justify-between items-center mt-4">
      <div>
        Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to
        {{ Math.min(currentPage * itemsPerPage, filteredLessonPlans.length) }}
        of {{ filteredLessonPlans.length }} entries
      </div>
      <div class="flex space-x-2">
        <Button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          icon="pi pi-chevron-left"
          label="Previous"
          severity="success"
          class="mr-2 custom-small-button"
        />
        <Button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          icon-pos="right"
          icon="pi pi-chevron-right"
          label="Next"
          severity="danger"
          class="custom-small-button"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-small-button {
  padding: 0.375rem 0.75rem !important;
  font-size: 0.875rem !important;
  height: 2.25rem !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
  transition: all 0.2s ease !important;
  border-width: 1px !important;
  border-style: solid !important;
  border-color: transparent !important;

  /* Text clarity improvements */
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: subpixel-antialiased;
  -moz-osx-font-smoothing: auto;
  font-kerning: normal;
  font-display: swap;
}

.custom-small-button:hover:not(:disabled) {
  box-shadow: 0 2px 4px rgba(0,0,0,0.15) !important;
}

.custom-small-button:focus {
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.5), 0 0 0 4px currentColor !important;
}

.custom-small-button:hover:not(:disabled) {
  box-shadow: 0 2px 4px rgba(0,0,0,0.15) !important;
}

.custom-small-button:focus {
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.5), 0 0 0 4px currentColor !important;
}
</style>
