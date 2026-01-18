<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Menu from 'primevue/menu';
import { useToast } from '../../composables/useToast';

const { showSuccess, showError, showWarning } = useToast();

// Viewing archived school year state
const isViewingArchived = ref(false);
const viewingSchoolYear = ref(null);

// Dashboard stats
const stats = ref({
    total_students: 0,
    total_teachers: 0,
    total_classrooms: 0,
    total_activities: 0,
    total_submissions: 0,
});
const currentSchoolYear = ref(null);
const recentStudents = ref([]);
const recentTeachers = ref([]);

// Users management
const users = ref([]);
const isLoadingUsers = ref(false);
const userRoleFilter = ref('all');
const userSearch = ref('');

// Classrooms management
const classrooms = ref([]);
const isLoadingClassrooms = ref(false);

// School years management
const schoolYears = ref([]);
const isLoadingSchoolYears = ref(false);

// Teachers list for dropdown
const teachersList = ref([]);

// Modals
const showCreateUserModal = ref(false);
const showCreateClassroomModal = ref(false);
const showCreateSchoolYearModal = ref(false);
const showAssignTeacherModal = ref(false);
const showArchiveConfirmModal = ref(false);
const schoolYearToArchive = ref(null);

// Edit/Delete modals
const showEditUserModal = ref(false);
const showDeleteUserModal = ref(false);
const showEditClassroomModal = ref(false);
const showDeleteClassroomModal = ref(false);
const showEditSchoolYearModal = ref(false);
const showDeleteSchoolYearModal = ref(false);

// Archive/Restore modals
const showArchiveUserModal = ref(false);
const showRestoreUserModal = ref(false);
const userToArchive = ref(null);
const userToRestore = ref(null);
const archiveUserData = ref({
    reason: '',
});

// Archived users management
const archivedUsers = ref([]);
const isLoadingArchivedUsers = ref(false);
const archivedUserRoleFilter = ref('all');
const archivedUserSearch = ref('');

// Password Recovery management
const recoveryRequests = ref([]);
const isLoadingRecoveryRequests = ref(false);
const recoveryStatusFilter = ref('all');
const showPhotoModal = ref(false);
const selectedRecoveryRequest = ref(null);
const showApproveConfirmModal = ref(false);
const showRejectConfirmModal = ref(false);
const requestToApprove = ref(null);
const requestToReject = ref(null);

// Menu refs for actions dropdown
const userActionMenu = ref();

// Selected items for edit/delete
const selectedUser = ref(null);
const selectedClassroomForEdit = ref(null);
const selectedSchoolYear = ref(null);

// Edit form data
const editUser = ref({
    first_name: '',
    last_name: '',
    email: '',
    is_active: true,
    password: '',
});

const editClassroom = ref({
    grade_level: null,
    section: '',
    teacher_id: null,
});

const editSchoolYear = ref({
    name: '',
});

// Form data
const newUser = ref({
    role: 'student',
    first_name: '',
    last_name: '',
    email: '',
    password: 'password123',
    grade_level: null,
});

const newClassroom = ref({
    grade_level: null,
    section: '',
    teacher_id: null,
});

const newSchoolYear = ref({
    name: '',
});

const selectedClassroom = ref(null);
const selectedTeacherId = ref(null);

// Options
const roleOptions = [
    { label: 'Student', value: 'student' },
    { label: 'Teacher', value: 'teacher' },
];

const gradeOptions = [
    { label: 'Grade 1', value: 1 },
    { label: 'Grade 2', value: 2 },
    { label: 'Grade 3', value: 3 },
    { label: 'Grade 4', value: 4 },
    { label: 'Grade 5', value: 5 },
    { label: 'Grade 6', value: 6 },
];

const sectionOptions = [
    { label: 'Section A', value: 'A' },
    { label: 'Section B', value: 'B' },
    { label: 'Section C', value: 'C' },
    { label: 'Section D', value: 'D' },
];

const archiveReasonOptions = computed(() => {
    if (userToArchive.value?.role === 'student') {
        return [
            { label: 'Graduate', value: 'Graduate' },
            { label: 'Transfer Out', value: 'Transfer Out' },
            { label: 'Other', value: 'Other' },
        ];
    } else {
        return [
            { label: 'Retire', value: 'Retire' },
            { label: 'Resign', value: 'Resign' },
            { label: 'Transfer Out', value: 'Transfer Out' },
            { label: 'Other', value: 'Other' },
        ];
    }
});

// Display school year name
const displaySchoolYear = computed(() => {
    if (isViewingArchived.value && viewingSchoolYear.value) {
        return viewingSchoolYear.value.name;
    }
    return currentSchoolYear.value?.name || 'Not Set';
});

