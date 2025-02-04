<template>
  <div class="space-y-4">
    <div class="bg-white p-4 rounded-lg shadow">
      <h3 class="font-semibold mb-2">Students ({{ students.length }})</h3>
      <ul class="space-y-2">
        <li v-for="(student, index) in students" :key="index" class="flex items-center space-x-4">
          <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center text-gray-700 font-bold">
            {{ student.name[0] }}
          </div>
          <p class="text-gray-700">{{ student.name }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineProps({
  students: {
    type: Array,
    default: () => []
  }
});
</script>