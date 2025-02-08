<template>
  <div class="p-6 w-full max-w-4xl mx-auto bg-white shadow-lg rounded-lg">
    <!-- Calendar Header -->
    <h2 class="text-3xl font-bold mb-4 text-center text-blue-700">NOVEMBER 2025</h2>

    <!-- Days of the Week -->
    <div class="grid grid-cols-7 text-center font-semibold text-gray-700 mb-2 bg-gray-100 p-2 rounded-md">
      <div>Monday</div>
      <div>Tuesday</div>
      <div>Wednesday</div>
      <div>Thursday</div>
      <div>Friday</div>
      <div class="text-red-500">Saturday</div>
      <div class="text-red-500">Sunday</div>
    </div>

    <!-- Calendar Grid -->
    <div class="grid grid-cols-7 gap-2 text-center">
      <!-- Empty Spaces for the Start of the Month -->
      <div v-for="i in 3" :key="'empty-' + i"></div>

      <!-- Dates with Subjects -->
      <div v-for="(subject, date) in schedule" :key="date"
           class="p-4 border rounded-lg shadow-md bg-gray-50 hover:bg-blue-100 cursor-pointer transition"
           :class="{'bg-red-200': date + 1 === 15}"
           @click="handleClick(date + 1)">
        <div class="text-lg font-bold">{{ date + 1 }}</div>
        <div class="text-sm text-gray-600">{{ subject }}</div>
      </div>
    </div>

    <!-- Schedule List Below Calendar in Columns -->
    <div class="mt-6 p-4 border-t bg-gray-50 rounded-lg shadow-md">
      <h3 class="text-xl font-bold mb-4 text-blue-700">Daily Schedule</h3>
      <div class="grid grid-cols-2 gap-4">
        <div v-for="(subject, date) in schedule" :key="'list-' + date" class="mb-2 p-3 bg-white shadow-sm rounded-md">
          <strong class="text-blue-700">November {{ date + 1 }}:</strong> {{ subject }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      subjects: ["Math", "English", "Science", "Art", "Music", "PE", "Reading"],
      schedule: [],
    };
  },
  created() {
    this.generateSchedule();
  },
  methods: {
    generateSchedule() {
      this.schedule = Array.from({ length: 30 }, () => {
        return this.subjects[Math.floor(Math.random() * this.subjects.length)];
      });
    },
    handleClick(date) {
      alert(`Schedule for November ${date}: ${this.schedule[date - 1]}`);
    },
  },
};
</script>
