<template>
  <div class="p-6">
    <!-- Header Section: Classroom Management + Create Class Button -->
    <div class="flex justify-between items-center bg-white rounded-lg shadow px-6 py-4 mb-6">
      <h2 class="text-xl font-bold">Classroom Management</h2>
      <button @click="showModal = true" class="bg-blue-500 text-white px-4 py-2 rounded">
        Create Class
      </button>
    </div>

    <!-- List of Created Classes -->
    <div v-if="createdClasses.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      <div v-for="(cls, index) in createdClasses" :key="index" class="bg-white rounded-lg shadow-lg overflow-hidden relative">
        <!-- Class Header -->
        <div class="bg-gradient-to-r from-blue-600 to-blue-400 text-white p-4 relative">
          <h3 class="text-lg font-bold">{{ cls.grade }} - {{ cls.section }}</h3>
          <p class="text-sm font-semibold">{{ cls.schedule }}</p>
          <p class="text-xs mt-1">{{ cls.subject !== 'N/A' ? cls.subject : 'General Education' }}</p>

          <!-- Profile Image -->
          <img
            class="absolute -bottom-6 right-4 w-12 h-12 rounded-full border-2 border-white"
            src="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png"
            alt="Teacher Profile"
          />
        </div>

        <!-- Class Details & Delete Button -->
        <div class="p-4 pt-6 flex justify-between items-center">
          <p class="text-gray-700 font-medium">Mike Madulara</p>
          <button @click="deleteClass(index)" class="text-red-500 text-sm font-semibold">Delete</button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 class="text-lg font-bold mb-4">Create a New Class</h2>
        <form @submit.prevent="saveClass">
          <!-- Grade Selection -->
          <div class="mb-4">
            <label class="block font-semibold">Grade</label>
            <select v-model="grade" class="w-full p-2 border rounded">
              <option value="" disabled selected hidden>Select Grade</option>
              <option value="1">Grade 1</option>
              <option value="2">Grade 2</option>
              <option value="3">Grade 3</option>
              <option value="4">Grade 4</option>
              <option value="5">Grade 5</option>
              <option value="6">Grade 6</option>
            </select>
          </div>

          <!-- Section Input -->
          <div class="mb-4">
            <label class="block font-semibold">Section</label>
            <input type="text" v-model="section" class="w-full p-2 border rounded" placeholder="Enter Section">
          </div>

          <!-- Subject Field (Only for Grade 4 to 6) -->
          <div class="mb-4" v-if="grade >= 4">
            <label class="block font-semibold">Subject</label>
            <input type="text" v-model="subject" class="w-full p-2 border rounded" placeholder="Enter Subject">
          </div>

          <div class="flex justify-end space-x-2">
            <button @click="showModal = false" type="button" class="px-4 py-2 border rounded">Cancel</button>
            <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const showModal = ref(false);
    const grade = ref('');
    const section = ref('');
    const subject = ref('');
    const createdClasses = ref([]); // Store created classes

    const saveClass = () => {
      if (!grade.value || !section.value) {
        alert("Please fill in all required fields!");
        return;
      }

      // Assign schedule based on grade level
      const schedule = grade.value <= 3 ? "MF 8:00 AM - 12:00 PM" : "MF 1:00 PM - 5:00 PM";

      // Add new class to list
      createdClasses.value.push({
        grade: grade.value,
        section: section.value,
        subject: grade.value >= 4 ? subject.value : "N/A",
        schedule: schedule
      });

      // Reset form fields
      grade.value = '';
      section.value = '';
      subject.value = '';

      showModal.value = false;
    };

    const deleteClass = (index) => {
      createdClasses.value.splice(index, 1);
    };

    return { showModal, grade, section, subject, createdClasses, saveClass, deleteClass };
  }
};
</script>

<style scoped>
/* Additional Styling (If needed) */
</style>
