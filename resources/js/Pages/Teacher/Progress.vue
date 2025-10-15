<template>
  <div class="p-6 max-w-7xl mx-auto min-h-screen bg-gradient-to-br from-indigo-50 via-violet-50 to-blue-50">
    <!-- Header Section with Student Info -->
    <div class="bg-white/80 backdrop-blur-sm rounded-xl shadow-sm overflow-hidden mb-6 border border-indigo-100">
      <div class="bg-gradient-to-r from-indigo-50 to-white p-6">
        <!-- Student Info Section -->
        <div class="flex flex-col">
          <div class="flex items-start justify-between">
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 bg-gradient-to-r from-indigo-600 to-violet-600 rounded-full flex items-center justify-center">
                <span class="text-white text-2xl font-bold">{{ studentInfo.initial }}</span>
              </div>
              <div>
                <h2 class="text-xl font-semibold text-indigo-900">{{ studentInfo.name }}</h2>
                <div class="flex items-center gap-4 mt-1">
                  <div class="flex items-center gap-2">
                    <span class="text-indigo-700">Student ID:</span>
                    <span class="text-indigo-900 font-medium">{{ studentInfo.id }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Back Button -->
            <button @click="goBack" 
              class="flex items-center gap-2 px-4 py-2 bg-indigo-100 text-indigo-700 hover:bg-indigo-200 rounded-lg transition-all">
              <i class="pi pi-arrow-left"></i>
              <span>Back to Student Progress</span>
            </button>
          </div>

          <!-- Teacher's Remarks Section -->
          <div class="mt-6 bg-indigo-50 p-4 rounded-lg border border-indigo-100">
            <div class="flex justify-between items-center mb-3">
              <div class="flex items-center gap-2">
                <i class="pi pi-comments text-indigo-600"></i>
                <h3 class="text-lg font-semibold text-indigo-900">Teacher's Remarks</h3>
                <span class="text-sm text-white bg-gradient-to-r from-indigo-500 to-violet-500 px-2 py-0.5 rounded-full">{{ remarksDate }}</span>
              </div>
              <button @click="openRemarksDialog" class="text-sm text-indigo-600 hover:text-indigo-800 font-medium transition-colors flex items-center gap-1">
                View All
                <i class="pi pi-angle-right text-xs"></i>
              </button>
            </div>
            <p class="text-indigo-900/80 leading-relaxed">
              "{{ studentInfo.name }}" has shown consistent improvement in completing assignments on time. 
              Actively participates in class discussions and demonstrates a strong understanding of course material. 
              Shows particular strength in creative problem-solving.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Table Section -->
    <div class="bg-white/80 backdrop-blur-sm p-6 rounded-xl shadow-sm border border-indigo-100">
      <div class="flex flex-col space-y-6">
        <!-- Top row with statistics and search -->
        <div class="flex flex-col lg:flex-row gap-4">
          <!-- Search on the left -->
          <div class="w-full lg:w-1/3">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search outputs..."
                class="w-full pl-12 pr-4 py-2.5 rounded-lg border border-indigo-200 focus:border-indigo-500 focus:ring focus:ring-indigo-200 transition-all duration-200 text-gray-700 placeholder-indigo-400"
              />
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <i class="pi pi-search text-indigo-500"></i>
              </div>
            </div>
          </div>

            <!-- Statistics on the right -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 flex-1">
            <!-- Total Activities -->
            <div class="bg-gradient-to-br from-indigo-50 to-white p-4 rounded-lg border border-indigo-100 shadow-sm">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center">
                        <i class="pi pi-book text-xl text-indigo-600"></i>
                    </div>
                    <div>
                        <p class="text-xs text-indigo-600">Total Activities</p>
                        <p class="text-lg font-bold text-indigo-900">{{ records.length }}</p>
                    </div>
                </div>
            </div>

            <!-- Completed -->
            <div class="bg-gradient-to-br from-green-50 to-white p-4 rounded-lg border border-green-100 shadow-sm">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                        <i class="pi pi-check text-xl text-green-600"></i>
                    </div>
                    <div>
                        <p class="text-xs text-green-600">Completed</p>
                        <p class="text-lg font-bold text-indigo-900">{{ completedCount }}</p>
                    </div>
                </div>
            </div>

            <!-- Pending -->
            <div class="bg-gradient-to-br from-amber-50 to-white p-4 rounded-lg border border-amber-100 shadow-sm">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center">
                        <i class="pi pi-clock text-xl text-amber-600"></i>
                    </div>
                    <div>
                        <p class="text-xs text-amber-600">Pending</p>
                        <p class="text-lg font-bold text-indigo-900">{{ pendingCount }}</p>
                    </div>
                </div>
            </div>
          </div>
        </div>

        <!-- Search Results Notification -->
        <div v-if="searchQuery" 
          class="p-3 bg-indigo-50 border border-indigo-200 text-indigo-900 rounded-lg flex items-center gap-2">
          <i class="pi pi-filter text-indigo-600"></i>
          <span>Showing results for "<strong class="font-medium">{{ searchQuery }}</strong>"</span>
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
                <i class="pi pi-clock mr-2 text-[#7BBBFE]"></i>
                {{ slotProps.data.history }}
              </span>
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>

  <!-- Remarks History Dialog -->
  <Dialog v-model:visible="showRemarksDialog" modal header="Remarks History" :style="{width: '50vw'}" class="p-fluid">
    <div class="space-y-4">
      <!-- Current Remarks -->
      <div class="bg-indigo-50 p-4 rounded-lg border border-indigo-100">
        <div class="flex items-center justify-between mb-3">
          <span class="font-semibold text-indigo-900">Current Remarks</span>
          <span class="text-sm text-white bg-gradient-to-r from-indigo-500 to-violet-500 px-3 py-1 rounded-full">{{ remarksDate }}</span>
        </div>
        <p class="text-indigo-900/80 leading-relaxed">
          "{{ studentInfo.name }}" has shown consistent improvement in completing assignments on time. 
          Actively participates in class discussions and demonstrates a strong understanding of course material. 
          Shows particular strength in creative problem-solving.
        </p>
      </div>

      <!-- Previous Remarks -->
      <div v-for="(remark, index) in remarksHistory" :key="index" 
           class="bg-white p-4 rounded-lg border border-indigo-100 shadow-sm">
        <div class="flex items-center justify-between mb-2">
          <span class="font-semibold text-indigo-900">Previous Remarks</span>
          <span class="text-sm text-indigo-600">{{ remark.date }}</span>
        </div>
        <p class="text-indigo-900/80 leading-relaxed">{{ remark.content }}</p>
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';

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
            name: 'Unknown Student'
        })
    }
});

