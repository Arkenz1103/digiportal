<template>
  <div class="p-6 max-w-7xl mx-auto">
    <div class="bg-white rounded-lg shadow-lg">
      <!-- Header -->
      <div class="bg-[#B8AAFF] p-6">
        <h1 class="text-2xl font-bold text-white">Notifications</h1>
      </div>

      <!-- Tabs -->
      <div class="p-6">
        <div class="flex space-x-4 mb-6">
          <button
            v-for="tab in ['all', 'new', 'unread']"
            :key="tab"
            @click="activeTab = tab"
            class="px-6 py-2.5 rounded-xl transition-all duration-200 flex items-center gap-2"
            :class="[
              activeTab === tab 
                ? 'bg-[#B6CFFF]/30 text-[#0E1836] font-semibold shadow-sm' 
                : 'text-[#0E1836] hover:bg-[#B8AAFF]/10'
            ]"
          >
            <i :class="[
              'pi',
              {
                'pi-bell': tab === 'all',
                'pi-star': tab === 'new',
                'pi-envelope': tab === 'unread'
              }
            ]"></i>
            <span class="capitalize">{{ tab }}</span>
            <span v-if="tab !== 'all'" 
                  class="ml-1 px-2 py-0.5 text-xs rounded-full"
                  :class="[
                    tab === 'new' ? 'bg-[#7BBBFE] text-white' : 'bg-[#B6CFFF] text-[#0E1836]'
                  ]">
              {{ tab === 'new' ? notifications.filter(n => n.isNew).length : notifications.filter(n => n.isUnread).length }}
            </span>
          </button>
        </div>

        <!-- Notification List -->
        <div class="space-y-4">
          <TransitionGroup name="list">
            <div
              v-for="notification in filteredNotifications"
              :key="notification.id"
              class="bg-white rounded-xl border transition-all duration-200 hover:shadow-md"
              :class="[
                notification.isUnread ? 'border-blue-200 bg-blue-50' : 'border-gray-200'
              ]"
            >
              <div class="p-4 flex items-start gap-4 cursor-pointer hover:bg-[#F2FDFF] transition-colors" @click="markAsRead(notification.id)">
                <!-- Icon -->
                <div
                  class="w-12 h-12 flex-shrink-0 flex items-center justify-center rounded-full shadow-sm"
                  :class="[
                    `bg-gradient-to-br ${getNotificationColor(notification.type)}`
                  ]"
                >
                  <i class="pi text-xl text-white"
                    :class="getNotificationIcon(notification.type)"
                  ></i>
                </div>
                
                <!-- Content -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2">
                    <h3 class="font-semibold text-gray-900">{{ notification.title }}</h3>
                    <span v-if="notification.isNew" 
                          class="px-2 py-0.5 bg-[#7BBBFE] text-white text-xs rounded-full">
                      New
                    </span>
                  </div>
                  <p class="text-gray-600 mt-1">{{ notification.message }}</p>
                  <div class="flex items-center gap-2 mt-2 text-sm text-gray-500">
                    <i class="pi pi-clock"></i>
                    <span>{{ formatDate(notification.date) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </TransitionGroup>

          <!-- Empty State -->
          <div v-if="filteredNotifications.length === 0" 
               class="text-center py-12 bg-[#F2FDFF] rounded-xl border-2 border-dashed border-[#B6CFFF]">
            <div class="w-16 h-16 mx-auto mb-4 bg-[#B6CFFF] rounded-full flex items-center justify-center">
              <i class="pi pi-bell text-white text-2xl"></i>
            </div>
            <h3 class="text-[#0E1836] font-medium">No notifications</h3>
            <p class="text-[#0E1836]/80 text-sm mt-1">You're all caught up!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Mock user data for notifications
const currentUser = ref({
    name: 'Student Name',
    email: 'student@example.com',
    role: 'student'
});

const auth = computed(() => ({
    user: currentUser.value
}));
const activeTab = ref('all');

// Sample notifications data - in a real app, this would come from your backend
const notifications = ref([
  {
    id: 1,
    type: 'output',
    title: 'Output Approved',
    message: 'Your "Math Exercise 3" has been approved by your teacher',
    date: new Date(),
    isNew: true,
    isUnread: true,
  },
  {
    id: 2,
    type: 'remark',
    title: 'New Remark Added',
    message: 'Your teacher added a positive remark on your performance',
    date: new Date('2024-02-18 14:30'),
    isNew: true,
    isUnread: true,
  },
  {
    id: 3,
    type: 'output',
    title: 'Output Graded',
    message: 'Your "English Essay" has been graded as Excellent',
    date: new Date('2024-02-18 09:15'),
    isNew: false,
    isUnread: false,
  },
  {
    id: 4,
    type: 'schedule',
    title: 'New Assignment Posted',
    message: 'A new assignment "Science Project" has been posted',
    date: new Date('2024-02-17 16:45'),
    isNew: false,
    isUnread: true,
  },
  {
    id: 5,
    type: 'output',
    title: 'Grade Updated',
    message: 'Your grade for "Math Quiz 2" has been updated',
    date: new Date('2024-02-17 11:20'),
    isNew: false,
    isUnread: true,
  },
  {
    id: 6,
    type: 'remark',
    title: 'Teacher Feedback',
    message: 'Your teacher provided feedback on your recent submission',
    date: new Date('2024-02-16 15:30'),
    isNew: false,
    isUnread: false,
  },
  {
    id: 7,
    type: 'schedule',
    title: 'Class Reminder',
    message: 'Your next class starts in 30 minutes',
    date: new Date('2024-02-16 10:45'),
    isNew: false,
    isUnread: false,
  }
]);

const getNotificationIcon = (type) => {
  switch (type) {
    case 'output':
      return 'pi-file-edit';
    case 'remark':
      return 'pi-comments';
    case 'schedule':
      return 'pi-calendar';
    default:
      return 'pi-bell';
  }
};

const getNotificationColor = (type) => {
  switch (type) {
    case 'output':
      return 'from-[#7BBBFE] to-[#7BBBFE]';
    case 'remark':
      return 'from-[#B8AAFF] to-[#B8AAFF]';
    case 'schedule':
      return 'from-[#7BBBFE] to-[#7BBBFE]';
    default:
      return 'from-[#B6CFFF] to-[#B6CFFF]';
  }
};

const filteredNotifications = computed(() => {
  if (activeTab.value === 'new') {
    return notifications.value.filter((n) => n.isNew);
  } else if (activeTab.value === 'unread') {
    return notifications.value.filter((n) => n.isUnread);
  }
  return notifications.value;
});

const formatDate = (date) => {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(date));
};

const dismissNotification = (id) => {
  notifications.value = notifications.value.filter((n) => n.id !== id);
};

const markAsRead = (id) => {
  const notification = notifications.value.find((n) => n.id === id);
  if (notification) {
    notification.isUnread = false;
    notification.isNew = false;
  }
};
</script>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.list-move {
  transition: transform 0.3s ease;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>