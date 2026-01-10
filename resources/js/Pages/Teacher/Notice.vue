<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useToast } from '../../composables/useToast';

// Define emits for navigation
const emit = defineEmits(['navigate']);

// Initialize toast
const { showSuccess, showError, showInfo, showWarning } = useToast();
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';

const pendingOutputs = ref([]);
const allPendingOutputs = ref([]); // Store all outputs before filtering
const isLoadingPending = ref(false);
const itemsPerPage = 5;
const displayedPendingCount = ref(itemsPerPage);

// Classroom filter
const classrooms = ref([]);
const selectedClassroom = ref(null);

// Helper function to get initials from name
const getInitials = (name) => {
    if (!name) return '?';
    const parts = name.trim().split(' ').filter(p => p.length > 0);
    if (parts.length >= 2) {
        return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
    }
    return name.charAt(0).toUpperCase();
};

// Helper function to format date and time
const formatDateTime = (dateString) => {
    if (!dateString) return { formatted: 'N/A', daysAgo: '', timestamp: 0 };

    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
    const diffMinutes = Math.floor(diffTime / (1000 * 60));

    // Format: Nov 6, 2025 — 10:45 PM (Manila Time)
    const formatted = date.toLocaleDateString('en-PH', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        timeZone: 'Asia/Manila'
    }) + ' — ' + date.toLocaleTimeString('en-PH', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
        timeZone: 'Asia/Manila'
    });

    // Calculate "days ago" text
    let daysAgo = '';
    if (diffMinutes < 1) {
        daysAgo = 'Just now';
    } else if (diffMinutes < 60) {
        daysAgo = `${diffMinutes} minute${diffMinutes !== 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
        daysAgo = `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    } else if (diffDays === 1) {
        daysAgo = '1 day ago';
    } else if (diffDays < 30) {
        daysAgo = `${diffDays} days ago`;
    } else {
        const months = Math.floor(diffDays / 30);
        daysAgo = `${months} month${months !== 1 ? 's' : ''} ago`;
    }

    return {
        formatted,
        daysAgo,
        timestamp: date.getTime()
    };
};

// Load classrooms for dropdown
const loadClassrooms = async () => {
    try {
        // Get teacher's assigned classrooms
        const assignedResponse = await axios.get('/api/classrooms/');
        let assignedClassrooms = [];
        if (assignedResponse.data && assignedResponse.data.classrooms) {
            assignedClassrooms = assignedResponse.data.classrooms;
        }
        
        // Get classrooms where teacher has folders
        const foldersResponse = await axios.get('/api/portfolio/folders/?current_school_year=true');
        let folderClassroomIds = new Set();
        if (foldersResponse.data) {
            foldersResponse.data.forEach(folder => {
                if (folder.classroom) {
                    folderClassroomIds.add(folder.classroom);
                }
            });
        }
        
        // Build classroom map
        const classroomMap = new Map();
        assignedClassrooms.forEach(c => {
            classroomMap.set(c.id, {
                id: c.id,
                name: c.name,
                isAssigned: true
            });
        });
        
        // Add classrooms from folders
        for (const classroomId of folderClassroomIds) {
            if (!classroomMap.has(classroomId)) {
                try {
                    const classroomResponse = await axios.get(`/api/classrooms/${classroomId}/`);
                    if (classroomResponse.data && !classroomResponse.data.is_archived) {
                        classroomMap.set(classroomId, {
                            id: classroomResponse.data.id,
                            name: classroomResponse.data.name,
                            isAssigned: false
                        });
                    }
                } catch (err) {
                    console.error(`Failed to fetch classroom ${classroomId}:`, err);
                }
            }
        }
        
        // Convert to array - assigned first
        const allClassrooms = Array.from(classroomMap.values());
        allClassrooms.sort((a, b) => {
            if (a.isAssigned && !b.isAssigned) return -1;
            if (!a.isAssigned && b.isAssigned) return 1;
            return a.name.localeCompare(b.name);
        });
        
        classrooms.value = allClassrooms;
        
        // Auto-select first classroom
        if (classrooms.value.length > 0) {
            selectedClassroom.value = classrooms.value[0];
        }
        
        console.log('📚 Loaded classrooms for approvals:', classrooms.value);
    } catch (error) {
        console.error('Error loading classrooms:', error);
    }
};

