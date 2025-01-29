<template>
  <div class="space-y-6">
    <div v-for="(post, index) in posts" :key="index" class="bg-white p-4 rounded-lg shadow">
      <div class="flex items-center mb-4">
        <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white font-bold">
          {{ post.author[0] }}
        </div>
        <div class="ml-4">
          <p class="font-semibold">{{ post.author }}</p>
          <p class="text-sm text-gray-500">Posted on {{ post.date }}</p>
        </div>
      </div>
      <p class="text-gray-700">{{ post.content }}</p>

      <!-- Comment input -->
      <div class="mt-4 flex">
        <input
          type="text"
          placeholder="Post an announcement..."
          class="flex-1 border rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button class="bg-blue-500 text-white px-4 rounded-r-lg hover:bg-blue-600">
          <i class="fas fa-paper-plane"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  posts: {
    type: Array,
    default: () => []
  }
});
</script>