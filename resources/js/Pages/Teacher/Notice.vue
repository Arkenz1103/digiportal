<script setup>
import { ref } from 'vue';
import { useForm } from '@inertiajs/vue3';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

const pendingOutputs = ref([
    {
        id: '2021-0001',
        studentName: 'John Smith',
        title: 'Self-Portrait: Reflections of Me',
        description: 'Just finished my mixed media self-portrait exploring my dual heritage! 🎨 #ArtClass #MixedMedia',
        submittedDate: '2025-03-18',
        subject: 'Art',
        sampleImages: [
            'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80'
        ],
        status: 'Completed',
        rank: 1,
        remarks: 'Excellent use of mixed media techniques. The composition is well-balanced and the symbolic elements add depth to your self-exploration. Consider experimenting with more texture in future works.'
    },
    {
        id: '2021-0002',
        studentName: 'Maria Garcia',
        title: 'Self-Portrait: Through My Eyes',
        description: 'Expressing myself through watercolor and ink today. Eyes are the window to the soul! ✨ #WatercolorArt',
        submittedDate: '2025-03-26',
        subject: 'Art',
        sampleImages: [
            'https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80'
        ],
        status: 'In Progress',
        rank: 2,
        remarks: 'Beautiful watercolor technique with excellent control of washes. The eyes are particularly expressive. Consider adding more contrast to make the facial features pop.'
    },
    {
        id: '2021-0003',
        studentName: 'James Wilson',
        title: 'Self-Portrait: Digital Me',
        description: 'Created this digital self-portrait on Procreate! Loving the vibrant colors and geometric vibes. 🎭 #DigitalArt',
        submittedDate: '2025-03-15',
        subject: 'Art',
        sampleImages: [
            'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80'
        ],
        status: 'Pending Review',
        rank: 3,
        remarks: 'Strong digital painting skills demonstrated. The color palette is vibrant and eye-catching. The geometric elements could be better integrated with the portrait for a more cohesive composition.'
    }
]);

const showPreviewDialog = ref(false);
const showRejectionDialog = ref(false);
const selectedOutput = ref(null);
const feedbackForm = useForm({
    isApproved: false,
    rejectionReason: '',
    rejectionDetails: ''
});

const rejectionReasons = [
    { id: 'lack_of_content', label: 'Lack of content' },
    { id: 'irrelevant_outputs', label: 'Irrelevant outputs' },
    { id: 'others', label: 'others' }
];

const previewOutput = (output) => {
    selectedOutput.value = output;
    showPreviewDialog.value = true;
};

const submitFeedback = (isApproved) => {
    feedbackForm.isApproved = isApproved;

    const index = pendingOutputs.value.findIndex(o => o.id === selectedOutput.value.id);
    if (index !== -1) {
        pendingOutputs.value.splice(index, 1);
    }

    showPreviewDialog.value = false;
    showRejectionDialog.value = false;
    feedbackForm.reset();
};

const showRejectionReasonsDialog = () => {
    showRejectionDialog.value = true;
};

