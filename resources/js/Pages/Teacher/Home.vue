<template>
    <Head title="Student Newsfeed" />

    <div class="p-6 max-w-4xl mx-auto">
        <!-- Post Creation Section -->
        <div class="bg-white p-6 rounded-2xl shadow-lg border border-gray-200">
            <div class="flex items-center gap-4">
                <div class="bg-gradient-to-r from-blue-500 to-blue-700 text-white font-bold w-12 h-12 flex items-center justify-center rounded-full shadow-md">
                    {{ userInitial }}
                </div>
                <input
                    v-model="newPostContent"
                    type="text"
                    placeholder="What's on your mind?"
                    class="flex-grow p-4 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                />
            </div>

            <!-- List Items Section (Shows when List button is clicked) -->
            <div v-if="showListInput" class="mt-4">
                <div class="space-y-2">
                    <div v-for="(item, index) in listItems" :key="index" class="flex items-center gap-2">
                        <input
                            v-model="listItems[index]"
                            type="text"
                            :placeholder="`List item ${index + 1}`"
                            class="flex-grow p-2 bg-gray-50 border border-gray-200 rounded-lg"
                        />
                        <button @click="removeListItem(index)" 
                            class="text-red-500 hover:text-red-700">
                            <i class="pi pi-times"></i>
                        </button>
                    </div>
                    <button @click="addListItem" 
                        class="text-blue-600 hover:text-blue-800 text-sm flex items-center gap-1">
                        <i class="pi pi-plus"></i>
                        Add Item
                    </button>
                </div>
            </div>

            <!-- Image Preview Section -->
            <div v-if="selectedImage" class="mt-4">
                <div class="relative inline-block">
                    <img :src="selectedImage" class="max-h-48 rounded-lg">
                    <button @click="removeImage" 
                        class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600">
                        <i class="pi pi-times"></i>
                    </button>
                </div>
            </div>

            <!-- Tagged Friends Section -->
            <div v-if="showTagInput" class="mt-4">
                <div class="relative">
                    <input
                        v-model="tagSearchQuery"
                        type="text"
                        placeholder="Search friends..."
                        class="w-full p-2 bg-gray-50 border border-gray-200 rounded-lg"
                        @input="searchFriends"
                    />
                    <!-- Search Results -->
                    <div v-if="showTagResults" 
                        class="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg">
                        <div v-for="friend in filteredFriends" 
                            :key="friend.id"
                            @click="tagFriend(friend)"
                            class="p-2 hover:bg-gray-50 cursor-pointer flex items-center gap-2">
                            <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                                {{ friend.name.charAt(0) }}
                            </div>
                            {{ friend.name }}
                        </div>
                    </div>
                </div>
                <!-- Tagged Friends List -->
                <div class="flex flex-wrap gap-2 mt-2">
                    <div v-for="friend in taggedFriends" 
                        :key="friend.id"
                        class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full flex items-center gap-2">
                        {{ friend.name }}
                        <button @click="untagFriend(friend)" class="hover:text-blue-900">
                            <i class="pi pi-times"></i>
                        </button>
                    </div>
                </div>
            </div>

            <div class="flex items-center justify-between mt-4 border-t pt-4">
                <button @click="toggleList" 
                    class="flex items-center gap-2 px-4 py-2 rounded-xl transition-all"
                    :class="showListInput ? 'bg-blue-100 text-blue-700' : 'bg-gray-50 text-gray-700 hover:bg-gray-100'">
                    <i class="pi pi-list"></i>
                    <span>List</span>
                </button>
                
                <label class="flex items-center gap-2 px-4 py-2 bg-gray-50 text-gray-700 hover:bg-gray-100 rounded-xl transition-all cursor-pointer">
                    <i class="pi pi-image"></i>
                    <span>Photo/Video</span>
                    <input
                        type="file"
                        accept="image/*"
                        class="hidden"
                        @change="handleImageUpload"
                    />
                </label>

                <button @click="toggleTagFriends"
                    class="flex items-center gap-2 px-4 py-2 rounded-xl transition-all"
                    :class="showTagInput ? 'bg-blue-100 text-blue-700' : 'bg-gray-50 text-gray-700 hover:bg-gray-100'">
                    <i class="pi pi-users"></i>
                    <span>Tag Friends</span>
                </button>
            </div>

            <!-- Post Button -->
            <div class="mt-4 flex justify-end">
                <button @click="createPost"
                    class="px-6 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all">
                    Post
                </button>
            </div>
        </div>

        <!-- Posts Feed -->
        <div class="space-y-6 mt-6">
            <div v-for="post in posts" :key="post.id" 
                class="bg-white p-6 rounded-2xl shadow-lg border border-gray-200 hover:shadow-xl transition-all">
                <!-- User Info -->
                <div class="flex items-center gap-4 mb-4">
                    <div class="bg-gradient-to-r from-blue-500 to-blue-700 text-white font-bold w-12 h-12 flex items-center justify-center rounded-full shadow-md">
                        {{ post.user.charAt(0) }}
                    </div>
                    <div>
                        <h3 class="font-semibold text-gray-900">{{ post.user }}</h3>
                        <p class="text-sm text-gray-500">{{ post.timestamp }} • {{ post.datePosted }}</p>
                    </div>
                </div>

                <!-- Post Content -->
                <p class="text-gray-800 mb-4 whitespace-pre-line">{{ post.content }}</p>

                <!-- Post Image -->
                <img v-if="post.image" :src="post.image" 
                    class="w-full h-64 object-cover rounded-xl shadow-md mb-4">

                <!-- Actions -->
                <div class="flex items-center gap-4 border-t pt-4">
                    <button @click="toggleLike(post)"
                        class="flex items-center gap-2 px-4 py-2 rounded-xl transition-all"
                        :class="post.isLiked ? 'bg-red-50 text-red-600' : 'bg-gray-50 text-gray-600 hover:bg-gray-100'">
                        <i class="pi" :class="post.isLiked ? 'pi-heart-fill' : 'pi-heart'"></i>
                        <span>{{ post.likes }} Loves</span>
                    </button>

                    <button class="flex items-center gap-2 px-4 py-2 bg-gray-50 text-gray-600 hover:bg-gray-100 rounded-xl transition-all">
                        <i class="pi pi-comments"></i>
                        <span>{{ post.comments.length }} Comments</span>
                    </button>
                </div>

                <!-- Comments Section -->
                <div class="mt-4 space-y-4">
                    <div v-for="comment in post.comments" :key="comment.id" 
                        class="flex items-start gap-3 bg-gray-50 p-3 rounded-xl">
                        <div class="bg-gradient-to-r from-blue-500 to-blue-700 text-white font-bold w-8 h-8 flex items-center justify-center rounded-full shadow-md text-sm">
                            {{ comment.user.charAt(0) }}
                        </div>
                        <div>
                            <p class="font-medium text-gray-900">{{ comment.user }}</p>
                            <p class="text-gray-700">{{ comment.text }}</p>
                        </div>
                    </div>

                    <!-- Comment Input -->
                    <div class="flex items-center gap-3 mt-4">
                        <div class="bg-gradient-to-r from-blue-500 to-blue-700 text-white font-bold w-8 h-8 flex items-center justify-center rounded-full shadow-md text-sm">
                            {{ userInitial }}
                        </div>
                        <input
                            type="text"
                            placeholder="Write a comment..."
                            class="flex-grow p-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { Head } from '@inertiajs/vue3';

