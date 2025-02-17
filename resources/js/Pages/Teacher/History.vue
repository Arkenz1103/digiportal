<template>
  <div class="flex flex-col md:flex-row gap-6 p-4 w-full max-w-6xl mx-auto">
    <!-- Calendar Section (Left) -->
    <div class="w-full md:w-2/3 p-4 border rounded-lg shadow-lg bg-white">
      <h2 class="text-2xl font-bold mb-4 text-center">📅 NOVEMBER 2025</h2>

      <!-- Days of the Week -->
      <div class="grid grid-cols-7 text-center font-semibold text-gray-600 mb-2">
        <div>Mon</div>
        <div>Tue</div>
        <div>Wed</div>
        <div>Thu</div>
        <div>Fri</div>
        <div>Sat</div>
        <div>Sun</div>
      </div>

      <!-- Calendar Grid -->
      <div class="grid grid-cols-7 gap-1 text-center">
        <!-- Empty Spaces for the Start of the Month -->
        <div v-for="i in firstDayOffset" :key="'empty-' + i"></div>

        <!-- Dates -->
        <div v-for="date in dates" :key="date"
             class="p-4 border rounded-md"
             :class="{
               'bg-blue-300 text-white font-bold': isToday(date),
               'bg-gray-200': isScheduled(date)
             }">
          <div>{{ date }}</div>
        </div>
      </div>
    </div>

    <!-- Today's Schedule Section (Right) -->
    <div class="w-full md:w-1/3 p-4 border rounded-lg shadow-lg bg-white">
      <h3 class="text-lg font-bold mb-2">📌 Schedule for Today: November {{ today }}</h3>

      <div v-if="todaySchedules.length > 0">
        <ul>
          <li v-for="cls in todaySchedules" :key="cls.id" class="border-b py-2">
            <p><strong>Teacher:</strong> {{ cls.teacher }}</p>
            <p><strong>Grade:</strong> {{ cls.grade }}</p>
            <p><strong>Section:</strong> {{ cls.section }}</p>
            <p><strong>Subject:</strong> {{ cls.subject }}</p>
            <p><strong>Time:</strong> {{ cls.time }}</p>
          </li>
        </ul>
      </div>
      <p v-else class="text-gray-500">No classes scheduled today.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      today: new Date().getDate(), // Get today's date
      firstDayOffset: new Date(2025, 10, 1).getDay(), // Get first day of November 2025
      dates: Array.from({ length: 30 }, (_, i) => i + 1), // Dates 1 to 30
      schedules: this.generateDailySchedules() // Generate a new schedule every day
    };
  },
  computed: {
    todaySchedules() {
      return this.schedules.filter(cls => cls.date === this.today);
    }
  },
  methods: {
    isScheduled(date) {
      return this.schedules.some(cls => cls.date === date);
    },
    isToday(date) {
      return date === this.today;
    },
    generateDailySchedules() {
      const teacher = "Mike Madulara"; // Fixed teacher name
      const subjects = ["Math", "English", "Science", "History", "PE", "Computer"];
      const grades = ["4", "5", "6"];
      const sections = ["A", "B", "C", "D"];
      const timeSlots = ["8:00 AM - 9:30 AM", "10:00 AM - 11:30 AM", "1:00 PM - 2:30 PM", "3:00 PM - 4:30 PM"];

      let schedules = [];

      for (let day = 1; day <= 30; day++) {
        let dailyClasses = Math.floor(Math.random() * 4) + 2; // Random 2 to 5 classes per day

        for (let i = 0; i < dailyClasses; i++) {
          const subject = subjects[Math.floor(Math.random() * subjects.length)];
          const grade = grades[Math.floor(Math.random() * grades.length)];
          const section = sections[Math.floor(Math.random() * sections.length)];
          const time = timeSlots[Math.floor(Math.random() * timeSlots.length)];

          schedules.push({ id: `${day}-${i}`, teacher, grade, section, subject, date: day, time });
        }
      }

      return schedules;
    }
  }
};
</script>

<style scoped>
/* Additional Styling */
</style>
