<script setup>
import { ref, computed, onMounted, onUnmounted, provide, watch } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import { useToast } from '../composables/useToast';

const { showSuccess, showError, showInfo, showWarning } = useToast();

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

// Add state for classes - will be loaded dynamically from API
const classes = ref([]);

// State for subjects in sidebar
const subjectsInSidebar = ref([]);

// State for selected subject to track active folder
const selectedSubject = ref(null);
const selectedClassForSubject = ref(null);

// State for My Classes dropdown
const isMyClassesDropdownOpen = ref(false);

// State for expanded classes - simplified to track single expanded class
const expandedClassId = ref(null);

// Initialize expanded classes when needed
const initializeExpandedClasses = () => {
    if (classes.value && classes.value.length > 0) {
        expandedClassId.value = classes.value[0]?.id || null; // Expand first class by default
    }
};

// Toggle class expansion
const toggleClass = (classId) => {
    expandedClassId.value = expandedClassId.value === classId ? null : classId;
};

// Safe helper to extract section letter from class name (e.g., "Grade 1 - A" -> "A")
const getClassSection = (className) => {
    if (!className || typeof className !== 'string') return '';
    const parts = className?.split(' ') || [];
    return parts.length > 1 ? parts[parts.length - 1] : (className || '');
};

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
const showDeleteAllDialog = ref(false);

// Load notifications from backend
const loadNotifications = async () => {
    try {
        console.log('🔄 Loading notifications from /api/notifications/...');

        const response = await fetch('/api/notifications/', {
            credentials: 'include', // Include cookies for authentication
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', // Help Django recognize AJAX requests
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
                showError('Failed to load notifications', 'Error');
            } catch (e) {
                console.error('❌ Failed to load notifications:', response.status, response.statusText);
                showError('Failed to load notifications', 'Error');
            }
        }
    } catch (error) {
        console.error('❌ Error loading notifications:', error);
        console.error('Error details:', error.message);
        showError('Failed to load notifications. Please check your connection.', 'Connection Error');
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
        // Find the notification first to get its type
        const notification = notifications.value.find(n => n.id === id) ||
                           allNotifications.value.find(n => n.id === id);

        const response = await fetch('/api/notifications/', {
            method: 'PUT',
            credentials: 'include', // Include session cookies
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', // Help Django recognize AJAX requests
            },
            body: JSON.stringify({ notification_id: id })
        });

        if (response.ok) {
            if (notification) {
                notification.isUnread = false;
                notification.isNew = false;
            }
            unreadCount.value = allNotifications.value.filter(n => n.isUnread).length;

            // Close the dropdown
            showNotifications.value = false;

            // Navigate based on notification type
            if (notification) {
                handleNotificationNavigation(notification);
            }
        } else if (response.status === 403 || response.status === 401) {
            console.error('❌ Authentication failed - Please refresh the page');
            // Just navigate without marking as read
            showNotifications.value = false;
            if (notification) {
                handleNotificationNavigation(notification);
            }
        }
    } catch (error) {
        console.error('Error marking notification as read:', error);
        // Still navigate even if marking as read fails
        showNotifications.value = false;
        const notification = notifications.value.find(n => n.id === id) ||
                           allNotifications.value.find(n => n.id === id);
        if (notification) {
            handleNotificationNavigation(notification);
        }
    }
};

