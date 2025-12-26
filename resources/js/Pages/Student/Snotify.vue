<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 p-6">
    <div class="max-w-5xl mx-auto">
      <!-- Header Card -->
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden mb-6">
        <div class="bg-gradient-to-r from-blue-600 to-blue-700 p-8">
          <div class="flex items-center justify-between">
            <h1 class="text-3xl font-bold text-white">
              Notifications
            </h1>

            <!-- Back to Home Button -->
            <button
              @click="goBackHome"
              class="flex items-center gap-2 px-4 py-2.5 bg-white/20 hover:bg-white/30 rounded-lg transition-all duration-200"
            >
              <i class="pi pi-arrow-left text-white"></i>
              <span class="text-white font-semibold">Back to Home</span>
            </button>
          </div>
        </div>

        <!-- Tabs -->
        <div class="p-6 bg-white border-b border-gray-100">
          <div class="flex items-center justify-between">
            <div class="flex flex-wrap gap-3">
              <button
                v-for="tab in ['all', 'unread']"
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
                    'pi-envelope': tab === 'unread'
                  },
                  activeTab === tab ? 'scale-110' : 'group-hover:scale-110'
                ]"></i>
                <span class="capitalize">{{ tab }}</span>
                <span v-if="tab === 'unread' && notifications.filter(n => n.isUnread).length > 0"
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

            <!-- Action Buttons -->
            <div class="flex items-center gap-2">
              <!-- Select Button -->
              <button
                v-if="notifications.length > 0"
                @click="toggleSelectMode"
                class="px-4 py-2.5 text-sm font-semibold transition-all duration-200 flex items-center gap-2 rounded-xl"
                :class="isSelectMode
                  ? 'text-white bg-indigo-600 hover:bg-indigo-700'
                  : 'text-indigo-600 hover:text-white hover:bg-indigo-600 border-2 border-indigo-300 hover:border-indigo-600'"
              >
                <i :class="isSelectMode ? 'pi pi-times' : 'pi pi-check-square'"></i>
                <span>{{ isSelectMode ? 'Cancel' : 'Select' }}</span>
              </button>

              <!-- Delete Selected Button -->
              <button
                v-if="isSelectMode && selectedNotifications.length > 0"
                @click="showDeleteConfirmation('selected')"
                class="px-4 py-2.5 text-sm font-semibold text-white bg-red-600 hover:bg-red-700 border-2 border-red-600 rounded-xl transition-all duration-200 flex items-center gap-2"
              >
                <i class="pi pi-trash"></i>
                <span>Delete ({{ selectedNotifications.length }})</span>
              </button>

              <!-- Delete All Button -->
              <button
                v-if="notifications.length > 0 && !isSelectMode"
                @click="showDeleteConfirmation('all')"
                class="px-4 py-2.5 text-sm font-semibold text-red-600 hover:text-white hover:bg-red-500 border-2 border-red-300 hover:border-red-500 rounded-xl transition-all duration-200 flex items-center gap-2"
              >
                <i class="pi pi-trash"></i>
                <span>Delete All</span>
              </button>
            </div>
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
              @click="handleNotificationClick(notification)"
            >
              <!-- Unread Indicator -->
              <div v-if="notification.isUnread" class="absolute top-0 left-0 w-1.5 h-full bg-gradient-to-b from-indigo-600 to-purple-600"></div>

              <div class="p-5 flex items-center gap-5">
                <!-- Checkbox (Select Mode) -->
                <div v-if="isSelectMode" class="flex items-center">
                  <input
                    type="checkbox"
                    :checked="selectedNotifications.includes(notification.id)"
                    @change="toggleNotificationSelection(notification.id)"
                    @click.stop
                    class="w-5 h-5 text-indigo-600 border-2 border-gray-300 rounded focus:ring-2 focus:ring-indigo-500 cursor-pointer"
                  />
                </div>

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
                  </div>

                  <p class="text-gray-700 leading-relaxed mb-3">{{ notification.message }}</p>

                  <div class="flex items-center gap-4 text-sm">
                    <div class="flex items-center gap-2 text-gray-500">
                      <i class="pi pi-clock"></i>
                      <span class="font-medium">{{ formatDate(notification.date) }}</span>
                    </div>
                  </div>
                </div>

                <!-- Unread Indicator (Right Middle) -->
                <div v-if="notification.isUnread" class="flex items-center">
                  <div class="flex items-center gap-2 text-indigo-600 bg-indigo-50 px-3 py-2 rounded-lg">
                    <div class="w-2 h-2 bg-indigo-600 rounded-full animate-pulse"></div>
                    <span class="font-semibold text-sm">Unread</span>
                  </div>
                </div>
              </div>
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

    <!-- Delete Confirmation Dialog -->
    <div
      v-if="showDeleteDialog"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      @click="cancelDelete"
    >
      <div
        class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 transform transition-all"
        @click.stop
      >
        <!-- Icon -->
        <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <i class="pi pi-exclamation-triangle text-red-600 text-3xl"></i>
        </div>

        <!-- Title -->
        <h3 class="text-xl font-bold text-gray-900 text-center mb-2">
          Confirm Delete
        </h3>

        <!-- Message -->
        <p class="text-gray-600 text-center mb-6">
          <span v-if="deleteAction === 'all'">
            Are you sure you want to delete all notifications? This action cannot be undone.
          </span>
          <span v-else-if="deleteAction === 'selected'">
            Are you sure you want to delete {{ selectedNotifications.length }} selected notification(s)?
          </span>
        </p>

        <!-- Actions -->
        <div class="flex gap-3">
          <button
            @click="cancelDelete"
            class="flex-1 px-4 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold rounded-xl transition-all duration-200"
          >
            Cancel
          </button>
          <button
            @click="confirmDelete"
            class="flex-1 px-4 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-xl transition-all duration-200"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useToast } from '../../composables/useToast';

