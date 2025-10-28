<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import Dialog from 'primevue/dialog';
import Textarea from 'primevue/textarea';
import { useToast } from '../../composables/useToast';

// Initialize toast
const { showSuccess, showError, showInfo, showWarning } = useToast();

// Load activity from localStorage
const activity = ref({
    title: 'Student Activity',
    description: 'View student submissions for this activity',
    id: null
});

// Load activity data from API
const loadActivityFromAPI = async (activityId) => {
    try {
        console.log('🔄 Reloading activity from API:', activityId);
        const response = await axios.get(`/api/activities/${activityId}/`);
        console.log('📥 API Response:', response.data);
        
        // Parse scoring criteria if it's a string
        let scoringCriteria = [];
        if (response.data.scoring_criteria) {
            try {
                scoringCriteria = typeof response.data.scoring_criteria === 'string'
                    ? JSON.parse(response.data.scoring_criteria)
                    : response.data.scoring_criteria;
                console.log('✅ Parsed scoring criteria:', scoringCriteria);
            } catch (error) {
                console.error('❌ Error parsing scoring criteria:', error);
            }
        }
        
        // Update activity with fresh data from API
        activity.value = {
            ...activity.value,
            title: response.data.title,
            description: response.data.description,
            type: response.data.activity_type,
            dueDate: response.data.due_date,
            scoringCriteria: scoringCriteria
        };
        
        console.log('✅ Activity updated from API:', activity.value);
    } catch (error) {
        console.error('❌ Error loading activity from API:', error);
    }
};

// Function to handle class change event
const handleClassChange = (event) => {
    console.log('🔄 Class changed in Outputs, clearing view state and navigating...', event.detail);
    
    // Clear the teacher view state so Room shows folders view
    localStorage.removeItem('teacher_current_view');
    
    // Navigate back to TeacherRoom when class is changed
    emit('navigate', 'TeacherRoom');
};

// Load selected activity on component mount
onMounted(async () => {
    const savedActivity = localStorage.getItem('selected_activity');
    if (savedActivity) {
        const parsedActivity = JSON.parse(savedActivity);
        
        console.log('📦 Raw saved activity from localStorage:', parsedActivity);
        console.log('📊 Raw scoring criteria:', parsedActivity.scoringCriteria);
        console.log('📊 Type:', typeof parsedActivity.scoringCriteria);
        console.log('📊 Is Array:', Array.isArray(parsedActivity.scoringCriteria));
        
        activity.value = {
            title: parsedActivity.title,
            description: parsedActivity.description || 'View student submissions for this activity',
            id: parsedActivity.id,
            type: parsedActivity.type,
            dueDate: parsedActivity.dueDate,
            scoringCriteria: parsedActivity.scoringCriteria,
            subject: parsedActivity.subject  // Add subject field
        };
        console.log('✅ Loaded activity from localStorage:', activity.value);
        
        // Reload fresh data from API to get any updates
        if (parsedActivity.id) {
            await loadActivityFromAPI(parsedActivity.id);
        }
    }
    
    // Load submissions for this specific activity
    loadUnscoredSubmissions();
    loadScoredSubmissions();
    
    // Listen for class change events
    window.addEventListener('classChanged', handleClassChange);
});

onUnmounted(() => {
    // Clean up event listener
    window.removeEventListener('classChanged', handleClassChange);
});

// Define emits for navigation
const emit = defineEmits(['navigate']);

const goBack = () => {
    // Store the subject/folder context so Room.vue can show the activities list
    console.log('Going back with activity:', activity.value);
    if (activity.value.subject) {
        const returnData = {
            subject: activity.value.subject,
            showActivities: true,
            timestamp: Date.now()  // Add timestamp to expire after 5 seconds
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

// Student outputs data - scores and remarks stored here
const studentOutputs = ref({});

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
            
            submissions.value = filteredSubmissions.map(submission => {
                const submittedDate = new Date(submission.submitted_at);
                const dateStr = submittedDate.toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                });
                const timeStr = submittedDate.toLocaleTimeString('en-US', {
                    hour: 'numeric',
                    minute: '2-digit',
                    hour12: true
                });
                
                console.log('📊 Submission data:', {
                    id: submission.id,
                    has_file_path: !!submission.file_path,
                    file_path_length: submission.file_path?.length,
                    file_type: submission.file_type,
                    file_path_preview: submission.file_path?.substring(0, 100)
                });
                
                return {
                    id: submission.id,
                    studentId: submission.student.id,
                    name: submission.student.username,
                    activityTitle: submission.activity_title,
                    activityType: submission.activity_type,
                    caption: submission.caption,
                    score: submission.score,
                    status: submission.display_status || 'Submitted',  // Use display_status from backend
                    date: dateStr,
                    time: timeStr,
                    file_path: submission.file_url || submission.file_path,  // Use file_url first, fallback to file_path
                    file_type: submission.file_type,
                    submitted_at: submission.submitted_at,
                    is_late: submission.is_late || false,
                    resubmit_count: submission.resubmit_count || 0
                };
            });
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
            
            scoredSubmissionsData.value = filteredSubmissions.map(submission => {
                const submittedDate = new Date(submission.scored_at || submission.submitted_at);
                const dateStr = submittedDate.toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                });
                const timeStr = submittedDate.toLocaleTimeString('en-US', {
                    hour: 'numeric',
                    minute: '2-digit',
                    hour12: true
                });
                
                return {
                    id: submission.id,
                    studentId: submission.student.id,
                    name: submission.student.username,
                    activityTitle: submission.activity_title,
                    activityType: submission.activity_type,
                    caption: submission.caption,
                    score: submission.score,
                    status: submission.display_status || 'Scored',  // Use display_status from backend
                    date: dateStr,
                    time: timeStr,
                    file_path: submission.file_url || submission.file_path,  // Use file_url first, fallback to file_path
                    file_type: submission.file_type,
                    submitted_at: submission.submitted_at,
                    is_late: submission.is_late || false,
                    resubmit_count: submission.resubmit_count || 0
                };
            });
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
                submitted_at: response.data.submitted_at,  // Raw datetime for formatting
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
const criteriaScores = ref([]); // Dynamic scores based on activity criteria
const scoreFeedback = ref(''); // Feedback for the student

