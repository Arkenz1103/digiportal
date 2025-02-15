<script setup>
import { Link, router, usePage } from '@inertiajs/vue3';
import { ref, computed } from 'vue';

// Get user from shared data
const page = usePage();
const auth = computed(() => page.props.auth);

// Sidebar collapse state
const isCollapsed = ref(false);

// Profile dropdown state
const isDropdownOpen = ref(false);

// Toggle sidebar visibility
const toggleSidebar = () => {
    isCollapsed.value = !isCollapsed.value;
};

// Toggle profile dropdown (Only the icon is clickable)
const toggleDropdown = () => {
    isDropdownOpen.value = !isDropdownOpen.value;
};

// Computed property for menu items based on user role
const sideBarItems = computed(() => {
    const commonItems = [
        {
            label: 'Logout',
            icon: 'pi pi-sign-out',
            action: () => {
                router.post(route('logout'));
            }
        }
    ];

    if (!auth.value?.user) {
        return commonItems;
    }

    const roleBasedItems = {
        admin: [
            {
                label: 'Lesson Plans',
                icon: 'pi pi-inbox',
                route: route('admin.lessons'),
                children: [
                    { label: 'Urgent Review', icon: 'pi pi-exclamation-triangle', route: route('admin.lessons', { view: 'urgent' }) },
                    { label: 'Upcoming Review', icon: 'pi pi-calendar', route: route('admin.lessons', { view: 'upcoming' }) },
                    { label: 'Approved Lessons', icon: 'pi pi-check-circle', route: route('admin.lessons', { view: 'approved' }) }
                ]
            },
        ],
        teacher: [
            { label: 'Class', icon: 'pi pi-users', route: route('teacher.class') },
            { label: 'Lesson Plans', icon: 'pi pi-book', route: route('teacher.lessons') },
            { label: 'Calendar', icon: 'pi pi-calendar', route: route('teacher.calendar') },
        ],
        student: [
            { label: 'Dashboard', icon: 'pi pi-th-large', route: route('student.dashboard') },
            { label: 'Class', icon: 'pi pi-users', route: route('student.class') },
            { label: 'Calendar', icon: 'pi pi-calendar', route: route('student.calendar') },
        ]
    };

    return [...(roleBasedItems[auth.value.user.role] || []), ...commonItems];
});
</script>

<template>
    <div class="bg-gray-100">
        <div class="flex">
            <!-- Sidebar -->
            <div :class="['h-screen bg-white shadow-lg sticky top-0 flex flex-col transition-all duration-300', isCollapsed ? 'w-16' : 'w-48']">
                <!-- Sidebar Header -->
                <div class="p-2 border-b flex items-center">
                    <button @click="toggleSidebar" class="p-2 px-4 focus:outline-none">
                        <i class="pi pi-bars text-xl"></i>
                    </button>
                </div>

                <!-- Navigation Section -->
                <nav class="flex-1 overflow-y-auto mt-4">
                    <div v-for="(item, index) in sideBarItems" :key="index" class="px-4 py-2">
                        <Link v-if="item.route" :href="item.route"
                              class="flex items-center text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg p-2 transition-colors duration-200">
                            <i :class="item.icon" class="text-lg"></i>
                            <span v-show="!isCollapsed" class="ml-3 text-[0.875rem] font-medium">{{ item.label }}</span> 
                        </Link>

                        <button v-else-if="item.children" class="flex items-center text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg p-2 transition-colors duration-200">
                            <i :class="item.icon" class="text-lg"></i>
                            <span v-show="!isCollapsed" class="ml-3 text-[0.875rem] font-medium">{{ item.label }}</span>
                            <i v-show="!isCollapsed" class="pi pi-angle-down ml-auto"></i>
                        </button>

                        <!-- Logout Button (Fixed Hover Effect) -->
                        <button v-else @click="item.action"
                                class="flex items-center w-full text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg p-2 transition-colors duration-200">
                            <i :class="item.icon" class="text-lg"></i>
                            <span v-show="!isCollapsed" class="ml-3 text-[0.875rem] font-medium">{{ item.label }}</span>
                        </button>
                    </div>
                </nav>
            </div>

            <!-- Main Content Area -->
            <div class="flex-1">
                <!-- Top Navigation Bar -->
                <nav class="bg-white shadow-md sticky top-0 z-50">
                    <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
                        <div class="flex justify-between py-1 items-center">
                            <!-- Logo (Always Visible) -->
                            <div class="flex items-center space-x-3">
                                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlC4Z2-qQHdn_TKc6z-SJGsVH1_hJB4iu4DA&s"
                                    alt="Eduboard Logo" class="h-8 w-8 rounded-full">
                                <span class="text-lg font-bold">EduBoard</span>
                            </div>

                            <!-- Right Navigation -->
                            <div class="flex items-center space-x-4">
                                <!-- Notifications -->
                                <button class="text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                    <span class="sr-only">View notifications</span>
                                    <i class="pi pi-bell text-xl"></i>
                                </button>

                                <!-- Profile & Dropdown Icon -->
                                <div class="relative flex items-center" v-if="auth?.user">
                                    <img
                                        class="h-8 w-8 rounded-full object-cover"
                                        src="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png"
                                        alt="Profile Picture"
                                    />

                                    <div class="ml-3">
                                        <div class="text-base font-medium text-gray-800">{{ auth.user.name }}</div>
                                        <div class="text-sm font-medium text-gray-500 capitalize">{{ auth.user.role }}</div>
                                    </div>

                                     <!-- Dropdown Icon (Clickable) -->
                                    <i @click="toggleDropdown" class="pi pi-angle-down text-gray-600 cursor-pointer px-4"></i>

                                    <!-- Dropdown Menu -->
                                    <div v-if="isDropdownOpen" class="absolute left-8 mt-24 w-28 bg-white rounded-md shadow-lg z-50">
                                        <ul class="py-0.5 text-gray-700">
                                            <li>
                                                <Link :href="route('profile')" class="block px-4 py-2 hover:bg-gray-100">
                                                    <i class="pi pi-user mr-2"></i> Profile
                                                </Link>
                                            </li>
                                        </ul>
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
</template>

<style scoped>
.collapsed {
    width: 4rem; /* Adjust sidebar width when collapsed */
}
</style>