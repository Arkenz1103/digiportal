<script setup>
import { Head } from '@inertiajs/vue3';

defineOptions({ layout: null })
</script>

<template>
    <Head title="" />
    <div class="min-h-screen bg-white">
        <!-- Header -->
        <div class="bg-[#7386D5] text-white py-4">
            <div class="container mx-auto px-4 flex justify-between items-center">
                <div class="text-2xl font-bold">Naawan Central School</div>
                <a href="/login" class="bg-gray-200 text-gray-800 px-6 py-2 rounded-md hover:bg-gray-300 transition-colors">
                    Login
                </a>
            </div>
        </div>

        <!-- Main Content -->
        <main class="container mx-auto flex flex-col md:flex-row items-center justify-center gap-16 px-4 py-16">
            <div class="w-64 md:w-96">
                <img
                    src="https://scontent.fmnl13-4.fna.fbcdn.net/v/t39.30808-6/368255360_324082253303069_319860159441260390_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeEeeZOV62u2x4mCX5FuSl2wJArEhEwobZUkCsSETChtlSadu9mg9xY6wtY1RoAhwpXAtpuI0SMtLSKiUSUzf-yu&_nc_ohc=ubF5iKQIDtUQ7kNvgEZt1Zt&_nc_zt=23&_nc_ht=scontent.fmnl13-4.fna&_nc_gid=A23xbZ_kfZlTXSq8V8A7lWK&oh=00_AYBsGcjiZbvKLr1F7j241bPB_XaYurmSq1fjC5iwKrccgw&oe=6762AD74"
                    alt="Naawan Central School Logo"
                    class="w-full h-auto"
                />
            </div>
            <div class="max-w-2xl text-center md:text-left">
                <h1 class="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-800 mb-1 leading-tight">
                    "Education is the most powerful weapon which you can use to change the world."
                </h1>
            </div>
        </main>
    </div>
</template>
