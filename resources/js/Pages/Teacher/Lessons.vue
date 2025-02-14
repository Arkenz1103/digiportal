<template>
  <div class="flex items-start justify-center min-h-screen bg-gray-100 p-10">
    <div class="flex w-full max-w-5xl gap-16">
      <!-- Upload Box (Left) -->
      <div class="w-1/2 bg-white shadow-lg rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">Upload Lesson Plan</h2>

        <div
          class="border-2 border-dashed border-gray-400 rounded-lg p-6 text-center cursor-pointer hover:border-blue-500"
          @dragover.prevent
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
        >
          <input type="file" ref="fileInput" multiple @change="handleFileUpload" accept=".pdf, .doc, .docx" hidden />
          <p class="text-gray-500">Drag & drop files here or <span class="text-blue-500 underline">browse</span></p>
          <p class="text-sm text-gray-400">Only PDF or DOCX files</p>
        </div>

        <button
          @click="uploadFiles"
          :disabled="selectedFiles.length === 0 || uploading"
          class="w-full mt-4 bg-blue-500 text-white px-4 py-3 rounded-lg shadow-md transition-all hover:bg-blue-600 disabled:bg-gray-400"
        >
          {{ uploading ? "Uploading..." : "Upload Lesson Plans" }}
        </button>
      </div>

      <!-- Uploaded Files List (Right) -->
      <div class="w-1/2 bg-white shadow-lg rounded-lg p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-3">Uploaded Files</h3>
        <div v-if="uploadedFiles.length > 0" class="space-y-3">
          <div v-for="(file, index) in uploadedFiles" :key="index" class="flex justify-between items-center p-3 bg-gray-50 rounded-lg border">
            <p class="text-gray-700 truncate w-40">{{ file.name }}</p>
            <div class="flex space-x-3">
              <a :href="file.url" target="_blank" class="text-blue-500 text-sm">View</a>
              <button @click="removeFile(index)" class="text-red-500 text-sm">Delete</button>
            </div>
          </div>
        </div>
        <p v-else class="text-gray-500 text-sm">No files uploaded yet.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  setup() {
    const selectedFiles = ref([]);
    const uploadedFiles = ref([]);
    const fileInput = ref(null);
    const uploading = ref(false);

    const handleFileUpload = (event) => {
      selectedFiles.value = [...event.target.files];
    };

    const handleDrop = (event) => {
      selectedFiles.value = [...event.dataTransfer.files];
    };

    const triggerFileInput = () => {
      fileInput.value.click();
    };

    const uploadFiles = () => {
      if (selectedFiles.value.length === 0) return;
      uploading.value = true;
      setTimeout(() => {
        uploadedFiles.value = [...uploadedFiles.value, ...selectedFiles.value.map(file => ({ name: file.name, url: "#" }))];
        selectedFiles.value = [];
        uploading.value = false;
      }, 1000);
    };

    const removeFile = (index) => {
      uploadedFiles.value.splice(index, 1);
    };

    return { selectedFiles, uploadedFiles, handleFileUpload, uploadFiles, handleDrop, triggerFileInput, removeFile, fileInput, uploading };
  },
};
</script>