// Remarks section state
const showRemarksSection = ref(true); // Show by default
const isEditingRemarks = ref(false);

const viewSubmission = async (submission) => {
    console.log('🔍 Opening submission:', {
        id: submission.id,
        file_type: submission.file_type,
        has_file_path: !!submission.file_path,
        file_path_length: submission.file_path?.length
    });
    
    // Use the submission data directly (it already has file_path and file_type)
    selectedSubmission.value = {
        ...submission,
        newRemark: '',
        rank: null
    };
    
    showSubmissionDialog.value = true;
};

const editRemarks = () => {
    isEditingRemarks.value = true;
    // Pre-fill the textarea with existing remarks
    selectedSubmission.value.newRemark = studentOutputs.value[selectedSubmission.value.id]?.remarks || '';
};

const deleteRemarks = async () => {
    if (confirm('Are you sure you want to delete these remarks?')) {
        try {
            const submissionId = selectedSubmission.value.id;
            const remarkId = studentOutputs.value[submissionId]?.remarkId;
            
            if (remarkId) {
                await axios.delete(`/api/submissions/${submissionId}/remarks/${remarkId}/`);
                console.log('Remark deleted successfully');
            }
            
            // Update local state
            if (studentOutputs.value[submissionId]) {
                studentOutputs.value[submissionId].remarks = '';
                studentOutputs.value[submissionId].remarkId = null;
            }
            selectedSubmission.value.newRemark = '';
            isEditingRemarks.value = false;
            
            showSuccess('Remark deleted successfully!', 'Deleted');
        } catch (error) {
            console.error('Error deleting remark:', error);
            showError(error.response?.data?.error || error.message, 'Delete Failed');
        }
    }
};

const cancelEditRemarks = () => {
    isEditingRemarks.value = false;
    selectedSubmission.value.newRemark = '';
};

const saveRemarks = async () => {
    if (selectedSubmission.value && selectedSubmission.value.newRemark.trim()) {
        try {
            const submissionId = selectedSubmission.value.id;
            const remarkText = selectedSubmission.value.newRemark.trim();
            
            if (isEditingRemarks.value && studentOutputs.value[submissionId]?.remarkId) {
                // Update existing remark
                const response = await axios.put(
                    `/api/submissions/${submissionId}/remarks/${studentOutputs.value[submissionId].remarkId}/`,
                    { text: remarkText }
                );
                console.log('Remark updated successfully:', response.data);
            } else {
                // Create new remark
                const response = await axios.post(
                    `/api/submissions/${submissionId}/remarks/`,
                    { text: remarkText }
                );
                console.log('Remark created successfully:', response.data);
                
                // Store the remark ID for future updates
                if (!studentOutputs.value[submissionId]) {
                    studentOutputs.value[submissionId] = {};
                }
                studentOutputs.value[submissionId].remarkId = response.data.id;
            }
            
            // Update local state
            if (!studentOutputs.value[submissionId]) {
                studentOutputs.value[submissionId] = {};
            }
            studentOutputs.value[submissionId].remarks = remarkText;
            
            // Reset editing state
            isEditingRemarks.value = false;
            selectedSubmission.value.newRemark = '';
            
            showSuccess('Remark saved successfully!', 'Saved');
        } catch (error) {
            console.error('Error saving remark:', error);
            showError(error.response?.data?.error || error.message, 'Save Failed');
        }
    }
};

const addScore = () => {
    // Reset form values
    creativityScore.value = '';
    technicalScore.value = '';
    requirementsScore.value = '';
    scoreFeedback.value = '';
    
    // Initialize criteria scores from activity
    console.log('Full activity object:', activity.value);
    console.log('Activity scoring criteria:', activity.value.scoringCriteria);
    console.log('Type of scoring criteria:', typeof activity.value.scoringCriteria);
    
    if (activity.value.scoringCriteria && activity.value.scoringCriteria.length > 0) {
        criteriaScores.value = activity.value.scoringCriteria.map(criterion => ({
            name: criterion.name,
            maxScore: criterion.maxScore,
            score: ''
        }));
        console.log('✅ Initialized criteria scores:', criteriaScores.value);
    } else {
        // Fallback to default criteria if none exist
        criteriaScores.value = [];
        console.log('❌ No scoring criteria found - using empty array');
    }
    
    // Show the add score dialog
    showAddScoreDialog.value = true;
};

