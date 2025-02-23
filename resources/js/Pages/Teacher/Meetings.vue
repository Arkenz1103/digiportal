<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <!-- Meetings for Today -->
    <div class="bg-white shadow-lg rounded-xl p-6 mb-6 border border-blue-200">
      <h2 class="text-2xl font-bold text-gray-700 mb-4">Meetings for Today</h2>
      <div v-if="todayMeetings.length" class="space-y-3">
        <div v-for="(meeting, index) in todayMeetings" :key="index"
             class="flex justify-between items-center p-4 bg-white border border-blue-300 rounded-lg shadow-md cursor-pointer hover:bg-blue-50 transition"
             @click="openStartMeetingPrompt(meeting)">
          <span class="font-semibold text-blue-900">{{ meeting.subject }}</span>
          <span class="text-gray-700">{{ meeting.pupil }}</span>
          <span class="text-gray-600">{{ meeting.day }} {{ meeting.time }}</span>
          <button @click.stop.prevent="openEditForm(meeting)" class="text-blue-600 hover:text-blue-800 z-10 relative">
            <i class="pi pi-pencil"></i>
          </button>
        </div>
      </div>
      <p v-else class="text-gray-500 text-sm">No meetings for today</p>
    </div>

    <!-- Pending Meetings -->
    <div class="bg-white shadow-lg rounded-xl p-6 border border-gray-200">
      <h2 class="text-2xl font-bold text-gray-700 mb-4">Pending Meetings</h2>
      <div v-if="pendingMeetings.length" class="space-y-3">
        <div v-for="(meeting, index) in pendingMeetings" :key="index"
             class="flex justify-between items-center p-4 bg-white border border-gray-300 rounded-lg shadow-md cursor-pointer hover:bg-blue-50 transition"
             @click="openStartMeetingPrompt(meeting)">
          <span class="font-semibold text-gray-900">{{ meeting.subject }}</span>
          <span class="text-gray-700">{{ meeting.pupil }}</span>
          <span class="text-gray-600">{{ meeting.day }} {{ meeting.time }}</span>
          <button @click.stop.prevent="openEditForm(meeting)" class="text-gray-600 hover:text-gray-800 z-10 relative">
            <i class="pi pi-pencil"></i>
          </button>
        </div>
      </div>
      <p v-else class="text-gray-500 text-sm">No pending meetings</p>
    </div>

    <!-- Start Meeting Modal -->
    <div v-if="showStartMeetingPrompt" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded-xl shadow-lg w-96">
        <h2 class="text-xl font-bold text-gray-700 mb-4">Start Meeting</h2>
        <p class="text-gray-600">Do you want to start the meeting early?</p>
        <div class="mt-4 flex justify-end space-x-2">
            <button @click="closeStartMeetingPrompt" class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600">Cancel</button>
          <button @click="startMeeting" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Start Meeting</button>

        </div>
      </div>
    </div>

    <!-- Edit Meeting Modal -->
    <div v-if="showEditForm" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded-xl shadow-lg w-96">
        <h2 class="text-xl font-bold text-gray-700 mb-4">Edit Meeting</h2>

        <label class="block text-sm font-medium text-gray-700">Subject</label>
        <input v-model="editingMeeting.subject" class="w-full p-2 border rounded-lg mb-3 bg-gray-100 text-gray-700" type="text" disabled>

        <label class="block text-sm font-medium text-gray-700">Pupil</label>
        <input v-model="editingMeeting.pupil" class="w-full p-2 border rounded-lg mb-3 bg-gray-100 text-gray-700" type="text" disabled>

        <label class="block text-sm font-medium text-gray-700">Day</label>
        <select v-model="editingMeeting.day" class="w-full p-2 border rounded-lg mb-3 text-gray-600">
          <option v-for="day in daysOfWeek" :key="day" :value="day">{{ day }}</option>
        </select>

        <label class="block text-sm font-medium text-gray-700">Time</label>
        <input v-model="editingMeeting.time" class="w-full p-2 border rounded-lg mb-3 text-gray-600" type="text">

        <div class="flex justify-end space-x-2">
          <button @click="closeEditForm" class="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500">Cancel</button>
          <button @click="saveEdit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue';

const meetings = ref([
  { subject: 'Math', pupil: 'MikeJerome Madulara', day: 'Friday', time: '6:00PM - 8:00PM' },
  { subject: 'Math', pupil: 'Ryan Mondega', day: 'Friday', time: '8:00PM - 9:00PM' },
  { subject: 'English', pupil: 'Sherry Jean Codaste', day: 'Saturday', time: '6:00PM - 8:00PM' },
  { subject: 'Science', pupil: 'Cherry Ann Pitalgo', day: 'Sunday', time: '8:00PM - 9:00PM' }
]);

const todayDay = new Date().toLocaleString('en-US', { weekday: 'long' });
const todayMeetings = computed(() => meetings.value.filter(meeting => meeting.day === todayDay));
const pendingMeetings = computed(() => meetings.value.filter(meeting => meeting.day !== todayDay));

const showStartMeetingPrompt = ref(false);
const selectedMeeting = ref(null);
const showEditForm = ref(false);
const editingMeeting = reactive({});
const daysOfWeek = ref(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']);

const openStartMeetingPrompt = (meeting) => {
  selectedMeeting.value = meeting;
  showStartMeetingPrompt.value = true;
};

const closeStartMeetingPrompt = () => {
  showStartMeetingPrompt.value = false;
};

const startMeeting = () => {
  alert(`Starting meeting for ${selectedMeeting.value.subject} with ${selectedMeeting.value.pupil}`);
  closeStartMeetingPrompt();
};

const openEditForm = (meeting) => {
  Object.assign(editingMeeting, meeting);
  showEditForm.value = true;
};

const closeEditForm = () => {
  showEditForm.value = false;
};

const saveEdit = () => {
  const index = meetings.value.findIndex(m => m.pupil === editingMeeting.pupil);
  if (index !== -1) {
    meetings.value[index] = { ...editingMeeting };
  }
  closeEditForm();
};
</script>