const userInitial = computed(() => 'S');

// New post creation state
const newPostContent = ref('');
const showListInput = ref(false);
const listItems = ref(['']);
const selectedImage = ref(null);
const showTagInput = ref(false);
const tagSearchQuery = ref('');
const showTagResults = ref(false);
const taggedFriends = ref([]);

// Sample friends data
const friends = ref([
    { id: 1, name: 'Emma Garcia' },
    { id: 2, name: 'Lucas Thompson' },
    { id: 3, name: 'Sophie Chen' },
    { id: 4, name: 'Noah Martinez' },
    { id: 5, name: 'Olivia Williams' },
    { id: 6, name: 'Ethan Brown' }
]);

// Computed property for filtered friends
const filteredFriends = computed(() => {
    if (!tagSearchQuery.value) return friends.value;
    return friends.value.filter(friend => 
        friend.name.toLowerCase().includes(tagSearchQuery.value.toLowerCase()) &&
        !taggedFriends.value.some(tagged => tagged.id === friend.id)
    );
});

// List functionality
const toggleList = () => {
    showListInput.value = !showListInput.value;
    if (!showListInput.value) {
        listItems.value = [''];
    }
};

const addListItem = () => {
    listItems.value.push('');
};

const removeListItem = (index) => {
    listItems.value.splice(index, 1);
    if (listItems.value.length === 0) {
        listItems.value = [''];
    }
};

