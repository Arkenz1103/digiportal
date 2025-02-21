<template>
    <div class="p-6">
        <!-- Meetings Header -->
        <div class="bg-white shadow-md rounded-lg p-6">
            <h1 class="text-2xl font-bold text-gray-800 mb-4">Meetings</h1>

            <!-- Search & Filters -->
            <div class="flex justify-between mb-4">
                <input
                    type="text"
                    v-model="searchQuery"
                    placeholder="Search for a meeting"
                    class="p-2 border rounded-lg w-1/3"
                />
                <select v-model="filterDay" class="p-2 border rounded-lg w-1/3">
                    <option value="">Filter by day</option>
                    <option v-for="day in daysOfWeek" :key="day" :value="day">{{ day }}</option>
                </select>
                <button @click="openAddMeetingModal" class="bg-blue-600 text-white px-4 py-2 rounded-lg">
                    + Add Meeting
                </button>
            </div>

            <!-- Meetings Table -->
            <div class="overflow-hidden rounded-lg shadow">
                <table class="w-full border-collapse">
                    <thead>
                        <tr class="bg-gray-100 text-gray-700 text-left">
                            <th class="p-3">SUBJECT</th>
                            <th class="p-3">PUPIL</th>
                            <th class="p-3">DAY & TIME</th>
                            <th class="p-3 text-right">ACTIONS</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="(meeting, index) in filteredMeetings"
                            :key="index"
                            class="border-t hover:bg-gray-100 transition-all"
                        >
                            <td class="p-3">{{ meeting.subject }}</td>
                            <td class="p-3">{{ meeting.pupil }}</td>
                            <td class="p-3">{{ meeting.day }} {{ meeting.time }}</td>
                            <td class="p-3 text-right">
                                <button @click="openEditMeetingModal(meeting, index)" class="text-blue-600">
                                    <i class="pi pi-pencil"></i>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Edit Meeting Modal -->
    <div v-if="showEditMeetingModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg shadow-md w-96">
            <h2 class="text-lg font-semibold mb-4">Edit Meeting Schedule</h2>

            <!-- Edit Form -->
            <div class="mb-4">
                <label class="block text-gray-600 mb-1">Select Day:</label>
                <select v-model="selectedMeeting.day" class="w-full p-2 border rounded-md">
                    <option v-for="day in daysOfWeek" :key="day" :value="day">{{ day }}</option>
                </select>
            </div>

            <div class="mb-4">
                <label class="block text-gray-600 mb-1">Edit Time:</label>
                <input type="text" v-model="selectedMeeting.time" class="w-full p-2 border rounded-md" />
            </div>

            <div class="flex justify-end space-x-2">
                <button @click="closeEditMeetingModal" class="px-4 py-2 bg-red-500 text-white rounded-md">Cancel</button>
                <button @click="saveMeetingChanges" class="px-4 py-2 bg-blue-600 text-white rounded-md">Save</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const meetings = ref([
    { subject: 'Math', pupil: 'MikeJerome Madulara', day: 'Friday', time: '6:00PM - 8:00PM' },
    { subject: 'Science', pupil: 'Jane Doe', day: 'Wednesday', time: '4:00PM - 5:00PM' }
]);

const searchQuery = ref('');
const filterDay = ref('');
const showEditMeetingModal = ref(false);
const selectedMeeting = ref(null);
const selectedMeetingIndex = ref(null);

const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

const filteredMeetings = computed(() => {
    return meetings.value.filter(meeting => {
        return (
            (!searchQuery.value || meeting.subject.toLowerCase().includes(searchQuery.value.toLowerCase())) &&
            (!filterDay.value || meeting.day === filterDay.value)
        );
    });
});

const openEditMeetingModal = (meeting, index) => {
    selectedMeeting.value = { ...meeting };
    selectedMeetingIndex.value = index;
    showEditMeetingModal.value = true;
};

const closeEditMeetingModal = () => {
    showEditMeetingModal.value = false;
};

const saveMeetingChanges = () => {
    if (selectedMeetingIndex.value !== null) {
        meetings.value[selectedMeetingIndex.value] = { ...selectedMeeting.value };
    }
    closeEditMeetingModal();
};
</script>

<style scoped>
/* Consistent Font & Text Size */
h1 {
    font-size: 1.5rem;
}

th {
    font-weight: bold;
}

table {
    width: 100%;
}

td {
    padding: 12px;
}

/* Hover Effect */
tr:hover {
    background-color: #f1f5f9;
}
</style>
