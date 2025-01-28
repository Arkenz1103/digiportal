<template>
    <div class="p-6">
      <div class="mb-6">
        <!-- Header -->
        <h1 class="text-2xl font-semibold mb-4">
          <Link :href="route('teacher.class')" class="text-gray-600 hover:text-gray-800">My Class</Link>
          <span class="text-gray-400"> / {{ className }}</span>
        </h1>

        <!-- Class Header -->
        <div class="bg-blue-100 p-6 rounded-lg mb-6">
          <h2 class="text-4xl text-gray-600 mb-2">{{ className }}</h2>
          <p class="text-gray-600">Grade 1 - A</p>
          <p class="text-gray-600">MW(7:00am-8:00am)</p>
        </div>

        <!-- Navigation Tabs -->
        <div class="border-b border-gray-200">
          <nav class="flex space-x-8">
            <button
              v-for="tab in tabs"
              :key="tab"
              @click="currentTab = tab"
              :class="[
                'py-4 px-1 border-b-2 font-medium text-sm',
                currentTab === tab
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab }}
            </button>
          </nav>
        </div>

        <!-- Tab Content -->
        <div class="mt-6">
          <!-- Overview Tab -->
          <div v-if="currentTab === 'Overview'" class="space-y-6">
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

          <!-- Classwork Tab -->
          <div v-if="currentTab === 'Classwork'" class="space-y-4">
            <div class="bg-white p-4 rounded-lg shadow">
              <h3 class="font-semibold mb-2">Upcoming Assignments</h3>
              <!-- Add classwork content here -->
            </div>
          </div>

          <!-- Students Tab -->
          <div v-if="currentTab === 'Students'" class="space-y-4">
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

          <!-- Grades Tab -->
          <div v-if="currentTab === 'Grades'" class="space-y-4">
            <div class="bg-white p-4 rounded-lg shadow">
              <h3 class="font-semibold mb-2">Student Grades</h3>
              <!-- Add grades content here -->
            </div>
          </div>

          <!-- Lesson Plan Tab -->
          <div v-if="currentTab === 'Lesson Plan'" class="space-y-4">
            <div class="bg-white p-4 rounded-lg shadow">
              <h3 class="font-semibold mb-2">Lesson Plan</h3>
              <!-- Add lesson plan content here -->
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import { Link } from '@inertiajs/vue3';

const props = defineProps({
  className: {
    type: String,
    required: true
  }
});

const tabs = ['Overview', 'Classwork', 'Students', 'Grades', 'Lesson Plan'];
const currentTab = ref('Overview');

// Sample data - replace with actual data from your backend
const posts = [
  {
    author: 'Teacher Name',
    date: 'Sep 22',
    content: 'Welcome to our class! I\'m excited to start this learning journey with you.'
  }
];

const students = [
  { name: 'Mike Madulara' },
  { name: 'Geomariz Jayson' },
  { name: 'Erica Jane Nunez' }
];
</script>

<style scoped>
/* Optional: Add any additional styling here */
</style>