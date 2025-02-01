<template>
  <div class="flex min-h-screen bg-gradient-to-br from-blue-100 to-indigo-200 p-6">
    <div class="flex-1 p-10">
      <div class="grid grid-cols-2 gap-6">

        <!-- Welcome Card (Top Left) -->
        <div class="bg-blue-500 text-white p-6 rounded-2xl shadow-lg text-center transform hover:scale-105 transition duration-300">
          <p class="font-bold text-lg">👋 Welcome Back, Erica!</p>
          <p class="text-md mt-2">How Are You Today? 😊</p>
        </div>

        <!-- Calendar (Top Right) -->
        <div class="bg-white border-2 border-blue-400 p-6 rounded-2xl shadow-lg text-center transform hover:scale-105 transition duration-300">
          <h2 class="font-bold text-xl text-blue-600">📅 Calendar</h2>
          <p class="text-gray-600 text-lg">2024</p>
        </div>

        <!-- To-Do List (Bottom Left) -->
        <div class="bg-white border-2 border-green-400 p-6 rounded-2xl shadow-lg text-center transform hover:scale-105 transition duration-300">
          <h2 class="font-bold text-xl text-green-600">✅ To Do</h2>
          <div class="mt-4 space-y-3">
            <div class="bg-green-300 h-8 rounded-lg flex items-center justify-center font-semibold">Math Homework</div>
            <div class="bg-green-300 h-8 rounded-lg flex items-center justify-center font-semibold">Reading Assignment</div>
          </div>
        </div>

        <!-- My Schedule (Bottom Right) -->
        <div class="bg-white border-2 border-purple-400 p-6 rounded-2xl shadow-lg text-center transform hover:scale-105 transition duration-300">
          <h2 class="font-bold text-xl text-purple-600">🕒 My Schedule</h2>
        </div>

      </div>
    </div>
  </div>
</template>





<script setup>
</script>
