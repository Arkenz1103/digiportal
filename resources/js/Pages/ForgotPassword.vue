<template>
  <Toast />
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-violet-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Back Button -->
      <button
        @click="goBack"
        class="mb-4 flex items-center gap-2 text-indigo-600 hover:text-indigo-700 transition-colors"
      >
        <i class="pi pi-arrow-left"></i>
        <span>Back to Login</span>
      </button>

      <!-- Card -->
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <i class="pi pi-lock text-indigo-600 text-2xl"></i>
          </div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">Forgot Your Password?</h1>
          <p class="text-gray-600 text-sm">Enter your ID number or email to find your account</p>
        </div>

        <!-- Find Account Form -->
        <div v-if="!accountFound" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">ID Number or Email</label>
            <input
              v-model="identifier"
              type="text"
              placeholder="Enter your ID number or email"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              @keyup.enter="findAccount"
            />
          </div>

          <button
            @click="findAccount"
            :disabled="isLoading || !identifier.trim()"
            class="w-full py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <i v-if="isLoading" class="pi pi-spin pi-spinner"></i>
            <i v-else class="pi pi-search"></i>
            <span>{{ isLoading ? 'Searching...' : 'Find Account' }}</span>
          </button>
        </div>

        <!-- Account Found - No Request -->
        <div v-else-if="accountFound && !accountData.has_request" class="space-y-4">
          <div class="bg-green-50 border border-green-200 rounded-lg p-4">
            <div class="flex items-start gap-3">
              <i class="pi pi-check-circle text-green-600 text-xl mt-0.5"></i>
              <div class="flex-1">
                <h3 class="font-semibold text-green-900 mb-1">Account Found!</h3>
                <p class="text-sm text-green-700 font-medium mb-1">{{ accountData.name }} • {{ accountData.role.charAt(0).toUpperCase() + accountData.role.slice(1) }}</p>
                <p class="text-xs text-green-600 mb-0.5">ID Number: {{ accountData.id_number || accountData.username }}</p>
                <p class="text-xs text-green-600">Email: {{ accountData.email }}</p>
              </div>
            </div>
          </div>

          <!-- ID Verification Section -->
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 class="font-semibold text-blue-900 mb-2 flex items-center gap-2">
              <i class="pi pi-shield"></i>
              Verify Your Identity
            </h4>
            <p class="text-sm text-blue-700 mb-4">Please upload clear photos of your ID (front and back) for verification.</p>
            
            <!-- Front Photo Upload -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">Front of ID *</label>
              <input
                type="file"
                ref="frontPhotoInput"
                @change="handleFrontPhotoUpload"
                accept="image/jpeg,image/jpg,image/png"
                class="hidden"
              />
              <button
                @click="$refs.frontPhotoInput.click()"
                class="w-full py-2 px-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-indigo-500 transition-colors flex items-center justify-center gap-2 text-gray-600 hover:text-indigo-600"
              >
                <i class="pi pi-upload"></i>
                <span>{{ idPhotoFront ? 'Change Photo' : 'Choose Photo' }}</span>
              </button>
              <div v-if="idPhotoFrontPreview" class="mt-2">
                <img :src="idPhotoFrontPreview" alt="Front of ID" class="w-full h-48 object-contain border rounded-lg" />
                <p class="text-xs text-gray-600 mt-1">{{ idPhotoFront.name }} ({{ formatFileSize(idPhotoFront.size) }})</p>
              </div>
            </div>

            <!-- Back Photo Upload -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Back of ID *</label>
              <input
                type="file"
                ref="backPhotoInput"
                @change="handleBackPhotoUpload"
                accept="image/jpeg,image/jpg,image/png"
                class="hidden"
              />
              <button
                @click="$refs.backPhotoInput.click()"
                class="w-full py-2 px-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-indigo-500 transition-colors flex items-center justify-center gap-2 text-gray-600 hover:text-indigo-600"
              >
                <i class="pi pi-upload"></i>
                <span>{{ idPhotoBack ? 'Change Photo' : 'Choose Photo' }}</span>
              </button>
              <div v-if="idPhotoBackPreview" class="mt-2">
                <img :src="idPhotoBackPreview" alt="Back of ID" class="w-full h-48 object-contain border rounded-lg" />
                <p class="text-xs text-gray-600 mt-1">{{ idPhotoBack.name }} ({{ formatFileSize(idPhotoBack.size) }})</p>
              </div>
            </div>
          </div>

          <button
            @click="sendRecoveryRequest"
            :disabled="isLoading || !idPhotoFront || !idPhotoBack"
            class="w-full py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            :title="!idPhotoFront || !idPhotoBack ? 'Please upload both front and back photos of your ID' : ''"
          >
            <i v-if="isLoading" class="pi pi-spin pi-spinner"></i>
            <i v-else class="pi pi-send"></i>
            <span>{{ isLoading ? 'Sending...' : 'Send Recovery Request' }}</span>
          </button>

          <button
            @click="resetForm"
            class="w-full py-2 text-gray-600 hover:text-gray-800 transition-colors text-sm"
          >
            Search Different Account
          </button>
        </div>

        <!-- Account Found - Pending Request -->
        <div v-else-if="accountFound && accountData.request_status === 'pending'" class="space-y-4">
          <div class="bg-amber-50 border border-amber-200 rounded-lg p-4">
            <div class="flex items-start gap-3">
              <i class="pi pi-clock text-amber-600 text-xl mt-0.5"></i>
              <div class="flex-1">
                <h3 class="font-semibold text-amber-900 mb-1">Request Pending</h3>
                <p class="text-sm text-amber-700 font-medium mb-1">{{ accountData.name }} • {{ accountData.role.charAt(0).toUpperCase() + accountData.role.slice(1) }}</p>
                <p class="text-xs text-amber-600 mb-0.5">ID Number: {{ accountData.id_number || accountData.username }}</p>
                <p class="text-xs text-amber-600">Email: {{ accountData.email }}</p>
              </div>
            </div>
          </div>

          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p class="text-sm text-blue-800">
              <i class="pi pi-info-circle mr-2"></i>
              Your password recovery request is waiting for admin approval. Please check back later.
            </p>
          </div>

          <button
            @click="resetForm"
            class="w-full py-2 text-gray-600 hover:text-gray-800 transition-colors text-sm"
          >
            Search Different Account
          </button>
        </div>

        <!-- Account Found - Approved Request -->
        <div v-else-if="accountFound && accountData.request_status === 'approved'" class="space-y-4">
          <div class="bg-green-50 border border-green-200 rounded-lg p-4">
            <div class="flex items-start gap-3">
              <i class="pi pi-check-circle text-green-600 text-xl mt-0.5"></i>
              <div class="flex-1">
                <h3 class="font-semibold text-green-900 mb-1">Password Reset Approved!</h3>
                <p class="text-sm text-green-700 font-medium mb-1">{{ accountData.name }} • {{ accountData.role.charAt(0).toUpperCase() + accountData.role.slice(1) }}</p>
                <p class="text-xs text-green-600 mb-0.5">ID Number: {{ accountData.id_number || accountData.username }}</p>
                <p class="text-xs text-green-600">Email: {{ accountData.email }}</p>
              </div>
            </div>
          </div>

          <div class="bg-indigo-50 border-2 border-indigo-300 rounded-lg p-6">
            <p class="text-sm text-gray-700 mb-3 text-center">Your temporary password is:</p>
            <div class="bg-white border-2 border-indigo-400 rounded-lg p-4 text-center">
              <p class="text-2xl font-bold text-indigo-600 tracking-wider">{{ accountData.temporary_password }}</p>
            </div>
            <p class="text-xs text-gray-600 mt-3 text-center">
              You can now login with this password. Please change it in your settings after logging in.
            </p>
          </div>

          <button
            @click="goToLogin"
            class="w-full py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition-colors flex items-center justify-center gap-2"
          >
            <i class="pi pi-sign-in"></i>
            <span>Go to Login</span>
          </button>
        </div>

        <!-- Account Found - Rejected Request -->
        <div v-else-if="accountFound && accountData.request_status === 'rejected'" class="space-y-4">
          <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <div class="flex items-start gap-3">
              <i class="pi pi-times-circle text-red-600 text-xl mt-0.5"></i>
              <div class="flex-1">
                <h3 class="font-semibold text-red-900 mb-1">Request Rejected</h3>
                <p class="text-sm text-red-700 font-medium mb-1">{{ accountData.name }} • {{ accountData.role.charAt(0).toUpperCase() + accountData.role.slice(1) }}</p>
                <p class="text-xs text-red-600 mb-0.5">ID Number: {{ accountData.id_number || accountData.username }}</p>
                <p class="text-xs text-red-600">Email: {{ accountData.email }}</p>
              </div>
            </div>
          </div>

          <p class="text-sm text-gray-600">
            Your previous recovery request was rejected. You can submit a new request.
          </p>

          <button
            @click="sendRecoveryRequest"
            :disabled="isLoading"
            class="w-full py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <i v-if="isLoading" class="pi pi-spin pi-spinner"></i>
            <i v-else class="pi pi-send"></i>
            <span>{{ isLoading ? 'Sending...' : 'Send New Request' }}</span>
          </button>

          <button
            @click="resetForm"
            class="w-full py-2 text-gray-600 hover:text-gray-800 transition-colors text-sm"
          >
            Search Different Account
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import Toast from 'primevue/toast';

