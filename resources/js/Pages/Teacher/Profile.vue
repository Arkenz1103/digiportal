<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useToast } from '../../composables/useToast';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

const { showSuccess, showError, showInfo } = useToast();

// User data
const user = ref({
    id: null,
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    id_number: '',
    department: '',
    years_of_experience: '',
    bio: '',
    profile_picture: null,
    role: 'teacher'
});

// Form states
const isEditingProfile = ref(false);
const isSavingProfile = ref(false);
const isChangingPassword = ref(false);
const showPasswordDialog = ref(false);
const showAccountStatusDialog = ref(false);

// Password change form
const passwordForm = ref({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
});

// Profile picture
const profilePicturePreview = ref(null);
const profilePictureFile = ref(null);

// Load user profile
const loadUserProfile = async () => {
    try {
        const response = await axios.get('/api/user/profile/');
        user.value = response.data;
        
        // Set profile picture preview if exists
        if (response.data.profile_picture_url) {
            profilePicturePreview.value = response.data.profile_picture_url;
        }
        
        console.log('✅ User profile loaded:', user.value);
    } catch (error) {
        console.error('❌ Error loading profile:', error);
        showError('Failed to load profile', 'Error');
    }
};

// Handle profile picture upload
const handleProfilePictureChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        if (file.size > 5 * 1024 * 1024) { // 5MB limit
            showError('File size must be less than 5MB', 'File Too Large');
            return;
        }
        
        if (!file.type.startsWith('image/')) {
            showError('Please select an image file', 'Invalid File Type');
            return;
        }
        
        profilePictureFile.value = file;
        
        // Create preview
        const reader = new FileReader();
        reader.onload = (e) => {
            profilePicturePreview.value = e.target.result;
        };
        reader.readAsDataURL(file);
        
        showInfo('Profile picture selected. Click "Save" to update.', 'Picture Selected');
    }
};

// Trigger file input
const triggerFileInput = () => {
    document.getElementById('profilePictureInput').click();
};

// Save profile changes
const saveProfile = async () => {
    if (!user.value.first_name || !user.value.email) {
        showError('Please fill in all required fields', 'Validation Error');
        return;
    }
    
    try {
        isSavingProfile.value = true;
        
        const formData = new FormData();
        formData.append('first_name', user.value.first_name);
        formData.append('last_name', user.value.last_name);
        formData.append('email', user.value.email);
        formData.append('phone_number', user.value.phone_number || '');
        formData.append('department', user.value.department || '');
        formData.append('years_of_experience', user.value.years_of_experience || '');
        formData.append('bio', user.value.bio || '');
        if (profilePictureFile.value) {
            formData.append('profile_picture', profilePictureFile.value);
        }
        
        const response = await axios.put('/api/user/profile/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        
        user.value = response.data;
        if (response.data.profile_picture_url) {
            profilePicturePreview.value = response.data.profile_picture_url;
        }
        
        showSuccess('Profile updated successfully!', 'Saved');
        isEditingProfile.value = false;
        profilePictureFile.value = null;
        
        console.log('✅ Profile saved:', user.value);
    } catch (error) {
        console.error('❌ Error saving profile:', error);
        showError(error.response?.data?.error || 'Failed to save profile', 'Error');
    } finally {
        isSavingProfile.value = false;
    }
};

// Cancel editing
const cancelEdit = () => {
    isEditingProfile.value = false;
    profilePicturePreview.value = null;
    profilePictureFile.value = null;
    loadUserProfile(); // Reload original data
};

// Open password change dialog
const openPasswordDialog = () => {
    passwordForm.value = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
    };
    showPasswordDialog.value = true;
};