// Load dashboard data
const loadDashboard = async (schoolYearName = null) => {
    try {
        let url = '/api/admin/dashboard/';
        if (schoolYearName) {
            url += `?school_year=${encodeURIComponent(schoolYearName)}`;
        }
        const response = await axios.get(url);
        stats.value = response.data.stats;
        if (!schoolYearName) {
            currentSchoolYear.value = response.data.current_school_year;
        }
        recentStudents.value = response.data.recent_students || [];
        recentTeachers.value = response.data.recent_teachers || [];
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
};

// Load users
const loadUsers = async (schoolYearName = null) => {
    isLoadingUsers.value = true;
    try {
        let url = '/api/admin/users/';
        const params = new URLSearchParams();
        
        // Handle role filter
        if (userRoleFilter.value && userRoleFilter.value !== 'all') {
            params.append('role', userRoleFilter.value);
        }
        
        // Handle search
        if (userSearch.value && userSearch.value.trim()) {
            params.append('search', userSearch.value.trim());
        }
        
        // Handle school year filter
        if (schoolYearName) {
            params.append('school_year', schoolYearName);
        }
        
        if (params.toString()) url += '?' + params.toString();
        
        const response = await axios.get(url);
        users.value = response.data.users || [];
    } catch (error) {
        console.error('Error loading users:', error);
        showError('Failed to load users');
    } finally {
        isLoadingUsers.value = false;
    }
};

// Load classrooms
const loadClassrooms = async (schoolYearName = null) => {
    isLoadingClassrooms.value = true;
    try {
        let url = '/api/admin/classrooms/';
        const params = new URLSearchParams();
        if (schoolYearName) {
            params.append('school_year', schoolYearName);
            params.append('include_archived', 'true');
        }
        if (params.toString()) url += '?' + params.toString();
        
        const response = await axios.get(url);
        classrooms.value = response.data.classrooms || [];
    } catch (error) {
        console.error('Error loading classrooms:', error);
        showError('Failed to load classrooms');
    } finally {
        isLoadingClassrooms.value = false;
    }
};

// Load school years
const loadSchoolYears = async () => {
    isLoadingSchoolYears.value = true;
    try {
        const response = await axios.get('/api/admin/school-years/');
        schoolYears.value = response.data.school_years || [];
    } catch (error) {
        console.error('Error loading school years:', error);
        showError('Failed to load school years');
    } finally {
        isLoadingSchoolYears.value = false;
    }
};

// Load teachers list
const loadTeachers = async () => {
    try {
        const response = await axios.get('/api/admin/teachers/');
        teachersList.value = response.data.teachers || [];
    } catch (error) {
        console.error('Error loading teachers:', error);
    }
};

// Load archived users
const loadArchivedUsers = async () => {
    isLoadingArchivedUsers.value = true;
    try {
        let url = '/api/admin/archived-users/';
        const params = new URLSearchParams();
        
        if (archivedUserRoleFilter.value && archivedUserRoleFilter.value !== 'all') {
            params.append('role', archivedUserRoleFilter.value);
        }
        
        if (archivedUserSearch.value && archivedUserSearch.value.trim()) {
            params.append('search', archivedUserSearch.value.trim());
        }
        
        if (params.toString()) url += '?' + params.toString();
        
        const response = await axios.get(url);
        archivedUsers.value = response.data.users || [];
    } catch (error) {
        console.error('Error loading archived users:', error);
        showError('Failed to load archived users');
    } finally {
        isLoadingArchivedUsers.value = false;
    }
};

// Load password recovery requests
const loadRecoveryRequests = async () => {
    isLoadingRecoveryRequests.value = true;
    try {
        let url = '/api/password-recovery/requests/';
        if (recoveryStatusFilter.value && recoveryStatusFilter.value !== 'all') {
            url += `?status=${recoveryStatusFilter.value}`;
        }
        
        const response = await axios.get(url);
        recoveryRequests.value = response.data || [];
        console.log('✅ Loaded recovery requests:', recoveryRequests.value.length);
    } catch (error) {
        console.error('Error loading recovery requests:', error);
        showError('Failed to load recovery requests');
    } finally {
        isLoadingRecoveryRequests.value = false;
    }
};

// Open approve confirmation
const openApproveConfirm = (request) => {
    requestToApprove.value = request;
    showApproveConfirmModal.value = true;
};

// Open reject confirmation
const openRejectConfirm = (request) => {
    requestToReject.value = request;
    showRejectConfirmModal.value = true;
};

// Approve recovery request
const approveRecoveryRequest = async () => {
    if (!requestToApprove.value) return;
    
    try {
        const response = await axios.post(`/api/password-recovery/approve/${requestToApprove.value.id}/`);
        showSuccess(`Password recovery approved for ${requestToApprove.value.name}. Temporary password: password123`);
        showApproveConfirmModal.value = false;
        requestToApprove.value = null;
        await loadRecoveryRequests();
    } catch (error) {
        console.error('Error approving recovery request:', error);
        showError('Failed to approve recovery request');
    }
};

// Reject recovery request
const rejectRecoveryRequest = async () => {
    if (!requestToReject.value) return;
    
    try {
        await axios.post(`/api/password-recovery/reject/${requestToReject.value.id}/`);
        showSuccess(`Password recovery request rejected for ${requestToReject.value.name}`);
        showRejectConfirmModal.value = false;
        requestToReject.value = null;
        await loadRecoveryRequests();
    } catch (error) {
        console.error('Error rejecting recovery request:', error);
        showError('Failed to reject recovery request');
    }
};

// View ID photos
const viewIdPhotos = (request) => {
    selectedRecoveryRequest.value = request;
    showPhotoModal.value = true;
};

// Computed menu items for user actions
const userActionMenuItems = computed(() => {
    if (!selectedUser.value) return [];
    return [
        {
            label: 'Edit',
            icon: 'pi pi-pencil',
            command: () => openEditUserModal(selectedUser.value)
        },
        {
            label: 'Archive',
            icon: 'pi pi-user-minus',
            command: () => openArchiveUserModal(selectedUser.value)
        }
    ];
});

// Toggle user action menu
const toggleUserActionMenu = (event, user) => {
    selectedUser.value = user;
    userActionMenu.value.toggle(event);
};

// Open archive user modal
const openArchiveUserModal = (user) => {
    userToArchive.value = user;
    archiveUserData.value = {
        reason: '',
    };
    showArchiveUserModal.value = true;
};

// Archive user
const archiveUser = async () => {
    if (!userToArchive.value) return;
    if (!archiveUserData.value.reason) {
        showError('Please select a reason for archiving');
        return;
    }
    
    try {
        const response = await axios.put(
            `/api/admin/users/${userToArchive.value.id}/archive/`,
            archiveUserData.value
        );
        showSuccess(response.data.message);
        showArchiveUserModal.value = false;
        userToArchive.value = null;
        archiveUserData.value = { reason: '' };
        loadUsers(isViewingArchived.value ? viewingSchoolYear.value?.name : null);
        loadDashboard(isViewingArchived.value ? viewingSchoolYear.value?.name : null);
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to archive user');
    }
};

// Open restore user modal
const openRestoreUserModal = (user) => {
    userToRestore.value = user;
    showRestoreUserModal.value = true;
};

// Restore user
const restoreUser = async () => {
    if (!userToRestore.value) return;
    try {
        const response = await axios.put(`/api/admin/users/${userToRestore.value.id}/restore/`);
        showSuccess(response.data.message);
        showRestoreUserModal.value = false;
        userToRestore.value = null;
        loadArchivedUsers();
        loadDashboard();
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to restore user');
    }
};

// Create user
const createUser = async () => {
    try {
        const response = await axios.post('/api/admin/users/', newUser.value);
        showSuccess(response.data.message);
        showCreateUserModal.value = false;
        resetNewUser();
        loadUsers();
        loadDashboard();
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to create user');
    }
};

// Create classroom
const createClassroom = async () => {
    try {
        const response = await axios.post('/api/admin/classrooms/', newClassroom.value);
        showSuccess(response.data.message);
        showCreateClassroomModal.value = false;
        resetNewClassroom();
        loadClassrooms();
        loadDashboard();
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to create classroom');
    }
};

// Create school year
const createSchoolYear = async () => {
    try {
        const response = await axios.post('/api/admin/school-years/', newSchoolYear.value);
        showSuccess(response.data.message);
        showCreateSchoolYearModal.value = false;
        newSchoolYear.value = { name: '' };
        loadSchoolYears();
        loadDashboard();
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to create school year');
    }
};

// Assign teacher to classroom
const assignTeacher = async () => {
    if (!selectedClassroom.value) return;
    try {
        const response = await axios.put(
            `/api/admin/classrooms/${selectedClassroom.value.id}/assign-teacher/`,
            { teacher_id: selectedTeacherId.value }
        );
        showSuccess(response.data.message);
        showAssignTeacherModal.value = false;
        selectedClassroom.value = null;
        selectedTeacherId.value = null;
        loadClassrooms(isViewingArchived.value ? viewingSchoolYear.value?.name : null);
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to assign teacher');
    }
};

// Open assign teacher modal
const openAssignTeacherModal = (classroom) => {
    selectedClassroom.value = classroom;
    selectedTeacherId.value = classroom.teacher?.id || null;
    showAssignTeacherModal.value = true;
};

// Open archive confirmation modal
const openArchiveConfirmModal = (schoolYear) => {
    schoolYearToArchive.value = schoolYear;
    showArchiveConfirmModal.value = true;
};

// Archive school year
const archiveSchoolYear = async () => {
    if (!schoolYearToArchive.value) return;
    try {
        const response = await axios.put(`/api/admin/school-years/${schoolYearToArchive.value.id}/archive/`);
        showSuccess(response.data.message);
        showArchiveConfirmModal.value = false;
        schoolYearToArchive.value = null;
        loadSchoolYears();
        loadDashboard();
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to archive school year');
    }
};

// View archived school year
const viewArchivedSchoolYear = (schoolYear) => {
    isViewingArchived.value = true;
    viewingSchoolYear.value = schoolYear;
    loadDashboard(schoolYear.name);
    loadUsers(schoolYear.name);
    loadClassrooms(schoolYear.name);
    showSuccess(`Viewing archived school year: ${schoolYear.name}`);
};

// Back to current school year
const backToCurrentSchoolYear = () => {
    isViewingArchived.value = false;
    viewingSchoolYear.value = null;
    loadDashboard();
    loadUsers();
    loadClassrooms();
    showSuccess('Returned to current school year');
};

// Reset forms
const resetNewUser = () => {
    newUser.value = {
        role: 'student',
        first_name: '',
        last_name: '',
        email: '',
        password: 'password123',
        grade_level: null,
    };
};

const resetNewClassroom = () => {
    newClassroom.value = {
        grade_level: null,
        section: '',
        teacher_id: null,
    };
};

// Computed
const filteredUsers = computed(() => {
    return users.value;
});

// Logout function
const logout = async () => {
    try {
        await axios.post('/api/auth/logout/');
        // Clear any stored data
        localStorage.clear();
        // Redirect to login page
        window.location.href = '/';
    } catch (error) {
        console.error('Logout error:', error);
        // Even if logout fails, redirect to login
        window.location.href = '/';
    }
};

// ===== USER EDIT/DELETE FUNCTIONS =====
const openEditUserModal = (user) => {
    selectedUser.value = user;
    editUser.value = {
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email,
        is_active: user.is_active,
        password: '',
    };
    showEditUserModal.value = true;
};

const openDeleteUserModal = (user) => {
    selectedUser.value = user;
    showDeleteUserModal.value = true;
};

const updateUser = async () => {
    if (!selectedUser.value) return;
    try {
        const payload = { ...editUser.value };
        if (!payload.password) delete payload.password;
        
        const response = await axios.put(`/api/admin/users/${selectedUser.value.id}/`, payload);
        showSuccess(response.data.message);
        showEditUserModal.value = false;
        selectedUser.value = null;
        loadUsers(isViewingArchived.value ? viewingSchoolYear.value?.name : null);
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to update user');
    }
};

const deleteUser = async () => {
    if (!selectedUser.value) return;
    try {
        const response = await axios.delete(`/api/admin/users/${selectedUser.value.id}/`);
        showSuccess(response.data.message);
        showDeleteUserModal.value = false;
        selectedUser.value = null;
        loadUsers(isViewingArchived.value ? viewingSchoolYear.value?.name : null);
        loadDashboard(isViewingArchived.value ? viewingSchoolYear.value?.name : null);
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to delete user');
    }
};

// ===== CLASSROOM EDIT/DELETE FUNCTIONS =====
const openEditClassroomModal = (classroom) => {
    selectedClassroomForEdit.value = classroom;
    editClassroom.value = {
        grade_level: classroom.grade_level,
        section: classroom.section,
        teacher_id: classroom.teacher?.id || null,
    };
    showEditClassroomModal.value = true;
};

const openDeleteClassroomModal = (classroom) => {
    selectedClassroomForEdit.value = classroom;
    showDeleteClassroomModal.value = true;
};

const updateClassroom = async () => {
    if (!selectedClassroomForEdit.value) return;
    try {
        const response = await axios.put(`/api/admin/classrooms/${selectedClassroomForEdit.value.id}/`, editClassroom.value);
        showSuccess(response.data.message);
        showEditClassroomModal.value = false;
        selectedClassroomForEdit.value = null;
        loadClassrooms(isViewingArchived.value ? viewingSchoolYear.value?.name : null);
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to update classroom');
    }
};

const deleteClassroom = async () => {
    if (!selectedClassroomForEdit.value) return;
    try {
        const response = await axios.delete(`/api/admin/classrooms/${selectedClassroomForEdit.value.id}/`);
        showSuccess(response.data.message);
        showDeleteClassroomModal.value = false;
        selectedClassroomForEdit.value = null;
        loadClassrooms(isViewingArchived.value ? viewingSchoolYear.value?.name : null);
        loadDashboard(isViewingArchived.value ? viewingSchoolYear.value?.name : null);
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to delete classroom');
    }
};

// ===== SCHOOL YEAR EDIT/DELETE FUNCTIONS =====
const openEditSchoolYearModal = (schoolYear) => {
    selectedSchoolYear.value = schoolYear;
    editSchoolYear.value = {
        name: schoolYear.name,
    };
    showEditSchoolYearModal.value = true;
};

const openDeleteSchoolYearModal = (schoolYear) => {
    selectedSchoolYear.value = schoolYear;
    showDeleteSchoolYearModal.value = true;
};

const updateSchoolYear = async () => {
    if (!selectedSchoolYear.value) return;
    try {
        const response = await axios.put(`/api/admin/school-years/${selectedSchoolYear.value.id}/`, editSchoolYear.value);
        showSuccess(response.data.message);
        showEditSchoolYearModal.value = false;
        selectedSchoolYear.value = null;
        loadSchoolYears();
        loadDashboard();
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to update school year');
    }
};

const deleteSchoolYear = async () => {
    if (!selectedSchoolYear.value) return;
    try {
        const response = await axios.delete(`/api/admin/school-years/${selectedSchoolYear.value.id}/`);
        showSuccess(response.data.message);
        showDeleteSchoolYearModal.value = false;
        selectedSchoolYear.value = null;
        loadSchoolYears();
        loadDashboard();
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to delete school year');
    }
};

onMounted(() => {
    loadDashboard();
    loadUsers();
    loadRecoveryRequests();
    loadClassrooms();
    loadSchoolYears();
    loadTeachers();
    loadArchivedUsers();
});
</script>

<template>
    <div class="flex flex-col min-h-screen bg-white/80">
        <!-- Header -->
        <div class="shadow-lg rounded-t-xl h-40 md:h-36 flex items-center px-6 md:px-8"
            :class="isViewingArchived ? 'bg-gradient-to-r from-amber-600 via-orange-600 to-amber-700' : 'bg-gradient-to-r from-indigo-700 via-violet-700 to-blue-700'">
            <div class="max-w-7xl mx-auto w-full flex items-center justify-between">
                <div>
                    <h1 class="text-3xl md:text-4xl font-bold text-white flex items-center gap-3">
                        Admin Dashboard
                    </h1>
                    <p v-if="isViewingArchived" class="text-amber-100 text-sm mt-1">
                        <i class="pi pi-history mr-1"></i>Viewing Archived: {{ viewingSchoolYear?.name }}
                    </p>
                </div>
                <div class="flex items-center gap-3">
                    <Button v-if="isViewingArchived" 
                        label="Back to Current" 
                        icon="pi pi-arrow-left" 
                        @click="backToCurrentSchoolYear"
                        class="bg-white text-amber-700 hover:bg-amber-50" />
                    <Button 
                        label="Logout" 
                        icon="pi pi-sign-out" 
                        @click="logout"
                        :class="isViewingArchived ? 'bg-amber-800 hover:bg-amber-900 border-amber-800' : 'bg-indigo-800 hover:bg-indigo-900 border-indigo-800'" />
                </div>
            </div>
        </div>

        <div class="max-w-7xl mx-auto px-8 py-6 w-full flex-1">
            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div class="bg-white rounded-lg shadow p-4">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                            <i class="pi pi-users text-blue-600 text-lg"></i>
                        </div>
                        <div>
                            <p class="text-xl font-bold text-gray-800">{{ stats.total_students }}</p>
                            <p class="text-xs text-gray-500">Students</p>
                        </div>
                    </div>
                </div>
                <div class="bg-white rounded-lg shadow p-4">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                            <i class="pi pi-user text-green-600 text-lg"></i>
                        </div>
                        <div>
                            <p class="text-xl font-bold text-gray-800">{{ stats.total_teachers }}</p>
                            <p class="text-xs text-gray-500">Teachers</p>
                        </div>
                    </div>
                </div>
                <div class="bg-white rounded-lg shadow p-4">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                            <i class="pi pi-building text-purple-600 text-lg"></i>
                        </div>
                        <div>
                            <p class="text-xl font-bold text-gray-800">{{ stats.total_classrooms }}</p>
                            <p class="text-xs text-gray-500">Classrooms</p>
                        </div>
                    </div>
                </div>
                <div class="bg-white rounded-lg shadow p-4">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-lg flex items-center justify-center"
                            :class="isViewingArchived ? 'bg-amber-100' : 'bg-indigo-100'">
                            <i class="pi pi-calendar text-lg" :class="isViewingArchived ? 'text-amber-600' : 'text-indigo-600'"></i>
                        </div>
                        <div>
                            <p class="text-base font-bold text-gray-800">{{ displaySchoolYear }}</p>
                            <p class="text-xs" :class="isViewingArchived ? 'text-amber-600' : 'text-gray-500'">
                                {{ isViewingArchived ? 'Archived' : 'School Year' }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tabs -->
            <TabView>
                <!-- Users Tab -->
                <TabPanel header="Users">
                    <div class="p-4">
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex items-center gap-4">
                                <Dropdown v-model="userRoleFilter" :options="[{label: 'All', value: 'all'}, ...roleOptions]" 
                                    optionLabel="label" optionValue="value"
                                    @change="loadUsers" class="w-40" />
                                <InputText v-model="userSearch" placeholder="Search users..." 
                                    @keyup.enter="loadUsers" class="w-64" />
                                <Button label="Search" icon="pi pi-search" @click="loadUsers" />
                            </div>
                            <Button label="Create User" icon="pi pi-plus" @click="showCreateUserModal = true" 
                                class="bg-indigo-600 hover:bg-indigo-700"
                                :disabled="isViewingArchived"
                                :title="isViewingArchived ? 'Cannot create users while viewing archived data' : ''" />
                        </div>
                        
                        <DataTable :value="users" :loading="isLoadingUsers" paginator :rows="10"
                            class="p-datatable-sm" stripedRows>
                            <Column field="id_number" header="ID Number" sortable />
                            <Column field="name" header="Name" sortable />
                            <Column field="email" header="Email" sortable />
                            <Column field="role" header="Role" sortable>
                                <template #body="{ data }">
                                    <span :class="data.role === 'teacher' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'"
                                        class="px-2 py-1 rounded-full text-xs font-medium capitalize">
                                        {{ data.role }}
                                    </span>
                                </template>
                            </Column>
                            <Column header="Classroom">
                                <template #body="{ data }">
                                    <div v-if="data.role === 'student'">
                                        <span v-if="data.classroom" class="text-gray-700">{{ data.classroom.name }}</span>
                                        <span v-else-if="data.classroom_history" class="text-amber-600">
                                            {{ data.classroom_history.classroom_name }}
                                            <span class="text-xs text-gray-500 block">
                                                Joined: {{ new Date(data.classroom_history.joined_at).toLocaleDateString() }}
                                            </span>
                                        </span>
                                        <span v-else class="text-gray-400">-</span>
                                    </div>
                                    <span v-else-if="data.role === 'teacher' && data.assigned_classroom" class="text-green-600">{{ data.assigned_classroom.name }}</span>
                                    <span v-else class="text-gray-400">-</span>
                                </template>
                            </Column>
                            <Column header="Status">
                                <template #body="{ data }">
                                    <span :class="data.is_active ? 'text-green-600' : 'text-red-600'">
                                        {{ data.is_active ? 'Active' : 'Inactive' }}
                                    </span>
                                </template>
                            </Column>
                            <Column header="Actions" v-if="!isViewingArchived">
                                <template #body="{ data }">
                                    <Button icon="pi pi-ellipsis-v" size="small" text rounded
                                        @click="toggleUserActionMenu($event, data)" 
                                        aria-haspopup="true" 
                                        aria-controls="user_action_menu" />
                                </template>
                            </Column>
                        </DataTable>
                        
                        <!-- User Actions Menu -->
                        <Menu ref="userActionMenu" id="user_action_menu" :model="userActionMenuItems" :popup="true" />
                    </div>
                </TabPanel>

                <!-- Classrooms Tab -->
                <TabPanel header="Classrooms">
                    <div class="p-4">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-semibold">Manage Classrooms</h3>
                            <Button label="Create Classroom" icon="pi pi-plus" @click="showCreateClassroomModal = true"
                                class="bg-indigo-600 hover:bg-indigo-700"
                                :disabled="isViewingArchived"
                                :title="isViewingArchived ? 'Cannot create classrooms while viewing archived data' : ''" />
                        </div>
                        
                        <DataTable :value="classrooms" :loading="isLoadingClassrooms" paginator :rows="10"
                            class="p-datatable-sm" stripedRows>
                            <Column field="name" header="Classroom" sortable />
                            <Column field="school_year" header="School Year" sortable />
                            <Column field="class_code" header="Class Code">
                                <template #body="{ data }">
                                    <code class="bg-gray-100 px-2 py-1 rounded text-sm">{{ data.class_code }}</code>
                                </template>
                            </Column>
                            <Column header="Teacher">
                                <template #body="{ data }">
                                    <span v-if="data.teacher" class="text-green-600">{{ data.teacher.name }}</span>
                                    <span v-else class="text-gray-400">Not assigned</span>
                                </template>
                            </Column>
                            <Column field="student_count" header="Students" />
                            <Column header="Actions">
                                <template #body="{ data }">
                                    <div class="flex gap-1">
                                        <Button v-if="!isViewingArchived" icon="pi pi-pencil" size="small" severity="info" text
                                            @click="openEditClassroomModal(data)" title="Edit" />
                                        <Button v-if="!isViewingArchived && data.student_count === 0" icon="pi pi-trash" size="small" severity="danger" text
                                            @click="openDeleteClassroomModal(data)" title="Delete" />
                                    </div>
                                </template>
                            </Column>
                        </DataTable>
                    </div>
                </TabPanel>

                <!-- School Years Tab -->
                <TabPanel header="School Years">
                    <div class="p-4">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-semibold">Manage School Years</h3>
                            <Button v-if="!isViewingArchived" label="New School Year" icon="pi pi-plus" @click="showCreateSchoolYearModal = true"
                                class="bg-indigo-600 hover:bg-indigo-700" />
                        </div>
                        
                        <DataTable :value="schoolYears" :loading="isLoadingSchoolYears" class="p-datatable-sm" stripedRows>
                            <Column field="name" header="School Year" sortable />
                            <Column header="Status">
                                <template #body="{ data }">
                                    <span v-if="data.is_current" class="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-medium">
                                        Current
                                    </span>
                                    <span v-else-if="data.is_archived" class="bg-gray-100 text-gray-600 px-2 py-1 rounded-full text-xs font-medium">
                                        Archived
                                    </span>
                                </template>
                            </Column>
                            <Column field="classrooms_count" header="Classrooms" />
                            <Column field="teachers_count" header="Teachers" />
                            <Column field="students_count" header="Students" />
                            <Column header="Actions">
                                <template #body="{ data }">
                                    <div class="flex items-center gap-1">
                                        <Button v-if="data.is_archived" label="View" size="small" severity="info"
                                            icon="pi pi-eye" @click="viewArchivedSchoolYear(data)" />
                                        <Button v-if="data.is_current && !isViewingArchived" label="Archive" size="small" severity="warning"
                                            @click="openArchiveConfirmModal(data)" />
                                        <Button v-if="!data.is_archived && !isViewingArchived" icon="pi pi-pencil" size="small" severity="secondary" text rounded
                                            @click="openEditSchoolYearModal(data)" title="Edit Name" />
                                        <Button v-if="!data.is_current && data.classrooms_count === 0 && !isViewingArchived" 
                                            icon="pi pi-trash" size="small" severity="danger" text rounded
                                            @click="openDeleteSchoolYearModal(data)" title="Delete" />
                                    </div>
                                </template>
                            </Column>
                        </DataTable>
                    </div>
                </TabPanel>

                <!-- Alumni & Retired Tab -->
                <TabPanel header="Alumni & Retired">
                    <div class="p-4">
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex items-center gap-4">
                                <Dropdown v-model="archivedUserRoleFilter" :options="[{label: 'All', value: 'all'}, ...roleOptions]" 
                                    optionLabel="label" optionValue="value"
                                    @change="loadArchivedUsers" class="w-40" />
                                <InputText v-model="archivedUserSearch" placeholder="Search archived users..." 
                                    @keyup.enter="loadArchivedUsers" class="w-64" />
                                <Button label="Search" icon="pi pi-search" @click="loadArchivedUsers" />
                            </div>
                        </div>
                        
                        <DataTable :value="archivedUsers" :loading="isLoadingArchivedUsers" paginator :rows="10"
                            class="p-datatable-sm" stripedRows>
                            <Column field="id_number" header="ID Number" sortable />
                            <Column field="name" header="Name" sortable />
                            <Column field="email" header="Email" sortable />
                            <Column field="role" header="Role" sortable>
                                <template #body="{ data }">
                                    <span :class="data.role === 'teacher' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'"
                                        class="px-2 py-1 rounded-full text-xs font-medium capitalize">
                                        {{ data.role }}
                                    </span>
                                </template>
                            </Column>
                            <Column field="archived_reason" header="Status" sortable>
                                <template #body="{ data }">
                                    <span class="bg-amber-100 text-amber-700 px-2 py-1 rounded-full text-xs font-medium">
                                        {{ data.archived_reason }}
                                    </span>
                                </template>
                            </Column>
                            <Column header="Archived Date" sortable>
                                <template #body="{ data }">
                                    <span class="text-gray-600 text-sm">
                                        {{ data.archived_at ? new Date(data.archived_at).toLocaleDateString() : '-' }}
                                    </span>
                                </template>
                            </Column>
                            <Column header="Actions">
                                <template #body="{ data }">
                                    <div class="flex gap-1">
                                        <Button icon="pi pi-replay" size="small" severity="success" text
                                            @click="openRestoreUserModal(data)" title="Restore User" />
                                    </div>
                                </template>
                            </Column>
                        </DataTable>
                    </div>
                </TabPanel>
                
                <!-- Password Recovery Tab -->
                <TabPanel header="Password Recovery">
                    <div class="p-4">
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex items-center gap-4">
                                <Dropdown v-model="recoveryStatusFilter" :options="[
                                    {label: 'All', value: 'all'},
                                    {label: 'Pending', value: 'pending'},
                                    {label: 'Approved', value: 'approved'},
                                    {label: 'Rejected', value: 'rejected'}
                                ]" 
                                    optionLabel="label" optionValue="value"
                                    @change="loadRecoveryRequests" class="w-40" />
                                <Button label="Refresh" icon="pi pi-refresh" @click="loadRecoveryRequests" />
                            </div>
                        </div>
                        
                        <DataTable :value="recoveryRequests" :loading="isLoadingRecoveryRequests" paginator :rows="10"
                            class="p-datatable-sm" stripedRows>
                            <Column header="ID Number" sortable>
                                <template #body="{ data }">
                                    {{ data.id_number || data.username }}
                                </template>
                            </Column>
                            <Column field="name" header="Name" sortable />
                            <Column field="email" header="Email" sortable />
                            <Column field="role" header="Role" sortable>
                                <template #body="{ data }">
                                    <span :class="data.role === 'teacher' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'"
                                        class="px-2 py-1 rounded-full text-xs font-medium capitalize">
                                        {{ data.role }}
                                    </span>
                                </template>
                            </Column>
                            <Column field="status" header="Status" sortable>
                                <template #body="{ data }">
                                    <span :class="{
                                        'bg-amber-100 text-amber-700': data.status === 'pending',
                                        'bg-green-100 text-green-700': data.status === 'approved',
                                        'bg-red-100 text-red-700': data.status === 'rejected'
                                    }" class="px-2 py-1 rounded-full text-xs font-medium capitalize">
                                        {{ data.status }}
                                    </span>
                                </template>
                            </Column>
                            <Column header="Requested Date" sortable>
                                <template #body="{ data }">
                                    <span class="text-gray-600 text-sm">
                                        {{ new Date(data.requested_at).toLocaleDateString() }}
                                        <br>
                                        <span class="text-xs text-gray-500">
                                            {{ new Date(data.requested_at).toLocaleTimeString() }}
                                        </span>
                                    </span>
                                </template>
                            </Column>
                            <Column header="ID Verification">
                                <template #body="{ data }">
                                    <Button v-if="data.has_photos" 
                                        icon="pi pi-eye" size="small" severity="info" text
                                        @click="viewIdPhotos(data)" title="View ID Photos" 
                                        label="View Photos" />
                                    <span v-else class="text-xs text-gray-400">No photos</span>
                                </template>
                            </Column>
                            <Column header="Actions">
                                <template #body="{ data }">
                                    <div class="flex gap-1">
                                        <Button v-if="data.status === 'pending'" 
                                            icon="pi pi-check" size="small" severity="success" text
                                            @click="openApproveConfirm(data)" title="Approve Request" />
                                        <Button v-if="data.status === 'pending'" 
                                            icon="pi pi-times" size="small" severity="danger" text
                                            @click="openRejectConfirm(data)" title="Reject Request" />
                                        <span v-if="data.status === 'approved'" class="text-xs text-gray-500">
                                            Approved by {{ data.approved_by }}
                                        </span>
                                    </div>
                                </template>
                            </Column>
                        </DataTable>
                    </div>
                </TabPanel>
            </TabView>
        </div>

        <!-- Create User Modal -->
        <Dialog v-model:visible="showCreateUserModal" modal header="Create New User" :style="{ width: '500px' }">
            <div class="space-y-4 p-2">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Role</label>
                    <Dropdown v-model="newUser.role" :options="roleOptions" optionLabel="label" optionValue="value" 
                        class="w-full" />
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                        <InputText v-model="newUser.first_name" class="w-full" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                        <InputText v-model="newUser.last_name" class="w-full" />
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <InputText v-model="newUser.email" type="email" class="w-full" />
                </div>
                <div v-if="newUser.role === 'student'">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Grade Level</label>
                    <Dropdown v-model="newUser.grade_level" :options="gradeOptions" optionLabel="label" optionValue="value"
                        placeholder="Select grade" class="w-full" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                    <InputText v-model="newUser.password" class="w-full" />
                    <p class="text-xs text-gray-500 mt-1">Default: password123</p>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showCreateUserModal = false" />
                <Button label="Create" @click="createUser" class="bg-indigo-600 hover:bg-indigo-700" />
            </template>
        </Dialog>

        <!-- Create Classroom Modal -->
        <Dialog v-model:visible="showCreateClassroomModal" modal header="Create New Classroom" :style="{ width: '450px' }">
            <div class="space-y-4 p-2">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Grade Level</label>
                    <Dropdown v-model="newClassroom.grade_level" :options="gradeOptions" optionLabel="label" optionValue="value"
                        placeholder="Select grade" class="w-full" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Section</label>
                    <Dropdown v-model="newClassroom.section" :options="sectionOptions" optionLabel="label" optionValue="value"
                        placeholder="Select section" class="w-full" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Assign Teacher (Optional)</label>
                    <Dropdown v-model="newClassroom.teacher_id" :options="teachersList" optionLabel="name" optionValue="id"
                        placeholder="Select teacher" class="w-full" showClear />
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showCreateClassroomModal = false" />
                <Button label="Create" @click="createClassroom" class="bg-indigo-600 hover:bg-indigo-700" />
            </template>
        </Dialog>

        <!-- Create School Year Modal -->
        <Dialog v-model:visible="showCreateSchoolYearModal" modal header="Start New School Year" :style="{ width: '450px' }">
            <div class="space-y-4 p-2">
                <div class="p-4 bg-amber-50 border border-amber-200 rounded-lg">
                    <p class="text-amber-800 text-sm">
                        <i class="pi pi-exclamation-triangle mr-2"></i>
                        Starting a new school year will archive the current one and unassign all students.
                    </p>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">School Year Name</label>
                    <InputText v-model="newSchoolYear.name" placeholder="e.g., 2025-2026" class="w-full" />
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showCreateSchoolYearModal = false" />
                <Button label="Confirm" @click="createSchoolYear" class="bg-amber-500 hover:bg-amber-600" />
            </template>
        </Dialog>

        <!-- Assign Teacher Modal -->
        <Dialog v-model:visible="showAssignTeacherModal" modal header="Assign Teacher" :style="{ width: '400px' }">
            <div class="space-y-4 p-2">
                <p class="text-gray-600">
                    Assign a teacher to <strong>{{ selectedClassroom?.name }}</strong>
                </p>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Select Teacher</label>
                    <Dropdown v-model="selectedTeacherId" :options="teachersList" optionLabel="name" optionValue="id"
                        placeholder="Select teacher" class="w-full" showClear />
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showAssignTeacherModal = false" />
                <Button label="Assign" @click="assignTeacher" class="bg-indigo-600 hover:bg-indigo-700" />
            </template>
        </Dialog>

        <!-- Archive School Year Confirmation Modal -->
        <Dialog v-model:visible="showArchiveConfirmModal" modal header="Archive School Year" :style="{ width: '450px' }">
            <div class="space-y-4 p-2">
                <div class="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                    <i class="pi pi-exclamation-triangle text-2xl text-amber-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">Are you sure you want to archive this school year?</p>
                        <p class="text-gray-600 text-sm mt-2">
                            School Year: <strong class="text-amber-700">{{ schoolYearToArchive?.name }}</strong>
                        </p>
                        <p class="text-amber-700 text-sm mt-2">
                            <i class="pi pi-info-circle mr-1"></i>
                            This will archive all classrooms and unassign all students from this school year.
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showArchiveConfirmModal = false" />
                <Button label="Archive" severity="warning" @click="archiveSchoolYear" icon="pi pi-archive" />
            </template>
        </Dialog>

        <!-- Edit User Modal -->
        <Dialog v-model:visible="showEditUserModal" modal header="Edit User" :style="{ width: '500px' }">
            <div class="space-y-4 p-2">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                        <InputText v-model="editUser.first_name" class="w-full" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                        <InputText v-model="editUser.last_name" class="w-full" />
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <InputText v-model="editUser.email" type="email" class="w-full" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">New Password (leave blank to keep current)</label>
                    <InputText v-model="editUser.password" type="password" class="w-full" placeholder="Enter new password" />
                </div>
                <div class="flex items-center gap-2">
                    <input type="checkbox" v-model="editUser.is_active" id="userActive" class="rounded" />
                    <label for="userActive" class="text-sm text-gray-700">Active</label>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showEditUserModal = false" />
                <Button label="Save" @click="updateUser" class="bg-indigo-600 hover:bg-indigo-700" />
            </template>
        </Dialog>

        <!-- Delete User Confirmation Modal -->
        <Dialog v-model:visible="showDeleteUserModal" modal header="Delete User" :style="{ width: '400px' }">
            <div class="space-y-4 p-2">
                <div class="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <i class="pi pi-exclamation-triangle text-2xl text-red-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">Are you sure you want to delete this user?</p>
                        <p class="text-gray-600 text-sm mt-2">
                            User: <strong class="text-red-700">{{ selectedUser?.name }}</strong>
                        </p>
                        <p class="text-red-700 text-sm mt-2">
                            <i class="pi pi-info-circle mr-1"></i>
                            This action cannot be undone.
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showDeleteUserModal = false" />
                <Button label="Delete" severity="danger" @click="deleteUser" icon="pi pi-trash" />
            </template>
        </Dialog>

        <!-- Archive User Modal -->
        <Dialog v-model:visible="showArchiveUserModal" modal header="Archive User" :style="{ width: '500px' }">
            <div class="space-y-4 p-2">
                <div class="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                    <i class="pi pi-info-circle text-2xl text-amber-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">Archive this user?</p>
                        <p class="text-gray-600 text-sm mt-2">
                            User: <strong class="text-amber-700">{{ userToArchive?.name }}</strong>
                        </p>
                        <p class="text-amber-700 text-sm mt-2">
                            <i class="pi pi-info-circle mr-1"></i>
                            This will move the user to Alumni & Retired. You can restore them later if needed.
                        </p>
                    </div>
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Reason *</label>
                    <Dropdown v-model="archiveUserData.reason" :options="archiveReasonOptions" 
                        optionLabel="label" optionValue="value"
                        placeholder="Select reason" class="w-full" />
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showArchiveUserModal = false" />
                <Button label="Archive" severity="warning" @click="archiveUser" icon="pi pi-archive" />
            </template>
        </Dialog>

        <!-- Restore User Modal -->
        <Dialog v-model:visible="showRestoreUserModal" modal header="Restore User" :style="{ width: '450px' }">
            <div class="space-y-4 p-2">
                <div class="flex items-start gap-3 p-4 bg-green-50 border border-green-200 rounded-lg">
                    <i class="pi pi-check-circle text-2xl text-green-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">Restore this user to active status?</p>
                        <p class="text-gray-600 text-sm mt-2">
                            User: <strong class="text-green-700">{{ userToRestore?.name }}</strong>
                        </p>
                        <p class="text-green-700 text-sm mt-2">
                            <i class="pi pi-info-circle mr-1"></i>
                            This will move the user back to the active users list.
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showRestoreUserModal = false" />
                <Button label="Restore" severity="success" @click="restoreUser" icon="pi pi-replay" />
            </template>
        </Dialog>

        <!-- Edit Classroom Modal -->
        <Dialog v-model:visible="showEditClassroomModal" modal header="Edit Classroom" :style="{ width: '450px' }">
            <div class="space-y-4 p-2">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Grade Level</label>
                    <Dropdown v-model="editClassroom.grade_level" :options="gradeOptions" optionLabel="label" optionValue="value"
                        placeholder="Select grade" class="w-full" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Section</label>
                    <Dropdown v-model="editClassroom.section" :options="sectionOptions" optionLabel="label" optionValue="value"
                        placeholder="Select section" class="w-full" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Assign Teacher</label>
                    <Dropdown v-model="editClassroom.teacher_id" :options="teachersList" optionLabel="name" optionValue="id"
                        placeholder="Select teacher" class="w-full" showClear />
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showEditClassroomModal = false" />
                <Button label="Save" @click="updateClassroom" class="bg-indigo-600 hover:bg-indigo-700" />
            </template>
        </Dialog>

        <!-- Delete Classroom Confirmation Modal -->
        <Dialog v-model:visible="showDeleteClassroomModal" modal header="Delete Classroom" :style="{ width: '400px' }">
            <div class="space-y-4 p-2">
                <div class="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <i class="pi pi-exclamation-triangle text-2xl text-red-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">Are you sure you want to delete this classroom?</p>
                        <p class="text-gray-600 text-sm mt-2">
                            Classroom: <strong class="text-red-700">{{ selectedClassroomForEdit?.name }}</strong>
                        </p>
                        <p class="text-red-700 text-sm mt-2">
                            <i class="pi pi-info-circle mr-1"></i>
                            This action cannot be undone.
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showDeleteClassroomModal = false" />
                <Button label="Delete" severity="danger" @click="deleteClassroom" icon="pi pi-trash" />
            </template>
        </Dialog>

        <!-- Edit School Year Modal -->
        <Dialog v-model:visible="showEditSchoolYearModal" modal header="Edit School Year" :style="{ width: '400px' }">
            <div class="space-y-4 p-2">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">School Year Name</label>
                    <InputText v-model="editSchoolYear.name" placeholder="e.g., 2025-2026" class="w-full" />
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showEditSchoolYearModal = false" />
                <Button label="Save" @click="updateSchoolYear" class="bg-indigo-600 hover:bg-indigo-700" />
            </template>
        </Dialog>

        <!-- Delete School Year Confirmation Modal -->
        <Dialog v-model:visible="showDeleteSchoolYearModal" modal header="Delete School Year" :style="{ width: '400px' }">
            <div class="space-y-4 p-2">
                <div class="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <i class="pi pi-exclamation-triangle text-2xl text-red-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">Are you sure you want to delete this school year?</p>
                        <p class="text-gray-600 text-sm mt-2">
                            School Year: <strong class="text-red-700">{{ selectedSchoolYear?.name }}</strong>
                        </p>
                        <p class="text-red-700 text-sm mt-2">
                            <i class="pi pi-info-circle mr-1"></i>
                            This action cannot be undone.
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showDeleteSchoolYearModal = false" />
                <Button label="Delete" severity="danger" @click="deleteSchoolYear" icon="pi pi-trash" />
            </template>
        </Dialog>

        <!-- ID Photo Viewing Modal -->
        <Dialog v-model:visible="showPhotoModal" modal header="ID Verification" :style="{ width: '800px' }">
            <div v-if="selectedRecoveryRequest" class="space-y-4 p-2">
                <!-- User Information -->
                <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <h4 class="font-semibold text-gray-900 mb-2">Student Information</h4>
                    <div class="grid grid-cols-2 gap-2 text-sm">
                        <div>
                            <span class="text-gray-600">Name:</span>
                            <span class="ml-2 font-medium">{{ selectedRecoveryRequest.name }}</span>
                        </div>
                        <div>
                            <span class="text-gray-600">Role:</span>
                            <span class="ml-2 font-medium capitalize">{{ selectedRecoveryRequest.role }}</span>
                        </div>
                        <div>
                            <span class="text-gray-600">ID Number:</span>
                            <span class="ml-2 font-medium">{{ selectedRecoveryRequest.id_number || selectedRecoveryRequest.username }}</span>
                        </div>
                        <div>
                            <span class="text-gray-600">Email:</span>
                            <span class="ml-2 font-medium">{{ selectedRecoveryRequest.email }}</span>
                        </div>
                    </div>
                </div>

                <!-- ID Photos -->
                <div class="space-y-4">
                    <!-- Front Photo -->
                    <div>
                        <h4 class="font-semibold text-gray-900 mb-2 flex items-center gap-2">
                            <i class="pi pi-image"></i>
                            Front of ID
                        </h4>
                        <div v-if="selectedRecoveryRequest.id_photo_front_url" 
                            class="border-2 border-gray-300 rounded-lg overflow-hidden bg-gray-50 flex items-center justify-center"
                            style="max-height: 300px;">
                            <img :src="selectedRecoveryRequest.id_photo_front_url" 
                                alt="Front of ID" 
                                class="max-h-[300px] w-auto object-contain" />
                        </div>
                        <p v-else class="text-gray-500 text-sm italic">No front photo available</p>
                    </div>

                    <!-- Back Photo -->
                    <div>
                        <h4 class="font-semibold text-gray-900 mb-2 flex items-center gap-2">
                            <i class="pi pi-image"></i>
                            Back of ID
                        </h4>
                        <div v-if="selectedRecoveryRequest.id_photo_back_url" 
                            class="border-2 border-gray-300 rounded-lg overflow-hidden bg-gray-50 flex items-center justify-center"
                            style="max-height: 300px;">
                            <img :src="selectedRecoveryRequest.id_photo_back_url" 
                                alt="Back of ID" 
                                class="max-h-[300px] w-auto object-contain" />
                        </div>
                        <p v-else class="text-gray-500 text-sm italic">No back photo available</p>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Close" @click="showPhotoModal = false" />
            </template>
        </Dialog>

        <!-- Approve Confirmation Dialog -->
        <Dialog v-model:visible="showApproveConfirmModal" modal header="Approve Password Recovery" :style="{ width: '450px' }">
            <div v-if="requestToApprove" class="space-y-4 p-2">
                <div class="flex items-start gap-3 p-4 bg-green-50 border border-green-200 rounded-lg">
                    <i class="pi pi-check-circle text-2xl text-green-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">Approve password recovery for {{ requestToApprove.name }}?</p>
                        <p class="text-gray-600 text-sm mt-2">
                            Their password will be reset to <span class="font-mono font-bold">"password123"</span>
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showApproveConfirmModal = false" />
                <Button label="Approve" severity="success" @click="approveRecoveryRequest" icon="pi pi-check" />
            </template>
        </Dialog>

        <!-- Reject Confirmation Dialog -->
        <Dialog v-model:visible="showRejectConfirmModal" modal header="Reject Password Recovery" :style="{ width: '450px' }">
            <div v-if="requestToReject" class="space-y-4 p-2">
                <div class="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <i class="pi pi-times-circle text-2xl text-red-600"></i>
                    <div>
                        <p class="text-gray-800 font-medium">Reject password recovery request from {{ requestToReject.name }}?</p>
                        <p class="text-gray-600 text-sm mt-2">
                            The user will be notified that their request was rejected.
                        </p>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" severity="secondary" @click="showRejectConfirmModal = false" />
                <Button label="Reject" severity="danger" @click="rejectRecoveryRequest" icon="pi pi-times" />
            </template>
        </Dialog>
    </div>
</template>
