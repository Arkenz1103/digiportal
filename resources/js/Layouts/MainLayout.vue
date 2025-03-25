<script setup>
import { Link, usePage, useForm } from '@inertiajs/vue3';
import { ref, computed, onMounted } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';

// Get user from shared data
const page = usePage();
const auth = computed(() => page.props.auth);
const currentRoute = computed(() => page.url); // Get the current route

// Sidebar collapse state
const isCollapsed = ref(false);

// Profile dropdown state
const isDropdownOpen = ref(false);

// State for class dropdown
const isClassDropdownOpen = ref(false);

// Add state for classes
const classes = ref([
    { id: 1, name: 'Grade 1 - A', theme: 'emerald' },
    { id: 2, name: 'Grade 2 - A', theme: 'blue' },
    { id: 3, name: 'Grade 3 - A', theme: 'purple' },
]);

// Add new state for the modal and form
const showAddClassModal = ref(false);
const newClassForm = useForm({
    grade: '',
    section: '',
    theme: 'emerald', // default theme
});

// Add these to your script setup section at the top
const showNotifications = ref(false);
const notifications = ref([
    {
        id: 1,
        type: 'output',
        title: 'New Student Output',
        message: 'Alice Smith has submitted "Math Exercise 3"',
        date: new Date(),
        isNew: true,
        isUnread: true,
    },
    {
        id: 2,
        type: 'remark',
        title: 'New Remark Added',
        message: 'You added a behavioral remark for Bob Johnson',
        date: new Date('2024-02-18 14:30'),
        isNew: true,
        isUnread: true,
    },
    {
        id: 3,
        type: 'schedule',
        title: 'Schedule Change',
        message: 'Class schedule for Grade 2 - Section A updated',
        date: new Date('2024-02-18 09:15'),
        isNew: true,
        isUnread: false,
    },
]);

// Add these helper functions
const getNotificationIcon = (type) => {
    switch (type) {
        case 'output': return 'pi-file-edit';
        case 'remark': return 'pi-comments';
        case 'schedule': return 'pi-calendar';
        default: return 'pi-bell';
    }
};

const getNotificationColor = (type) => {
    switch (type) {
        case 'output': return 'text-blue-600 bg-blue-50';
        case 'remark': return 'text-purple-600 bg-purple-50';
        case 'schedule': return 'text-green-600 bg-green-50';
        default: return 'text-gray-600 bg-gray-50';
    }
};

const formatDate = (date) => {
    return new Intl.DateTimeFormat('en-US', {
        hour: 'numeric',
        minute: 'numeric',
    }).format(new Date(date));
};

// Function to mark notification as read
const markAsRead = (id) => {
    const notification = notifications.value.find(n => n.id === id);
    if (notification) {
        notification.isUnread = false;
        notification.isNew = false;
    }
};

// Toggle sidebar visibility
const toggleSidebar = () => {
    isCollapsed.value = !isCollapsed.value;
};

// Toggle profile dropdown
const toggleDropdown = () => {
    isDropdownOpen.value = !isDropdownOpen.value;
};

// Toggle class dropdown
const toggleClassDropdown = () => {
    isClassDropdownOpen.value = !isClassDropdownOpen.value;
};

// Sidebar menu items
const sideBarItems = computed(() => {
    if (!auth.value?.user) {
        return [];
    }

    const roleBasedItems = {
        teacher: [
            { label: 'Home', icon: 'pi pi-home', route: route('teacher.home') },
            { label: 'Remarks', icon: 'pi pi-comments', route: route('teacher.remarks') },
            { label: 'Archived', icon: 'pi pi-folder', route: route('teacher.archived') },
        ],
        student: [
            { label: 'Home', icon: 'pi pi-home', route: route('student.newsfeed') },
            { label: 'Sketch', icon: 'pi pi-pencil', route: route('student.sketch') },
            { label: 'Archived', icon: 'pi pi-folder', route: route('student.archived') },
        ],
    };

    // Return the appropriate items based on user role
    return roleBasedItems[auth.value.user.role] || [];
});

// Logout Function using Inertia
const logoutForm = useForm({});
const logout = () => {
    logoutForm.post(route('logout'));
};