// Change password
const changePassword = async () => {
    if (!passwordForm.value.currentPassword || !passwordForm.value.newPassword || !passwordForm.value.confirmPassword) {
        showError('Please fill in all password fields', 'Validation Error');
        return;
    }
    
    if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
        showError('New passwords do not match', 'Validation Error');
        return;
    }
    
    if (passwordForm.value.newPassword.length < 8) {
        showError('Password must be at least 8 characters long', 'Validation Error');
        return;
    }
    
    try {
        isChangingPassword.value = true;
        
        const response = await axios.post('/api/user/change-password/', {
            current_password: passwordForm.value.currentPassword,
            new_password: passwordForm.value.newPassword
        });
        
        showSuccess('Password changed successfully!', 'Success');
        showPasswordDialog.value = false;
        passwordForm.value = {
            currentPassword: '',
            newPassword: '',
            confirmPassword: ''
        };
        
        console.log('✅ Password changed');
    } catch (error) {
        console.error('❌ Error changing password:', error);
        showError(error.response?.data?.error || 'Failed to change password', 'Error');
    } finally {
        isChangingPassword.value = false;
    }
};

// Account status actions
const openAccountStatusDialog = () => {
    showAccountStatusDialog.value = true;
};

const verifyAccount = async () => {
    try {
        // TODO: Implement verification logic
        showInfo('Verification email sent to your email address', 'Verification Sent');
        showAccountStatusDialog.value = false;
    } catch (error) {
        showError('Failed to send verification email', 'Error');
    }
};

// Load profile on mount
onMounted(() => {
    loadUserProfile();
});
</script>

