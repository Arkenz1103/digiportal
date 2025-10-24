<script setup>
import { ref, computed, onMounted, onUnmounted, provide, watch } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import { useToast } from '@/Composables/useToast';

// Define emits for navigation
const emit = defineEmits(['navigate']);

// Use a runtime URL so Vite doesn't transform it to an import
const logoUrl = '/logo.jpg';

// Sidebar collapse state
const isCollapsed = ref(false);
provide('isSidebarCollapsed', isCollapsed);

// Profile dropdown state
const isDropdownOpen = ref(false);

// Initialize toast
const { showSuccess, showInfo } = useToast();

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
const allNotifications = ref([]);
const unreadCount = ref(0);
const displayLimit = ref(5);
const isLoadingMore = ref(false);
const lastOpenedCount = ref(parseInt(localStorage.getItem('notifications_last_opened') || '0'));
const newNotificationsCount = ref(0);

// Load notifications from backend
const loadNotifications = async () => {
    try {
        console.log('🔄 Loading notifications from /api/notifications/...');
        const response = await fetch('/api/notifications/', {
            credentials: 'include', // Include cookies for authentication
            headers: {
                'Accept': 'application/json',
            }
        });
        
        console.log('📡 Response status:', response.status);
        
        if (response.ok) {
            const data = await response.json();
            console.log('📦 Raw data received:', data);
            
            // Get the last time user opened dropdown
            const lastOpenedTime = parseInt(localStorage.getItem('notifications_last_opened_time') || '0');
            
            allNotifications.value = data.map(notif => {
                const createdTime = new Date(notif.created_at).getTime();
                
                // Mark as NEW if created after the last time dropdown was opened
                const isNew = createdTime > lastOpenedTime;
                
                return {
                    id: notif.id,
                    type: notif.notification_type,
                    title: notif.title,
                    message: notif.message,
                    date: new Date(notif.created_at),
                    isNew: isNew,
                    isUnread: !notif.is_read,
                };
            });
            
            // Show only first 5 initially
            notifications.value = allNotifications.value.slice(0, displayLimit.value);
            unreadCount.value = allNotifications.value.filter(n => n.isUnread).length;
            
            // Calculate badge count: count notifications with isNew = true (created within last 1 minute)
            const newCount = allNotifications.value.filter(n => n.isNew).length;
            
            // Update badge count
            newNotificationsCount.value = newCount;
            
            console.log('✅ Loaded notifications:', allNotifications.value.length, 'total');
            console.log('📊 Displaying:', notifications.value.length, 'notifications');
            console.log('🔔 Unread count:', unreadCount.value);
            console.log('🆕 New notifications (< 1 min):', newCount);
            console.log('🎯 Badge count:', newNotificationsCount.value);
        } else {
            try {
                const errorData = await response.json();
                console.error('❌ Failed to load notifications:', response.status, errorData);
            } catch (e) {
                console.error('❌ Failed to load notifications:', response.status, response.statusText);
            }
        }
    } catch (error) {
        console.error('❌ Error loading notifications:', error);
        console.error('Error details:', error.message);
    }
};

// Load more notifications
const loadMoreNotifications = () => {
    isLoadingMore.value = true;
    displayLimit.value += 5;
    notifications.value = allNotifications.value.slice(0, displayLimit.value);
    
    setTimeout(() => {
        isLoadingMore.value = false;
    }, 300);
};

// Watch for dropdown open/close
watch(showNotifications, (isOpen) => {
    if (isOpen) {
        // When dropdown opens, save the current timestamp
        const currentTime = Date.now();
        localStorage.setItem('notifications_last_opened_time', currentTime.toString());
        
        // Hide badge immediately
        newNotificationsCount.value = 0;
        
        console.log('📂 Dropdown opened');
        console.log('⏰ Saved timestamp:', new Date(currentTime).toLocaleString());
        console.log('🔕 Badge hidden');
    }
});

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
        'portfolio_created': 'bg-gradient-to-br from-green-400 to-emerald-500',
        'portfolio_updated': 'bg-gradient-to-br from-blue-400 to-blue-500',
        'portfolio_deleted': 'bg-gradient-to-br from-red-400 to-rose-500',
        'activity_created': 'bg-gradient-to-br from-indigo-400 to-indigo-500',
        'activity_updated': 'bg-gradient-to-br from-blue-400 to-cyan-500',
        'activity_deleted': 'bg-gradient-to-br from-red-400 to-pink-500',
        'submission_approved': 'bg-gradient-to-br from-green-400 to-teal-500',
        'submission_rejected': 'bg-gradient-to-br from-red-500 to-orange-500',
        'score_added': 'bg-gradient-to-br from-yellow-400 to-amber-500',
        'submission_received': 'bg-gradient-to-br from-indigo-400 to-purple-500',
        'approval_requested': 'bg-gradient-to-br from-violet-400 to-purple-500',
    };
    return colorMap[type] || 'bg-gradient-to-br from-indigo-400 to-purple-500';
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
            unreadCount.value = allNotifications.value.filter(n => n.isUnread).length;
        }
    } catch (error) {
        console.error('Error marking notification as read:', error);
    }
};

