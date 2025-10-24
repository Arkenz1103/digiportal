<template>
    <div class="flex flex-col h-screen bg-gray-50">
        <!-- Header -->
        <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-4 md:p-6 shadow-lg">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl md:text-3xl font-bold text-white">Settings</h1>
                    <p class="text-white/90 mt-1 text-sm">Customize your preferences and app settings</p>
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
                
                <!-- Notification Settings -->
                <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
                    <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                        <i class="pi pi-bell text-indigo-600"></i>
                        Notification Settings
                    </h2>
                    
                    <div class="space-y-4">
                        <SettingToggle
                            v-model="settings.notifications.email"
                            title="Email Notifications"
                            description="Receive email updates about student submissions and activities"
                            @change="saveSettings"
                        />
                        <SettingToggle
                            v-model="settings.notifications.push"
                            title="Push Notifications"
                            description="Get instant notifications in the app"
                            @change="saveSettings"
                        />
                        <SettingToggle
                            v-model="settings.notifications.submissions"
                            title="Student Submission Alerts"
                            description="Notify when students submit their work"
                            @change="saveSettings"
                        />
                        <SettingToggle
                            v-model="settings.notifications.reminders"
                            title="Activity Reminders"
                            description="Remind about upcoming activity deadlines"
                            @change="saveSettings"
                        />
                    </div>
                </div>

                <!-- Display Preferences -->
                <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
                    <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                        <i class="pi pi-palette text-indigo-600"></i>
                        Display Preferences
                    </h2>
                    
                    <div class="space-y-4">
                        <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <label class="block font-semibold text-gray-800 mb-2">Theme</label>
                            <select 
                                v-model="settings.display.theme"
                                @change="saveSettings"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            >
                                <option value="light">Light</option>
                                <option value="dark">Dark</option>
                                <option value="auto">Auto (System)</option>
                            </select>
                        </div>

                        <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <label class="block font-semibold text-gray-800 mb-2">Language</label>
                            <select 
                                v-model="settings.display.language"
                                @change="saveSettings"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            >
                                <option value="en">English</option>
                                <option value="fil">Filipino</option>
                                <option value="es">Spanish</option>
                            </select>
                        </div>

                        <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <label class="block font-semibold text-gray-800 mb-2">Items Per Page</label>
                            <select 
                                v-model="settings.display.itemsPerPage"
                                @change="saveSettings"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            >
                                <option :value="10">10</option>
                                <option :value="25">25</option>
                                <option :value="50">50</option>
                                <option :value="100">100</option>
                            </select>
                        </div>

                        <SettingToggle
                            v-model="settings.display.compactView"
                            title="Compact View"
                            description="Show more content in less space"
                            @change="saveSettings"
                        />
                    </div>
                </div>

                <!-- Privacy & Security -->
                <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
                    <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                        <i class="pi pi-shield text-indigo-600"></i>
                        Privacy & Security
                    </h2>
                    
                    <div class="space-y-4">
                        <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <label class="block font-semibold text-gray-800 mb-2">Profile Visibility</label>
                            <select 
                                v-model="settings.privacy.profileVisibility"
                                @change="saveSettings"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            >
                                <option value="public">Public (All users)</option>
                                <option value="students">Students Only</option>
                                <option value="teachers">Teachers Only</option>
                                <option value="private">Private</option>
                            </select>
                        </div>

                        <SettingToggle
                            v-model="settings.privacy.showEmail"
                            title="Show Email Address"
                            description="Display your email on your profile"
                            @change="saveSettings"
                        />

                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <div class="flex-1">
                                <h3 class="font-semibold text-gray-800">Two-Factor Authentication</h3>
                                <p class="text-sm text-gray-600">Add an extra layer of security</p>
                            </div>
                            <button
                                @click="toggle2FA"
                                class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors duration-200"
                            >
                                {{ settings.privacy.twoFactorEnabled ? 'Enabled' : 'Enable' }}
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Grading Preferences -->
                <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
                    <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                        <i class="pi pi-star text-indigo-600"></i>
                        Grading Preferences
                    </h2>
                    
                    <div class="space-y-4">
                        <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <label class="block font-semibold text-gray-800 mb-2">Default Grading Scale</label>
                            <select 
                                v-model="settings.grading.scale"
                                @change="saveSettings"
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            >
                                <option value="100">100 Points</option>
                                <option value="letter">Letter Grade (A-F)</option>
                                <option value="percentage">Percentage (%)</option>
                            </select>
                        </div>

                        <SettingToggle
                            v-model="settings.grading.autoSave"
                            title="Auto-Save Grades"
                            description="Automatically save grades as you enter them"
                            @change="saveSettings"
                        />

                        <SettingToggle
                            v-model="settings.grading.showFeedback"
                            title="Show Feedback to Students"
                            description="Students can see your feedback immediately"
                            @change="saveSettings"
                        />
                    </div>
                </div>

                <!-- Data Management -->
                <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
                    <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                        <i class="pi pi-database text-indigo-600"></i>
                        Data Management
                    </h2>
                    
                    <div class="space-y-4">
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <div class="flex-1">
                                <h3 class="font-semibold text-gray-800">Export Your Data</h3>
                                <p class="text-sm text-gray-600">Download all your data in CSV format</p>
                            </div>
                            <button
                                @click="exportData"
                                class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200 flex items-center gap-2"
                            >
                                <i class="pi pi-download"></i>
                                Export
                            </button>
                        </div>

                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
                            <div class="flex-1">
                                <h3 class="font-semibold text-gray-800">Clear Cache</h3>
                                <p class="text-sm text-gray-600">Clear temporary data to improve performance</p>
                            </div>
                            <button
                                @click="clearCache"
                                class="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors duration-200"
                            >
                                Clear
                            </button>
                        </div>

                        <div class="flex items-center justify-between p-4 bg-red-50 rounded-lg border border-red-200">
                            <div class="flex-1">
                                <h3 class="font-semibold text-red-800">Reset All Settings</h3>
                                <p class="text-sm text-red-600">Restore default settings (cannot be undone)</p>
                            </div>
                            <button
                                @click="resetAllSettings"
                                class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-200"
                            >
                                Reset
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useToast } from '@/Composables/useToast';