// Initialize toast
const { showSuccess, showError, showInfo, showWarning } = useToast();

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
const isSelectMode = ref(false);
const selectedNotifications = ref([]);
const showDeleteDialog = ref(false);
const deleteAction = ref(null); // 'all' or 'selected'

// Notifications data from backend
const notifications = ref([]);

// Load notifications from backend
const loadNotifications = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get('/api/notifications/');
    if (response.data) {
      // Get the last time user opened notifications page or dropdown
      const lastOpenedTime = parseInt(localStorage.getItem('notifications_last_opened_time') || '0');

      notifications.value = response.data.map(notif => {
        const createdTime = new Date(notif.created_at).getTime();
        const currentTime = Date.now();
        const oneMinute = 60 * 1000; // 1 minute in milliseconds

        // Mark as NEW if created within the last 1 minute
        const isNew = (currentTime - createdTime) < oneMinute;

        return {
          id: notif.id,
          type: notif.notification_type,
          title: notif.title,
          message: notif.message,
          date: new Date(notif.created_at),
          isNew: isNew,
          isUnread: !notif.is_read,
          // Include related entity IDs for navigation
          activityId: notif.activity,
          submissionId: notif.submission,
          portfolioId: notif.portfolio,
          remarkId: notif.remark,
        };
      });
      console.log('✅ Loaded student notifications:', notifications.value.length);
      console.log('🆕 New notifications:', notifications.value.filter(n => n.isNew).length);
      console.log('⏰ Last opened time:', new Date(lastOpenedTime).toLocaleString());
    }
  } catch (error) {
    console.error('❌ Error loading notifications:', error);
  } finally {
    isLoading.value = false;
  }
};

// Load notifications on mount
onMounted(() => {
  // Load notifications
  loadNotifications();
});

// Toggle select mode
const toggleSelectMode = () => {
  isSelectMode.value = !isSelectMode.value;
  if (!isSelectMode.value) {
    selectedNotifications.value = [];
  }
};

// Toggle notification selection
const toggleNotificationSelection = (id) => {
  const index = selectedNotifications.value.indexOf(id);
  if (index > -1) {
    selectedNotifications.value.splice(index, 1);
  } else {
    selectedNotifications.value.push(id);
  }
};

// Show delete confirmation dialog
const showDeleteConfirmation = (action) => {
  deleteAction.value = action;
  showDeleteDialog.value = true;
};

// Confirm delete action
const confirmDelete = async () => {
  showDeleteDialog.value = false;

  if (deleteAction.value === 'selected') {
    await deleteSelectedNotifications();
  } else if (deleteAction.value === 'all') {
    await deleteAllNotifications();
  }

  deleteAction.value = null;
};

// Cancel delete action
const cancelDelete = () => {
  showDeleteDialog.value = false;
  deleteAction.value = null;
};

