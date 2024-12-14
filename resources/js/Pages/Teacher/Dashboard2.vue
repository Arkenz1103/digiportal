<template>
  <div class="p-6 bg-gray-50 min-h-screen font-sans">
  <!-- Container for Welcome Section and Calendar -->
  <div class="flex flex-col md:flex-row gap-x-60">
    <!-- Welcome Section -->
    <div class="flex-1 bg-blue-100 rounded-lg p-4">
      <h2 class="text-lg font-bold">
        Welcome Back, <span class="text-green-600">Mike!</span>
      </h2>
      <p class="text-gray-700">
        Your Students completed
        <span class="font-bold">100%</span> of the task.
        Progress is <span class="text-green-600">Excellent!</span>
      </p>
    </div>

    <!-- Calendar -->
    <div class="w-full md:w-1/4 bg-blue-300 rounded-lg flex items-center justify-center h-23">
      <div class="text-center">
        <h3 class="font-bold text-gray-700">CALENDAR</h3>
        <p class="text-lg font-bold text-black">2024</p>
      </div>
    </div>
  </div>

    <!-- Progress Section -->
    <div class="grid grid-cols-2 gap-6 mt-6">
      <!-- Working Hours -->
      <div class="bg-white rounded-lg shadow p-4">
        <h3 class="font-semibold mb-2 text-gray-700">Working Hours</h3>
        <div class="flex justify-between items-center mb-2">
          <p class="text-gray-600">Today</p>
          <Dropdown
            v-model="selectedOption"
            :options="['Today']"
            class="p-dropdown-sm"
          />
        </div>
        <div class="flex items-center justify-center">
          <CircleProgress :percentage="100" />
        </div>
      </div>



  <!-- Parent Container with justify-end -->
  <div class="flex justify-end">
    <!-- My Students Box -->
    <div class="bg-blue-100 w-3/4 md:w-3/5 rounded-lg shadow p-4">
      <!-- Header -->
      <div class="flex justify-between mb-2">
        <h3 class="font-semibold text-gray-700">My Students</h3>
        <a href="#" class="text-indigo-500 text-sm hover:bg-indigo-300 cursor-pointer">View all</a>
      </div>

      <!-- Content -->
      <div class="flex justify-between items-center">
        <div class="flex items-center space-x-3">
          <!-- User Icon -->
          <div class="bg-gray-300 rounded-full w-10 h-10 flex items-center justify-center">
            <i class="pi pi-user text-xl"></i>
          </div>
          <!-- Student Name -->
          <div>
            <p class="font-semibold text-gray-700">Milo</p>
          </div>
        </div>
        <!-- Percentage aligned to the right -->
        <div class="text-right">
          <p class="text-green-600 font-bold">100%</p>
        </div>
      </div>
    </div>
  </div>
</div>



    <!-- Uploads Section -->
    <div class="mt-6">
      <h3 class="font-semibold text-gray-700 mb-2">Uploads</h3>
      <div class="space-y-2">
        <div class="bg-indigo-300 h-10 rounded-lg"></div>
        <div class="bg-indigo-300 h-10 rounded-lg"></div>
        <div class="bg-indigo-300 h-10 rounded-lg"></div>
      </div>
    </div>
  </div>
</template>

<script>
import Dropdown from "primevue/dropdown";
import CircleProgress from "../Components/CircleProgress.vue"; // Custom Circle Progress Component

export default {
  name: "Dashboard",
  components: {
    Dropdown,
    CircleProgress,
  },
  data() {
    return {
      selectedOption: "Today",
    };
  },
};
</script>

<style>
.p-dropdown-sm {
  width: 100px;
  font-size: 0.9rem;
}
</style>
