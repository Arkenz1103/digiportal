<template>
    <div class="p-6">
        <!-- Pupils Card -->
        <div class="bg-white shadow-md rounded-lg overflow-hidden">
            <!-- Header -->
            <div class="px-6 py-4 border-b bg-white text-gray-700 font-semibold">
                Pupils
            </div>

            <!-- Pupils List -->
            <div class="p-4">
                <div
                    v-for="(pupil, index) in pupils"
                    :key="index"
                    class="flex items-center p-4 rounded-lg mb-2 cursor-pointer bg-blue-200 hover:bg-blue-300 transition-all"
                >
                    <span class="flex-1 font-medium text-gray-700">{{ pupil.name }}</span>
                    <span class="flex-1 text-center text-gray-600">{{ pupil.subject }}</span>

                    <!-- Schedule Button -->
                    <button
                        class="ml-3 p-2 rounded-md bg-white hover:bg-gray-300 transition-all"
                        @click="openScheduleModal(pupil)"
                    >
                        <i class="pi pi-pencil text-gray-700"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Schedule Meeting Modal -->
    <div v-if="showScheduleModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg shadow-md w-96">
            <h2 class="text-lg font-semibold mb-4">Schedule Meeting</h2>

            <p><strong>Pupil:</strong> {{ selectedPupil.name }}</p>
            <p><strong>Subject:</strong> {{ selectedPupil.subject }}</p>

            <!-- Select Day -->
            <div class="mb-4">
                <label class="block text-gray-600 mb-1">Select Day:</label>
                <select v-model="meetingDay" class="w-full p-2 border rounded-md">
                    <option v-for="day in daysOfWeek" :key="day" :value="day">{{ day }}</option>
                </select>
            </div>

            <!-- Styled Time Picker -->
            <div class="mb-4">
                <label class="block text-gray-600 mb-1">Select Time:</label>
                <div class="relative flex items-center">
                    <i class="pi pi-clock text-gray-500 absolute left-2"></i>
                    <input
                        type="text"
                        v-model="meetingTime"
                        class="w-full p-2 border rounded-md pl-8"
                        placeholder="HH:MM AM/PM"
                    />
                </div>
            </div>

            <div class="flex justify-end space-x-2">
                <button @click="closeScheduleModal" class="px-4 py-2 bg-red-500 text-white rounded-md">Cancel</button>
                <button @click="scheduleMeeting" class="px-4 py-2 bg-blue-600 text-white rounded-md">Save</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { router } from '@inertiajs/vue3';

// Sample pupil data
const pupils = ref([
    { name: 'MikeJerome Madulara', subject: 'Math' },
    { name: 'Sherry Jean Codaste', subject: 'Science' },

]);

const showScheduleModal = ref(false);
const selectedPupil = ref(null);
const meetingDay = ref('');
const meetingTime = ref('');

const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

const openScheduleModal = (pupil) => {
    selectedPupil.value = pupil;
    showScheduleModal.value = true;
};

const closeScheduleModal = () => {
    showScheduleModal.value = false;
};

// Schedule Meeting and Redirect to Meetings Page
const scheduleMeeting = () => {
    if (!meetingDay.value || !meetingTime.value) {
        alert("Please select a day and time.");
        return;
    }

    // Example: Store the meeting (in a real app, save to the backend)
    const newMeeting = {
        subject: selectedPupil.value.subject,
        pupil: selectedPupil.value.name,
        day: meetingDay.value,
        time: meetingTime.value,
    };

    localStorage.setItem('newMeeting', JSON.stringify(newMeeting)); // Simulating a backend save

    // Close modal and redirect
    closeScheduleModal();
    router.visit('/meetings'); // Redirects to the meetings page
};
</script>

<style scoped>
.bg-blue-200 {
    background-color: #b3d9ff;
}
.hover\:bg-blue-300:hover {
    background-color: #99ccff;
}
</style>
