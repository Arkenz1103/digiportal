<template>
  <div class="flex flex-col h-screen">
    <!-- Header -->
    <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-4 md:p-3 shadow-lg rounded-t-xl">
      <div class="space-y-3">
        <h1 class="text-xl md:text-2xl font-bold text-white px-4 py-2 md:px-5 md:py-2 rounded-lg inline-block bg-white/20">
          👥 Student Directory
        </h1>
        <p class="text-white/90 ml-2 flex items-center gap-2 text-sm">
          <span>📚 Manage and view all students</span>
        </p>
        
        <!-- Filter Tabs -->
        <div class="flex flex-wrap gap-2 md:gap-4 mt-3 md:mt-4">
          <button
            @click="selectedGrade = null"
            :class="[
              'flex items-center gap-2 text-white/90 px-4 py-2 md:px-5 md:py-2.5 rounded-lg transition-all duration-300 relative overflow-hidden group',
              selectedGrade === null ? 'bg-white/30' : 'bg-white/10 hover:bg-white/20'
            ]"
          >
            <span>All Grades</span>
            <span class="bg-white/20 px-2 py-0.5 rounded-full text-xs">{{ totalStudents }}</span>
          </button>
          
          <button
            v-for="grade in [1, 2, 3, 4, 5, 6]"
            :key="grade"
            @click="selectedGrade = grade"
            :class="[
              'flex items-center gap-2 text-white/90 px-4 py-2 md:px-5 md:py-2.5 rounded-lg transition-all duration-300 relative overflow-hidden group',
              selectedGrade === grade ? 'bg-white/30' : 'bg-white/10 hover:bg-white/20'
            ]"
          >
            <span>Grade {{ grade }}</span>
            <span class="bg-white/20 px-2 py-0.5 rounded-full text-xs">{{ getGradeCount(grade) }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="w-full bg-white/80 flex-1 overflow-hidden">
      <div class="w-full px-4 sm:px-6 pt-4 pb-6 transition-all duration-300 h-full flex flex-col">
        
        <!-- Search and Section Filter -->
        <div class="flex flex-col md:flex-row gap-4 mb-6">
          <div class="flex-1">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by name or student ID..."
                class="w-full px-4 py-3 pl-12 rounded-lg border-2 border-indigo-200 focus:border-indigo-500 focus:outline-none transition-all"
              />
              <svg class="w-5 h-5 absolute left-4 top-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
          
          <div class="flex gap-2">
            <button
              @click="selectedSection = null"
              :class="[
                'px-6 py-3 rounded-lg font-medium transition-all',
                selectedSection === null ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              ]"
            >
              All Sections
            </button>
            <button
              @click="selectedSection = 'A'"
              :class="[
                'px-6 py-3 rounded-lg font-medium transition-all',
                selectedSection === 'A' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              ]"
            >
              Section A
            </button>
            <button
              @click="selectedSection = 'B'"
              :class="[
                'px-6 py-3 rounded-lg font-medium transition-all',
                selectedSection === 'B' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              ]"
            >
              Section B
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex flex-col items-center justify-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
          <p class="text-gray-600">Loading students...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="flex flex-col items-center justify-center py-20">
          <svg class="h-16 w-16 text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Failed to load students</h3>
          <p class="text-sm text-gray-500 mb-4">{{ error }}</p>
          <button
            @click="fetchStudents"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Try Again
          </button>
        </div>

        <!-- Students Table -->
        <div v-else class="flex-1 overflow-auto bg-white rounded-lg shadow-lg">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-indigo-600 to-violet-600 text-white sticky top-0">
              <tr>
                <th class="px-6 py-4 text-left text-sm font-semibold">Student ID</th>
                <th class="px-6 py-4 text-left text-sm font-semibold">Full Name</th>
                <th class="px-6 py-4 text-left text-sm font-semibold">Grade & Section</th>
                <th class="px-6 py-4 text-left text-sm font-semibold">Gender</th>
                <th class="px-6 py-4 text-left text-sm font-semibold">Contact</th>
                <th class="px-6 py-4 text-left text-sm font-semibold">Average</th>
                <th class="px-6 py-4 text-left text-sm font-semibold">Attendance</th>
                <th class="px-6 py-4 text-left text-sm font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr
                v-for="student in filteredStudents"
                :key="student.id"
                class="hover:bg-indigo-50 transition-colors"
              >
                <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ student.student_id }}</td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-400 to-violet-400 flex items-center justify-center text-white font-bold">
                      {{ student.first_name[0] }}{{ student.last_name[0] }}
                    </div>
                    <div>
                      <div class="text-sm font-medium text-gray-900">
                        {{ student.first_name }} {{ student.middle_name }} {{ student.last_name }}
                      </div>
                      <div class="text-xs text-gray-500">{{ student.email }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800">
                    Grade {{ student.grade_level }} - {{ student.section }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-700">
                  <span :class="student.gender === 'M' ? 'text-blue-600' : 'text-pink-600'">
                    {{ student.gender === 'M' ? '♂ Male' : '♀ Female' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-700">{{ student.contact_number }}</td>
                <td class="px-6 py-4">
                  <span :class="[
                    'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium',
                    student.current_average >= 90 ? 'bg-green-100 text-green-800' :
                    student.current_average >= 85 ? 'bg-blue-100 text-blue-800' :
                    student.current_average >= 80 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  ]">
                    {{ student.current_average }}%
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span :class="[
                    'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium',
                    student.attendance_percentage >= 95 ? 'bg-green-100 text-green-800' :
                    student.attendance_percentage >= 90 ? 'bg-blue-100 text-blue-800' :
                    student.attendance_percentage >= 85 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  ]">
                    {{ student.attendance_percentage }}%
                  </span>
                </td>
                <td class="px-6 py-4">
                  <button
                    @click="viewStudent(student)"
                    class="text-indigo-600 hover:text-indigo-900 font-medium text-sm"
                  >
                    View Details
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          
          <!-- No Results -->
          <div v-if="filteredStudents.length === 0" class="text-center py-20">
            <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <h3 class="mt-4 text-lg font-medium text-gray-900">No students found</h3>
            <p class="mt-2 text-sm text-gray-500">Try adjusting your search or filter criteria.</p>
          </div>
        </div>

        <!-- Summary Stats -->
        <div class="mt-4 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-4 text-white">
            <div class="text-sm opacity-90">Total Students</div>
            <div class="text-3xl font-bold">{{ filteredStudents.length }}</div>
          </div>
          <div class="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-4 text-white">
            <div class="text-sm opacity-90">Male Students</div>
            <div class="text-3xl font-bold">{{ maleCount }}</div>
          </div>
          <div class="bg-gradient-to-br from-pink-500 to-pink-600 rounded-lg p-4 text-white">
            <div class="text-sm opacity-90">Female Students</div>
            <div class="text-3xl font-bold">{{ femaleCount }}</div>
          </div>
          <div class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-4 text-white">
            <div class="text-sm opacity-90">Average Grade</div>
            <div class="text-3xl font-bold">{{ averageGrade }}%</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useToast } from '../../composables/useToast';

const { showSuccess, showError, showInfo, showWarning } = useToast();

const students = ref([]);
const loading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const selectedGrade = ref(null);
const selectedSection = ref(null);

// Fetch students from API
const fetchStudents = async () => {
  try {
    loading.value = true;
    error.value = null;
    const response = await window.axios.get('/api/students/');
    students.value = response.data;
    console.log('✓ Loaded students:', students.value.length);
  } catch (err) {
    console.error('❌ Error fetching students:', err);
    if (err.response) {
      error.value = `Server error: ${err.response.status} - ${err.response.statusText}`;
      showError(error.value, 'Failed to Load Students');
    } else if (err.request) {
      error.value = 'Cannot connect to server. Please check your connection.';
      showError(error.value, 'Connection Error');
    } else {
      error.value = err.message;
      showError(error.value, 'Error');
    }
  } finally {
    loading.value = false;
  }
};

// Filtered students based on search and filters
const filteredStudents = computed(() => {
  let filtered = students.value;
  
  // Filter by grade
  if (selectedGrade.value !== null) {
    filtered = filtered.filter(s => s.grade_level === selectedGrade.value);
  }
  
  // Filter by section
  if (selectedSection.value !== null) {
    filtered = filtered.filter(s => s.section === selectedSection.value);
  }
  
  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(s =>
      s.student_id.toLowerCase().includes(query) ||
      s.first_name.toLowerCase().includes(query) ||
      s.last_name.toLowerCase().includes(query) ||
      s.middle_name?.toLowerCase().includes(query)
    );
  }
  
  return filtered;
});

// Computed stats
const totalStudents = computed(() => students.value.length);
const maleCount = computed(() => filteredStudents.value.filter(s => s.gender === 'M').length);
const femaleCount = computed(() => filteredStudents.value.filter(s => s.gender === 'F').length);
const averageGrade = computed(() => {
  if (filteredStudents.value.length === 0) return 0;
  const sum = filteredStudents.value.reduce((acc, s) => acc + parseFloat(s.current_average || 0), 0);
  return (sum / filteredStudents.value.length).toFixed(2);
});

const getGradeCount = (grade) => {
  return students.value.filter(s => s.grade_level === grade).length;
};

const viewStudent = (student) => {
  // TODO: Implement student detail view
  alert(`Viewing details for ${student.first_name} ${student.last_name}`);
};

onMounted(() => {
  fetchStudents();
});
</script>
