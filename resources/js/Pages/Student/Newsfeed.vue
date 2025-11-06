<template>
    <div class="min-h-screen bg-gradient-to-br from-teal-50 via-cyan-50 to-blue-50">
        <!-- Main Content -->
        <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8">

            <!-- Loading State -->
            <div v-if="isLoading" class="flex flex-col items-center justify-center py-16 bg-white rounded-2xl shadow-xl border-2 border-teal-100">
                <div class="relative">
                    <div class="animate-spin rounded-full h-16 w-16 border-4 border-teal-200"></div>
                    <div class="absolute top-0 animate-spin rounded-full h-16 w-16 border-t-4 border-teal-600"></div>
                </div>
                <p class="mt-4 text-gray-600 font-medium">Loading amazing content...</p>
            </div>

            <!-- Empty State -->
            <div v-else-if="posts.length === 0" class="text-center py-16 bg-white rounded-2xl shadow-xl border-2 border-teal-100">
                <div class="max-w-sm mx-auto">
                    <div class="w-24 h-24 bg-gradient-to-br from-teal-100 to-cyan-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <i class="pi pi-palette text-4xl text-teal-600"></i>
                    </div>
                    <h3 class="text-xl font-bold text-gray-800 mb-2">No Posts Yet</h3>
                    <p class="text-gray-600">No posts from your classroom yet. Check back later!</p>
                </div>
            </div>

            <!-- Posts Feed -->
            <div v-else class="space-y-6">
                <div v-for="post in posts" :key="post.id" 
                    class="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border-2 border-teal-100 hover:border-teal-300">
                    
                    <!-- Post Header -->
                    <div class="p-6 pb-4">
                        <div class="flex items-start justify-between">
                            <div class="flex items-center gap-4">
                                <div class="relative">
                                    <div class="w-14 h-14 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-full flex items-center justify-center text-white text-xl font-bold shadow-lg ring-2 ring-teal-200">
                                        {{ post.user.charAt(0).toUpperCase() }}
                                    </div>
                                    <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-teal-500 rounded-full border-2 border-white"></div>
                                </div>
                                <div>
                                    <h3 class="font-bold text-lg text-gray-800">{{ post.user }}</h3>
                                    <div class="flex items-center gap-2 text-sm">
                                        <span class="text-gray-500">{{ post.timestamp }}</span>
                                        <span v-if="post.activityTitle" class="text-teal-700 font-semibold">
                                            <i class="pi pi-bookmark-fill text-xs"></i>
                                            {{ post.activityType }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- 3-Dot Menu -->
                            <div class="relative">
                                <button @click="togglePostMenu(post)" 
                                    class="text-gray-400 hover:text-gray-600 transition-colors p-2 hover:bg-gray-100 rounded-full">
                                    <i class="pi pi-ellipsis-v text-xl"></i>
                                </button>
                                
                                <!-- Dropdown Menu -->
                                <div v-if="post.showMenu" 
                                    class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-2xl border border-gray-200 z-50 overflow-hidden">
                                    <div class="py-2">
                                        <button @click="bookmarkPost(post)" 
                                            class="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors text-left">
                                            <i class="pi pi-bookmark text-indigo-600"></i>
                                            <span class="text-sm font-medium text-gray-700">Save Post</span>
                                        </button>
                                        <button @click="reportPost(post)" 
                                            class="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors text-left">
                                            <i class="pi pi-flag text-orange-600"></i>
                                            <span class="text-sm font-medium text-gray-700">Report Content</span>
                                        </button>
                                        <button @click="hidePost(post)" 
                                            class="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors text-left">
                                            <i class="pi pi-eye-slash text-gray-600"></i>
                                            <span class="text-sm font-medium text-gray-700">Hide Post</span>
                                        </button>
                                        <div class="border-t border-gray-100 my-1"></div>
                                        <button @click="copyLink(post)" 
                                            class="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors text-left">
                                            <i class="pi pi-link text-blue-600"></i>
                                            <span class="text-sm font-medium text-gray-700">Copy Link</span>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Post Content -->
                    <div class="px-6 pb-4">
                        <p class="text-gray-700 leading-relaxed">{{ post.content }}</p>
                        <div v-if="post.activityTitle" class="mt-3 inline-flex items-center gap-2 px-3 py-1 bg-gradient-to-r from-teal-100 to-cyan-100 rounded-full border border-teal-200">
                            <i class="pi pi-tag text-teal-600 text-sm"></i>
                            <span class="text-sm font-semibold text-teal-800">{{ post.activityTitle }}</span>
                        </div>
                    </div>

                    <!-- Post Image with Placeholder -->
                    <div v-if="post.image" class="px-6 pb-4">
                        <div class="relative group cursor-pointer bg-gray-100 rounded-2xl overflow-hidden">
                            <!-- Smaller aspect ratio container -->
                            <div class="relative w-full" style="padding-bottom: 50%; min-height: 200px; max-height: 400px;">
                                <img :src="post.image" 
                                    :alt="post.content"
                                    class="absolute inset-0 w-full h-full object-contain bg-gray-50"
                                    @error="handleImageError"
                                    loading="lazy">
                                <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all duration-300"></div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Smaller placeholder for missing image -->
                    <div v-else-if="post.activityType" class="px-6 pb-4">
                        <div class="relative bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl flex items-center justify-center" style="min-height: 200px;">
                            <div class="text-center text-gray-400">
                                <i class="pi pi-image text-4xl mb-2"></i>
                                <p class="text-xs font-medium">No image available</p>
                            </div>
                        </div>
                    </div>

                    <!-- Interaction Bar -->
                    <div class="px-6 py-4 border-t-2 border-teal-50 bg-gradient-to-r from-teal-50/50 to-cyan-50/50">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <!-- Like Button -->
                                <button @click="toggleLike(post)" 
                                    class="flex items-center gap-2 px-4 py-2 rounded-lg font-semibold transition-all duration-300 group"
                                    :class="post.isLiked 
                                        ? 'bg-gradient-to-r from-red-50 to-pink-50 text-red-600 border border-red-200 shadow-md' 
                                        : 'bg-gradient-to-r from-teal-50 to-cyan-50 text-teal-700 border border-teal-200 hover:from-teal-100 hover:to-cyan-100'">
                                    <i class="pi text-lg transition-transform group-hover:scale-110" 
                                        :class="post.isLiked ? 'pi-heart-fill animate-pulse' : 'pi-heart'"></i>
                                    <span class="font-semibold">{{ post.likes }}</span>
                                </button>

                                <!-- Comment Button -->
                                <button @click="toggleComments(post)"
                                    :class="post.showComments 
                                        ? 'bg-gradient-to-r from-cyan-100 to-blue-100 text-cyan-700 border border-cyan-200' 
                                        : 'bg-gradient-to-r from-cyan-50 to-blue-50 text-cyan-700 border border-cyan-200 hover:from-cyan-100 hover:to-blue-100'"
                                    class="flex items-center gap-2 px-4 py-2 rounded-lg font-semibold transition-all duration-300 group">
                                    <i class="pi pi-comments text-lg transition-transform group-hover:scale-110"></i>
                                    <span class="font-semibold">{{ post.comments.length }}</span>
                                </button>
                            </div>

                            <!-- Bookmark Button -->
                            <button @click="bookmarkPost(post)" 
                                :class="post.isBookmarked ? 'text-amber-600' : 'text-gray-400 hover:text-amber-600'"
                                class="transition-colors p-2 hover:bg-amber-50 rounded-full">
                                <i class="pi text-xl" :class="post.isBookmarked ? 'pi-bookmark-fill' : 'pi-bookmark'"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Comments Section -->
                    <div v-if="post.showComments" 
                        class="px-6 pb-6 border-t-2 border-teal-50 bg-gradient-to-b from-teal-50/30 to-transparent">
                        <h4 class="font-semibold text-gray-700 mb-4 mt-4 flex items-center gap-2">
                            <i class="pi pi-comments text-cyan-600"></i>
                            Comments ({{ post.comments.length }})
                        </h4>
                        
                        <!-- Comment Input -->
                        <div class="mb-4">
                            <div class="flex items-start gap-3">
                                <div class="w-10 h-10 bg-gradient-to-br from-teal-600 to-cyan-600 rounded-full flex items-center justify-center text-white text-sm font-bold ring-2 ring-teal-200 shadow-lg">
                                    S
                                </div>
                                <div class="flex-1">
                                    <textarea 
                                        v-model="post.newComment"
                                        @keydown.enter.ctrl="addComment(post)"
                                        placeholder="Write a comment... (Ctrl+Enter to post)"
                                        class="w-full px-4 py-3 border-2 border-teal-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-teal-500 resize-none"
                                        rows="2"></textarea>
                                    <div class="flex items-center justify-between mt-2">
                                        <span class="text-xs text-gray-500">Press Ctrl+Enter to post</span>
                                        <button @click="addComment(post)"
                                            :disabled="!post.newComment || post.newComment.trim() === ''"
                                            class="px-4 py-2 bg-gradient-to-r from-teal-600 to-cyan-600 text-white rounded-lg hover:from-teal-700 hover:to-cyan-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all text-sm font-semibold shadow-md">
                                            <i class="pi pi-send mr-2"></i>
                                            Post Comment
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Comments List -->
                        <div v-if="post.comments.length > 0" class="space-y-3">
                            <div v-for="comment in post.comments" :key="comment.id" 
                                class="flex items-start gap-3 bg-gradient-to-r from-white to-teal-50/50 hover:from-teal-50 hover:to-cyan-50 p-4 rounded-xl border border-teal-100 transition-colors">
                                <div class="w-10 h-10 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-full flex items-center justify-center text-white text-sm font-bold ring-2 ring-teal-200">
                                    {{ comment.user.charAt(0).toUpperCase() }}
                                </div>
                                <div class="flex-1">
                                    <div class="flex items-center justify-between">
                                        <p class="font-semibold text-gray-800">{{ comment.user }}</p>
                                        <span class="text-xs text-gray-400">{{ comment.timestamp || 'Just now' }}</span>
                                    </div>
                                    <p class="text-gray-600 mt-1">{{ comment.text }}</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Empty State -->
                        <div v-else class="text-center py-8">
                            <i class="pi pi-comments text-4xl text-gray-300 mb-2"></i>
                            <p class="text-gray-400 text-sm">No comments yet. Be the first to comment!</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useToast } from '../../composables/useToast';

