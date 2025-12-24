<template>
    <div class="min-h-screen bg-gradient-to-br from-teal-50 via-cyan-50 to-blue-50">
        <!-- Main Content -->
        <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8">
            <!-- Loading State -->
            <div v-if="isLoading" class="flex justify-center items-center py-20">
                <div class="text-center">
                    <div class="animate-spin rounded-full h-16 w-16 border-4 border-indigo-600 border-t-transparent mx-auto mb-4"></div>
                    <p class="text-gray-600">Loading amazing work...</p>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else-if="posts.length === 0" class="text-center py-20">
                <div class="bg-white rounded-2xl shadow-xl p-12 max-w-md mx-auto border-2 border-teal-100">
                    <div class="w-20 h-20 bg-gradient-to-br from-teal-100 to-cyan-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <i class="pi pi-image text-4xl text-teal-600"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-800 mb-2">No Posts Yet</h3>
                    <p class="text-gray-600">Approved student artwork will appear here</p>
                    <p class="text-sm text-gray-500 mt-2">Check back soon for creative submissions!</p>
                </div>
            </div>

            <!-- Posts Feed -->
            <div v-else class="space-y-6">
                <!-- Post Card -->
                <div v-for="post in posts" :key="post.id"
                    class="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border-2 border-teal-100 hover:border-teal-300">

                    <!-- Post Header -->
                    <div class="p-6 pb-4">
                        <div class="flex items-start justify-between">
                            <div class="flex items-center gap-4">
                                <!-- Avatar -->
                                <div class="relative">
                                    <div :class="getAvatarColor(post.user)"
                                        class="w-14 h-14 flex items-center justify-center rounded-full text-white font-bold text-lg shadow-lg ring-2 ring-teal-200">
                                        {{ post.user.charAt(0).toUpperCase() }}
                                    </div>
                                    <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-teal-500 rounded-full border-2 border-white"></div>
                                </div>

                                <!-- User Info -->
                                <div>
                                    <h3 class="font-bold text-gray-900 text-lg">{{ post.user }}</h3>
                                    <div class="flex items-center gap-2 text-sm text-gray-500">
                                        <i class="pi pi-clock text-xs"></i>
                                        <span>{{ post.timestamp }}</span>
                                    </div>
                                    <div v-if="post.activityTitle" class="flex items-center gap-2 mt-1">
                                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-gradient-to-r from-teal-100 to-cyan-100 text-teal-800 border border-teal-200">
                                            <i class="pi pi-bookmark text-[10px] mr-1"></i>
                                            {{ post.activityType }}
                                        </span>
                                        <span class="text-xs text-gray-600 font-medium">{{ post.activityTitle }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Post Content -->
                    <div class="px-6 pb-4">
                        <p class="text-gray-700 leading-relaxed">{{ post.content }}</p>
                    </div>

                    <!-- Post Images with Navigation -->
                    <div v-if="post.files && post.files.length > 0" class="relative group bg-gray-100">
                        <!-- Image container -->
                        <div class="relative w-full" style="padding-bottom: 50%; min-height: 200px; max-height: 400px;">
                            <img :src="getCurrentFile(post).file_path"
                                :alt="post.content"
                                class="absolute inset-0 w-full h-full object-contain cursor-pointer bg-gray-50"
                                @click="openImageModal(getCurrentFile(post).file_path)"
                                @error="handleImageError"
                                loading="lazy">
                            
                            <!-- Navigation Arrows (only show if multiple files) -->
                            <div v-if="post.files.length > 1" class="absolute inset-0 flex items-center justify-between px-2 pointer-events-none">
                                <!-- Previous Button -->
                                <button
                                    @click.stop="previousPostFile(post)"
                                    :disabled="post.currentFileIndex === 0"
                                    class="pointer-events-auto w-10 h-10 rounded-full bg-white/90 hover:bg-white shadow-lg flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed z-10"
                                    :class="post.currentFileIndex === 0 ? '' : 'hover:scale-110'"
                                >
                                    <i class="pi pi-chevron-left text-teal-600"></i>
                                </button>
                                
                                <!-- Next Button -->
                                <button
                                    @click.stop="nextPostFile(post)"
                                    :disabled="post.currentFileIndex >= post.files.length - 1"
                                    class="pointer-events-auto w-10 h-10 rounded-full bg-white/90 hover:bg-white shadow-lg flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed z-10"
                                    :class="post.currentFileIndex >= post.files.length - 1 ? '' : 'hover:scale-110'"
                                >
                                    <i class="pi pi-chevron-right text-teal-600"></i>
                                </button>
                            </div>

                            <!-- File Counter (only show if multiple files) -->
                            <div v-if="post.files.length > 1" class="absolute top-3 right-3 z-10">
                                <div class="bg-black/60 text-white px-3 py-1 rounded-full text-xs font-medium">
                                    {{ post.currentFileIndex + 1 }} / {{ post.files.length }}
                                </div>
                            </div>

                            <!-- Zoom overlay -->
                            <div class="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors duration-300 flex items-center justify-center pointer-events-none">
                                <i class="pi pi-search-plus text-white text-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></i>
                            </div>
                        </div>
                    </div>

                    <!-- Legacy single image support -->
                    <div v-else-if="post.image" class="relative group bg-gray-100">
                        <div class="relative w-full" style="padding-bottom: 50%; min-height: 200px; max-height: 400px;">
                            <img :src="post.image"
                                :alt="post.content"
                                class="absolute inset-0 w-full h-full object-contain cursor-pointer bg-gray-50"
                                @click="openImageModal(post.image)"
                                @error="handleImageError"
                                loading="lazy">
                            <div class="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors duration-300 flex items-center justify-center pointer-events-none">
                                <i class="pi pi-search-plus text-white text-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></i>
                            </div>
                        </div>
                    </div>

                    <!-- Smaller placeholder for missing image -->
                    <div v-else-if="post.activityType" class="relative bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center" style="min-height: 200px;">
                        <div class="text-center text-gray-400">
                            <i class="pi pi-image text-4xl mb-2"></i>
                            <p class="text-xs font-medium">No image available</p>
                        </div>
                    </div>

                    <!-- Engagement Stats -->
                    <div class="px-6 py-3 border-t-2 border-teal-50 bg-gradient-to-r from-teal-50/50 to-cyan-50/50">
                        <div class="flex items-center justify-between text-sm font-medium">
                            <span class="flex items-center gap-1.5 text-teal-700">
                                <i class="pi pi-heart-fill text-red-500 text-sm"></i>
                                {{ post.likes }} {{ post.likes === 1 ? 'like' : 'likes' }}
                            </span>
                            <span class="text-cyan-700">{{ getTotalCommentsCount(post) }} {{ getTotalCommentsCount(post) === 1 ? 'comment' : 'comments' }}</span>
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="px-6 py-3 border-t-2 border-teal-50 flex items-center gap-2">
                        <button @click="toggleLike(post)"
                            class="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg font-semibold transition-all duration-200"
                            :class="post.isLiked
                                ? 'bg-gradient-to-r from-red-50 to-pink-50 text-red-600 hover:from-red-100 hover:to-pink-100 border border-red-200'
                                : 'bg-gradient-to-r from-teal-50 to-cyan-50 text-teal-700 hover:from-teal-100 hover:to-cyan-100 border border-teal-200'">
                            <i class="pi text-lg" :class="post.isLiked ? 'pi-heart-fill' : 'pi-heart'"></i>
                        </button>

                        <button @click="toggleComments(post)"
                            class="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg font-semibold bg-gradient-to-r from-cyan-50 to-blue-50 text-cyan-700 hover:from-cyan-100 hover:to-blue-100 border border-cyan-200 transition-all duration-200">
                            <i class="pi pi-comment text-lg"></i>
                            <span>Comment</span>
                        </button>
                    </div>

                    <!-- Comments Section -->
                    <div v-if="post.showComments" class="px-6 pb-6 border-t-2 border-teal-50 bg-gradient-to-b from-teal-50/30 to-transparent">
                        <!-- Existing Comments -->
                        <div v-if="post.comments.length > 0" class="mt-4 space-y-3 max-h-96 overflow-y-auto">
                            <div v-for="comment in post.comments" :key="comment.id"
                                class="flex items-start gap-3 p-3 rounded-xl bg-gradient-to-r from-white to-teal-50/50 hover:from-teal-50 hover:to-cyan-50 transition-colors border border-teal-100">
                                <div :class="getAvatarColor(comment.user)"
                                    class="w-10 h-10 flex items-center justify-center rounded-full text-white font-bold text-sm flex-shrink-0 ring-2 ring-teal-200">
                                    {{ comment.user.charAt(0).toUpperCase() }}
                                </div>
                                <div class="flex-1 min-w-0">
                                    <div class="bg-white rounded-lg p-3 shadow-md border border-teal-100">
                                        <p class="font-semibold text-gray-900 text-sm">{{ comment.user }}</p>
                                        <p class="text-gray-700 mt-1">{{ comment.text }}</p>
                                    </div>
                                    <div class="flex items-center gap-4 mt-2 text-xs text-gray-600">
                                        <span>{{ comment.timestamp }}</span>
                                        <button @click="toggleCommentLike(post, comment)" class="hover:text-red-600 font-semibold transition-colors flex items-center gap-1">
                                            <i class="pi text-xs" :class="comment.isLiked ? 'pi-heart-fill text-red-500' : 'pi-heart'"></i>
                                            <span v-if="comment.likes > 0">{{ comment.likes }}</span>
                                        </button>
                                        <button @click="toggleReplyInput(comment)" class="hover:text-cyan-600 font-semibold transition-colors">Reply</button>
                                    </div>
                                    <!-- Reply Input -->
                                    <div v-if="comment.showReplyInput" class="mt-3 flex items-start gap-2">
                                        <div class="bg-gradient-to-br from-teal-600 to-cyan-600 w-8 h-8 flex items-center justify-center rounded-full text-white font-bold text-xs flex-shrink-0">
                                            T
                                        </div>
                                        <div class="flex-1">
                                            <textarea
                                                v-model="comment.replyText"
                                                @keydown.enter.prevent="addReply(post, comment)"
                                                placeholder="Write a reply..."
                                                rows="2"
                                                class="w-full px-3 py-2 border-2 border-teal-200 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 resize-none text-sm"
                                            ></textarea>
                                            <div class="flex items-center justify-end gap-2 mt-2">
                                                <button @click="toggleReplyInput(comment)" class="px-3 py-1 text-gray-600 hover:text-gray-800 text-sm font-medium">Cancel</button>
                                                <button
                                                    @click="addReply(post, comment)"
                                                    :disabled="!comment.replyText || comment.replyText.trim() === ''"
                                                    class="px-3 py-1 bg-gradient-to-r from-teal-600 to-cyan-600 text-white rounded-lg font-semibold hover:from-teal-700 hover:to-cyan-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all text-sm">
                                                    Reply
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    <!-- Replies -->
                                    <div v-if="comment.replies && Array.isArray(comment.replies) && comment.replies.length > 0" class="mt-3 space-y-2 pl-4 border-l-2 border-teal-200">
                                        <div v-for="(reply, idx) in comment.replies" :key="`reply-${reply.id}-${idx}`" class="flex items-start gap-2">
                                            <div :class="getAvatarColor(reply.user)" class="w-8 h-8 flex items-center justify-center rounded-full text-white font-bold text-xs flex-shrink-0">
                                                {{ reply.user.charAt(0).toUpperCase() }}
                                            </div>
                                            <div class="flex-1 min-w-0">
                                                <div class="bg-gray-50 rounded-lg p-2">
                                                    <p class="font-semibold text-gray-900 text-xs">{{ reply.user }}</p>
                                                    <p class="text-gray-700 text-sm mt-0.5">{{ reply.text }}</p>
                                                </div>
                                                <div class="flex items-center gap-2 mt-1 text-xs text-gray-500">
                                                    <span>{{ reply.timestamp }}</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Add Comment Input -->
                        <div class="mt-4 flex items-start gap-3">
                            <div class="bg-gradient-to-br from-teal-600 to-cyan-600 w-10 h-10 flex items-center justify-center rounded-full text-white font-bold text-sm flex-shrink-0 ring-2 ring-teal-200 shadow-lg">
                                T
                            </div>
                            <div class="flex-1">
                                <textarea
                                    v-model="post.newComment"
                                    @keydown.enter.prevent="addComment(post)"
                                    placeholder="Write a comment..."
                                    rows="2"
                                    class="w-full px-4 py-3 border-2 border-teal-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-teal-500 resize-none"
                                ></textarea>
                                <div class="flex items-center justify-end mt-2">

                                    <button
                                        @click="addComment(post)"
                                        :disabled="!post.newComment || post.newComment.trim() === ''"
                                        class="px-5 py-2 bg-gradient-to-r from-teal-600 to-cyan-600 text-white rounded-lg font-semibold hover:from-teal-700 hover:to-cyan-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all shadow-md">
                                        Post
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Image Modal -->
        <div v-if="selectedImage"
            @click="selectedImage = null"
            class="fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4 backdrop-blur-sm">
            <button @click="selectedImage = null"
                class="absolute top-4 right-4 text-white hover:text-gray-300 transition-colors">
                <i class="pi pi-times text-3xl"></i>
            </button>
            <img :src="selectedImage"
                class="max-w-full max-h-full object-contain rounded-lg shadow-2xl"
                @click.stop>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '../../axios'; // Use configured axios with interceptors

// Define emits
const emit = defineEmits(['navigate']);

const isLoading = ref(false);
const posts = ref([]);
const selectedImage = ref(null);

// Avatar colors - Modern Blue-Green Theme
const avatarColors = [
  'bg-gradient-to-br from-teal-500 to-cyan-600',
  'bg-gradient-to-br from-cyan-500 to-blue-600',
  'bg-gradient-to-br from-blue-500 to-indigo-600',
  'bg-gradient-to-br from-teal-600 to-emerald-600',
  'bg-gradient-to-br from-amber-500 to-orange-500',
  'bg-gradient-to-br from-cyan-600 to-teal-700',
  'bg-gradient-to-br from-blue-600 to-cyan-700',
  'bg-gradient-to-br from-emerald-500 to-teal-600'
];

// Get consistent avatar color based on username
const getAvatarColor = (username) => {
  const hash = username.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  return avatarColors[hash % avatarColors.length];
};

// Load newsfeed from API
const loadNewsfeed = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get('/api/newsfeed/', {
      withCredentials: true
    });
    if (response.data && Array.isArray(response.data)) {
      // Map posts and load comments for each
      const postsPromises = response.data.map(async (post) => {
        // Load comments for this post
        let comments = [];
        try {
          const commentsResponse = await axios.get(`/api/posts/${post.id}/comments/`, {
            withCredentials: true
          });
          console.log(`📝 Comments for post ${post.id}:`, commentsResponse.data);
          comments = (commentsResponse.data || []).map(comment => ({
            id: comment.id,
            user: comment.user,
            text: comment.text,
            timestamp: comment.timestamp || getTimeAgo(comment.created_at),
            likes: comment.likes || 0,
            isLiked: comment.is_liked || false,
            replies: comment.replies || [],
            showReplyInput: false,
            replyText: ''
          }));
          console.log(`📝 Mapped ${comments.length} comments for post ${post.id}`);
        } catch (error) {
          console.error(`Error loading comments for post ${post.id}:`, error);
        }

        return {
          id: post.id,
          user: post.student_name,
          content: post.caption || 'No description provided',
          image: post.file_type === 'image' ? post.file_path : null,
          files: post.files || [],
          currentFileIndex: 0,
          likes: post.likes || 0,
          isLiked: post.is_liked || false,
          timestamp: getTimeAgo(post.posted_at),
          activityTitle: post.activity_title,
          activityType: post.activity_type,
          comments: comments,
          showComments: false,
          newComment: ''
        };
      });

      posts.value = await Promise.all(postsPromises);
      console.log('Loaded newsfeed for teacher:', posts.value);
    } else {
      posts.value = [];
    }
  } catch (error) {
    console.error('Error loading newsfeed:', error);
    posts.value = [];
  } finally {
    isLoading.value = false;
  }
};