const router = useRouter();
const toast = useToast();

const identifier = ref('');
const isLoading = ref(false);
const accountFound = ref(false);
const accountData = ref(null);

// ID Photo upload state
const idPhotoFront = ref(null);
const idPhotoBack = ref(null);
const idPhotoFrontPreview = ref(null);
const idPhotoBackPreview = ref(null);
const frontPhotoInput = ref(null);
const backPhotoInput = ref(null);

// File upload handlers
const handleFrontPhotoUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
  if (!allowedTypes.includes(file.type)) {
    toast.add({ severity: 'error', summary: 'Invalid File', detail: 'Please upload only JPG or PNG images', life: 4000 });
    event.target.value = '';
    return;
  }

  // Validate file size (10MB)
  const maxSize = 10 * 1024 * 1024;
  if (file.size > maxSize) {
    toast.add({ severity: 'error', summary: 'File Too Large', detail: 'Front photo must be less than 10MB', life: 4000 });
    event.target.value = '';
    return;
  }

  idPhotoFront.value = file;
  
  // Create preview
  const reader = new FileReader();
  reader.onload = (e) => {
    idPhotoFrontPreview.value = e.target.result;
  };
  reader.readAsDataURL(file);
};

const handleBackPhotoUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
  if (!allowedTypes.includes(file.type)) {
    toast.add({ severity: 'error', summary: 'Invalid File', detail: 'Please upload only JPG or PNG images', life: 4000 });
    event.target.value = '';
    return;
  }

  // Validate file size (10MB)
  const maxSize = 10 * 1024 * 1024;
  if (file.size > maxSize) {
    toast.add({ severity: 'error', summary: 'File Too Large', detail: 'Back photo must be less than 10MB', life: 4000 });
    event.target.value = '';
    return;
  }

  idPhotoBack.value = file;
  
  // Create preview
  const reader = new FileReader();
  reader.onload = (e) => {
    idPhotoBackPreview.value = e.target.result;
  };
  reader.readAsDataURL(file);
};

