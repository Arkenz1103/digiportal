<script setup>
import { Link, router, usePage } from '@inertiajs/vue3';
import { ref, computed } from 'vue';

// Get user from shared data
const page = usePage();
const auth = computed(() => page.props.auth);

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
                route: route('admin.lessons', { view: 'urgent_and_upcoming' }),
                children: [
                    {
                        label: 'Urgent Review',
                        icon: 'pi pi-exclamation-triangle',
                        route: route('admin.lessons', { view: 'urgent' })
                    },
                    {
                        label: 'Upcoming Review',
                        icon: 'pi pi-calendar',
                        route: route('admin.lessons', { view: 'upcoming' })
                    },
                    {
                        label: 'Approved Lessons',
                        icon: 'pi pi-check-circle',
                        route: route('admin.lessons', { view: 'approved' })
                    }
                ]
            },
        ],
        teacher: [
            {
                label: 'Class',
                icon: 'pi pi-users',
                route: route('teacher.class')
            },
            {
                label: 'Lesson Plan',
                icon: 'pi pi-file-edit',
                route: route('teacher.lessons')
            },
            {
                label: 'Calendar',
                icon: 'pi pi-calendar',
                route: route('teacher.calendar')
            },
        ],
        student: [
            {
                label: 'Class',
                icon: 'pi pi-users',
                route: route('student.classes')
            },
            {
                label: 'Calendar',
                icon: 'pi pi-calendar',
                route: route('student.calendar')
            },
        ]
    };

    return [...(roleBasedItems[auth.value.user.role] || []), ...commonItems];
});
</script>

<template>
    <div class="bg-gray-100">
        <div class="flex">
            <!-- Sidebar -->
      <div class="w-64 h-screen bg-white shadow-lg sticky top-0 flex flex-col">
     <!-- Logo Section -->
     <div class="p-2 border-b">
        <div class="flex items-center">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlC4Z2-qQHdn_TKc6z-SJGsVH1_hJB4iu4DA&s"
                 alt="Eduboard Logo" class="h-12 w-12 mr-3 rounded-full">
            <span class="text-xl font-bold">EDUBOARD</span>
        </div>
    </div>

    <!-- Navigation Section -->
    <nav class="flex-1 overflow-y-auto mt-4">
        <div v-for="(item, index) in sideBarItems" :key="index" class="px-4 py-2">
            <Link v-if="item.route" :href="item.route"
                  class="flex items-center text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg p-2 transition-colors duration-200">
                <i :class="item.icon" class="mr-3 text-lg"></i>
                <span class="text-sm font-medium">{{ item.label }}</span>
            </Link>
            <button v-else-if="item.children" class="flex items-center text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg p-2 transition-colors duration-200">
                <i :class="item.icon" class="mr-3 text-lg"></i>
                <span class="text-sm font-medium">{{ item.label }}</span>
                <i class="pi pi-angle-down ml-auto"></i>
            </button>
            <button v-else @click="item.action" class="flex items-center text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg p-2 transition-colors duration-200">
                <i :class="item.icon" class="mr-3 text-lg"></i>
                <span class="text-sm font-medium">{{ item.label }}</span>
            </button>
            <div v-if="item.children" class="ml-4 mt-2">
                <Link v-for="(child, childIndex) in item.children" :key="childIndex" :href="child.route"
                      class="flex items-center text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg p-2 transition-colors duration-200">
                    <i :class="child.icon" class="mr-3 text-lg"></i>
                    <span class="text-sm font-medium">{{ child.label }}</span>
                </Link>
            </div>
        </div>
    </nav>
 </div>


            <!-- Main Content Area -->
            <div class="flex-1">
               <!-- Top Navigation Bar -->
<nav class="bg-white shadow-md sticky top-0 z-50">
    <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
            <!-- Left side (empty for now, can add breadcrumbs or page title later) -->
            <div class="flex-1"></div>

            <!-- Right Navigation -->
            <div class="flex items-center space-x-4">
                <!-- Notifications -->
                <button class="text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    <span class="sr-only">View notifications</span>
                    <i class="pi pi-bell text-xl"></i>
                </button>

                <!-- Profile dropdown -->
                <div class="relative flex items-center" v-if="auth?.user">
                    <Link :href="route('profile')">
                        <img
                            class="h-8 w-8 rounded-full object-cover cursor-pointer"
                            src="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png"
                            alt="Profile Picture"
                        />
                    </Link>
                    <div class="ml-3">
                        <div class="text-base font-medium text-gray-800">{{ auth.user.name }}</div>
                        <div class="text-sm font-medium text-gray-500 capitalize">{{ auth.user.role }}</div>
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
.nav-link {
    @apply px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50;
}
</style>
