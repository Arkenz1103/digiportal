<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-gray-800">Welcome back, {{ user?.name }}!!</h1>
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
