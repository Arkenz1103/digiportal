<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import * as XLSX from 'xlsx';
import Dialog from 'primevue/dialog';
import Textarea from 'primevue/textarea';
import { useToast } from '../../composables/useToast';

// Initialize toast
const { showSuccess, showError, showInfo, showWarning } = useToast();

// Activity export dropdown state
const showActivityExportDropdown = ref(false);
const activityExportDropdownRef = ref(null);

// Export confirmation dialog state
const showExportConfirmDialog = ref(false);

// Confirm export action
const confirmExportAction = () => {
    showExportConfirmDialog.value = false;
    exportActivityResults('complete');
};

// Toggle activity export dropdown
const toggleActivityExportDropdown = () => {
    showActivityExportDropdown.value = !showActivityExportDropdown.value;
};

// Close dropdown when clicking outside
const handleExportClickOutside = (event) => {
    if (activityExportDropdownRef.value && !activityExportDropdownRef.value.contains(event.target)) {
        showActivityExportDropdown.value = false;
    }
};

// Helper function to get last name for sorting
const getLastName = (name) => {
    const parts = name.trim().split(' ');
    return parts.length > 1 ? parts[parts.length - 1].toLowerCase() : name.toLowerCase();
};

// Helper function to format student name properly (convert username format to proper name)
const formatStudentName = (name) => {
    if (!name) return 'Unknown';
    // If name looks like a username (contains dots or underscores), format it
    if (name.includes('.') || name.includes('_')) {
        return name
            .replace(/[._]/g, ' ')
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
            .join(' ');
    }
    return name;
};

// Helper function to get initials from name (first and last name initials)
const getInitials = (name) => {
    if (!name) return '?';
    const parts = name.trim().split(' ').filter(p => p.length > 0);
    if (parts.length >= 2) {
        return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
    }
    return name.charAt(0).toUpperCase();
};

// Helper function to determine accurate status
const getAccurateStatus = (submission) => {
    if (!submission || submission.status === 'Missing' || submission.status === 'Not Submitted') {
        return 'Missing';
    }
    if (submission.status === 'scored') {
        return submission.is_late ? 'Submitted Late' : 'Submitted';
    }
    if (submission.status === 'submitted' || submission.status === 'Submitted') {
        return submission.is_late ? 'Submitted Late' : 'Pending';
    }
    if (submission.resubmit_count > 0) {
        return 'Resubmitted';
    }
    return submission.status || 'Pending';
};

// Export activity results function - generates XLSX from displayed data
const exportActivityResults = (exportType) => {
    showActivityExportDropdown.value = false;

    if (!activity.value.id) {
        showError('Activity not loaded', 'Export Error');
        return;
    }

    try {
        const timestamp = new Date().toISOString().slice(0, 10);
        const activityName = activity.value.title.replace(/\s+/g, '_');
        const className = activity.value.class ? activity.value.class.replace(/\s+/g, '_') : 'Class';

        if (exportType === 'submitted') {
            // Export submitted (unscored) submissions only - CSV
            if (submissions.value.length === 0) {
                showError('No pending submissions to export', 'Export Error');
                return;
            }

            let csvContent = 'No,Student ID,Student Name,Status,Date & Time Submitted,Late Submission,Resubmissions\n';
            const sortedSubs = [...submissions.value].sort((a, b) => getLastName(a.name).localeCompare(getLastName(b.name)));
            sortedSubs.forEach((sub, index) => {
                const dateTime = sub.date && sub.time ? `${sub.date} ${sub.time}` : 'N/A';
                csvContent += `${index + 1},"${sub.studentId}","${formatStudentName(sub.name)}","Pending","${dateTime}","${sub.is_late ? 'Yes' : 'No'}","${sub.resubmit_count || 0}"\n`;
            });
            
            const filename = `${activityName}_Pending_${className}_${timestamp}.csv`;
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
            showSuccess(`Exported ${filename}`, 'Download Complete');
            return;

        } else if (exportType === 'not_submitted') {
            // Export students who haven't submitted - CSV
            if (incompleteSubmissions.value.length === 0) {
                showError('All students have submitted!', 'Export Info');
                return;
            }

            let csvContent = 'No,Student ID,Student Name,Status\n';
            const sortedStudents = [...incompleteSubmissions.value].sort((a, b) => getLastName(a.name).localeCompare(getLastName(b.name)));
            sortedStudents.forEach((student, index) => {
                csvContent += `${index + 1},"${student.studentIdNumber}","${formatStudentName(student.name)}","Missing"\n`;
            });
            
            const filename = `${activityName}_NotSubmitted_${className}_${timestamp}.csv`;
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
            showSuccess(`Exported ${filename}`, 'Download Complete');
            return;

        } else {
            // Complete report - ALL students with scores - XLSX format
            const totalStudents = scoredSubmissionsData.value.length + submissions.value.length + incompleteSubmissions.value.length;
            
            if (totalStudents === 0) {
                showError('No data to export', 'Export Error');
                return;
            }

            // Create workbook
            const workbook = XLSX.utils.book_new();

            // Calculate totals
            const totalSubmissions = scoredSubmissionsData.value.length + submissions.value.length;
            const totalIncomplete = incompleteSubmissions.value.length;

            // Calculate max score from scoring criteria
            let maxScore = 0;
            if (activity.value.scoringCriteria && Array.isArray(activity.value.scoringCriteria)) {
                maxScore = activity.value.scoringCriteria.reduce((sum, c) => sum + (parseInt(c.maxScore) || 0), 0);
            }

            // Combine all students and sort by last name
            const allStudents = [];
            const seenStudentIds = new Set(); // Track seen student IDs to prevent duplicates

            // Add scored submissions
            scoredSubmissionsData.value.forEach(sub => {
                const studentKey = sub.studentId || sub.studentDbId;
                if (seenStudentIds.has(studentKey)) return; // Skip duplicates
                seenStudentIds.add(studentKey);
                
                // Format score with overall
                let scoreDisplay = 'None';
                if (sub.score !== null && sub.score !== undefined && sub.score !== 'None') {
                    scoreDisplay = maxScore > 0 ? `${sub.score}/${maxScore}` : `${sub.score}`;
                }
                
                // Determine status including compiled and resubmitted
                let status = 'Submitted';
                if (sub.compiled || sub.is_compilation) {
                    status = 'Compiled';
                } else if (sub.resubmit_count > 0) {
                    status = `Resubmitted x${sub.resubmit_count}`;
                } else if (sub.is_late) {
                    status = 'Submitted Late';
                }
                
                allStudents.push({
                    studentId: sub.studentId,
                    name: formatStudentName(sub.name),
                    status: status,
                    dateTimeSubmitted: sub.date && sub.time ? `${sub.date} ${sub.time}` : (sub.date || 'N/A'),
                    score: scoreDisplay
                });
            });

            // Add unscored/pending submissions
            submissions.value.forEach(sub => {
                const studentKey = sub.studentId || sub.studentDbId;
                if (seenStudentIds.has(studentKey)) return; // Skip duplicates
                seenStudentIds.add(studentKey);
                
                // Determine status including compiled
                let status = 'Pending';
                if (sub.compiled || sub.is_compilation) {
                    status = 'Compiled';
                } else if (sub.resubmit_count > 0) {
                    status = `Resubmitted x${sub.resubmit_count}`;
                } else if (sub.is_late) {
                    status = 'Submitted Late';
                }
                allStudents.push({
                    studentId: sub.studentId,
                    name: formatStudentName(sub.name),
                    status: status,
                    dateTimeSubmitted: sub.date && sub.time ? `${sub.date} ${sub.time}` : (sub.date || 'N/A'),
                    score: 'None'
                });
            });

            // Add students who haven't submitted
            incompleteSubmissions.value.forEach(student => {
                const studentKey = student.studentIdNumber || student.studentPk;
                if (seenStudentIds.has(studentKey)) return; // Skip duplicates
                seenStudentIds.add(studentKey);
                
                allStudents.push({
                    studentId: student.studentIdNumber,
                    name: formatStudentName(student.name),
                    status: 'Missing',
                    dateTimeSubmitted: 'N/A',
                    score: 'None'
                });
            });

            // Sort by last name alphabetically
            allStudents.sort((a, b) => getLastName(a.name).localeCompare(getLastName(b.name)));

            // Format deadline date and time (12-hour format)
            let deadlineDisplay = 'N/A';
            if (activity.value.dueDate) {
                const dueDate = new Date(activity.value.dueDate);
                const dateStr = dueDate.toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
                
                // Format time to 12-hour format
                let timeStr = activity.value.formattedTime || '11:59 PM';
                if (activity.value.dueTime && !activity.value.formattedTime) {
                    // Convert 24-hour format (HH:MM:SS) to 12-hour format
                    const timeParts = activity.value.dueTime.split(':');
                    if (timeParts.length >= 2) {
                        let hours = parseInt(timeParts[0], 10);
                        const minutes = timeParts[1];
                        const ampm = hours >= 12 ? 'PM' : 'AM';
                        hours = hours % 12;
                        hours = hours ? hours : 12; // 0 should be 12
                        timeStr = `${hours}:${minutes} ${ampm}`;
                    }
                }
                deadlineDisplay = `${dateStr}, ${timeStr}`;
            }

            // Build sheet data
            const sheetData = [];

            // Title row
            sheetData.push([]);
            sheetData.push([`ACTIVITY REPORT - ${activity.value.title.toUpperCase()}`]);
            sheetData.push([`Subject/Folder: ${activity.value.subject || 'N/A'}`]);
            sheetData.push([`Activity Type: ${activity.value.type || activity.value.activityType || 'N/A'}`]);
            sheetData.push([`Class: ${activity.value.class || 'N/A'}`]);
            sheetData.push([`Deadline: ${deadlineDisplay}`]);
            sheetData.push([`Generated: ${new Date().toLocaleString()}`]);
            sheetData.push([]);
            sheetData.push([`Total Submissions: ${totalSubmissions}`]);
            sheetData.push([`Total Incomplete: ${totalIncomplete}`]);
            sheetData.push([]);

            // Header row - Score at the end
            sheetData.push(['No', 'Student ID', 'Student Name', 'Status', 'Date & Time Submitted', 'Score']);

            // Data rows
            allStudents.forEach((student, index) => {
                sheetData.push([
                    index + 1,
                    student.studentId,
                    student.name,
                    student.status,
                    student.dateTimeSubmitted,
                    student.score
                ]);
            });

            // Create worksheet
            const worksheet = XLSX.utils.aoa_to_sheet(sheetData);

            // Set column widths
            worksheet['!cols'] = [
                { wch: 5 },   // No
                { wch: 15 },  // Student ID
                { wch: 25 },  // Student Name
                { wch: 18 },  // Status
                { wch: 22 },  // Date & Time Submitted
                { wch: 12 }   // Score
            ];

            // Add worksheet to workbook
            XLSX.utils.book_append_sheet(workbook, worksheet, 'All Students');

            // Generate filename and download
            const filename = `${activityName}_AllStudents_${className}_${timestamp}.xlsx`;
            XLSX.writeFile(workbook, filename);

            showSuccess(`Exported ${filename}`, 'Download Complete');
        }
    } catch (error) {
        console.error('Export error:', error);
        showError('Failed to export activity results', 'Export Error');
    }
};

