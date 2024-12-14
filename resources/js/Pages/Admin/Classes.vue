<script setup>
import { ref } from 'vue';
const visible = ref(false);
</script>

<template>
    <Head :title="`| ${$page.component}`"/>

    <!-- Main Content -->
    <main class="flex-1">
        <header class="mb-4 flex justify-between items-center">
            <h1 class="text-1xl font-semibold">Class / SY 2024-2025</h1>
        </header>

        <!-- Flex Container for Dashboard and Card -->
        <div class="flex gap-4">
            <!-- Card Component -->
            <Card style="width: 15rem; overflow: hidden,">
                <template #header>
                    <img alt="user header" src="https://images.theconversation.com/files/560517/original/file-20231120-20-pxbkgm.jpg?ixlib=rb-4.1.0&rect=0%2C0%2C4928%2C3260&q=20&auto=format&w=320&fit=clip&dpr=2&usm=12&cs=strip" />
                </template>
                <template #title>Grade 1 - A</template>
            </Card>

            <Card style="width: 15rem; overflow: hidden,">
                <template #header>
                    <img alt="user header" src="https://images.theconversation.com/files/560517/original/file-20231120-20-pxbkgm.jpg?ixlib=rb-4.1.0&rect=0%2C0%2C4928%2C3260&q=20&auto=format&w=320&fit=clip&dpr=2&usm=12&cs=strip" />
                </template>
                <template #title>Grade 1 - A</template>
            </Card>

            <Card style="width: 15rem; overflow: hidden,">
                <template #header>
                    <img alt="user header" src="https://images.theconversation.com/files/560517/original/file-20231120-20-pxbkgm.jpg?ixlib=rb-4.1.0&rect=0%2C0%2C4928%2C3260&q=20&auto=format&w=320&fit=clip&dpr=2&usm=12&cs=strip" />
                </template>
                <template #title>Grade 1 - A</template>
            </Card>

            <Card style="width: 15rem; overflow: hidden,">
                <template #header>
                    <img alt="user header" src="https://images.theconversation.com/files/560517/original/file-20231120-20-pxbkgm.jpg?ixlib=rb-4.1.0&rect=0%2C0%2C4928%2C3260&q=20&auto=format&w=320&fit=clip&dpr=2&usm=12&cs=strip" />
                </template>
                <template #title>Grade 1 - A</template>
            </Card>
        </div>
    </main>
</template>
