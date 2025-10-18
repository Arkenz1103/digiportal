<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 p-6">
    <div class="max-w-5xl mx-auto">
      <!-- Header Card -->
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden mb-6">
        <div class="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 p-8">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold text-white mb-2 flex items-center gap-3">
                <i class="pi pi-bell"></i>
                Notifications
              </h1>
              <p class="text-indigo-100">Stay updated with your latest activities</p>
            </div>
            <div class="bg-white/20 backdrop-blur-sm rounded-2xl px-6 py-4 text-center">
              <div class="text-3xl font-bold text-white">{{ notifications.filter(n => n.isUnread).length }}</div>
              <div class="text-sm text-indigo-100">Unread</div>
            </div>
          </div>
        </div>

        <!-- Tabs -->
        <div class="p-6 bg-white border-b border-gray-100">
          <div class="flex flex-wrap gap-3">
            <button
              v-for="tab in ['all', 'new', 'unread']"
              :key="tab"
              @click="activeTab = tab"
              class="group relative px-6 py-3 rounded-xl transition-all duration-300 flex items-center gap-2.5 font-medium"
              :class="[
                activeTab === tab 
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-200 scale-105' 
                  : 'bg-gray-50 text-gray-600 hover:bg-gray-100 hover:scale-105'
              ]"
            >
              <i :class="[
                'pi text-lg transition-transform duration-300',
                {
                  'pi-bell': tab === 'all',
                  'pi-star': tab === 'new',
                  'pi-envelope': tab === 'unread'
                },
                activeTab === tab ? 'scale-110' : 'group-hover:scale-110'
              ]"></i>
              <span class="capitalize">{{ tab }}</span>
              <span v-if="tab !== 'all' && (tab === 'new' ? notifications.filter(n => n.isNew).length : notifications.filter(n => n.isUnread).length) > 0" 
                    class="ml-1 px-2.5 py-0.5 text-xs font-bold rounded-full animate-pulse"
                    :class="[
                      activeTab === tab 
                        ? 'bg-white/30 text-white' 
                        : tab === 'new' ? 'bg-indigo-100 text-indigo-600' : 'bg-purple-100 text-purple-600'
                    ]">
                {{ tab === 'new' ? notifications.filter(n => n.isNew).length : notifications.filter(n => n.isUnread).length }}
              </span>
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="p-12">
          <div class="flex flex-col items-center justify-center">
            <div class="relative">
              <div class="animate-spin rounded-full h-16 w-16 border-4 border-indigo-200"></div>
              <div class="animate-spin rounded-full h-16 w-16 border-4 border-t-indigo-600 absolute top-0 left-0"></div>
            </div>
            <p class="text-gray-600 mt-6 font-medium">Loading notifications...</p>
          </div>
        </div>

        <!-- Notification List -->
        <div v-else class="p-6">
          <TransitionGroup name="list" tag="div" class="space-y-4">
            <div
              v-for="notification in filteredNotifications"
              :key="notification.id"
              class="group relative bg-white rounded-2xl border-2 transition-all duration-300 hover:shadow-2xl hover:scale-[1.02] cursor-pointer overflow-hidden"
              :class="[
                notification.isUnread 
                  ? 'border-indigo-200 bg-gradient-to-r from-indigo-50 to-purple-50' 
                  : 'border-gray-200 hover:border-indigo-200'
              ]"
              @click="markAsRead(notification.id)"
            >
              <!-- Unread Indicator -->
              <div v-if="notification.isUnread" class="absolute top-0 left-0 w-1.5 h-full bg-gradient-to-b from-indigo-600 to-purple-600"></div>
              
              <div class="p-5 flex items-start gap-5">
                <!-- Icon -->
                <div class="relative">
                  <div
                    class="w-14 h-14 flex-shrink-0 flex items-center justify-center rounded-2xl shadow-lg transition-transform duration-300 group-hover:scale-110 group-hover:rotate-6"
                    :class="[
                      `bg-gradient-to-br ${getNotificationColor(notification.type)}`
                    ]"
                  >
                    <i class="pi text-2xl text-white"
                      :class="getNotificationIcon(notification.type)"
                    ></i>
                  </div>
                  <div v-if="notification.isNew" class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full border-2 border-white animate-pulse"></div>
                </div>
                
                <!-- Content -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-start justify-between gap-3 mb-2">
                    <div class="flex items-center gap-2 flex-wrap">
                      <h3 class="font-bold text-gray-900 text-lg">{{ notification.title }}</h3>
                      <span v-if="notification.isNew" 
                            class="px-3 py-1 bg-gradient-to-r from-red-500 to-pink-500 text-white text-xs font-bold rounded-full shadow-md animate-pulse">
                        NEW
                      </span>
                    </div>
                    <button 
                      @click.stop="dismissNotification(notification.id)"
                      class="opacity-0 group-hover:opacity-100 transition-opacity p-2 hover:bg-red-50 rounded-lg"
                    >
                      <i class="pi pi-times text-gray-400 hover:text-red-500"></i>
                    </button>
                  </div>
                  
                  <p class="text-gray-700 leading-relaxed mb-3">{{ notification.message }}</p>
                  
                  <div class="flex items-center gap-4 text-sm">
                    <div class="flex items-center gap-2 text-gray-500">
                      <i class="pi pi-clock"></i>
                      <span class="font-medium">{{ formatDate(notification.date) }}</span>
                    </div>
                    <div v-if="notification.isUnread" class="flex items-center gap-2 text-indigo-600">
                      <div class="w-2 h-2 bg-indigo-600 rounded-full animate-pulse"></div>
                      <span class="font-semibold">Unread</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Hover Effect Border -->
              <div class="absolute inset-0 border-2 border-transparent group-hover:border-indigo-400 rounded-2xl transition-colors duration-300 pointer-events-none"></div>
            </div>
          </TransitionGroup>

          <!-- Empty State -->
          <div v-if="filteredNotifications.length === 0" 
               class="text-center py-16 bg-gradient-to-br from-gray-50 to-indigo-50 rounded-2xl border-2 border-dashed border-indigo-200">
            <div class="relative inline-block mb-6">
              <div class="w-24 h-24 mx-auto bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full flex items-center justify-center shadow-xl">
                <i class="pi pi-bell text-white text-4xl"></i>
              </div>
              <div class="absolute -top-2 -right-2 w-8 h-8 bg-green-500 rounded-full border-4 border-white flex items-center justify-center">
                <i class="pi pi-check text-white text-sm"></i>
              </div>
            </div>
            <h3 class="text-gray-900 font-bold text-xl mb-2">All Caught Up!</h3>
            <p class="text-gray-600 max-w-md mx-auto">You have no {{ activeTab === 'all' ? '' : activeTab }} notifications. Great job staying on top of things!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

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
const isLoading = ref(false);