const emit = defineEmits(['navigate']);
const { showSuccess, showError, showInfo } = useToast();

const settings = reactive({
    notifications: { email: true, push: true, submissions: true, reminders: true },
    display: { theme: 'light', language: 'en', itemsPerPage: 25, compactView: false },
    privacy: { profileVisibility: 'students', showEmail: false, twoFactorEnabled: false },
    grading: { scale: '100', autoSave: true, showFeedback: true }
});

const SettingToggle = {
    props: ['modelValue', 'title', 'description'],
    emits: ['update:modelValue', 'change'],
    template: `
        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
            <div class="flex-1">
                <h3 class="font-semibold text-gray-800">{{ title }}</h3>
                <p class="text-sm text-gray-600">{{ description }}</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
                <input 
                    type="checkbox" 
                    :checked="modelValue"
                    @change="$emit('update:modelValue', $event.target.checked); $emit('change')"
                    class="sr-only peer"
                >
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
            </label>
        </div>
    `
};

onMounted(() => {
    const saved = localStorage.getItem('digiportal_teacher_settings');
    if (saved) Object.assign(settings, JSON.parse(saved));
});

const saveSettings = () => {
    localStorage.setItem('digiportal_teacher_settings', JSON.stringify(settings));
    showSuccess('Settings saved successfully!', 'Settings Updated');
};

const goBackToHome = () => emit('navigate', 'TeacherHome');

const toggle2FA = () => {
    settings.privacy.twoFactorEnabled = !settings.privacy.twoFactorEnabled;
    saveSettings();
    showSuccess(settings.privacy.twoFactorEnabled ? '2FA enabled!' : '2FA disabled!', '2FA Updated');
};

const exportData = () => showInfo('Data export feature coming soon!', 'Export Data');
const clearCache = () => { localStorage.clear(); showSuccess('Cache cleared!', 'Cache Cleared'); };
const resetAllSettings = () => {
    if (confirm('Reset all settings to default?')) {
        Object.assign(settings, {
            notifications: { email: true, push: true, submissions: true, reminders: true },
            display: { theme: 'light', language: 'en', itemsPerPage: 25, compactView: false },
            privacy: { profileVisibility: 'students', showEmail: false, twoFactorEnabled: false },
            grading: { scale: '100', autoSave: true, showFeedback: true }
        });
        saveSettings();
    }
};
</script>

<style scoped>
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #f1f1f1; }
::-webkit-scrollbar-thumb { background: #888; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #555; }
</style>
