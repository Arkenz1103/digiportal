<template>
  <div class="p-6 max-w-7xl mx-auto">
    <!-- Header Section with Student Info -->
    <div class="bg-white rounded-lg shadow-lg overflow-hidden mb-6">
      <div class="bg-gradient-to-r from-blue-50 to-white p-6">
        <div class="flex items-center justify-between">
          <!-- Left side - Student Info -->
          <div class="flex items-center gap-4">
            <div class="w-16 h-16 bg-gradient-to-r from-blue-600 to-blue-700 rounded-full flex items-center justify-center">
              <span class="text-white text-2xl font-bold">{{ studentInfo.initial }}</span>
            </div>
            <div>
              <h2 class="text-xl font-semibold text-gray-900">{{ studentInfo.name }}</h2>
              <div class="flex items-center gap-4 mt-1">
                <div class="flex items-center gap-2">
                  <span class="text-gray-500">Student ID:</span>
                  <span class="text-gray-900 font-medium">{{ studentInfo.id }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-gray-500">Grade Level:</span>
                  <span class="text-gray-900 font-medium">{{ studentInfo.grade }} {{ studentInfo.section }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Right side - Back Button -->
          <button @click="goBack" 
            class="flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-xl transition-all">
            <i class="pi pi-arrow-left"></i>
            <span>Back to List</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Remarks Section moved to header -->
    <div class="bg-blue-50 p-4 rounded-xl border border-blue-200 mb-6">
      <div class="flex justify-between items-start mb-2">
        <h3 class="text-lg font-semibold text-blue-800 flex items-center gap-2">
          <i class="pi pi-comments"></i>
          Teacher's Remarks
        </h3>
        <span class="text-sm text-blue-600">Last updated: {{ remarksDate }}</span>
      </div>
      <p class="text-blue-700 italic">
        Student has shown improvement in completing assignments on time. 
        Consistently participates in class activities and demonstrates good understanding of the subjects.
      </p>
    </div>

    <!-- Filters and Table Section -->
    <div class="bg-white p-6 rounded-2xl shadow-lg">
      <div class="flex flex-col space-y-6">
        <!-- Top row with statistics and search -->
        <div class="flex flex-wrap gap-4">
          <!-- Search on the left -->
          <div class="w-full lg:w-1/3">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search outputs..."
                class="w-full pl-12 pr-4 py-2.5 rounded-xl border border-gray-200 focus:border-blue-500 focus:ring focus:ring-blue-200 transition-all duration-200 text-gray-700 placeholder-gray-400"
              />
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <i class="pi pi-search text-gray-400"></i>
              </div>
            </div>
          </div>

          <!-- Statistics on the right -->
          <div class="grid grid-cols-3 gap-3 flex-1">
            <!-- Total Activities -->
            <div class="bg-gradient-to-br from-gray-50 to-gray-100 p-3 rounded-xl border border-gray-200 shadow-sm">
                <div class="flex items-center gap-2">
                    <div class="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                        <i class="pi pi-book text-lg text-gray-600"></i>
                    </div>
                    <div>
                        <p class="text-xs text-gray-600">Total Activities</p>
                        <p class="text-lg font-bold text-gray-800">{{ records.length }}</p>
                    </div>
                </div>
            </div>

            <!-- Completed -->
            <div class="bg-gradient-to-br from-green-50 to-green-100 p-3 rounded-xl border border-green-200 shadow-sm">
                <div class="flex items-center gap-2">
                    <div class="w-10 h-10 bg-green-200 rounded-full flex items-center justify-center">
                        <i class="pi pi-check text-lg text-green-600"></i>
                    </div>
                    <div>
                        <p class="text-xs text-green-600">Completed</p>
                        <p class="text-lg font-bold text-green-700">{{ completedCount }}</p>
                    </div>
                </div>
            </div>

            <!-- Pending -->
            <div class="bg-gradient-to-br from-red-50 to-red-100 p-3 rounded-xl border border-red-200 shadow-sm">
                <div class="flex items-center gap-2">
                    <div class="w-10 h-10 bg-red-200 rounded-full flex items-center justify-center">
                        <i class="pi pi-clock text-lg text-red-600"></i>
                    </div>
                    <div>
                        <p class="text-xs text-red-600">Pending</p>
                        <p class="text-lg font-bold text-red-700">{{ pendingCount }}</p>
                    </div>
                </div>
            </div>
          </div>
        </div>

        <!-- Search Results Notification -->
        <div v-if="searchQuery" 
          class="p-3 bg-blue-50 border border-blue-100 text-blue-700 rounded-xl flex items-center gap-2">
          <i class="pi pi-filter"></i>
          <span>Showing results for "<strong>{{ searchQuery }}</strong>"</span>
        </div>

        <!-- Updated DataTable -->
        <DataTable 
          :value="filteredRecords" 
          :scrollable="true" 
          scrollHeight="400px" 
          class="p-datatable-rounded"
          stripedRows
          showGridlines>
          <Column field="subject" header="Subject" class="font-semibold"></Column>
          <Column field="output" header="Output Name"></Column>
          <Column field="dueDate" header="Due Date"></Column>
          <Column field="time" header="Time"></Column>
          <Column field="status" header="Status">
            <template #body="slotProps">
              <Tag :value="slotProps.data.status" 
                   :severity="getStatusColor(slotProps.data.status)"
                   class="text-sm" />
            </template>
          </Column>
          <Column field="history" header="History">
            <template #body="slotProps">
              <span class="text-gray-600 text-sm">
                <i class="pi pi-clock mr-2"></i>
                {{ slotProps.data.history }}
              </span>
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { router } from '@inertiajs/vue3';
import InputText from "primevue/inputtext";
import Dropdown from "primevue/dropdown";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Tag from "primevue/tag";
import Button from "primevue/button";
import Card from "primevue/card";
import TeacherLayout from '@/Layouts/MainLayout.vue';

const searchQuery = ref("");

const records = ref([
    { subject: "Math", output: "Artwork 1", dueDate: "10/10/24 - 10/22/24", time: "12:00 PM", status: "Passed", history: "Last Edit 5 days ago" },
    { subject: "Science", output: "Artwork 2", dueDate: "12/12/24 - 12/16/24", time: "3:30 PM", status: "Missing", history: "Last Edit 2 days ago" },
    { subject: "English", output: "Artwork 3", dueDate: "12/12/24 - 12/16/24", time: "3:30 PM", status: "Missing", history: "Last Edit 2 days ago" },
    { subject: "Painting", output: "Landscape Painting", dueDate: "01/15/25 - 01/20/25", time: "2:00 PM", status: "Passed", history: "Last Edit 3 days ago" },
    { subject: "Sculpture", output: "Clay Modeling", dueDate: "02/10/25 - 02/15/25", time: "1:00 PM", status: "Missing", history: "Last Edit 1 day ago" },
    { subject: "Graphic Design", output: "Logo Design", dueDate: "03/05/25 - 03/10/25", time: "11:00 AM", status: "Passed", history: "Last Edit 4 days ago" }
]);

const filteredRecords = computed(() => {
    if (!searchQuery.value) return records.value;
    
    const query = searchQuery.value.toLowerCase();
    return records.value.filter(record => 
        record.subject.toLowerCase().includes(query) ||
        record.output.toLowerCase().includes(query) ||
        record.status.toLowerCase().includes(query) ||
        record.history.toLowerCase().includes(query)
    );
});

const getStatusColor = (status) => {
    switch (status) {
        case "Passed": return "success";
        case "Missing": return "danger";
        default: return "info";
    }
};

const props = defineProps({
    selectedStudent: {
        type: Object,
        required: false,
        default: () => ({
            id: 'N/A',
            name: 'Unknown Student',
            grade: 'Grade',
            section: 'Section'
        })
    }
});

// Add computed properties for student info
const studentInfo = computed(() => ({
    name: props.selectedStudent?.name || 'Unknown Student',
    id: props.selectedStudent?.id || 'N/A',
    grade: props.selectedStudent?.grade || 'Grade',
    section: props.selectedStudent?.section || 'Section',
    initial: (props.selectedStudent?.name || '?').charAt(0)
}));

// Update the onMounted hook to handle missing student data
onMounted(() => {
    console.log('Received student data:', props.selectedStudent);
    if (!props.selectedStudent?.id) {
        console.warn('No student data provided');
        router.visit(route('teacher.class'));
    }
});

const goBack = () => {
    router.visit(route('teacher.class'));
};

// Add remarks date
const remarksDate = ref(new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
}));

// Remove the percentage computeds since they're no longer needed
const completedCount = computed(() => {
    return records.value.filter(record => record.status === "Passed").length;
});

const pendingCount = computed(() => {
    return records.value.filter(record => record.status === "Missing").length;
});
</script>

<script>
export default {
    layout: TeacherLayout
};
</script>

<style scoped>
input:focus {
    outline: none;
}

:deep(.p-datatable) {
    border-radius: 0.75rem;
    overflow: hidden;
    margin-top: 1rem;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
    background-color: #f8fafc;
    color: #1e293b;
    font-weight: 600;
    padding: 1rem;
    border-bottom: 2px solid #e2e8f0;
}

:deep(.p-datatable .p-datatable-tbody > tr) {
    transition: background-color 0.2s;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
    background-color: #f1f5f9;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
    padding: 1rem;
}

/* Add this new style for better responsive layout */
@media (max-width: 1024px) {
    .lg\:w-64 {
        width: 100%;
    }
}

/* Add these styles for smooth transitions */
.bg-gradient-to-br {
    transition: all 0.3s ease;
}

.h-2 {
    transition: width 0.5s ease;
}
</style> 