// Helper function to get time ago
const getTimeAgo = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now - date) / 1000);

  if (seconds < 60) return 'Just now';
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days} day${days > 1 ? 's' : ''} ago`;
  return date.toLocaleDateString();
};

// Helper function to get total comments count (including replies)
const getTotalCommentsCount = (post) => {
  if (!post.comments || post.comments.length === 0) return 0;
  
  let total = post.comments.length;
  post.comments.forEach(comment => {
    if (comment.replies && comment.replies.length > 0) {
      total += comment.replies.length;
    }
  });
  return total;
};

// Toggle like functionality
const toggleLike = async (post) => {
  const wasLiked = post.isLiked;
  const wasLikes = post.likes;

  // Optimistic update
  post.isLiked = !post.isLiked;
  post.likes += post.isLiked ? 1 : -1;

  try {
    // Send like/unlike to backend
    const response = await axios.post(`/api/posts/${post.id}/like/`, {
      liked: post.isLiked
    }, {
      withCredentials: true
    });

    // Update with actual count from backend
    if (response.data) {
      post.likes = response.data.likes_count;
      post.isLiked = response.data.is_liked;
    }
  } catch (error) {
    console.error('Error toggling like:', error);
    // Revert on error
    post.isLiked = wasLiked;
    post.likes = wasLikes;
    alert('Failed to update like. Please try again.');
  }
};

// Toggle comments section
const toggleComments = (post) => {
  post.showComments = !post.showComments;
};

// Add comment functionality
const addComment = async (post) => {
  if (!post.newComment || post.newComment.trim() === '') return;

  const commentText = post.newComment.trim();

  try {
    // Send comment to backend
    const response = await axios.post(`/api/posts/${post.id}/comments/`, {
      text: commentText
    }, {
      withCredentials: true
    });

    // Use the comment returned from backend
    if (response.data && response.data.comment) {
      const newComment = {
        id: response.data.comment.id,
        user: response.data.comment.user,
        text: response.data.comment.text,
        timestamp: response.data.comment.timestamp || 'Just now',
        likes: 0,
        isLiked: false,
        replies: [],
        showReplyInput: false,
        replyText: ''
      };
      post.comments.push(newComment);
    }

    post.newComment = '';
    console.log('Comment added successfully');
  } catch (error) {
    console.error('Error adding comment:', error);
    alert('Failed to add comment. Please try again.');
  }
};

// Toggle comment like functionality
const toggleCommentLike = async (post, comment) => {
  const wasLiked = comment.isLiked;
  const wasLikes = comment.likes || 0;

  // Optimistic update
  comment.isLiked = !comment.isLiked;
  comment.likes = (comment.likes || 0) + (comment.isLiked ? 1 : -1);

  try {
    // Send comment like to backend
    const response = await axios.post(`/api/posts/${post.id}/comments/${comment.id}/like/`, {
      liked: comment.isLiked
    }, {
      withCredentials: true
    });

    // Update with actual count from backend
    if (response.data) {
      comment.likes = response.data.likes_count || 0;
      comment.isLiked = response.data.is_liked || false;
    }
  } catch (error) {
    console.error('Error toggling comment like:', error);
    // Revert on error
    comment.isLiked = wasLiked;
    comment.likes = wasLikes;
  }
};

// Toggle reply input visibility
const toggleReplyInput = (comment) => {
  comment.showReplyInput = !comment.showReplyInput;
  if (!comment.showReplyInput) {
    comment.replyText = '';
  }
};

// Add reply to comment
const addReply = async (post, comment) => {
  if (!comment.replyText || comment.replyText.trim() === '') return;

  const replyText = comment.replyText.trim();
  console.log(`📤 Sending reply to post ${post.id}, comment ${comment.id}`);

  try {
    // Send reply to backend
    const response = await axios.post(`/api/posts/${post.id}/comments/${comment.id}/replies/`, {
      text: replyText
    }, {
      withCredentials: true
    });

    console.log('📥 Reply response:', response.data);

    // Add reply to comment
    if (response.data && response.data.reply) {
      // Ensure replies array exists
      if (!comment.replies) {
        comment.replies = [];
      }

      const newReply = {
        id: response.data.reply.id,
        user: response.data.reply.user,
        text: response.data.reply.text,
        timestamp: response.data.reply.timestamp || getTimeAgo(response.data.reply.created_at)
      };

      // Push the reply to the array
      comment.replies.push(newReply);

      console.log('✅ Reply added to UI:', newReply);
      console.log('📝 Total replies for comment:', comment.replies.length);

      // Force Vue reactivity by reassigning
      comment.replies = [...comment.replies];
    } else {
      console.error('❌ Invalid reply response structure:', response.data);
    }

    comment.replyText = '';
    comment.showReplyInput = false;
    console.log('✅ Reply added successfully');
  } catch (error) {
    console.error('❌ Error adding reply:', error);
    console.error('Error response:', error.response?.data);
    alert('Failed to add reply. Please try again.');
  }
};

// Open image in modal
const openImageModal = (imageUrl) => {
  selectedImage.value = imageUrl;
};

// Handle image load error
const handleImageError = (event) => {
  console.error('Failed to load image:', event.target.src);
  event.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect fill="%23f3f4f6" width="400" height="300"/%3E%3Ctext fill="%239ca3af" font-family="sans-serif" font-size="18" dy="10.5" font-weight="bold" x="50%25" y="50%25" text-anchor="middle"%3EImage not found%3C/text%3E%3C/svg%3E';
};

// Get current file for a post
const getCurrentFile = (post) => {
  if (post.files && post.files.length > 0) {
    return post.files[post.currentFileIndex || 0];
  }
  return { file_path: post.image, file_type: 'image' };
};

// Navigate to previous file in post
const previousPostFile = (post) => {
  if (post.currentFileIndex > 0) {
    post.currentFileIndex--;
  }
};

// Navigate to next file in post
const nextPostFile = (post) => {
  if (post.files && post.currentFileIndex < post.files.length - 1) {
    post.currentFileIndex++;
  }
};

// Load on mount
onMounted(() => {
  loadNewsfeed();
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
.bg-pink-500 { background-color: #ec4899; }
.bg-teal-500 { background-color: #14b8a6; }

/* Smooth scrollbar for comments */
.max-h-96::-webkit-scrollbar {
    width: 6px;
}

.max-h-96::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

.max-h-96::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 10px;
}

.max-h-96::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

/* Image hover effects */
.group:hover .group-hover\:bg-black\/10 {
    background-color: rgba(0, 0, 0, 0.1);
}

.group:hover .group-hover\:opacity-100 {
    opacity: 1;
}

/* Backdrop blur for modal */
.backdrop-blur-sm {
    backdrop-filter: blur(4px);
}

/* Smooth animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.space-y-6 > div {
    animation: fadeIn 0.3s ease-out;
}

/* Focus styles for accessibility */
textarea:focus {
    outline: none;
}

button:focus-visible {
    outline: 2px solid #6366f1;
    outline-offset: 2px;
}

/* Responsive adjustments */
@media (max-width: 640px) {
    .max-w-5xl {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}
</style>