const cancelRejection = () => {
    showRejectionDialog.value = false;
    feedbackForm.rejectionReason = '';
    feedbackForm.rejectionDetails = '';
};
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-violet-50 to-blue-50 p-4 md:p-6">
        <div class="rounded-2xl shadow-lg bg-white/90 backdrop-blur-sm border border-indigo-100 overflow-hidden">
            <!-- Header -->
            <div class="p-6 bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700">
                <h1 class="text-2xl font-semibold text-white">Student Output Approval</h1>
            </div>

            <!-- Pending Count -->
            <div class="px-6 py-4 bg-indigo-50 border-b border-indigo-100 flex justify-between items-center">
                <h2 class="text-lg font-medium text-indigo-900">Pending Approvals</h2>
                <span class="bg-indigo-600 text-white text-sm font-medium px-3 py-1 rounded-full">
                    {{ pendingOutputs.length }} Pending
                </span>
            </div>

            <!-- Outputs List -->
            <div class="divide-y divide-indigo-100">
                <div v-for="output in pendingOutputs" :key="output.id" 
                    class="p-6 hover:bg-indigo-50/50 transition-colors duration-200">
                    <div class="flex justify-between items-start">
                        <div class="flex-1">
                            <div class="flex items-center space-x-3 mb-2">
                                <span class="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-sm font-medium text-white">
                                    {{ output.studentName.charAt(0) }}
                                </span>
                                <h3 class="font-medium text-indigo-900">{{ output.studentName }}</h3>
                                <span class="text-sm text-indigo-700/80">submitted {{ output.title }}</span>
                            </div>
                            <div class="ml-11">
                                <p class="text-indigo-900/80">{{ output.description }}</p>
                                <div class="mt-2">
                                    <div class="text-sm font-medium text-indigo-900 mb-2">Output:</div>
                                    <div class="flex gap-2 overflow-x-auto pb-2">
                                        <img 
                                            :src="output.sampleImages[0]"
                                            class="h-24 w-auto rounded-md border border-indigo-200 cursor-pointer hover:opacity-90 transition-opacity"
                                            @click="previewOutput(output)"
                                            :alt="`Sample of ${output.title}`"
                                        />
                                    </div>
                                </div>
                                <div class="mt-2 flex items-center space-x-4 text-sm">
                                    <span class="text-indigo-700/80">
                                        <i class="pi pi-calendar mr-1"></i>
                                        {{ output.submittedDate }}
                                    </span>
                                    <span class="text-indigo-700/80">
                                        <i class="pi pi-book mr-1"></i>
                                        {{ output.subject }}
                                    </span>
                                    <!-- Add rank badge if available -->
                                    <span v-if="output.rank" :class="['rank-badge', `rank-${output.rank}`]">
                                        {{ output.rank }}
                                    </span>
                                </div>
                            </div>
                        </div>
                        <Button 
                            label="Review" 
                            class="p-button-sm"
                            style="background: linear-gradient(to right, #4f46e5, #6366f1); border: none;" 
                            @click="previewOutput(output)"
                        />
                    </div>
                </div>
            </div>
        </div>

        <!-- Preview Dialog -->
        <Dialog 
            v-model:visible="showPreviewDialog"
            modal
            header="Review Student Output"
            :style="{ width: '70vw', maxWidth: '800px' }"
            :dismissableMask="true"
            headerClass="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 text-white"
        >
            <div v-if="selectedOutput" class="space-y-6">
                <!-- Student Info -->
                <div class="bg-indigo-50 p-4 rounded-lg border border-indigo-100">
                    <div class="flex items-center space-x-3">
                        <span class="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-sm font-medium text-white">
                            {{ selectedOutput.studentName.charAt(0) }}
                        </span>
                        <div>
                            <h3 class="font-medium text-indigo-900">{{ selectedOutput.studentName }}</h3>
                            <p class="text-sm text-indigo-700/80">{{ selectedOutput.subject }}</p>
                        </div>
                        <!-- Medal for top ranked submissions -->
                        <div v-if="selectedOutput.rank <= 3" class="ml-auto">
                            <div :class="[
                                    'medal-container', 
                                    `medal-${selectedOutput.rank === 1 ? 'gold' : 
                                            selectedOutput.rank === 2 ? 'silver' : 'bronze'}`
                                ]"
                            >
                                <!-- Ribbon -->
                                <div class="medal-ribbon">
                                    <div class="ribbon-left"></div>
                                    <div class="ribbon-right"></div>
                                    <div class="ribbon-connector"></div>
                                </div>
                                
                                <!-- Medal -->
                                <div class="medal-star">
                                    <div class="medal-star-shape"></div>
                                    <div class="medal-rays"></div>
                                    <div class="medal-inner">
                                        {{ selectedOutput.rank }}
                                    </div>
                                    <div class="medal-shine"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Output Details -->
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-indigo-900">Title</label>
                        <p class="mt-1 text-indigo-900">{{ selectedOutput.title }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-[#0E1836]">Description</label>
                        <p class="mt-1 text-[#0E1836]">{{ selectedOutput.description }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-[#0E1836] mb-2">Sample Image</label>
                        <div class="border border-[#B6CFFF] rounded-lg overflow-hidden">
                            <img 
                                :src="selectedOutput.sampleImages[0]" 
                                class="w-full h-auto max-h-64 object-contain"
                                :alt="`Sample of ${selectedOutput.title}`"
                            />
                            <div class="p-2 bg-[#F2FDFF] text-center text-sm text-[#0E1836]/80">
                                Student Artwork
                            </div>
                        </div>
                    </div>
                    <!-- Add remarks section -->
                    <div v-if="selectedOutput.remarks">
                        <label class="block text-sm font-medium text-[#0E1836]">Remarks</label>
                        <p class="mt-1 text-[#0E1836] p-3 bg-[#F2FDFF] rounded-lg border border-[#B6CFFF]">
                            {{ selectedOutput.remarks }}
                        </p>
                    </div>
                </div>
            </div>

            <template #footer>
                <div class="mt-6 flex justify-end space-x-3">
                    <Button 
                        label="Cancel"
                        class="p-button-secondary"
                        style="background: #f3f4f6; border: 1px solid #d1d5db; color: #1f2937; margin-right: 0.5rem;" 
                        @click="showPreviewDialog = false"
                    />
                    <Button 
                        label="Reject"
                        class="p-button-danger"
                        style="background: linear-gradient(to right, #dc2626, #ef4444); border: none; color: white; margin-right: 0.5rem;" 
                        @click="showRejectionReasonsDialog"
                    />
                    <Button 
                        label="Approve"
                        style="background: linear-gradient(to right, #4f46e5, #6366f1); border: none; color: white;" 
                        @click="submitFeedback(true)"
                    />
                </div>
            </template>
        </Dialog>

        <!-- Rejection Reasons Dialog -->
        <Dialog 
            v-model:visible="showRejectionDialog"
            modal
            header="Rejection Reasons"
            :style="{ width: '50vw', maxWidth: '600px' }"
            :dismissableMask="true"
            headerClass="bg-gradient-to-r from-red-700 to-red-600 text-white"
        >
            <div v-if="selectedOutput" class="space-y-4">
                <!-- Student Info Summary -->
                <div class="bg-red-50 p-4 rounded-lg border border-red-100">
                    <h3 class="font-semibold text-red-900 mb-2">Student Output</h3>
                    <p class="text-red-800"><strong>{{ selectedOutput.studentName }}</strong> - {{ selectedOutput.title }}</p>
                </div>

                <!-- Rejection Reason Selection -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                        Select Reason for Rejection <span class="text-red-500">*</span>
                    </label>
                    <div class="space-y-2">
                        <div v-for="reason in rejectionReasons" :key="reason.id" class="flex items-center">
                            <input
                                type="radio"
                                :id="reason.id"
                                :value="reason.id"
                                v-model="feedbackForm.rejectionReason"
                                class="h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300"
                            />
                            <label :for="reason.id" class="ml-3 block text-sm text-gray-700">
                                {{ reason.label }}
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Additional Details -->
                <div>
                    <label for="rejectionDetails" class="block text-sm font-medium text-gray-700 mb-2">
                        Additional Details (Optional)
                    </label>
                    <textarea
                        id="rejectionDetails"
                        v-model="feedbackForm.rejectionDetails"
                        rows="4"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500"
                        placeholder="Please provide any additional comments or specific feedback for the student..."
                    ></textarea>
                </div>
            </div>

            <template #footer>
                <div class="mt-6 flex justify-end space-x-3">
                    <Button 
                        label="Cancel"
                        class="p-button-secondary"
                        style="background: #f3f4f6; border: 1px solid #d1d5db; color: #1f2937; margin-right: 0.5rem;" 
                        @click="cancelRejection"
                    />
                    <Button 
                        label="Confirm Rejection"
                        class="p-button-danger"
                        style="background: linear-gradient(to right, #dc2626, #ef4444); border: none; color: white;" 
                        @click="submitFeedback(false)"
                        :disabled="!feedbackForm.rejectionReason"
                    />
                </div>
            </template>
        </Dialog>
    </div>
</template>

<style scoped>
/* Add theme variables */
:root {
    --theme-purple: #B8AAFF;
    --theme-blue: #B6CFFF;
    --theme-light: #F2FDFF;
    --theme-accent: #7BBBFE;
    --theme-dark: #0E1836;
}

/* Custom styles for dialog header */
:deep(.p-dialog-header) {
    background-color: #B8AAFF;
    color: white;
}

:deep(.p-dialog .p-dialog-content) {
    background-color: white;
}

:deep(.p-dialog .p-dialog-footer) {
    background-color: white;
    border-top: 1px solid #B6CFFF;
}

/* Custom scrollbar for image thumbnails */
::-webkit-scrollbar {
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb {
    background: #B6CFFF;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #7BBBFE;
}

/* Rank badge styles */
.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    font-weight: bold;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.rank-badge::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        transparent, 
        transparent, 
        transparent, 
        rgba(255, 255, 255, 0.3)
    );
    transform: rotate(45deg);
    animation: shine-effect 3s infinite;
}

@keyframes shine-effect {
    0% { transform: rotate(45deg) translateY(0%); }
    100% { transform: rotate(45deg) translateY(100%); }
}

.rank-1 {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: white;
}

.rank-2 {
    background: linear-gradient(135deg, #E0E0E0, #A0A0A0);
    color: white;
}

.rank-3 {
    background: linear-gradient(135deg, #CD7F32, #8B4513);
    color: white;
}

.rank-other {
    background: linear-gradient(135deg, #7BBBFE, #B8AAFF);
    color: white;
}

/* Enhanced Medal Styles */
.medal-container {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    transform-style: preserve-3d;
    perspective: 1000px;
}

.medal-container:hover {
    transform: translateY(-5px) rotate(5deg);
}

.medal-ribbon {
    position: absolute;
    top: -30px;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 60px;
    z-index: -1;
    filter: drop-shadow(0 5px 5px rgba(0, 0, 0, 0.3));
}

.ribbon-left, .ribbon-right {
    position: absolute;
    width: 20px;
    height: 60px;
    top: 0;
}

.ribbon-left {
    left: 0;
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 85%);
}

.ribbon-right {
    right: 0;
    clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
}

.ribbon-connector {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 40px;
    height: 10px;
    border-radius: 5px 5px 0 0;
}

.medal-star {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, white, transparent);
    box-shadow: 
        0 10px 20px rgba(0, 0, 0, 0.2),
        0 6px 6px rgba(0, 0, 0, 0.1),
        inset 0 -5px 15px rgba(0, 0, 0, 0.2);
    transform-style: preserve-3d;
    transition: transform 0.3s ease;
}

.medal-star::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background: inherit;
    border-radius: inherit;
    filter: blur(5px);
    opacity: 0.7;
    z-index: -1;
}

.medal-star-shape {
    position: absolute;
    width: 100%;
    height: 100%;
    clip-path: polygon(
        50% 0%, 61% 35%, 98% 35%, 68% 57%,
        79% 91%, 50% 70%, 21% 91%, 32% 57%,
        2% 35%, 39% 35%
    );
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.5), rgba(0, 0, 0, 0.2));
    z-index: 1;
}

.medal-inner {
    position: relative;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 18px;
    color: white;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    z-index: 2;
    box-shadow: 
        inset 0 2px 5px rgba(255, 255, 255, 0.5),
        inset 0 -2px 5px rgba(0, 0, 0, 0.3);
}

.medal-rays {
    position: absolute;
    width: 120%;
    height: 120%;
    background: conic-gradient(
        transparent 0deg,
        rgba(255, 255, 255, 0.8) 10deg,
        transparent 20deg,
        rgba(255, 255, 255, 0.8) 30deg,
        transparent 40deg,
        rgba(255, 255, 255, 0.8) 50deg,
        transparent 60deg,
        rgba(255, 255, 255, 0.8) 70deg,
        transparent 80deg,
        rgba(255, 255, 255, 0.8) 90deg,
        transparent 100deg,
        rgba(255, 255, 255, 0.8) 110deg,
        transparent 120deg,
        rgba(255, 255, 255, 0.8) 130deg,
        transparent 140deg,
        rgba(255, 255, 255, 0.8) 150deg,
        transparent 160deg,
        rgba(255, 255, 255, 0.8) 170deg,
        transparent 180deg,
        rgba(255, 255, 255, 0.8) 190deg,
        transparent 200deg,
        rgba(255, 255, 255, 0.8) 210deg,
        transparent 220deg,
        rgba(255, 255, 255, 0.8) 230deg,
        transparent 240deg,
        rgba(255, 255, 255, 0.8) 250deg,
        transparent 260deg,
        rgba(255, 255, 255, 0.8) 270deg,
        transparent 280deg,
        rgba(255, 255, 255, 0.8) 290deg,
        transparent 300deg,
        rgba(255, 255, 255, 0.8) 310deg,
        transparent 320deg,
        rgba(255, 255, 255, 0.8) 330deg,
        transparent 340deg,
        rgba(255, 255, 255, 0.8) 350deg,
        transparent 360deg
    );
    border-radius: 50%;
    animation: rotate 20s linear infinite;
    opacity: 0.7;
    z-index: 0;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes shine {
    0% { opacity: 0.5; }
    50% { opacity: 1; }
    100% { opacity: 0.5; }
}

.medal-shine {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.7) 0%, rgba(255, 255, 255, 0) 50%, rgba(255, 255, 255, 0) 100%);
    animation: shine 3s ease-in-out infinite;
    z-index: 3;
    pointer-events: none;
}

