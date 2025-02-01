<template>
  <div class="flex flex-col items-center min-h-screen bg-gradient-to-br from-blue-200 to-blue-400 p-6">

    <!-- Profile Card -->
    <div class="bg-white p-8 rounded-2xl shadow-xl w-96 text-center transform hover:scale-105 transition duration-300">

      <!-- Profile Picture -->
      <div class="relative w-24 h-24 mx-auto mb-6">
        <img :src="profilePic" alt="Profile" class="w-24 h-24 rounded-full border-4 border-blue-500 shadow-md">
        <label for="upload" class="absolute bottom-0 right-0 bg-blue-500 text-white p-1 rounded-full cursor-pointer shadow-md">
          📷
        </label>
        <input id="upload" type="file" class="hidden" @change="uploadImage">
      </div>

      <!-- Profile Info Form -->
      <div class="space-y-6">
        <!-- Full Name -->
        <div>
          <label class="font-bold text-lg text-blue-600">👤 Full Name</label>
          <input v-model="user.fullName" type="text" class="w-full mt-1 p-2 border-2 border-blue-400 rounded-lg text-center text-lg" placeholder="Enter full name">
        </div>

        <!-- Email -->
        <div>
          <label class="font-bold text-lg text-blue-600">📧 Email</label>
          <input v-model="user.email" type="email" class="w-full mt-1 p-2 border-2 border-blue-400 rounded-lg text-center text-lg" placeholder="Enter email">
        </div>

        <!-- Password -->
        <div>
          <label class="font-bold text-lg text-blue-600">🔒 Password</label>
          <input v-model="user.password" type="password" class="w-full mt-1 p-2 border-2 border-blue-400 rounded-lg text-center text-lg" placeholder="Enter password">
        </div>

        <!-- Role Selection (Teacher, Student, Admin) -->
        <div>
          <label class="font-bold text-lg text-blue-600">🎓 Role</label>
          <select v-model="user.role" class="w-full mt-1 p-2 border-2 border-blue-400 rounded-lg text-center text-lg">
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <!-- Additional Fields for Teachers and Admins -->
        <div v-if="user.role === 'teacher'">
          <div>
            <label class="font-bold text-lg text-blue-600">🏫 Subject</label>
            <input v-model="user.subject" type="text" class="w-full mt-1 p-2 border-2 border-blue-400 rounded-lg text-center text-lg" placeholder="Enter subject taught">
          </div>
        </div>

        <div v-if="user.role === 'admin'">
          <div>
            <label class="font-bold text-lg text-blue-600">🏢 Department</label>
            <input v-model="user.department" type="text" class="w-full mt-1 p-2 border-2 border-blue-400 rounded-lg text-center text-lg" placeholder="Enter department">
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex justify-center gap-4 mt-6">
        <button @click="saveProfile" class="bg-blue-500 text-white px-6 py-2 rounded-full shadow-lg hover:bg-blue-600 transition duration-300">💾 Save</button>
        <button @click="resetProfile" class="bg-blue-500 text-white px-6 py-2 rounded-full shadow-lg hover:bg-blue-600 transition duration-300">❌ Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      profilePic: "https://via.placeholder.com/100", // Default avatar
      user: {
        fullName: "Erica Jane",
        email: "erica@example.com",
        password: "",
        role: "student", // 'student', 'teacher', 'admin'
        subject: "", // Only for teachers
        department: "", // Only for admins
      }
    };
  },
  methods: {
    saveProfile() {
      alert("Profile saved! 🎉");
    },
    resetProfile() {
      this.user = {
        fullName: "Erica Jane",
        email: "erica@example.com",
        password: "",
        role: "student",
        subject: "",
        department: "",
      };
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

<style scoped>
/* Custom styles */
input, select {
  font-size: 1rem;
  padding: 12px;
  transition: border-color 0.3s ease;
}

input:focus, select:focus {
  border-color: #3b82f6; /* Blue focus */
  outline: none;
}

button:hover {
  transform: scale(1.05);
}
</style>