// Load activity from localStorage
const activity = ref({
    title: 'Student Activity',
    description: 'View student submissions for this activity',
    id: null,
    class: null, // Add class property
    subject: null
});

// Load activity data from API
const loadActivityFromAPI = async (activityId, setClassContext = false) => {
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

        // Format due date and time if available
        let formattedDateTime = '';
        if (response.data.due_date) {
            formattedDateTime = response.data.due_date;
            if (response.data.due_time) {
                const [hours, minutes, seconds] = response.data.due_time.split(':');
                const hour = parseInt(hours);
                const ampm = hour >= 12 ? 'PM' : 'AM';
                const displayHour = hour % 12 || 12;
                const secs = seconds || '00';
                formattedDateTime = `${response.data.due_date} at ${displayHour}:${minutes}:${secs} ${ampm}`;
            }
        }

        // Update activity with fresh data from API
        activity.value = {
            ...activity.value,
            id: activityId,
            title: response.data.title,
            description: response.data.description,
            type: response.data.activity_type,
            dueDate: response.data.due_date,
            dueTime: response.data.due_time,
            formattedDateTime: formattedDateTime,
            scoringCriteria: scoringCriteria,
            instruction_files: response.data.instruction_files || [],
            class: response.data.classroom_name || activity.value.class, // Get from API, fallback to existing
            subject: response.data.folder_name || activity.value.subject // Get folder name as subject
        };

        console.log('✅ Activity updated from API:', activity.value);

        // If coming from notification, set the class context in localStorage
        // This ensures "Back to Activities" works correctly
        if (setClassContext && response.data.classroom_id && response.data.classroom_name) {
            const classContext = {
                id: response.data.classroom_id,
                name: response.data.classroom_name
            };
            localStorage.setItem('digiportal_selected_class', JSON.stringify(classContext));
            console.log('✅ Set class context from notification:', classContext);
        }
        
        // After activity is fully updated (including class), load class members
        if (activity.value.class) {
            await loadClassMembers();
        }
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
    // Check if we're coming from a notification click
    const notificationContext = localStorage.getItem('notification_context');
    if (notificationContext) {
        try {
            const context = JSON.parse(notificationContext);
            // Only use if recent (within 10 seconds) to avoid stale data
            if (Date.now() - context.timestamp < 10000) {
                console.log('📬 Coming from notification:', context);
                
                // If notification has an activity ID, load that specific activity
                if (context.activityId) {
                    console.log('🎯 Loading specific activity from notification:', context.activityId);
                    // Pass true to set class context since we're coming from notification
                    await loadActivityFromAPI(context.activityId, true);
                    // Clear the notification context after using it
                    localStorage.removeItem('notification_context');
                    
                    // Load submissions for this activity
                    await Promise.all([
                        loadUnscoredSubmissions(),
                        loadScoredSubmissions()
                    ]);
                    loadClassMembers();
                    
                    // Listen for events
                    window.addEventListener('classChanged', handleClassChange);
                    document.addEventListener('click', handleExportClickOutside);
                    return; // Exit early since we've loaded the activity
                }
            }
            // Clear stale notification context
            localStorage.removeItem('notification_context');
        } catch (e) {
            console.error('Error parsing notification context:', e);
            localStorage.removeItem('notification_context');
        }
    }

    // Default behavior: load from saved activity
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
            instruction_files: parsedActivity.instruction_files || [],
            subject: parsedActivity.subject,
            class: parsedActivity.class // Load class from localStorage
        };
        console.log('✅ Loaded activity from localStorage:', activity.value);

        // Reload fresh data from API to get any updates
        if (parsedActivity.id) {
            await loadActivityFromAPI(parsedActivity.id);
        }
    }

    // Load submissions for this specific activity
    await Promise.all([
        loadUnscoredSubmissions(),
        loadScoredSubmissions()
    ]);
    
    // Load class members to calculate incomplete submissions
    loadClassMembers();

    // Listen for class change events
    window.addEventListener('classChanged', handleClassChange);

    // Listen for click outside to close export dropdown
    document.addEventListener('click', handleExportClickOutside);
});

onUnmounted(() => {
    // Clean up event listeners
    window.removeEventListener('classChanged', handleClassChange);
    document.removeEventListener('click', handleExportClickOutside);
});

// Define emits for navigation
const emit = defineEmits(['navigate']);

