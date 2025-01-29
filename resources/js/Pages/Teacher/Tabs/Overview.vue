<template>
  <div class="container mx-auto px-4 py-2">
    <!-- Post Input Box -->
    <div class="bg-white border border-gray-300 rounded-lg p-4 shadow-sm hover:shadow-md transition duration-200">
      <div class="flex items-center space-x-2">
        <!-- Profile Icon -->
        <div class="w-8 h-8 bg-green-600 text-white font-bold flex items-center justify-center rounded-full text-sm">
          {{ $page.props.auth.user.name[0].toUpperCase() }}
        </div>
        <!-- Input Field -->
        <div class="flex-1">
          <textarea
            v-model="announcementContent"
            placeholder="Post something on the class..."
            :rows="isExpanded ? 3 : 1"
            class="w-full bg-transparent border-none focus:outline-none text-gray-600 placeholder-gray-500 resize-none overflow-hidden"
            @focus="isExpanded = true"
          ></textarea>
        </div>
      </div>

      <!-- Expanded Post Box -->
      <div v-if="isExpanded" class="mt-2 border-t pt-2">
        <div class="flex justify-between items-center mt-2">
          <div class="flex space-x-2">
            <!-- Upload Button -->
            <button 
              class="p-2 rounded-full hover:bg-blue-50 transition-all duration-300 group relative"
              title="Upload File"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke-width="1.5" 
                stroke="currentColor" 
                class="w-5 h-5 text-blue-500 group-hover:text-blue-600 transition-colors duration-300"
              >
                <path 
                  stroke-linecap="round" 
                  stroke-linejoin="round" 
                  d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" 
                />
              </svg>
              <span class="absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                Upload
              </span>
            </button>
            <!-- Create Quiz Button -->
            <button 
              class="p-2 rounded-full hover:bg-green-50 transition-all duration-300 group relative"
              title="Create Quiz"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke-width="1.5" 
                stroke="currentColor" 
                class="w-5 h-5 text-green-500 group-hover:text-green-600 transition-colors duration-300"
              >
                <path 
                  stroke-linecap="round" 
                  stroke-linejoin="round" 
                  d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" 
                />
              </svg>
              <span class="absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                Create Quiz
              </span>
            </button>
          </div>
          <div>
            <button @click="cancelPost" class="bg-gray-300 text-gray-700 px-4 py-1 rounded-lg mr-2">Cancel</button>
            <button @click="postAnnouncement" class="bg-blue-500 text-white px-4 py-1 rounded-lg">Post</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Announcements Section -->
    <div class="mt-4 space-y-4">
      <div v-for="announcement in announcements" :key="announcement.id" class="bg-white border border-gray-300 rounded-lg p-4 shadow-sm">
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 bg-green-600 text-white font-bold flex items-center justify-center rounded-full text-sm">
            {{ announcement.author[0].toUpperCase() }}
          </div>
          <div>
            <p class="text-gray-700 font-semibold">{{ announcement.author }} posted a new announcement</p>
            <p class="text-gray-500 text-sm">{{ formatDate(announcement.date) }}</p>
          </div>
        </div>
        <p class="mt-2 text-gray-700">{{ announcement.content }}</p>
        <div class="mt-2 border-t pt-2">
          <input
            type="text"
            v-model="announcement.comment"
            placeholder="Comment on the announcement..."
            class="w-full bg-gray-100 border border-gray-300 rounded-full px-3 py-1 focus:outline-none text-gray-600"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { router } from '@inertiajs/vue3';

const announcementContent = ref('');
const isExpanded = ref(false);
const announcements = ref([
  {
    id: 1,
    author: 'Erica Jane Bucol',
    date: new Date('2023-09-22'),
    content: "I'm thrilled to have each and every one of you here as we embark on this exciting learning journey together...",
    comment: ''
  },
  {
    id: 2,
    author: 'Erica Jane Bucol',
    date: new Date('2023-09-22'),
    content: 'Posted a new material: Fraction Modules',
    comment: ''
  },
  {
    id: 3,
    author: 'Erica Jane Bucol',
    date: new Date('2023-09-22'),
    content: 'Posted a new assignment: Addition Activity',
    comment: ''
  }
]);

const cancelPost = () => {
  announcementContent.value = '';
  isExpanded.value = false;
};

const postAnnouncement = () => {
  const content = announcementContent.value.trim();
  
  if (content === '') return;

  // Create a new announcement
  const newAnnouncement = {
    id: Date.now(),
    author: $page.props.auth.user.name,
    date: new Date(),
    content: content,
    comment: ''
  };

  // Add to the top of announcements
  announcements.value.unshift(newAnnouncement);

  // Send to backend
  router.post(route('teacher.post_announcement'), {
    content: content
  }, {
    onSuccess: () => {
      // Reset input
      announcementContent.value = '';
      isExpanded.value = false;
    }
  });
};

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};
</script>

<style scoped>
textarea {
  min-height: 1.5rem;
  max-height: 10rem;
}
</style>
