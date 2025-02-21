    <template>
    <div class="p-6 bg-white rounded-lg shadow-md">
        <h2 class="text-3xl font-bold mb-6 text-gray-800">Notifications</h2>

        <!-- Tabs -->
        <div class="flex space-x-4 border-b mb-4">
        <button
            class="pb-2 px-4 border-b-2"
            :class="activeTab === 'all' ? 'border-blue-500 text-blue-500 font-semibold' : 'text-gray-500'"
            @click="activeTab = 'all'"
        >
            All
        </button>
        <button
            class="pb-2 px-4 border-b-2"
            :class="activeTab === 'new' ? 'border-blue-500 text-blue-500 font-semibold' : 'text-gray-500'"
            @click="activeTab = 'new'"
        >
            New
        </button>
        <button
            class="pb-2 px-4 border-b-2"
            :class="activeTab === 'unread' ? 'border-blue-500 text-blue-500 font-semibold' : 'text-gray-500'"
            @click="activeTab = 'unread'"
        >
            Unread
        </button>
        </div>

        <!-- Notification List -->
        <div class="space-y-4">
        <div
            v-for="notification in filteredNotifications"
            :key="notification.id"
            class="flex items-center justify-between p-4 rounded-lg shadow-sm border-l-4 transition-all duration-200"
            :class="[
            notification.isUnread ? 'bg-blue-100 border-blue-500' : 'bg-gray-100 border-gray-300',
            'hover:bg-gray-200'
            ]"
        >
            <!-- Icon & Content -->
            <div class="flex items-center space-x-3">
            <div
                class="w-10 h-10 flex items-center justify-center rounded-full"
                :class="notification.type === 'meeting' ? 'bg-green-500' : 'bg-blue-500'"
            >
                <i class="text-white text-xl" :class="notification.icon"></i>
            </div>
            <div>
                <p class="text-gray-800 font-semibold">{{ notification.title }}</p>
                <p class="text-gray-600 text-sm">{{ notification.message }}</p>
                <p class="text-gray-400 text-xs mt-1">{{ formatDate(notification.date) }}</p>
            </div>
            </div>

            <!-- Dismiss Button -->
            <button
            @click="dismissNotification(notification.id)"
            class="text-red-500 hover:text-red-700"
            >
            Dismiss
            </button>
        </div>

        <!-- No Notifications Message -->
        <p v-if="filteredNotifications.length === 0" class="text-gray-500 text-center">
            No notifications available.
        </p>
        </div>
    </div>
    </template>

    <script>
    export default {
    data() {
        return {
        activeTab: "all",
        notifications: [
            {
            id: 1,
            type: "meeting",
            icon: "fas fa-video",
            title: "Upcoming Meeting",
            message: "You have a tutoring session tomorrow at 10:00 AM.",
            date: new Date(),
            isNew: true,
            isUnread: true, // Unread notification
            },
            {
            id: 2,
            type: "student",
            icon: "fas fa-user-plus",
            title: "New Student Assigned",
            message: "John Doe has been assigned to you for tutoring.",
            date: new Date("2025-02-18"),
            isNew: true,
            isUnread: false, // Read notification
            },
            {
            id: 3,
            type: "meeting",
            icon: "fas fa-video",
            title: "Upcoming Meeting",
            message: "You have a tutoring session on February 25 at 2:00 PM.",
            date: new Date("2025-02-25"),
            isNew: false,
            isUnread: true, // Unread notification
            },
        ],
        };
    },
    computed: {
        filteredNotifications() {
        if (this.activeTab === "new") {
            return this.notifications.filter((n) => n.isNew);
        }
        if (this.activeTab === "unread") {
            return this.notifications.filter((n) => n.isUnread);
        }
        return this.notifications;
        },
    },
    methods: {
        formatDate(date) {
        return new Intl.DateTimeFormat("en-US", {
            dateStyle: "medium",
            timeStyle: "short",
        }).format(new Date(date));
        },
        dismissNotification(id) {
        this.notifications = this.notifications.filter((n) => n.id !== id);
        },
    },
    };
    </script>

    <style>
    /* FontAwesome Icons */
    @import "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css";
    </style>
