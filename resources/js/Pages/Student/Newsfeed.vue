<template>
    <div class="p-6 max-w-4xl mx-auto">
        <!-- Loading State -->
        <div v-if="isLoading" class="flex justify-center items-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>

        <!-- Empty State -->
        <div v-else-if="posts.length === 0" class="text-center py-12">
            <i class="pi pi-inbox text-6xl text-gray-400 mb-4"></i>
            <p class="text-gray-500 text-lg">No posts yet</p>
            <p class="text-gray-400 text-sm">Approved student work will appear here</p>
        </div>

        <!-- Posts Feed -->
        <div v-else class="space-y-6">
            <!-- Dynamic Post -->
            <div v-for="post in posts" :key="post.id" class="bg-white p-6 rounded-2xl shadow-lg">
                <div class="flex items-center gap-4 mb-4">
                    <div class="bg-indigo-500 text-white font-bold w-12 h-12 flex items-center justify-center rounded-full">
                        {{ post.user.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                        <h3 class="font-semibold">{{ post.user }}</h3>
                        <p class="text-sm text-gray-500">{{ post.timestamp }}</p>
                        <p v-if="post.activityTitle" class="text-xs text-indigo-600">{{ post.activityType }} - {{ post.activityTitle }}</p>
                    </div>
                </div>

                <p class="mb-4">{{ post.content }}</p>

                <img v-if="post.image" 
                    :src="post.image" 
                    :alt="post.content"
                    class="w-full h-auto max-h-96 object-contain rounded-xl mb-4">

                <div class="flex items-center gap-4 pt-4 border-t">
                    <button @click="toggleLike(post)" 
                        class="flex items-center gap-2 px-4 py-2 rounded-xl transition-colors"
                        :class="post.isLiked ? 'bg-red-50 text-red-500' : 'bg-gray-100 hover:bg-gray-200'">
                        <i class="pi" :class="post.isLiked ? 'pi-heart-fill' : 'pi-heart'"></i>
                        <span>{{ post.likes }} Likes</span>
                    </button>

                    <button class="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-xl">
                        <i class="pi pi-comments"></i>
                        <span>{{ post.comments.length }} Comments</span>
                    </button>
                </div>

                <!-- Comments Section -->
                <div v-if="post.comments.length > 0" class="mt-4 space-y-3">
                    <div v-for="comment in post.comments" :key="comment.id" class="flex items-start gap-3 bg-gray-50 p-3 rounded-xl">
                        <div class="bg-green-500 text-white font-bold w-8 h-8 flex items-center justify-center rounded-full text-sm">
                            {{ comment.user.charAt(0).toUpperCase() }}
                        </div>
                        <div>
                            <p class="font-medium">{{ comment.user }}</p>
                            <p class="text-gray-700">{{ comment.text }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Define emits
const emit = defineEmits(['navigate']);

const isLoading = ref(false);
const posts = ref([]);

// Load newsfeed from API
const loadNewsfeed = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get('/api/newsfeed/');
    if (response.data && Array.isArray(response.data)) {
      posts.value = response.data.map(submission => ({
        id: submission.id,
        user: submission.student_name || submission.student?.username || 'Student',
        content: submission.caption || 'No description provided',
        image: submission.file_type === 'image' ? submission.file_path : null,
        likes: 0,
        isLiked: false,
        timestamp: getTimeAgo(submission.submitted_at),
        activityTitle: submission.activity_title || null,
        activityType: submission.activity_type || null,
        comments: []
      }));
      console.log('Loaded newsfeed:', posts.value);
    } else {
      posts.value = [];
    }
  } catch (error) {
    console.error('Error loading newsfeed:', error);
    // Check if it's an authentication error
    if (error.response?.status === 403) {
      console.warn('Authentication required for newsfeed. User may not be logged in.');
    }
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

// Load on mount
onMounted(() => {
  loadNewsfeed();
});

// Old hardcoded data for reference
const oldPosts = ref([
  {
    id: 1,
    user: "Emma Garcia",
    content: "My watercolor landscape inspired by our field trip to the mountains last week. Used techniques we learned in class about wet-on-wet blending. 🏔️🎨",
    image: "https://images.unsplash.com/photo-1579762715118-a6f1d4b934f1?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
    likes: 24,
    isLiked: false,
    timestamp: "15 minutes ago",
    comments: [
      {
        id: 1,
        user: "Ms. Parker",
        text: "Beautiful color blending, Emma! You've really mastered the technique we practiced."
      },
      {
        id: 2,
        user: "Lucas Thompson",
        text: "The way you did the sky is amazing! Can you show me how you did that?"
      }
    ]
  },
  {
    id: 2,
    user: "Sophie Chen",
    content: "Finished my clay sculpture of an owl! It took three art classes to complete. The hardest part was the feather details. 🦉",
    image: "https://images.unsplash.com/photo-1605000797499-95a51c5269ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
    likes: 32,
    isLiked: false,
    timestamp: "2 hours ago",
    comments: [
      {
        id: 1,
        user: "Alex Kim",
        text: "The texture looks so real! How did you make the feathers?"
      },
      {
        id: 2,
        user: "Mr. Rodriguez",
        text: "Excellent craftsmanship, Sophie! Your attention to detail is impressive."
      }
    ]
  },
  {
    id: 3,
    user: "Noah Martinez",
    content: "My mixed media collage about ocean conservation. Used recycled magazines, acrylic paint, and beach sand. 🌊♻️",
    image: "https://images.unsplash.com/photo-1534945773093-9c5332a4a9a3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
    likes: 41,
    isLiked: false,
    timestamp: "1 day ago",
    comments: [
      {
        id: 1,
        user: "Emma Garcia",
        text: "This is so creative! I love how you incorporated real sand."
      },
      {
        id: 2,
        user: "Teacher Sarah",
        text: "Powerful message and excellent execution! Would you like to display this in the school gallery?"
      }
    ]
  }
]);

const toggleLike = (post) => {
    post.isLiked = !post.isLiked;
    post.likes += post.isLiked ? 1 : -1;
};
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