// Format file size for display
const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
};

const findAccount = async () => {
  if (!identifier.value.trim()) return;

  isLoading.value = true;
  try {
    const response = await axios.post('/api/password-recovery/find-account/', {
      identifier: identifier.value.trim()
    });

    accountFound.value = true;
    accountData.value = response.data;
    console.log('Account found:', response.data);
  } catch (error) {
    console.error('Error finding account:', error);
    if (error.response?.status === 404) {
      toast.add({ severity: 'error', summary: 'Not Found', detail: 'Account not found. Please check your ID number or email.', life: 4000 });
    } else if (error.response?.status === 403) {
      toast.add({ severity: 'warn', summary: 'Access Denied', detail: 'Admin accounts cannot use password recovery.', life: 4000 });
    } else {
      toast.add({ severity: 'error', summary: 'Error', detail: 'An error occurred. Please try again.', life: 4000 });
    }
  } finally {
    isLoading.value = false;
  }
};

const sendRecoveryRequest = async () => {
  // Validate photos are uploaded
  if (!idPhotoFront.value || !idPhotoBack.value) {
    toast.add({ severity: 'warn', summary: 'Photos Required', detail: 'Please upload both front and back photos of your ID', life: 4000 });
    return;
  }

  isLoading.value = true;
  try {
    // Create FormData to send files
    const formData = new FormData();
    formData.append('user_id', accountData.value.user_id);
    formData.append('id_photo_front', idPhotoFront.value);
    formData.append('id_photo_back', idPhotoBack.value);

    const response = await axios.post('/api/password-recovery/request/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    toast.add({ severity: 'success', summary: 'Request Sent', detail: 'Recovery request sent successfully! Please wait for admin approval.', life: 4000 });
    
    // Reset photo uploads
    idPhotoFront.value = null;
    idPhotoBack.value = null;
    idPhotoFrontPreview.value = null;
    idPhotoBackPreview.value = null;
    
    // Refresh account data to show pending status
    await findAccount();
  } catch (error) {
    console.error('Error sending recovery request:', error);
    const errorMessage = error.response?.data?.error || 'An error occurred while sending the request. Please try again.';
    toast.add({ severity: 'error', summary: 'Error', detail: errorMessage, life: 4000 });
  } finally {
    isLoading.value = false;
  }
};

// Get CSRF token from cookie
const getCsrfToken = () => {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

const resetForm = () => {
  identifier.value = '';
  accountFound.value = false;
  accountData.value = null;
  idPhotoFront.value = null;
  idPhotoBack.value = null;
  idPhotoFrontPreview.value = null;
  idPhotoBackPreview.value = null;
};

const emit = defineEmits(['navigate']);

const goBack = () => {
  emit('navigate', 'Login');
};

const goToLogin = () => {
  emit('navigate', 'Login');
};
</script>

<style scoped>
/* Add any custom styles here */
</style>
