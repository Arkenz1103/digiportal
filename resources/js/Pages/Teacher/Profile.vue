<template>
    <div class="flex flex-col h-screen bg-gray-50">
        <!-- Header -->
        <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-4 md:p-6 shadow-lg">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl md:text-3xl font-bold text-white">My Profile</h1>
                    <p class="text-white/90 mt-1 text-sm">Manage your personal information and preferences</p>
                </div>
                <button
                    @click="goBackToHome"
                    class="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-all duration-200"
                >
                    <i class="pi pi-arrow-left"></i>
                    <span class="hidden md:inline">Back to Home</span>
                </button>
            </div>
        </div>

        <!-- Main Content -->
        <div class="flex-1 overflow-y-auto p-4 md:p-6">
            <div class="max-w-4xl mx-auto space-y-6">
                <!-- Profile Picture Section -->
                <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
                    <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                        <i class="pi pi-image text-indigo-600"></i>
                        Profile Picture
                    </h2>
                    <div class="flex flex-col md:flex-row items-center gap-6">
                        <div class="relative">
                            <div class="w-32 h-32 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-4xl font-bold shadow-lg overflow-hidden border-4 border-white">
                                <img
                                    v-if="profileData.profilePicture"
                                    :src="profileData.profilePicture"
                                    :alt="`${profileData.name}'s profile picture`"
                                    class="w-full h-full object-cover"
                                    @error="onProfileImageError"
                                />
                                <span v-else>
                                    {{ getInitials(profileData.name) }}
                                </span>
                            </div>
                            <button
                                @click="triggerFileUpload"
                                class="absolute bottom-0 right-0 w-10 h-10 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full flex items-center justify-center shadow-lg transition-colors duration-200"
                            >
                                <i class="pi pi-camera text-sm"></i>
                            </button>
                            <input
                                ref="fileInput"
                                type="file"
                                accept="image/*"
                                @change="handleImageUpload"
                                class="hidden"
                            />
                        </div>
                        <div class="flex-1 text-center md:text-left">
                            <h3 class="text-lg font-semibold text-gray-800">{{ profileData.name }}</h3>
                            <p class="text-gray-600">{{ profileData.email }}</p>
                            <p class="text-sm text-gray-500 mt-1">Teacher</p>
                        </div>
                    </div>
                </div>

                <!-- Personal Information -->
                <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">
                            <i class="pi pi-user text-indigo-600"></i>
                            Personal Information
                        </h2>
                        <button
                            v-if="!isEditing"
                            @click="startEditing"
                            class="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors duration-200"
                        >
                            <i class="pi pi-pencil"></i>
                            Edit
                        </button>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <!-- Full Name -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                            <input
                                v-model="editData.name"
                                :disabled="!isEditing"
                                type="text"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
                                placeholder="Enter your full name"
                            />
                        </div>

                        <!-- Email -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                            <input
                                v-model="editData.email"
                                :disabled="!isEditing"
                                type="email"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
                                placeholder="Enter your email"
                            />
                        </div>

                        <!-- Phone Number -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
                            <input
                                v-model="editData.phone"
                                :disabled="!isEditing"
                                type="tel"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
                                placeholder="Enter your phone number"
                            />
                        </div>

                        <!-- Department -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Department</label>
                            <input
                                v-model="editData.department"
                                :disabled="!isEditing"
                                type="text"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
                                placeholder="Enter your department"
                            />
                        </div>

                        <!-- Subject Specialization -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Subject Specialization</label>
                            <input
                                v-model="editData.subject"
                                :disabled="!isEditing"
                                type="text"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
                                placeholder="e.g., Mathematics, Science"
                            />
                        </div>

                        <!-- Years of Experience -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Years of Experience</label>
                            <input
                                v-model="editData.experience"
                                :disabled="!isEditing"
                                type="number"
                                min="0"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
                                placeholder="Enter years"
                            />
                        </div>
                    </div>

                    <!-- Bio -->
                    <div class="mt-4">
                        <label class="block text-sm font-medium text-gray-700 mb-2">Bio</label>
                        <textarea
                            v-model="editData.bio"
                            :disabled="!isEditing"
                            rows="4"
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed resize-none"
                            placeholder="Tell us about yourself..."
                        ></textarea>
                    </div>

                    <!-- Action Buttons (when editing) -->
                    <div v-if="isEditing" class="flex items-center gap-3 mt-6 pt-6 border-t border-gray-200">
                        <button
                            @click="saveProfile"
                            :disabled="isSaving"
                            class="flex items-center gap-2 px-6 py-2.5 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <i class="pi pi-check"></i>
                            <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
                        </button>
                        <button
                            @click="cancelEditing"
                            :disabled="isSaving"
                            class="flex items-center gap-2 px-6 py-2.5 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors duration-200 disabled:opacity-50"
                        >
                            <i class="pi pi-times"></i>
                            Cancel
                        </button>
                    </div>
                </div>

                <!-- Account Settings -->
                <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
                    <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                        <i class="pi pi-lock text-indigo-600"></i>
                        Account Settings
                    </h2>
                    
                    <div class="space-y-4">
                        <!-- Change Password -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <div>
                                <h3 class="font-semibold text-gray-800">Change Password</h3>
                                <p class="text-sm text-gray-600">Update your password to keep your account secure</p>
                            </div>
                            <button
                                @click="showChangePasswordDialog = true"
                                class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors duration-200"
                            >
                                Change
                            </button>
                        </div>

                        <!-- Account Status -->
                        <div class="flex items-center justify-between p-4 bg-green-50 rounded-lg border border-green-200">
                            <div>
                                <h3 class="font-semibold text-gray-800">Account Status</h3>
                                <p class="text-sm text-gray-600">Your account is active and verified</p>
                            </div>
                            <span class="px-4 py-2 bg-green-600 text-white rounded-lg font-medium">
                                Active
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Change Password Dialog -->
        <Dialog 
            v-model:visible="showChangePasswordDialog" 
            modal 
            header="Change Password"
            :style="{ width: '90vw', maxWidth: '500px' }"
        >
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Current Password</label>
                    <input
                        v-model="passwordData.current"
                        type="password"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                        placeholder="Enter current password"
                    />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">New Password</label>
                    <input
                        v-model="passwordData.new"
                        type="password"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                        placeholder="Enter new password"
                    />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Confirm New Password</label>
                    <input
                        v-model="passwordData.confirm"
                        type="password"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                        placeholder="Confirm new password"
                    />
                </div>
            </div>

            <template #footer>
                <div class="flex items-center justify-end gap-3">
                    <button
                        @click="showChangePasswordDialog = false"
                        class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors duration-200"
                    >
                        Cancel
                    </button>
                    <button
                        @click="changePassword"
                        class="px-5 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors duration-200"
                    >
                        Update Password
                    </button>
                </div>
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import Dialog from 'primevue/dialog';
import { useToast } from '@/Composables/useToast';

