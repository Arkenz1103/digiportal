<template>
    <Head :title="`| ${className}`"/>
    <div class="min-h-screen bg-gray-50">
        <!-- Class Header -->
        <div :class="[themeClasses.header, 'p-6 shadow-md rounded-[10px]']">
            <div class="flex justify-between items-center">
                <div>
                    <h1 :class="[themeClasses.badge, 'text-xl font-bold inline-block px-4 py-2 rounded-lg shadow-sm']">
                        {{ className }}
                    </h1>
                    <p class="text-white mt-2">Student: {{ auth.user.name }}</p>
                </div>
                <div class="flex items-center gap-4">
                    <button class="text-white hover:bg-white/20 p-2 rounded-full transition-colors">
                        <i class="pi pi-cog text-xl"></i>
                    </button>
                </div>
            </div>
            
            <!-- Navigation Tabs -->
            <div class="flex gap-4 mt-6">
                <button 
                    v-for="tab in tabs" 
                    :key="tab.id"
                    @click="activeTab = tab.id"
                    :class="[
                        'text-white px-6 py-2 rounded-t-lg transition-colors',
                        activeTab === tab.id ? 'bg-white/20 font-medium' : 'hover:bg-white/10'
                    ]"
                >
                    <i :class="['pi', tab.icon, 'mr-2']"></i>
                    {{ tab.name }}
                </button>
            </div>
        </div>

        <!-- Main Content Area -->
        <div class="flex gap-6 p-6">
            <!-- Right Content Area -->
            <div :class="[
                'bg-white rounded-[10px] shadow-sm w-full'
            ]">
                <template v-if="activeTab === 'portfolio'">
                    <div v-if="!portfolioCreated" class="p-8">
                        <div class="flex flex-col items-center justify-center text-center max-w-md mx-auto">
                            <!-- Portfolio Icon -->
                            <div class="w-32 h-32 mb-6">
                                <div class="bg-orange-100 w-full h-full rounded-lg flex items-center justify-center relative">
                                    <i class="pi pi-pencil text-orange-500 text-4xl"></i>
                                    <div class="absolute -top-2 -right-2">
                                        <i class="pi pi-sun text-orange-400 text-2xl"></i>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Inspirational Quote -->
                            <p class="text-gray-600 text-lg font-medium mb-2">
                                "Every output tells a story of creativity, perseverance, and excellence."
                            </p>
                            
                            <!-- No Results Message -->
                            <p class="text-gray-400 text-sm mb-6">No results for portfolio</p>
                            
                            <!-- Create Button -->
                            <button 
                                class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-full flex items-center gap-2 transition-colors"
                                @click="createPortfolio"
                            >
                                <i class="pi pi-plus"></i>
                                Create now
                            </button>
                        </div>
                    </div>
                    <div v-else class="p-6">
                        <!-- Portfolio Content -->
                        <div class="w-full" :class="{
                            'bg-white': selectedPortfolioTheme !== 'dark',
                            'bg-gray-900': selectedPortfolioTheme === 'dark'
                        }">
                            <!-- Toolbar -->
                            <div class="mb-6 shadow-sm p-4 rounded-lg flex justify-between items-center"
                                :class="{
                                    'bg-white': selectedPortfolioTheme === 'minimal',
                                    'bg-gradient-to-r from-purple-50 to-pink-50': selectedPortfolioTheme === 'creative',
                                    'bg-blue-50': selectedPortfolioTheme === 'professional',
                                    'bg-gradient-to-r from-emerald-50 to-teal-50': selectedPortfolioTheme === 'modern',
                                    'bg-gray-800': selectedPortfolioTheme === 'dark',
                                    'bg-gradient-to-r from-yellow-50 to-orange-50': selectedPortfolioTheme === 'playful'
                                }"
                            >
                                <div class="flex flex-col">
                                    <h2 class="text-3xl font-bold flex items-center gap-2"
                                        :class="{
                                            'text-gray-800': selectedPortfolioTheme === 'minimal',
                                            'text-purple-600': selectedPortfolioTheme === 'creative',
                                            'text-blue-800': selectedPortfolioTheme === 'professional',
                                            'text-emerald-600': selectedPortfolioTheme === 'modern',
                                            'text-white': selectedPortfolioTheme === 'dark',
                                            'text-orange-600': selectedPortfolioTheme === 'playful'
                                        }"
                                    >
                                        {{ selectedFolder ? selectedFolder.title : 'My Portfolio' }}
                                    </h2>
                                    <!-- Tabs for selected folder -->
                                    <div v-if="selectedFolder" class="flex space-x-4 mt-2">
                                        <button 
                                            v-for="tab in [
                                                { id: 'Recent', icon: 'pi-clock' },
                                                { id: 'Shared', icon: 'pi-share-alt' },
                                                { id: 'Favorites', icon: 'pi-star' }
                                            ]" 
                                            :key="tab.id"
                                            class="px-3 py-1 rounded-full text-sm transition-colors flex items-center gap-2"
                                            :class="[
                                                selectedTab === tab.id 
                                                    ? {
                                                        'bg-gray-200 text-gray-800': selectedPortfolioTheme === 'minimal',
                                                        'bg-purple-100 text-purple-600': selectedPortfolioTheme === 'creative',
                                                        'bg-blue-100 text-blue-600': selectedPortfolioTheme === 'professional',
                                                        'bg-emerald-100 text-emerald-600': selectedPortfolioTheme === 'modern',
                                                        'bg-gray-700 text-white': selectedPortfolioTheme === 'dark',
                                                        'bg-orange-100 text-orange-600': selectedPortfolioTheme === 'playful'
                                                    }
                                                    : 'text-gray-500 hover:text-gray-700'
                                            ]"
                                            @click="selectedTab = tab.id"
                                        >
                                            <i :class="['pi', tab.icon]"></i>
                                            {{ tab.id }}
                                        </button>
                                    </div>
                                </div>
                                <div class="flex space-x-3">
                                    <button v-if="selectedFolder" 
                                        @click="showAddProjectDialog = true"
                                        :class="[
                                            'px-4 py-2 rounded-lg flex items-center gap-2 transition-colors',
                                            {
                                                'bg-gray-900 text-white hover:bg-gray-800': selectedPortfolioTheme === 'minimal',
                                                'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-700 hover:to-pink-700': selectedPortfolioTheme === 'creative',
                                                'bg-blue-600 text-white hover:bg-blue-700': selectedPortfolioTheme === 'professional',
                                                'bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:from-emerald-700 hover:to-teal-700': selectedPortfolioTheme === 'modern',
                                                'bg-gray-700 text-white hover:bg-gray-600': selectedPortfolioTheme === 'dark',
                                                'bg-gradient-to-r from-yellow-500 to-orange-500 text-white hover:from-yellow-600 hover:to-orange-600': selectedPortfolioTheme === 'playful'
                                            }
                                        ]">
                                        <i class="pi pi-plus"></i>
                                        Add Project
                                    </button>
                                    <button v-if="!selectedFolder" 
                                        :class="[
                                            'px-4 py-2 rounded-lg flex items-center gap-2 transition-colors',
                                            {
                                                'bg-gray-900 text-white hover:bg-gray-800': selectedPortfolioTheme === 'minimal',
                                                'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-700 hover:to-pink-700': selectedPortfolioTheme === 'creative',
                                                'bg-blue-600 text-white hover:bg-blue-700': selectedPortfolioTheme === 'professional',
                                                'bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:from-emerald-700 hover:to-teal-700': selectedPortfolioTheme === 'modern',
                                                'bg-gray-700 text-white hover:bg-gray-600': selectedPortfolioTheme === 'dark',
                                                'bg-gradient-to-r from-yellow-500 to-orange-500 text-white hover:from-yellow-600 hover:to-orange-600': selectedPortfolioTheme === 'playful'
                                            }
                                        ]"
                                        @click="showNewFolderDialog = true">
                                        <i class="pi pi-folder"></i>
                                        New Folder
                                    </button>
                                </div>
                            </div>

                            <!-- Folder Grid -->
                            <div v-if="!selectedFolder" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                                <div v-for="folder in portfolioFolders" 
                                    :key="folder.id"
                                    @click="openFolderContent(folder)"
                                    class="group bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-all cursor-pointer p-6"
                                    :class="{
                                        'border-gray-200 hover:border-gray-300': selectedPortfolioTheme === 'minimal',
                                        'border-purple-100 hover:border-purple-200': selectedPortfolioTheme === 'creative',
                                        'border-blue-100 hover:border-blue-200': selectedPortfolioTheme === 'professional',
                                        'border-emerald-100 hover:border-emerald-200': selectedPortfolioTheme === 'modern',
                                        'border-gray-700 hover:border-gray-600': selectedPortfolioTheme === 'dark',
                                        'border-orange-100 hover:border-orange-200': selectedPortfolioTheme === 'playful'
                                    }">
                                    <!-- Folder Preview -->
                                    <div class="relative h-32 mb-4">
                                        <!-- Stacked Preview Images -->
                                        <div class="absolute top-0 right-0 w-24 h-28 flex items-center justify-center">
                                            <div class="absolute w-20 h-24 bg-gray-100 rounded-lg transform rotate-[-15deg] transition-transform group-hover:rotate-[-20deg]"></div>
                                            <div class="absolute w-20 h-24 bg-gray-200 rounded-lg transform rotate-[-5deg] transition-transform group-hover:rotate-[-10deg]"></div>
                                            <div class="absolute w-20 h-24 bg-gray-300 rounded-lg transform rotate-[5deg] transition-transform group-hover:rotate-[10deg]"></div>
                                        </div>
                                        <!-- Folder Title -->
                                        <h3 class="text-xl font-semibold text-gray-800 mb-1 relative z-10">{{ folder.title }}</h3>
                                        <span class="text-sm text-gray-500 relative z-10">{{ folder.items }} items</span>
                                    </div>
                                    
                                    <!-- Folder Description -->
                                    <p class="text-gray-600 text-sm">{{ folder.description }}</p>
                                </div>
                            </div>

                            <!-- Selected Folder Content -->
                            <div v-else class="space-y-6">
                                <!-- Back Button and Folder Header -->
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-2xl font-bold text-gray-800">{{ selectedFolder.title }}</h2>
                                    <button @click="selectedFolder = null" 
                                        :class="[
                                            'flex items-center gap-2 px-4 py-2 rounded-lg transition-colors',
                                            {
                                                'bg-gray-100 text-gray-700 hover:bg-gray-200': selectedPortfolioTheme === 'minimal',
                                                'bg-purple-50 text-purple-600 hover:bg-purple-100': selectedPortfolioTheme === 'creative',
                                                'bg-blue-50 text-blue-600 hover:bg-blue-100': selectedPortfolioTheme === 'professional',
                                                'bg-emerald-50 text-emerald-600 hover:bg-emerald-100': selectedPortfolioTheme === 'modern',
                                                'bg-gray-700 text-white hover:bg-gray-600': selectedPortfolioTheme === 'dark',
                                                'bg-orange-50 text-orange-600 hover:bg-orange-100': selectedPortfolioTheme === 'playful'
                                            }
                                        ]"
                                    >
                                        <i class="pi pi-arrow-left"></i>
                                        <span>Back to Folders</span>
                                    </button>
                                </div>

                                <!-- Activities Grid -->
                                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    <div v-for="(activity, index) in folderActivities" 
                                        :key="index"
                                        class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow"
                                        :class="{
                                            'border-gray-200': selectedPortfolioTheme === 'minimal',
                                            'border-purple-100': selectedPortfolioTheme === 'creative',
                                            'border-blue-100': selectedPortfolioTheme === 'professional',
                                            'border-emerald-100': selectedPortfolioTheme === 'modern',
                                            'border-gray-700': selectedPortfolioTheme === 'dark',
                                            'border-orange-100': selectedPortfolioTheme === 'playful'
                                        }">
                                        <!-- Activity Image -->
                                        <div class="aspect-video w-full bg-gray-100 relative">
                                            <img :src="activity.image" 
                                                :alt="activity.title"
                                                class="w-full h-full object-cover">
                                            <div class="absolute top-2 right-2">
                                                <span :class="[
                                                    'px-2 py-1 rounded-full text-xs font-medium',
                                                    {
                                                        'bg-green-100 text-green-700': activity.status === 'Completed',
                                                        'bg-yellow-100 text-yellow-700': activity.status === 'In Progress',
                                                        'bg-blue-100 text-blue-700': activity.status === 'New'
                                                    }
                                                ]">
                                                    {{ activity.status }}
                                                </span>
                                            </div>
                                        </div>
                                        
                                        <!-- Activity Content -->
                                        <div class="p-4">
                                            <h4 class="text-lg font-semibold text-gray-800 mb-2">{{ activity.title }}</h4>
                                            <p class="text-gray-600 text-sm mb-4 line-clamp-2">{{ activity.description }}</p>
                                            
                                            <!-- Activity Meta -->
                                            <div class="flex items-center justify-between text-sm">
                                                <span class="text-gray-500">{{ activity.date }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>

                <!-- Schedule Tab Content -->
                <template v-if="activeTab === 'schedule'">
                    <div class="p-6">
                        <!-- Calendar Header -->
                        <div class="flex justify-between items-center mb-6">
                            <h2 class="text-xl font-bold" :class="`text-${props.theme}-700`">NOVEMBER 2025</h2>
                            <div class="flex gap-4 items-center">
                                <span class="flex items-center gap-2">
                                    <div :class="`w-3 h-3 rounded-full bg-${props.theme}-100`"></div>
                                    <span class="text-sm text-gray-600">Class Day</span>
                                </span>
                                <span class="flex items-center gap-2">
                                    <div class="w-3 h-3 rounded-full bg-gray-100"></div>
                                    <span class="text-sm text-gray-600">No Class</span>
                                </span>
                            </div>
                        </div>

                        <!-- Days of the Week -->
                        <div class="grid grid-cols-7 text-center font-semibold text-gray-700 mb-4 bg-gray-50 p-3 rounded-lg">
                            <div>Mon</div>
                            <div>Tue</div>
                            <div>Wed</div>
                            <div>Thu</div>
                            <div>Fri</div>
                            <div class="text-red-500">Sat</div>
                            <div class="text-red-500">Sun</div>
                        </div>

                        <!-- Calendar Grid -->
                        <div class="grid grid-cols-7 gap-2">
                            <!-- Empty Spaces for the Start of the Month -->
                            <div v-for="i in 3" :key="'empty-' + i" class="p-4"></div>

                            <!-- Dates with Class Schedule -->
                            <div v-for="(day, date) in schedule" :key="date"
                                class="p-4 border rounded-lg hover:shadow-md cursor-pointer transition-all"
                                :class="{
                                    [`bg-${props.theme}-100 border-${props.theme}-200`]: isClassDay(date + 1),
                                    'bg-gray-50': !isClassDay(date + 1)
                                }"
                                @click="showScheduleDetails(date + 1)">
                                <div class="font-semibold text-gray-800">{{ date + 1 }}</div>
                                <div v-if="isClassDay(date + 1)" :class="`text-sm text-${props.theme}-600 mt-1`">
                                    {{ day.time }}
                                </div>
                            </div>
                        </div>

                        <!-- Current Schedule Display -->
                        <div v-if="selectedDate" :class="`mt-6 p-4 bg-${props.theme}-50 rounded-lg`">
                            <h3 :class="`font-semibold text-${props.theme}-800 mb-2`">
                                Selected Date: November {{ selectedDate }}
                            </h3>
                            <p v-if="isClassDay(selectedDate)" class="text-gray-700">
                                Class Time: {{ schedule[selectedDate - 1].time }}
                            </p>
                            <p v-else class="text-gray-700">
                                No class scheduled for this date
                            </p>
                        </div>
                    </div>
                </template>
            </div>
        </div>

        <!-- Portfolio Theme Selection Dialog -->
        <Dialog v-model:visible="showPortfolioThemeDialog" 
            modal 
            header="Choose Your Portfolio Theme" 
            :style="{ width: '80vw' }"
            :breakpoints="{ '960px': '85vw', '641px': '95vw' }">
            <div class="p-6">
                <h3 class="text-lg text-gray-700 mb-6">Select a theme that best represents your style</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    <!-- Minimal Theme -->
                    <div 
                        class="border rounded-xl p-4 cursor-pointer transition-all hover:shadow-lg"
                        :class="{ 'ring-2 ring-blue-500': selectedTheme === 'minimal' }"
                        @click="selectedTheme = 'minimal'"
                    >
                        <div class="bg-gray-100 h-40 rounded-lg mb-4 flex items-center justify-center">
                            <i class="pi pi-minus-circle text-4xl text-gray-400"></i>
                        </div>
                        <h4 class="font-medium text-gray-800">Minimal</h4>
                        <p class="text-sm text-gray-500">Clean and simple design focusing on content</p>
                    </div>

                    <!-- Creative Theme -->
                    <div 
                        class="border rounded-xl p-4 cursor-pointer transition-all hover:shadow-lg"
                        :class="{ 'ring-2 ring-blue-500': selectedTheme === 'creative' }"
                        @click="selectedTheme = 'creative'"
                    >
                        <div class="bg-gradient-to-br from-purple-100 to-pink-100 h-40 rounded-lg mb-4 flex items-center justify-center">
                            <i class="pi pi-palette text-4xl text-purple-400"></i>
                        </div>
                        <h4 class="font-medium text-gray-800">Creative</h4>
                        <p class="text-sm text-gray-500">Vibrant and artistic with dynamic layouts</p>
                    </div>

                    <!-- Professional Theme -->
                    <div 
                        class="border rounded-xl p-4 cursor-pointer transition-all hover:shadow-lg"
                        :class="{ 'ring-2 ring-blue-500': selectedTheme === 'professional' }"
                        @click="selectedTheme = 'professional'"
                    >
                        <div class="bg-blue-100 h-40 rounded-lg mb-4 flex items-center justify-center">
                            <i class="pi pi-briefcase text-4xl text-blue-400"></i>
                        </div>
                        <h4 class="font-medium text-gray-800">Professional</h4>
                        <p class="text-sm text-gray-500">Sophisticated and structured presentation</p>
                    </div>

                    <!-- Modern Theme -->
                    <div 
                        class="border rounded-xl p-4 cursor-pointer transition-all hover:shadow-lg"
                        :class="{ 'ring-2 ring-blue-500': selectedTheme === 'modern' }"
                        @click="selectedTheme = 'modern'"
                    >
                        <div class="bg-gradient-to-br from-emerald-100 to-teal-100 h-40 rounded-lg mb-4 flex items-center justify-center">
                            <i class="pi pi-compass text-4xl text-emerald-400"></i>
                        </div>
                        <h4 class="font-medium text-gray-800">Modern</h4>
                        <p class="text-sm text-gray-500">Contemporary design with bold elements</p>
                    </div>

                    <!-- Dark Theme -->
                    <div 
                        class="border rounded-xl p-4 cursor-pointer transition-all hover:shadow-lg"
                        :class="{ 'ring-2 ring-blue-500': selectedTheme === 'dark' }"
                        @click="selectedTheme = 'dark'"
                    >
                        <div class="bg-gray-900 h-40 rounded-lg mb-4 flex items-center justify-center">
                            <i class="pi pi-moon text-4xl text-gray-400"></i>
                        </div>
                        <h4 class="font-medium text-gray-800">Dark</h4>
                        <p class="text-sm text-gray-500">Elegant dark mode with high contrast</p>
                    </div>

                    <!-- Playful Theme -->
                    <div 
                        class="border rounded-xl p-4 cursor-pointer transition-all hover:shadow-lg"
                        :class="{ 'ring-2 ring-blue-500': selectedTheme === 'playful' }"
                        @click="selectedTheme = 'playful'"
                    >
                        <div class="bg-gradient-to-br from-yellow-100 via-orange-100 to-red-100 h-40 rounded-lg mb-4 flex items-center justify-center">
                            <i class="pi pi-star text-4xl text-yellow-400"></i>
                        </div>
                        <h4 class="font-medium text-gray-800">Playful</h4>
                        <p class="text-sm text-gray-500">Fun and energetic with bright colors</p>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-end gap-2">
                    <button @click="showPortfolioThemeDialog = false"
                        class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                        Cancel
                    </button>
                    <button 
                        @click="createPortfolioWithTheme"
                        :disabled="!selectedTheme"
                        :class="[
                            'px-4 py-2 rounded-lg transition-colors',
                            selectedTheme ? 'bg-blue-600 text-white hover:bg-blue-700' : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                        ]"
                    >
                        Create Portfolio
                    </button>
                </div>
            </template>
        </Dialog>

        <!-- New Folder Dialog -->
        <Dialog v-model:visible="showNewFolderDialog" 
            modal 
            header="Create New Folder" 
            :style="{ width: '40rem' }">
            <div class="p-6">
                <div class="grid grid-cols-2 gap-6">
                    <!-- Form Fields -->
                    <div class="space-y-4">
                        <div>
                            <label for="folderTitle" class="block text-sm font-medium text-gray-700 mb-1">Folder Title</label>
                            <input 
                                id="folderTitle"
                                v-model="newFolder.title"
                                type="text"
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Enter folder title"
                            >
                        </div>
                        <div>
                            <label for="folderDescription" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                            <textarea 
                                id="folderDescription"
                                v-model="newFolder.description"
                                rows="3"
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Enter folder description"
                            ></textarea>
                        </div>
                    </div>

                    <!-- Preview -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-3">Preview</label>
                        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <!-- Folder Preview -->
                            <div class="relative h-32 mb-4">
                                <!-- Stacked Preview Images -->
                                <div class="absolute top-0 right-0 w-24 h-28 flex items-center justify-center">
                                    <div class="absolute w-20 h-24 bg-gray-100 rounded-lg transform rotate-[-15deg] transition-transform"></div>
                                    <div class="absolute w-20 h-24 bg-gray-200 rounded-lg transform rotate-[-5deg] transition-transform"></div>
                                    <div class="absolute w-20 h-24 bg-gray-300 rounded-lg transform rotate-[5deg] transition-transform"></div>
                                </div>
                                <!-- Folder Title -->
                                <h3 class="text-xl font-semibold text-gray-800 mb-1 relative z-10">{{ newFolder.title || 'Folder Title' }}</h3>
                                <span class="text-sm text-gray-500 relative z-10">0 items</span>
                            </div>
                            <!-- Folder Description -->
                            <p class="text-gray-600 text-sm">{{ newFolder.description || 'Your folder description will appear here' }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-between items-center">
                    <p class="text-sm text-gray-500">* Preview updates as you type</p>
                    <div class="flex gap-2">
                        <button @click="showNewFolderDialog = false"
                            class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                            Cancel
                        </button>
                        <button 
                            @click="createNewFolder"
                            :disabled="!newFolder.title"
                            :class="[
                                'px-4 py-2 rounded-lg transition-colors flex items-center gap-2',
                                newFolder.title ? 'bg-blue-600 text-white hover:bg-blue-700' : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                            ]"
                        >
                            <i class="pi pi-check"></i>
                            Create Folder
                        </button>
                    </div>
                </div>
            </template>
        </Dialog>

        <!-- Add Project Dialog -->
        <Dialog v-model:visible="showAddProjectDialog" 
            modal 
            header="Add New Project" 
            :style="{ width: '40rem' }">
            <div class="p-6">
                <div class="grid grid-cols-2 gap-6">
                    <!-- Form Fields -->
                    <div class="space-y-4">
                        <div>
                            <label for="projectTitle" class="block text-sm font-medium text-gray-700 mb-1">Project Title</label>
                            <input 
                                id="projectTitle"
                                v-model="newProject.title"
                                type="text"
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Enter project title"
                            >
                        </div>
                        <div>
                            <label for="projectDescription" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                            <textarea 
                                id="projectDescription"
                                v-model="newProject.description"
                                rows="3"
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Enter project description"
                            ></textarea>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Project Type</label>
                            <select 
                                v-model="newProject.type"
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            >
                                <option value="document">Document</option>
                                <option value="presentation">Presentation</option>
                                <option value="spreadsheet">Spreadsheet</option>
                                <option value="image">Image</option>
                                <option value="video">Video</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                    </div>

                    <!-- Preview -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-3">Preview</label>
                        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <div class="mb-4">
                                <div :class="[
                                    'w-full h-32 rounded-lg mb-3 flex items-center justify-center',
                                    {
                                        'bg-blue-50': newProject.type === 'document',
                                        'bg-purple-50': newProject.type === 'presentation',
                                        'bg-green-50': newProject.type === 'spreadsheet',
                                        'bg-yellow-50': newProject.type === 'image',
                                        'bg-red-50': newProject.type === 'video',
                                        'bg-gray-50': newProject.type === 'other'
                                    }
                                ]">
                                    <i :class="[
                                        'pi text-2xl',
                                        {
                                            'pi-file-pdf text-blue-500': newProject.type === 'document',
                                            'pi-images text-purple-500': newProject.type === 'presentation',
                                            'pi-table text-green-500': newProject.type === 'spreadsheet',
                                            'pi-image text-yellow-600': newProject.type === 'image',
                                            'pi-video text-red-500': newProject.type === 'video',
                                            'pi-file text-gray-500': newProject.type === 'other'
                                        }
                                    ]"></i>
                                </div>
                                <h3 class="text-lg font-semibold text-gray-800">{{ newProject.title || 'Project Title' }}</h3>
                                <p class="text-sm text-gray-500 capitalize">{{ newProject.type || 'Type' }}</p>
                            </div>
                            <p class="text-gray-600 text-sm">{{ newProject.description || 'Project description will appear here' }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <template #footer>
                <div class="flex justify-between items-center">
                    <p class="text-sm text-gray-500">* Preview updates as you type</p>
                    <div class="flex gap-2">
                        <button @click="showAddProjectDialog = false"
                            class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                            Cancel
                        </button>
                        <button 
                            @click="createNewProject"
                            :disabled="!newProject.title"
                            :class="[
                                'px-4 py-2 rounded-lg transition-colors flex items-center gap-2',
                                newProject.title ? 'bg-blue-600 text-white hover:bg-blue-700' : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                            ]"
                        >
                            <i class="pi pi-check"></i>
                            Create Project
                        </button>
                    </div>
                </div>
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Head, usePage } from '@inertiajs/vue3';
import MainLayout from '@/Layouts/MainLayout.vue';
import Dialog from 'primevue/dialog';

