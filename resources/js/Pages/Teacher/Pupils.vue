<template>
    <div class="p-6">
        <!-- Pupils Management Card -->
        <div class="bg-white shadow-md rounded-lg overflow-hidden">
            <!-- Header -->
            <div class="px-6 py-4 border-b bg-white text-gray-700 font-semibold text-xl">
                Pupils
            </div>

            <!-- Controls: Search, Filter, and Sort -->
            <div class="flex flex-wrap items-center gap-4 p-4">
                <!-- Search Input -->
                <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Search for a pupil"
                    class="w-full md:w-1/3 p-2 border rounded-md focus:ring focus:ring-blue-300"
                />

                <!-- Filter by Subject -->
                <select v-model="selectedSubject" class="w-full md:w-1/4 p-2 border rounded-md">
                    <option value="">Filter by subject</option>
                    <option v-for="subject in subjects" :key="subject" :value="subject">
                        {{ subject }}
                    </option>
                </select>

                <!-- Sort By -->
                <select v-model="sortBy" class="w-full md:w-1/4 p-2 border rounded-md">
                    <option value="">Sort by</option>
                    <option value="name">Name</option>
                    <option value="subject">Subject</option>
                </select>
            </div>

            <!-- Pupils Table -->
            <div class="overflow-x-auto">
                <table class="w-full border-collapse">
                    <thead class="bg-gray-100 text-gray-700">
                        <tr>
                            <th class="p-3 text-left">Pupil Name</th>
                            <th class="p-3 text-left">Subject</th>
                            <th class="p-3 text-left">Status</th>
                            <th class="p-3 text-left">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="(pupil, index) in filteredPupils"
                            :key="index"
                            class="border-t hover:bg-gray-50"
                        >
                            <td class="p-3">{{ pupil.name }}</td>
                            <td class="p-3">{{ pupil.subject }}</td>
                            <td class="p-3">
                                <span
                                    class="px-2 py-1 rounded-md text-xs"
                                    :class="{
                                        'bg-green-100 text-green-700': pupil.scheduled,
                                        'bg-red-100 text-red-600': !pupil.scheduled
                                    }"
                                >
                                    {{ pupil.scheduled ? 'Scheduled' : 'Not Scheduled' }}
                                </span>
                            </td>
                            <td class="p-3">
                                <button
                                    v-if="!pupil.scheduled"
                                    class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                                    @click="openScheduleModal(pupil)"
                                >
                                    Schedule
                                </button>
                                <span
                                    v-else
                                    class="bg-gray-300 text-gray-700 px-4 py-2 rounded-md cursor-not-allowed"
                                >
                                    Scheduled 
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
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
import { ref, computed } from 'vue';
import { router } from '@inertiajs/vue3';

// Sample pupil data
const pupils = ref([
    { name: 'MikeJerome Madulara', subject: 'Math', scheduled: false },
    { name: 'John Doe', subject: 'Science', scheduled: false },
    { name: 'Jane Smith', subject: 'English', scheduled: true },
]);

// Search, Filter, and Sort
const searchQuery = ref('');
const selectedSubject = ref('');
const sortBy = ref('');
const subjects = ['Math', 'Science', 'English'];

const filteredPupils = computed(() => {
    let result = pupils.value;

    // Search by name
    if (searchQuery.value) {
        result = result.filter((pupil) =>
            pupil.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        );
    }

    // Filter by subject
    if (selectedSubject.value) {
        result = result.filter((pupil) => pupil.subject === selectedSubject.value);
    }

    // Sort by name or subject
    if (sortBy.value === 'name') {
        result = result.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy.value === 'subject') {
        result = result.sort((a, b) => a.subject.localeCompare(b.subject));
    }

    return result;
});

// Scheduling logic
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

// Schedule Meeting and Update Status
const scheduleMeeting = () => {
    if (!meetingDay.value || !meetingTime.value) {
        alert("Please select a day and time.");
        return;
    }

    // Update pupil status
    selectedPupil.value.scheduled = true;

    // Save meeting (simulated)
    const newMeeting = {
        subject: selectedPupil.value.subject,
        pupil: selectedPupil.value.name,
        day: meetingDay.value,
        time: meetingTime.value,
    };

    localStorage.setItem('newMeeting', JSON.stringify(newMeeting));

    // Close modal and redirect
    closeScheduleModal();
    router.visit('/meetings');
};
</script>