// Add theme options
const themeOptions = [
    { id: 'emerald', color: 'bg-emerald-500', name: 'Emerald' },
    { id: 'blue', color: 'bg-blue-500', name: 'Blue' },
    { id: 'purple', color: 'bg-purple-500', name: 'Purple' },
    { id: 'rose', color: 'bg-rose-500', name: 'Rose' },
    { id: 'amber', color: 'bg-amber-500', name: 'Amber' },
    { id: 'teal', color: 'bg-teal-500', name: 'Teal' },
];

// Function to handle class creation
const addClass = () => {
    if (!newClassForm.grade || !newClassForm.section) {
        return;
    }

    const className = `Grade ${newClassForm.grade} - ${newClassForm.section.toUpperCase()}`;
    
    classes.value.push({
        id: classes.value.length + 1,
        name: className,
        theme: newClassForm.theme,
    });

    newClassForm.reset();
    showAddClassModal.value = false;
};

// Function to validate grade input
const validateGrade = (event) => {
    // Only allow numbers
    const value = event.target.value;
    if (!/^\d*$/.test(value)) {
        event.target.value = value.replace(/[^\d]/g, '');
    }
};

// Function to validate section input
const validateSection = (event) => {
    // Only allow single letters
    const value = event.target.value;
    if (!/^[a-zA-Z]?$/.test(value)) {
        event.target.value = value.slice(0, 1).toUpperCase();
    }
};

// Add new state for join class modal and form
const showJoinClassModal = ref(false);
const joinClassForm = useForm({
    code: '',
});

// Add this function to handle joining a class
const joinClass = () => {
    if (!joinClassForm.code) {
        return;
    }
    
    // Here you would typically make an API call to join the class
    // For now, we'll just close the modal
    joinClassForm.reset();
    showJoinClassModal.value = false;
};
</script>

