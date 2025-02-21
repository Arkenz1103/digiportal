<template>
  <div class="p-6 bg-white rounded-lg shadow-md">
    <h2 class="text-3xl font-bold mb-6 text-gray-800">Quizzes</h2>

    <div v-if="!creatingQuiz">
      <!-- Search and Filter Controls -->
      <div class="flex flex-wrap gap-4 mb-6 items-center">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search for a quiz"
          class="border rounded-lg px-4 py-2 w-full md:w-1/3 focus:ring-2 focus:ring-blue-500"
        />
        <select v-model="selectedStudent" class="border rounded-lg px-4 py-2 w-full md:w-1/4 focus:ring-2 focus:ring-blue-500">
          <option value="">Filter by Student</option>
          <option v-for="student in studentNames" :key="student" :value="student">
            {{ student }}
          </option>
        </select>
        <select v-model="sortBy" class="border rounded-lg px-4 py-2 w-full md:w-1/4 focus:ring-2 focus:ring-blue-500">
          <option value="">Sort by</option>
          <option value="points">Points</option>
          <option value="questions">Number of Questions</option>
        </select>

        <!-- Add Quiz Button -->
        <button
          @click="creatingQuiz = true"
          class="bg-[#0076A8] text-white px-4 py-2 rounded-md font-semibold shadow-md hover:bg-[#005F87] transition duration-200 flex items-center gap-2"
        >
          <span class="text-white">+</span> Add Quiz
        </button>
      </div>

      <!-- Quiz Table -->
      <div class="overflow-x-auto rounded-lg border">
        <table class="w-full border-collapse">
          <thead>
            <tr class="bg-gray-200 text-gray-700 uppercase text-sm tracking-wider">
              <th class="text-left px-6 py-3">Quiz Title</th>
              <th class="text-left px-6 py-3">Student Name</th>
              <th class="text-left px-6 py-3">Points</th>
              <th class="text-left px-6 py-3">Questions</th>
              <th class="text-left px-6 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in filteredQuizzes" :key="quiz.id" class="border-b last:border-none">
              <td class="px-6 py-4 text-gray-900 font-medium">{{ quiz.title }}</td>
              <td class="px-6 py-4 text-gray-700">{{ quiz.student }}</td>
              <td class="px-6 py-4 text-gray-700">{{ quiz.points }}</td>
              <td class="px-6 py-4 text-gray-700">{{ quiz.questions.length }}</td>
              <td class="px-6 py-4">
                <button
                  @click="confirmDelete(quiz.id)"
                  class="bg-red-500 text-white px-3 py-1 rounded-md hover:bg-red-700 transition"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Quiz Creation Form -->
    <div v-else>
      <div class="p-6 bg-white border rounded-lg shadow-md">
        <h3 class="text-xl font-semibold mb-4">Create Quiz</h3>

        <label class="block text-gray-700 font-semibold mb-2">Quiz Name</label>
        <input v-model="quizForm.name" type="text" class="border rounded-lg px-4 py-2 w-full" placeholder="Enter quiz name" />

        <label class="block text-gray-700 font-semibold mt-4 mb-2">Quiz Instructions</label>
        <textarea v-model="quizForm.instructions" class="border rounded-lg px-4 py-2 w-full" placeholder="Enter instructions"></textarea>

        <!-- Question Form -->
        <div class="mt-6 p-4 border rounded-lg">
          <div class="flex gap-2 mb-2">
            <button class="border rounded-lg px-4 py-2">Question</button>
            <select class="border rounded-lg px-4 py-2">
              <option>Multiple Choice</option>
            </select>
          </div>

          <p class="text-gray-600 text-sm">Enter your question and multiple answers, then select the correct one.</p>
          <label class="block text-gray-700 font-semibold mt-4">Question:</label>
          <textarea v-model="quizForm.question" class="border rounded-lg px-4 py-2 w-full"></textarea>

          <div class="mt-4">
            <label class="block text-green-600 font-semibold flex items-center">
              <span class="text-lg">➡</span> Correct Answer
            </label>
            <input v-model="quizForm.correctAnswer" type="text" class="border rounded-lg px-4 py-2 w-full mt-2" />
          </div>

          <div v-for="(answer, index) in quizForm.possibleAnswers" :key="index" class="mt-2 flex items-center gap-2">
            <input v-model="quizForm.possibleAnswers[index]" type="text" class="border rounded-lg px-4 py-2 w-full" />
            <button @click="removeAnswer(index)" class="text-red-600">🗑</button>
          </div>

          <button @click="addAnswer" class="text-blue-600 mt-2 flex items-center">
            + Add Another Answer
          </button>

          <div class="flex justify-between mt-6">
            <button @click="creatingQuiz = false" class="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-700">Cancel</button>
            <button @click="submitQuiz" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-700">Update Question</button>
          </div>
        </div>

        <button class="mt-6 w-full bg-gray-200 text-gray-700 px-4 py-2 rounded-lg">+ New Question</button>
        <button @click="submitQuiz" class="mt-4 w-full bg-blue-500 text-white px-4 py-2 rounded-lg">Save</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      creatingQuiz: false,
      searchQuery: "",
      selectedStudent: "",
      sortBy: "",
      quizzes: JSON.parse(localStorage.getItem("quizzes")) || [],
      quizForm: {
        name: "",
        instructions: "",
        question: "",
        correctAnswer: "",
        possibleAnswers: ["", ""],
      },
    };
  },
  computed: {
    studentNames() {
      return [...new Set(this.quizzes.map((q) => q.student))];
    },
    filteredQuizzes() {
      return this.quizzes.filter((quiz) =>
        quiz.title.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    addAnswer() {
      this.quizForm.possibleAnswers.push("");
    },
    removeAnswer(index) {
      this.quizForm.possibleAnswers.splice(index, 1);
    },
    submitQuiz() {
      this.quizzes.push({
        id: this.quizzes.length + 1,
        title: this.quizForm.name,
        student: "Unassigned",
        points: 0,
        questions: [{ text: this.quizForm.question, answers: [this.quizForm.correctAnswer, ...this.quizForm.possibleAnswers] }],
      });

      localStorage.setItem("quizzes", JSON.stringify(this.quizzes));
      this.creatingQuiz = false;
      this.quizForm = { name: "", instructions: "", question: "", correctAnswer: "", possibleAnswers: ["", ""] };
    },
  },
};
</script>