// Define emits
const emit = defineEmits(['navigate']);

// Initialize toast
const { showSuccess, showError, showInfo } = useToast();

// Profile data
const profileData = reactive({
    name: 'Teacher User',
    email: 'teacher@gmail.com',
    phone: '',
    department: '',
    subject: '',
    experience: 0,
    bio: '',
    profilePicture: null
});

// Edit mode
const isEditing = ref(false);
const isSaving = ref(false);
const editData = reactive({ ...profileData });

// Password change
const showChangePasswordDialog = ref(false);
const passwordData = reactive({
    current: '',
    new: '',
    confirm: ''
});

// File input ref
const fileInput = ref(null);

// Load profile data
onMounted(() => {
    loadProfile();
});

const loadProfile = () => {
    // Load from localStorage or API
    const savedName = localStorage.getItem('digiportal_user_name');
    const savedEmail = localStorage.getItem('digiportal_user_email');
    const savedAvatar = localStorage.getItem('digiportal_user_avatar');
    
    if (savedName) profileData.name = savedName;
    if (savedEmail) profileData.email = savedEmail;
    
    // Load additional profile data from localStorage
    const savedProfile = localStorage.getItem('digiportal_teacher_profile');
    if (savedProfile) {
        const parsed = JSON.parse(savedProfile);
        Object.assign(profileData, parsed);
    }
    if (!profileData.profilePicture && savedAvatar) {
        profileData.profilePicture = savedAvatar;
    }
    
    // Copy to edit data
    Object.assign(editData, profileData);
};