const page = usePage();
const auth = computed(() => page.props.auth);

const props = defineProps({
    className: {
        type: String,
        required: true,
        default: 'Digital Arts'
    },
    theme: {
        type: String,
        default: 'emerald'
    }
});

// Computed theme classes
const themeClasses = computed(() => ({
    header: `bg-${props.theme}-400`,
    badge: `bg-${props.theme}-200`,
    memberHeader: `bg-${props.theme}-600`,
    buttons: `bg-${props.theme}-500`,
    activeTab: `bg-${props.theme}-400`
}));

const activeTab = ref('portfolio');
const activeContentTab = ref('portfolio');

// Tab configurations
const tabs = [
    { id: 'portfolio', name: 'My Portfolio', icon: 'pi-image' },
    { id: 'schedule', name: 'Schedule', icon: 'pi-calendar' }
];

// Portfolio state
const showPortfolioThemeDialog = ref(false);
const selectedTheme = ref(null);
const portfolioCreated = ref(false);
const selectedPortfolioTheme = ref('minimal'); // Default theme

// Folder and Activity State
const selectedFolder = ref(null);
const selectedTab = ref('Recent');

// Sample activities data for each folder
const getFolderActivities = (folderId) => {
    const activities = {
        'Mapeh': [
            {
                title: "Essay on Arts History",
                description: "A comprehensive analysis of Renaissance art and its influence on modern culture.",
                image: "https://images.unsplash.com/photo-1577083552431-6e5fd01988ec?ixlib=rb-4.0.3",
                status: "Completed",
                date: "Mar 20, 2025",
                files: [
                    { name: "renaissance_essay.pdf", size: "2.4 MB" },
                    { name: "art_references.zip", size: "5.1 MB" }
                ]
            },
            {
                title: "Music Theory Assignment",
                description: "Analysis of classical music compositions and their structures.",
                image: "https://images.unsplash.com/photo-1507838153414-b4b713384a76?ixlib=rb-4.0.3",
                status: "In Progress",
                date: "Mar 22, 2025",
                files: [
                    { name: "music_notes.pdf", size: "1.8 MB" },
                    { name: "composition.mp3", size: "3.2 MB" }
                ]
            }
        ],
        'Science': [
            {
                title: "Lab Report: Photosynthesis",
                description: "Detailed documentation of our plant growth experiment and findings.",
                image: "https://images.unsplash.com/photo-1576086213369-97a306d36557?ixlib=rb-4.0.3",
                status: "Completed",
                date: "Mar 22, 2025",
                files: [
                    { name: "lab_report.docx", size: "1.8 MB" },
                    { name: "experiment_photos.zip", size: "5.2 MB" }
                ]
            },
            {
                title: "Chemistry Experiment Results",
                description: "Analysis of chemical reactions and their outcomes.",
                image: "https://images.unsplash.com/photo-1532187643603-ba119ca4109e?ixlib=rb-4.0.3",
                status: "In Progress",
                date: "Mar 24, 2025",
                files: [
                    { name: "chemistry_data.xlsx", size: "1.1 MB" }
                ]
            }
        ],
        'English': [
            {
                title: "Literary Analysis Essay",
                description: "Critical analysis of Shakespeare's Macbeth.",
                image: "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?ixlib=rb-4.0.3",
                status: "Completed",
                date: "Mar 18, 2025",
                files: [
                    { name: "macbeth_analysis.pdf", size: "3.1 MB" }
                ]
            }
        ],
        'Math': [
            {
                title: "Calculus Problem Set",
                description: "Solutions to advanced calculus problems and proofs.",
                image: "https://images.unsplash.com/photo-1635372722656-389f87a941b7?ixlib=rb-4.0.3",
                status: "New",
                date: "Mar 24, 2025",
                files: [
                    { name: "calculus_solutions.pdf", size: "3.1 MB" }
                ]
            }
        ],
        'AP': [
            {
                title: "Historical Research Paper",
                description: "Analysis of World War II impacts on Southeast Asia.",
                image: "https://images.unsplash.com/photo-1447069387593-a5de0862481e?ixlib=rb-4.0.3",
                status: "In Progress",
                date: "Mar 21, 2025",
                files: [
                    { name: "research_paper.docx", size: "4.2 MB" },
                    { name: "historical_data.pdf", size: "2.8 MB" }
                ]
            }
        ]
    };
    return activities[folderId] || [];
};

