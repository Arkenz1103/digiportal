<template>
  <div class="p-6 max-w-7xl mx-auto">
    <div class="bg-white rounded-lg shadow-lg">
      <!-- Header -->
      <div class="border-b p-6">
        <h1 class="text-2xl font-bold text-gray-900">Notifications</h1>
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
                ? 'bg-blue-50 text-blue-600 font-semibold shadow-sm' 
                : 'text-gray-600 hover:bg-gray-50'
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
                    tab === 'new' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'
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
              <div class="p-4 flex items-start justify-between gap-4">
                <!-- Icon & Content -->
                <div class="flex items-start gap-4">
                  <div
                    class="w-12 h-12 flex items-center justify-center rounded-full shadow-sm"
                    :class="[
                      `bg-gradient-to-br ${getNotificationColor(notification.type)}`
                    ]"
                  >
                    <i class="pi text-xl text-white"
                      :class="getNotificationIcon(notification.type)"
                    ></i>
                  </div>
                  <div>
                    <div class="flex items-center gap-2">
                      <h3 class="font-semibold text-gray-900">{{ notification.title }}</h3>
                      <span v-if="notification.isNew" 
                            class="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">
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

                <!-- Actions -->
                <div class="flex items-center gap-2">
                  <button v-if="notification.isUnread"
                    @click="markAsRead(notification.id)"
                    class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                    <i class="pi pi-check"></i>
                  </button>
                  <button
                    @click="dismissNotification(notification.id)"
                    class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                    <i class="pi pi-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </TransitionGroup>

          <!-- Empty State -->
          <div v-if="filteredNotifications.length === 0" 
               class="text-center py-12 bg-gray-50 rounded-xl border border-dashed border-gray-300">
            <div class="w-16 h-16 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
              <i class="pi pi-bell text-gray-400 text-2xl"></i>
            </div>
            <h3 class="text-gray-600 font-medium">No notifications</h3>
            <p class="text-gray-500 text-sm mt-1">You're all caught up!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const activeTab = ref('all');
const notifications = ref([
  {
    id: 1,
    type: 'output',
    title: 'New Student Output',
    message: 'Alice Smith has submitted "Math Exercise 3" for Grade 1 - Section A',
    date: new Date(),
    isNew: true,
    isUnread: true,
  },
  {
    id: 2,
    type: 'remark',
    title: 'New Remark Added',
    message: 'You added a behavioral remark for Bob Johnson in Grade 1 - Section B',
    date: new Date('2024-02-18 14:30'),
    isNew: true,
    isUnread: true,
  },
  {
    id: 3,
    type: 'schedule',
    title: 'Schedule Change',
    message: 'Class schedule for Grade 2 - Section A has been updated to 1:30 PM - 3:30 PM',
    date: new Date('2024-02-18 09:15'),
    isNew: true,
    isUnread: false,
  },
  {
    id: 4,
    type: 'output',
    title: 'Missing Output',
    message: 'Carol Williams has not submitted "Science Project" due yesterday',
    date: new Date('2024-02-17 16:45'),
    isNew: false,
    isUnread: true,
  },
  {
    id: 5,
    type: 'remark',
    title: 'Remark Update',
    message: 'Academic remark for David Brown has been updated',
    date: new Date('2024-02-17 11:20'),
    isNew: false,
    isUnread: true,
  },
  {
    id: 6,
    type: 'schedule',
    title: 'Upcoming Class',
    message: 'Reminder: Grade 3 - Section B class starts in 30 minutes',
    date: new Date('2024-02-17 10:00'),
    isNew: false,
    isUnread: false,
  },
  {
    id: 7,
    type: 'output',
    title: 'Output Graded',
    message: 'You have graded Emma Davies\'s "English Essay" as Excellent',
    date: new Date('2024-02-16 15:30'),
    isNew: false,
    isUnread: false,
  },
  {
    id: 8,
    type: 'remark',
    title: 'Multiple Remarks',
    message: '3 new remarks have been added for Grade 1 - Section A students',
    date: new Date('2024-02-16 13:45'),
    isNew: false,
    isUnread: true,
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
      return 'from-blue-500 to-blue-600';
    case 'remark':
      return 'from-purple-500 to-purple-600';
    case 'schedule':
      return 'from-green-500 to-green-600';
    default:
      return 'from-gray-500 to-gray-600';
  }
};

const filteredNotifications = computed(() => {
  if (activeTab.value === 'new') {
    return notifications.value.filter((n) => n.isNew);
  }
  if (activeTab.value === 'unread') {
    return notifications.value.filter((n) => n.isUnread);
  }
  return notifications.value;
});

function formatDate(date) {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(date));
}

function dismissNotification(id) {
  notifications.value = notifications.value.filter((n) => n.id !== id);
}

function markAsRead(id) {
  const notification = notifications.value.find(n => n.id === id);
  if (notification) {
    notification.isUnread = false;
  }
}
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

.bg-gradient-to-r {
  background-size: 200% 200%;
  animation: gradient 15s ease infinite;
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
