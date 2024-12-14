<template>
  <div class="p-6 bg-gray-50 min-h-screen font-sans">
    <!-- Lesson Plan Header -->
    <div class="flex justify-between items-center">
      <!-- Left Section: Title -->
      <div>
        <h1 class="text-lg font-bold text-black">
          My Lesson Plan
          <span class="font-normal text-gray-600">/ Grade-1 / Mathematics</span>
        </h1>
      </div>

      <!-- Right Section: Button -->
      <Button
        label="Create Lesson Plan"
        icon="pi pi-plus"
        class="bg-white text-blue-500 border border-blue-500 rounded-md px-4 py-2 hover:bg-blue-500 hover:text-white transition duration-300"
        @click="handleCreateLessonPlan"
      />
    </div>
  </div>
</template>

<script>
</script>