// Portfolio folders data
const portfolioFolders = [
    { id: 'Mapeh', title: 'Mapeh', description: 'Essay-related activities and writing projects.', items: 10 },
    { id: 'Science', title: 'Science', description: 'Lab reports, experiments, and notes.', items: 15 },
    { id: 'English', title: 'English', description: 'Essays, literature reviews, and projects.', items: 12 },
    { id: 'Math', title: 'Math', description: 'Problem sets, formulas, and worksheets.', items: 18 },
    { id: 'AP', title: 'AP', description: 'History and social studies documents.', items: 8 }
];

// Folder activities data
const folderActivities = ref([]);

// Function to open folder content
const openFolderContent = (folder) => {
    selectedFolder.value = folder;
    folderActivities.value = getFolderActivities(folder.id);
};

// New Folder Dialog State
const showNewFolderDialog = ref(false);
const newFolder = ref({ title: '', description: '' });

// Function to create new folder
const createNewFolder = () => {
    // Add new folder to portfolioFolders array
    portfolioFolders.push({ id: newFolder.value.title, title: newFolder.value.title, description: newFolder.value.description, items: 0 });
    showNewFolderDialog.value = false;
    newFolder.value = { title: '', description: '' };
};

// Add Project Dialog State
const showAddProjectDialog = ref(false);
const newProject = ref({ title: '', description: '', type: '' });