<template>
    <div class="flex flex-col min-h-screen">
        <!-- Header -->
        <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-4 md:p-6 shadow-lg rounded-t-xl">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl md:text-3xl font-bold text-white">My Profile</h1>
                    <p class="text-white/80 text-sm mt-1">Manage your personal information and preferences</p>
                </div>
                <button
                    @click="$emit('navigate', 'TeacherHome')"
                    class="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-colors duration-200"
                >
                    <i class="pi pi-arrow-left"></i>
                    <span class="hidden md:inline">Back to Home</span>
                </button>
            </div>
        </div>

        <!-- Main Content -->
        <div class="w-full bg-white/80 flex-1">
            <div class="max-w-4xl mx-auto p-4 md:p-6 space-y-6">
                
                <!-- Profile Picture Section -->
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    <div class="px-6 py-4 bg-gradient-to-r from-indigo-50 to-purple-50 border-b border-indigo-100">
                        <div class="flex items-center gap-2">
                            <i class="pi pi-image text-indigo-600"></i>
                            <h2 class="text-lg font-semibold text-gray-900">Profile Picture</h2>
                        </div>
                    </div>
                    
                    <div class="p-6">
                        <div class="flex items-center gap-6">
                            <!-- Profile Picture Display -->
                            <div class="relative">
                                <div class="w-24 h-24 rounded-full overflow-hidden bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg">
                                    <img 
                                        v-if="profilePicturePreview || user.profile_picture"
                                        :src="profilePicturePreview || user.profile_picture"
                                        alt="Profile"
                                        class="w-full h-full object-cover"
                                    />
                                    <span v-else class="text-3xl font-bold text-white">
                                        {{ user.first_name?.charAt(0) || 'T' }}{{ user.last_name?.charAt(0) || 'U' }}
                                    </span>
                                </div>
                                <button
                                    v-if="isEditingProfile"
                                    @click="triggerFileInput"
                                    class="absolute bottom-0 right-0 w-8 h-8 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full flex items-center justify-center shadow-lg transition-colors"
                                >
                                    <i class="pi pi-camera text-xs"></i>
                                </button>
                            </div>
                            
                            <!-- Profile Info -->
                            <div class="flex-1">
                                <h3 class="text-xl font-bold text-gray-900">{{ user.first_name }} {{ user.last_name }}</h3>
                                <p class="text-gray-600">{{ user.email }}</p>
                                <p class="text-sm text-indigo-600 mt-1">{{ user.role === 'teacher' ? 'Teacher' : user.role }}</p>
                            </div>
                            
                            <!-- Hidden file input -->
                            <input
                                type="file"
                                id="profilePictureInput"
                                accept="image/*"
                                @change="handleProfilePictureChange"
                                class="hidden"
                            />
                        </div>
                    </div>
                </div>

                <!-- Personal Information Section -->
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    <div class="px-6 py-4 bg-gradient-to-r from-indigo-50 to-purple-50 border-b border-indigo-100 flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <i class="pi pi-user text-indigo-600"></i>
                            <h2 class="text-lg font-semibold text-gray-900">Personal Information</h2>
                        </div>
                        <button
                            v-if="!isEditingProfile"
                            @click="isEditingProfile = true"
                            class="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors text-sm font-medium"
                        >
                            <i class="pi pi-pencil"></i>
                            <span>Edit</span>
                        </button>
                        <div v-else class="flex gap-2">
                            <button
                                @click="cancelEdit"
                                class="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors text-sm font-medium"
                            >
                                Cancel
                            </button>
                            <button
                                @click="saveProfile"
                                :disabled="isSavingProfile"
                                class="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors text-sm font-medium disabled:opacity-50"
                            >
                                <i class="pi pi-check"></i>
                                <span>{{ isSavingProfile ? 'Saving...' : 'Save' }}</span>
                            </button>
                        </div>
                    </div>
                    
                    <div class="p-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <!-- Full Name -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                                <input
                                    v-model="user.first_name"
                                    :disabled="!isEditingProfile"
                                    type="text"
                                    placeholder="Johnny Sins"
                                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-50 disabled:text-gray-500"
                                />
                            </div>
                            
                            <!-- Email Address -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                                <input
                                    v-model="user.email"
                                    :disabled="!isEditingProfile"
                                    type="email"
                                    placeholder="teacher@gmail.com"
                                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-50 disabled:text-gray-500"
                                />
                            </div>
                            
                            <!-- Phone Number -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
                                <input
                                    v-model="user.phone_number"
                                    :disabled="!isEditingProfile"
                                    type="tel"
                                    placeholder="+123-456-7890"
                                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-50 disabled:text-gray-500"
                                />
                            </div>
                            
                            <!-- Teacher ID (Read-only) -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Teacher ID</label>
                                <input
                                    :value="user.id_number || 'Not assigned'"
                                    disabled
                                    type="text"
                                    :class="[
                                        'w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50',
                                        user.id_number ? 'text-gray-700' : 'text-gray-400 italic'
                                    ]"
                                />
                            </div>
                            
                            <!-- Department -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Department</label>
                                <input
                                    :value="user.department || 'Not assigned'"
                                    disabled
                                    type="text"
                                    :class="[
                                        'w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50',
                                        user.department ? 'text-gray-700' : 'text-gray-400 italic'
                                    ]"
                                />
                            </div>
                            
                            <!-- Years of Experience -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Years of Experience</label>
                                <input
                                    v-model="user.years_of_experience"
                                    :disabled="!isEditingProfile"
                                    type="number"
                                    placeholder="5"
                                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-50 disabled:text-gray-500"
                                />
                            </div>
                            
                            <!-- Bio (Full Width) -->
                            <div class="md:col-span-2">
                                <label class="block text-sm font-medium text-gray-700 mb-2">Bio</label>
                                <textarea
                                    v-model="user.bio"
                                    :disabled="!isEditingProfile"
                                    rows="4"
                                    placeholder="Tell us about yourself..."
                                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-50 disabled:text-gray-500 resize-none"
                                ></textarea>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Account Settings Section -->
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    <div class="px-6 py-4 bg-gradient-to-r from-indigo-50 to-purple-50 border-b border-indigo-100">
                        <div class="flex items-center gap-2">
                            <i class="pi pi-cog text-indigo-600"></i>
                            <h2 class="text-lg font-semibold text-gray-900">Account Settings</h2>
                        </div>
                    </div>
                    
                    <div class="p-6 space-y-4">
                        <!-- Change Password -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <div>
                                <h3 class="font-medium text-gray-900">Change Password</h3>
                                <p class="text-sm text-gray-600 mt-1">Update your password to keep your account secure</p>
                            </div>
                            <button
                                @click="openPasswordDialog"
                                class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors text-sm font-medium"
                            >
                                Change
                            </button>
                        </div>
                        
                        <!-- Account Status -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <div>
                                <h3 class="font-medium text-gray-900">Account Status</h3>
                                <p class="text-sm text-gray-600 mt-1">Your account is active and verified</p>
                            </div>
                            <button
                                @click="openAccountStatusDialog"
                                class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors text-sm font-medium"
                            >
                                Active
                            </button>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <!-- Change Password Dialog -->
        <Dialog 
            v-model:visible="showPasswordDialog"
            modal
            header="Change Password"
            :style="{ width: '90vw', maxWidth: '500px' }"
            :dismissableMask="true"
        >
            <div class="space-y-4">
                <!-- Current Password -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Current Password</label>
                    <input
                        v-model="passwordForm.currentPassword"
                        type="password"
                        placeholder="Enter current password"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </div>
                
                <!-- New Password -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">New Password</label>
                    <input
                        v-model="passwordForm.newPassword"
                        type="password"
                        placeholder="Enter new password (min 8 characters)"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </div>
                
                <!-- Confirm Password -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Confirm New Password</label>
                    <input
                        v-model="passwordForm.confirmPassword"
                        type="password"
                        placeholder="Confirm new password"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </div>
                
                <!-- Password Requirements -->
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                    <p class="text-xs text-blue-800 font-medium mb-1">Password Requirements:</p>
                    <ul class="text-xs text-blue-700 space-y-1 ml-4 list-disc">
                        <li>At least 8 characters long</li>
                        <li>Contains uppercase and lowercase letters</li>
                        <li>Contains at least one number</li>
                    </ul>
                </div>
            </div>
            
            <template #footer>
                <div class="flex justify-end gap-2">
                    <Button
                        label="Cancel"
                        @click="showPasswordDialog = false"
                        class="p-button-secondary"
                        style="background: #f3f4f6; border: 1px solid #d1d5db; color: #1f2937;"
                    />
                    <Button
                        :label="isChangingPassword ? 'Changing...' : 'Change Password'"
                        @click="changePassword"
                        :disabled="isChangingPassword"
                        style="background: linear-gradient(to right, #4f46e5, #6366f1); border: none;"
                    />
                </div>
            </template>
        </Dialog>

        <!-- Account Status Dialog -->
        <Dialog 
            v-model:visible="showAccountStatusDialog"
            modal
            header="Account Status"
            :style="{ width: '90vw', maxWidth: '500px' }"
            :dismissableMask="true"
        >
            <div class="space-y-4">
                <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div class="flex items-center gap-3">
                        <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                            <i class="pi pi-check-circle text-green-600 text-2xl"></i>
                        </div>
                        <div>
                            <h3 class="font-semibold text-green-900">Account Active</h3>
                            <p class="text-sm text-green-700">Your account is in good standing</p>
                        </div>
                    </div>
                </div>
                
                <div class="space-y-2">
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <span class="text-sm text-gray-700">Email Verified</span>
                        <i class="pi pi-check text-green-600"></i>
                    </div>
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <span class="text-sm text-gray-700">Profile Complete</span>
                        <i class="pi pi-check text-green-600"></i>
                    </div>
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <span class="text-sm text-gray-700">Account Type</span>
                        <span class="text-sm font-medium text-indigo-600">Teacher</span>
                    </div>
                </div>
            </div>
            
            <template #footer>
                <div class="flex justify-end">
                    <Button
                        label="Close"
                        @click="showAccountStatusDialog = false"
                        style="background: linear-gradient(to right, #4f46e5, #6366f1); border: none;"
                    />
                </div>
            </template>
        </Dialog>

    </div>
</template>

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
