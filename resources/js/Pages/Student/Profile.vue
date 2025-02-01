<template>
  <div class="flex flex-col items-center min-h-screen bg-gradient-to-br from-blue-100 to-indigo-200 p-6">

    <!-- Profile Card -->
    <div class="bg-white p-6 rounded-2xl shadow-xl w-96 text-center transform hover:scale-105 transition duration-300">

      <!-- Profile Picture -->
      <div class="relative w-24 h-24 mx-auto">
        <img :src="profilePic" alt="Profile" class="w-24 h-24 rounded-full border-4 border-blue-400 shadow-md">
        <label for="upload" class="absolute bottom-0 right-0 bg-blue-500 text-white p-1 rounded-full cursor-pointer shadow-md">
          📷
        </label>
        <input id="upload" type="file" class="hidden" @change="uploadImage">
      </div>

      <!-- Student Info Form -->
      <div class="mt-4 space-y-3">
        <div>
          <label class="font-bold text-lg text-blue-600">👤 Name</label>
          <input v-model="student.name" type="text" class="w-full mt-1 p-2 border-2 border-blue-300 rounded-lg text-center text-lg">
        </div>
        <div>
          <label class="font-bold text-lg text-green-600">🎂 Age</label>
          <input v-model="student.age" type="number" class="w-full mt-1 p-2 border-2 border-green-300 rounded-lg text-center text-lg">
        </div>
        <div>
          <label class="font-bold text-lg text-purple-600">🏫 Grade</label>
          <select v-model="student.grade" class="w-full mt-1 p-2 border-2 border-purple-300 rounded-lg text-center text-lg">
            <option>Grade 1</option>
            <option>Grade 2</option>
            <option>Grade 3</option>
            <option>Grade 4</option>
            <option>Grade 5</option>
            <option>Grade 6</option>
          </select>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex justify-center gap-4 mt-6">
        <button @click="saveProfile" class="bg-green-500 text-white px-6 py-2 rounded-full shadow-lg hover:bg-green-600 transition duration-300">💾 Save</button>
        <button @click="resetProfile" class="bg-red-500 text-white px-6 py-2 rounded-full shadow-lg hover:bg-red-600 transition duration-300">❌ Cancel</button>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      profilePic: "https://via.placeholder.com/100", // Default avatar
      student: {
        name: "Erica Jane",
        age: 10,
        grade: "Grade 4"
      }
    };
  },
  methods: {
    saveProfile() {
      alert("Profile saved! 🎉");
    },
    resetProfile() {
      this.student = { name: "Erica Jane", age: 10, grade: "Grade 4" };
      alert("Changes canceled! 🔄");
    },
    uploadImage(event) {
      const file = event.target.files[0];
      if (file) {
        this.profilePic = URL.createObjectURL(file);
      }
    }
  }
};
</script>
