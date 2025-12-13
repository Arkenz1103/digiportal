<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from '../../axios';
import { useToast } from '../../composables/useToast';
import { useTheme } from '../../composables/useTheme';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

const { showSuccess, showError, showInfo, showWarning } = useToast();
const { currentTheme, setTheme } = useTheme();

// Settings data
const settings = ref({
    notifications: {
        emailNotifications: true,
        pushNotifications: true,
        submissionAlerts: true,
        remarkAlerts: true,
        activityReminders: true
    },
    privacy: {
        profileVisibility: 'public',
        showEmail: false,
        showPhone: false
    },
    preferences: {
        language: 'en',
        timezone: 'Asia/Manila',
        dateFormat: 'MM/DD/YYYY',
        theme: 'light'
    }
});

// Dialog states
const showDeleteAccountDialog = ref(false);
const showExportDataDialog = ref(false);
const isExportingData = ref(false);
const isSavingSettings = ref(false);

// Language options
const languageOptions = [
    { value: 'en', label: 'English' },
    { value: 'fil', label: 'Filipino' },
    { value: 'es', label: 'Spanish' }
];

// Timezone options
const timezoneOptions = [
    { value: 'Asia/Manila', label: 'Asia/Manila (GMT+8)' },
    { value: 'America/New_York', label: 'America/New_York (GMT-5)' },
    { value: 'Europe/London', label: 'Europe/London (GMT+0)' }
];

// Date format options
const dateFormatOptions = [
    { value: 'MM/DD/YYYY', label: 'MM/DD/YYYY' },
    { value: 'DD/MM/YYYY', label: 'DD/MM/YYYY' },
    { value: 'YYYY-MM-DD', label: 'YYYY-MM-DD' }
];

// Theme options
const themeOptions = [
    { value: 'light', label: 'Light', icon: 'pi-sun' },
    { value: 'dark', label: 'Dark', icon: 'pi-moon' },
    { value: 'auto', label: 'Auto', icon: 'pi-desktop' }
];

// Load settings from backend
const loadSettings = async () => {
    try {
        console.log('📥 Loading settings from backend...');
        const response = await axios.get('/api/user/settings/');
        
        if (response.data) {
            settings.value = response.data;
            
            // Sync theme from backend
            if (response.data.preferences?.theme) {
                const backendTheme = response.data.preferences.theme;
                console.log('🎨 Theme from backend:', backendTheme);
                
                // Update local theme
                currentTheme.value = backendTheme;
                setTheme(backendTheme);
            }
            
            console.log('✅ Settings loaded:', settings.value);
        }
    } catch (error) {
        console.error('❌ Error loading settings:', error);
        // Don't show error if endpoint doesn't exist yet
        if (error.response?.status !== 404) {
            showError('Failed to load settings', 'Error');
        }
    }
};

// Save settings to backend
const saveSettings = async () => {
    try {
        isSavingSettings.value = true;
        
        console.log('💾 Saving settings to backend...');
        console.log('📤 Theme to save:', settings.value.preferences.theme);
        
        const response = await axios.put('/api/user/settings/', settings.value);
        
        if (response.data) {
            settings.value = response.data;
            console.log('✅ Settings saved to backend:', settings.value);
        }
        
        showSuccess('Settings saved successfully!', 'Saved');
    } catch (error) {
        console.error('❌ Error saving settings:', error);
        showError(error.response?.data?.error || 'Failed to save settings', 'Error');
    } finally {
        isSavingSettings.value = false;
    }
};

// Export data
const exportData = async () => {
    try {
        isExportingData.value = true;
        
        const response = await axios.get('/api/user/export-data/', {
            responseType: 'blob'
        });
        
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `user_data_${Date.now()}.json`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        
        showSuccess('Your data has been exported successfully!', 'Export Complete');
        showExportDataDialog.value = false;
        
        console.log('✅ Data exported');
    } catch (error) {
        console.error('❌ Error exporting data:', error);
        showError(error.response?.data?.error || 'Failed to export data', 'Error');
    } finally {
        isExportingData.value = false;
    }
};

// Delete account
const deleteAccount = async () => {
    showWarning('This feature is not yet available', 'Coming Soon');
    showDeleteAccountDialog.value = false;
};