// Validate criterion score doesn't exceed max
const validateCriterionScore = (criterion) => {
    if (criterion.score > criterion.maxScore) {
        criterion.score = criterion.maxScore;
    }
    if (criterion.score < 0) {
        criterion.score = 0;
    }
};

const saveScore = async () => {
    // Validate that all criteria have scores
    const allScoresEntered = criteriaScores.value.every(criterion => 
        criterion.score !== '' && criterion.score !== null && criterion.score !== undefined
    );
    
    if (!selectedSubmission.value || !allScoresEntered) {
        showWarning('Please enter scores for all criteria', 'Incomplete Scores');
        return;
    }
    
    try {
        const totalScore = calculateDynamicTotalScore();
        const maxScore = calculateMaxTotalScore();
        
        // Build scores object from criteria
        const scoresData = {};
        criteriaScores.value.forEach((criterion, index) => {
            scoresData[`criterion_${index}`] = {
                name: criterion.name,
                score: parseInt(criterion.score),
                maxScore: parseInt(criterion.maxScore)
            };
        });
        
        // Call the backend API to save the score
        const response = await axios.post(`/api/submissions/${selectedSubmission.value.id}/score/`, {
            score: totalScore,
            feedback: scoreFeedback.value.trim() || '',
            criteria_scores: JSON.stringify(criteriaScores.value.map(c => ({
                name: c.name,
                score: parseInt(c.score),
                maxScore: parseInt(c.maxScore)
            })))
        });
        
        console.log('✅ Score saved successfully:', response.data);
        
        // Small delay to ensure database is updated
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // Refresh both lists to move submission from unscored to scored
        console.log('🔄 Reloading submissions...');
        await Promise.all([
            loadUnscoredSubmissions(),
            loadScoredSubmissions()
        ]);
        console.log('✅ Submissions reloaded');
        console.log('📊 Unscored count:', submissions.value.length);
        console.log('📊 Scored count:', scoredSubmissionsData.value.length);
        
        // Show success message
        showSuccess('Score saved successfully!', 'Scored');
        
        // Close both dialogs AFTER everything is done
        closeAddScoreDialog();
        closeDialog();
    } catch (error) {
        console.error('Error saving score:', error);
        showError(error.response?.data?.error || error.message, 'Save Failed');
    }
};

const calculateTotalScore = () => {
    const creativity = parseInt(creativityScore.value) || 0;
    const technical = parseInt(technicalScore.value) || 0;
    const requirements = parseInt(requirementsScore.value) || 0;
    return creativity + technical + requirements;
};

// Calculate total score from dynamic criteria
const calculateDynamicTotalScore = () => {
    return criteriaScores.value.reduce((total, criterion) => {
        return total + (parseInt(criterion.score) || 0);
    }, 0);
};

// Calculate maximum possible score
const calculateMaxTotalScore = () => {
    return criteriaScores.value.reduce((total, criterion) => {
        return total + (parseInt(criterion.maxScore) || 0);
    }, 0);
};

// Computed properties for filtering submissions
const unscoredSubmissions = computed(() => {
    // Backend already filters by status='unscored', so just return the submissions
    // No need to filter again on frontend
    return submissions.value;
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
    criteriaScores.value = [];
    scoreFeedback.value = '';
};

const closeDialog = () => {
    showSubmissionDialog.value = false;
    selectedSubmission.value = null;
};

// Format submission date
const formatSubmissionDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    } catch (error) {
        return 'Invalid Date';
    }
};