// Delete all notifications
const deleteAllNotifications = async () => {
    if (!confirm('Are you sure you want to delete all notifications?')) {
        return;
    }
    
    try {
        // Delete all notifications via API
        const deletePromises = allNotifications.value.map(notif => 
            fetch(`/api/notifications/${notif.id}/`, {
                method: 'DELETE',
                credentials: 'include',
            })
        );
        
        await Promise.all(deletePromises);
        
        // Clear local state
        allNotifications.value = [];
        notifications.value = [];
        unreadCount.value = 0;
        newNotificationsCount.value = 0;
        
        console.log('✅ All notifications deleted');
    } catch (error) {
        console.error('❌ Error deleting notifications:', error);
        alert('Failed to delete notifications. Please try again.');
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
    const savedAvatar = localStorage.getItem('digiportal_user_avatar');
    
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

    currentUser.value.avatar = savedAvatar || null;
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
            { label: 'Remarked', icon: 'pi pi-comments', route: 'StudentRemarked' },
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

// Profile Function
const goToProfile = () => {
    isDropdownOpen.value = false; // Close dropdown
    emit('navigate', 'TeacherProfile');
    console.log('📱 Navigate to Profile page');
};

// Settings Function
const goToSettings = () => {
    isDropdownOpen.value = false; // Close dropdown
    emit('navigate', 'TeacherSettings');
    console.log('⚙️ Navigate to Settings page');
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
    
    // Determine target route based on user role
    const targetRoute = currentUser.value.role === 'teacher' ? 'TeacherRoom' : 'StudentRoom';
    
    // Always dispatch the classChanged event so Room component can reload
    console.log('🔄 Class selected, dispatching classChanged event...', class_.name);
    window.dispatchEvent(new CustomEvent('classChanged', { detail: class_ }));
    
    // If not already on the room page, navigate to it
    if (currentRoute.value !== targetRoute) {
        console.log('📍 Navigating to room page...');
        navigateToPage(targetRoute);
    } else {
        console.log('✅ Already on room page, event will trigger reload');
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
    if ([
        'digiportal_user_role',
        'digiportal_user_email',
        'digiportal_user_name',
        'digiportal_user_avatar'
    ].includes(e.key)) {
        loadUserData();
        console.log('User data refreshed from storage change');
    }
};

// Custom event listener for same-tab localStorage changes
const handleUserDataChange = (event) => {
    const detail = event?.detail || {};
    if (detail.name) {
        currentUser.value.name = detail.name;
    }
    if (detail.email) {
        currentUser.value.email = detail.email;
    }
    if (Object.prototype.hasOwnProperty.call(detail, 'avatar')) {
        currentUser.value.avatar = detail.avatar;
        if (detail.avatar) {
            localStorage.setItem('digiportal_user_avatar', detail.avatar);
        } else {
            localStorage.removeItem('digiportal_user_avatar');
        }
    }
    console.log('User data refreshed from custom event', detail);
};

onMounted(() => {
    document.addEventListener('click', closeDropdowns);
    loadUserData(); // Load user data when component mounts
    loadNotifications(); // Load notifications
    
    // Listen for storage changes from other tabs
    window.addEventListener('storage', handleStorageChange);
    
    // Listen for custom event for same-tab changes
    window.addEventListener('userDataChanged', handleUserDataChange);
    
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
                <div class="p-4 border-b h-[52px] flex items-center relative overflow-hidden">
                    <button 
                        @click="toggleSidebar" 
                        class="p-2 rounded-lg hover:bg-blue-500 transition-all duration-300 ease-in-out focus:outline-none"
                        :style="{ transform: isCollapsed ? 'translateX(0)' : 'translateX(192px)' }"
                    >
                        <i class="pi pi-bars text-gray-600"></i>
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
                            class="flex items-center p-3 rounded-lg transition-all duration-200 mx-1 group relative overflow-hidden w-full text-left"
                            :class="{
                                'bg-indigo-50 text-indigo-600 shadow-sm': isRouteActive(item.route),
                                'hover:bg-indigo-50 hover:text-indigo-600': !isRouteActive(item.route),
                                'active:bg-indigo-100 active:scale-[0.98]': true
                            }"
                            :style="isRouteActive(item.route) ? 'background-color: rgba(99, 102, 241, 0.1);' : ''"
                            :title="isCollapsed ? item.label : ''"
                        >
                            <div v-if="isRouteActive(item.route)" class="absolute left-0 top-0 bottom-0 w-1 bg-indigo-600"></div>
                            <div class="flex items-center gap-3 w-full">
                                <i :class="[item.icon, 'text-lg', isRouteActive(item.route) ? 'text-indigo-600' : 'text-gray-600']"></i>
                                <span v-if="!isCollapsed" :class="['text-sm font-medium truncate', isRouteActive(item.route) ? 'text-indigo-600' : 'text-gray-600']">{{ item.label }}</span>
                                <div
                                    v-if="isRouteActive(item.route) && !isCollapsed"
                                    class="ml-auto w-1.5 h-5 rounded-sm bg-indigo-600 transition-all duration-200"
                                ></div>
                            </div>
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
                                        class="relative w-12 h-12 flex items-center justify-center hover:bg-gray-100 rounded-full transition-all duration-300 focus:outline-none group"
                                        :class="{ 'bg-gray-100': showNotifications }"
                                    >
                                        <i class="pi pi-bell text-gray-700 text-2xl transition-transform duration-300 group-hover:scale-110" 
                                           :class="{ 'animate-bounce text-indigo-600': newNotificationsCount > 0 && !showNotifications }"></i>
                                        <!-- Notification Badge -->
                                        <div
                                            v-if="newNotificationsCount > 0 && !showNotifications"
                                            class="absolute top-0 right-0 bg-gradient-to-r from-red-500 to-pink-500 text-white text-[10px] w-5 h-5 flex items-center justify-center rounded-full font-bold shadow-lg animate-pulse"
                                        >
                                            {{ newNotificationsCount > 9 ? '9+' : newNotificationsCount }}
                                        </div>
                                    </button>

                                    <!-- Notifications Dropdown -->
                                    <div
                                        v-show="showNotifications"
                                        class="absolute right-0 top-full mt-2 w-96 max-h-[600px] bg-white rounded-2xl shadow-2xl border-2 border-indigo-100 overflow-hidden z-50 transform transition-all duration-300"
                                        :class="showNotifications ? 'scale-100 opacity-100' : 'scale-95 opacity-0'"
                                        @click.stop
                                    >
                                        <!-- Header -->
                                        <div class="px-5 py-4 border-b border-gray-100 bg-gradient-to-r from-indigo-50 to-purple-50">
                                            <div class="flex items-center justify-between">
                                                <div class="flex items-center gap-2">
                                                    <div class="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center">
                                                        <i class="pi pi-bell text-white text-sm"></i>
                                                    </div>
                                                    <h3 class="font-bold text-gray-900">Notifications</h3>
                                                    <span v-if="unreadCount > 0" class="px-2 py-0.5 bg-red-500 text-white text-xs rounded-full font-bold">
                                                        {{ unreadCount }}
                                                    </span>
                                                </div>
                                                <button
                                                    @click="navigateToNotifications"
                                                    class="text-sm text-indigo-600 hover:text-indigo-900 font-semibold hover:underline transition-all"
                                                >
                                                    View All
                                                </button>
                                            </div>
                                        </div>

                                        <!-- Notifications List -->
                                        <div class="max-h-[400px] overflow-y-auto">
                                            <div
                                                v-for="notification in notifications"
                                                :key="notification.id"
                                                @click="markAsRead(notification.id)"
                                                class="group px-5 py-4 hover:bg-gradient-to-r hover:from-indigo-50 hover:to-purple-50 transition-all duration-200 cursor-pointer border-b border-gray-100 last:border-0"
                                                :class="{ 'bg-gradient-to-r from-indigo-50/50 to-purple-50/50': notification.isUnread }"
                                            >
                                                
                                                <div class="flex items-start gap-3">
                                                    <!-- Icon -->
                                                    <div class="relative">
                                                        <div
                                                            class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 shadow-md transition-transform duration-200 group-hover:scale-110"
                                                            :class="getNotificationColor(notification.type)"
                                                        >
                                                            <i :class="['pi text-white', getNotificationIcon(notification.type)]"></i>
                                                        </div>
                                                        <div v-if="notification.isNew" class="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full border-2 border-white animate-pulse"></div>
                                                    </div>

                                                    <!-- Content -->
                                                    <div class="flex-1 min-w-0">
                                                        <div class="flex items-start justify-between gap-2 mb-1">
                                                            <p class="font-semibold text-sm text-gray-900 line-clamp-1">
                                                                {{ notification.title }}
                                                            </p>
                                                            <span
                                                                v-if="notification.isNew"
                                                                class="px-2 py-0.5 bg-gradient-to-r from-red-500 to-pink-500 text-white text-xs rounded-full font-bold shrink-0"
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

                                                </div>
                                            </div>

                                            <!-- Empty State -->
                                            <div
                                                v-if="notifications.length === 0"
                                                class="px-6 py-12 text-center"
                                            >
                                                <div class="relative inline-block mb-4">
                                                    <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center">
                                                        <i class="pi pi-bell text-indigo-400 text-3xl"></i>
                                                    </div>
                                                    <div class="absolute -bottom-1 -right-1 w-6 h-6 bg-green-500 rounded-full border-2 border-white flex items-center justify-center">
                                                        <i class="pi pi-check text-white text-xs"></i>
                                                    </div>
                                                </div>
                                                <p class="text-gray-700 font-semibold mb-1">All Caught Up!</p>
                                                <p class="text-gray-500 text-sm">No new notifications at the moment</p>
                                            </div>
                                        </div>

                                        <!-- Load More Notifications Button -->
                                        <div v-if="notifications.length < allNotifications.length" class="border-t border-gray-100 p-3 bg-gray-50">
                                            <button
                                                @click="loadMoreNotifications"
                                                :disabled="isLoadingMore"
                                                class="w-full py-3 px-4 bg-gradient-to-r from-gray-100 to-gray-200 hover:from-indigo-50 hover:to-purple-50 text-gray-700 hover:text-indigo-700 font-semibold rounded-xl transition-all duration-300 flex items-center justify-center gap-2 group disabled:opacity-50 disabled:cursor-not-allowed"
                                            >
                                                <i v-if="!isLoadingMore" class="pi pi-history text-sm group-hover:scale-110 transition-transform"></i>
                                                <i v-else class="pi pi-spin pi-spinner text-sm"></i>
                                                <span>{{ isLoadingMore ? 'Loading...' : 'See previous notifications' }}</span>
                                            </button>
                                        </div>
                                        
                                        <!-- View All Button (when all loaded) -->
                                        <div v-else-if="allNotifications.length > 5" class="border-t border-gray-100 p-3 bg-gray-50">
                                            <button
                                                @click="navigateToNotifications"
                                                class="w-full py-3 px-4 bg-gradient-to-r from-indigo-100 to-purple-100 hover:from-indigo-200 hover:to-purple-200 text-indigo-700 font-semibold rounded-xl transition-all duration-300 flex items-center justify-center gap-2 group"
                                            >
                                                <i class="pi pi-external-link text-sm group-hover:scale-110 transition-transform"></i>
                                                <span>View all in notifications page</span>
                                            </button>
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
                                                @click="goToProfile"
                                                class="flex items-center justify-between w-full text-left text-sm font-medium text-indigo-900 hover:bg-indigo-50 px-4 py-2.5 rounded-lg transition-colors duration-200"
                                            >
                                                <i class="pi pi-user text-gray-400"></i>
                                                Profile
                                            </button>
                                            <button
                                                @click="goToSettings"
                                                class="flex items-center justify-between w-full text-left text-sm font-medium text-indigo-900 hover:bg-indigo-50 px-4 py-2.5 rounded-lg transition-colors duration-200"
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
