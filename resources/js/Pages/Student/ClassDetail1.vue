<template>
  <div class="p-6">
    <div class="mb-6">
      <!-- Header -->
      <h1 class="text-2xl font-semibold mb-4">
        <Link :href="route('student.class')" class="text-gray-600 hover:text-gray-800">My Class</Link>
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
          </div>
        </div>

        <!-- Classwork Tab -->
        <div v-if="currentTab === 'Classwork'" class="space-y-4">
          <div class="bg-white p-4 rounded-lg shadow">
            <h3 class="font-semibold mb-2">Upcoming Work</h3>

            <!-- Display Activities -->
            <div v-for="activity in activities" :key="activity.id" class="border p-3 rounded-lg mb-2">
              <h4 class="font-semibold">{{ activity.title }}</h4>
              <p class="text-sm text-gray-600">{{ activity.description }}</p>

              <!-- Student Answer Input -->
              <div class="mt-2">
                <textarea v-model="activity.answer" placeholder="Write your answer here..." class="w-full p-2 border rounded"></textarea>
              </div>

              <!-- File Upload -->
              <div class="mt-2">
                <input type="file" @change="handleFileUpload($event, activity.id)" />
              </div>

              <!-- Submit Button -->
              <button @click="submitAnswer(activity.id)" class="mt-2 bg-blue-500 text-white px-4 py-2 rounded">Submit</button>
            </div>
          </div>
        </div>

        <!-- Classmates Tab -->
        <div v-if="currentTab === 'Classmates'" class="space-y-4">
          <div class="bg-white p-4 rounded-lg shadow">
            <h3 class="font-semibold mb-2">Teacher</h3>
            <p class="text-gray-700">{{ teacher.name }}</p>
          </div>
          <div class="bg-white p-4 rounded-lg shadow">
            <h3 class="font-semibold mb-2">Classmates ({{ uniqueClassmates.length }} Students)</h3>
            <ul class="space-y-2">
              <li v-for="(student, index) in uniqueClassmates" :key="index" class="text-gray-700">{{ student.name }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { Link } from "@inertiajs/vue3";

const props = defineProps({
  className: {
    type: String,
    required: true,
  },
});

const tabs = ["Overview", "Classwork", "Classmates"];
const currentTab = ref("Overview");
const teacher = { name: "Erica Jane Bucol" };
const classmates = [
  { name: "Mike Madulara" },
  { name: "Geomariz Jayson" },
  { name: "Erica Jane Nunez" },
];
const uniqueClassmates = classmates.filter((student, index, self) =>
  index === self.findIndex((s) => s.name === student.name)
);
const posts = [
  { author: "Erica Jane Bucol", date: "Sep 22", content: "Welcome to our class!" },
];
const activities = ref([
  { id: 1, title: "Math Assignment", description: "Solve the given equations.", answer: "", file: null },
  { id: 2, title: "History Essay", description: "Write a 500-word essay on WWII.", answer: "", file: null },
]);

const handleFileUpload = (event, activityId) => {
  const file = event.target.files[0];
  const activity = activities.value.find(a => a.id === activityId);
  if (activity) {
    activity.file = file;
  }
};

const submitAnswer = (activityId) => {
  const activity = activities.value.find(a => a.id === activityId);
  if (activity) {
    console.log("Submitting Answer:", activity);
    alert("Your answer has been submitted!");
  }
};
</script>
