<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import Dialog from 'primevue/dialog';
import Textarea from 'primevue/textarea';

// Load activity from localStorage
const activity = ref({
    title: 'Student Activity',
    description: 'View student submissions for this activity',
    id: null
});

// Load selected activity on component mount
onMounted(() => {
    const savedActivity = localStorage.getItem('selected_activity');
    if (savedActivity) {
        const parsedActivity = JSON.parse(savedActivity);
        activity.value = {
            title: parsedActivity.title,
            description: parsedActivity.description || 'View student submissions for this activity',
            id: parsedActivity.id,
            type: parsedActivity.type,
            dueDate: parsedActivity.dueDate,
            scoringCriteria: parsedActivity.scoringCriteria,
            subject: parsedActivity.subject  // Add subject field
        };
        console.log('Loaded activity:', activity.value);
    }
    
    // Load submissions for this specific activity
    loadUnscoredSubmissions();
    loadScoredSubmissions();
});

// Define emits for navigation
const emit = defineEmits(['navigate']);

const goBack = () => {
    // Store the subject/folder context so Room.vue can show the activities list
    console.log('Going back with activity:', activity.value);
    if (activity.value.subject) {
        const returnData = {
            subject: activity.value.subject,
            showActivities: true
        };
        console.log('Storing return context:', returnData);
        localStorage.setItem('return_to_activities', JSON.stringify(returnData));
    } else {
        console.warn('No subject found in activity, cannot restore activities view');
    }
    emit('navigate', 'TeacherRoom');
};

// Add view mode state
const viewMode = ref('list'); // 'list' or 'card'

const toggleView = (mode) => {
    viewMode.value = mode;
};

// Sample student submissions data with their self-portrait artworks
// Updated to match the data structure in notice.vue
const studentOutputs = ref({
    '2021-0001': {
        title: 'Self-Portrait: Reflections of Me',
        description: 'A mixed media self-portrait combining acrylic paint, collage elements, and charcoal. The artwork explores my dual heritage with symbolic elements representing both cultures.',
        date: 'Mar 18, 2025',
        status: 'Completed',
        image: 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80',
        rank: 1,
    },
    '2021-0002': {
        title: 'Self-Portrait: Through My Eyes',
        description: 'Watercolor and ink self-portrait focusing on expressive eyes and subtle facial expressions. The background incorporates abstract patterns representing my thoughts.',
        date: 'Mar 26, 2025',
        status: 'In Progress',
        image: 'https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80',
        rank: 2,
    },
    '2021-0003': {
        title: 'Self-Portrait: Digital Me',
        description: 'Digital painting created using Procreate, showcasing a stylized version of myself with vibrant colors and geometric elements in the background.',
        date: 'Mar 15, 2025',
        status: 'Pending Review',
        image: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80',
        rank: 3,
    }
});

const submissions = ref([]);
const scoredSubmissionsData = ref([]);
const isLoadingSubmissions = ref(false);

// Load unscored submissions from API
const loadUnscoredSubmissions = async () => {
    isLoadingSubmissions.value = true;
    try {
        const response = await axios.get('/api/submissions/unscored/');
        if (response.data) {
            console.log('All unscored submissions:', response.data);
            console.log('Filtering by activity ID:', activity.value.id);
            
            // Filter submissions by the current activity ID
            const filteredSubmissions = response.data.filter(submission => {
                // Try both activity and activity_id fields
                const submissionActivityId = submission.activity || submission.activity_id;
                console.log('Submission activity ID:', submissionActivityId, 'matches:', submissionActivityId === activity.value.id);
                return submissionActivityId === activity.value.id;
            });
            
            submissions.value = filteredSubmissions.map(submission => ({
                id: submission.id,
                studentId: submission.student.id,
                name: submission.student.username,
                activityTitle: submission.activity_title,
                activityType: submission.activity_type,
                caption: submission.caption,
                score: submission.score,
                status: 'Submitted',
                date: new Date(submission.submitted_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                })
            }));
            console.log('Loaded unscored submissions for activity:', activity.value.id, submissions.value);
        }
    } catch (error) {
        console.error('Error loading submissions:', error);
        submissions.value = [];
    } finally {
        isLoadingSubmissions.value = false;
    }
};

// Load scored submissions from API
const loadScoredSubmissions = async () => {
    try {
        const response = await axios.get('/api/submissions/scored/');
        if (response.data) {
            console.log('All scored submissions:', response.data);
            
            // Filter submissions by the current activity ID
            const filteredSubmissions = response.data.filter(submission => {
                // Try both activity and activity_id fields
                const submissionActivityId = submission.activity || submission.activity_id;
                return submissionActivityId === activity.value.id;
            });
            
            scoredSubmissionsData.value = filteredSubmissions.map(submission => ({
                id: submission.id,
                studentId: submission.student.id,
                name: submission.student.username,
                activityTitle: submission.activity_title,
                activityType: submission.activity_type,
                caption: submission.caption,
                score: submission.score,
                status: 'Scored',
                date: new Date(submission.scored_at || submission.submitted_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                })
            }));
            console.log('Loaded scored submissions for activity:', activity.value.id, scoredSubmissionsData.value);
        }
    } catch (error) {
        console.error('Error loading scored submissions:', error);
        scoredSubmissionsData.value = [];
    }
};