// Function to create new project
const createNewProject = () => {
    // Add new project to folderActivities array
    folderActivities.value.push({
        title: newProject.value.title,
        description: newProject.value.description,
        type: newProject.value.type,
        status: 'New',
        date: 'Mar 24, 2025',
        files: []
    });
    showAddProjectDialog.value = false;
    newProject.value = { title: '', description: '', type: '' };
};

// Add these for the calendar functionality
const selectedDate = ref(null);

// Generate random schedule
const generateRandomSchedule = () => {
    const times = [
        '8:00 AM - 9:30 AM',
        '9:45 AM - 11:15 AM',
        '1:00 PM - 2:30 PM',
        '2:45 PM - 4:15 PM'
    ];
    
    return Array.from({ length: 30 }, () => ({
        time: times[Math.floor(Math.random() * times.length)]
    }));
};

const schedule = ref(generateRandomSchedule());

// Helper function to determine if it's a class day (Monday & Wednesday)
const isClassDay = (date) => {
    const dayOfWeek = new Date(2025, 10, date).getDay(); // 0 = Sunday, 1 = Monday, etc.
    return dayOfWeek === 1 || dayOfWeek === 3; // Monday or Wednesday
};

// Show schedule details
const showScheduleDetails = (date) => {
    selectedDate.value = date;
};