// Handle classroom change
const onClassroomChange = () => {
    filterPendingByClassroom();
};

// Filter pending outputs by selected classroom
const filterPendingByClassroom = () => {
    if (!selectedClassroom.value) {
        pendingOutputs.value = allPendingOutputs.value;
    } else {
        pendingOutputs.value = allPendingOutputs.value.filter(output => 
            output.classroomId === selectedClassroom.value.id ||
            output.classroomName === selectedClassroom.value.name
        );
    }
    displayedPendingCount.value = itemsPerPage;
};

// Load pending approvals from API
const loadPendingApprovals = async () => {
    isLoadingPending.value = true;
    try {
        console.log('🔄 Loading pending approvals...');
        const response = await axios.get('/api/submissions/pending-approvals/');
        console.log('📥 API Response:', response.data);

        if (response.data) {
            // Map and format submissions (backend already sorted them properly)
            pendingOutputs.value = response.data.map(submission => {
                // Check if submission has multiple files
                const submissionFiles = submission.files || [];
                let sampleImages = [];
                let fileTypes = [];

                if (submissionFiles.length > 0) {
                    // Process multiple files
                    submissionFiles.forEach(file => {
                        let fileUrl = file.file_url || file.file_path || '';
                        const fileType = file.file_type || 'unknown';
                        
                        // Build proper URL
                        if (fileUrl && !fileUrl.startsWith('http') && !fileUrl.startsWith('data:')) {
                            fileUrl = `http://localhost:8000${fileUrl.startsWith('/') ? '' : '/'}${fileUrl}`;
                        }
                        
                        if (fileUrl) {
                            sampleImages.push(fileUrl);
                            fileTypes.push(fileType);
                        }
                    });
                } else {
                    // Fallback to single file from main submission
                    let imageUrl = submission.file_url || submission.file_path || submission.file || '';
                    const fileType = submission.file_type || 'unknown';

                    // Check if file is actually an image
                    const isImageFile = imageUrl && (
                        imageUrl.toLowerCase().endsWith('.jpg') ||
                        imageUrl.toLowerCase().endsWith('.jpeg') ||
                        imageUrl.toLowerCase().endsWith('.png') ||
                        imageUrl.toLowerCase().endsWith('.gif') ||
                        imageUrl.toLowerCase().endsWith('.webp') ||
                        imageUrl.toLowerCase().endsWith('.svg') ||
                        fileType.toLowerCase().startsWith('image')
                    );

                    // Build proper URL
                    if (imageUrl && !imageUrl.startsWith('http') && !imageUrl.startsWith('data:')) {
                        imageUrl = `http://localhost:8000${imageUrl.startsWith('/') ? '' : '/'}${imageUrl}`;
                    }

                    if (imageUrl) {
                        sampleImages.push(imageUrl);
                        fileTypes.push(fileType);
                    }
                }

                const dateInfo = formatDateTime(submission.post_requested_at || submission.submitted_at);
                
                // Check if this is from Sketch Pad (no activity or activity_title is "Sketch Pad")
                const isSketchPad = !submission.activity || 
                                    submission.activity_title === 'Sketch Pad' || 
                                    submission.activity_title === 'Sketch' ||
                                    (submission.activity_type && submission.activity_type.toLowerCase() === 'sketch');

                return {
                    id: submission.id,
                    studentName: submission.student_name || submission.student?.username || 'Unknown',
                    profilePicture: submission.student?.profile_picture_url || null,
                    title: submission.activity_title || 'Sketch Pad',
                    subject: submission.activity_type || 'Sketch',
                    description: submission.post_caption || submission.caption || 'No caption',
                    submittedDate: dateInfo.formatted,
                    daysAgo: dateInfo.daysAgo,
                    timestamp: dateInfo.timestamp,
                    rawDate: submission.post_requested_at || submission.submitted_at,
                    sampleImages: sampleImages,
                    fileTypes: fileTypes,
                    file_path: submission.file_url || submission.file_path,
                    file_type: submission.file_type || (fileTypes.length > 0 ? fileTypes[0] : 'unknown'),
                    isImageFile: fileTypes.some(t => t === 'image'),
                    isSketchPad: isSketchPad,
                    status: 'Pending',
                    files: submissionFiles,
                    // Classroom info for filtering
                    classroomId: submission.classroom_id || submission.student?.classroom_id,
                    classroomName: submission.classroom_name || submission.student?.classroom_name
                };
            });

            // Store all outputs for filtering
            allPendingOutputs.value = pendingOutputs.value;
            
            // Apply classroom filter
            filterPendingByClassroom();

            console.log('✅ Loaded pending approvals:', allPendingOutputs.value.length, 'items');
            console.log('📊 Display order (as received from backend - already sorted):');
            pendingOutputs.value.forEach((item, index) => {
                console.log(`   ${index + 1}. ${item.studentName} - ${item.title} - ${item.submittedDate} - ${item.sampleImages.length} files`);
            });
        }
    } catch (error) {
        console.error('❌ Error loading pending approvals:', error);
        console.error('   Error response:', error.response?.data);
        console.error('   Error status:', error.response?.status);
        pendingOutputs.value = [];
        allPendingOutputs.value = [];
    } finally {
        isLoadingPending.value = false;
    }
};