// Handle navigation based on notification type
const handleNotificationNavigation = (notification) => {
    const type = notification.type;
    const userRole = currentUser.value.role;

    console.log(`📍 Navigating for notification type: ${type}, user role: ${userRole}`);

    if (userRole === 'student') {
        // Student navigation
        if (type === 'activity_created' || type === 'activity_updated') {
            if (window.navigateTo) {
                window.navigateTo('StudentRoom');
            } else {
                window.location.href = '/student/room';
            }
        } else if (type === 'submission_approved') {
            if (window.navigateTo) {
                window.navigateTo('StudentNewsfeed');
            } else {
                window.location.href = '/student/newsfeed';
            }
        } else if (type === 'submission_rejected') {
            if (window.navigateTo) {
                window.navigateTo('StudentSketch');
            } else {
                window.location.href = '/student/sketch';
            }
        } else if (type === 'score_added') {
            if (window.navigateTo) {
                window.navigateTo('StudentRoom');
            } else {
                window.location.href = '/student/room';
            }
        } else if (type === 'portfolio_created' || type === 'portfolio_updated') {
            if (window.navigateTo) {
                window.navigateTo('StudentRoom');
            } else {
                window.location.href = '/student/room';
            }
        } else {
            // Default: navigate to classroom
            if (window.navigateTo) {
                window.navigateTo('StudentRoom');
            } else {
                window.location.href = '/student/room';
            }
        }
    } else if (userRole === 'teacher') {
        // Teacher navigation
        if (type === 'submission_received' || type === 'approval_requested') {
            if (window.navigateTo) {
                window.navigateTo('TeacherNotice');
            } else {
                window.location.href = '/teacher/notice';
            }
        } else if (type === 'submission_approved' || type === 'submission_rejected') {
            if (window.navigateTo) {
                window.navigateTo('TeacherOutputs');
            } else {
                window.location.href = '/teacher/outputs';
            }
        } else if (type === 'activity_created' || type === 'activity_updated') {
            if (window.navigateTo) {
                window.navigateTo('TeacherRoom');
            } else {
                window.location.href = '/teacher/room';
            }
        } else if (type === 'portfolio_created' || type === 'portfolio_updated') {
            if (window.navigateTo) {
                window.navigateTo('TeacherRoom');
            } else {
                window.location.href = '/teacher/room';
            }
        } else {
            // Default: navigate to home
            if (window.navigateTo) {
                window.navigateTo('TeacherHome');
            } else {
                window.location.href = '/teacher/home';
            }
        }
    }
};

// Delete all notifications
const deleteAllNotifications = () => {
    showDeleteAllDialog.value = true;
};

