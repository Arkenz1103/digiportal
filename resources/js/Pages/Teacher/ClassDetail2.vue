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
          <Overview v-if="currentTab === 'Overview'" :posts="posts" />
          <Classwork v-if="currentTab === 'Classwork'" />
          <Students v-if="currentTab === 'Students'" :students="students" />
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import { Link } from '@inertiajs/vue3';
import Overview from './Tabs/Overview.vue';
import Classwork from './Tabs/Classwork.vue';
import Students from './Tabs/Students.vue';

const props = defineProps({
  className: {
    type: String,
    required: true
  }
});

const tabs = ['Overview', 'Classwork', 'Students'];
const currentTab = ref('Overview');


const students = [
  { name: 'Mike Madulara' },
  { name: 'Geomariz Jayson' },
  { name: 'Erica Jane Nunez' }
];
</script>

<style scoped>
/* Optional: Add any additional styling here */
</style>
