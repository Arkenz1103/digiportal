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
                label: 'Dashboard',
                icon: 'pi pi-th-large',
                route: route('admin.dashboard')
            },
            {
                label: 'Class',
                icon: 'pi pi-book',
                route: route('admin.classes')
            },
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
                label: 'Dashboard',
                icon: 'pi pi-th-large',
                route: route('teacher.dashboard')
            },
            {
                label: 'Lesson Plan',
                icon: 'pi pi-inbox',
                route: route('teacher.lessons')
            },
            {
                label: 'Class',
                icon: 'pi pi-users',
                route: route('teacher.class')
            },
            {
                label: 'Calendar',
                icon: 'pi pi-calendar',
                route: route('teacher.calendar')
            },
        ],
        student: [
            {
                label: 'Dashboard',
                icon: 'pi pi-th-large',
                route: route('student.dashboard')
            },
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
     <div class="p-4 border-b">
        <div class="flex items-center">
            <img src="https://scontent.fmnl13-4.fna.fbcdn.net/v/t39.30808-6/368255360_324082253303069_319860159441260390_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeEeeZOV62u2x4mCX5FuSl2wJArEhEwobZUkCsSETChtlSadu9mg9xY6wtY1RoAhwpXAtpuI0SMtLSKiUSUzf-yu&_nc_ohc=ubF5iKQIDtUQ7kNvgEZt1Zt&_nc_zt=23&_nc_ht=scontent.fmnl13-4.fna&_nc_gid=AvtJ5qeJYzczZsKMH7NwsX-&oh=00_AYD4Mk_MKvBv0VUAMpE1RImZfJgXNyCrwS6Ez5c6F0D3HA&oe=67631DF4"
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
        <div class="flex justify-between h-16">
            <!-- Search Bar -->
            <div class="flex-1 flex items-center">
                <div class="max-w-lg w-full lg:max-w-xs">
                    <label for="search" class="sr-only">Search</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i class="pi pi-search text-gray-400"></i>
                        </div>
                        <input id="search" class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 sm:text-sm" placeholder="Search" type="search">
                    </div>
                </div>
            </div>

            <!-- Right Navigation -->
            <div class="flex items-center">
                <!-- Notifications -->
                <button class="p-2 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    <span class="sr-only">View notifications</span>
                    <i class="pi pi-bell text-xl"></i>
                </button>

                     <!-- Profile dropdown -->
                      <div class="ml-4 relative flex items-center">
                      <div class="flex items-center" v-if="auth?.user">
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