const confirmDeleteAllNotifications = async () => {
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
        showDeleteAllDialog.value = false;

        console.log('✅ All notifications deleted');
        showSuccess('All notifications deleted successfully', 'Deleted');
    } catch (error) {
        console.error('❌ Error deleting notifications:', error);
        showError('Failed to delete notifications. Please try again.', 'Error');
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

// User data loaded from localStorage and API
const currentUser = ref({
    name: 'User Name',
    email: 'user@example.com',
    role: 'student', // Default to student
    student_id: null,
    grade_level: null,
    section: null,
    department: null,
    id_number: null,
    profile_picture_url: null
});

// Load user profile from API
const loadUserProfile = async () => {
    try {
        const response = await fetch('/api/user/profile/', {
            credentials: 'include',
            headers: { 'Accept': 'application/json' }
        });

        if (response.ok) {
            const data = await response.json();

            // Construct name and remove "Teacher" or "Student" suffix for teachers
            let displayName = `${data.first_name || ''} ${data.last_name || ''}`.trim() || 'User';
            if (data.role === 'teacher') {
                // Remove "Teacher" or "Student" from the end of the name
                displayName = displayName.replace(/\s+(Teacher|Student)$/i, '').trim();
            }

            currentUser.value = {
                name: displayName,
                email: data.email || '',
                role: data.role || 'student',
                student_id: data.student_id || data.id_number,
                grade_level: data.grade_level,
                section: data.section,
                department: data.department,
                id_number: data.id_number,
                profile_picture_url: data.profile_picture_url
            };

            // Save to localStorage
            localStorage.setItem('digiportal_user_name', currentUser.value.name);
            localStorage.setItem('digiportal_user_email', currentUser.value.email);
            localStorage.setItem('digiportal_user_role', currentUser.value.role);

            console.log('✅ User profile loaded:', currentUser.value);
        }
    } catch (error) {
        console.error('❌ Error loading user profile:', error);
        // Fallback to localStorage
        loadUserDataFromLocalStorage();
    }
};

// Load user data from localStorage (fallback)
const loadUserDataFromLocalStorage = () => {
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

// Sidebar menu items (without Classroom - moved to MY CLASSES section)
const sideBarItems = computed(() => {
    const roleBasedItems = {
        teacher: [
            { label: 'Home', icon: 'pi pi-home', route: 'TeacherHome' },
            { label: 'Remarks', icon: 'pi pi-comments', route: 'TeacherRemarks' },
            { label: 'Notice', icon: 'pi pi-check-circle', route: 'TeacherNotice' },
            // { label: 'Archived', icon: 'pi pi-inbox', route: 'TeacherArchived' },
        ],
        student: [
            { label: 'Home', icon: 'pi pi-home', route: 'StudentNewsfeed' },
            { label: 'Sketch', icon: 'pi pi-pencil', route: 'StudentSketch' },
            { label: 'Remarked', icon: 'pi pi-comments', route: 'StudentRemarked' },
            // { label: 'Archived', icon: 'pi pi-inbox', route: 'StudentArchived' },
        ],
    };

    return roleBasedItems[currentUser.value.role] || [];
});

// Logout Function
const logout = async () => {
    try {
        // Call backend logout API to clear server-side session
        await fetch('/api/auth/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
    } catch (error) {
        console.error('Logout API error:', error);
    }

    // Clear ALL localStorage items related to user session
    localStorage.removeItem('digiportal_logged_in');
    localStorage.removeItem('digiportal_user_role');
    localStorage.removeItem('digiportal_user_email');
    localStorage.removeItem('digiportal_user_name');
    localStorage.removeItem('digiportal_user_id');
    localStorage.removeItem('digiportal_auth_token');
    localStorage.removeItem('digiportal_current_page');

    // Clear any other session data
    sessionStorage.clear();

    // Dispatch event to notify other components
    window.dispatchEvent(new Event('userLoggedOut'));

    // Navigate to landing page
    emit('navigate', 'Landing');
};

// Navigate to Profile
const navigateToProfile = () => {
    isDropdownOpen.value = false; // Close dropdown
    emit('navigate', 'Profile');
};

// Navigate to Settings
const navigateToSettings = () => {
    isDropdownOpen.value = false; // Close dropdown
    emit('navigate', 'Settings');
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

    // Clear selected subject and class when navigating to other pages
    // This prevents the active hover state from remaining when clicking other sidebar items
    if (page !== 'TeacherRoom' && page !== 'StudentRoom') {
        selectedSubject.value = null;
        selectedClassForSubject.value = null;
        localStorage.removeItem('digiportal_selected_subject');
        localStorage.removeItem('digiportal_selected_class');
    }

    emit('navigate', page);
};

// Navigate to class room
const navigateToClass = (class_) => {
    // Clear any selected subject
    selectedSubject.value = null;
    selectedClassForSubject.value = null;

    // Store selected class information
    localStorage.setItem('digiportal_selected_class', JSON.stringify(class_));

    // Determine target route based on user role
    const targetRoute = currentUser.value.role === 'teacher' ? 'TeacherRoom' : 'StudentRoom';

    // Always dispatch the classChanged event so Room component can reload
    console.log('🔄 Class selected, dispatching classChanged event...', class_.name);
    window.dispatchEvent(new CustomEvent('classChanged', {
        detail: {
            classItem: class_,
            subject: null // Explicitly set subject to null
        }
    }));

    // If not already on the room page, navigate to it
    if (currentRoute.value !== targetRoute) {
        console.log('📍 Navigating to room page...');
        navigateToPage(targetRoute);
    } else {
        console.log('✅ Already on room page, event will trigger reload');
    }
};

// Navigate to subject folder - Always navigate to Student Activities (Room page)
const navigateToSubject = (classItem, subject) => {
    // Update selected subject tracking
    selectedSubject.value = subject;
    selectedClassForSubject.value = classItem;

    // Store selected class and subject information
    localStorage.setItem('digiportal_selected_class', JSON.stringify(classItem));
    localStorage.setItem('digiportal_selected_subject', subject);

    // Determine target route based on user role
    const targetRoute = currentUser.value.role === 'teacher' ? 'TeacherRoom' : 'StudentRoom';

    // Dispatch event with subject information
    console.log('📂 Subject selected:', subject, 'in class:', classItem.name);
    window.dispatchEvent(new CustomEvent('subjectChanged', {
        detail: {
            classItem: classItem, // Changed 'class' to 'classItem' to match Sroom.vue
            subject: subject
        }
    }));

    // Always navigate to the Student Activities (Room) page
    console.log('📍 Navigating to Student Activities page...');
    navigateToPage(targetRoute);
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
        loadUserProfile();
        console.log('User data refreshed from storage change');
    }
};

// Custom event listener for same-tab localStorage changes
const handleUserDataChange = () => {
    loadUserProfile();
    console.log('User data refreshed from custom event');
};

// Handle user logout event
const handleUserLogout = () => {
    console.log('User logged out, clearing data');
    // Reset user data to defaults
    currentUser.value = {
        name: '',
        email: '',
        role: 'student'
    };
};


// Load classrooms from API
const loadClassrooms = async () => {
    try {
        console.log('🏫 Loading classrooms from API...');
        const response = await fetch('/api/classrooms/', {
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
            }
        });

        if (response.ok) {
            const data = await response.json();
            console.log('📚 Classrooms data:', data);

            if (data.classrooms && data.classrooms.length > 0) {
                // Initialize classes without default subjects
                classes.value = data.classrooms.map(classroom => ({
                    id: classroom.id,
                    name: classroom.name,
                    grade_level: classroom.grade_level,
                    section: classroom.section,
                    theme: 'purple',
                    subjects: [] // Start with empty subjects array
                }));

                // Now load the actual subjects for each class
                await loadSubjectsForAllClasses();
                console.log('✅ Loaded classrooms with actual subjects:', classes.value);
            } else {
                console.log('⚠️ No classrooms found for this user');
                classes.value = []; // No default classes
            }
        } else {
            console.error('❌ Failed to load classrooms:', response.status);
            classes.value = []; // No default classes
        }
    } catch (error) {
        console.error('❌ Error loading classrooms:', error);
        classes.value = []; // No default classes
    }
};

// Load subjects for all classes from actual folders
const loadSubjectsForAllClasses = async () => {
    if (!classes.value || classes.value.length === 0) return;

    try {
        console.log('📂 Loading subjects from portfolio folders...');
        const response = await fetch('/api/portfolio/folders/', {
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
            }
        });

        if (response.ok) {
            const folders = await response.json();
            console.log('📂 Loaded folders:', folders);

            // Group folders by class
            const foldersByClass = {};
            folders.forEach(folder => {
                if (folder.classroom) {
                    if (!foldersByClass[folder.classroom]) {
                        foldersByClass[folder.classroom] = [];
                    }
                    foldersByClass[folder.classroom].push(folder.name);
                }
            });

            // Update classes with their actual subjects
            classes.value = classes.value.map(classItem => {
                const classFolders = foldersByClass[classItem.id] || [];
                return {
                    ...classItem,
                    subjects: [...new Set(classFolders)] // Remove duplicates
                };
            });

            console.log('✅ Updated classes with actual subjects:', classes.value);
        } else {
            console.error('❌ Failed to load folders:', response.status);
        }
    } catch (error) {
        console.error('❌ Error loading subjects from folders:', error);
    }
};


