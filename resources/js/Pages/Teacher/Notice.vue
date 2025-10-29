<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useToast } from '../../composables/useToast';

// Initialize toast
const { showSuccess, showError, showInfo, showWarning } = useToast();
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

const pendingOutputs = ref([]);
const isLoadingPending = ref(false);

// Load pending approvals from API
const loadPendingApprovals = async () => {
    isLoadingPending.value = true;
    try {
        console.log('🔄 Loading pending approvals...');
        const response = await axios.get('/api/submissions/pending-approvals/');
        console.log('📥 API Response:', response.data);
        
        if (response.data) {
            pendingOutputs.value = response.data.map(submission => {
                // Get image URL from multiple possible sources
                const imageUrl = submission.file_url || submission.file_path || submission.file || '';
                console.log('Submission:', {
                    id: submission.id,
                    student: submission.student_name,
                    activity: submission.activity_title,
                    imageUrl: imageUrl,
                    approval_status: submission.approval_status
                });
                
                return {
                    id: submission.id,
                    studentName: submission.student_name || submission.student?.username || 'Unknown',
                    title: submission.activity_title || 'Untitled',
                    subject: submission.activity_type || 'Unknown',
                    description: submission.caption || 'No caption provided',
                    submittedDate: submission.submitted_at ? new Date(submission.submitted_at).toLocaleDateString() : 'N/A',
                    sampleImages: imageUrl ? [imageUrl] : [],
                    file_path: imageUrl,
                    file_type: submission.file_type || 'image',
                    status: 'Pending'
                };
            });
            console.log('✅ Loaded pending approvals:', pendingOutputs.value.length, 'items');
        }
    } catch (error) {
        console.error('❌ Error loading pending approvals:', error);
        console.error('   Error response:', error.response?.data);
        console.error('   Error status:', error.response?.status);
        pendingOutputs.value = [];
    } finally {
        isLoadingPending.value = false;
    }
};

// Load on mount
onMounted(() => {
    loadPendingApprovals();
});

