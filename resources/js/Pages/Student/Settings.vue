<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from '../../composables/useToast';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

const { showSuccess, showError, showInfo, showWarning } = useToast();

// Settings data
const settings = ref({
    notifications: {
        emailNotifications: true,
        activityReminders: true,
        scoreNotifications: true,
        remarkNotifications: true
    },
    privacy: {
        profileVisibility: 'classmates',
        showScores: true
    },
    preferences: {
        language: 'en',
        theme: 'light'
    }
});

// Dialog states
const showExportDataDialog = ref(false);
const isExportingData = ref(false);
const isSavingSettings = ref(false);

// Language options
const languageOptions = [
    { value: 'en', label: 'English' },
    { value: 'fil', label: 'Filipino' },
    { value: 'es', label: 'Spanish' }
];

// Theme options
const themeOptions = [
    { value: 'light', label: 'Light', icon: 'pi-sun' },
    { value: 'dark', label: 'Dark', icon: 'pi-moon' },
    { value: 'auto', label: 'Auto', icon: 'pi-desktop' }
];

// Load settings
const loadSettings = async () => {
    try {
        const response = await axios.get('/api/user/settings/');
        settings.value = response.data;
        console.log('✅ Settings loaded:', settings.value);
    } catch (error) {
        console.error('❌ Error loading settings:', error);
        showError('Failed to load settings', 'Error');
    }
};

// Save settings
const saveSettings = async () => {
    try {
        isSavingSettings.value = true;
        
        const response = await axios.put('/api/user/settings/', settings.value);
        settings.value = response.data;
        
        showSuccess('Settings saved successfully!', 'Saved');
        console.log('✅ Settings saved:', settings.value);
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

// Load settings on mount
onMounted(() => {
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
                    <p class="text-white/80 text-sm mt-1">Manage your account preferences</p>
                </div>
                <button
                    @click="$emit('navigate', 'StudentNewsfeed')"
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
                            <h2 class="text-lg font-semibold text-gray-900">Notifications</h2>
                        </div>
                    </div>
                    
                    <div class="p-6 space-y-4">
                        <!-- Email Notifications -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Email Notifications</h3>
                                <p class="text-sm text-gray-600 mt-1">Receive updates via email</p>
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
                        
                        <!-- Activity Reminders -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Activity Reminders</h3>
                                <p class="text-sm text-gray-600 mt-1">Get reminded about due dates</p>
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
                        
                        <!-- Score Notifications -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Score Updates</h3>
                                <p class="text-sm text-gray-600 mt-1">Notified when work is scored</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input 
                                    type="checkbox" 
                                    v-model="settings.notifications.scoreNotifications"
                                    class="sr-only peer"
                                />
                                <div class="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                            </label>
                        </div>
                        
                        <!-- Teacher Remarks -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Teacher Remarks</h3>
                                <p class="text-sm text-gray-600 mt-1">New feedback from teachers</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input 
                                    type="checkbox" 
                                    v-model="settings.notifications.remarkNotifications"
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
                            <h2 class="text-lg font-semibold text-gray-900">Privacy</h2>
                        </div>
                    </div>
                    
                    <div class="p-6 space-y-4">
                        <!-- Profile Visibility -->
                        <div class="p-4 bg-gray-50 rounded-lg">
                            <h3 class="font-medium text-gray-900 mb-3">Who can see your profile</h3>
                            <select 
                                v-model="settings.privacy.profileVisibility"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            >
                                <option value="everyone">Everyone</option>
                                <option value="classmates">Classmates Only</option>
                                <option value="teachers">Teachers Only</option>
                                <option value="private">Private</option>
                            </select>
                        </div>
                        
                        <!-- Show Scores -->
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Show My Scores</h3>
                                <p class="text-sm text-gray-600 mt-1">Let classmates see your scores</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input 
                                    type="checkbox" 
                                    v-model="settings.privacy.showScores"
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

                <!-- Data Management -->
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
                                <p class="text-sm text-gray-600 mt-1">Download your learning data</p>
                            </div>
                            <button
                                @click="showExportDataDialog = true"
                                class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors text-sm font-medium"
                            >
                                Export
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
                        <span>{{ isSavingSettings ? 'Saving...' : 'Save Settings' }}</span>
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
                    We'll prepare your learning data including:
                </p>
                <ul class="space-y-2 ml-4">
                    <li class="flex items-center gap-2 text-sm text-gray-600">
                        <i class="pi pi-check text-green-600"></i>
                        Profile information
                    </li>
                    <li class="flex items-center gap-2 text-sm text-gray-600">
                        <i class="pi pi-check text-green-600"></i>
                        Activity submissions
                    </li>
                    <li class="flex items-center gap-2 text-sm text-gray-600">
                        <i class="pi pi-check text-green-600"></i>
                        Scores and progress
                    </li>
                    <li class="flex items-center gap-2 text-sm text-gray-600">
                        <i class="pi pi-check text-green-600"></i>
                        Teacher feedback
                    </li>
                </ul>
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                    <p class="text-xs text-blue-800">
                        <i class="pi pi-info-circle mr-1"></i>
                        Data will be sent to your email within 24 hours.
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
                        :label="isExportingData ? 'Exporting...' : 'Export'"
                        @click="exportData"
                        :disabled="isExportingData"
                        style="background: linear-gradient(to right, #4f46e5, #6366f1); border: none;"
                    />
                </div>
            </template>
        </Dialog>

    </div>
</template>

<style scoped>
/* Custom toggle switch styling handled by Tailwind */
</style>