onMounted(async () => {
    // Load user data and notifications
    await loadUserProfile(); // Load from API first
    await loadNotifications(); // Load notifications
    await loadClassrooms(); // Load classrooms dynamically

    // Initialize expanded classes state
    initializeExpandedClasses();

    // Restore selected class from localStorage (but NOT the selected subject/folder)
    // This ensures only the class shows as active on page refresh, not the specific folder
    const savedClass = localStorage.getItem('digiportal_selected_class');
    if (savedClass) {
        try {
            const classData = JSON.parse(savedClass);
            selectedClassForSubject.value = classData;
            // Expand the class that was previously selected
            expandedClassId.value = classData.id;
            // Do NOT restore selectedSubject - it should be cleared on page refresh
            selectedSubject.value = null;
        } catch (e) {
            console.error('Error parsing saved class data:', e);
        }
    }

    // Small delay to ensure classrooms are loaded before loading subjects
    setTimeout(() => {
        loadSubjectsForAllClasses();
        initializeExpandedClasses();
    }, 500);

    // Detect current route from URL if not set
    if (!currentRoute.value || currentRoute.value === 'StudentNewsfeed') {
        const path = window.location.pathname;
        const routeMap = {
            '/student/newsfeed': 'StudentNewsfeed',
            '/student/room': 'StudentRoom',
            '/student/classroom': 'StudentClassroom',
            '/student/sketch': 'StudentSketch',
            '/student/remarked': 'StudentRemarked',
            '/student/notify': 'StudentNotify',
            '/student/archived': 'StudentArchived',
            '/teacher/home': 'TeacherHome',
            '/teacher/room': 'TeacherRoom',
            '/teacher/classroom': 'TeacherClassroom',
            '/teacher/notice': 'TeacherNotice',
            '/teacher/outputs': 'TeacherOutputs',
            '/teacher/progress': 'TeacherProgress',
            '/teacher/students': 'TeacherStudents',
            '/teacher/remarks': 'TeacherRemarks',
            '/teacher/notify': 'TeacherNotify',
            '/teacher/archived': 'TeacherArchived',
        };

        if (routeMap[path]) {
            currentRoute.value = routeMap[path];
            localStorage.setItem('digiportal_current_page', routeMap[path]);
            console.log('📍 Detected current route from URL:', routeMap[path]);
        }
    }

    // Listen for user data changes
    window.addEventListener('userDataChanged', handleUserDataChange);
    window.addEventListener('userLoggedOut', handleUserLogout);

    // Listen for folder selection from Room.vue to update sidebar active state
    window.addEventListener('folderSelected', (event) => {
        const { subject, classItem } = event.detail;
        console.log('📂 Folder selected event received:', subject, 'in class:', classItem?.name);
        selectedSubject.value = subject;
        selectedClassForSubject.value = classItem;
        // Expand the class that has the selected subject
        if (classItem?.id) {
            expandedClassId.value = classItem.id;
        }
    });

    // Debug: Log user data
    console.log('MainLayout mounted, user data:', currentUser.value);
});