.medal-gold .medal-star {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    border: 2px solid #FFD700;
}

.medal-silver .medal-star {
    background: linear-gradient(135deg, #E0E0E0, #A0A0A0);
    border: 2px solid #C0C0C0;
}

.medal-bronze .medal-star {
    background: linear-gradient(135deg, #CD7F32, #8B4513);
    border: 2px solid #CD7F32;
}

.medal-gold .medal-inner {
    background: linear-gradient(135deg, #FF0000, #990000);
    border: 2px solid #FFD700;
}

.medal-silver .medal-inner {
    background: linear-gradient(135deg, #3366FF, #003399);
    border: 2px solid #C0C0C0;
}

.medal-bronze .medal-inner {
    background: linear-gradient(135deg, #009900, #006600);
    border: 2px solid #CD7F32;
}

.medal-gold .ribbon-left, 
.medal-gold .ribbon-right,
.medal-gold .ribbon-connector {
    background: linear-gradient(135deg, #FF0000, #990000);
}

.medal-silver .ribbon-left, 
.medal-silver .ribbon-right,
.medal-silver .ribbon-connector {
    background: linear-gradient(135deg, #3366FF, #003399);
}

.medal-bronze .ribbon-left, 
.medal-bronze .ribbon-right,
.medal-bronze .ribbon-connector {
    background: linear-gradient(135deg, #009900, #006600);
}
</style>