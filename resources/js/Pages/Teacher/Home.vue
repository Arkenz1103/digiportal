<template>
    <!-- Back to Home Button -->
    <div class="absolute top-4 left-4 z-50">
        <button 
            @click="emit('navigate', 'landing')"
            class="bg-white text-[#6366F1] px-6 py-2 rounded-full hover:bg-gray-100 transition-all hover:shadow-lg hover:-translate-y-0.5 font-semibold flex items-center gap-2 shadow-lg"
        >
            <i class="pi pi-arrow-left"></i>
            Back to Home
        </button>
    </div>

    <div class="p-6 max-w-4xl mx-auto">
        <!-- Posts Feed -->
        <div class="space-y-6">
            <!-- Watercolor Painting Post -->
            <div class="bg-white p-6 rounded-2xl shadow-lg">
                <div class="flex items-center gap-4 mb-4">
                    <div class="bg-blue-500 text-white font-bold w-12 h-12 flex items-center justify-center rounded-full">
                        E
                    </div>
                    <div>
                        <h3 class="font-semibold">Emma Garcia</h3>
                        <p class="text-sm text-gray-500">15 minutes ago</p>
                    </div>
                </div>

                <p class="mb-4">My watercolor landscape inspired by our field trip to the mountains last week. Used techniques we learned in class about wet-on-wet blending. 🏔️🎨</p>

                <img src="https://images.unsplash.com/photo-1579762715118-a6f1d4b934f1?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80" 
                    class="w-full h-auto max-h-96 object-contain rounded-xl mb-4">

                <div class="flex items-center gap-4 pt-4 border-t">
                    <button @click="toggleLike(posts[0])" 
                        class="flex items-center gap-2 px-4 py-2 rounded-xl transition-colors"
                        :class="posts[0].isLiked ? 'bg-red-50 text-red-500' : 'bg-gray-100 hover:bg-gray-200'">
                        <i class="pi" :class="posts[0].isLiked ? 'pi-heart-fill' : 'pi-heart'"></i>
                        <span>{{ posts[0].likes }} Likes</span>
                    </button>

                    <button class="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-xl">
                        <i class="pi pi-comments"></i>
                        <span>3 Comments</span>
                    </button>
                </div>

                <!-- Comments Section -->
                <div class="mt-4 space-y-3">
                    <div class="flex items-start gap-3 bg-gray-50 p-3 rounded-xl">
                        <div class="bg-green-500 text-white font-bold w-8 h-8 flex items-center justify-center rounded-full text-sm">
                            M
                        </div>
                        <div>
                            <p class="font-medium">Ms. Parker</p>
                            <p class="text-gray-700">Beautiful color blending, Emma! You've really mastered the technique we practiced.</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3 bg-gray-50 p-3 rounded-xl">
                        <div class="bg-purple-500 text-white font-bold w-8 h-8 flex items-center justify-center rounded-full text-sm">
                            L
                        </div>
                        <div>
                            <p class="font-medium">Lucas Thompson</p>
                            <p class="text-gray-700">The way you did the sky is amazing! Can you show me how you did that?</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Clay Sculpture Post -->
            <div class="bg-white p-6 rounded-2xl shadow-lg">
                <div class="flex items-center gap-4 mb-4">
                    <div class="bg-purple-500 text-white font-bold w-12 h-12 flex items-center justify-center rounded-full">
                        S
                    </div>
                    <div>
                        <h3 class="font-semibold">Sophie Chen</h3>
                        <p class="text-sm text-gray-500">2 hours ago</p>
                    </div>
                </div>

                <p class="mb-4">Finished my clay sculpture of an owl! It took three art classes to complete. The hardest part was the feather details. 🦉</p>

                <img src="https://images.unsplash.com/photo-1605000797499-95a51c5269ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80" 
                    class="w-full h-auto max-h-96 object-contain rounded-xl mb-4">

                <div class="flex items-center gap-4 pt-4 border-t">
                    <button @click="toggleLike(posts[1])" 
                        class="flex items-center gap-2 px-4 py-2 rounded-xl transition-colors"
                        :class="posts[1].isLiked ? 'bg-red-50 text-red-500' : 'bg-gray-100 hover:bg-gray-200'">
                        <i class="pi" :class="posts[1].isLiked ? 'pi-heart-fill' : 'pi-heart'"></i>
                        <span>{{ posts[1].likes }} Likes</span>
                    </button>

                    <button class="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-xl">
                        <i class="pi pi-comments"></i>
                        <span>5 Comments</span>
                    </button>
                </div>

                <!-- Comments Section -->
                <div class="mt-4 space-y-3">
                    <div class="flex items-start gap-3 bg-gray-50 p-3 rounded-xl">
                        <div class="bg-blue-500 text-white font-bold w-8 h-8 flex items-center justify-center rounded-full text-sm">
                            A
                        </div>
                        <div>
                            <p class="font-medium">Alex Kim</p>
                            <p class="text-gray-700">The texture looks so real! How did you make the feathers?</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3 bg-gray-50 p-3 rounded-xl">
                        <div class="bg-yellow-500 text-white font-bold w-8 h-8 flex items-center justify-center rounded-full text-sm">
                            M
                        </div>
                        <div>
                            <p class="font-medium">Mr. Rodriguez</p>
                            <p class="text-gray-700">Excellent craftsmanship, Sophie! Your attention to detail is impressive.</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Collage Art Post -->
            <div class="bg-white p-6 rounded-2xl shadow-lg">
                <div class="flex items-center gap-4 mb-4">
                    <div class="bg-red-500 text-white font-bold w-12 h-12 flex items-center justify-center rounded-full">
                        N
                    </div>
                    <div>
                        <h3 class="font-semibold">Noah Martinez</h3>
                        <p class="text-sm text-gray-500">1 day ago</p>
                    </div>
                </div>

                <p class="mb-4">My mixed media collage about ocean conservation. Used recycled magazines, acrylic paint, and beach sand. 🌊♻️</p>

                <img src="https://images.unsplash.com/photo-1534945773093-9c5332a4a9a3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80" 
                    class="w-full h-auto max-h-96 object-contain rounded-xl mb-4">

                <div class="flex items-center gap-4 pt-4 border-t">
                    <button @click="toggleLike(posts[2])" 
                        class="flex items-center gap-2 px-4 py-2 rounded-xl transition-colors"
                        :class="posts[2].isLiked ? 'bg-red-50 text-red-500' : 'bg-gray-100 hover:bg-gray-200'">
                        <i class="pi" :class="posts[2].isLiked ? 'pi-heart-fill' : 'pi-heart'"></i>
                        <span>{{ posts[2].likes }} Likes</span>
                    </button>

                    <button class="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-xl">
                        <i class="pi pi-comments"></i>
                        <span>7 Comments</span>
                    </button>
                </div>

                <!-- Comments Section -->
                <div class="mt-4 space-y-3">
                    <div class="flex items-start gap-3 bg-gray-50 p-3 rounded-xl">
                        <div class="bg-green-500 text-white font-bold w-8 h-8 flex items-center justify-center rounded-full text-sm">
                            E
                        </div>
                        <div>
                            <p class="font-medium">Emma Garcia</p>
                            <p class="text-gray-700">This is so creative! I love how you incorporated real sand.</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3 bg-gray-50 p-3 rounded-xl">
                        <div class="bg-indigo-500 text-white font-bold w-8 h-8 flex items-center justify-center rounded-full text-sm">
                            T
                        </div>
                        <div>
                            <p class="font-medium">Teacher Sarah</p>
                            <p class="text-gray-700">Powerful message and excellent execution! Would you like to display this in the school gallery?</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

// Define emits
const emit = defineEmits(['navigate']);

const posts = ref([
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