const goBack = () => {
    // Store the subject/folder context so Room.vue can show the activities list
    console.log('Going back with activity:', activity.value);
    
    // Ensure class context is set (in case it wasn't set earlier)
    const existingClass = localStorage.getItem('digiportal_selected_class');
    if (!existingClass && activity.value.class) {
        // Try to construct class context from activity data
        console.log('⚠️ No class context found, attempting to set from activity');
        // We need classroom_id which might not be available, so just ensure class name is there
    }
    
    if (activity.value.subject) {
        const returnData = {
            subject: activity.value.subject,
            showActivities: true,
            timestamp: Date.now()  // Add timestamp to expire after 5 seconds
        };
        console.log('Storing return context:', returnData);
        localStorage.setItem('return_to_activities', JSON.stringify(returnData));
    } else {
        console.warn('No subject found in activity, will show folders view instead');
        // Clear any stale return context
        localStorage.removeItem('return_to_activities');
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
const classMembers = ref([]); // Store all students in the class
const currentTab = ref('submitted'); // 'submitted', 'scored', 'incomplete'
const searchQuery = ref(''); // Search filter for student name and ID
const isLoadingSubmissions = ref(false);
const isClassMembersLoaded = ref(false);
const visibleIncompleteCount = ref(10); // Number of students to show initially in Incomplete tab

// Load class members from API
const loadClassMembers = async () => {
    if (!activity.value.class || activity.value.class === 'General') {
        console.warn('⚠️ Invalid or missing class information:', activity.value.class);
        return;
    }

    try {
        console.log('🔍 Fetching class members for:', activity.value.class);
        
        let grade = '';
        let section = '';

        // Parsing "Grade 3 - B" or "Grade 3-B"
        if (activity.value.class.includes(' - ')) {
            const parts = activity.value.class.split(' - ');
            grade = parts[0].trim();
            section = parts[1].trim();
        } else if (activity.value.class.includes('-')) {
            const parts = activity.value.class.split('-');
            grade = parts[0].trim();
            section = parts[1].trim();
        }

        if (grade && section) {
            console.log(`📡 API Request: /api/students/?grade_level=${grade}&section=${section}`);
            const response = await axios.get('/api/students/', {
                params: {
                    grade_level: grade,
                    section: section
                }
            });
            
            if (response.data && response.data.students) {
                console.log('✅ Loaded class members:', response.data.students.length);
                classMembers.value = response.data.students;
                isClassMembersLoaded.value = true;
            } else if (Array.isArray(response.data)) {
                classMembers.value = response.data;
                isClassMembersLoaded.value = true;
            }
        } else {
            console.warn('⚠️ Could not parse grade and section from:', activity.value.class);
        }
    } catch (error) {
        console.error('❌ Error loading class members:', error);
    }
};

// Calculate incomplete submissions (students who haven't submitted)
const incompleteSubmissions = computed(() => {
    if (!classMembers.value || !classMembers.value.length) return [];
    
    // Get database IDs of students who have submitted (either scored or unscored)
    // Use studentDbId (database ID) for accurate comparison with classMembers
    const submittedStudentDbIds = new Set([
        ...submissions.value.map(s => String(s.studentDbId || s.studentId)),
        ...scoredSubmissionsData.value.map(s => String(s.studentDbId || s.studentId))
    ]);
    
    // Logic for Pending vs Missing
    const now = new Date();
    let isPastDue = false;
    if (activity.value.dueDate) {
        try {
            // activity.value.dueDate is YYYY-MM-DD
            // activity.value.dueTime is HH:MM:SS
            const dateStr = activity.value.dueDate;
            const timeStr = activity.value.dueTime || '23:59:59';
            // Construct a proper ISO string for parsing to avoid browser-specific behavior
            const dueDateTime = new Date(`${dateStr}T${timeStr}`);
            isPastDue = now > dueDateTime;
        } catch (e) {
            console.error("❌ Error calculating due date status:", e);
        }
    }
    
    // Filter class members who are NOT in the submitted set (using database ID)
    // Also deduplicate by student ID to prevent repeated names
    const seenStudentIds = new Set();
    const list = classMembers.value
        .filter(student => {
            // Check if student has already submitted
            if (submittedStudentDbIds.has(String(student.id))) {
                return false;
            }
            // Deduplicate by student_id to prevent repeated names
            const studentIdKey = student.student_id || student.id;
            if (seenStudentIds.has(studentIdKey)) {
                return false;
            }
            seenStudentIds.add(studentIdKey);
            return true;
        })
        .map(student => {
            // Format name properly: "FirstName LastName" format
            let displayName = student.name || '';
            // If name looks like a username (contains dots or underscores), try to format it
            if (displayName.includes('.') || displayName.includes('_')) {
                // Try to use first_name and last_name if available
                if (student.first_name && student.last_name) {
                    displayName = `${student.first_name} ${student.last_name}`.trim();
                } else {
                    // Convert username format to proper name (e.g., "pablo.aguilar" -> "Pablo Aguilar")
                    displayName = displayName
                        .replace(/[._]/g, ' ')
                        .split(' ')
                        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
                        .join(' ');
                }
            }
            
            return {
                id: `missing-${student.id}`, // specific ID for this list
                studentPk: student.id,
                studentIdNumber: student.student_id || student.id_number || 'N/A', // Use actual student_id from API
                name: displayName || student.username || 'Unknown',
                // Add other necessary fields for the simplified view
                status: isPastDue ? 'Missing' : 'Pending',
                avatar: student.profile_picture || null,
                email: student.email || 'No email available'
            };
        });

    // Sort alphabetically by last name
    return list.sort((a, b) => {
        // Extract last name (assuming format: "FirstName LastName" or "LastName, FirstName")
        const getLastName = (fullName) => {
            const parts = fullName.trim().split(/\s+/);
            // If name has multiple parts, take the last part as last name
            return parts.length > 1 ? parts[parts.length - 1] : parts[0];
        };
        
        const lastNameA = getLastName(a.name);
        const lastNameB = getLastName(b.name);
        return lastNameA.localeCompare(lastNameB);
    });
});

// Paginated incomplete submissions with search filter
const filteredIncompleteSubmissions = computed(() => {
    if (!searchQuery.value.trim()) {
        return incompleteSubmissions.value;
    }
    const query = searchQuery.value.toLowerCase().trim();
    return incompleteSubmissions.value.filter(item => {
        const name = (item.name || '').toLowerCase();
        const studentId = (item.studentIdNumber || '').toString().toLowerCase();
        return name.includes(query) || studentId.includes(query);
    });
});

const displayedIncompleteSubmissions = computed(() => {
    return filteredIncompleteSubmissions.value.slice(0, visibleIncompleteCount.value);
});

const hasMoreIncomplete = computed(() => {
    return visibleIncompleteCount.value < filteredIncompleteSubmissions.value.length;
});

const loadMoreIncomplete = () => {
    visibleIncompleteCount.value += 10;
};

// Load unscored submissions from API
const loadUnscoredSubmissions = async () => {
    isLoadingSubmissions.value = true;
    try {
        const response = await axios.get('/api/submissions/unscored/');
        if (response.data) {
            console.log('📥 All unscored submissions from API:', response.data.length);
            console.log('🎯 Filtering by activity ID:', activity.value.id, 'type:', typeof activity.value.id);

            // Log compiled submissions before filtering
            const compiledSubs = response.data.filter(s => s.compiled || s.is_compilation);
            console.log('📦 Compiled submissions in response:', compiledSubs.length);
            compiledSubs.forEach(s => {
                console.log(`  - ID: ${s.id}, Student: ${s.student?.username}, Activity: ${s.activity || s.activity_id} (type: ${typeof (s.activity || s.activity_id)}), Status: ${s.display_status}`);
            });

            // Filter submissions by the current activity ID
            // Use == for loose comparison to handle string/number type differences
            const filteredSubmissions = response.data.filter(submission => {
                // Try both activity and activity_id fields
                const submissionActivityId = submission.activity || submission.activity_id;
                // Use loose equality (==) to handle type differences (string vs number)
                const matches = submissionActivityId == activity.value.id;
                
                // Log compiled submissions that don't match
                if ((submission.compiled || submission.is_compilation) && !matches) {
                    console.log(`⚠️ Compiled submission ${submission.id} has activity ${submissionActivityId} (type: ${typeof submissionActivityId}), expected ${activity.value.id} (type: ${typeof activity.value.id})`);
                }
                
                return matches;
            });

            console.log('✅ Filtered submissions count:', filteredSubmissions.length);

            submissions.value = filteredSubmissions.map(submission => {
                const submittedDate = new Date(submission.submitted_at);
                const dateStr = submittedDate.toLocaleDateString('en-PH', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    timeZone: 'Asia/Manila'
                });
                const timeStr = submittedDate.toLocaleTimeString('en-PH', {
                    hour: 'numeric',
                    minute: '2-digit',
                    hour12: true,
                    timeZone: 'Asia/Manila'
                });

                // Format student name properly
                let studentName = submission.student.full_name || '';
                if (!studentName || studentName === submission.student.username) {
                    if (submission.student.first_name && submission.student.last_name) {
                        studentName = `${submission.student.first_name} ${submission.student.last_name}`.trim();
                    } else if (submission.student.username) {
                        // Convert username format to proper name (e.g., "pablo.aguilar" -> "Pablo Aguilar")
                        studentName = submission.student.username
                            .replace(/[._]/g, ' ')
                            .split(' ')
                            .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
                            .join(' ');
                    }
                }

                return {
                    id: submission.id,
                    studentDbId: submission.student.id, // Database ID for comparison with classMembers
                    studentId: submission.student.student_id || submission.student.id_number || submission.student.id,
                    name: studentName,
                    profilePicture: submission.student.profile_picture_url || null,
                    activityTitle: submission.activity_title,
                    activityType: submission.activity_type,
                    caption: submission.caption,
                    score: submission.score,
                    status: submission.display_status || 'Submitted',
                    date: dateStr,
                    time: timeStr,
                    file_path: submission.file_url || submission.file_path,
                    file_type: submission.file_type,
                    submitted_at: submission.submitted_at,
                    is_late: submission.is_late || false,
                    resubmit_count: submission.resubmit_count || 0,
                    compiled: submission.compiled || false,
                    is_compilation: submission.is_compilation || false
                };
            });
            
            // Log final compiled submissions
            const finalCompiled = submissions.value.filter(s => s.compiled || s.is_compilation);
            console.log('📦 Final compiled submissions in list:', finalCompiled.length);
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
            console.log('📥 All scored submissions from API:', response.data.length);

            // Filter submissions by the current activity ID
            // Use == for loose comparison to handle string/number type differences
            const filteredSubmissions = response.data.filter(submission => {
                // Try both activity and activity_id fields
                const submissionActivityId = submission.activity || submission.activity_id;
                return submissionActivityId == activity.value.id;
            });

            scoredSubmissionsData.value = filteredSubmissions.map(submission => {
                const submittedDate = new Date(submission.scored_at || submission.submitted_at);
                const dateStr = submittedDate.toLocaleDateString('en-PH', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    timeZone: 'Asia/Manila'
                });
                const timeStr = submittedDate.toLocaleTimeString('en-PH', {
                    hour: 'numeric',
                    minute: '2-digit',
                    hour12: true,
                    timeZone: 'Asia/Manila'
                });

                // Format student name properly
                let studentName = submission.student.full_name || '';
                if (!studentName || studentName === submission.student.username) {
                    if (submission.student.first_name && submission.student.last_name) {
                        studentName = `${submission.student.first_name} ${submission.student.last_name}`.trim();
                    } else if (submission.student.username) {
                        // Convert username format to proper name (e.g., "pablo.aguilar" -> "Pablo Aguilar")
                        studentName = submission.student.username
                            .replace(/[._]/g, ' ')
                            .split(' ')
                            .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
                            .join(' ');
                    }
                }

                return {
                    id: submission.id,
                    studentDbId: submission.student.id, // Database ID for comparison with classMembers
                    studentId: submission.student.student_id || submission.student.id_number || submission.student.id,
                    name: studentName,
                    profilePicture: submission.student.profile_picture_url || null,
                    activityTitle: submission.activity_title,
                    activityType: submission.activity_type,
                    caption: submission.caption,
                    score: submission.score,
                    feedback: submission.feedback || '',
                    criteria_scores: submission.criteria_scores || null,
                    status: submission.display_status || 'Scored',
                    date: dateStr,
                    time: timeStr,
                    file_path: submission.file_url || submission.file_path,
                    file_type: submission.file_type,
                    submitted_at: submission.submitted_at,
                    is_late: submission.is_late || false,
                    resubmit_count: submission.resubmit_count || 0,
                    compiled: submission.compiled || false,
                    is_compilation: submission.is_compilation || false
                };
            });
            console.log('✅ Loaded scored submissions for activity:', activity.value.id, scoredSubmissionsData.value.length);
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
                status: response.data.display_status || (response.data.status === 'scored' ? 'Scored' : 'Submitted'),
                submitted_at: response.data.submitted_at,  // Raw datetime for formatting
                resubmit_count: response.data.resubmit_count || 0,
                submission_version: response.data.submission_version || 1,
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
const showInstructionExpandDialog = ref(false);
const showDeleteRemarksDialog = ref(false); // Delete remarks confirmation dialog
const creativityScore = ref('');
const technicalScore = ref('');
const requirementsScore = ref('');
const criteriaScores = ref([]); // Dynamic scores based on activity criteria
const scoreFeedback = ref(''); // Feedback for the student
const isEditingScore = ref(false); // Track if we're editing an existing score

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

    // Load full submission details including all files
    try {
        const response = await axios.get(`/api/submissions/${submission.id}/`);
        console.log('📥 Full submission data:', response.data);

        // Check if submission has multiple files
        const submissionFiles = response.data.files || [];
        
        // Use the submission data directly (it already has file_path and file_type)
        selectedSubmission.value = {
            ...submission,
            ...response.data,
            newRemark: '',
            rank: null,
            files: submissionFiles,
            currentFileIndex: 0, // Start with first file
            totalFiles: submissionFiles.length || 1
        };

        console.log(`📁 Submission has ${selectedSubmission.value.totalFiles} file(s)`);
    } catch (error) {
        console.error('❌ Error loading submission details:', error);
        // Fallback to basic submission data
        selectedSubmission.value = {
            ...submission,
            newRemark: '',
            rank: null,
            files: [],
            currentFileIndex: 0,
            totalFiles: 1
        };
    }

    showSubmissionDialog.value = true;
};

// Navigate to previous file
const previousFile = () => {
    if (selectedSubmission.value && selectedSubmission.value.currentFileIndex > 0) {
        selectedSubmission.value.currentFileIndex--;
    }
};

// Navigate to next file
const nextFile = () => {
    if (selectedSubmission.value && selectedSubmission.value.currentFileIndex < selectedSubmission.value.totalFiles - 1) {
        selectedSubmission.value.currentFileIndex++;
    }
};

// Get current file to display
const currentFile = computed(() => {
    if (!selectedSubmission.value) return null;
    
    // If submission has multiple files array
    if (selectedSubmission.value.files && selectedSubmission.value.files.length > 0) {
        const file = selectedSubmission.value.files[selectedSubmission.value.currentFileIndex];
        return {
            file_path: file.file_url || file.file_path,
            file_type: file.file_type,
            caption: file.file_name || selectedSubmission.value.caption
        };
    }
    
    // Fallback to main submission file
    return {
        file_path: selectedSubmission.value.file_path,
        file_type: selectedSubmission.value.file_type,
        caption: selectedSubmission.value.caption
    };
});

const editRemarks = () => {
    isEditingRemarks.value = true;
    // Pre-fill the textarea with existing remarks
    selectedSubmission.value.newRemark = studentOutputs.value[selectedSubmission.value.id]?.remarks || '';
};

// Show delete confirmation dialog
const confirmDeleteRemarks = () => {
    showDeleteRemarksDialog.value = true;
};

const deleteRemarks = async () => {
    showDeleteRemarksDialog.value = false;
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
    isEditingScore.value = false; // Not editing, adding new score

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

// Edit existing score
const editScore = () => {
    // Set editing mode
    isEditingScore.value = true;
    
    // Load existing feedback
    scoreFeedback.value = selectedSubmission.value.feedback || '';
    
    console.log('📝 Editing score for submission:', selectedSubmission.value.id);
    console.log('📊 Existing criteria_scores:', selectedSubmission.value.criteria_scores);
    
    // Try to load existing criteria scores
    let existingCriteriaScores = [];
    if (selectedSubmission.value.criteria_scores) {
        try {
            existingCriteriaScores = typeof selectedSubmission.value.criteria_scores === 'string'
                ? JSON.parse(selectedSubmission.value.criteria_scores)
                : selectedSubmission.value.criteria_scores;
            console.log('✅ Parsed existing criteria scores:', existingCriteriaScores);
        } catch (e) {
            console.error('❌ Error parsing existing criteria scores:', e);
        }
    }
    
    // Initialize criteria scores - prefer existing scores, fallback to activity criteria
    if (existingCriteriaScores && existingCriteriaScores.length > 0) {
        // Use existing scores
        criteriaScores.value = existingCriteriaScores.map(criterion => ({
            name: criterion.name,
            maxScore: parseInt(criterion.maxScore),
            score: parseInt(criterion.score)
        }));
        console.log('✅ Loaded existing criteria scores for editing:', criteriaScores.value);
    } else if (activity.value.scoringCriteria && activity.value.scoringCriteria.length > 0) {
        // Fallback to activity criteria with empty scores
        criteriaScores.value = activity.value.scoringCriteria.map(criterion => ({
            name: criterion.name,
            maxScore: criterion.maxScore,
            score: ''
        }));
        console.log('⚠️ No existing scores, using activity criteria:', criteriaScores.value);
    } else {
        criteriaScores.value = [];
        console.log('❌ No scoring criteria found');
    }
    
    // Show the score dialog
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

        const requestData = {
            score: totalScore,
            feedback: scoreFeedback.value.trim() || '',
            criteria_scores: JSON.stringify(criteriaScores.value.map(c => ({
                name: c.name,
                score: parseInt(c.score),
                maxScore: parseInt(c.maxScore)
            })))
        };

        // Use PUT for editing, POST for new scores
        const method = isEditingScore.value ? 'put' : 'post';
        const response = await axios[method](`/api/submissions/${selectedSubmission.value.id}/score/`, requestData);

        console.log(`✅ Score ${isEditingScore.value ? 'updated' : 'saved'} successfully:`, response.data);

        // Small delay to ensure database is updated
        await new Promise(resolve => setTimeout(resolve, 300));

        // Refresh both lists to update the submission data
        console.log('🔄 Reloading submissions...');
        await Promise.all([
            loadUnscoredSubmissions(),
            loadScoredSubmissions()
        ]);
        console.log('✅ Submissions reloaded');
        console.log('📊 Unscored count:', submissions.value.length);
        console.log('📊 Scored count:', scoredSubmissionsData.value.length);

        // Show success message
        showSuccess(isEditingScore.value ? 'Score updated successfully!' : 'Score saved successfully!', isEditingScore.value ? 'Updated' : 'Scored');

        // Switch to Scored tab to show the scored submission
        currentTab.value = 'scored';

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

// Get max score for a submission (from criteria_scores or activity scoring criteria)
const getMaxScoreForSubmission = (submission) => {
    // First try to get from submission's criteria_scores
    if (submission.criteria_scores) {
        try {
            const criteria = typeof submission.criteria_scores === 'string'
                ? JSON.parse(submission.criteria_scores)
                : submission.criteria_scores;
            if (criteria && criteria.length > 0) {
                return criteria.reduce((total, c) => total + (parseInt(c.maxScore) || 0), 0);
            }
        } catch (e) {
            console.error('Error parsing criteria_scores:', e);
        }
    }
    // Fallback to activity scoring criteria
    if (activity.value.scoringCriteria && activity.value.scoringCriteria.length > 0) {
        return activity.value.scoringCriteria.reduce((sum, c) => sum + (parseInt(c.maxScore) || 0), 0);
    }
    // Default fallback
    return 100;
};

// Computed properties for filtering submissions
const unscoredSubmissions = computed(() => {
    // Backend already filters by status='unscored', so just return the submissions
    // Apply search filter if query exists
    if (!searchQuery.value.trim()) {
        return submissions.value;
    }
    const query = searchQuery.value.toLowerCase().trim();
    return submissions.value.filter(item => {
        const name = (item.name || item.studentName || '').toLowerCase();
        const studentId = (item.studentIdNumber || item.studentId || '').toString().toLowerCase();
        return name.includes(query) || studentId.includes(query);
    });
});

const scoredSubmissions = computed(() => {
    // Apply search filter if query exists
    if (!searchQuery.value.trim()) {
        return scoredSubmissionsData.value;
    }
    const query = searchQuery.value.toLowerCase().trim();
    return scoredSubmissionsData.value.filter(item => {
        const name = (item.name || item.studentName || '').toLowerCase();
        const studentId = (item.studentIdNumber || item.studentId || '').toString().toLowerCase();
        return name.includes(query) || studentId.includes(query);
    });
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
    isEditingScore.value = false; // Reset editing state
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
        return date.toLocaleDateString('en-PH', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            timeZone: 'Asia/Manila'
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
        return date.toLocaleTimeString('en-PH', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true,
            timeZone: 'Asia/Manila'
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
<div class="bg-white p-4 md:p-3 shadow-sm border-b border-gray-200">
    <div class="flex flex-col lg:flex-row gap-4 lg:items-stretch">
        <!-- Left: Activity Details (50%) -->
        <div class="lg:w-1/2 flex flex-col gap-2">
            <!-- Subject Folder -->
            <div class="flex flex-col gap-1">
                <p class="text-sm text-black">
                    <span class="font-bold">Subject Folder:</span> {{ activity.subject || activity.folder || 'N/A' }}
                </p>
            </div>

            <!-- Activity Title -->
            <div class="flex flex-col gap-1">
                <p class="text-sm text-black">
                    <span class="font-bold">Activity Title:</span> {{ activity.title || 'Activity' }}
                </p>
            </div>

            <!-- Activity Type -->
            <div class="flex flex-col gap-1">
                <p class="text-sm text-black">
                    <span class="font-bold">Activity Type:</span> {{ activity.type || 'N/A' }}
                </p>
            </div>

            <!-- Due Date -->
            <div class="flex flex-col gap-1">
                <p class="text-sm text-black">
                    <span class="font-bold">Due date & time:</span> {{ activity.formattedDateTime || 'No due date set' }}
                </p>
            </div>

            <!-- Instructions/Description -->
            <div class="flex flex-col gap-2 flex-1">
                <div class="flex items-center justify-between flex-wrap gap-2">
                    <div class="flex items-center gap-2 flex-wrap">
                        <p class="text-sm font-bold text-black">Instruction:</p>
                        <!-- Attached Files next to Instruction label -->
                        <div v-if="activity.instruction_files && activity.instruction_files.length > 0" class="flex items-center gap-1 flex-wrap">
                            <a 
                                v-for="file in activity.instruction_files.slice(0, 2)" 
                                :key="file.id"
                                :href="file.file_url"
                                target="_blank"
                                class="flex items-center gap-1 px-2 py-1 bg-indigo-50 border border-indigo-200 rounded-lg text-xs hover:bg-indigo-100 transition-colors"
                            >
                                <i class="pi pi-file text-indigo-600"></i>
                                <span class="text-indigo-700 max-w-[100px] truncate">{{ file.file_name }}</span>
                            </a>
                            <span 
                                v-if="activity.instruction_files.length > 2"
                                class="flex items-center px-2 py-1 bg-gray-100 border border-gray-200 rounded-lg text-xs text-gray-600"
                            >
                                +{{ activity.instruction_files.length - 2 }} more
                            </span>
                        </div>
                    </div>
                    <button 
                        @click="showInstructionExpandDialog = true"
                        class="flex items-center gap-1 px-2 py-1 text-xs text-indigo-600 hover:text-indigo-800 hover:bg-indigo-50 rounded transition-colors"
                        title="Expand instruction"
                    >
                        <i class="pi pi-expand text-xs"></i>
                        <span>Expand</span>
                    </button>
                </div>
                <div class="p-3 bg-gray-50 rounded-lg border border-gray-200 flex-1 overflow-y-auto" style="max-height: 120px;">
                    <p v-if="activity.description" class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap break-words">{{ activity.description }}</p>
                    <p v-else class="text-sm text-gray-500 italic">No instructions provided</p>
                </div>
            </div>
        </div>

        <!-- Right: Scoring Criteria (50%) -->
        <div class="lg:w-1/2 lg:border-l lg:border-gray-200 lg:pl-4">
            <div class="flex flex-col gap-2 h-full">
                <div class="flex items-center gap-2">
                    <h3 class="text-sm font-bold text-gray-900">Scoring Criteria:</h3>
                </div>
                <div v-if="activity.scoringCriteria && activity.scoringCriteria.length > 0" class="space-y-2 flex-1 overflow-y-auto" style="max-height: 180px;">
                    <div v-for="(criterion, index) in activity.scoringCriteria" :key="index" class="flex items-start gap-2 p-2 bg-gray-50 rounded-lg border border-gray-200">
                        <div class="flex-1 min-w-0">
                            <p class="text-xs font-semibold text-gray-700 truncate">{{ criterion.name }}</p>
                            <p class="text-xs text-gray-600">{{ criterion.maxScore }} pts</p>
                        </div>
                    </div>
                </div>
                <div v-else class="text-xs text-gray-500 italic p-2 bg-gray-50 rounded-lg border border-gray-200">
                    No criteria defined
                </div>
            </div>
        </div>
    </div>
</div>


        <div class="p-4 space-y-4">
            <!-- Show submissions list only when no submission is selected -->
            <div v-if="!selectedSubmission" class="space-y-4">
                <!-- Back to Activities Button -->
                <div class="flex justify-start">
                    <button
                        @click="goBack"
                        class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
                    >
                        <i class="pi pi-arrow-left"></i>
                        <span>Back to Activities</span>
                    </button>
                </div>

                <!-- Tabbed Interface for Submissions -->
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden flex flex-col">
                    <!-- Export Button Row -->
                    <div class="px-6 py-3 bg-gradient-to-r from-gray-50 to-white border-b border-gray-200 flex justify-between items-center">
                        <div class="text-sm font-medium text-gray-700">
                            <i class="pi pi-users mr-2 text-indigo-600"></i>
                            Student Submissions
                        </div>
                        <button
                            @click="showExportConfirmDialog = true"
                            class="flex items-center gap-2 px-3 py-1.5 bg-emerald-600 text-white hover:bg-emerald-700 rounded-lg transition-all shadow-sm text-sm">
                            <i class="pi pi-file-excel text-xs"></i>
                            <span class="font-medium">Export Activity Record</span>
                        </button>
                    </div>

                    <!-- Tabs Header -->
                    <div class="flex border-b border-gray-200">
                        <button
                            @click="currentTab = 'submitted'"
                            class="flex-1 py-4 text-sm font-medium text-center transition-colors relative focus:outline-none"
                            :class="currentTab === 'submitted' ? 'text-indigo-600 bg-indigo-50/50' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'"
                        >
                            <span class="flex items-center justify-center gap-2">
                                <i class="pi pi-inbox"></i>
                                Submitted
                                <span v-if="unscoredSubmissions.length > 0" class="bg-indigo-100 text-indigo-700 py-0.5 px-2 rounded-full text-xs font-bold">
                                    {{ unscoredSubmissions.length }}
                                </span>
                            </span>
                            <div v-if="currentTab === 'submitted'" class="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-600"></div>
                        </button>
                        <button
                            @click="currentTab = 'scored'"
                            class="flex-1 py-4 text-sm font-medium text-center transition-colors relative focus:outline-none"
                            :class="currentTab === 'scored' ? 'text-indigo-600 bg-indigo-50/50' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'"
                        >
                            <span class="flex items-center justify-center gap-2">
                                <i class="pi pi-check-circle"></i>
                                Scored
                                <span v-if="scoredSubmissions.length > 0" class="bg-green-100 text-green-700 py-0.5 px-2 rounded-full text-xs font-bold">
                                    {{ scoredSubmissions.length }}
                                </span>
                            </span>
                            <div v-if="currentTab === 'scored'" class="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-600"></div>
                        </button>
                        <button
                            @click="currentTab = 'incomplete'"
                            class="flex-1 py-4 text-sm font-medium text-center transition-colors relative focus:outline-none"
                            :class="currentTab === 'incomplete' ? 'text-indigo-600 bg-indigo-50/50' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'"
                        >
                            <span class="flex items-center justify-center gap-2">
                                <i class="pi pi-exclamation-circle"></i>
                                Incomplete
                                <span v-if="incompleteSubmissions.length > 0" class="bg-red-100 text-red-700 py-0.5 px-2 rounded-full text-xs font-bold">
                                    {{ incompleteSubmissions.length }}
                                </span>
                            </span>
                            <div v-if="currentTab === 'incomplete'" class="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-600"></div>
                        </button>
                    </div>

                    <!-- Filter & View Controls -->
                    <div class="px-6 py-3 border-b border-gray-200 bg-gray-50/30 flex flex-col sm:flex-row gap-3 sm:justify-between sm:items-center">
                        <div class="flex items-center gap-4">
                            <!-- Search Input -->
                            <div class="relative">
                                <input
                                    v-model="searchQuery"
                                    type="text"
                                    placeholder="Search by name or ID..."
                                    class="w-64 px-4 py-2 pl-10 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
                                />
                                <i class="pi pi-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 text-sm"></i>
                                <button 
                                    v-if="searchQuery" 
                                    @click="searchQuery = ''"
                                    class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                                >
                                    <i class="pi pi-times text-xs"></i>
                                </button>
                            </div>

                        </div>
                        <div v-if="currentTab !== 'incomplete'" class="flex items-center rounded-lg bg-white border border-gray-200 p-1 shadow-sm">
                            <button @click="toggleView('list')"
                                    :class="['p-1.5 rounded-md transition-all', viewMode === 'list' ? 'bg-indigo-100 text-indigo-600' : 'text-gray-400 hover:text-gray-600 hover:bg-gray-50']"
                                    title="List View">
                                <i class="pi pi-list"></i>
                            </button>
                            <button @click="toggleView('card')"
                                    :class="['p-1.5 rounded-md transition-all', viewMode === 'card' ? 'bg-indigo-100 text-indigo-600' : 'text-gray-400 hover:text-gray-600 hover:bg-gray-50']"
                                    title="Card View">
                                <i class="pi pi-th-large"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Content Area -->
                    <div class="min-h-[300px] relative">
                        <!-- Loading State -->
                        <div v-if="isLoadingSubmissions" class="absolute inset-0 flex justify-center items-center bg-white/80 z-10">
                            <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
                        </div>

                        <!-- Empty States -->
                        <div v-if="(currentTab === 'submitted' && unscoredSubmissions.length === 0) || 
                                   (currentTab === 'scored' && scoredSubmissions.length === 0) || 
                                   (currentTab === 'incomplete' && incompleteSubmissions.length === 0)" 
                             class="flex flex-col items-center justify-center py-20 text-center">
                            <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4">
                                <i :class="['pi text-3xl text-gray-300', 
                                    currentTab === 'submitted' ? 'pi-inbox' : 
                                    currentTab === 'scored' ? 'pi-check-circle' : 'pi-user']"></i>
                            </div>
                            <h3 class="text-lg font-medium text-gray-900">
                                {{ currentTab === 'submitted' ? 'No new submissions' : 
                                   currentTab === 'scored' ? 'No scored submissions' : 
                                   (!isClassMembersLoaded ? 'Loading students...' : 'All students have submitted') }}
                            </h3>
                            <p class="text-gray-500 mt-1 max-w-xs">
                                {{ currentTab === 'submitted' ? 'Great job! You have reviewed all current submissions.' : 
                                   currentTab === 'scored' ? 'Graded work will appear here.' : 
                                   (!isClassMembersLoaded ? 'Checking class roster...' : 'Everyone in the class has turned in their work.') }}
                            </p>
                        </div>

                        <!-- Lists -->
                        <template v-else>
                            <!-- List View (always show for incomplete tab) -->
                            <div v-if="viewMode === 'list' || currentTab === 'incomplete'">
                                <!-- Table Header -->
                                <div class="bg-gray-50/50 border-b border-gray-100 grid grid-cols-12 gap-4 px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                    <template v-if="currentTab === 'incomplete'">
                                        <div class="col-span-3">Student Name</div>
                                        <div class="col-span-2">ID Number</div>
                                        <div class="col-span-5">Contact Info</div>
                                        <div class="col-span-2">Status</div>
                                    </template>
                                    <template v-else-if="currentTab === 'scored'">
                                        <div class="col-span-3">Student Name</div>
                                        <div class="col-span-2">ID Number</div>
                                        <div class="col-span-2">Status</div>
                                        <div class="col-span-3">Date & Time Submitted</div>
                                        <div class="col-span-2 text-center">Score</div>
                                    </template>
                                    <template v-else>
                                        <div class="col-span-4">Student Name</div>
                                        <div class="col-span-2">ID Number</div>
                                        <div class="col-span-3">Status</div>
                                        <div class="col-span-3">Date & Time Submitted</div>
                                    </template>
                                </div>

                                <div class="divide-y divide-gray-100">
                                    <div v-for="item in (currentTab === 'submitted' ? unscoredSubmissions : currentTab === 'scored' ? scoredSubmissions : displayedIncompleteSubmissions)" 
                                         :key="item.id"
                                         class="grid grid-cols-12 gap-4 px-6 py-4 items-center hover:bg-gray-50 transition-colors"
                                         :class="{'cursor-pointer': currentTab !== 'incomplete'}"
                                         @click="currentTab !== 'incomplete' ? viewSubmission(item) : null"
                                    >
                                        <template v-if="currentTab === 'incomplete'">
                                            <!-- Name & Avatar -->
                                            <div class="col-span-3 flex items-center gap-3">
                                                <div class="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold shadow-sm overflow-hidden"
                                                     :class="item.avatar ? '' : 'bg-indigo-100 text-indigo-700'">
                                                    <img v-if="item.avatar" :src="item.avatar" :alt="item.name" class="w-full h-full object-cover" />
                                                    <span v-else>{{ getInitials(item.name) }}</span>
                                                </div>
                                                <div class="font-medium text-gray-900">{{ item.name }}</div>
                                            </div>

                                            <!-- ID Number -->
                                            <div class="col-span-2 text-sm text-gray-600">
                                                {{ item.studentIdNumber }}
                                            </div>

                                            <!-- Contact Info -->
                                            <div class="col-span-5 text-sm text-gray-500 italic truncate" :title="item.email">
                                                {{ item.email }}
                                            </div>

                                            <!-- Status -->
                                            <div class="col-span-2">
                                                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border whitespace-nowrap"
                                                      :class="item.status === 'Missing' ? 'bg-red-100 text-red-800 border-red-200' : 'bg-yellow-100 text-yellow-800 border-yellow-200'">
                                                    <i :class="['pi mr-1 text-[10px]', item.status === 'Missing' ? 'pi-times-circle' : 'pi-clock']"></i>
                                                    {{ item.status }}
                                                </span>
                                            </div>
                                        </template>
                                        <template v-else>
                                            <!-- Standard View for Submitted/Scored -->
                                            <!-- Name & Avatar -->
                                            <div :class="currentTab === 'scored' ? 'col-span-3' : 'col-span-4'" class="flex items-center gap-3">
                                                <div class="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold shadow-sm overflow-hidden"
                                                     :class="item.profilePicture ? '' : 'bg-indigo-100 text-indigo-700'">
                                                    <img v-if="item.profilePicture" :src="item.profilePicture" :alt="item.name" class="w-full h-full object-cover" />
                                                    <span v-else>{{ getInitials(item.name) }}</span>
                                                </div>
                                                <div>
                                                    <div class="font-medium text-gray-900">{{ item.name }}</div>
                                                </div>
                                            </div>

                                            <!-- ID Number -->
                                            <div class="col-span-2 text-sm text-gray-700 font-medium">
                                                {{ item.studentId || 'No ID' }}
                                            </div>

                                            <!-- Status Badge -->
                                            <div :class="currentTab === 'scored' ? 'col-span-2' : 'col-span-3'">
                                                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border"
                                                      :class="{
                                                          'bg-purple-50 text-purple-700 border-purple-200': item.status === 'Compiled' || item.compiled || item.is_compilation,
                                                          'bg-blue-50 text-blue-700 border-blue-200': item.resubmit_count > 0 && item.status !== 'Compiled',
                                                          'bg-orange-50 text-orange-700 border-orange-200': item.is_late && !item.resubmit_count && item.status !== 'Compiled',
                                                          'bg-green-50 text-green-700 border-green-200': !item.is_late && !item.resubmit_count && item.status !== 'Compiled' && !item.compiled && !item.is_compilation
                                                      }">
                                                    <i v-if="item.status === 'Compiled' || item.compiled || item.is_compilation" class="pi pi-folder-open mr-1 text-[10px]"></i>
                                                    <i v-else-if="item.resubmit_count > 0" class="pi pi-refresh mr-1 text-[10px]"></i>
                                                    <i v-else-if="item.is_late" class="pi pi-clock mr-1 text-[10px]"></i>
                                                    <i v-else class="pi pi-check-circle mr-1 text-[10px]"></i>
                                                    {{ (item.status === 'Compiled' || item.compiled || item.is_compilation) ? 'Compiled' : (item.resubmit_count > 0 ? `Resubmitted x${item.resubmit_count}` : (item.is_late ? 'Submitted Late' : 'Submitted')) }}
                                                </span>
                                            </div>

                                            <!-- Date & Time Submitted -->
                                            <div class="col-span-3 text-sm text-gray-600">
                                                <div class="font-medium text-gray-900">{{ item.date }}</div>
                                                <div class="text-xs text-gray-500">{{ item.time }}</div>
                                            </div>

                                            <!-- Score (only for scored tab) -->
                                            <div v-if="currentTab === 'scored'" class="col-span-2 flex justify-center">
                                                <div class="font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-lg">
                                                    {{ item.score }}<span class="text-gray-400">/</span><span class="text-gray-600">{{ getMaxScoreForSubmission(item) }}</span> <span class="text-xs text-gray-500">pts</span>
                                                </div>
                                            </div>
                                        </template>
                                    </div>
                                </div>

                                <!-- Load More Button for Incomplete Tab -->
                                <div v-if="currentTab === 'incomplete' && hasMoreIncomplete" class="px-6 py-4 bg-gray-50/30 border-t border-gray-100 flex justify-center">
                                    <button 
                                        @click="loadMoreIncomplete"
                                        class="px-6 py-2 text-sm font-semibold text-indigo-600 bg-white border border-indigo-200 rounded-full hover:bg-indigo-50 hover:border-indigo-300 transition-all shadow-sm flex items-center gap-2"
                                    >
                                        <i class="pi pi-plus text-xs"></i>
                                        Load More Students
                                    </button>
                                </div>
                            </div>

                            <!-- Card View -->
                            <div v-else class="p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                                <div v-for="item in (currentTab === 'submitted' ? unscoredSubmissions : currentTab === 'scored' ? scoredSubmissions : filteredIncompleteSubmissions)" 
                                     :key="item.id"
                                     class="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-all transform hover:-translate-y-1 duration-200 group"
                                     :class="{'cursor-pointer': currentTab !== 'incomplete'}"
                                     @click="currentTab !== 'incomplete' ? viewSubmission(item) : null"
                                >
                                    <!-- Preview Area -->
                                    <div class="aspect-video bg-gray-100 relative overflow-hidden group-hover:opacity-95 transition-opacity">
                                        <template v-if="currentTab === 'incomplete'">
                                            <div class="w-full h-full flex flex-col items-center justify-center bg-gray-50 text-gray-400">
                                                <i class="pi pi-user text-4xl mb-2 opacity-50"></i>
                                                <span class="text-xs font-medium uppercase tracking-wide">Not Submitted</span>
                                            </div>
                                        </template>
                                        <template v-else>
                                            <div class="w-full h-full flex items-center justify-center bg-white">
                                                <img v-if="item.file_type === 'image' && item.file_path" 
                                                     :src="item.file_path.startsWith('http') || item.file_path.startsWith('data:') ? item.file_path : `data:image/png;base64,${item.file_path}`" 
                                                     class="w-full h-full object-contain p-2" />
                                                <div v-else class="flex flex-col items-center justify-center text-gray-500">
                                                    <i :class="['pi text-4xl mb-2', item.file_type === 'pdf' ? 'pi-file-pdf text-red-500' : 'pi-file text-blue-500']"></i>
                                                    <span class="text-xs font-medium">{{ item.file_type || 'Document' }}</span>
                                                </div>
                                            </div>
                                            <!-- Overlay gradient -->
                                            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                        </template>

                                        <!-- Status Badge (Top Left) -->
                                        <div v-if="currentTab !== 'incomplete'" class="absolute top-3 left-3">
                                            <span class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md shadow-sm"
                                                  :class="{
                                                      'bg-purple-500 text-white': item.status === 'Compiled' || item.compiled || item.is_compilation,
                                                      'bg-blue-500 text-white': item.resubmit_count > 0 && item.status !== 'Compiled',
                                                      'bg-orange-500 text-white': item.is_late && !item.resubmit_count && item.status !== 'Compiled',
                                                      'bg-green-500 text-white': (item.status === 'Submitted' || item.status === 'Scored') && !item.compiled && !item.is_compilation
                                                  }">
                                                {{ (item.status === 'Compiled' || item.compiled || item.is_compilation) ? 'Compiled' : (item.resubmit_count > 0 ? 'Resubmitted' : (item.is_late ? 'Late' : item.status)) }}
                                            </span>
                                        </div>
                                    </div>

                                    <!-- Card Content -->
                                    <div class="p-4">
                                        <div class="flex items-center gap-3">
                                            <div class="w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold shrink-0 overflow-hidden"
                                                 :class="(currentTab === 'incomplete' ? (item.avatar ? '' : 'bg-gray-100 text-gray-600') : (item.profilePicture ? '' : 'bg-indigo-100 text-indigo-700'))">
                                                <img v-if="currentTab === 'incomplete' ? item.avatar : item.profilePicture" 
                                                     :src="currentTab === 'incomplete' ? item.avatar : item.profilePicture" 
                                                     :alt="item.name" 
                                                     class="w-full h-full object-cover" />
                                                <span v-else>{{ getInitials(item.name) }}</span>
                                            </div>
                                            <div class="min-w-0 flex-1">
                                                <h4 class="text-sm font-semibold text-gray-900 truncate">{{ item.name }}</h4>
                                                <div class="flex items-center text-xs text-gray-500 mt-0.5">
                                                    <i v-if="currentTab !== 'incomplete'" class="pi pi-calendar mr-1 opacity-70"></i>
                                                    <span class="truncate">
                                                        {{ currentTab === 'incomplete' ? 'Missing work' : item.date }}
                                                    </span>
                                                </div>
                                            </div>
                                            <!-- Score on Card -->
                                            <div v-if="currentTab === 'scored'" class="shrink-0 font-bold text-indigo-600 bg-indigo-50 px-2 py-1 rounded text-xs">
                                                {{ item.score }}/{{ getMaxScoreForSubmission(item) }}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>
            </div>

            <!-- Show submission details when a submission is selected -->
            <div v-if="selectedSubmission" class="space-y-6">
                <!-- Back to Submissions Button -->
                <div class="flex justify-start">
                    <button
                        @click="selectedSubmission = null"
                        class="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
                    >
                        <i class="pi pi-arrow-left"></i>
                        <span>Back to Submissions</span>
                    </button>
                </div>

                <div class="bg-white rounded-3xl shadow-lg overflow-hidden border border-indigo-100">
                    <div class="px-6 py-4 border-b border-indigo-100">
                        <div class="flex items-center gap-3">
                            <h2 class="text-xl font-semibold text-gray-900 flex items-center gap-2">
                                <i class="pi pi-user-edit text-indigo-700"></i>
                                Submission Details
                            </h2>
                        </div>
                    </div>

                    <div class="p-6">
                        <div class="flex justify-between items-center mb-6 relative">
                        <h3 class="text-2xl font-semibold text-gray-900 px-2">
                            {{ selectedSubmission.caption || selectedSubmission.activityTitle || 'Submission Details' }}
                        </h3>

                        <!-- Add Score Button (replaced with Edit Score if already scored) -->
                        <button
                            v-if="selectedSubmission.score !== null && selectedSubmission.score !== undefined"
                            @click="editScore"
                            class="px-4 py-2 bg-amber-100 text-amber-800 rounded-lg font-medium flex items-center gap-2 border border-amber-300 hover:bg-amber-200 transition-colors cursor-pointer"
                        >
                            <i class="pi pi-pencil"></i>
                            <span>Edit Score</span>
                        </button>
                        <button
                            v-else
                            @click="addScore"
                            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors duration-200 flex items-center gap-2"
                        >
                            <i class="pi pi-plus-circle"></i>
                            <span>Add Score</span>
                        </button>


                    </div>

                    <div class="space-y-6">
                        <!-- Top Row - Image and Student Info -->
                        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                            <!-- Image -->
                            <div class="lg:col-span-2 flex flex-col">
                                <div class="bg-white rounded-xl overflow-hidden border-2 border-indigo-100 flex-1" style="min-height: 350px;">
                                    <div class="w-full h-full flex items-center justify-center p-4 bg-white relative">
                                        <!-- Navigation Arrows (only show if multiple files) -->
                                        <div v-if="selectedSubmission.totalFiles > 1" class="absolute inset-0 flex items-center justify-between px-2 pointer-events-none z-10">
                                            <!-- Previous Button -->
                                            <button
                                                @click="previousFile"
                                                :disabled="selectedSubmission.currentFileIndex === 0"
                                                class="pointer-events-auto w-10 h-10 rounded-full bg-white/90 hover:bg-white shadow-lg flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed"
                                                :class="selectedSubmission.currentFileIndex === 0 ? '' : 'hover:scale-110'"
                                            >
                                                <i class="pi pi-chevron-left text-indigo-600"></i>
                                            </button>
                                            
                                            <!-- Next Button -->
                                            <button
                                                @click="nextFile"
                                                :disabled="selectedSubmission.currentFileIndex >= selectedSubmission.totalFiles - 1"
                                                class="pointer-events-auto w-10 h-10 rounded-full bg-white/90 hover:bg-white shadow-lg flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed"
                                                :class="selectedSubmission.currentFileIndex >= selectedSubmission.totalFiles - 1 ? '' : 'hover:scale-110'"
                                            >
                                                <i class="pi pi-chevron-right text-indigo-600"></i>
                                            </button>
                                        </div>

                                        <!-- File Counter (only show if multiple files) -->
                                        <div v-if="selectedSubmission.totalFiles > 1" class="absolute top-4 left-1/2 transform -translate-x-1/2 z-10">
                                            <div class="bg-indigo-600 text-white px-3 py-1 rounded-full text-xs font-medium shadow-lg">
                                                {{ selectedSubmission.currentFileIndex + 1 }} / {{ selectedSubmission.totalFiles }}
                                            </div>
                                        </div>

                                        <!-- Image Display -->
                                        <img v-if="currentFile && currentFile.file_type === 'image' && currentFile.file_path && currentFile.file_path.length > 0"
                                            :src="currentFile.file_path.startsWith('http') || currentFile.file_path.startsWith('/media') || currentFile.file_path.startsWith('data:') ? currentFile.file_path : `data:image/png;base64,${currentFile.file_path}`"
                                            :alt="currentFile.caption || 'Student submission'"
                                            class="max-w-full max-h-[450px] object-contain rounded-lg"
                                        />
                                        <!-- PDF Display -->
                                        <div v-else-if="currentFile && currentFile.file_type === 'pdf' && currentFile.file_path" class="flex flex-col items-center justify-center text-red-600">
                                            <i class="pi pi-file-pdf text-8xl mb-4"></i>
                                            <span class="text-lg font-medium">PDF Document</span>
                                            <span class="text-sm text-gray-500 mt-2">{{ currentFile.caption || 'Untitled' }}</span>
                                            <!-- View File Button for PDF -->
                                            <a
                                                :href="currentFile.file_path"
                                                target="_blank"
                                                class="mt-4 flex items-center justify-center gap-2 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors duration-200 font-medium shadow-md hover:shadow-lg"
                                            >
                                                <i class="pi pi-external-link"></i>
                                                <span>View File</span>
                                            </a>
                                        </div>
                                        <!-- Word Document Display -->
                                        <div v-else-if="currentFile && currentFile.file_type === 'document' && currentFile.file_path" class="flex flex-col items-center justify-center text-blue-600">
                                            <i class="pi pi-file-word text-8xl mb-4"></i>
                                            <span class="text-lg font-medium">Word Document</span>
                                            <span class="text-sm text-gray-500 mt-2">{{ currentFile.caption || 'Untitled' }}</span>
                                            <!-- View File Button for Document -->
                                            <a
                                                :href="currentFile.file_path"
                                                target="_blank"
                                                class="mt-4 flex items-center justify-center gap-2 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors duration-200 font-medium shadow-md hover:shadow-lg"
                                            >
                                                <i class="pi pi-external-link"></i>
                                                <span>View File</span>
                                            </a>
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

                            <!-- Student Info and Remarks Column -->
                            <div class="flex flex-col gap-4">
                                <div class="bg-white p-4 rounded-xl border-2 border-indigo-100">
                                    <h4 class="text-md font-semibold text-gray-900 mb-3 flex items-center gap-2">
                                        <i class="pi pi-user" style="color: #6366f1;"></i>
                                        Student Information
                                    </h4>
                                    <div class="space-y-2">
                                        <div class="flex items-center gap-3">
                                            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-lg font-medium overflow-hidden"
                                                :style="selectedSubmission.profilePicture ? '' : 'background-color: #e0e7ff; color: #111827;'">
                                                <img v-if="selectedSubmission.profilePicture" :src="selectedSubmission.profilePicture" :alt="selectedSubmission.name" class="w-full h-full object-cover" />
                                                <span v-else>{{ getInitials(selectedSubmission.name) }}</span>
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
                                                    (selectedSubmission.status === 'Compiled' || selectedSubmission.compiled || selectedSubmission.is_compilation) ? 'bg-purple-100 text-purple-800' :
                                                    selectedSubmission.resubmit_count > 0 ? 'bg-blue-100 text-blue-800' :
                                                    selectedSubmission.is_late ? 'bg-orange-100 text-orange-800' :
                                                    'bg-green-100 text-green-800'
                                                ]">
                                                    <i v-if="selectedSubmission.status === 'Compiled' || selectedSubmission.compiled || selectedSubmission.is_compilation" class="pi pi-folder-open text-xs"></i>
                                                    <i v-else-if="selectedSubmission.resubmit_count > 0" class="pi pi-refresh text-xs"></i>
                                                    <i v-else-if="selectedSubmission.is_late" class="pi pi-clock text-xs"></i>
                                                    <i v-else class="pi pi-check-circle text-xs"></i>
                                                    <span v-if="selectedSubmission.status === 'Compiled' || selectedSubmission.compiled || selectedSubmission.is_compilation">Compiled</span>
                                                    <span v-else-if="selectedSubmission.resubmit_count > 0">Resubmitted</span>
                                                    <span v-else-if="selectedSubmission.is_late">Submitted Late</span>
                                                    <span v-else>Submitted</span>
                                                </span>
                                            </div>
                                            <div class="flex justify-between text-sm">
                                                <span class="text-gray-500">Submitted:</span>
                                                <div class="text-right">
                                                    <div class="font-medium">{{ formatSubmissionDate(selectedSubmission.submitted_at) }}</div>
                                                    <div class="text-xs text-gray-400 mt-0.5">{{ formatSubmissionTime(selectedSubmission.submitted_at) }}</div>
                                                </div>
                                            </div>
                                            <!-- Score Display (only if scored) -->
                                            <div v-if="selectedSubmission.score !== null && selectedSubmission.score !== undefined" class="flex justify-between items-center text-sm pt-2 border-t border-indigo-100 mt-2">
                                                <span class="text-gray-500">Score:</span>
                                                <div class="font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-lg">
                                                    {{ selectedSubmission.score }}<span class="text-gray-400">/</span><span class="text-gray-600">{{ getMaxScoreForSubmission(selectedSubmission) }}</span> <span class="text-xs text-gray-500">pts</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Teacher's Remarks (Optional/Collapsible) - Below Student Info -->
                                <div class="bg-white p-4 rounded-xl border-2 border-indigo-100 flex-1">
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
                                                <button @click="confirmDeleteRemarks"
                                                        class="px-3 py-1.5 text-xs font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors flex items-center gap-1">
                                                    <i class="pi pi-trash text-xs"></i>
                                                    Delete
                                                </button>
                                            </div>
                                        </div>

                                        <!-- Textarea for new/updated remarks -->
                                        <div v-if="!studentOutputs[selectedSubmission.id]?.remarks || isEditingRemarks">
                                            <Textarea v-model="selectedSubmission.newRemark"
                                                    rows="3"
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
            </div>
        </div>
    </div>

    <!-- Add/Edit Score Dialog -->
    <Dialog v-model:visible="showAddScoreDialog" modal :header="isEditingScore ? 'Edit Score' : 'Add Score'" :style="{ width: '800px' }">
        <div class="space-y-4">
            <!-- Student Info -->
            <div class="bg-indigo-50 p-3 rounded-lg">
                <p class="text-sm font-medium text-indigo-900">Student: {{ selectedSubmission?.name }}</p>
                <p class="text-sm text-indigo-700">Output: {{ selectedSubmission?.content?.title || 'Submission' }}</p>
            </div>

            <!-- Scoring Criteria -->
            <div>
                <h4 class="text-sm font-medium text-gray-700 mb-3">Scoring Criteria:</h4>
                <div v-if="criteriaScores.length > 0" class="space-y-3 max-h-48 overflow-y-auto pr-1">
                    <div v-for="(criterion, index) in criteriaScores" :key="index"
                         class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div class="flex items-start gap-2 flex-1 min-w-0">
                            <div class="w-2 h-2 bg-indigo-500 rounded-full mt-1.5 flex-shrink-0"></div>
                            <p class="text-sm text-gray-600 truncate" :title="criterion.name">{{ criterion.name }}</p>
                        </div>
                        <div class="flex items-center gap-2 flex-shrink-0">
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
                {{ isEditingScore ? 'Update Score' : 'Confirm' }}
            </button>
        </template>
    </Dialog>

    <!-- Instruction Expand Dialog -->
    <Dialog v-model:visible="showInstructionExpandDialog" modal header="Activity Instruction" :style="{ width: '600px' }">
        <div class="space-y-4">
            <!-- Instruction Text -->
            <div v-if="activity.description" class="p-4 bg-gray-50 rounded-lg border border-gray-200">
                <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap break-words">{{ activity.description }}</p>
            </div>
            <div v-else-if="!activity.instruction_files || activity.instruction_files.length === 0" class="p-4 bg-gray-50 rounded-lg border border-gray-200">
                <p class="text-sm text-gray-500 italic">No instructions provided</p>
            </div>

            <!-- Attached Files -->
            <div v-if="activity.instruction_files && activity.instruction_files.length > 0">
                <h4 class="text-sm font-semibold text-gray-700 mb-2">Attached Files:</h4>
                <div class="flex flex-wrap gap-2">
                    <a 
                        v-for="file in activity.instruction_files" 
                        :key="file.id"
                        :href="file.file_url"
                        target="_blank"
                        class="flex items-center gap-2 px-3 py-2 bg-indigo-50 border border-indigo-200 rounded-lg text-sm hover:bg-indigo-100 transition-colors"
                    >
                        <i class="pi pi-file text-indigo-600"></i>
                        <span class="text-indigo-700">{{ file.file_name }}</span>
                        <i class="pi pi-external-link text-indigo-400 text-sm"></i>
                    </a>
                </div>
            </div>
        </div>
        <template #footer>
            <button
                @click="showInstructionExpandDialog = false"
                class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
            >
                Close
            </button>
        </template>
    </Dialog>

    <!-- Export Confirmation Dialog -->
    <Dialog v-model:visible="showExportConfirmDialog" modal header="Export Activity Results" :style="{ width: '400px' }">
        <div class="text-center py-4">
            <div class="w-16 h-16 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-4">
                <i class="pi pi-file-excel text-3xl text-emerald-600"></i>
            </div>
            <p class="text-gray-600 text-sm">Are you sure you want to export all students' results for this activity? This will generate an Excel file.</p>
        </div>
        <template #footer>
            <div class="flex gap-3 justify-center">
                <button
                    @click="showExportConfirmDialog = false"
                    class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-colors">
                    Cancel
                </button>
                <button
                    @click="confirmExportAction"
                    class="px-6 py-2 rounded-lg bg-emerald-600 text-white font-medium hover:bg-emerald-700 transition-colors">
                    Export
                </button>
            </div>
        </template>
    </Dialog>

    <!-- Delete Remarks Confirmation Dialog -->
    <Dialog v-model:visible="showDeleteRemarksDialog" modal header="Delete Remarks" :style="{ width: '400px' }">
        <div class="text-center py-4">
            <div class="w-16 h-16 rounded-full bg-red-100 flex items-center justify-center mx-auto mb-4">
                <i class="pi pi-trash text-3xl text-red-600"></i>
            </div>
            <p class="text-gray-600 text-sm">Are you sure you want to delete these remarks? This action cannot be undone.</p>
        </div>
        <template #footer>
            <div class="flex gap-3 justify-center">
                <button
                    @click="showDeleteRemarksDialog = false"
                    class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-colors">
                    Cancel
                </button>
                <button
                    @click="deleteRemarks"
                    class="px-6 py-2 rounded-lg bg-red-600 text-white font-medium hover:bg-red-700 transition-colors">
                    Delete
                </button>
            </div>
        </template>
    </Dialog>
</template>
