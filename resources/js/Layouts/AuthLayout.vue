<template>
    <div class="flex min-h-screen">
        <!-- Left side with back button -->
        <div class="w-16 p-4">
            <Link href="/" class="text-gray-600 hover:text-gray-800">
                <i class="pi pi-arrow-left text-xl"></i>
            </Link>
        </div>

        <!-- Main content -->
        <div class="flex-1 flex items-center justify-center gap-24 px-4">
            <!-- School Logo -->
            <div class="order-first">
                <img
                    src="https://scontent.fmnl13-4.fna.fbcdn.net/v/t39.30808-6/368255360_324082253303069_319860159441260390_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeEeeZOV62u2x4mCX5FuSl2wJArEhEwobZUkCsSETChtlSadu9mg9xY6wtY1RoAhwpXAtpuI0SMtLSKiUSUzf-yu&_nc_ohc=ubF5iKQIDtUQ7kNvgEZt1Zt&_nc_zt=23&_nc_ht=scontent.fmnl13-4.fna&_nc_gid=A23xbZ_kfZlTXSq8V8A7lWK&oh=00_AYBsGcjiZbvKLr1F7j241bPB_XaYurmSq1fjC5iwKrccgw&oe=6762AD74"
                    alt="Naawan Central School Logo"
                    class="w-60 h-60 object-contain bg-white shadow-lg p-2"
                />
            </div>

            <!-- Login Content -->
            <div class="w-full max-w-md">
                <!-- Welcome Text -->
                <h1 class="text-2xl font-bold mb-8 text-[#1B2850] text-center">Welcome to EduBoard!</h1>

                <!-- Slot for page content -->
                <slot />
            </div>
        </div>
    </div>
</template>

<script setup>
import { Link } from '@inertiajs/vue3';
</script>
