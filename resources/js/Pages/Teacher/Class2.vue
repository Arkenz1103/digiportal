<template>
  <div class="flex justify-between items-start p-6">
    <!-- Classroom Management Title (Left) -->
    <div class="bg-white rounded-lg shadow px-6 py-4">
      <h2 class="text-xl font-bold">Classroom Management</h2>
    </div>

    <!-- Create Class Button (Right, But Lower) -->
    <div class="bg-white rounded-lg shadow px-6 py-4 mt-12">
      <button
        @click="showModal = true"
        class="bg-blue-500 text-white px-4 py-2 rounded">
        Create Class
      </button>
    </div>
  </div>

  <!-- Modal -->
  <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-96">
      <h2 class="text-lg font-bold mb-4">Create a New Class</h2>
      <form @submit.prevent="saveClass">
        <!-- Grade Selection (Starts Empty) -->
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

        <!-- Subject Field (Only Shows for Grade 4 to 6) -->
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
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const showModal = ref(false);
    const grade = ref('');
    const section = ref('');
    const subject = ref('');

    const saveClass = () => {
      console.log("Class Created:", {
        grade: grade.value,
        section: section.value,
        subject: grade.value >= 4 ? subject.value : "N/A"
      });
      alert("Class Created Successfully! (Check console)");
      showModal.value = false;
    };

    return { showModal, grade, section, subject, saveClass };
  }
};
</script>
