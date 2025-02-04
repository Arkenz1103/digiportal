<template>
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-semibold">My Class / SY 2024-2025</h1>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-4">
        <!-- Grade 1 -->
        <Link :href="route('admin.class.show', { className: 'mathematics' })" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div class="h-32 flex items-center justify-center bg-blue-500 text-white text-2xl font-bold">
                    Grade 1
                </div>
                <div class="p-4">
                    <h3 class="text-lg font-semibold">Grade 1</h3>
                    <p class="text-gray-600">Details</p>
                </div>
            </div>
        </Link>

        <!-- Grade 2 -->
        <Link :href="route('admin.class.show', { className: 'english' })" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div class="h-32 flex items-center justify-center bg-red-500 text-white text-2xl font-bold">
                    Grade 2
                </div>
                <div class="p-4">
                    <h3 class="text-lg font-semibold">Grade 2</h3>
                    <p class="text-gray-600">Details</p>
                </div>
            </div>
        </Link>

        <!-- Grade 3 -->
        <Link :href="route('admin.class.show', { className: 'science' })" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div class="h-32 flex items-center justify-center bg-green-500 text-white text-2xl font-bold">
                    Grade 3
                </div>
                <div class="p-4">
                    <h3 class="text-lg font-semibold">Grade 3</h3>
                    <p class="text-gray-600">Details</p>
                </div>
            </div>
        </Link>

        <!-- Grade 4 -->
        <Link :href="route('admin.class.show', { className: 'history' })" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div class="h-32 flex items-center justify-center bg-blue-500 text-white text-2xl font-bold">
                    Grade 4
                </div>
                <div class="p-4">
                    <h3 class="text-lg font-semibold">Grade 4</h3>
                    <p class="text-gray-600">Details</p>
                </div>
            </div>
        </Link>

        <!-- Grade 5 -->
        <Link :href="route('admin.class.show', { className: 'TLE' })" class="block">
            <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div class="h-32 flex items-center justify-center bg-red-500 text-white text-2xl font-bold">
                    Grade 5
                </div>
                <div class="p-4">
                    <h3 class="text-lg font-semibold">Grade 5</h3>
                    <p class="text-gray-600">Details</p>
                </div>
            </div>
        </Link>
    </div>
</template>
