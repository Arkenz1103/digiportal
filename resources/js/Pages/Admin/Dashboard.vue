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
const userRoleFilter = ref(null);
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
        if (userRoleFilter.value) params.append('role', userRoleFilter.value);
        if (userSearch.value) params.append('search', userSearch.value);
        if (schoolYearName) params.append('school_year', schoolYearName);
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

onMounted(() => {
    loadDashboard();
    loadUsers();
    loadClassrooms();
    loadSchoolYears();
    loadTeachers();
});
</script>

<template>
    <div class="min-h-screen bg-gray-100">
        <!-- Header -->
        <div class="text-white py-6 px-8" :class="isViewingArchived ? 'bg-amber-600' : 'bg-indigo-700'">
            <div class="max-w-7xl mx-auto flex items-center justify-between">
                <div>
                    <h1 class="text-3xl font-bold">Admin Dashboard</h1>
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
                        :class="isViewingArchived ? 'bg-amber-700 hover:bg-amber-800 border-amber-700' : 'bg-indigo-800 hover:bg-indigo-900 border-indigo-800'" />
                </div>
            </div>
        </div>

        <div class="max-w-7xl mx-auto px-8 py-6">
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
                                <Dropdown v-model="userRoleFilter" :options="[{label: 'All', value: null}, ...roleOptions]" 
                                    optionLabel="label" optionValue="value" placeholder="Filter by role"
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
                        </DataTable>
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
                                    <Button label="Assign Teacher" size="small" severity="secondary"
                                        @click="openAssignTeacherModal(data)" />
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
                                    <div class="flex gap-2">
                                        <Button v-if="data.is_archived" label="View" size="small" severity="info"
                                            icon="pi pi-eye" @click="viewArchivedSchoolYear(data)" />
                                        <Button v-if="data.is_current && !isViewingArchived" label="Archive" size="small" severity="warning"
                                            @click="openArchiveConfirmModal(data)" />
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
                <Button label="Start New Year" @click="createSchoolYear" class="bg-amber-500 hover:bg-amber-600" />
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
    </div>
</template>