const { showSuccess, showError, showInfo, showWarning } = useToast();

// Define emits
const emit = defineEmits(['navigate']);

const isLoading = ref(false);
const posts = ref([]);
const sidebarCollapsed = ref(false);
const statsExpanded = ref(false);
const currentFilter = ref('all');
const showMobileStats = ref(false);

// Computed values for stats
const totalLikes = computed(() => {
  return posts.value.reduce((sum, post) => sum + (post.likes || 0), 0);
});

const totalComments = computed(() => {
  return posts.value.reduce((sum, post) => sum + (post.comments?.length || 0), 0);
});

// Load newsfeed from API
const loadNewsfeed = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get('/api/newsfeed/');
    if (response.data && Array.isArray(response.data)) {
      posts.value = response.data.map(post => ({
        id: post.id,
        user: post.student_name,
        content: post.caption || 'No description provided',
        image: post.file_type === 'image' ? post.file_path : null,
        likes: post.likes || 0,
        isLiked: post.is_liked || false,
        timestamp: getTimeAgo(post.posted_at),
        activityTitle: post.activity_title,
        activityType: post.activity_type,
        comments: [],
        showComments: false,
        showMenu: false,
        isBookmarked: false,
        newComment: ''
      }));
      console.log('✅ Loaded newsfeed:', posts.value);
    } else {
      posts.value = [];
    }
  } catch (error) {
    console.error('❌ Error loading newsfeed:', error);
    showError('Failed to load newsfeed posts', 'Error');
    posts.value = [];
  } finally {
    isLoading.value = false;
  }
};