// Dialog state and selected submission
const showSubmissionDialog = ref(false);
const selectedSubmission = ref(null);
const isLoadingSubmissionDetail = ref(false);

// Load full submission details including image
const loadSubmissionDetail = async (submissionId) => {
    isLoadingSubmissionDetail.value = true;
    try {
        const response = await axios.get(`/api/submissions/${submissionId}/`);
        if (response.data) {
            return {
                id: response.data.id,
                studentId: response.data.student.id,
                name: response.data.student.username,
                activityTitle: response.data.activity_title,
                activityType: response.data.activity_type,
                caption: response.data.caption,
                filePath: response.data.file_path,
                fileType: response.data.file_type,
                score: response.data.score,
                status: response.data.status === 'scored' ? 'Scored' : 'Submitted',
                date: new Date(response.data.submitted_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                })
            };
        }
    } catch (error) {
        console.error('Error loading submission detail:', error);
        return null;
    } finally {
        isLoadingSubmissionDetail.value = false;
    }
};

// Add score dialog state
const showAddScoreDialog = ref(false);
const creativityScore = ref('');
const technicalScore = ref('');
const requirementsScore = ref('');

const viewSubmission = async (submission) => {
    // Load full submission details including image
    const fullSubmission = await loadSubmissionDetail(submission.id);
    
    if (fullSubmission) {
        selectedSubmission.value = {
            ...fullSubmission,
            content: {
                title: fullSubmission.activityTitle || 'Submission',
                description: fullSubmission.caption || 'No description provided',
                image: fullSubmission.filePath,
                date: fullSubmission.date,
                status: fullSubmission.status
            },
            newRemark: '',
            rank: null
        };
        showSubmissionDialog.value = true;
    } else {
        alert('Failed to load submission details');
    }
};

const saveRemarks = () => {
    if (selectedSubmission.value) {
        // Ensure the student output exists
        if (!studentOutputs.value[selectedSubmission.value.id]) {
            studentOutputs.value[selectedSubmission.value.id] = {};
        }
        // Save the remarks
        studentOutputs.value[selectedSubmission.value.id].remarks = selectedSubmission.value.newRemark || '';

        // Show success message (you can replace this with a toast notification if available)
        console.log('Remarks saved successfully');

        // Optional: Close the dialog after saving
        // closeDialog();
    }
};

const addScore = () => {
    // Reset form values
    creativityScore.value = '';
    technicalScore.value = '';
    requirementsScore.value = '';
    
    // Show the add score dialog
    showAddScoreDialog.value = true;
};

const saveScore = async () => {
    if (selectedSubmission.value && creativityScore.value && technicalScore.value && requirementsScore.value) {
        try {
            const totalScore = calculateTotalScore();
            
            // Call the backend API to save the score
            const response = await axios.post(`/api/submissions/${selectedSubmission.value.id}/score/`, {
                scores: {
                    creativity: parseInt(creativityScore.value),
                    creativity_max: 10,
                    technical_skill: parseInt(technicalScore.value),
                    technical_skill_max: 10,
                    requirements: parseInt(requirementsScore.value),
                    requirements_max: 10
                },
                feedback: '', // You can add a feedback field later
                total_score: totalScore,
                max_score: 30
            });
            
            console.log('Score saved successfully:', response.data);
            
            // Update local state
            if (!studentOutputs.value[selectedSubmission.value.id]) {
                studentOutputs.value[selectedSubmission.value.id] = {};
            }
            
            studentOutputs.value[selectedSubmission.value.id].scores = {
                creativity: parseInt(creativityScore.value),
                technical: parseInt(technicalScore.value),
                requirements: parseInt(requirementsScore.value),
                total: totalScore
            };
            
            // Close the dialog
            closeAddScoreDialog();
            
            // Refresh both lists
            await loadUnscoredSubmissions();
            await loadScoredSubmissions();
            
            // Show success message
            alert('Score saved successfully!');
        } catch (error) {
            console.error('Error saving score:', error);
            alert('Failed to save score: ' + (error.response?.data?.error || error.message));
        }
    }
};

const calculateTotalScore = () => {
    const creativity = parseInt(creativityScore.value) || 0;
    const technical = parseInt(technicalScore.value) || 0;
    const requirements = parseInt(requirementsScore.value) || 0;
    return creativity + technical + requirements;
};

// Computed properties for filtering submissions
const unscoredSubmissions = computed(() => {
    return submissions.value.filter(submission => 
        !studentOutputs.value[submission.id]?.scores
    );
});

const scoredSubmissions = computed(() => {
    return scoredSubmissionsData.value;
});

const validateScoreInput = (value, type) => {
    const numValue = parseInt(value);
    if (numValue < 1) {
        if (type === 'creativity') creativityScore.value = '1';
        if (type === 'technical') technicalScore.value = '1';
        if (type === 'requirements') requirementsScore.value = '1';
    } else if (numValue > 10) {
        if (type === 'creativity') creativityScore.value = '10';
        if (type === 'technical') technicalScore.value = '10';
        if (type === 'requirements') requirementsScore.value = '10';
    }
};

const closeAddScoreDialog = () => {
    showAddScoreDialog.value = false;
    creativityScore.value = '';
    technicalScore.value = '';
    requirementsScore.value = '';
};

const closeDialog = () => {
    showSubmissionDialog.value = false;
    selectedSubmission.value = null;
};