// Image functionality
const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            selectedImage.value = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};

const removeImage = () => {
    selectedImage.value = null;
};

// Tag friends functionality
const toggleTagFriends = () => {
    showTagInput.value = !showTagInput.value;
    if (!showTagInput.value) {
        tagSearchQuery.value = '';
        showTagResults.value = false;
    }
};

const searchFriends = () => {
    showTagResults.value = true;
};

const tagFriend = (friend) => {
    if (!taggedFriends.value.some(tagged => tagged.id === friend.id)) {
        taggedFriends.value.push(friend);
    }
    tagSearchQuery.value = '';
    showTagResults.value = false;
};

const untagFriend = (friend) => {
    taggedFriends.value = taggedFriends.value.filter(f => f.id !== friend.id);
};

// Create post
const createPost = () => {
    if (!newPostContent.value.trim() && !selectedImage.value && listItems.value[0] === '') {
        return; // Don't create empty posts
    }

    const newPost = {
        id: Date.now(),
        user: "Current User",
        content: newPostContent.value,
        image: selectedImage.value,
        likes: 0,
        isLiked: false,
        timestamp: "Just now",
        datePosted: new Date().toLocaleDateString(),
        comments: []
    };

    // Add list items if any
    if (showListInput.value && listItems.value[0] !== '') {
        newPost.content += '\n\nList:\n' + listItems.value
            .filter(item => item.trim())
            .map(item => `• ${item}`)
            .join('\n');
    }

    // Add tagged friends if any
    if (taggedFriends.value.length > 0) {
        newPost.content += '\n\nWith: ' + taggedFriends.value
            .map(friend => friend.name)
            .join(', ');
    }

    posts.value.unshift(newPost);

    // Reset all inputs
    newPostContent.value = '';
    showListInput.value = false;
    listItems.value = [''];
    selectedImage.value = null;
    showTagInput.value = false;
    taggedFriends.value = [];
    tagSearchQuery.value = '';
};