onUnmounted(() => {
    document.removeEventListener('click', closeDropdowns);
    window.removeEventListener('storage', handleStorageChange);
    window.removeEventListener('userDataChanged', handleUserDataChange);
    window.removeEventListener('userLoggedOut', handleUserLogout);
    window.removeEventListener('folderSelected', () => {});
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
            <div :class="['bg-gradient-to-b from-indigo-600 via-indigo-700 to-blue-800 shadow-2xl sticky top-0 h-screen flex flex-col transition-all duration-200 ease-in-out z-10', isCollapsed ? 'w-16' : 'w-64']">
                <!-- Sidebar Header -->
                <div class="h-[52px] flex items-center justify-end pr-3 border-b border-white/10">
                    <button
                        @click="toggleSidebar"
                        class="p-2 rounded-lg hover:bg-white/20 transition-all duration-200 ease-in-out focus:outline-none"
                    >
                        <i class="pi pi-bars text-white text-lg"></i>
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
                            class="flex items-center rounded-lg transition-all duration-200 mx-1 group relative overflow-hidden w-full text-left"
                            :class="{
                                'bg-white/20 text-white shadow-lg backdrop-blur-sm': isRouteActive(item.route),
                                'text-white/80 hover:bg-white/10 hover:text-white': !isRouteActive(item.route),
                                'active:bg-white/25 active:scale-[0.98]': true,
                                'p-2 justify-center': isCollapsed,
                                'p-3': !isCollapsed
                            }"
                            :title="isCollapsed ? item.label : ''"
                        >
                            <div v-if="isRouteActive(item.route) && !isCollapsed" class="absolute left-0 top-0 bottom-0 w-1 bg-white rounded-r-full"></div>
                            <div class="flex items-center gap-3 w-full" :class="{'justify-center': isCollapsed}">
                                <i :class="[item.icon, 'text-lg flex-shrink-0', isRouteActive(item.route) ? 'text-white' : 'text-white/70']"></i>
                                <span v-if="!isCollapsed" :class="['text-sm font-medium truncate', isRouteActive(item.route) ? 'text-white' : 'text-white/80']">{{ item.label }}</span>
                                <div
                                    v-if="isRouteActive(item.route) && !isCollapsed"
                                    class="ml-auto w-1.5 h-5 rounded-sm bg-white transition-all duration-200"
                                ></div>
                            </div>
                            <span v-if="isCollapsed && item.badge" class="absolute top-1 right-1 flex items-center justify-center h-4 w-4 text-xs font-medium text-white bg-red-500 rounded-full">{{ item.badge }}</span>
                        </button>
                    </div>

                    <!-- Horizontal Line -->
                    <div :class="['my-4', isCollapsed ? 'mx-2' : 'mx-3']">
                        <div class="border-t border-white/20"></div>
                    </div>

                    <!-- My Classes Section - Clean Minimal Design -->
                    <template v-if="auth?.user?.role === 'teacher' || auth?.user?.role === 'student'">
                        <div class="mb-4">
                            <!-- MY CLASSES Header - Simple Text without Chevron -->
                            <div
                                v-if="!isCollapsed"
                                class="flex items-center gap-2 px-4 py-2 w-full text-left text-white/80"
                            >
                                <i class="pi pi-book text-sm text-white/70"></i>
                                <span class="text-sm font-medium flex-1">My Classes</span>
                            </div>
                            <div
                                v-else
                                class="flex items-center justify-center py-3 w-full text-white/70"
                                title="My Classes"
                            >
                                <i class="pi pi-book text-base"></i>
                            </div>

                            <!-- Classes and Subjects List - Always Visible -->
                            <template v-if="classes && classes.length > 0">
                                <div v-for="classItem in classes" :key="classItem?.id" class="transition-all duration-200" :class="isCollapsed ? 'mt-3' : 'mt-4'">
                                    <!-- Class Name - Dropdown Button -->
                                    <div class="flex items-center py-1.5 px-2 transition-all duration-200 w-full group" :class="{'justify-center': isCollapsed}">
                                        <div @click="navigateToClass(classItem)" class="flex items-center justify-center cursor-pointer transition-all duration-200 rounded-lg" :class="{
                                            'text-white bg-white/20': isRouteActive('TeacherRoom') || isRouteActive('StudentRoom'),
                                            'text-white/80 hover:text-white hover:bg-white/10': !isRouteActive('TeacherRoom') && !isRouteActive('StudentRoom'),
                                            'w-10 h-10': isCollapsed,
                                            'w-full px-3 py-2': !isCollapsed
                                        }" :title="isCollapsed ? classItem.name : ''">
                                            <div class="flex items-center gap-3 w-full">
                                                <div
                                                    class="w-8 h-8 rounded-lg flex items-center justify-center text-white text-xs font-semibold flex-shrink-0 transition-all duration-200"
                                                    :class="{
                                                        'bg-white/40': isRouteActive('TeacherRoom') || isRouteActive('StudentRoom'),
                                                        'bg-white/20 group-hover:bg-white/30': !isRouteActive('TeacherRoom') && !isRouteActive('StudentRoom')
                                                    }"
                                                >
                                                    {{ getClassSection(classItem?.name) }}
                                                </div>
                                                <span v-if="!isCollapsed" class="text-sm font-medium">{{ classItem?.name }}</span>
                                            </div>
                                        </div>
                                        <button v-if="!isCollapsed" @click.stop="toggleClass(classItem.id)" :class="['pi text-xs transition-transform duration-200 p-2', expandedClassId === classItem.id ? 'pi-chevron-down' : 'pi-chevron-right', 'text-white/60']"></button>
                                    </div>

                                    <!-- Subjects List - Visible When Class is Expanded -->
                                    <template v-if="!isCollapsed && expandedClassId === classItem.id && classItem?.subjects && classItem.subjects.length > 0">
                                        <div class="mt-1 ml-2 space-y-1 border-l-2 border-white/10 pl-3">
                                            <div
                                                v-for="(subject, index) in classItem.subjects"
                                                :key="`${classItem.id}-${index}-${subject}`"
                                                @click="navigateToSubject(classItem, subject)"
                                                class="flex items-center gap-3 px-3 py-1.5 w-full text-left transition-all duration-200 rounded-lg cursor-pointer"
                                                :class="{
                                                    'bg-white/20 text-white shadow-lg backdrop-blur-sm': selectedSubject === subject && selectedClassForSubject?.id === classItem.id,
                                                    'text-white/70 hover:text-white hover:bg-white/10': !(selectedSubject === subject && selectedClassForSubject?.id === classItem.id),
                                                    'opacity-0 h-0 py-0 my-0 overflow-hidden': isCollapsed
                                                }"
                                                :title="`Open ${subject} folder in ${classItem.name}`"
                                            >
                                                <i class="pi pi-folder text-sm" :class="selectedSubject === subject && selectedClassForSubject?.id === classItem.id ? 'text-white' : 'text-white/60'"></i>
                                                <span class="text-sm font-medium flex-1" :class="selectedSubject === subject && selectedClassForSubject?.id === classItem.id ? 'text-white' : ''">{{ subject }}</span>
                                                <div v-if="selectedSubject === subject && selectedClassForSubject?.id === classItem.id" class="ml-auto w-1.5 h-5 rounded-sm bg-white transition-all duration-200"></div>
                                            </div>
                                        </div>
                                    </template>
                                </div>
                            </template>
                        </div>
                    </template>
                </nav>
            </div>

            <!-- Main Content Area -->
            <div class="flex-1 flex flex-col w-full min-h-screen">
                <nav class="bg-white/90 backdrop-blur-sm shadow-md sticky top-0 border-b border-indigo-100 h-[52px] z-50 w-full">
                    <div class="w-full h-full">
                        <div class="flex justify-between items-center px-4 h-full">
                            <!-- Logo -->
                            <div class="flex items-center gap-2">
                                <!-- Modern Logo SVG -->
                                <div class="w-10 h-10">
                                    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" class="w-full h-full">
                                        <defs>
                                            <linearGradient id="headerLogoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                                <stop offset="0%" style="stop-color:#4F46E5;stop-opacity:1" />
                                                <stop offset="100%" style="stop-color:#7C3AED;stop-opacity:1" />
                                            </linearGradient>
                                        </defs>
                                        <g transform="translate(50, 50)">
                                            <!-- D Shape -->
                                            <path d="M -20 -25 L -20 25 Q -20 25, -10 25 L -10 25 Q 5 25, 5 10 L 5 -10 Q 5 -25, -10 -25 Z"
                                                  fill="url(#headerLogoGrad)" opacity="0.9"/>
                                            <!-- P Shape -->
                                            <path d="M 0 -25 L 0 25 M 0 -25 L 15 -25 Q 25 -25, 25 -15 L 25 -5 Q 25 5, 15 5 L 0 5"
                                                  fill="none" stroke="url(#headerLogoGrad)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                                            <!-- Digital Dot -->
                                            <circle cx="0" cy="0" r="3" fill="#06B6D4"/>
                                        </g>
                                    </svg>
                                </div>
                                <div class="flex flex-col leading-tight">
                                    <span class="text-lg font-bold">
                                        <span class="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Digi</span><span class="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Portal</span>
                                    </span>
                                </div>
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
                                        <div class="w-8 h-8 rounded-full overflow-hidden border-2 border-white shadow-sm bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                                            <img
                                                v-if="auth?.user?.profile_picture_url"
                                                :src="auth?.user?.profile_picture_url"
                                                class="w-full h-full object-cover"
                                                :alt="auth?.user?.name"
                                                @error="$event.target.style.display='none'"
                                            />
                                            <span v-if="!auth?.user?.profile_picture_url" class="text-xs font-bold text-white">
                                                {{ (auth?.user?.name || 'U').split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() }}
                                            </span>
                                        </div>
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
                                            <!-- Student/Teacher ID and Grade/Department -->
                                            <div v-if="auth?.user?.role === 'student'" class="mt-2 space-y-1">
                                                <p class="text-xs text-indigo-600">
                                                    <i class="pi pi-id-card mr-1"></i>
                                                    ID: {{ auth?.user?.student_id || auth?.user?.id_number || 'Not assigned' }}
                                                </p>
                                                <p v-if="auth?.user?.grade_level && auth?.user?.section" class="text-xs text-gray-600">
                                                    <i class="pi pi-book mr-1"></i>
                                                    {{ auth?.user?.grade_level }} - {{ auth?.user?.section }}
                                                </p>
                                            </div>
                                            <div v-else-if="auth?.user?.role === 'teacher'" class="mt-2 space-y-1">
                                                <p class="text-xs text-indigo-600">
                                                    <i class="pi pi-id-card mr-1"></i>
                                                    ID: {{ auth?.user?.id_number || 'Not assigned' }}
                                                </p>
                                                <p v-if="auth?.user?.department" class="text-xs text-gray-600">
                                                    <i class="pi pi-briefcase mr-1"></i>
                                                    {{ auth?.user?.department }}
                                                </p>
                                            </div>
                                        </div>

                                        <!-- Menu Items -->
                                        <div class="py-1">
                                            <button
                                                @click="navigateToProfile"
                                                class="flex items-center justify-between w-full text-left text-sm font-medium text-indigo-900 hover:bg-indigo-50 px-4 py-2.5 rounded-lg transition-colors"
                                            >
                                                <i class="pi pi-user text-gray-400"></i>
                                                Profile
                                            </button>
                                            <button
                                                @click="navigateToSettings"
                                                class="flex items-center justify-between w-full text-left text-sm font-medium text-indigo-900 hover:bg-indigo-50 px-4 py-2.5 rounded-lg transition-colors"
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

    <!-- Delete All Notifications Confirmation Dialog -->
    <Dialog v-model:visible="showDeleteAllDialog"
            modal
            header="Delete All Notifications"
            :style="{ width: '90%', maxWidth: '28rem' }">
        <div class="space-y-4">
            <div class="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div class="flex-shrink-0">
                    <i class="pi pi-exclamation-triangle text-2xl text-red-600"></i>
                </div>
                <div>
                    <h3 class="text-lg font-medium text-gray-900">Delete All Notifications?</h3>
                    <p class="mt-1 text-gray-600">
                        Are you sure you want to delete all notifications? This action cannot be undone.
                    </p>
                </div>
            </div>
        </div>
        <template #footer>
            <div class="flex justify-end gap-3">
                <button @click="showDeleteAllDialog = false"
                    class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                    Cancel
                </button>
                <button @click="confirmDeleteAllNotifications"
                    class="px-4 py-2 text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2">
                    <i class="pi pi-trash"></i>
                    Delete All
                </button>
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