// Format submission time
const formatSubmissionTime = (dateString) => {
    if (!dateString) return '';
    try {
        const date = new Date(dateString);
        return date.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true
        });
    } catch (error) {
        return '';
    }
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
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    <!-- Section Header -->
                    <div class="bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700 px-6 py-4 border-b border-indigo-300">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                                    <i class="pi pi-clock text-white text-lg"></i>
                                </div>
                                <div>
                                    <h3 class="text-lg font-bold text-white">Unscored Submissions</h3>
                                    <p class="text-sm text-white/80">Pending review and scoring</p>
                                </div>
                            </div>
                            <div class="flex items-center gap-3">
                                <span class="px-3 py-1 bg-white/20 text-white text-sm font-medium rounded-full">
                                    {{ unscoredSubmissions.length }} Submission{{ unscoredSubmissions.length !== 1 ? 's' : '' }}
                                </span>
                                <div class="flex items-center rounded-lg bg-white/20 p-1">
                                    <!-- List View Button -->
                                    <button @click="toggleView('list')"
                                            :class="[
                                                'p-2 rounded-lg transition-all duration-200',
                                                viewMode === 'list'
                                                    ? 'bg-white text-indigo-600'
                                                    : 'text-white/80 hover:text-white'
                                            ]"
                                    >
                                        <i class="pi pi-list text-base"></i>
                                    </button>
                                    <!-- Card View Button -->
                                    <button @click="toggleView('card')"
                                            :class="[
                                                'p-2 rounded-lg transition-all duration-200',
                                                viewMode === 'card'
                                                    ? 'bg-white text-indigo-600'
                                                    : 'text-white/80 hover:text-white'
                                            ]"
                                    >
                                        <i class="pi pi-th-large text-base"></i>
                                    </button>
                                </div>
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
                    <div class="bg-gray-50 border-b border-gray-200">
                        <div class="grid grid-cols-12 gap-3 px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider">
                            <div class="col-span-3">
                                <span>Name</span>
                            </div>
                            <div class="col-span-2">
                                <span>ID Number</span>
                            </div>
                            <div class="col-span-2">
                                <span>Status</span>
                            </div>
                            <div class="col-span-3">
                                <span>Date & Time</span>
                            </div>
                            <div class="col-span-2 text-center">
                                <span>Score</span>
                            </div>
                        </div>
                    </div>

                    <!-- Table Body -->
                    <div class="divide-y divide-gray-200">
                        <div v-for="submission in unscoredSubmissions" :key="submission.id"
                            class="group hover:bg-gray-50 transition-colors duration-150 cursor-pointer"
                            @click="viewSubmission(submission)"
                        >
                            <div class="grid grid-cols-12 gap-3 px-6 py-4 items-center">
                                <!-- Name -->
                                <div class="col-span-3 flex items-center gap-3">
                                    <div class="w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center">
                                        <span class="text-sm font-bold text-indigo-600">
                                            {{ submission.name.charAt(0).toUpperCase() }}
                                        </span>
                                    </div>
                                    <div>
                                        <div class="font-medium text-gray-900">{{ submission.name }}</div>
                                        <div v-if="studentOutputs[submission.id]?.rank" class="mt-1">
                                            <span :class="['rank-badge', `rank-${studentOutputs[submission.id].rank}`]">
                                                {{ studentOutputs[submission.id].rank }}
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                <!-- ID Number -->
                                <div class="col-span-2">
                                    <span class="text-sm text-gray-700">{{ submission.studentId }}</span>
                                </div>

                                <!-- Status -->
                                <div class="col-span-2">
                                    <span 
                                        v-if="submission.is_late"
                                        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-orange-100 text-orange-800 text-xs font-medium"
                                    >
                                        <i class="pi pi-clock text-xs"></i>
                                        <span>Submitted late</span>
                                    </span>
                                    <span 
                                        v-else-if="submission.status === 'Resubmitted'"
                                        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-blue-100 text-blue-800 text-xs font-medium"
                                    >
                                        <i class="pi pi-refresh text-xs"></i>
                                        <span>{{ submission.status }}</span>
                                        <span v-if="submission.resubmit_count > 0" class="text-xs">({{ submission.resubmit_count }}x)</span>
                                    </span>
                                    <span 
                                        v-else
                                        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-green-100 text-green-800 text-xs font-medium"
                                    >
                                        <i class="pi pi-check-circle text-xs"></i>
                                        <span>{{ submission.status || 'Submitted' }}</span>
                                    </span>
                                </div>

                                <!-- Date & Time -->
                                <div class="col-span-3">
                                    <div class="text-sm text-gray-700">{{ submission.date }}</div>
                                    <div class="text-xs text-gray-500 mt-0.5">{{ submission.time }}</div>
                                </div>

                                <!-- Score -->
                                <div class="col-span-2 text-center">
                                    <span class="text-sm text-gray-400">-</span>
                                </div>
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
                                        <!-- Image Display -->
                                        <img v-if="submission.file_type === 'image' && submission.file_path && submission.file_path.length > 0"
                                            :src="submission.file_path.startsWith('http') || submission.file_path.startsWith('/media') || submission.file_path.startsWith('data:') ? submission.file_path : `data:image/png;base64,${submission.file_path}`"
                                            :alt="submission.caption || 'Student submission'"
                                            class="max-w-full max-h-full object-contain transition-transform duration-300 group-hover:scale-105"
                                            style="max-height: 100%; max-width: 100%; object-fit: contain;"
                                        />
                                        <!-- PDF Display -->
                                        <div v-else-if="submission.file_type === 'pdf' && submission.file_path" class="flex flex-col items-center justify-center text-red-600">
                                            <i class="pi pi-file-pdf text-6xl mb-3"></i>
                                            <span class="text-sm font-medium">PDF Document</span>
                                            <span class="text-xs text-gray-500 mt-1">{{ submission.caption || 'Untitled' }}</span>
                                        </div>
                                        <!-- Word Document Display -->
                                        <div v-else-if="submission.file_type === 'document' && submission.file_path" class="flex flex-col items-center justify-center text-blue-600">
                                            <i class="pi pi-file-word text-6xl mb-3"></i>
                                            <span class="text-sm font-medium">Word Document</span>
                                            <span class="text-xs text-gray-500 mt-1">{{ submission.caption || 'Untitled' }}</span>
                                        </div>
                                        <!-- No file data - minimal message -->
                                        <div v-else class="flex flex-col items-center justify-center text-gray-400 px-4 text-center">
                                            <p class="text-sm">{{ submission.caption || 'No file data available' }}</p>
                                            <p class="text-xs mt-2 text-gray-300">Student needs to resubmit</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Status Badge -->
                                <div class="absolute top-3 left-3">
                                    <span :class="[
                                        'px-3 py-1.5 text-xs font-medium rounded-full shadow-sm',
                                        submission.status === 'Submitted' ? 'bg-green-400/90 text-white' :
                                        submission.status === 'Resubmitted' ? 'bg-blue-400/90 text-white' :
                                        submission.status === 'Late' ? 'bg-yellow-400/90 text-white' :
                                        submission.status === 'Scored' ? 'bg-purple-400/90 text-white' :
                                        'bg-red-400/90 text-white'
                                    ]">
                                        {{ submission.status }}
                                        <span v-if="submission.resubmit_count > 0" class="ml-1">({{ submission.resubmit_count }})</span>
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
                                    <div class="min-w-0 flex-1">
                                        <div class="flex items-center gap-2">
                                            <p class="text-sm font-medium text-gray-900 truncate">{{ submission.name }}</p>
                                            <span v-if="submission.is_late" class="text-xs px-2 py-0.5 rounded bg-orange-100 text-orange-800 font-medium flex-shrink-0">
                                                Late Submitted
                                            </span>
                                        </div>
                                        <p class="text-xs text-gray-500 truncate">ID: {{ submission.studentId }}</p>
                                    </div>
                                </div>

                                <!-- Submission Details with Icons -->
                                <div class="pt-3 border-t flex items-center justify-between text-sm"
                                     style="border-color: #e0e7ff;">
                                    <div class="flex items-center text-gray-500">
                                        <i class="pi pi-calendar mr-2" style="color: #6366f1;"></i>
                                        <div>
                                            <div>{{ submission.date }}</div>
                                            <div class="text-xs text-gray-400 mt-0.5">{{ submission.time }}</div>
                                        </div>
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
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    <!-- Section Header -->
                    <div class="bg-gradient-to-r from-green-600 to-green-500 px-6 py-4 border-b border-green-300">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                                    <i class="pi pi-check-circle text-white text-lg"></i>
                                </div>
                                <div>
                                    <h3 class="text-lg font-bold text-white">Scored Submissions</h3>
                                    <p class="text-sm text-white/80">Completed and graded work</p>
                                </div>
                            </div>
                            <span class="px-3 py-1 bg-white/20 text-white text-sm font-medium rounded-full">
                                {{ scoredSubmissions.length }} Submission{{ scoredSubmissions.length !== 1 ? 's' : '' }}
                            </span>
                        </div>
                    </div>

                    <!-- Empty State -->
                    <div v-if="scoredSubmissions.length === 0" class="text-center py-12">
                        <i class="pi pi-inbox text-4xl text-gray-400 mb-4"></i>
                        <p class="text-gray-500">No scored submissions yet.</p>
                    </div>

                    <!-- List View -->
                    <template v-else-if="viewMode === 'list'">
                        <!-- Table Header -->
                        <div class="bg-gray-50 border-b border-gray-200">
                            <div class="grid grid-cols-12 gap-3 px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                <div class="col-span-3">
                                    <span>Name</span>
                                </div>
                                <div class="col-span-2">
                                    <span>ID Number</span>
                                </div>
                                <div class="col-span-2">
                                    <span>Status</span>
                                </div>
                                <div class="col-span-3">
                                    <span>Date & Time</span>
                                </div>
                                <div class="col-span-2 text-center">
                                    <span>Score</span>
                                </div>
                            </div>
                        </div>

                        <!-- Table Body -->
                        <div class="divide-y divide-gray-200">
                            <div v-for="submission in scoredSubmissions" :key="submission.id"
                                class="group hover:bg-gray-50 transition-colors duration-150 cursor-pointer"
                                @click="viewSubmission(submission)"
                            >
                                <div class="grid grid-cols-12 gap-3 px-6 py-4 items-center">
                                    <!-- Name -->
                                    <div class="col-span-3 flex items-center gap-3">
                                        <div class="w-8 h-8 rounded-lg bg-green-100 flex items-center justify-center">
                                            <span class="text-sm font-bold text-green-600">
                                                {{ submission.name.charAt(0).toUpperCase() }}
                                            </span>
                                        </div>
                                        <div>
                                            <div class="font-medium text-gray-900">{{ submission.name }}</div>
                                            <div v-if="studentOutputs[submission.id]?.rank" class="mt-1">
                                                <span :class="['rank-badge', `rank-${studentOutputs[submission.id].rank}`]">
                                                    {{ studentOutputs[submission.id].rank }}
                                                </span>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- ID Number -->
                                    <div class="col-span-2">
                                        <span class="text-sm text-gray-700">{{ submission.studentId }}</span>
                                    </div>

                                    <!-- Status -->
                                    <div class="col-span-2">
                                        <span 
                                            v-if="submission.is_late"
                                            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-orange-100 text-orange-800 text-xs font-medium"
                                        >
                                            <i class="pi pi-clock text-xs"></i>
                                            <span>Submitted late</span>
                                        </span>
                                        <span 
                                            v-else-if="submission.status === 'Resubmitted'"
                                            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-blue-100 text-blue-800 text-xs font-medium"
                                        >
                                            <i class="pi pi-refresh text-xs"></i>
                                            <span>{{ submission.status }}</span>
                                            <span v-if="submission.resubmit_count > 0" class="text-xs">({{ submission.resubmit_count }}x)</span>
                                        </span>
                                        <span 
                                            v-else
                                            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-green-100 text-green-800 text-xs font-medium"
                                        >
                                            <i class="pi pi-check-circle text-xs"></i>
                                            <span>{{ submission.status || 'Submitted' }}</span>
                                        </span>
                                    </div>

                                    <!-- Date & Time -->
                                    <div class="col-span-3">
                                        <div class="text-sm text-gray-700">{{ submission.date }}</div>
                                        <div class="text-xs text-gray-500 mt-0.5">{{ submission.time }}</div>
                                    </div>

                                    <!-- Score -->
                                    <div class="col-span-2 text-center">
                                        <span v-if="submission.score !== null && submission.score !== undefined" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-green-100 text-green-800 text-sm font-bold">
                                            <i class="pi pi-star-fill text-xs"></i>
                                            {{ submission.score }}
                                        </span>
                                        <span v-else class="text-sm text-gray-400">-</span>
                                    </div>
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
                                            <!-- Image Display -->
                                            <img v-if="submission.file_type === 'image' && submission.file_path && submission.file_path.length > 0"
                                                :src="submission.file_path.startsWith('http') || submission.file_path.startsWith('/media') || submission.file_path.startsWith('data:') ? submission.file_path : `data:image/png;base64,${submission.file_path}`"
                                                :alt="submission.caption || 'Student submission'"
                                                class="max-w-full max-h-full object-contain transition-transform duration-300 group-hover:scale-105"
                                                style="max-height: 100%; max-width: 100%; object-fit: contain;"
                                            />
                                            <!-- PDF Display -->
                                            <div v-else-if="submission.file_type === 'pdf' && submission.file_path" class="flex flex-col items-center justify-center text-red-600">
                                                <i class="pi pi-file-pdf text-6xl mb-3"></i>
                                                <span class="text-sm font-medium">PDF Document</span>
                                                <span class="text-xs text-gray-500 mt-1">{{ submission.caption || 'Untitled' }}</span>
                                            </div>
                                            <!-- Word Document Display -->
                                            <div v-else-if="submission.file_type === 'document' && submission.file_path" class="flex flex-col items-center justify-center text-blue-600">
                                                <i class="pi pi-file-word text-6xl mb-3"></i>
                                                <span class="text-sm font-medium">Word Document</span>
                                                <span class="text-xs text-gray-500 mt-1">{{ submission.caption || 'Untitled' }}</span>
                                            </div>
                                            <!-- No file data - minimal message -->
                                            <div v-else class="flex flex-col items-center justify-center text-gray-400 px-4 text-center">
                                                <p class="text-sm">{{ submission.caption || 'No file data available' }}</p>
                                                <p class="text-xs mt-2 text-gray-300">Student needs to resubmit</p>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Status Badge -->
                                    <div class="absolute top-3 left-3">
                                        <span 
                                            v-if="submission.is_late"
                                            class="px-3 py-1.5 text-xs font-medium rounded-full shadow-sm bg-orange-400/90 text-white flex items-center gap-1.5"
                                        >
                                            <i class="pi pi-clock text-xs"></i>
                                            <span>Submitted late</span>
                                        </span>
                                        <span 
                                            v-else-if="submission.status === 'Resubmitted'"
                                            class="px-3 py-1.5 text-xs font-medium rounded-full shadow-sm bg-blue-400/90 text-white flex items-center gap-1.5"
                                        >
                                            <i class="pi pi-refresh text-xs"></i>
                                            <span>{{ submission.status }}</span>
                                            <span v-if="submission.resubmit_count > 0" class="text-xs">({{ submission.resubmit_count }})</span>
                                        </span>
                                        <span 
                                            v-else
                                            class="px-3 py-1.5 text-xs font-medium rounded-full shadow-sm bg-green-400/90 text-white flex items-center gap-1.5"
                                        >
                                            <i class="pi pi-check-circle text-xs"></i>
                                            <span>{{ submission.status || 'Submitted' }}</span>
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
                                        <div class="min-w-0 flex-1">
                                            <div class="flex items-center gap-2">
                                                <p class="text-sm font-medium text-gray-900 truncate">{{ submission.name }}</p>
                                            </div>
                                            <p class="text-xs text-gray-500 truncate">ID: {{ submission.studentId }}</p>
                                        </div>
                                    </div>

                                    <!-- Score Display -->
                                    <div v-if="submission.score !== null && submission.score !== undefined" class="flex items-center justify-between">
                                        <div class="flex items-center text-gray-500">
                                            <i class="pi pi-star mr-2" style="color: #6366f1;"></i>
                                            <span class="text-sm font-medium text-indigo-700">Score: {{ submission.score }}</span>
                                        </div>
                                    </div>
                                    
                                    <!-- Submission Details with Icons -->
                                    <div class="pt-3 border-t flex items-center justify-between text-sm"
                                         style="border-color: #e0e7ff;">
                                        <div class="flex items-center text-gray-500">
                                            <i class="pi pi-calendar mr-2" style="color: #6366f1;"></i>
                                            <div>
                                                <div>{{ submission.date }}</div>
                                                <div class="text-xs text-gray-400 mt-0.5">{{ submission.time }}</div>
                                            </div>
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
                            {{ selectedSubmission.caption || selectedSubmission.activityTitle || 'Submission Details' }}
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
                                        <!-- Image Display -->
                                        <img v-if="selectedSubmission.file_type === 'image' && selectedSubmission.file_path && selectedSubmission.file_path.length > 0"
                                            :src="selectedSubmission.file_path.startsWith('http') || selectedSubmission.file_path.startsWith('/media') || selectedSubmission.file_path.startsWith('data:') ? selectedSubmission.file_path : `data:image/png;base64,${selectedSubmission.file_path}`"
                                            :alt="selectedSubmission.caption || 'Student submission'"
                                            class="max-h-full max-w-full object-contain"
                                            style="max-height: 100%; max-width: 100%; object-fit: contain;"
                                        />
                                        <!-- PDF Display -->
                                        <div v-else-if="selectedSubmission.file_type === 'pdf' && selectedSubmission.file_path" class="flex flex-col items-center justify-center text-red-600">
                                            <i class="pi pi-file-pdf text-8xl mb-4"></i>
                                            <span class="text-lg font-medium">PDF Document</span>
                                            <span class="text-sm text-gray-500 mt-2">{{ selectedSubmission.caption || 'Untitled' }}</span>
                                        </div>
                                        <!-- Word Document Display -->
                                        <div v-else-if="selectedSubmission.file_type === 'document' && selectedSubmission.file_path" class="flex flex-col items-center justify-center text-blue-600">
                                            <i class="pi pi-file-word text-8xl mb-4"></i>
                                            <span class="text-lg font-medium">Word Document</span>
                                            <span class="text-sm text-gray-500 mt-2">{{ selectedSubmission.caption || 'Untitled' }}</span>
                                        </div>
                                        <!-- No file data - minimal text only -->
                                        <div v-else class="flex flex-col items-center justify-center text-gray-400 px-6 text-center">
                                            <p class="text-base text-gray-600 mb-2">{{ selectedSubmission.caption || 'No file data available' }}</p>
                                            <p class="text-sm text-gray-400">Student needs to resubmit their work</p>
                                        </div>
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
                                                <p class="text-sm text-gray-500">ID: {{ selectedSubmission.studentId || 'N/A' }}</p>
                                            </div>
                                        </div>
                                        <div class="pt-3 mt-3 border-t border-indigo-100 space-y-2">
                                            <div class="flex justify-between text-sm">
                                                <span class="text-gray-500">Status:</span>
                                                <span :class="[
                                                    'px-3 py-1 rounded-full text-xs font-medium inline-flex items-center gap-1.5',
                                                    selectedSubmission.is_late ? 'bg-orange-100 text-orange-800' :
                                                    selectedSubmission.status === 'Resubmitted' ? 'bg-blue-100 text-blue-800' :
                                                    selectedSubmission.status === 'Submitted' || selectedSubmission.status === 'Scored' ? 'bg-green-100 text-green-800' :
                                                    selectedSubmission.status === 'Late' ? 'bg-yellow-100 text-yellow-800' :
                                                    'bg-red-100 text-red-800'
                                                ]">
                                                    <i v-if="selectedSubmission.status === 'Resubmitted'" class="pi pi-refresh text-xs"></i>
                                                    <i v-else-if="selectedSubmission.is_late" class="pi pi-clock text-xs"></i>
                                                    <i v-else class="pi pi-check-circle text-xs"></i>
                                                    <span>{{ selectedSubmission.is_late ? 'Late Submitted' : (selectedSubmission.status || 'Unknown') }}</span>
                                                    <span v-if="selectedSubmission.resubmit_count > 0" class="text-xs">({{ selectedSubmission.resubmit_count }}x)</span>
                                                </span>
                                            </div>
                                            <div class="flex justify-between text-sm">
                                                <span class="text-gray-500">Submitted:</span>
                                                <div class="text-right">
                                                    <div class="font-medium">{{ formatSubmissionDate(selectedSubmission.submitted_at) }}</div>
                                                    <div class="text-xs text-gray-400">{{ formatSubmissionTime(selectedSubmission.submitted_at) }}</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Activity Details -->
                                <div class="bg-white p-5 rounded-xl border-2 border-indigo-100">
                                    <div class="space-y-3">
                                        <div>
                                            <p class="text-xs font-bold text-gray-700 uppercase tracking-wide mb-1">Activity Type:</p>
                                            <p class="text-gray-900 text-sm capitalize">{{ selectedSubmission.activityType || 'N/A' }}</p>
                                        </div>
                                        <div>
                                            <p class="text-xs font-bold text-gray-700 uppercase tracking-wide mb-1">Activity Title:</p>
                                            <p class="text-gray-900 text-sm">{{ selectedSubmission.activityTitle || 'N/A' }}</p>
                                        </div>
                                        <div>
                                            <p class="text-xs font-bold text-gray-700 uppercase tracking-wide mb-1">Description:</p>
                                            <p class="text-gray-900 text-sm">
                                                {{ selectedSubmission.caption || 'No description provided.' }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Teacher's Remarks (Optional/Collapsible) -->
                        <div class="bg-white p-5 rounded-xl border-2 border-indigo-100">
                            <div class="flex items-center justify-between mb-3">
                                <h4 class="text-md font-semibold text-gray-900 flex items-center gap-2">
                                    <i class="pi pi-comment" style="color: #6366f1;"></i>
                                    Output Remarks
                                    <span class="text-xs text-gray-400 font-normal">(Optional)</span>
                                </h4>
                                <button @click="showRemarksSection = !showRemarksSection" 
                                        class="text-indigo-600 hover:text-indigo-700">
                                    <i :class="showRemarksSection ? 'pi pi-chevron-up' : 'pi pi-chevron-down'"></i>
                                </button>
                            </div>
                            
                            <div v-show="showRemarksSection" class="space-y-3">
                                <!-- Display existing remarks with Edit/Delete buttons -->
                                <div v-if="studentOutputs[selectedSubmission.id]?.remarks && !isEditingRemarks" class="mb-4 p-3 bg-gray-50 rounded-lg">
                                    <p class="text-sm text-gray-600 mb-3">{{ studentOutputs[selectedSubmission.id].remarks }}</p>
                                    <div class="flex gap-2">
                                        <button @click="editRemarks" 
                                                class="px-3 py-1.5 text-xs font-medium text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors flex items-center gap-1">
                                            <i class="pi pi-pencil text-xs"></i>
                                            Edit
                                        </button>
                                        <button @click="deleteRemarks" 
                                                class="px-3 py-1.5 text-xs font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors flex items-center gap-1">
                                            <i class="pi pi-trash text-xs"></i>
                                            Delete
                                        </button>
                                    </div>
                                </div>

                                <!-- Textarea for new/updated remarks -->
                                <div v-if="!studentOutputs[selectedSubmission.id]?.remarks || isEditingRemarks">
                                    <Textarea v-model="selectedSubmission.newRemark"
                                            rows="4"
                                            class="w-full"
                                            placeholder="Add your remarks here..."
                                            :pt="{
                                                root: 'w-full rounded-xl border-indigo-100 focus:border-indigo-500 focus:ring-indigo-500',
                                            }"
                                    />
                                    <div class="flex justify-end gap-2 mt-3">
                                        <button @click="cancelEditRemarks"
                                                class="px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                                            Cancel
                                        </button>
                                        <button @click="saveRemarks"
                                                class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors">
                                            {{ isEditingRemarks ? 'Update Remarks' : 'Save Remarks' }}
                                        </button>
                                    </div>
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
                <div v-if="criteriaScores.length > 0" class="space-y-3">
                    <div v-for="(criterion, index) in criteriaScores" :key="index" 
                         class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div class="flex items-start gap-2">
                            <div class="w-2 h-2 bg-indigo-500 rounded-full mt-1.5"></div>
                            <p class="text-sm text-gray-600">{{ criterion.name }}</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <input
                                v-model.number="criterion.score"
                                type="number"
                                min="0"
                                :max="criterion.maxScore"
                                @input="validateCriterionScore(criterion)"
                                class="w-16 px-2 py-1 text-sm border border-indigo-100 rounded focus:outline-none focus:ring-1 focus:ring-indigo-500 text-center"
                                placeholder="0"
                            />
                            <span class="text-sm text-gray-500">/{{ criterion.maxScore }}</span>
                        </div>
                    </div>
                </div>
                <div v-else class="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                    <div class="flex items-start gap-3">
                        <i class="pi pi-exclamation-triangle text-yellow-600 text-lg mt-0.5"></i>
                        <div>
                            <p class="text-sm font-medium text-yellow-900 mb-1">No scoring criteria defined for this activity.</p>
                            <p class="text-xs text-yellow-700">This activity was created without scoring criteria. You can still score it manually, but it's recommended to create new activities with scoring criteria for better grading consistency.</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Total Score Display -->
            <div v-if="criteriaScores.length > 0" class="p-3 bg-indigo-50 rounded-lg">
                <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-indigo-900">Total Score:</span>
                    <span class="text-lg font-bold text-indigo-700">
                        {{ calculateDynamicTotalScore() }}/{{ calculateMaxTotalScore() }}
                    </span>
                </div>
            </div>
            
            <!-- Feedback Section -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                    Feedback for Student: 
                    <span class="text-xs text-gray-500 font-normal">(Optional)</span>
                </label>
                <textarea
                    v-model="scoreFeedback"
                    rows="4"
                    class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
                    placeholder="Provide constructive feedback on the student's work... (Optional)"
                ></textarea>
                <p class="text-xs text-gray-500 mt-1">This feedback will be visible to the student if provided.</p>
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
                :disabled="criteriaScores.length === 0 || !criteriaScores.every(c => c.score !== '' && c.score !== null)"
                :class="{ 'opacity-50 cursor-not-allowed': criteriaScores.length === 0 || !criteriaScores.every(c => c.score !== '' && c.score !== null) }"
            >
                Confirm
            </button>
        </template>
    </Dialog>
</template>