// Medal animation states
const medalHovered = ref(null);

// Helper function to get medal details
const getMedalDetails = (rank) => {
    if (rank === 1) {
        return {
            color: '#FFD700',
            ribbonColor: '#FF0000',
            label: '1st',
            icon: 'pi-trophy'
        };
    } else if (rank === 2) {
        return {
            color: '#C0C0C0',
            ribbonColor: '#3366FF',
            label: '2nd',
            icon: 'pi-star-fill'
        };
    } else if (rank === 3) {
        return {
            color: '#CD7F32',
            ribbonColor: '#009900',
            label: '3rd',
            icon: 'pi-star'
        };
    }
    return {
        color: '#6366f1',
        ribbonColor: '#4338ca',
        label: rank + 'th',
        icon: 'pi-check'
    };
};

</script>

<style scoped>
.submission-dialog {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.submission-dialog :deep(.p-dialog-header) {
    display: none;
}

.submission-dialog :deep(.p-dialog-content) {
    padding: 0;
    border: none;
}

/* Add hover effect to student rows */
.divide-y > div {
    transition: all 0.2s ease;
}

.divide-y > div:hover {
    background-color: rgba(0, 0, 0, 0.02);
}

/* Add theme variables */
:root {
    --theme-purple: #4338ca;
    --theme-blue: #2563eb;
    --theme-light: #f9fafb;
    --theme-accent: #6366f1;
    --theme-dark: #111827;
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
    height: 35px;
    background: #FF6B6B;
    border-radius: 3px;
    top: 0;
    transform-origin: bottom center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.ribbon-left {
    left: 8px;
    transform: rotate(-30deg);
    background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
}

.ribbon-right {
    right: 8px;
    transform: rotate(30deg);
    background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
}

.ribbon-connector {
    position: absolute;
    width: 16px;
    height: 8px;
    background: #FF6B6B;
    top: 30px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 0 0 3px 3px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

.medal-star {
    position: relative;
    width: 100%;
    height: 100%;
    background: #FFD700;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
    z-index: 2;
    border: 2px solid rgba(255, 255, 255, 0.5);
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
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 24px;
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

/* Floating animation */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-5px); }
    100% { transform: translateY(0px); }
}

.floating {
    animation: float 3s ease-in-out infinite;
    filter: drop-shadow(0 5px 10px rgba(0, 0, 0, 0.3));
}

.medal-hover {
    animation: float 1.5s ease-in-out infinite, pulse 1.5s infinite;
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

.medal-hover {
    animation: pulse 1s infinite alternate;
}

@keyframes pulse {
    0% { transform: scale(1); }
    100% { transform: scale(1.1); }
}

.medal-score {
    position: absolute;
    bottom: -18px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.7);
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 0.65rem;
    font-weight: bold;
    color: white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    opacity: 1;
    transition: all 0.3s ease;
    z-index: 5;
    white-space: nowrap;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.medal-container:hover .medal-score {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
}

/* Rank badge in list view */
.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    font-weight: bold;
    margin-right: 8px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
    background: linear-gradient(135deg, #6366f1, #4338ca);
    color: white;
}
</style>

<template>
    <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-violet-50 to-blue-50">
<!-- Header -->
<div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 p-6 md:p-4 shadow-lg rounded-lg">
    <div class="flex flex-col gap-4">
        <div class="flex justify-between items-start">
            <h1 class="text-xl md:text-2xl font-bold text-white px-4 py-2 md:px-6 md:py-3 rounded-lg inline-block bg-white/20">
                {{ activity.title }}
            </h1>
            <button
                @click="goBack"
                class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
            >
                <i class="pi pi-arrow-left"></i>
                <span>Back to Activities</span>
            </button>
        </div>
        <div class="flex flex-col gap-2 ml-2">
            <p class="text-white/90 flex items-center gap-2">
                <i class="pi pi-align-left"></i>
                <span>Description: {{ activity.description }}</span>
            </p>
            <p class="text-white/90 flex items-center gap-2">
                <i class="pi pi-calendar"></i>
                <span>Due: {{ activity.date }}</span>
            </p>
        </div>
    </div>
</div>


        <div class="p-8 space-y-8">
            <!-- Show submissions list only when no submission is selected -->
            <div v-if="!selectedSubmission" class="space-y-8">
                <!-- Unscored Submissions Section -->
                <div class="bg-white rounded-3xl shadow-lg overflow-hidden border border-indigo-100">
                    <div class="px-6 py-4 border-b border-indigo-100 flex justify-between items-center">
                        <h2 class="text-xl font-semibold text-gray-900 flex items-center gap-2">
                            <i class="pi pi-clock text-orange-500"></i>
                            Unscored Submissions
                            <span class="text-sm font-normal text-gray-500">({{ unscoredSubmissions.length }})</span>
                        </h2>
                        <div class="flex items-center gap-2">
                            <div class="flex items-center rounded-xl bg-indigo-50 p-1 shadow-sm">
                                <!-- List View Button -->
                                <button @click="toggleView('list')"
                                        :class="[
                                            'p-2.5 rounded-xl transition-all duration-300 ease-in-out transform',
                                            viewMode === 'list'
                                                ? 'bg-indigo-600 text-white scale-105 shadow-md'
                                                : 'bg-indigo-50 text-gray-600 hover:bg-indigo-50/30'
                                        ]"
                                >
                                    <i class="pi pi-list text-lg"></i>
                                </button>
                                <!-- Card View Button -->
                                <button @click="toggleView('card')"
                                        :class="[
                                            'p-2.5 rounded-xl transition-all duration-300 ease-in-out transform',
                                            viewMode === 'card'
                                                ? 'bg-indigo-600 text-white scale-105 shadow-md'
                                                : 'bg-indigo-50 text-gray-600 hover:bg-indigo-50/30'
                                        ]"
                                >
                                    <i class="pi pi-th-large text-lg"></i>
                                </button>
                            </div>
                        </div>
                    </div>

                <!-- Loading State -->
                <div v-if="isLoadingSubmissions" class="flex justify-center items-center py-12">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                </div>

                <!-- Empty State -->
                <div v-else-if="unscoredSubmissions.length === 0" class="text-center py-12">
                    <i class="pi pi-inbox text-4xl text-gray-400 mb-4"></i>
                    <p class="text-gray-500">No unscored submissions yet.</p>
                </div>

                <!-- List View -->
                <template v-else-if="viewMode === 'list'">
                    <!-- Table Header -->
                    <div class="px-6 py-4 flex items-center text-sm font-medium text-gray-600 border-b border-indigo-100 bg-indigo-50">
                        <div class="w-1/3 flex items-center gap-2">
                            <i class="pi pi-user text-indigo-700"></i>
                            Name
                        </div>
                        <div class="w-1/4 flex items-center gap-2">
                            <i class="pi pi-id-card text-indigo-700"></i>
                            ID Number
                        </div>
                        <div class="w-1/4 flex items-center gap-2">
                            <i class="pi pi-check-circle text-indigo-700"></i>
                            Status
                        </div>
                        <div class="w-1/5 flex items-center gap-2 pl-4">
                            <i class="pi pi-calendar text-indigo-700 flex-shrink-0"></i>
                            <span class="whitespace-nowrap">Date Submitted</span>
                        </div>
                        <div class="w-1/6 flex items-center gap-2">
                            <i class="pi pi-star text-indigo-700"></i>
                            <span class="whitespace-nowrap">Score</span>
                        </div>
                        <div class="w-8"></div>
                    </div>

                    <!-- Table Content -->
                    <div class="divide-y divide-indigo-100/50">
                        <div v-for="submission in unscoredSubmissions" :key="submission.id"
                            class="px-6 py-4 flex items-center justify-between cursor-pointer transition-all duration-300 hover:bg-indigo-50 group"
                            @click="viewSubmission(submission)"
                        >
                            <div class="w-1/3 flex items-center gap-3">
                                <span class="w-9 h-9 rounded-xl flex items-center justify-center text-sm font-medium bg-indigo-50 text-gray-900 shadow-sm group-hover:shadow transition-shadow duration-300">
                                    {{ submission.name.charAt(0) }}
                                </span>
                                <span class="font-medium text-gray-900">{{ submission.name }}</span>
                                <div v-if="studentOutputs[submission.id]?.rank" class="ml-2">
                                    <span :class="['rank-badge', `rank-${studentOutputs[submission.id].rank}`]">
                                        {{ studentOutputs[submission.id].rank }}
                                    </span>
                                </div>
                            </div>
                            <div class="w-1/4 text-gray-600 font-medium">
                                {{ submission.id }}
                            </div>
                            <div class="w-1/4">
                                <span :class="[
                                    'px-4 py-2 text-sm font-medium rounded-xl shadow-sm transition-all duration-300',
                                    submission.status === 'Submitted' ? 'bg-green-100 text-green-800 group-hover:bg-green-200' :
                                    submission.status === 'Late' ? 'bg-yellow-100 text-yellow-800 group-hover:bg-yellow-200' :
                                    'bg-red-100 text-red-800 group-hover:bg-red-200'
                                ]">
                                    {{ submission.status }}
                                </span>
                            </div>
                            <div class="w-1/5 text-gray-600 font-medium pl-4">{{ submission.date }}</div>
                            <div class="w-1/6">
                                <span v-if="studentOutputs[submission.id]?.scores" class="px-3 py-1 text-sm font-medium rounded-full bg-indigo-100 text-indigo-800">
                                    {{ studentOutputs[submission.id].scores.total }}/30
                                </span>
                                <span v-else class="text-sm text-gray-400">-</span>
                            </div>
                            <div class="w-8">
                                <button class="p-2 rounded-lg text-gray-400 hover:text-indigo-700 hover:bg-indigo-50 transition-all duration-300">
                                    <i class="pi pi-ellipsis-v"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </template>

                <!-- Card View -->
                <template v-else>
                    <div class="p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-6 bg-white rounded-xl">
                        <div v-for="submission in unscoredSubmissions" :key="submission.id"
                            class="rounded-xl shadow-sm border overflow-hidden hover:shadow-lg transition-all transform hover:-translate-y-1 duration-200 cursor-pointer group"
                            style="background-color: #f9fafb; border-color: #e0e7ff;"
                            @click="viewSubmission(submission)"
                        >
                            <!-- Activity Output Preview with Gradient Overlay -->
                            <div class="relative h-64 overflow-hidden bg-white">
                                <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent z-10"></div>
                                <div class="w-full h-full flex items-center justify-center bg-white border-b-2 border-indigo-100 p-4">
                                    <div class="relative w-full h-full max-w-full max-h-full flex items-center justify-center">
                                        <img
                                            v-if="studentOutputs[submission.id]?.image"
                                            :src="studentOutputs[submission.id].image"
                                            :alt="studentOutputs[submission.id].title"
                                            class="max-w-full max-h-full object-contain transition-transform duration-300 group-hover:scale-105"
                                            style="max-height: 100%; max-width: 100%; object-fit: contain;"
                                        />
                                        <div v-else class="w-full h-full flex items-center justify-center"
                                             style="background: linear-gradient(to bottom right, #f9fafb, #e0e7ff);">
                                            <i class="pi pi-file text-4xl" style="color: #6366f1;"></i>
                                        </div>
                                    </div>
                                </div>

                                <!-- Status Badge -->
                                <div class="absolute top-3 left-3">
                                    <span :class="[
                                        'px-3 py-1.5 text-xs font-medium rounded-full shadow-sm',
                                        submission.status === 'Submitted' ? 'bg-green-400/90 text-white' :
                                        submission.status === 'Late' ? 'bg-yellow-400/90 text-white' :
                                        'bg-red-400/90 text-white'
                                    ]">
                                        {{ submission.status }}
                                    </span>
                                </div>
                            </div>

                            <!-- Submission Info -->
                            <div class="p-4 space-y-4" style="background-color: #f9fafb;">
                                <!-- Student Info with Avatar -->
                                <div class="flex items-center space-x-3">
                                    <div class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-lg shadow-sm font-medium"
                                         style="background-color: #e0e7ff; color: #111827;">
                                        {{ submission.name.charAt(0) }}
                                    </div>
                                    <div class="min-w-0">
                                        <p class="text-sm font-medium text-gray-900 truncate">{{ submission.name }}</p>
                                        <p class="text-xs text-gray-500 truncate">ID: {{ submission.id }}</p>
                                    </div>
                                </div>

                                <!-- Score Display -->
                                <div v-if="studentOutputs[submission.id]?.scores" class="flex items-center justify-between">
                                    <div class="flex items-center text-gray-500">
                                        <i class="pi pi-star mr-2" style="color: #6366f1;"></i>
                                        <span class="text-sm font-medium text-indigo-700">Score: {{ studentOutputs[submission.id].scores.total }}/30</span>
                                    </div>
                                </div>
                                
                                <!-- Submission Details with Icons -->
                                <div class="pt-3 border-t flex items-center justify-between text-sm"
                                     style="border-color: #e0e7ff;">
                                    <div class="flex items-center text-gray-500">
                                        <i class="pi pi-calendar mr-2" style="color: #6366f1;"></i>
                                        <span>{{ submission.date }}</span>
                                    </div>
                                    <button class="transition-colors hover:text-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-indigo-50">
                                        <i class="pi pi-eye"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
                </div>
                
                <!-- Scored Submissions Section -->
                <div class="bg-white rounded-3xl shadow-lg overflow-hidden border border-indigo-100">
                    <div class="px-6 py-4 border-b border-indigo-100 flex justify-between items-center">
                        <h2 class="text-xl font-semibold text-gray-900 flex items-center gap-2">
                            <i class="pi pi-check-circle text-green-500"></i>
                            Scored Submissions
                            <span class="text-sm font-normal text-gray-500">({{ scoredSubmissions.length }})</span>
                        </h2>
                    </div>

                    <!-- Empty State -->
                    <div v-if="scoredSubmissions.length === 0" class="text-center py-12">
                        <i class="pi pi-inbox text-4xl text-gray-400 mb-4"></i>
                        <p class="text-gray-500">No scored submissions yet.</p>
                    </div>

                    <!-- List View -->
                    <template v-else-if="viewMode === 'list'">
                        <!-- Table Header -->
                        <div class="px-6 py-4 flex items-center text-sm font-medium text-gray-600 border-b border-indigo-100 bg-indigo-50">
                            <div class="w-1/3 flex items-center gap-2">
                                <i class="pi pi-user text-indigo-700"></i>
                                Name
                            </div>
                            <div class="w-1/4 flex items-center gap-2">
                                <i class="pi pi-id-card text-indigo-700"></i>
                                ID Number
                            </div>
                            <div class="w-1/4 flex items-center gap-2">
                                <i class="pi pi-check-circle text-indigo-700"></i>
                                Status
                            </div>
                            <div class="w-1/5 flex items-center gap-2 pl-4">
                                <i class="pi pi-calendar text-indigo-700 flex-shrink-0"></i>
                                <span class="whitespace-nowrap">Date Submitted</span>
                            </div>
                            <div class="w-1/6 flex items-center gap-2">
                                <i class="pi pi-star text-indigo-700"></i>
                                <span class="whitespace-nowrap">Score</span>
                            </div>
                            <div class="w-8"></div>
                        </div>

                        <!-- Table Content -->
                        <div class="divide-y divide-indigo-100/50">
                            <div v-for="submission in scoredSubmissions" :key="submission.id"
                                class="px-6 py-4 flex items-center justify-between cursor-pointer transition-all duration-300 hover:bg-indigo-50 group"
                                @click="viewSubmission(submission)"
                            >
                                <div class="w-1/3 flex items-center gap-3">
                                    <span class="w-9 h-9 rounded-xl flex items-center justify-center text-sm font-medium bg-indigo-50 text-gray-900 shadow-sm group-hover:shadow transition-shadow duration-300">
                                        {{ submission.name.charAt(0) }}
                                    </span>
                                    <span class="font-medium text-gray-900">{{ submission.name }}</span>
                                    <div v-if="studentOutputs[submission.id]?.rank" class="ml-2">
                                        <span :class="['rank-badge', `rank-${studentOutputs[submission.id].rank}`]">
                                            {{ studentOutputs[submission.id].rank }}
                                        </span>
                                    </div>
                                </div>
                                <div class="w-1/4 text-gray-600 font-medium">
                                    {{ submission.id }}
                                </div>
                                <div class="w-1/4">
                                    <span :class="[
                                        'px-4 py-2 text-sm font-medium rounded-xl shadow-sm transition-all duration-300',
                                        submission.status === 'Submitted' ? 'bg-green-100 text-green-800 group-hover:bg-green-200' :
                                        submission.status === 'Late' ? 'bg-yellow-100 text-yellow-800 group-hover:bg-yellow-200' :
                                        'bg-red-100 text-red-800 group-hover:bg-red-200'
                                    ]">
                                        {{ submission.status }}
                                    </span>
                                </div>
                                <div class="w-1/5 text-gray-600 font-medium pl-4">{{ submission.date }}</div>
                                <div class="w-1/6">
                                    <span v-if="studentOutputs[submission.id]?.scores" class="px-3 py-1 text-sm font-medium rounded-full bg-indigo-100 text-indigo-800">
                                        {{ studentOutputs[submission.id].scores.total }}/30
                                    </span>
                                    <span v-else class="text-sm text-gray-400">-</span>
                                </div>
                                <div class="w-8">
                                    <button class="p-2 rounded-lg text-gray-400 hover:text-indigo-700 hover:bg-indigo-50 transition-all duration-300">
                                        <i class="pi pi-ellipsis-v"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </template>

                    <!-- Card View -->
                    <template v-else>
                        <div class="p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-6 bg-white rounded-xl">
                            <div v-for="submission in scoredSubmissions" :key="submission.id"
                                class="rounded-xl shadow-sm border overflow-hidden hover:shadow-lg transition-all transform hover:-translate-y-1 duration-200 cursor-pointer group"
                                style="background-color: #f9fafb; border-color: #e0e7ff;"
                                @click="viewSubmission(submission)"
                            >
                                <!-- Activity Output Preview with Gradient Overlay -->
                                <div class="relative h-64 overflow-hidden bg-white">
                                    <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent z-10"></div>
                                    <div class="w-full h-full flex items-center justify-center bg-white border-b-2 border-indigo-100 p-4">
                                        <div class="relative w-full h-full max-w-full max-h-full flex items-center justify-center">
                                            <img
                                                v-if="studentOutputs[submission.id]?.image"
                                                :src="studentOutputs[submission.id].image"
                                                :alt="studentOutputs[submission.id].title"
                                                class="max-w-full max-h-full object-contain transition-transform duration-300 group-hover:scale-105"
                                                style="max-height: 100%; max-width: 100%; object-fit: contain;"
                                            />
                                            <div v-else class="w-full h-full flex items-center justify-center"
                                                 style="background: linear-gradient(to bottom right, #f9fafb, #e0e7ff);">
                                                <i class="pi pi-file text-4xl" style="color: #6366f1;"></i>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Status Badge -->
                                    <div class="absolute top-3 left-3">
                                        <span :class="[
                                            'px-3 py-1.5 text-xs font-medium rounded-full shadow-sm',
                                            submission.status === 'Submitted' ? 'bg-green-400/90 text-white' :
                                            submission.status === 'Late' ? 'bg-yellow-400/90 text-white' :
                                            'bg-red-400/90 text-white'
                                        ]">
                                            {{ submission.status }}
                                        </span>
                                    </div>
                                </div>

                                <!-- Submission Info -->
                                <div class="p-4 space-y-4" style="background-color: #f9fafb;">
                                    <!-- Student Info with Avatar -->
                                    <div class="flex items-center space-x-3">
                                        <div class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-lg shadow-sm font-medium"
                                             style="background-color: #e0e7ff; color: #111827;">
                                            {{ submission.name.charAt(0) }}
                                        </div>
                                        <div class="min-w-0">
                                            <p class="text-sm font-medium text-gray-900 truncate">{{ submission.name }}</p>
                                            <p class="text-xs text-gray-500 truncate">ID: {{ submission.id }}</p>
                                        </div>
                                    </div>

                                    <!-- Score Display -->
                                    <div v-if="studentOutputs[submission.id]?.scores" class="flex items-center justify-between">
                                        <div class="flex items-center text-gray-500">
                                            <i class="pi pi-star mr-2" style="color: #6366f1;"></i>
                                            <span class="text-sm font-medium text-indigo-700">Score: {{ studentOutputs[submission.id].scores.total }}/30</span>
                                        </div>
                                    </div>
                                    
                                    <!-- Submission Details with Icons -->
                                    <div class="pt-3 border-t flex items-center justify-between text-sm"
                                         style="border-color: #e0e7ff;">
                                        <div class="flex items-center text-gray-500">
                                            <i class="pi pi-calendar mr-2" style="color: #6366f1;"></i>
                                            <span>{{ submission.date }}</span>
                                        </div>
                                        <button class="transition-colors hover:text-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-indigo-50">
                                            <i class="pi pi-eye"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
            </div>

            <!-- Show submission details when a submission is selected -->
            <div v-if="selectedSubmission" class="bg-white rounded-3xl shadow-lg overflow-hidden border border-indigo-100">
                <div class="px-6 py-4 border-b border-indigo-100 flex justify-between items-center">
                    <h2 class="text-xl font-semibold text-gray-900 flex items-center gap-2">
                        <i class="pi pi-user-edit text-indigo-700"></i>
                        Submission Details
                    </h2>
                    <button
                        @click="selectedSubmission = null"
                        class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200 shadow-md hover:shadow-lg"
                    >
                        <i class="pi pi-arrow-left"></i>
                        <span>Back to Submissions</span>
                    </button>
                </div>

                <div class="p-6">
                    <div class="flex justify-between items-center mb-6 relative">
                        <h3 class="text-2xl font-semibold text-gray-900 px-2">
                            {{ selectedSubmission.content?.title || 'Submission Details' }}
                        </h3>

                        <!-- Add Score Button -->
                        <button @click="addScore" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors duration-200">
                            <span>Add score</span>
                        </button>


                    </div>

                    <div class="space-y-6">
                        <!-- Top Row - Image and Student Info -->
                        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                            <!-- Image -->
                            <div class="lg:col-span-2">
                                <div class="bg-white rounded-xl overflow-hidden border-2 border-indigo-100" style="height: 400px;">
                                    <div class="w-full h-full flex items-center justify-center p-4 bg-white relative">
                                        <!-- Image -->
                                        <img v-if="selectedSubmission.content?.image"
                                            :src="selectedSubmission.content.image"
                                            :alt="selectedSubmission.content.title"
                                            class="max-h-full max-w-full object-contain"
                                            style="max-height: 100%; max-width: 100%; object-fit: contain;"
                                        />
                                        <!-- Medal Badge - Floating over image -->
                                        <div v-if="selectedSubmission.rank" class="absolute top-0 right-0 z-20 transform -translate-x-1/4 translate-y-1/4">
                                            <div :class="[
                                                'medal-container relative inline-block floating',
                                                selectedSubmission.rank === 1 ? 'medal-gold' :
                                                selectedSubmission.rank === 2 ? 'medal-silver' :
                                                'medal-bronze',
                                                { 'medal-hover': medalHovered === selectedSubmission.id }
                                            ]"
                                            style="width: 70px; height: 70px;"
                                            @mouseenter="medalHovered = selectedSubmission.id"
                                            @mouseleave="medalHovered = null">
                                                <!-- Medal Ribbon -->
                                                <div class="medal-ribbon" style="top: -12px;">
                                                    <div class="ribbon-left"></div>
                                                    <div class="ribbon-right"></div>
                                                    <div class="ribbon-connector"></div>
                                                </div>

                                                <!-- Medal Star -->
                                                <div class="medal-star">
                                                    <div class="medal-star-shape"></div>
                                                    <div class="medal-rays"></div>
                                                    <div class="medal-inner flex items-center justify-center" style="font-size: 1.75rem; font-weight: bold;">
                                                        {{ selectedSubmission.rank }}
                                                    </div>
                                                    <div class="medal-shine"></div>
                                                </div>
                                            </div>
                                        </div>
                                        <div v-else class="w-full h-full flex items-center justify-center"
                                            style="background: linear-gradient(to bottom right, #f9fafb, #e0e7ff);">
                                            <i class="pi pi-image text-5xl" style="color: #6366f1;"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Student Info -->
                            <div class="space-y-6">
                                <div class="bg-white p-5 rounded-xl border-2 border-indigo-100">
                                    <h4 class="text-md font-semibold text-gray-900 mb-4 flex items-center gap-2">
                                        <i class="pi pi-user" style="color: #6366f1;"></i>
                                        Student Information
                                    </h4>
                                    <div class="space-y-3">
                                        <div class="flex items-center gap-3">
                                            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-lg font-medium"
                                                style="background-color: #e0e7ff; color: #111827;">
                                                {{ selectedSubmission.name?.charAt(0) || 'U' }}
                                            </div>
                                            <div>
                                                <p class="font-medium text-gray-900">{{ selectedSubmission.name || 'Unknown Student' }}</p>
                                                <p class="text-sm text-gray-500">ID: {{ selectedSubmission.id || 'N/A' }}</p>
                                            </div>
                                        </div>
                                        <div class="pt-3 mt-3 border-t border-indigo-100 space-y-2">
                                            <div class="flex justify-between text-sm">
                                                <span class="text-gray-500">Status:</span>
                                                <span :class="[
                                                    'px-3 py-1 rounded-full text-xs font-medium',
                                                    selectedSubmission.status === 'Submitted' ? 'bg-green-100 text-green-800' :
                                                    selectedSubmission.status === 'Late' ? 'bg-yellow-100 text-yellow-800' :
                                                    'bg-red-100 text-red-800'
                                                ]">
                                                    {{ selectedSubmission.status || 'Unknown' }}
                                                </span>
                                            </div>
                                            <div class="flex justify-between text-sm">
                                                <span class="text-gray-500">Submitted:</span>
                                                <span class="font-medium">{{ selectedSubmission.date || 'N/A' }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Description -->
                                <div class="bg-white p-5 rounded-xl border-2 border-indigo-100">
                                    <h4 class="text-md font-semibold text-gray-900 mb-3 flex items-center gap-2">
                                        <i class="pi pi-align-left" style="color: #6366f1;"></i>
                                        Description
                                    </h4>
                                    <p class="text-gray-600 text-sm">
                                        {{ selectedSubmission.content?.description || 'No description provided.' }}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Teacher's Remarks -->
                        <div class="bg-white p-5 rounded-xl border-2 border-indigo-100">
                            <h4 class="text-md font-semibold text-gray-900 mb-3 flex items-center gap-2">
                                <i class="pi pi-comment" style="color: #6366f1;"></i>
                                Output Remarks
                            </h4>
                            <div class="space-y-3">
                                <!-- Display existing remarks if any -->
                                <div v-if="studentOutputs[selectedSubmission.id]?.remarks" class="mb-4 p-3 bg-gray-50 rounded-lg">
                                    <p class="text-sm text-gray-600">{{ studentOutputs[selectedSubmission.id].remarks }}</p>
                                </div>

                                <!-- Textarea for new/updated remarks -->
                                <Textarea v-model="selectedSubmission.newRemark"
                                        rows="4"
                                        class="w-full"
                                        placeholder="Add your remarks here..."
                                        :pt="{
                                            root: 'w-full rounded-xl border-indigo-100 focus:border-indigo-500 focus:ring-indigo-500',
                                        }"
                                />
                                <div class="flex justify-end gap-2">
                                    <button @click="closeDialog"
                                            class="px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                                        Cancel
                                    </button>
                                    <button @click="saveRemarks"
                                            class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors">
                                        {{ studentOutputs[selectedSubmission.id]?.remarks ? 'Update Remarks' : 'Save Remarks' }}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Add Score Dialog -->
    <Dialog v-model:visible="showAddScoreDialog" modal header="Add Score" :style="{ width: '450px' }">
        <div class="space-y-4">
            <!-- Student Info -->
            <div class="bg-indigo-50 p-3 rounded-lg">
                <p class="text-sm font-medium text-indigo-900">Student: {{ selectedSubmission?.name }}</p>
                <p class="text-sm text-indigo-700">Output: {{ selectedSubmission?.content?.title || 'Submission' }}</p>
            </div>
            
            <!-- Scoring Criteria -->
            <div>
                <h4 class="text-sm font-medium text-gray-700 mb-3">Scoring Criteria:</h4>
                <div class="space-y-3">
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div class="flex items-start gap-2">
                            <div class="w-2 h-2 bg-indigo-500 rounded-full mt-1.5"></div>
                            <p class="text-sm text-gray-600">Creativity and originality</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <input
                                v-model="creativityScore"
                                type="number"
                                min="1"
                                max="10"
                                @input="validateScoreInput(creativityScore, 'creativity')"
                                class="w-16 px-2 py-1 text-sm border border-indigo-100 rounded focus:outline-none focus:ring-1 focus:ring-indigo-500 text-center"
                                placeholder="0"
                            />
                            <span class="text-sm text-gray-500">/10</span>
                        </div>
                    </div>
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div class="flex items-start gap-2">
                            <div class="w-2 h-2 bg-indigo-500 rounded-full mt-1.5"></div>
                            <p class="text-sm text-gray-600">Technical skill and execution</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <input
                                v-model="technicalScore"
                                type="number"
                                min="1"
                                max="10"
                                @input="validateScoreInput(technicalScore, 'technical')"
                                class="w-16 px-2 py-1 text-sm border border-indigo-100 rounded focus:outline-none focus:ring-1 focus:ring-indigo-500 text-center"
                                placeholder="0"
                            />
                            <span class="text-sm text-gray-500">/10</span>
                        </div>
                    </div>
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div class="flex items-start gap-2">
                            <div class="w-2 h-2 bg-indigo-500 rounded-full mt-1.5"></div>
                            <p class="text-sm text-gray-600">Following assignment requirements</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <input
                                v-model="requirementsScore"
                                type="number"
                                min="1"
                                max="10"
                                @input="validateScoreInput(requirementsScore, 'requirements')"
                                class="w-16 px-2 py-1 text-sm border border-indigo-100 rounded focus:outline-none focus:ring-1 focus:ring-indigo-500 text-center"
                                placeholder="0"
                            />
                            <span class="text-sm text-gray-500">/10</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Total Score Display -->
            <div class="p-3 bg-indigo-50 rounded-lg">
                <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-indigo-900">Total Score:</span>
                    <span class="text-lg font-bold text-indigo-700">
                        {{ calculateTotalScore() }}/30
                    </span>
                </div>
            </div>
        </div>
        
        <template #footer>
            <button
                @click="closeAddScoreDialog"
                class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
            >
                Cancel
            </button>
            <button
                @click="saveScore"
                class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                :disabled="!creativityScore || !technicalScore || !requirementsScore"
                :class="{ 'opacity-50 cursor-not-allowed': !creativityScore || !technicalScore || !requirementsScore }"
            >
                Confirm
            </button>
        </template>
    </Dialog>
</template>
