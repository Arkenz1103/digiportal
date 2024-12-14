<template>
  <div class="p-4 w-full max-w-4xl mx-auto">
    <!-- Calendar Header -->
    <h2 class="text-2xl font-bold mb-4">NOVEMBER 2024</h2>

    <!-- Days of the Week -->
    <div class="grid grid-cols-7 text-center font-semibold text-gray-600 mb-2">
      <div>Monday</div>
      <div>Tuesday</div>
      <div>Wednesday</div>
      <div>Thursday</div>
      <div>Friday</div>
      <div>Saturday</div>
      <div>Sunday</div>
    </div>

    <!-- Calendar Grid -->
    <div class="grid grid-cols-7 gap-1 text-center">
      <!-- Empty Spaces for the Start of the Month -->
      <div v-for="i in 3" :key="'empty-' + i"></div>

      <!-- Dates -->
      <div v-for="date in dates" :key="date"
           class="p-4 border rounded-md hover:bg-gray-200 cursor-pointer"
           :class="{'bg-red-200': date === 15}"
           @click="handleClick(date)">
        {{ date }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dates: Array.from({ length: 30 }, (_, i) => i + 1), // Generate dates 1 to 30
    };
  },
};
</script>