// Load comments for each post
const loadComments = async () => {
  for (const post of posts.value) {
    try {
      const response = await axios.get(`/api/posts/${post.id}/comments/`);
      if (response.data && Array.isArray(response.data)) {
        post.comments = response.data.map(comment => ({
          id: comment.id,
          user: comment.user,
          text: comment.text,
          timestamp: comment.timestamp || getTimeAgo(comment.created_at)
        }));
      }
    } catch (error) {
      console.error(`Error loading comments for post ${post.id}:`, error);
      showError('Failed to load comments', 'Error');
    }
  }
};

// Handle image load error
const handleImageError = (event) => {
  console.error('Failed to load image:', event.target.src);
  event.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect fill="%23f3f4f6" width="400" height="300"/%3E%3Ctext fill="%239ca3af" font-family="sans-serif" font-size="18" dy="10.5" font-weight="bold" x="50%25" y="50%25" text-anchor="middle"%3EImage not found%3C/text%3E%3C/svg%3E';
};

// Toggle like
const toggleLike = async (post) => {
  try {
    const newLikedState = !post.isLiked;
    const response = await axios.post(`/api/posts/${post.id}/like/`, {
      liked: newLikedState
    });
    
    if (response.data.success) {
      post.isLiked = newLikedState;
      post.likes = response.data.likes_count;
      console.log('✅ Like toggled successfully');
    }
  } catch (error) {
    console.error('❌ Error toggling like:', error);
    if (error.response?.status === 403) {
      const message = error.response?.data?.message || 'Please log in to like posts';
      showError(message, 'Authentication Required');
      if (confirm(`${message}\n\nWould you like to log in now?`)) {
        emit('navigate', 'Login');
      }
    } else {
      alert('Failed to like post. Please try again.');
    }
  }
};

// Toggle comments visibility
const toggleComments = (post) => {
  post.showComments = !post.showComments;
};