// Delete selected notifications
const deleteSelectedNotifications = async () => {
  try {
    // Delete selected notifications via API
    const deletePromises = selectedNotifications.value.map(id =>
      axios.delete('/api/notifications/', {
        data: { notification_id: id }
      })
    );

    await Promise.all(deletePromises);

    // Remove deleted notifications from local state
    notifications.value = notifications.value.filter(
      n => !selectedNotifications.value.includes(n.id)
    );

    console.log(`✅ Deleted ${selectedNotifications.value.length} notifications`);

    // Clear selection and exit select mode
    selectedNotifications.value = [];
    isSelectMode.value = false;
  } catch (error) {
    console.error('❌ Error deleting notifications:', error);
    showError('Failed to delete notifications', 'Update Failed');
  }
};

// Delete all notifications
const deleteAllNotifications = async () => {
  try {
    // Delete all notifications via API
    const response = await axios.delete('/api/notifications/', {
      data: { delete_all: true }
    });

    if (response.status === 200) {
      // Clear local state
      notifications.value = [];
      console.log('✅ All notifications deleted:', response.data.message);
    }
  } catch (error) {
    console.error('❌ Error deleting notifications:', error);
    showError('Failed to delete notifications', 'Update Failed');
  }
};

// Go back to home (Student -> Newsfeed)
const goBackHome = () => {
  window.location.href = '/student/newsfeed/';
};

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

// Filtered notifications based on active tab
const filteredNotifications = computed(() => {
  if (activeTab.value === 'all') {
    return notifications.value;
  } else if (activeTab.value === 'unread') {
    return notifications.value.filter(n => n.isUnread);
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

// Handle notification click - mark as read and navigate
const handleNotificationClick = async (notification) => {
  // Don't navigate if in select mode
  if (isSelectMode.value) {
    return;
  }

  // Mark as read
  await markAsRead(notification.id);

  // Navigate based on notification type using window.navigateTo
  const type = notification.type;

  if (type === 'activity_created' || type === 'activity_updated') {
    // Navigate to classroom to view the activity
    console.log('📍 Navigating to classroom for activity notification');
    // Set notification context with activity ID for direct navigation
    if (notification.activityId) {
      localStorage.setItem('notification_context', JSON.stringify({
        activityId: notification.activityId,
        timestamp: Date.now()
      }));
    }
    if (window.navigateTo) {
      window.navigateTo('StudentRoom');
    } else {
      window.location.href = '/student/room';
    }
  } else if (type === 'submission_approved') {
    // Navigate to newsfeed to see approved post
    console.log('📍 Navigating to newsfeed for approved submission');
    if (window.navigateTo) {
      window.navigateTo('StudentNewsfeed');
    } else {
      window.location.href = '/student/newsfeed';
    }
  } else if (type === 'submission_rejected') {
    // Navigate to sketch pad to resubmit
    console.log('📍 Navigating to sketch for rejected submission');
    if (window.navigateTo) {
      window.navigateTo('StudentSketch');
    } else {
      window.location.href = '/student/sketch';
    }
  } else if (type === 'score_added') {
    // Navigate to classroom to view the specific scored activity
    console.log('📍 Navigating to classroom for score notification, activityId:', notification.activityId);
    // Set notification context with activity ID for direct navigation to the scored activity
    if (notification.activityId) {
      localStorage.setItem('notification_context', JSON.stringify({
        activityId: notification.activityId,
        timestamp: Date.now()
      }));
    }
    if (window.navigateTo) {
      window.navigateTo('StudentRoom');
    } else {
      window.location.href = '/student/room';
    }
  } else if (type === 'remark_added' || type === 'remark_updated' || type === 'remark_deleted') {
    // Navigate to remarked page to view remarks
    console.log('📍 Navigating to remarked page for remark notification');
    if (window.navigateTo) {
      window.navigateTo('StudentRemarked');
    } else {
      window.location.href = '/student/remarked';
    }
  } else if (type === 'portfolio_created' || type === 'portfolio_updated') {
    // Navigate to classroom
    console.log('📍 Navigating to classroom for portfolio notification');
    if (window.navigateTo) {
      window.navigateTo('StudentRoom');
    } else {
      window.location.href = '/student/room';
    }
  } else {
    // Default: navigate to classroom
    console.log('📍 Navigating to classroom (default)');
    if (window.navigateTo) {
      window.navigateTo('StudentRoom');
    } else {
      window.location.href = '/student/room';
    }
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