const studentInfo = computed(() => ({
    name: props.selectedStudent?.name || 'Unknown Student',
    id: props.selectedStudent?.id || 'N/A',
    initial: (props.selectedStudent?.name || '?').charAt(0)
}));

onMounted(() => {
    console.log('Received student data:', props.selectedStudent);
    if (!props.selectedStudent?.id) {
        console.warn('No student data provided');
        router.visit(route('teacher.class'));
    }
});

const goBack = () => {
    router.visit(route('teacher.sprogress'));
};

const remarksDate = ref(new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
}));

const showRemarksDialog = ref(false);
const remarksHistory = ref([
    {
        date: '2025-05-10',
        content: 'Student shows good progress in recent assignments. Participation in group activities has improved significantly.'
    },
    {
        date: '2025-05-03',
        content: 'Completed all assignments for the week. Needs to work on time management for future projects.'
    },
    {
        date: '2025-04-26',
        content: 'Excellent performance in recent project presentation. Shows strong leadership qualities in team activities.'
    }
]);

const openRemarksDialog = () => {
    showRemarksDialog.value = true;
};

const completedCount = computed(() => {
    return records.value.filter(record => record.status === "Passed").length;
});

const pendingCount = computed(() => {
    return records.value.filter(record => record.status === "Missing").length;
});
</script>

<script>
import TeacherLayout from '@/Layouts/MainLayout.vue';

export default {
    layout: TeacherLayout
};
</script>

<style scoped>
input:focus {
    outline: none;
    @apply ring-2 ring-indigo-200 border-indigo-400;
}

:deep(.p-datatable) {
    @apply rounded-lg overflow-hidden mt-4 border border-indigo-100;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
    @apply bg-indigo-50 text-indigo-900 font-semibold p-4 border-b border-indigo-100;
}

:deep(.p-datatable .p-datatable-tbody > tr) {
    @apply transition-colors duration-200;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
    @apply bg-indigo-50;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
    @apply p-4 border-b border-indigo-50;
}

:deep(.p-datatable .p-datatable-tbody > tr:last-child > td) {
    @apply border-b-0;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
    .lg\:w-64 {
        @apply w-full;
    }
}

/* Smooth transitions */
.bg-gradient-to-br {
    @apply transition-all duration-300 ease-in-out;
}

/* Custom scrollbar */
:deep(::-webkit-scrollbar) {
    @apply w-2 h-2;
}

:deep(::-webkit-scrollbar-track) {
    @apply bg-indigo-50 rounded-full;
}

:deep(::-webkit-scrollbar-thumb) {
    @apply bg-indigo-200 rounded-full hover:bg-indigo-300;
}

/* Dialog styles */
:deep(.p-dialog) {
    @apply rounded-xl overflow-hidden shadow-xl border border-indigo-100;
}

:deep(.p-dialog .p-dialog-header) {
    @apply bg-indigo-50 border-b border-indigo-100 p-4;
}

:deep(.p-dialog .p-dialog-content) {
    @apply bg-white p-6;
}

:deep(.p-dialog .p-dialog-footer) {
    @apply bg-indigo-50 border-t border-indigo-100 p-4 flex justify-end gap-2;
}

/* Tag styles */
:deep(.p-tag) {
    @apply px-3 py-1.5 text-sm rounded-lg;
}

:deep(.p-tag.p-tag-success) {
    @apply bg-green-100 text-green-800 border border-green-200;
}

:deep(.p-tag.p-tag-danger) {
    @apply bg-red-100 text-red-800 border border-red-200;
}

:deep(.p-tag.p-tag-warning) {
    @apply bg-amber-100 text-amber-800 border border-amber-200;
}

:deep(.p-tag.p-tag-info) {
    @apply bg-blue-100 text-blue-800 border border-blue-200;
}
</style>