const getInitials = (name) => {
    if (!name) return 'TU';
    const parts = name.split(' ');
    if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
};

const startEditing = () => {
    isEditing.value = true;
    Object.assign(editData, profileData);
};

const cancelEditing = () => {
    isEditing.value = false;
    Object.assign(editData, profileData);
};

const saveProfile = async () => {
    isSaving.value = true;
    
    try {
        // Validate required fields
        if (!editData.name || !editData.email) {
            showError('Name and email are required fields', 'Validation Error');
            return;
        }
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Save to localStorage
        Object.assign(profileData, editData);
        localStorage.setItem('digiportal_user_name', profileData.name);
        localStorage.setItem('digiportal_user_email', profileData.email);
        localStorage.setItem('digiportal_teacher_profile', JSON.stringify(profileData));
        if (profileData.profilePicture) {
            localStorage.setItem('digiportal_user_avatar', profileData.profilePicture);
        } else {
            localStorage.removeItem('digiportal_user_avatar');
        }
        
        // Dispatch event to update MainLayout
        dispatchUserDataUpdate();
        
        isEditing.value = false;
        showSuccess('Your profile has been updated successfully!', 'Profile Updated');
        
        console.log('✅ Profile saved:', profileData);
    } catch (error) {
        console.error('❌ Error saving profile:', error);
        showError('Failed to save profile. Please try again.', 'Save Failed');
    } finally {
        isSaving.value = false;
    }
};

const triggerFileUpload = () => {
    fileInput.value?.click();
};

const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
        if (file.size > 5 * 1024 * 1024) {
            showError('Image size should be less than 5MB', 'File Too Large');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = (e) => {
            profileData.profilePicture = e.target.result;
            localStorage.setItem('digiportal_teacher_profile', JSON.stringify(profileData));
            localStorage.setItem('digiportal_user_avatar', profileData.profilePicture);
            dispatchUserDataUpdate();
            showSuccess('Profile picture updated successfully!', 'Picture Updated');
        };
        reader.readAsDataURL(file);
        event.target.value = '';
    }
};

const goBackToHome = () => {
    // Check if there are unsaved changes
    if (isEditing.value) {
        const confirmLeave = confirm('You have unsaved changes. Are you sure you want to leave?');
        if (!confirmLeave) {
            return;
        }
    }
    
    emit('navigate', 'TeacherHome');
    console.log('🏠 Navigating back to Teacher Home');
};

const changePassword = () => {
    if (!passwordData.current || !passwordData.new || !passwordData.confirm) {
        showError('All password fields are required', 'Validation Error');
        return;
    }
    
    if (passwordData.new !== passwordData.confirm) {
        showError('New passwords do not match', 'Validation Error');
        return;
    }
    
    if (passwordData.new.length < 6) {
        showError('Password must be at least 6 characters long', 'Validation Error');
        return;
    }
    
    // Simulate password change
    showSuccess('Password changed successfully!', 'Password Updated');
    showChangePasswordDialog.value = false;
    passwordData.current = '';
    passwordData.new = '';
    passwordData.confirm = '';
};

const onProfileImageError = () => {
    profileData.profilePicture = null;
    localStorage.removeItem('digiportal_user_avatar');
    const savedProfile = localStorage.getItem('digiportal_teacher_profile');
    if (savedProfile) {
        const parsed = JSON.parse(savedProfile);
        parsed.profilePicture = null;
        localStorage.setItem('digiportal_teacher_profile', JSON.stringify(parsed));
    }
    dispatchUserDataUpdate();
};

const dispatchUserDataUpdate = () => {
    const detail = {
        name: profileData.name,
        email: profileData.email,
        avatar: profileData.profilePicture
    };
    window.dispatchEvent(new CustomEvent('userDataChanged', { detail }));
    window.dispatchEvent(new CustomEvent('user-data-updated', { detail }));
};
</script>

<style scoped>
/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}
</style>
