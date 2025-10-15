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
              <div class="p-4 flex items-start justify-between gap-4 hover:bg-[#F2FDFF] transition-colors">
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

                <!-- Actions -->
                <div class="flex items-center gap-2">
                  <button v-if="notification.isUnread"
                    @click="markAsRead(notification.id)"
                    class="p-2 text-[#0E1836] hover:bg-[#B6CFFF]/30 rounded-lg transition-colors">
                    <i class="pi pi-check"></i>
                  </button>
                  <button
                    @click="dismissNotification(notification.id)"
                    class="p-2 text-[#0E1836] hover:bg-[#B6CFFF]/30 rounded-lg transition-colors">
                    <i class="pi pi-trash"></i>
                  </button>
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

const activeTab = ref('all');
const notifications = ref([
  {
    id: 1,
    type: 'output',
    title: 'Post Approval Request',
    message: 'Alice Smith is requesting approval to post "Math Exercise 3" for Grade 1 - A',
    date: new Date(),
    isNew: true,
    isUnread: true,
  },
  {
    id: 2,
    type: 'output',
    title: 'Post Approval Request',
    message: 'Bob Johnson is requesting approval to post "Science Project" for Grade 2 - A',
    date: new Date('2024-02-18 14:30'),
    isNew: true,
    isUnread: true,
  },
  {
    id: 3,
    type: 'output',
    title: 'Post Approval Request',
    message: 'Emma Davies is requesting approval to post "English Essay" for Grade 3 - A',
    date: new Date('2024-02-18 09:15'),
    isNew: true,
    isUnread: false,
  },
  {
    id: 4,
    type: 'output',
    title: 'Post Approval Request',
    message: 'Carol Williams is requesting approval to post "History Timeline" for Grade 1 - A',
    date: new Date('2024-02-17 16:45'),
    isNew: false,
    isUnread: true,
  },
  {
    id: 5,
    type: 'output',
    title: 'Post Approval Request',
    message: 'David Brown is requesting approval to post "Geography Map" for Grade 2 - A',
    date: new Date('2024-02-17 11:20'),
    isNew: false,
    isUnread: true,
  },
  {
    id: 6,
    type: 'output',
    title: 'Post Approval Request',
    message: 'Frank Miller is requesting approval to post "Art Project" for Grade 3 - A',
    date: new Date('2024-02-17 10:00'),
    isNew: false,
    isUnread: false,
  },
  {
    id: 7,
    type: 'output',
    title: 'Post Approval Request',
    message: 'Grace Taylor is requesting approval to post "Music Composition" for Grade 1 - A',
    date: new Date('2024-02-16 15:30'),
    isNew: false,
    isUnread: false,
  },
  {
    id: 8,
    type: 'output',
    title: 'Post Approval Request',
    message: 'Henry Wilson is requesting approval to post "Physical Education Activity" for Grade 2 - A',
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