// Filter by topic
const filterByTopic = (topic) => {
  currentFilter.value = topic;
  // You can implement actual filtering logic here
  // For now, just setting the active filter
  console.log('Filtering by:', topic);
};

// Add comment
const addComment = async (post) => {
  if (!post.newComment || post.newComment.trim() === '') return;
  
  try {
    const response = await axios.post(`/api/posts/${post.id}/comments/`, {
      text: post.newComment.trim()
    });
    
    if (response.data.success) {
      // Add comment to the list
      post.comments.push({
        id: response.data.comment.id,
        user: response.data.comment.user,
        text: response.data.comment.text,
        timestamp: response.data.comment.timestamp || 'Just now'
      });
      
      // Clear input
      post.newComment = '';
      
      console.log('✅ Comment added successfully');
    }
  } catch (error) {
    console.error('❌ Error adding comment:', error);
    if (error.response?.status === 403) {
      const message = error.response?.data?.message || 'Please log in to comment on posts';
      showError(message, 'Authentication Required');
      if (confirm(`${message}\n\nWould you like to log in now?`)) {
        emit('navigate', 'Login');
      }
    } else {
      const errorMsg = error.response?.data?.error || 'Failed to add comment. Please try again.';
      alert(errorMsg);
    }
  }
};

// Toggle post menu
const togglePostMenu = (post) => {
  // Close all other menus
  posts.value.forEach(p => {
    if (p.id !== post.id) p.showMenu = false;
  });
  post.showMenu = !post.showMenu;
};

// Bookmark post
const bookmarkPost = (post) => {
  post.isBookmarked = !post.isBookmarked;
  post.showMenu = false;
  
  const message = post.isBookmarked ? 'Post saved!' : 'Post removed from saved';
  console.log(`📌 ${message}`);
  
  // You can add API call here to persist bookmark
  // await axios.post(`/api/posts/${post.id}/bookmark/`, { bookmarked: post.isBookmarked });
};

// Report post
const reportPost = (post) => {
  post.showMenu = false;
  
  const reason = prompt('Please tell us why you\'re reporting this post:\n\n1. Inappropriate content\n2. Spam\n3. Harassment\n4. Other\n\nEnter reason:');
  
  if (reason) {
    console.log(`🚩 Post ${post.id} reported: ${reason}`);
    alert('Thank you for your report. We will review this content.');
    
    // Add API call here
    // await axios.post(`/api/posts/${post.id}/report/`, { reason });
  }
};

// Hide post
const hidePost = (post) => {
  post.showMenu = false;
  
  if (confirm('Hide this post? You won\'t see it in your feed anymore.')) {
    const index = posts.value.findIndex(p => p.id === post.id);
    if (index > -1) {
      posts.value.splice(index, 1);
      console.log(`👁️‍🗨️ Post ${post.id} hidden`);
      
      // Add API call here
      // await axios.post(`/api/posts/${post.id}/hide/`);
    }
  }
};

// Copy link
const copyLink = (post) => {
  post.showMenu = false;
  
  const link = `${window.location.origin}/post/${post.id}`;
  navigator.clipboard.writeText(link).then(() => {
    alert('Link copied to clipboard!');
    console.log(`🔗 Link copied: ${link}`);
  }).catch(err => {
    console.error('Failed to copy link:', err);
  });
};

// Get time ago
const getTimeAgo = (dateString) => {
  if (!dateString) return 'Just now';
  
  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now - date) / 1000);
  
  if (seconds < 60) return 'Just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
  if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`;
  
  return date.toLocaleDateString();
};

// Load data on mount
onMounted(async () => {
  await loadNewsfeed();
  await loadComments();
});
</script>

<style scoped>
/* Avatar colors */
.bg-blue-500 { background-color: #3b82f6; }
.bg-purple-500 { background-color: #8b5cf6; }
.bg-red-500 { background-color: #ef4444; }
.bg-green-500 { background-color: #10b981; }
.bg-yellow-500 { background-color: #f59e0b; }
.bg-indigo-500 { background-color: #6366f1; }

/* Like button active state */
.bg-red-50 { background-color: #fef2f2; }
.text-red-500 { color: #ef4444; }

/* Hover effects */
.hover\:bg-gray-200:hover { background-color: #e5e7eb; }

/* Responsive images */
img {
    max-width: 100%;
    height: auto;
    display: block;
}

/* Card styling */
.rounded-xl { border-radius: 1rem; }
.shadow-lg { 
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
                0 2px 4px -1px rgba(0, 0, 0, 0.06); 
}

/* Smooth transitions */
.transition-colors {
    transition: background-color 0.2s ease, color 0.2s ease;
}
</style>    