// Load on mount
onMounted(async () => {
    await loadClassrooms();
    await loadPendingApprovals();
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
const currentFileIndex = ref(0); // For navigating multiple files
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
    currentFileIndex.value = 0; // Reset to first file
    showPreviewDialog.value = true;
};

// Navigate to previous file
const previousOutputFile = () => {
    if (currentFileIndex.value > 0) {
        currentFileIndex.value--;
    }
};

// Navigate to next file
const nextOutputFile = () => {
    const totalFiles = selectedOutput.value?.sampleImages?.length || 1;
    if (currentFileIndex.value < totalFiles - 1) {
        currentFileIndex.value++;
    }
};

// Get current file to display
const currentOutputFile = computed(() => {
    if (!selectedOutput.value) return null;
    const images = selectedOutput.value.sampleImages || [];
    if (images.length > 0) {
        return images[currentFileIndex.value] || images[0];
    }
    return null;
});

// Get current file type
const currentOutputFileType = computed(() => {
    if (!selectedOutput.value) return 'unknown';
    const fileTypes = selectedOutput.value.fileTypes || [];
    if (fileTypes.length > 0) {
        return fileTypes[currentFileIndex.value] || fileTypes[0] || 'unknown';
    }
    return selectedOutput.value.file_type || 'unknown';
});

// Check if current file is an image
const isCurrentFileImage = computed(() => {
    const fileType = currentOutputFileType.value;
    const fileUrl = currentOutputFile.value || '';
    return fileType === 'image' || 
           fileUrl.toLowerCase().endsWith('.jpg') ||
           fileUrl.toLowerCase().endsWith('.jpeg') ||
           fileUrl.toLowerCase().endsWith('.png') ||
           fileUrl.toLowerCase().endsWith('.gif') ||
           fileUrl.toLowerCase().endsWith('.webp');
});

// Get total files count
const totalOutputFiles = computed(() => {
    return selectedOutput.value?.sampleImages?.length || 0;
});

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
                Student Posting Approval
            </h1>
        </div>

        <div class="w-full bg-white/80 flex-1">
            <div class="p-4 md:p-6">
                <div class="rounded-2xl shadow-lg bg-white/90 backdrop-blur-sm border border-indigo-100 overflow-hidden">

            <!-- Pending Count -->
            <div class="px-6 py-4 bg-indigo-50 border-b border-indigo-100 flex justify-between items-center gap-4">
                <div class="flex items-center gap-4">
                    <h2 class="text-lg font-medium text-indigo-900 whitespace-nowrap">Pending Approvals</h2>
                    <Dropdown
                        v-model="selectedClassroom"
                        :options="classrooms"
                        optionLabel="name"
                        placeholder="Select Class"
                        class="w-40"
                        @change="onClassroomChange"
                    >
                        <template #value="slotProps">
                            <span v-if="slotProps.value" class="font-medium text-sm">{{ slotProps.value.name }}</span>
                            <span v-else class="text-gray-500 text-sm">Select Class</span>
                        </template>
                        <template #option="slotProps">
                            <span class="font-medium">{{ slotProps.option.name }}</span>
                        </template>
                    </Dropdown>
                </div>
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
                <div v-for="output in pendingOutputs.slice(0, displayedPendingCount)" :key="output.id"
                    class="p-6 hover:bg-indigo-50/50 transition-colors duration-200 border-l-4 border-transparent hover:border-indigo-400">
                    <div class="flex justify-between items-start gap-4">
                        <div class="flex-1">
                            <div class="flex items-center space-x-3 mb-3">
                                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center text-white font-bold shadow-md overflow-hidden flex-shrink-0">
                                    <img v-if="output.profilePicture" :src="output.profilePicture" :alt="output.studentName" class="w-full h-full object-cover" />
                                    <span v-else>{{ getInitials(output.studentName) }}</span>
                                </div>
                                <div class="flex-1">
                                    <div class="flex items-center gap-2 flex-wrap">
                                        <h3 class="font-semibold text-indigo-900 text-base">{{ output.studentName }}</h3>
                                        <span v-if="output.isSketchPad" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-violet-100 text-violet-700">
                                            <i class="pi pi-pencil mr-1 text-xs"></i>
                                            Sketch Pad
                                        </span>
                                        <span v-else class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-700">
                                            <i class="pi pi-book mr-1 text-xs"></i>
                                            {{ output.subject }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <p class="text-indigo-900/80 text-sm leading-relaxed mb-3 line-clamp-2" :title="output.description">{{ output.description || 'No caption' }}</p>

                                <!-- Submission Date/Time -->
                                <div class="flex items-center gap-4 text-sm mb-3">
                                    <div class="flex items-center gap-1.5 text-indigo-700/90">
                                        <i class="pi pi-clock text-xs"></i>
                                        <span class="font-medium">Requested on:</span>
                                        <span>{{ output.submittedDate }}</span>
                                    </div>
                                    <span v-if="output.daysAgo" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-violet-100 text-violet-700">
                                        {{ output.daysAgo }}
                                    </span>
                                </div>

                                <div class="mt-3">
                                    <div class="text-sm font-semibold text-indigo-900 mb-2">Student Work:</div>
                                    <div class="flex gap-2 overflow-x-auto pb-2">
                                        <!-- Image File Display -->
                                        <div v-if="output.isImageFile && output.sampleImages && output.sampleImages.length > 0 && output.sampleImages[0]" class="relative group cursor-pointer">
                                            <img
                                                :src="output.sampleImages[0]"
                                                class="h-28 w-auto rounded-lg border-2 border-indigo-200 cursor-pointer hover:border-indigo-500 hover:shadow-xl transition-all duration-300 group-hover:scale-105"
                                                @click="previewOutput(output)"
                                                @error="(e) => { console.error('Image failed to load:', output.sampleImages[0]); }"
                                                :alt="`${output.studentName}'s work`"
                                                :title="`Click to preview ${output.studentName}'s work`"
                                            />
                                            <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 rounded-lg transition-all duration-300 flex items-center justify-center">
                                                <div class="flex flex-col items-center gap-1">
                                                    <i class="pi pi-search-plus text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-2xl drop-shadow-lg"></i>
                                                    <span class="text-white text-xs opacity-0 group-hover:opacity-100 transition-opacity duration-300 font-medium">Click to Preview</span>
                                                </div>
                                            </div>
                                        </div>
                                        <!-- Non-Image File Display -->
                                        <div v-else-if="output.file_path && !output.isImageFile" class="relative group cursor-pointer h-28 w-28 rounded-lg border-2 border-indigo-200 bg-indigo-50 flex flex-col items-center justify-center hover:bg-indigo-100 hover:border-indigo-500 hover:shadow-xl transition-all duration-300 group-hover:scale-105">
                                            <i class="pi pi-file text-3xl text-indigo-600 mb-1"></i>
                                            <span class="text-xs text-indigo-700 font-medium text-center px-1 truncate">{{ output.file_type || 'File' }}</span>
                                            <span class="text-xs text-gray-500 mt-1">{{ output.file_path.split('/').pop().substring(0, 12) }}...</span>
                                        </div>
                                        <!-- No File Display -->
                                        <div v-else class="h-28 w-28 rounded-lg border-2 border-indigo-200 bg-gray-100 flex items-center justify-center">
                                            <i class="pi pi-image text-3xl text-gray-400"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="flex flex-col gap-2 flex-shrink-0">
                            <Button
                                label="Review"
                                icon="pi pi-eye"
                                class="p-button-sm whitespace-nowrap"
                                style="background: linear-gradient(to right, #4f46e5, #6366f1); border: none; box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);"
                                @click="previewOutput(output)"
                            />
                        </div>
                    </div>
                </div>
            </div>

                <!-- Load More Button -->
                <div v-if="displayedPendingCount < pendingOutputs.length" class="p-6 text-center border-t border-indigo-100 bg-indigo-50/50">
                    <button
                        @click="displayedPendingCount += itemsPerPage"
                        class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors duration-200 flex items-center gap-2 mx-auto"
                    >
                        <i class="pi pi-chevron-down"></i>
                        <span>Load More ({{ pendingOutputs.length - displayedPendingCount }} more)</span>
                    </button>
                </div>

        <!-- Preview Dialog -->
        <Dialog
            v-model:visible="showPreviewDialog"
            modal
            :closable="true"
            header="Review Student Output"
            :style="{ width: '600px', maxWidth: '90vw', height: 'auto', maxHeight: '95vh' }"
            :contentStyle="{ padding: '0' }"
            :dismissableMask="true"
        >
            <div v-if="selectedOutput" class="p-4">
                <!-- Student Info - Simplified -->
                <div class="flex items-center gap-3 mb-3">
                    <h3 class="font-semibold text-indigo-900 text-lg">{{ selectedOutput.studentName }}</h3>
                    <span v-if="selectedOutput.isSketchPad" class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-violet-100 text-violet-700">
                        <i class="pi pi-pencil mr-1 text-xs"></i>
                        Sketch Pad
                    </span>
                    <span v-else class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-700">
                        <i class="pi pi-book mr-1 text-xs"></i>
                        {{ selectedOutput.subject }}
                    </span>
                </div>

                <!-- Caption -->
                <div v-if="selectedOutput.description && selectedOutput.description !== 'No caption'" class="bg-gray-50 p-2 rounded-lg border border-gray-200 mb-3">
                    <p class="text-gray-700 text-sm">{{ selectedOutput.description }}</p>
                </div>

                <!-- Student Work - Auto height based on image -->
                <div class="border-2 border-indigo-200 rounded-lg overflow-hidden bg-gray-100">
                    <div class="flex items-center justify-center p-4 relative" style="min-height: 300px;">
                        <!-- Navigation Arrows (only show if multiple files) -->
                        <button
                            v-if="totalOutputFiles > 1"
                            @click="previousOutputFile"
                            :disabled="currentFileIndex === 0"
                            class="absolute left-2 top-1/2 -translate-y-1/2 z-10 w-10 h-10 rounded-full bg-white shadow-lg flex items-center justify-center transition-all hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed"
                        >
                            <i class="pi pi-chevron-left text-indigo-600 text-lg"></i>
                        </button>
                        
                        <button
                            v-if="totalOutputFiles > 1"
                            @click="nextOutputFile"
                            :disabled="currentFileIndex >= totalOutputFiles - 1"
                            class="absolute right-2 top-1/2 -translate-y-1/2 z-10 w-10 h-10 rounded-full bg-white shadow-lg flex items-center justify-center transition-all hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed"
                        >
                            <i class="pi pi-chevron-right text-indigo-600 text-lg"></i>
                        </button>

                        <!-- File Counter (only show if multiple files) -->
                        <div v-if="totalOutputFiles > 1" class="absolute top-2 left-1/2 transform -translate-x-1/2 z-10">
                            <div class="bg-indigo-600 text-white px-3 py-1 rounded-full text-xs font-medium shadow-lg">
                                {{ currentFileIndex + 1 }} / {{ totalOutputFiles }}
                            </div>
                        </div>

                        <!-- Image Display - Full size -->
                        <img
                            v-if="currentOutputFile && isCurrentFileImage"
                            :src="currentOutputFile"
                            class="max-w-full h-auto rounded"
                            style="max-height: 60vh;"
                            :alt="`${selectedOutput.studentName}'s work`"
                            @error="(e) => {
                                console.error('Image load error:', e.target.src);
                                console.error('File type:', currentOutputFileType);
                            }"
                        />
                        <!-- PDF Display -->
                        <div v-else-if="currentOutputFile && currentOutputFileType === 'pdf'" class="flex flex-col items-center justify-center text-red-600 py-8">
                            <i class="pi pi-file-pdf text-6xl mb-3"></i>
                            <span class="text-base font-medium">PDF Document</span>
                            <a :href="currentOutputFile" target="_blank" class="mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm">
                                <i class="pi pi-external-link mr-2"></i>View PDF
                            </a>
                        </div>
                        <!-- Document Display -->
                        <div v-else-if="currentOutputFile && currentOutputFileType === 'document'" class="flex flex-col items-center justify-center text-blue-600 py-8">
                            <i class="pi pi-file-word text-6xl mb-3"></i>
                            <span class="text-base font-medium">Document</span>
                            <a :href="currentOutputFile" target="_blank" class="mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm">
                                <i class="pi pi-external-link mr-2"></i>View Document
                            </a>
                        </div>
                        <!-- No file data -->
                        <div v-else class="text-center py-8">
                            <i class="pi pi-image text-5xl text-gray-400 mb-3"></i>
                            <p class="text-gray-600 font-medium">No file available</p>
                        </div>
                    </div>
                    <div class="p-2 bg-indigo-50 border-t border-indigo-200 flex items-center justify-between">
                        <p class="text-sm font-medium text-indigo-900">
                            {{ selectedOutput.studentName }}'s Work
                            <span v-if="totalOutputFiles > 1" class="text-indigo-600 ml-2">({{ totalOutputFiles }} files)</span>
                        </p>
                        <a 
                            v-if="currentOutputFile"
                            :href="currentOutputFile" 
                            target="_blank" 
                            class="text-sm text-indigo-600 hover:text-indigo-800 font-medium flex items-center gap-1"
                        >
                            <i class="pi pi-external-link"></i>
                            Full Size
                        </a>
                    </div>
                </div>
            </div>

            <template #footer>
                <div class="flex justify-end gap-2 px-4 py-3 border-t">
                    <Button
                        label="Cancel"
                        class="p-button-secondary p-button-sm"
                        style="background: #f3f4f6; border: 1px solid #d1d5db; color: #1f2937;"
                        @click="showPreviewDialog = false"
                    />
                    <Button
                        label="Reject"
                        class="p-button-danger p-button-sm"
                        style="background: linear-gradient(to right, #dc2626, #ef4444); border: none; color: white;"
                        @click="showRejectionReasonsDialog"
                    />
                    <Button
                        label="Approve"
                        class="p-button-sm"
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
            :style="{ width: '420px', maxWidth: '90vw' }"
            :contentStyle="{ padding: '0', overflow: 'visible' }"
            :dismissableMask="true"
        >
            <div class="p-4">
                <div class="mb-4 text-center">
                    <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-3">
                        <i class="pi pi-times-circle text-2xl text-red-600"></i>
                    </div>
                    <h3 class="text-base font-semibold text-gray-900 mb-1">Reject this submission?</h3>
                    <p class="text-xs text-gray-600">
                        This will reject <strong>{{ selectedOutput?.studentName }}'s</strong> work.
                    </p>
                </div>

                <div class="bg-red-50 border border-red-200 rounded-lg p-3 mb-3">
                    <div class="flex items-start gap-2">
                        <i class="pi pi-info-circle text-red-600 text-sm mt-0.5"></i>
                        <div class="text-xs text-red-800">
                            <p class="font-medium mb-1">What happens next:</p>
                            <ul class="list-disc list-inside space-y-0.5 text-red-700">
                                <li>Will NOT be posted to class feed</li>
                                <li>Student will be notified</li>
                                <li>Student can resubmit</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- Rejection Reason Selection -->
                <div class="mb-3">
                    <label class="block text-xs font-medium text-gray-700 mb-1">
                        Reason for Rejection <span class="text-red-500">*</span>
                    </label>
                    <div class="grid grid-cols-2 gap-1">
                        <div v-for="reason in rejectionReasons" :key="reason.id" class="flex items-center">
                            <input
                                type="radio"
                                :id="reason.id"
                                :value="reason.id"
                                v-model="feedbackForm.rejectionReason"
                                class="w-3 h-3 text-red-600 focus:ring-red-500"
                            />
                            <label :for="reason.id" class="ml-1.5 text-xs text-gray-700">
                                {{ reason.label }}
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Additional Details -->
                <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">
                        Additional Details (Optional)
                    </label>
                    <textarea
                        v-model="feedbackForm.rejectionDetails"
                        rows="2"
                        class="w-full px-2 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500"
                        placeholder="Provide additional context..."
                    ></textarea>
                </div>
            </div>

            <template #footer>
                <div class="flex justify-end gap-2 px-4 py-3 border-t">
                    <Button
                        label="Cancel"
                        class="p-button-secondary p-button-sm"
                        style="background: #f3f4f6; border: 1px solid #d1d5db; color: #1f2937;"
                        @click="cancelRejection"
                    />
                    <Button
                        label="Yes, Reject"
                        class="p-button-sm"
                        :disabled="!feedbackForm.rejectionReason"
                        style="background: linear-gradient(to right, #dc2626, #ef4444); border: none; color: white;"
                        @click="confirmRejection"
                    >
                        <i class="pi pi-times mr-1"></i>
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
            :style="{ width: '420px', maxWidth: '90vw' }"
            :contentStyle="{ padding: '0', overflow: 'visible' }"
            :dismissableMask="true"
        >
            <div class="p-4">
                <div class="mb-4 text-center">
                    <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 mb-3">
                        <i class="pi pi-check-circle text-2xl text-green-600"></i>
                    </div>
                    <h3 class="text-base font-semibold text-gray-900 mb-1">Approve this submission?</h3>
                    <p class="text-xs text-gray-600">
                        This will approve <strong>{{ selectedOutput?.studentName }}'s</strong> work to be posted.
                    </p>
                </div>

                <div class="bg-green-50 border border-green-200 rounded-lg p-3">
                    <div class="flex items-start gap-2">
                        <i class="pi pi-info-circle text-green-600 text-sm mt-0.5"></i>
                        <div class="text-xs text-green-800">
                            <p class="font-medium mb-1">What happens next:</p>
                            <ul class="list-disc list-inside space-y-0.5 text-green-700">
                                <li>Visible to all students in class</li>
                                <li>Will appear in class newsfeed</li>
                                <li>Student will be notified</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <template #footer>
                <div class="flex justify-end gap-2 px-4 py-3 border-t">
                    <Button
                        label="Cancel"
                        class="p-button-secondary p-button-sm"
                        style="background: #f3f4f6; border: 1px solid #d1d5db; color: #1f2937;"
                        @click="cancelApproval"
                    />
                    <Button
                        label="Yes, Approve"
                        class="p-button-sm"
                        style="background: linear-gradient(to right, #10b981, #059669); border: none; color: white;"
                        @click="confirmApproval"
                    >
                        <i class="pi pi-check mr-1"></i>
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
