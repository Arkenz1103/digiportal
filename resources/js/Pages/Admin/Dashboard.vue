<template>
    <div class="p-6 bg-gray-100 min-h-screen">
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-800">Welcome back, {{ user?.name }}!!</h1>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
        <!-- Lesson Plan Card -->
        <div class="bg-blue-100 rounded-lg p-6 shadow-sm h-40">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-xl font-semibold text-gray-800">Lesson Plan</h3>
              <p class="text-3xl font-bold text-blue-600">30</p>
            </div>
            <div class="bg-blue-200 p-3 rounded-full">
              <i class="pi pi-file text-blue-600 text-3xl"></i>
            </div>
          </div>
        </div>

        <!-- Class Card -->
        <div class="bg-purple-100 rounded-lg p-6 shadow-sm h-40">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-xl font-semibold text-gray-800">Class</h3>
              <p class="text-3xl font-bold text-purple-600">10</p>
            </div>
            <div class="bg-purple-200 p-3 rounded-full">
              <i class="pi pi-book text-purple-600 text-3xl"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

  <script setup>
  defineProps({
    user: {
      type: Object,
      required: true
    }
  });
  </script>