// Portfolio functions
const createPortfolio = () => {
    showPortfolioThemeDialog.value = true;
};

const createPortfolioWithTheme = () => {
    if (!selectedTheme.value) return;
    
    selectedPortfolioTheme.value = selectedTheme.value;
    showPortfolioThemeDialog.value = false;
    selectedTheme.value = null;
    portfolioCreated.value = true;
};

defineOptions({
    layout: MainLayout
});
</script>

<style scoped>
.aspect-video {
    aspect-ratio: 16 / 9;
}

/* Add these styles for consistent calendar styling */
.calendar-day {
    @apply p-4 border rounded-lg hover:shadow-md cursor-pointer transition-all;
}

.calendar-day-active {
    @apply font-semibold text-gray-800;
}

.calendar-time {
    @apply text-sm mt-1;
}

/* DataTable styles */
:deep(.p-datatable) {
    border-radius: 0.75rem;
    overflow: hidden;
    margin-top: 1rem;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
    background-color: #f8fafc;
    color: #1e293b;
    font-weight: 600;
    padding: 1rem;
    border-bottom: 2px solid #e2e8f0;
}

:deep(.p-datatable .p-datatable-tbody > tr) {
    transition: background-color 0.2s;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
    background-color: #f1f5f9;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
    padding: 1rem;
}

/* Responsive and transition styles */
@media (max-width: 1024px) {
    .lg\:w-64 {
        width: 100%;
    }
}

.bg-gradient-to-br {
    transition: all 0.3s ease;
}

.h-2 {
    transition: width 0.5s ease;
}
</style>