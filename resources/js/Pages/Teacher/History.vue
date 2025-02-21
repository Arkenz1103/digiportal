<template>
  <div class="p-6 bg-white rounded-lg shadow-md">
    <h2 class="text-3xl font-bold mb-6 text-gray-800">Meeting History</h2>

    <!-- History List -->
    <div class="space-y-4">
      <div
        v-for="history in meetingHistory"
        :key="history.id"
        class="p-4 rounded-lg shadow-sm border-l-4 transition-all duration-200 bg-gray-100 border-gray-300 hover:bg-gray-200"
      >
        <div class="flex justify-between items-center">
          <div>
            <p class="text-gray-800 font-semibold">Date: {{ formatDate(history.date) }}</p>
            <p class="text-gray-600 text-sm">Time: {{ formatTime(history.startTime) }} - {{ formatTime(history.endTime) }}</p>
            <p class="text-gray-600 text-sm">Duration: {{ history.duration }} minutes</p>
            <p class="text-gray-600 text-sm">Quiz Score: <span class="font-bold text-blue-600">{{ history.quizScore }}/100</span></p>
          </div>
        </div>
      </div>

      <!-- No History Message -->
      <p v-if="meetingHistory.length === 0" class="text-gray-500 text-center">
        No past meetings available.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      meetingHistory: [
        {
          id: 1,
          date: "2025-02-10",
          startTime: "10:00",
          endTime: "10:45",
          duration: 45,
          quizScore: 85,
        },
        {
          id: 2,
          date: "2025-02-15",
          startTime: "14:00",
          endTime: "14:50",
          duration: 50,
          quizScore: 90,
        },
        {
          id: 3,
          date: "2025-02-18",
          startTime: "09:30",
          endTime: "10:15",
          duration: 45,
          quizScore: 78,
        },
      ],
    };
  },
  methods: {
    formatDate(date) {
      return new Intl.DateTimeFormat("en-US", { dateStyle: "medium" }).format(new Date(date));
    },
    formatTime(time) {
      const [hours, minutes] = time.split(":");
      const date = new Date();
      date.setHours(hours, minutes);
      return date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" });
    },
  },
};
</script>

