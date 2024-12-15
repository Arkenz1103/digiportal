<template>
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-semibold">My Class / SY 2024-2025</h1>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Mathematics Class Card -->
        <Link :href="route('student.class.show', 'mathematics')" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <img src="https://radiant.edu.np/wp-content/uploads/2023/03/mmmmmmm.jpg" alt="Mathematics" class="w-full h-48 object-cover">
                <div class="p-4 bg-blue-100">
                    <h3 class="text-xl font-semibold mb-2">Mathematics</h3>
                    <p class="text-gray-600">Grade 1 - A</p>
                    <p class="text-gray-600">MW(7:00am-8:00am)</p>
                </div>
            </div>
        </Link>

        <!-- Science Class Card -->
        <Link :href="route('student.class.show', 'science')" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <img src="https://www.shutterstock.com/image-vector/word-design-science-illustration-260nw-767861248.jpg" alt="Science" class="w-full h-48 object-cover">
                <div class="p-4 bg-blue-100">
                    <h3 class="text-xl font-semibold mb-2">Science</h3>
                    <p class="text-gray-600">Grade 1 - A</p>
                    <p class="text-gray-600">MW(7:00am-8:00am)</p>
                </div>
            </div>
        </Link>

        <!-- English Class Card -->
        <Link :href="route('student.class.show', 'english')" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <img src="https://img.freepik.com/free-vector/hand-drawn-english-book-background_23-2149483336.jpg" alt="English" class="w-full h-48 object-cover">
                <div class="p-4 bg-blue-100">
                    <h3 class="text-xl font-semibold mb-2">English</h3>
                    <p class="text-gray-600">Grade 1 - A</p>
                    <p class="text-gray-600">MW(7:00am-8:00am)</p>
                </div>
            </div>
        </Link>
    </div>
</template>

<script setup>
import { Link } from '@inertiajs/vue3';
</script>
