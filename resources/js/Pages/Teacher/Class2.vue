<template>
    <div class="p-4">
        <!-- Meetings Card -->
        <div class="bg-white shadow-md rounded-lg overflow-hidden">
            <!-- Header -->
            <div class="px-6 py-4 border-b bg-white text-gray-700 font-semibold">
                Meetings
            </div>

            <!-- Meeting List -->
            <div class="p-4">
                <div
                    v-for="(meeting, index) in meetings"
                    :key="index"
                    class="flex items-center p-4 rounded-lg mb-2 cursor-pointer bg-gray-300 hover:bg-gray-400 transition-all"
                    @click="openStartMeetingModal(meeting)"
                >
                    <span class="flex-1 font-medium text-gray-700">{{ meeting.subject }}</span>
                    <span class="flex-1 text-center text-gray-600">{{ meeting.pupil }}</span>
                    <span class="flex-1 text-right text-gray-700">{{ meeting.day }} {{ meeting.time }}</span>

                    <!-- Edit Button (Separately Clickable) -->
                    <button
                        class="ml-3 p-2 rounded-md bg-transparent hover:bg-gray-400 transition-all"
                        @click.stop="openEditMeetingModal(meeting, index, $event)"
                    >
                        <i class="pi pi-pencil text-gray-700"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Start Meeting Modal -->
    <div v-if="showStartMeetingModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg shadow-md w-96">
            <h2 class="text-lg font-semibold mb-4">Start Meeting</h2>
            <p><strong>Subject:</strong> {{ selectedMeeting.subject }}</p>
            <p><strong>Pupil:</strong> {{ selectedMeeting.pupil }}</p>
            <p><strong>Date:</strong> {{ selectedMeeting.day }}</p>
            <p><strong>Time:</strong> {{ selectedMeeting.time }}</p>

            <div class="flex justify-end space-x-2 mt-4">
                <button @click="closeStartMeetingModal" class="px-4 py-2 bg-red-500 text-white rounded-md">Cancel</button>
                <button class="px-4 py-2 bg-blue-600 text-white rounded-md">Start</button>
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
                <div class="relative">
                    <select v-model="selectedMeeting.day" class="w-full p-2 border rounded-md">
                        <option v-for="day in daysOfWeek" :key="day" :value="day">{{ day }}</option>
                    </select>
                </div>
            </div>

            <div class="mb-4">
                <label class="block text-gray-600 mb-1">Edit Time:</label>
                <div class="relative flex items-center">
                    <i class="pi pi-clock text-gray-500 absolute left-2"></i>
                    <input type="text" v-model="selectedMeeting.time" class="w-full p-2 border rounded-md pl-8" />
                </div>
            </div>

            <div class="flex justify-end space-x-2">
                <button @click="closeEditMeetingModal" class="px-4 py-2 bg-red-500 text-white rounded-md">Cancel</button>
                <button @click="saveMeetingChanges" class="px-4 py-2 bg-blue-600 text-white rounded-md">Save</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const meetings = ref([
    {
        subject: 'Math',
        pupil: 'MikeJerome Madulara',
        day: 'Friday',
        time: '6:00PM - 8:00PM'
    }
]);

const showStartMeetingModal = ref(false);
const showEditMeetingModal = ref(false);
const selectedMeeting = ref(null);
const selectedMeetingIndex = ref(null);

const openStartMeetingModal = (meeting) => {
    selectedMeeting.value = meeting;
    showStartMeetingModal.value = true;
};

const closeStartMeetingModal = () => {
    showStartMeetingModal.value = false;
};

const openEditMeetingModal = (meeting, index, event) => {
    event.stopPropagation();
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

const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
</script>

<style scoped>
/* Match the exact gray background */
.bg-gray-300 {
    background-color: #b3d9ff;
}

.text-gray-700 {
    color: #374151;
}

.text-gray-600 {
    color: #4B5563;
}

.hover\:bg-gray-400:hover {
    background-color: #BFBFBF;
}

/* Make sure the row is rounded properly */
.rounded-lg {
    border-radius: 8px;
}

/* Transition effect */
.transition-all {
    transition: all 0.2s ease-in-out;
}
</style>
