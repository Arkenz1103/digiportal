<script setup>
import { ref, computed, onMounted, onUnmounted, provide, watch } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';

// Define emits for navigation
const emit = defineEmits(['navigate']);

// Use a runtime URL so Vite doesn't transform it to an import
const logoUrl = '/logo.jpg';

// Sidebar collapse state
const isCollapsed = ref(false);
provide('isSidebarCollapsed', isCollapsed);

// Profile dropdown state
const isDropdownOpen = ref(false);

// State for class dropdown
const isClassDropdownOpen = ref(false);

// Add state for classes
const classes = ref([
    { id: 1, name: 'Grade 1 - A', theme: 'purple' }
]);

// Add new state for the modal and form
const showAddClassModal = ref(false);
const newClassForm = ref({
    grade: '',
    section: '',
    theme: 'purple',
});

// Notifications state
const showNotifications = ref(false);
const notifications = ref([]);
const unreadCount = ref(0);

// Load notifications from backend
const loadNotifications = async () => {
    try {
        const response = await fetch('/api/notifications/', {
            credentials: 'include', // Include cookies for authentication
            headers: {
                'Accept': 'application/json',
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            notifications.value = data.map(notif => ({
                id: notif.id,
                type: notif.notification_type,
                title: notif.title,
                message: notif.message,
                date: new Date(notif.created_at),
                isNew: !notif.is_read,
                isUnread: !notif.is_read,
            }));
            unreadCount.value = notifications.value.filter(n => n.isUnread).length;
            console.log('✅ Loaded notifications:', notifications.value.length, 'notifications');
            console.log('Unread count:', unreadCount.value);
        } else {
            const errorData = await response.json();
            console.error('❌ Failed to load notifications:', response.status, errorData);
        }
    } catch (error) {
        console.error('❌ Error loading notifications:', error);
    }
};

// Helper functions
const getNotificationIcon = (type) => {
    // Map notification types to icons
    const iconMap = {
        'portfolio_created': 'pi-folder-open',
        'portfolio_updated': 'pi-folder',
        'portfolio_deleted': 'pi-trash',
        'activity_created': 'pi-plus-circle',
        'activity_updated': 'pi-pencil',
        'activity_deleted': 'pi-times-circle',
        'submission_approved': 'pi-check-circle',
        'submission_rejected': 'pi-times-circle',
        'score_added': 'pi-star',
        'submission_received': 'pi-file-edit',
        'approval_requested': 'pi-question-circle',
    };
    return iconMap[type] || 'pi-bell';
};

const getNotificationColor = (type) => {
    const colorMap = {
        'portfolio_created': 'text-green-600 bg-green-50',
        'portfolio_updated': 'text-blue-600 bg-blue-50',
        'portfolio_deleted': 'text-red-600 bg-red-50',
        'activity_created': 'text-indigo-600 bg-indigo-50',
        'activity_updated': 'text-blue-600 bg-blue-50',
        'activity_deleted': 'text-red-600 bg-red-50',
        'submission_approved': 'text-green-600 bg-green-50',
        'submission_rejected': 'text-red-600 bg-red-50',
        'score_added': 'text-yellow-600 bg-yellow-50',
        'submission_received': 'text-indigo-600 bg-indigo-50',
        'approval_requested': 'text-violet-600 bg-violet-50',
    };
    return colorMap[type] || 'text-indigo-600 bg-indigo-50';
};

const formatDate = (date) => {
    return new Intl.DateTimeFormat('en-US', {
        hour: 'numeric',
        minute: 'numeric',
    }).format(new Date(date));
};

const markAsRead = async (id) => {
    try {
        const response = await fetch('/api/notifications/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ notification_id: id })
        });
        
        if (response.ok) {
            const notification = notifications.value.find(n => n.id === id);
            if (notification) {
                notification.isUnread = false;
                notification.isNew = false;
            }
            unreadCount.value = notifications.value.filter(n => n.isUnread).length;
        }
    } catch (error) {
        console.error('Error marking notification as read:', error);
    }
};


const toggleSidebar = () => {
    isCollapsed.value = !isCollapsed.value;
};

const toggleDropdown = () => {
    isDropdownOpen.value = !isDropdownOpen.value;
};

const toggleClassDropdown = () => {
    isClassDropdownOpen.value = !isClassDropdownOpen.value;
};

// User data loaded from localStorage
const currentUser = ref({
    name: 'User Name',
    email: 'user@example.com',
    role: 'student', // Default to student
    avatar: null
});

// Load user data from localStorage
const loadUserData = () => {
    const savedRole = localStorage.getItem('digiportal_user_role');
    const savedEmail = localStorage.getItem('digiportal_user_email');
    const savedName = localStorage.getItem('digiportal_user_name');
    const savedPage = localStorage.getItem('digiportal_current_page');
    
    if (savedRole) {
        currentUser.value.role = savedRole;
    }
    if (savedEmail) {
        currentUser.value.email = savedEmail;
    }
    if (savedName) {
        currentUser.value.name = savedName;
    } else {
        // Fallback names based on role
        if (savedRole === 'teacher') {
            currentUser.value.name = 'Teacher Name';
        } else {
            currentUser.value.name = 'Student Name';
        }
    }
    
    // Restore current page from localStorage
    if (savedPage) {
        currentRoute.value = savedPage;
    } else {
        // Set default page based on role
        if (savedRole === 'teacher') {
            currentRoute.value = 'TeacherHome';
        } else {
            currentRoute.value = 'StudentNewsfeed';
        }
    }
};

// Current page tracking - default based on role
const currentRoute = ref('StudentNewsfeed'); // Default to student, will be updated by loadUserData

// Sidebar menu items
const sideBarItems = computed(() => {
    const roleBasedItems = {
        teacher: [
            { label: 'Home', icon: 'pi pi-home', route: 'TeacherHome' },
            { label: 'Remarks', icon: 'pi pi-comments', route: 'TeacherRemarks' },
            { label: 'Notice', icon: 'pi pi-check-circle', route: 'TeacherNotice' },
            { label: 'Archived', icon: 'pi pi-folder', route: 'TeacherArchived' },
        ],
        student: [
            { label: 'Home', icon: 'pi pi-home', route: 'StudentNewsfeed' },
            { label: 'Sketch', icon: 'pi pi-pencil', route: 'StudentSketch' },
            { label: 'Archived', icon: 'pi pi-folder', route: 'StudentArchived' },
        ],
    };

    return roleBasedItems[currentUser.value.role] || [];
});

// Logout Function
const logout = () => {
    // Clear session storage
    localStorage.removeItem('digiportal_logged_in');
    localStorage.removeItem('digiportal_user_role');
    localStorage.removeItem('digiportal_current_page');
    
    // Navigate to landing page
    emit('navigate', 'Landing');
};

// Theme options
const themeOptions = [
    { id: 'indigo', color: 'bg-indigo-600', name: 'Indigo' },
    { id: 'violet', color: 'bg-violet-600', name: 'Violet' },
    { id: 'blue', color: 'bg-blue-600', name: 'Blue' }
];

// Function to handle class creation
const addClass = () => {
    if (!newClassForm.value.grade || !newClassForm.value.section) {
        return;
    }

    const className = `Grade ${newClassForm.value.grade} - ${newClassForm.value.section.toUpperCase()}`;

    classes.value.push({
        id: classes.value.length + 1,
        name: className,
        theme: newClassForm.value.theme,
    });

    // Reset form
    newClassForm.value = {
        grade: '',
        section: '',
        theme: 'purple',
    };
    showAddClassModal.value = false;
};

// Validation functions
const validateGrade = (event) => {
    const value = event.target.value;
    if (!/^\d*$/.test(value)) {
        event.target.value = value.replace(/[^\d]/g, '');
    }
};

const validateSection = (event) => {
    const value = event.target.value;
    if (!/^[a-zA-Z]?$/.test(value)) {
        event.target.value = value.slice(0, 1).toUpperCase();
    }
};

// Join class modal and form
const showJoinClassModal = ref(false);
const joinClassForm = ref({
    code: '',
});

const joinClass = () => {
    if (!joinClassForm.value.code) {
        return;
    }

    // Reset form
    joinClassForm.value = {
        code: '',
    };
    showJoinClassModal.value = false;
};

// Function to get class color based on theme
const getClassColor = (theme) => {
    switch (theme) {
        case 'indigo': return 'bg-indigo-600';
        case 'violet': return 'bg-violet-600';
        case 'blue': return 'bg-blue-600';
        default: return 'bg-indigo-600';
    }
};

// Check if a route is active
const isRouteActive = (routePath) => {
    return currentRoute.value === routePath;
};

// Navigation function
const navigateToPage = (page) => {
    currentRoute.value = page;
    // Save current page to localStorage so it persists on refresh
    localStorage.setItem('digiportal_current_page', page);
    emit('navigate', page);
};

// Navigate to class room
const navigateToClass = (class_) => {
    // Store selected class information
    localStorage.setItem('digiportal_selected_class', JSON.stringify(class_));
    
    // Navigate to room based on user role
    if (currentUser.value.role === 'teacher') {
        navigateToPage('TeacherRoom');
    } else if (currentUser.value.role === 'student') {
        navigateToPage('StudentRoom');
    }
};

// Navigate to notifications
const navigateToNotifications = () => {
    if (currentUser.value.role === 'teacher') {
        navigateToPage('TeacherNotify');
    } else {
        navigateToPage('StudentNotify');
    }
    showNotifications.value = false;
};

// Close dropdowns when clicking outside
const closeDropdowns = () => {
    isDropdownOpen.value = false;
    showNotifications.value = false;
};

// Listen for storage changes (when user logs in/out in another tab or page refreshes)
const handleStorageChange = (e) => {
    if (e.key === 'digiportal_user_role' || e.key === 'digiportal_user_email' || e.key === 'digiportal_user_name') {
        loadUserData();
        console.log('User data refreshed from storage change');
    }
};

// Custom event listener for same-tab localStorage changes
const handleUserDataChange = () => {
    loadUserData();
    console.log('User data refreshed from custom event');
};

onMounted(() => {
    document.addEventListener('click', closeDropdowns);
    loadUserData(); // Load user data when component mounts
    loadNotifications(); // Load notifications
    
    // Listen for storage changes from other tabs
    window.addEventListener('storage', handleStorageChange);
    
    // Listen for custom event for same-tab changes
    window.addEventListener('userDataChanged', handleUserDataChange);
    
    // Refresh notifications every 30 seconds
    setInterval(loadNotifications, 30000);
    
    // Debug: Log user data
    console.log('MainLayout mounted, user data:', currentUser.value);
});

onUnmounted(() => {
    document.removeEventListener('click', closeDropdowns);
    window.removeEventListener('storage', handleStorageChange);
    window.removeEventListener('userDataChanged', handleUserDataChange);
});

// Computed auth for template compatibility
const auth = computed(() => ({
    user: currentUser.value
}));
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-violet-50 to-blue-50">
        <div class="flex">
            <!-- Sidebar -->
            <div :class="['bg-white/90 backdrop-blur-sm shadow-lg sticky top-0 flex flex-col transition-all duration-300 border-r border-indigo-100 z-10', isCollapsed ? 'w-20' : 'w-64']">
                <!-- Sidebar Header -->
                <div class="p-4 border-b h-[52px] flex items-center justify-between">
                    <button @click="toggleSidebar" class="p-2 rounded-lg hover:bg-violet-500 transition-colors focus:outline-none">
                        <i :class="['pi', isCollapsed ? 'pi-bars' : 'pi-arrow-left', 'text-gray-600']"></i>
                    </button>
                </div>

                <!-- Navigation Section -->
                <nav class="flex-1 overflow-y-auto py-4 px-2">
                    <!-- Regular menu items -->
                    <div class="space-y-1">
                        <button
                            v-for="(item, index) in sideBarItems"
                            :key="index"
                            @click="navigateToPage(item.route)"
                            :class="[
                                'relative flex items-center rounded-lg transition-colors duration-200 w-full text-left',
                                isCollapsed ? 'justify-center p-3' : 'p-2',
                                isRouteActive(item.route)
                                    ? 'text-indigo-600 bg-indigo-50 hover:bg-indigo-50'
                                    : 'text-gray-600 hover:bg-gray-100'
                            ]"
                            :title="isCollapsed ? item.label : ''"
                        >
                            <i :class="[item.icon, isCollapsed ? 'text-lg' : 'text-lg mr-3', isRouteActive(item.route) ? 'text-indigo-600' : '']"></i>
                            <span :class="[isCollapsed ? 'hidden' : '', isRouteActive(item.route) ? 'font-medium' : '']">{{ item.label }}</span>
                            <div v-if="isRouteActive(item.route)" class="absolute left-0 top-0 bottom-0 w-1.5 bg-indigo-600 rounded-r"></div>
                            <span v-if="isCollapsed && item.badge" class="absolute top-1 right-1 flex items-center justify-center h-4 w-4 text-xs font-medium text-white bg-red-500 rounded-full">{{ item.badge }}</span>
                        </button>
                    </div>

                    <!-- Horizontal Line -->
                    <div :class="['my-4', isCollapsed ? 'mx-2' : 'mx-3']">
                        <div class="border-t border-gray-200"></div>
                    </div>

                    <!-- My Classes Section -->
                    <div v-if="auth?.user?.role === 'teacher' || auth?.user?.role === 'student'" class="mb-4">
                        <div class="flex items-center justify-between px-4 mb-2">
                            <div v-if="!isCollapsed" class="text-xs uppercase font-semibold text-gray-500 tracking-wider">My Classes</div>
                            <div :class="['flex', isCollapsed ? 'justify-center' : '']">
                                <button
                                    v-if="auth?.user?.role === 'teacher'"
                                    @click="showAddClassModal = true"
                                    class="text-indigo-600 hover:bg-indigo-50 rounded-lg p-1.5 transition-all duration-200"
                                    :title="isCollapsed ? 'Add Class' : ''"
                                >
                                    <i class="pi pi-plus" :class="{'text-lg': isCollapsed}"></i>
                                </button>
                            </div>
                        </div>

                        <!-- Classes List -->
                        <div class="space-y-1">
                            <button
                                v-for="class_ in classes"
                                :key="class_.id"
                                @click="navigateToClass(class_)"
                                class="flex items-center p-3 rounded-lg transition-all duration-200 mx-1 group relative overflow-hidden w-full text-left"
                                :class="{
                                    'bg-indigo-50 text-indigo-600 shadow-sm': isRouteActive('TeacherRoom') || isRouteActive('StudentRoom'),
                                    'hover:bg-indigo-50 hover:text-indigo-600': !isRouteActive('TeacherRoom') && !isRouteActive('StudentRoom'),
                                    'active:bg-indigo-100 active:scale-[0.98]': true
                                }"
                                :style="(isRouteActive('TeacherRoom') || isRouteActive('StudentRoom')) ? 'background-color: rgba(99, 102, 241, 0.1);' : ''"
                                :title="isCollapsed ? class_.name : ''"
                            >
                                <div v-if="isRouteActive('TeacherRoom') || isRouteActive('StudentRoom')" class="absolute left-0 top-0 bottom-0 w-1 bg-indigo-600"></div>
                                <div class="flex items-center gap-3 w-full">
                                    <div
                                        :class="[
                                            'w-8 h-8 rounded-lg flex items-center justify-center text-white shadow-sm transition-all duration-200',
                                            getClassColor(class_.theme),
                                            (isRouteActive('TeacherRoom') || isRouteActive('StudentRoom'))
                                                ? 'scale-110 ring-2 ring-offset-2 ring-indigo-600'
                                                : 'group-hover:scale-105 group-hover:ring-2 group-hover:ring-offset-2 group-hover:ring-indigo-600/50'
                                        ]"
                                    >
                                        <span class="text-xs font-semibold">{{ class_.name.split(' ')[1] }}</span>
                                    </div>
                                    <span v-if="!isCollapsed" class="text-sm font-medium truncate">{{ class_.name }}</span>
                                    <div
                                        v-if="(isRouteActive('TeacherRoom') || isRouteActive('StudentRoom')) && !isCollapsed"
                                        class="ml-auto w-1.5 h-5 rounded-sm bg-indigo-600 transition-all duration-200"
                                    ></div>
                                </div>
                            </button>
                        </div>

                        <!-- Join Class Button -->
                        <div class="mt-4 px-3" v-if="auth?.user?.role === 'student'">
                            <button
                                @click="showJoinClassModal = true"
                                :class="[
                                    'flex items-center justify-center gap-2 p-3 text-gray-700 hover:bg-gray-100 rounded-lg transition-all duration-200 border border-gray-200 w-full',
                                    isCollapsed ? 'w-10 h-10 mx-auto' : 'w-full'
                                ]"
                            >
                                <i class="pi pi-plus text-sm"></i>
                                <span v-if="!isCollapsed" class="text-sm font-medium">Join Class</span>
                            </button>
                        </div>
                    </div>
                </nav>
            </div>

            <!-- Main Content Area -->
            <div class="flex-1 flex flex-col overflow-hidden w-full min-h-screen">
                <nav class="bg-white/90 backdrop-blur-sm shadow-md sticky top-0 border-b border-indigo-100 h-[52px] z-10 w-full">
                    <div class="w-full h-full">
                        <div class="flex justify-between items-center px-4 h-full">
                            <!-- Logo -->
                            <div class="flex items-center">
                                <img
                                    :src="logoUrl"
                                    class="w-auto h-8 mr-2"
                                    alt="DigiPort Logo"
                                />
                                <span class="text-xl font-bold text-gray-800">DigiPort</span>
                            </div>

                            <!-- Bell and User Profile -->
                            <div class="flex items-center gap-6">
                                <!-- Bell Icon with Dropdown -->
                                <div class="relative">
                                    <button
                                        @click.stop="showNotifications = !showNotifications"
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
                                        class="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden z-50"
                                        @click.stop
                                    >
                                        <!-- Header -->
                                        <div class="px-4 py-3 border-b border-gray-100 bg-gray-50">
                                            <div class="flex items-center justify-between">
                                                <h3 class="font-semibold text-gray-900">Notifications</h3>
                                                <button
                                                    @click="navigateToNotifications"
                                                    class="text-sm text-indigo-600 hover:text-indigo-900 font-medium"
                                                >
                                                    View All
                                                </button>
                                            </div>
                                        </div>

                                        <!-- Notifications List -->
                                        <div class="max-h-[400px] overflow-y-auto">
                                            <div
                                                v-for="notification in notifications.slice(0, 5)"
                                                :key="notification.id"
                                                @click="markAsRead(notification.id)"
                                                class="group px-4 py-3 hover:bg-gray-50 transition-colors cursor-pointer border-b border-gray-100 last:border-0"
                                                :class="{ 'bg-indigo-50': notification.isUnread }"
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
                                                        <p class="text-sm text-gray-600 line-clamp-2">
                                                            {{ notification.message }}
                                                        </p>
                                                        <p class="text-xs text-gray-500">
                                                            {{ formatDate(notification.date) }}
                                                        </p>
                                                    </div>

                                                    <!-- Unread Indicator -->
                                                    <div v-if="notification.isUnread"
                                                        class="w-2 h-2 rounded-full bg-indigo-600 shrink-0 mt-2">
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
                                        @click.stop="toggleDropdown"
                                        class="flex items-center gap-3 hover:bg-gray-100 rounded-full py-1.5 px-2 transition-all duration-200"
                                    >
                                        <img
                                            :src="auth?.user?.avatar || `https://ui-avatars.com/api/?name=${auth?.user?.name}`"
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
                                        @click.stop
                                    >
                                        <!-- User Info -->
                                        <div class="px-4 py-3 border-b border-gray-100">
                                            <p class="text-sm font-medium text-gray-900">{{ auth?.user?.name }}</p>
                                            <p class="text-xs text-gray-500">{{ auth?.user?.email }}</p>
                                        </div>

                                        <!-- Menu Items -->
                                        <div class="py-1">
                                            <button
                                                class="flex items-center justify-between w-full text-left text-sm font-medium text-indigo-900 hover:bg-indigo-50 px-4 py-2.5 rounded-lg"
                                            >
                                                <i class="pi pi-user text-gray-400"></i>
                                                Profile
                                            </button>
                                            <button
                                                class="flex items-center justify-between w-full text-left text-sm font-medium text-indigo-900 hover:bg-indigo-50 px-4 py-2.5 rounded-lg"
                                            >
                                                <i class="pi pi-cog text-gray-400"></i>
                                                Settings
                                            </button>
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
                <main class="flex-1 overflow-y-auto bg-transparent min-h-screen">
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
        class="rounded-xl"
    >
        <div class="flex flex-col gap-4 p-4">
            <div class="flex flex-col gap-2">
                <label class="text-sm font-medium text-gray-700">Grade</label>
                <InputText
                    v-model="newClassForm.grade"
                    placeholder="Enter grade number (1-12)"
                    @input="validateGrade"
                    class="p-2 w-full rounded-lg border-gray-300 focus:border-[#B8AAFF] focus:ring focus:ring-[#B8AAFF]/20 hover:bg-gray-50 hover:border-gray-400 transition-all duration-200"
                />
            </div>

            <div class="flex flex-col gap-2">
                <label class="text-sm font-medium text-gray-700">Section</label>
                <InputText
                    v-model="newClassForm.section"
                    placeholder="Enter section letter (A-Z)"
                    @input="validateSection"
                    class="p-2 w-full rounded-lg border-gray-300 focus:border-[#B8AAFF] focus:ring focus:ring-[#B8AAFF]/20 hover:bg-gray-50 hover:border-gray-400 transition-all duration-200"
                />
            </div>

            <!-- Theme Selection -->
            <div class="flex flex-col gap-2">
                <label class="text-sm font-medium text-gray-700">Theme Color</label>
                <div class="grid grid-cols-3 gap-2">
                    <button
                        v-for="theme in themeOptions"
                        :key="theme.id"
                        @click="newClassForm.theme = theme.id"
                        :class="[
                            'p-2 rounded-lg border-2 flex items-center gap-2 transition-all',
                            newClassForm.theme === theme.id ? 'border-[#7BBBFE] bg-[#7BBBFE]/10' : 'border-transparent hover:bg-gray-50'
                        ]"
                    >
                        <div :class="['w-4 h-4 rounded-full', theme.color]"></div>
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
                    class="bg-[#B8AAFF] border-[#B8AAFF] hover:bg-[#A799EE] hover:border-[#A799EE]"
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
        class="rounded-xl"
    >
        <div class="flex flex-col gap-4 p-4">
            <div class="flex flex-col gap-2">
                <label class="text-sm font-medium text-gray-700">Class Code</label>
                <InputText
                    v-model="joinClassForm.code"
                    placeholder="Enter class code"
                    class="p-2 w-full rounded-lg border-gray-300 focus:border-[#B8AAFF] focus:ring focus:ring-[#B8AAFF]/20 hover:bg-gray-50 hover:border-gray-400 transition-all duration-200"
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
                    class="bg-[#B8AAFF] border-[#B8AAFF] hover:bg-[#A799EE] hover:border-[#A799EE]"
                />
            </div>
        </template>
    </Dialog>
</template>

<style scoped>
.line-clamp-1 {
    display: -webkit-box;
    -webkit-line-clamp: 1;
    line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

:deep(.p-dialog) {
    border-radius: 0.75rem;
    overflow: hidden;
}

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

:deep(.p-button) {
    border-radius: 0.5rem;
}
</style>