// Old hardcoded data (keeping for reference)
const oldPendingOutputs = ref([
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
const showApprovalDialog = ref(false);
const selectedOutput = ref(null);
const feedbackForm = ref({
    isApproved: false,
    rejectionReason: '',
    rejectionDetails: ''
});

const rejectionReasons = [
    { id: 'invalid', label: 'Invalid' },
    { id: 'unrelated', label: 'Unrelated' },
    { id: 'disturbing', label: 'Disturbing' },
    { id: 'lack_of_content', label: 'Lack of content' },
    { id: 'others', label: 'Others' }
];

const previewOutput = (output) => {
    selectedOutput.value = output;
    showPreviewDialog.value = true;
};

const submitFeedback = async (isApproved) => {
    if (!selectedOutput.value) return;
    
    try {
        const action = isApproved ? 'approve' : 'reject';
        const payload = {
            action: action
        };
        
        // Include rejection reason and details if rejecting
        if (!isApproved) {
            payload.rejectionReason = feedbackForm.value.rejectionReason;
            payload.rejectionDetails = feedbackForm.value.rejectionDetails;
        }
        
        const response = await axios.put(`/api/submissions/${selectedOutput.value.id}/approve/`, payload);
        
        if (response.data) {
            console.log(`Submission ${action}d:`, response.data);
            
            // Remove from pending list
            const index = pendingOutputs.value.findIndex(o => o.id === selectedOutput.value.id);
            if (index !== -1) {
                pendingOutputs.value.splice(index, 1);
            }
            
            showPreviewDialog.value = false;
            showRejectionDialog.value = false;
            
            // Reset form
            feedbackForm.value = {
                isApproved: false,
                rejectionReason: '',
                rejectionDetails: ''
            };
            
            const message = isApproved 
                ? 'Output approved and posted to class feed!' 
                : 'Output rejected. Student has been notified.';
            showSuccess(message, isApproved ? 'Approved' : 'Rejected');
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
        showError(error.response?.data?.error || error.message, 'Send Failed');
    }
};

// Cancel/Remove pending request
const cancelRequest = async (output) => {
    if (!confirm(`Are you sure you want to cancel this post request from ${output.studentName}?`)) {
        return;
    }
    
    try {
        // Cancel by rejecting with a specific reason
        const response = await axios.put(`/api/submissions/${output.id}/approve/`, {
            action: 'cancel'
        });
        
        if (response.data) {
            // Remove from pending list
            const index = pendingOutputs.value.findIndex(o => o.id === output.id);
            if (index !== -1) {
                pendingOutputs.value.splice(index, 1);
            }
            
            showInfo('Post request cancelled', 'Cancelled');
        }
    } catch (error) {
        console.error('Error cancelling request:', error);
        showError(error.response?.data?.error || 'Failed to cancel request', 'Error');
    }
};

const showApprovalConfirmDialog = () => {
    showApprovalDialog.value = true;
};

const confirmApproval = async () => {
    showApprovalDialog.value = false;
    await submitFeedback(true);
};

const cancelApproval = () => {
    showApprovalDialog.value = false;
};

const showRejectionReasonsDialog = () => {
    // Keep the review dialog open so teacher can see the work
    showRejectionDialog.value = true; // Open the rejection dialog
};

const confirmRejection = async () => {
    if (!feedbackForm.value.rejectionReason) {
        showWarning('Please fill in all fields', 'Missing Information');
        return;
    }
    await submitFeedback(false);
};

const cancelRejection = () => {
    showRejectionDialog.value = false;
    feedbackForm.value.rejectionReason = '';
    feedbackForm.value.rejectionDetails = '';
};
</script>

<template>
    <div class="flex flex-col">
        <!-- Header -->
        <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 shadow-lg rounded-t-xl h-40 md:h-36 flex items-center px-6 md:px-8">
            <h1 class="text-3xl md:text-4xl font-bold text-white flex items-center gap-3">
                <i class="pi pi-check-circle"></i>
                Student Output Approval
            </h1>
        </div>

        <div class="w-full bg-white/80 flex-1">
            <div class="p-4 md:p-6">
                <div class="rounded-2xl shadow-lg bg-white/90 backdrop-blur-sm border border-indigo-100 overflow-hidden">

            <!-- Pending Count -->
            <div class="px-6 py-4 bg-indigo-50 border-b border-indigo-100 flex justify-between items-center">
                <h2 class="text-lg font-medium text-indigo-900">Pending Approvals</h2>
                <span class="bg-indigo-600 text-white text-sm font-medium px-3 py-1 rounded-full">
                    {{ pendingOutputs.length }} Pending
                </span>
            </div>

            <!-- Loading State -->
            <div v-if="isLoadingPending" class="p-12 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
                <p class="text-gray-600">Loading pending approvals...</p>
            </div>

            <!-- Empty State -->
            <div v-else-if="pendingOutputs.length === 0" class="p-12 text-center">
                <i class="pi pi-inbox text-4xl text-gray-400 mb-4"></i>
                <p class="text-gray-600 text-lg font-medium">No pending approvals</p>
                <p class="text-gray-500 text-sm mt-2">Students' post requests will appear here</p>
            </div>

            <!-- Outputs List -->
            <div v-else class="divide-y divide-indigo-100">
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
                                    <div class="text-sm font-medium text-indigo-900 mb-2">Student Work:</div>
                                    <div class="flex gap-2 overflow-x-auto pb-2">
                                        <div v-if="output.sampleImages && output.sampleImages.length > 0 && output.sampleImages[0]" class="relative">
                                            <img 
                                                :src="output.sampleImages[0]"
                                                class="h-24 w-auto rounded-md border border-indigo-200 cursor-pointer hover:opacity-90 transition-opacity"
                                                @click="previewOutput(output)"
                                                @error="(e) => { console.error('Image failed to load:', output.sampleImages[0]); e.target.src = 'data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'100\' height=\'100\'%3E%3Crect fill=\'%23ddd\' width=\'100\' height=\'100\'/%3E%3Ctext x=\'50%25\' y=\'50%25\' text-anchor=\'middle\' dy=\'.3em\' fill=\'%23999\'%3ENo Image%3C/text%3E%3C/svg%3E'; }"
                                                :alt="`${output.studentName}'s work for ${output.title}`"
                                            />
                                        </div>
                                        <div v-else class="h-24 w-24 rounded-md border border-indigo-200 bg-gray-100 flex items-center justify-center">
                                            <i class="pi pi-image text-2xl text-gray-400"></i>
                                        </div>
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
                                </div>
                            </div>
                        </div>
                        <div class="flex flex-col gap-2">
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
            :closable="true"
            header="Review Student Output"
            :style="{ width: '70vw', maxWidth: '800px' }"
            :dismissableMask="true"
        >
            <div v-if="selectedOutput" class="space-y-6">
                <!-- Student Info -->
                <div class="bg-indigo-50 p-4 rounded-lg border border-indigo-100">
                    <div class="flex items-center space-x-3">
                        <span class="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-sm font-medium text-white">
                            {{ selectedOutput.studentName.charAt(0) }}
                        </span>
                        <div class="flex items-center gap-3">
                            <h3 class="font-medium text-indigo-900">{{ selectedOutput.studentName }}</h3>
                            <p class="text-sm text-indigo-700/80">{{ selectedOutput.subject }}</p>
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
                        <label class="block text-sm font-medium text-indigo-900 mb-2">Student Work</label>
                        <div class="border-2 border-indigo-200 rounded-lg overflow-hidden bg-gray-50">
                            <div class="flex items-center justify-center p-4" style="min-height: 300px;">
                                <img 
                                    v-if="selectedOutput.sampleImages && selectedOutput.sampleImages.length > 0 && selectedOutput.sampleImages[0]"
                                    :src="selectedOutput.sampleImages[0]" 
                                    class="w-full h-auto max-h-[500px] object-contain rounded"
                                    :alt="`${selectedOutput.studentName}'s work for ${selectedOutput.title}`"
                                    @error="(e) => { 
                                        console.error('Image load error:', e.target.src); 
                                        console.error('File type:', selectedOutput.file_type);
                                        console.error('File path:', selectedOutput.file_path);
                                    }"
                                />
                                <div v-else class="text-center py-12">
                                    <i class="pi pi-image text-6xl text-gray-400 mb-4"></i>
                                    <p class="text-gray-600 text-lg font-medium">No image available</p>
                                    <p class="text-sm text-gray-500 mt-2">File type: {{ selectedOutput.file_type || 'Unknown' }}</p>
                                    <p class="text-xs text-gray-400 mt-1">The student's work could not be displayed</p>
                                </div>
                            </div>
                            <div class="p-3 bg-indigo-50 border-t border-indigo-200 text-center">
                                <p class="text-sm font-medium text-indigo-900">
                                    <i class="pi pi-user mr-2"></i>
                                    {{ selectedOutput.studentName }}'s Work
                                </p>
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
                        @click="showApprovalConfirmDialog"
                    />
                </div>
            </template>
        </Dialog>

        <!-- Rejection Confirmation Dialog -->
        <Dialog 
            v-model:visible="showRejectionDialog"
            modal
            header="Confirm Rejection"
            :style="{ width: '90vw', maxWidth: '500px' }"
            :dismissableMask="true"
        >
            <div class="p-6">
                <div class="mb-6 text-center">
                    <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-red-100 mb-4">
                        <i class="pi pi-times-circle text-3xl text-red-600"></i>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Reject this submission?</h3>
                    <p class="text-sm text-gray-600">
                        This will reject <strong>{{ selectedOutput?.studentName }}'s</strong> work 
                        "<strong>{{ selectedOutput?.title }}</strong>".
                    </p>
                </div>

                <div class="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                    <div class="flex items-start gap-3">
                        <i class="pi pi-info-circle text-red-600 mt-0.5"></i>
                        <div class="text-sm text-red-800">
                            <p class="font-medium mb-1">What happens next:</p>
                            <ul class="list-disc list-inside space-y-1 text-red-700">
                                <li>The submission will NOT be posted to the class feed</li>
                                <li>The student will be notified of the rejection</li>
                                <li>The student can resubmit their work</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- Rejection Reason Selection -->
                <div class="mb-4">
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
                                class="w-4 h-4 text-red-600 focus:ring-red-500"
                            />
                            <label :for="reason.id" class="ml-2 text-sm text-gray-700">
                                {{ reason.label }}
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Additional Details -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                        Additional Details (Optional)
                    </label>
                    <textarea
                        v-model="feedbackForm.rejectionDetails"
                        rows="3"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
                        placeholder="Provide additional context for the rejection..."
                    ></textarea>
                </div>
            </div>

            <template #footer>
                <div class="flex justify-end gap-3 px-6 pb-6">
                    <Button 
                        label="Cancel"
                        class="p-button-secondary"
                        style="background: #f3f4f6; border: 1px solid #d1d5db; color: #1f2937;" 
                        @click="cancelRejection"
                    />
                    <Button 
                        label="Yes, Reject"
                        :disabled="!feedbackForm.rejectionReason"
                        style="background: linear-gradient(to right, #dc2626, #ef4444); border: none; color: white;" 
                        @click="confirmRejection"
                    >
                        <i class="pi pi-times mr-2"></i>
                        Yes, Reject
                    </Button>
                </div>
            </template>
        </Dialog>

        <!-- Approval Confirmation Dialog -->
        <Dialog 
            v-model:visible="showApprovalDialog"
            modal
            header="Confirm Approval"
            :style="{ width: '90vw', maxWidth: '500px' }"
            :dismissableMask="true"
        >
            <div class="p-6">
                <div class="mb-6 text-center">
                    <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-green-100 mb-4">
                        <i class="pi pi-check-circle text-3xl text-green-600"></i>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Approve this submission?</h3>
                    <p class="text-sm text-gray-600">
                        This will approve <strong>{{ selectedOutput?.studentName }}'s</strong> work 
                        "<strong>{{ selectedOutput?.title }}</strong>" to be posted to the class feed.
                    </p>
                </div>

                <div class="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                    <div class="flex items-start gap-3">
                        <i class="pi pi-info-circle text-green-600 mt-0.5"></i>
                        <div class="text-sm text-green-800">
                            <p class="font-medium mb-1">What happens next:</p>
                            <ul class="list-disc list-inside space-y-1 text-green-700">
                                <li>The submission will be visible to all students in the class</li>
                                <li>It will appear in the class newsfeed</li>
                                <li>The student will be notified of the approval</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <template #footer>
                <div class="flex justify-end gap-3 px-6 pb-6">
                    <Button 
                        label="Cancel"
                        class="p-button-secondary"
                        style="background: #f3f4f6; border: 1px solid #d1d5db; color: #1f2937;" 
                        @click="cancelApproval"
                    />
                    <Button 
                        label="Yes, Approve"
                        style="background: linear-gradient(to right, #10b981, #059669); border: none; color: white;" 
                        @click="confirmApproval"
                    >
                        <i class="pi pi-check mr-2"></i>
                        Yes, Approve
                    </Button>
                </div>
            </template>
        </Dialog>
            </div>
        </div>
        </div>
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

</style>