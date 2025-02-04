<template>
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-semibold">Class/ Grade 1   </h1>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Mathematics Class Card -->
        <Link :href="route('admin.class.show', { className: 'mathematics' })" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div class="h-48 flex items-center justify-center bg-blue-500 text-white text-3xl font-bold">
                    Mathematics
                </div>
                <div class="p-4 bg-gray-100">
                    <h3 class="text-lg font-semibold">Mathematics</h3>
                    <p class="text-gray-600">Grade 1 - A</p>
                    <p class="text-gray-600">MW(7:00am-8:00am)</p>
                </div>
            </div>
        </Link>

        <!-- English Class Card -->
        <Link :href="route('admin.class.show', { className: 'english' })" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div class="h-48 flex items-center justify-center bg-red-500 text-white text-3xl font-bold">
                    English
                </div>
                <div class="p-4 bg-gray-100">
                    <h3 class="text-lg font-semibold">English</h3>
                    <p class="text-gray-600">Grade 1 - A</p>
                    <p class="text-gray-600">TT(8:00am-9:00am)</p>
                </div>
            </div>
        </Link>

        <!-- Science Class Card -->
        <Link :href="route('admin.class.show', { className: 'science' })" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div class="h-48 flex items-center justify-center bg-green-500 text-white text-3xl font-bold">
                    Science
                </div>
                <div class="p-4 bg-gray-100">
                    <h3 class="text-lg font-semibold">Science</h3>
                    <p class="text-gray-600">Grade 1 - A</p>
                    <p class="text-gray-600">WF(9:00am-10:00am)</p>
                </div>
            </div>
        </Link>

        <!-- History Class Card -->
        <Link :href="route('admin.class.show', { className: 'history' })" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div class="h-48 flex items-center justify-center bg-blue-500 text-white text-3xl font-bold">
                    History
                </div>
                <div class="p-4 bg-gray-100">
                    <h3 class="text-lg font-semibold">History</h3>
                    <p class="text-gray-600">Grade 1 - A</p>
                    <p class="text-gray-600">TH(10:00am-11:00am)</p>
                </div>
            </div>
        </Link>

        <!-- TLE Class Card -->
        <Link :href="route('admin.class.show', { className: 'TLE' })" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div class="h-48 flex items-center justify-center bg-red-500 text-white text-3xl font-bold">
                    TLE
                </div>
                <div class="p-4 bg-gray-100">
                    <h3 class="text-lg font-semibold">TLE</h3>
                    <p class="text-gray-600">Grade 1 - A</p>
                    <p class="text-gray-600">TH(11:00am-12:00am)</p>
                </div>
            </div>
        </Link>
        </div>
</template>

<script setup>
import { Link } from '@inertiajs/vue3';
</script>
