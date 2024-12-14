<script setup>
import { ref } from 'vue';
const visible = ref(false);
</script>

<template>
    <Head :title="`| ${$page.component}`"/>

    <!-- Main Content -->
    <main class="flex-2">
        <header class="mb-4 flex justify-between items-center">
            <h1 class="text-2xl font-bold">Lesson Plan</h1>
        </header>

        <!-- Flex Container for Dashboard and Card -->
        <div class="flex gap-4">
            <!-- Card Component -->
            <Card style="width: 40rem; overflow: hidden; margin: 0 auto">

                <template #title>Lesson Plan - Mike Madulara</template>
                <template #content>
                    <p class="m-20">
                        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Inventore sed consequuntur error repudiandae numquam deserunt quisquam repellat libero asperiores earum nam nobis, culpa ratione quam perferendis esse, cupiditate neque
                        quas!
                    </p>
                </template>
                <template #footer>
                    <div class="flex gap-4 mt-1">
                        <Button label="APPROVE" class="w-full" />
                        <Button label="REVISE" class="w-full" />
                    </div>
                </template>
            </Card>

        </div>
    </main>

</template>