// Watch for theme changes in settings
watch(() => settings.value.preferences.theme, (newTheme) => {
    console.log('🎨 Theme changed in settings:', newTheme);
    // Apply theme using global composable
    setTheme(newTheme);
});

// Load settings on mount
onMounted(() => {
    // Sync with global theme state
    settings.value.preferences.theme = currentTheme.value;
    
    // Load all settings from backend (will sync theme)
    loadSettings();
});
</script>

<template>
    <div class="flex flex-col min-h-screen">
        <!-- Header -->
        <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-4 md:p-6 shadow-lg rounded-t-xl">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl md:text-3xl font-bold text-white">Settings</h1>
                </div>
                <button
                    @click="$emit('navigate', 'TeacherHome')"
                    class="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-colors duration-200"
                >
                    <i class="pi pi-arrow-left"></i>
                    <span class="hidden md:inline">Back</span>
                </button>
            </div>
        </div>

        <!-- Main Content -->
        <div class="w-full bg-white/80 flex-1">
            <div class="max-w-4xl mx-auto p-4 md:p-6 space-y-6">
                
                <!-- Notifications Settings -->
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    <div class="px-6 py-4 bg-gradient-to-r from-indigo-50 to-purple-50 border-b border-indigo-100">
                        <div class="flex items-center gap-2">
                            <i class="pi pi-bell text-indigo-600"></i>
                            <h2 class="text-lg font-semibold text-gray-900">Notification Preferences</h2>
                        </div>
                    </div>
                    
                    <div class="p-6 space-y-4">
                        <!-- Email Notifications -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Email Notifications</h3>
                                <p class="text-sm text-gray-600 mt-1">Receive notifications via email</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input 
                                    type="checkbox" 
                                    v-model="settings.notifications.emailNotifications"
                                    class="sr-only peer"
                                />
                                <div class="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                            </label>
                        </div>
                        
                        <!-- Push Notifications -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Push Notifications</h3>
                                <p class="text-sm text-gray-600 mt-1">Receive push notifications in browser</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input 
                                    type="checkbox" 
                                    v-model="settings.notifications.pushNotifications"
                                    class="sr-only peer"
                                />
                                <div class="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                            </label>
                        </div>
                        
                        <!-- Submission Alerts -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Submission Alerts</h3>
                                <p class="text-sm text-gray-600 mt-1">Get notified when students submit work</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input 
                                    type="checkbox" 
                                    v-model="settings.notifications.submissionAlerts"
                                    class="sr-only peer"
                                />
                                <div class="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                            </label>
                        </div>
                        
                        <!-- Remark Alerts -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Remark Alerts</h3>
                                <p class="text-sm text-gray-600 mt-1">Get notified about new remarks and comments</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input 
                                    type="checkbox" 
                                    v-model="settings.notifications.remarkAlerts"
                                    class="sr-only peer"
                                />
                                <div class="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                            </label>
                        </div>
                        
                        <!-- Activity Reminders -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Activity Reminders</h3>
                                <p class="text-sm text-gray-600 mt-1">Reminders for upcoming activity deadlines</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input 
                                    type="checkbox" 
                                    v-model="settings.notifications.activityReminders"
                                    class="sr-only peer"
                                />
                                <div class="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Privacy Settings -->
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    <div class="px-6 py-4 bg-gradient-to-r from-indigo-50 to-purple-50 border-b border-indigo-100">
                        <div class="flex items-center gap-2">
                            <i class="pi pi-lock text-indigo-600"></i>
                            <h2 class="text-lg font-semibold text-gray-900">Privacy Settings</h2>
                        </div>
                    </div>
                    
                    <div class="p-6 space-y-4">
                        <!-- Profile Visibility -->
                        <div class="p-4 bg-gray-50 rounded-lg">
                            <h3 class="font-medium text-gray-900 mb-3">Profile Visibility</h3>
                            <select 
                                v-model="settings.privacy.profileVisibility"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            >
                                <option value="public">Public - Visible to everyone</option>
                                <option value="students">Students Only - Visible to your students</option>
                                <option value="private">Private - Only you can see</option>
                            </select>
                        </div>
                        
                        <!-- Show Email -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Show Email Address</h3>
                                <p class="text-sm text-gray-600 mt-1">Display your email on your profile</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input 
                                    type="checkbox" 
                                    v-model="settings.privacy.showEmail"
                                    class="sr-only peer"
                                />
                                <div class="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                            </label>
                        </div>
                        
                        <!-- Show Phone -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Show Phone Number</h3>
                                <p class="text-sm text-gray-600 mt-1">Display your phone number on your profile</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input 
                                    type="checkbox" 
                                    v-model="settings.privacy.showPhone"
                                    class="sr-only peer"
                                />
                                <div class="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Preferences -->
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    <div class="px-6 py-4 bg-gradient-to-r from-indigo-50 to-purple-50 border-b border-indigo-100">
                        <div class="flex items-center gap-2">
                            <i class="pi pi-sliders-h text-indigo-600"></i>
                            <h2 class="text-lg font-semibold text-gray-900">Preferences</h2>
                        </div>
                    </div>
                    
                    <div class="p-6 space-y-4">
                        <!-- Language -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Language</label>
                            <select 
                                v-model="settings.preferences.language"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            >
                                <option v-for="lang in languageOptions" :key="lang.value" :value="lang.value">
                                    {{ lang.label }}
                                </option>
                            </select>
                        </div>
                        
                        <!-- Timezone -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Timezone</label>
                            <select 
                                v-model="settings.preferences.timezone"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            >
                                <option v-for="tz in timezoneOptions" :key="tz.value" :value="tz.value">
                                    {{ tz.label }}
                                </option>
                            </select>
                        </div>
                        
                        <!-- Date Format -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Date Format</label>
                            <select 
                                v-model="settings.preferences.dateFormat"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            >
                                <option v-for="format in dateFormatOptions" :key="format.value" :value="format.value">
                                    {{ format.label }}
                                </option>
                            </select>
                        </div>
                        
                        <!-- Theme -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Theme</label>
                            <div class="grid grid-cols-3 gap-3">
                                <button
                                    v-for="theme in themeOptions"
                                    :key="theme.value"
                                    @click="settings.preferences.theme = theme.value"
                                    :class="[
                                        'p-4 border-2 rounded-lg transition-all',
                                        settings.preferences.theme === theme.value
                                            ? 'border-indigo-600 bg-indigo-50'
                                            : 'border-gray-300 hover:border-indigo-400'
                                    ]"
                                >
                                    <i :class="['pi', theme.icon, 'text-2xl mb-2', settings.preferences.theme === theme.value ? 'text-indigo-600' : 'text-gray-600']"></i>
                                    <p :class="['text-sm font-medium', settings.preferences.theme === theme.value ? 'text-indigo-600' : 'text-gray-700']">
                                        {{ theme.label }}
                                    </p>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Data & Account Management -->
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    <div class="px-6 py-4 bg-gradient-to-r from-indigo-50 to-purple-50 border-b border-indigo-100">
                        <div class="flex items-center gap-2">
                            <i class="pi pi-database text-indigo-600"></i>
                            <h2 class="text-lg font-semibold text-gray-900">Data & Account</h2>
                        </div>
                    </div>
                    
                    <div class="p-6 space-y-4">
                        <!-- Export Data -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <div>
                                <h3 class="font-medium text-gray-900">Export Your Data</h3>
                                <p class="text-sm text-gray-600 mt-1">Download a copy of your account data</p>
                            </div>
                            <button
                                @click="showExportDataDialog = true"
                                class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors text-sm font-medium"
                            >
                                Export
                            </button>
                        </div>
                        
                        <!-- Delete Account -->
                        <div class="flex items-center justify-between p-4 bg-red-50 rounded-lg border border-red-200">
                            <div>
                                <h3 class="font-medium text-red-900">Delete Account</h3>
                                <p class="text-sm text-red-700 mt-1">Permanently delete your account and all data</p>
                            </div>
                            <button
                                @click="showDeleteAccountDialog = true"
                                class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors text-sm font-medium"
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Save Button -->
                <div class="flex justify-end">
                    <button
                        @click="saveSettings"
                        :disabled="isSavingSettings"
                        class="flex items-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors font-medium disabled:opacity-50"
                    >
                        <i class="pi pi-check"></i>
                        <span>{{ isSavingSettings ? 'Saving...' : 'Save All Settings' }}</span>
                    </button>
                </div>

            </div>
        </div>

        <!-- Export Data Dialog -->
        <Dialog 
            v-model:visible="showExportDataDialog"
            modal
            header="Export Your Data"
            :style="{ width: '90vw', maxWidth: '500px' }"
            :dismissableMask="true"
        >
            <div class="space-y-4">
                <p class="text-gray-700">
                    We'll prepare a copy of your data including:
                </p>
                <ul class="space-y-2 ml-4">
                    <li class="flex items-center gap-2 text-sm text-gray-600">
                        <i class="pi pi-check text-green-600"></i>
                        Profile information
                    </li>
                    <li class="flex items-center gap-2 text-sm text-gray-600">
                        <i class="pi pi-check text-green-600"></i>
                        Activities and assignments
                    </li>
                    <li class="flex items-center gap-2 text-sm text-gray-600">
                        <i class="pi pi-check text-green-600"></i>
                        Student submissions and scores
                    </li>
                    <li class="flex items-center gap-2 text-sm text-gray-600">
                        <i class="pi pi-check text-green-600"></i>
                        Remarks and feedback
                    </li>
                </ul>
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                    <p class="text-xs text-blue-800">
                        <i class="pi pi-info-circle mr-1"></i>
                        The export will be sent to your email address within 24 hours.
                    </p>
                </div>
            </div>
            
            <template #footer>
                <div class="flex justify-end gap-2">
                    <Button
                        label="Cancel"
                        @click="showExportDataDialog = false"
                        class="p-button-secondary"
                        style="background: #f3f4f6; border: 1px solid #d1d5db; color: #1f2937;"
                    />
                    <Button
                        :label="isExportingData ? 'Exporting...' : 'Export Data'"
                        @click="exportData"
                        :disabled="isExportingData"
                        style="background: linear-gradient(to right, #4f46e5, #6366f1); border: none;"
                    />
                </div>
            </template>
        </Dialog>

        <!-- Delete Account Dialog -->
        <Dialog 
            v-model:visible="showDeleteAccountDialog"
            modal
            header="Delete Account"
            :style="{ width: '90vw', maxWidth: '500px' }"
            :dismissableMask="true"
        >
            <div class="space-y-4">
                <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                    <div class="flex items-start gap-3">
                        <i class="pi pi-exclamation-triangle text-red-600 text-2xl"></i>
                        <div>
                            <h3 class="font-semibold text-red-900 mb-1">Warning: This action cannot be undone</h3>
                            <p class="text-sm text-red-700">
                                Deleting your account will permanently remove:
                            </p>
                        </div>
                    </div>
                </div>
                
                <ul class="space-y-2 ml-4">
                    <li class="flex items-center gap-2 text-sm text-gray-600">
                        <i class="pi pi-times text-red-600"></i>
                        Your profile and personal information
                    </li>
                    <li class="flex items-center gap-2 text-sm text-gray-600">
                        <i class="pi pi-times text-red-600"></i>
                        All your classes and activities
                    </li>
                    <li class="flex items-center gap-2 text-sm text-gray-600">
                        <i class="pi pi-times text-red-600"></i>
                        Student submissions and scores
                    </li>
                    <li class="flex items-center gap-2 text-sm text-gray-600">
                        <i class="pi pi-times text-red-600"></i>
                        All remarks and feedback
                    </li>
                </ul>
                
                <p class="text-sm text-gray-700 font-medium">
                    Are you absolutely sure you want to delete your account?
                </p>
            </div>
            
            <template #footer>
                <div class="flex justify-end gap-2">
                    <Button
                        label="Cancel"
                        @click="showDeleteAccountDialog = false"
                        style="background: #f3f4f6; border: 1px solid #d1d5db; color: #1f2937;"
                    />
                    <Button
                        label="Delete Account"
                        @click="deleteAccount"
                        style="background: linear-gradient(to right, #dc2626, #ef4444); border: none;"
                    />
                </div>
            </template>
        </Dialog>

    </div>
</template>

<style scoped>
/* Custom toggle switch styling is handled by Tailwind classes */
</style>