// Notifications data from backend
const notifications = ref([]);

// Load notifications from backend
const loadNotifications = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get('/api/notifications/');
    if (response.data) {
      notifications.value = response.data.map(notif => ({
        id: notif.id,
        type: notif.notification_type,
        title: notif.title,
        message: notif.message,
        date: new Date(notif.created_at),
        isNew: !notif.is_read,
        isUnread: !notif.is_read,
      }));
      console.log('✅ Loaded notifications:', notifications.value.length);
    }
  } catch (error) {
    console.error('❌ Error loading notifications:', error);
  } finally {
    isLoading.value = false;
  }
};

// Load notifications on mount
onMounted(() => {
  loadNotifications();
  
  // Refresh every 30 seconds
  setInterval(loadNotifications, 30000);
});

const getNotificationIcon = (type) => {
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
    'portfolio_created': 'from-green-400 to-green-500',
    'portfolio_updated': 'from-blue-400 to-blue-500',
    'portfolio_deleted': 'from-red-400 to-red-500',
    'activity_created': 'from-[#7BBBFE] to-[#7BBBFE]',
    'activity_updated': 'from-blue-400 to-blue-500',
    'activity_deleted': 'from-red-400 to-red-500',
    'submission_approved': 'from-green-400 to-green-500',
    'submission_rejected': 'from-red-400 to-red-500',
    'score_added': 'from-yellow-400 to-yellow-500',
    'submission_received': 'from-[#7BBBFE] to-[#7BBBFE]',
    'approval_requested': 'from-[#B8AAFF] to-[#B8AAFF]',
  };
  return colorMap[type] || 'from-[#B6CFFF] to-[#B6CFFF]';
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

const markAsRead = async (id) => {
  try {
    const response = await axios.put('/api/notifications/', {
      notification_id: id
    });
    
    if (response.status === 200) {
      const notification = notifications.value.find((n) => n.id === id);
      if (notification) {
        notification.isUnread = false;
        notification.isNew = false;
      }
    }
  } catch (error) {
    console.error('Error marking notification as read:', error);
  }
};
</script>

<style scoped>
/* Enhanced List Animations */
.list-enter-active {
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.list-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 1, 1);
}

.list-enter-from {
  opacity: 0;
  transform: translateX(50px) scale(0.9);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(-50px) scale(0.9);
}

.list-move {
  transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Gradient Animation */
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

/* Pulse Animation for Badges */
@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.7);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(99, 102, 241, 0);
  }
}

/* Shimmer Effect */
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.shimmer {
  animation: shimmer 2s infinite;
  background: linear-gradient(
    to right,
    transparent 0%,
    rgba(255, 255, 255, 0.3) 50%,
    transparent 100%
  );
  background-size: 1000px 100%;
}

/* Smooth Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #6366f1, #8b5cf6);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #4f46e5, #7c3aed);
}
</style>