<template>
    <div class="bg-gray-100">
        <div class="flex">
            <!-- Sidebar -->
            <div :class="['h-screen bg-white shadow-lg sticky top-0 flex flex-col transition-all duration-300', isCollapsed ? 'w-16' : 'w-48']">
                <!-- Sidebar Header -->
                <div class="p-2 border-b h-[52px] flex items-center">
                    <button @click="toggleSidebar" class="p-2 px-4 focus:outline-none">
                        <i class="pi pi-bars text-xl"></i>
                    </button>
                </div>

                <!-- Navigation Section -->
                <nav class="flex-1 overflow-y-auto mt-4">
                    <!-- Regular menu items -->
                    <div v-for="(item, index) in sideBarItems" :key="index" class="px-4 py-2">
                        <Link :href="item.route"
                            class="flex items-center p-2 rounded-lg transition-colors duration-200"
                            :class="{
                                'bg-blue-50 text-blue-600 font-semibold': currentRoute === item.route,
                                'text-gray-700 hover:bg-blue-50 hover:text-blue-600': currentRoute !== item.route
                            }">
                            <i :class="item.icon" class="text-lg"></i>
                            <span v-show="!isCollapsed" class="ml-3 text-[0.875rem] font-medium">{{ item.label }}</span>
                        </Link>
                    </div>

                    <!-- Horizontal Line -->
                    <div class="px-4 py-2">
                        <hr class="border-gray-200">
                    </div>

                    <!-- My Classes Section -->
                    <div class="px-4 py-2" v-if="auth?.user?.role === 'teacher' || auth?.user?.role === 'student'">
                        <div class="flex items-center justify-between p-2">
                            <div class="flex items-center">
                                <span v-show="!isCollapsed" class="text-[0.875rem] font-medium">My Classes</span>
                            </div>
                            <button 
                                v-if="auth?.user?.role === 'teacher'"
                                @click="showAddClassModal = true" 
                                class="text-blue-600 hover:bg-blue-50 rounded-lg p-1 transition-all duration-200"
                            >
                                <i class="pi pi-plus text-sm"></i>
                            </button>
                        </div>

                        <!-- Classes List -->
                        <div class="ml-2 mt-2 space-y-1">
                            <Link v-for="class_ in classes" 
                                  :key="class_.id"
                                  :href="route(auth?.user?.role + '.class.show', class_.name.toLowerCase().replace(' - ', '-'))"
                                  class="flex items-center p-2 rounded-lg transition-all duration-200"
                                  :class="{
                                      'hover:bg-blue-50 hover:text-blue-600': true,
                                      'bg-blue-50 text-blue-600': currentRoute === route(auth?.user?.role + '.class.show', class_.name.toLowerCase().replace(' - ', '-'))
                                  }"
                                  :title="class_.name">
                                <div v-if="!isCollapsed" 
                                     class="flex items-center gap-3">
                                    <div :class="[
                                        'w-7 h-7 rounded-lg flex items-center justify-center text-white shadow-sm',
                                        `bg-${class_.theme}-500`
                                    ]">
                                        <span class="text-xs font-semibold">{{ class_.name.split(' ')[1] }}</span>
                                    </div>
                                    <span class="text-sm font-medium">{{ class_.name }}</span>
                                </div>
                                <div v-else 
                                     :class="[
                                         'w-7 h-7 rounded-lg flex items-center justify-center text-white shadow-sm',
                                         `bg-${class_.theme}-500`
                                     ]"
                                     :title="class_.name">
                                    <span class="text-xs font-semibold">{{ class_.name.split(' ')[1] }}</span>
                                </div>
                            </Link>
                        </div>

                        <!-- Join Class Button -->
                        <div class="px-4 py-2" v-if="auth?.user?.role === 'student'">
                            <button 
                                @click="showJoinClassModal = true"
                                class="w-full flex items-center justify-center gap-2 p-2 text-gray-700 hover:bg-gray-50 rounded-lg transition-all duration-200 border border-gray-300"
                            >
                                <i class="pi pi-plus text-sm"></i>
                                <span v-show="!isCollapsed" class="text-sm font-medium">Join Class</span>
                            </button>
                        </div>
                    </div>
                </nav>
            </div>

            <!-- Main Content Area -->
            <div class="flex-1">
                <nav class="bg-white shadow-md sticky top-0 border-b h-[52px]">
                    <div class="max-w-full mx-auto h-full">
                        <div class="flex justify-between items-center pl-2 h-full">
                            <!-- Logo -->
                            <div class="flex items-center">
                                <button @click="toggleSidebar" class="p-2 focus:outline-none md:hidden">
                                    <i class="pi pi-bars text-xl"></i>
                                </button>
                                <img
                                    src="C:\Users\ncslogo.jpg"
                                    class="w-auto h-8 mr-2"
                                />
                                <span class="text-xl font-bold">DigiPort</span>
                            </div>

                            <!-- Add Bell and User Profile -->
                            <div class="flex items-center gap-6 pr-6">
                                <!-- Bell Icon with Dropdown -->
                                <div class="relative">
                                    <button 
                                        @click="showNotifications = !showNotifications" 
                                        @blur="setTimeout(() => showNotifications = false, 200)"
                                        class="relative p-2 hover:bg-gray-100 rounded-full transition-all duration-200 focus:outline-none"
                                    >
                                        <i class="pi pi-bell text-gray-600 text-xl"></i>
                                        <!-- Notification Badge -->
                                        <div 
                                            v-if="notifications.filter(n => n.isUnread).length > 0"
                                            class="absolute -top-1 -right-1 bg-red-500 text-white text-xs w-5 h-5 flex items-center justify-center rounded-full"
                                        >
                                            {{ notifications.filter(n => n.isUnread).length }}
                                        </div>
                                    </button>

                                    <!-- Notifications Dropdown -->
                                    <div 
                                        v-show="showNotifications"
                                        class="absolute right-0 mt-2 w-96 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden z-50"
                                    >
                                        <!-- Header -->
                                        <div class="px-4 py-3 border-b border-gray-100 bg-gray-50">
                                            <div class="flex items-center justify-between">
                                                <h3 class="font-semibold text-gray-900">Notifications</h3>
                                                <Link 
                                                    :href="route('teacher.notify')"
                                                    class="text-sm text-blue-600 hover:text-blue-700 font-medium"
                                                >
                                                    View All
                                                </Link>
                                            </div>
                                        </div>

                                        <!-- Notifications List -->
                                        <div class="max-h-[400px] overflow-y-auto">
                                            <div 
                                                v-for="notification in notifications.slice(0, 5)" 
                                                :key="notification.id"
                                                @click="markAsRead(notification.id)"
                                                class="group px-4 py-3 hover:bg-gray-50 transition-colors cursor-pointer border-b border-gray-100 last:border-0"
                                                :class="{ 'bg-blue-50/60': notification.isUnread }"
                                            >
                                                <div class="flex items-start gap-3">
                                                    <!-- Icon -->
                                                    <div 
                                                        class="p-2 rounded-full shrink-0"
                                                        :class="getNotificationColor(notification.type)"
                                                    >
                                                        <i :class="['pi', getNotificationIcon(notification.type)]"></i>
                                                    </div>
                                                    
                                                    <!-- Content -->
                                                    <div class="flex-1 min-w-0">
                                                        <div class="flex items-center gap-2 mb-1">
                                                            <p class="font-medium text-sm text-gray-900 truncate">
                                                                {{ notification.title }}
                                                            </p>
                                                            <span 
                                                                v-if="notification.isNew"
                                                                class="px-1.5 py-0.5 bg-green-100 text-green-700 text-xs rounded-full font-medium"
                                                            >
                                                                New
                                                            </span>
                                                        </div>
                                                        <p class="text-sm text-gray-600 line-clamp-2 mb-1">
                                                            {{ notification.message }}
                                                        </p>
                                                        <p class="text-xs text-gray-500">
                                                            {{ formatDate(notification.date) }}
                                                        </p>
                                                    </div>
                                                    
                                                    <!-- Unread Indicator -->
                                                    <div v-if="notification.isUnread" 
                                                        class="w-2 h-2 rounded-full bg-blue-600 shrink-0 mt-2">
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Empty State -->
                                            <div 
                                                v-if="notifications.length === 0"
                                                class="px-4 py-8 text-center"
                                            >
                                                <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gray-100 mb-3">
                                                    <i class="pi pi-bell text-gray-500 text-xl"></i>
                                                </div>
                                                <p class="text-gray-500 font-medium">No notifications yet</p>
                                                <p class="text-gray-400 text-sm">We'll notify you when something arrives</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- User Profile -->
                                <div class="relative">
                                    <button 
                                        @click="toggleDropdown"
                                        @blur="setTimeout(() => isDropdownOpen = false, 200)"
                                        class="flex items-center gap-3 hover:bg-gray-100 rounded-full py-1.5 px-2 transition-all duration-200"
                                    >
                                        <img 
                                            :src="auth?.user?.avatar || 'https://ui-avatars.com/api/?name=' + auth?.user?.name" 
                                            class="w-8 h-8 rounded-full object-cover border-2 border-white shadow-sm"
                                            :alt="auth?.user?.name"
                                        />
                                        <div class="hidden md:block text-left">
                                            <p class="text-sm font-medium text-gray-700 line-clamp-1">
                                                {{ auth?.user?.name }}
                                            </p>
                                            <p class="text-xs text-gray-500 line-clamp-1">
                                                {{ auth?.user?.role.charAt(0).toUpperCase() + auth?.user?.role.slice(1) }}
                                            </p>
                                        </div>
                                        <i class="pi pi-chevron-down text-gray-500 text-xs hidden md:block"></i>
                                    </button>

                                    <!-- Dropdown Menu -->
                                    <div 
                                        v-show="isDropdownOpen" 
                                        class="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-xl border border-gray-100 py-1 z-50"
                                    >
                                        <!-- User Info -->
                                        <div class="px-4 py-3 border-b border-gray-100">
                                            <p class="text-sm font-medium text-gray-900">{{ auth?.user?.name }}</p>
                                            <p class="text-xs text-gray-500">{{ auth?.user?.email }}</p>
                                        </div>
                                        
                                        <!-- Menu Items -->
                                        <div class="py-1">
                                            <Link 
                                                href="#" 
                                                class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                                            >
                                                <i class="pi pi-user text-gray-400"></i>
                                                Profile
                                            </Link>
                                            <Link 
                                                href="#" 
                                                class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                                            >
                                                <i class="pi pi-cog text-gray-400"></i>
                                                Settings
                                            </Link>
                                        </div>
                                        
                                        <!-- Logout -->
                                        <div class="border-t border-gray-100 py-1">
                                            <button 
                                                @click="logout" 
                                                class="flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 w-full text-left"
                                            >
                                                <i class="pi pi-power-off text-red-500"></i>
                                                Logout
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </nav>

                <!-- Page Content -->
                <main class="p-6">
                    <slot></slot>
                </main>
            </div>
        </div>
    </div>

    <!-- Add Class Modal -->
    <Dialog 
        v-model:visible="showAddClassModal" 
        modal 
        header="Add New Class" 
        :style="{ width: '30vw' }"
        :dismissableMask="true"
    >
        <div class="flex flex-col gap-4 p-4">
            <div class="flex flex-col gap-2">
                <label class="text-sm font-medium">Grade</label>
                <InputText 
                    v-model="newClassForm.grade"
                    placeholder="Enter grade number (1-12)"
                    @input="validateGrade"
                    class="p-2"
                />
            </div>
            
            <div class="flex flex-col gap-2">
                <label class="text-sm font-medium">Section</label>
                <InputText 
                    v-model="newClassForm.section"
                    placeholder="Enter section letter (A-Z)"
                    @input="validateSection"
                    class="p-2"
                />
            </div>

            <!-- Add Theme Selection -->
            <div class="flex flex-col gap-2">
                <label class="text-sm font-medium">Theme Color</label>
                <div class="grid grid-cols-3 gap-2">
                    <button
                        v-for="theme in themeOptions"
                        :key="theme.id"
                        @click="newClassForm.theme = theme.id"
                        :class="[
                            'p-2 rounded-lg border-2 flex items-center gap-2',
                            newClassForm.theme === theme.id ? 'border-blue-500' : 'border-transparent'
                        ]"
                    >
                        <div :class="[
                            'w-4 h-4 rounded-full',
                            theme.color
                        ]"></div>
                        <span class="text-sm">{{ theme.name }}</span>
                    </button>
                </div>
            </div>
        </div>

        <template #footer>
            <div class="flex justify-end gap-2">
                <Button 
                    label="Cancel" 
                    @click="showAddClassModal = false"
                    class="p-button-text" 
                />
                <Button 
                    label="Add Class" 
                    @click="addClass"
                    :disabled="!newClassForm.grade || !newClassForm.section"
                />
            </div>
        </template>
    </Dialog>

    <!-- Join Class Modal -->
    <Dialog 
        v-model:visible="showJoinClassModal" 
        modal 
        header="Join Class" 
        :style="{ width: '30vw' }"
        :dismissableMask="true"
    >
        <div class="flex flex-col gap-4 p-4">
            <div class="flex flex-col gap-2">
                <label class="text-sm font-medium">Class Code</label>
                <InputText 
                    v-model="joinClassForm.code"
                    placeholder="Enter class code"
                    class="p-2"
                />
                <p class="text-xs text-gray-500">
                    Ask your teacher for the class code
                </p>
            </div>
        </div>

        <template #footer>
            <div class="flex justify-end gap-2">
                <Button 
                    label="Cancel" 
                    @click="showJoinClassModal = false"
                    class="p-button-text" 
                />
                <Button 
                    label="Join Class" 
                    @click="joinClass"
                    :disabled="!joinClassForm.code"
                />
            </div>
        </template>
    </Dialog>
</template>

<style scoped>
/* Add these styles for the modal */
:deep(.p-dialog-header) {
    padding: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
}

:deep(.p-dialog-footer) {
    padding: 1.5rem;
    border-top: 1px solid #e5e7eb;
}

:deep(.p-dialog-content) {
    padding: 0;
}

:deep(.p-inputtext) {
    width: 100%;
}

/* Add styles for theme selection */
.theme-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
}

.theme-option {
    display: flex;
    align-items: center;
    padding: 0.5rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.2s;
}

.theme-option:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

.theme-color {
    width: 1rem;
    height: 1rem;
    border-radius: 9999px;
    margin-right: 0.5rem;
}

/* Add to existing styles */
.line-clamp-1 {
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Smooth dropdown animations */
.dropdown-enter-active,
.dropdown-leave-active {
    transition: all 0.2s;
}

.dropdown-enter-from,
.dropdown-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

/* Smooth transitions for class items */
.transition-all {
    transition-property: all;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 200ms;
}

/* Shadow for class indicators */
.shadow-sm {
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

/* Hover effect for class indicators */
.hover\:shadow-md:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style>