// Existing posts data
const posts = ref([
  {
    id: 1,
    user: "Emma Garcia",
    content: "Look at my watercolor painting of our family! 🎨 We learned about primary and secondary colors in art class today. I mixed blue and yellow to make green for the trees! Thank you Ms. Parker for teaching us color theory! 🌈 #ArtClass #Grade3Art",
    image: "/assets/images/watercolor-family.jpg",
    likes: 24,
    isLiked: false,
    timestamp: "15 minutes ago",
    datePosted: "March 15, 2024",
    comments: [
      {
        id: 1,
        user: "Ms. Parker",
        text: "Beautiful work, Emma! Your color mixing skills are improving so much! 🎨"
      },
      {
        id: 2,
        user: "Sarah Lee",
        text: "I love how you drew your family! The colors are so bright and happy! 😊"
      }
    ]
  },
  {
    id: 2,
    user: "Lucas Thompson",
    content: "My first book report! 📚 I read 'Charlotte's Web' and made this diorama showing Wilbur and Charlotte in the barn. It was so fun using cotton balls for the spider web! #Reading #Grade2 #BookReport",
    image: "/assets/images/book-diorama.jpg",
    likes: 31,
    isLiked: true,
    timestamp: "2 hours ago",
    datePosted: "March 15, 2024",
    comments: [
      {
        id: 1,
        user: "Mrs. Rodriguez",
        text: "Amazing attention to detail, Lucas! I love how you included all the main characters! 👏"
      },
      {
        id: 2,
        user: "Reading Buddy Jenny",
        text: "Your diorama looks just like the story! Great job! 🌟"
      }
    ]
  },
  {
    id: 3,
    user: "Sophie Chen",
    content: "Today in science class we learned about plants! 🌱 Here's my plant growth experiment - I'm growing beans in different conditions to see what they need to grow best. Day 1 of recording in my science journal! #Science #Grade4 #PlantExperiment",
    image: "/assets/images/plant-experiment.jpg",
    likes: 19,
    isLiked: false,
    timestamp: "4 hours ago",
    datePosted: "March 15, 2024",
    comments: [
      {
        id: 1,
        user: "Mr. Wilson",
        text: "Great start to your experiment, Sophie! Remember to water them daily! 🌿"
      },
      {
        id: 2,
        user: "Alex Kim",
        text: "My beans are growing too! Let's compare results next week! 🌱"
      }
    ]
  },
  {
    id: 4,
    user: "Noah Martinez",
    content: "My multiplication tables practice sheet! ✏️ Got all my times tables right up to 12! Been practicing every day with flash cards. Math is getting more fun! #Math #Grade3 #Multiplication",
    image: "/assets/images/math-practice.jpg",
    likes: 27,
    isLiked: false,
    timestamp: "Yesterday",
    datePosted: "March 14, 2024",
    comments: [
      {
        id: 1,
        user: "Ms. Thompson",
        text: "Excellent work, Noah! Your practice is really paying off! 💯"
      },
      {
        id: 2,
        user: "Math Buddy Sam",
        text: "Way to go! Want to practice together at recess tomorrow? 🔢"
      }
    ]
  },
  {
    id: 5,
    user: "Olivia Williams",
    content: "My 'All About Me' poster for show and tell! 🌟 I included pictures of my favorite things, my family, and my pet goldfish Bubbles. Can't wait to present it tomorrow! #ShowAndTell #Grade1",
    image: "/assets/images/about-me-poster.jpg",
    likes: 35,
    isLiked: true,
    timestamp: "2 days ago",
    datePosted: "March 13, 2024",
    comments: [
      {
        id: 1,
        user: "Mrs. Anderson",
        text: "Such a creative poster, Olivia! Love all the colorful decorations! ⭐"
      },
      {
        id: 2,
        user: "Emily Davis",
        text: "Your goldfish drawing is so cute! Can't wait to see your presentation! 🐠"
      }
    ]
  },
  {
    id: 6,
    user: "Ethan Brown",
    content: "Look at our class recycling project! ♻️ We collected plastic bottles and turned them into a rainbow garden! Each color has different flowers we're going to grow. Working together to help our Earth! #EarthDay #Grade4 #Recycling",
    image: "/assets/images/recycling-garden.jpg",
    likes: 42,
    isLiked: false,
    timestamp: "3 days ago",
    datePosted: "March 12, 2024",
    comments: [
      {
        id: 1,
        user: "Green Team Leader",
        text: "What a creative way to reuse plastic bottles! Great job everyone! 🌍"
      },
      {
        id: 2,
        user: "Principal Johnson",
        text: "This is exactly the kind of project that makes our school special. Well done! 🌱"
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