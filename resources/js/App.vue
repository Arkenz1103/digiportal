<template>
  <div id="app">
    <!-- Toast Notification Component -->
    <Toast position="top-right" />
    
    <!-- Debug info -->
    <div v-if="false" class="fixed top-0 right-0 bg-red-500 text-white p-2 z-50">
      Current Page: {{ currentPage }}
    </div>
    <!-- Landing Page -->
    <Landing v-if="currentPage === 'Landing'" @navigate="handleNavigation" />
    
    <!-- Login Page -->
    <AuthLogin v-if="currentPage === 'Login'" @navigate="handleNavigation" />
    
    <!-- Teacher Pages with MainLayout -->
    <MainLayout v-if="currentPage.startsWith('Teacher') || (currentPage === 'Profile' && userRole === 'teacher') || (currentPage === 'Settings' && userRole === 'teacher')" @navigate="handleNavigation">
      <TeacherHome v-if="currentPage === 'TeacherHome'" @navigate="handleNavigation" />
      <TeacherClassroom v-if="currentPage === 'TeacherClassroom'" @navigate="handleNavigation" />
      <TeacherRoom v-if="currentPage === 'TeacherRoom'" @navigate="handleNavigation" />
      <TeacherOutputs v-if="currentPage === 'TeacherOutputs'" @navigate="handleNavigation" />
      <TeacherSprogress v-if="currentPage === 'TeacherSprogress'" @navigate="handleNavigation" />
      <TeacherProgress v-if="currentPage === 'TeacherProgress'" @navigate="handleNavigation" />
      <TeacherRemarks v-if="currentPage === 'TeacherRemarks'" @navigate="handleNavigation" />
      <TeacherNotice v-if="currentPage === 'TeacherNotice'" @navigate="handleNavigation" />
      <TeacherNotify v-if="currentPage === 'TeacherNotify'" @navigate="handleNavigation" />
      <TeacherArchived v-if="currentPage === 'TeacherArchived'" @navigate="handleNavigation" />
      <TeacherProfile v-if="currentPage === 'Profile' && userRole === 'teacher'" @navigate="handleNavigation" />
      <TeacherSettings v-if="currentPage === 'Settings' && userRole === 'teacher'" @navigate="handleNavigation" />
    </MainLayout>
    
    <!-- Student Pages with MainLayout -->
    <MainLayout v-if="currentPage.startsWith('Student') || (currentPage === 'Profile' && userRole === 'student') || (currentPage === 'Settings' && userRole === 'student')" @navigate="handleNavigation">
      <StudentNewsfeed v-if="currentPage === 'StudentNewsfeed'" @navigate="handleNavigation" />
      <StudentClassroom v-if="currentPage === 'StudentClassroom'" @navigate="handleNavigation" />
      <StudentRoom v-if="currentPage === 'StudentRoom'" @navigate="handleNavigation" />
      <StudentSketch v-if="currentPage === 'StudentSketch'" @navigate="handleNavigation" />
      <StudentRemarked v-if="currentPage === 'StudentRemarked'" @navigate="handleNavigation" />
      <StudentNotify v-if="currentPage === 'StudentNotify'" @navigate="handleNavigation" />
      <StudentArchived v-if="currentPage === 'StudentArchived'" @navigate="handleNavigation" />
      <StudentProfile v-if="currentPage === 'Profile' && userRole === 'student'" @navigate="handleNavigation" />
      <StudentSettings v-if="currentPage === 'Settings' && userRole === 'student'" @navigate="handleNavigation" />
    </MainLayout>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Toast from 'primevue/toast'
import Landing from './Pages/Landing.vue'
import AuthLogin from './Pages/Auth/Login.vue'
import MainLayout from './Layouts/MainLayout.vue'

// Teacher components
import TeacherHome from './Pages/Teacher/Home.vue'
import TeacherClassroom from './Pages/Teacher/Classroom.vue'
import TeacherRoom from './Pages/Teacher/Room.vue'
import TeacherOutputs from './Pages/Teacher/Outputs.vue'
import TeacherSprogress from './Pages/Teacher/Sprogress.vue'
import TeacherProgress from './Pages/Teacher/Progress.vue'
import TeacherRemarks from './Pages/Teacher/Remarks.vue'
import TeacherNotice from './Pages/Teacher/Notice.vue'
import TeacherNotify from './Pages/Teacher/Notify.vue'
import TeacherArchived from './Pages/Teacher/Archived.vue'
import TeacherProfile from './Pages/Teacher/Profile.vue'
import TeacherSettings from './Pages/Teacher/Settings.vue'

// Student components
import StudentNewsfeed from './Pages/Student/Newsfeed.vue'
import StudentClassroom from './Pages/Student/Classroom.vue'
import StudentRoom from './Pages/Student/Sroom.vue'
import StudentSketch from './Pages/Student/Sketch.vue'
import StudentRemarked from './Pages/Student/Sremarked.vue'
import StudentNotify from './Pages/Student/Snotify.vue'
import StudentArchived from './Pages/Student/Sarchived.vue'
import StudentProfile from './Pages/Student/Profile.vue'
import StudentSettings from './Pages/Student/Settings.vue'

// Current page state - using route names from routes.js
const currentPage = ref('Landing')
const isLoggedIn = ref(false)
const userRole = ref(null)

// Handle navigation between pages
const handleNavigation = (page) => {
  console.log('Navigating to:', page);
  
  // 🔒 SECURITY: Prevent role-based unauthorized access
  const currentRole = userRole.value || localStorage.getItem('digiportal_user_role');
  
  // Block students from accessing teacher pages
  if (currentRole === 'student' && page.startsWith('Teacher')) {
    console.warn('🚫 Access Denied: Students cannot access teacher pages');
    alert('Access Denied: You do not have permission to view this page.');
    return; // Don't navigate
  }
  
  // Block teachers from accessing student pages
  if (currentRole === 'teacher' && page.startsWith('Student')) {
    console.warn('🚫 Access Denied: Teachers cannot access student pages');
    alert('Access Denied: You do not have permission to view this page.');
    return; // Don't navigate
  }
  
  currentPage.value = page
  
  // Save current page and login state to localStorage
  if (page.startsWith('Teacher') || page.startsWith('Student')) {
    isLoggedIn.value = true
    userRole.value = page.startsWith('Teacher') ? 'teacher' : 'student'
    localStorage.setItem('digiportal_logged_in', 'true')
    localStorage.setItem('digiportal_user_role', userRole.value)
    localStorage.setItem('digiportal_current_page', page)
  } else if (page === 'Landing' || page === 'Login') {
    // Only clear session if explicitly going to Landing or Login
    if (page === 'Landing') {
      isLoggedIn.value = false
      userRole.value = null
      localStorage.removeItem('digiportal_logged_in')
      localStorage.removeItem('digiportal_user_role')
      localStorage.removeItem('digiportal_current_page')
    }
  }
  
  // Update document title based on page
  const titles = {
    'Landing': 'DigiPortal | Digital Portfolio & Learning Management',
    'Login': 'Sign In | DigiPortal',
    'TeacherHome': 'Dashboard | DigiPortal Teacher',
    'TeacherClassroom': 'My Classroom | DigiPortal',
    'TeacherRoom': 'Classroom Management | DigiPortal',
    'TeacherOutputs': 'Student Submissions | DigiPortal',
    'TeacherSprogress': 'Progress Tracking | DigiPortal',
    'TeacherProgress': 'Student Analytics | DigiPortal',
    'TeacherRemarks': 'Feedback & Remarks | DigiPortal',
    'TeacherNotice': 'Announcements | DigiPortal',
    'TeacherNotify': 'Notifications | DigiPortal',
    'TeacherArchived': 'Archive | DigiPortal',
    'Profile': 'My Profile | DigiPortal',
    'Settings': 'Account Settings | DigiPortal',
    'StudentNewsfeed': 'Home | DigiPortal Student',
    'StudentClassroom': 'My Classes | DigiPortal',
    'StudentRoom': 'Classroom | DigiPortal',
    'StudentSketch': 'Creative Studio | DigiPortal',
    'StudentRemarked': 'Teacher Feedback | DigiPortal',
    'StudentNotify': 'Notifications | DigiPortal',
    'StudentArchived': 'Archive | DigiPortal'
  }
  
  document.title = titles[page] || 'DigiPortal | Digital Learning Platform'
  
  // Update URL to match current page (role-based for Profile/Settings)
  const urlMap = {
    'Landing': '/',
    'Login': '/login',
    'TeacherHome': '/teacher/home',
    'TeacherClassroom': '/teacher/classroom',
    'TeacherRoom': '/teacher/room',
    'TeacherOutputs': '/teacher/outputs',
    'TeacherSprogress': '/teacher/sprogress',
    'TeacherProgress': '/teacher/progress',
    'TeacherRemarks': '/teacher/remarks',
    'TeacherNotice': '/teacher/notice',
    'TeacherNotify': '/teacher/notify',
    'TeacherArchived': '/teacher/archived',
    'StudentNewsfeed': '/student/newsfeed',
    'StudentClassroom': '/student/classroom',
    'StudentRoom': '/student/room',
    'StudentSketch': '/student/sketch',
    'StudentRemarked': '/student/remarked',
    'StudentNotify': '/student/notify',
    'StudentArchived': '/student/archived'
  }
  
  // Handle Profile and Settings based on role
  let newUrl = urlMap[page]
  if (page === 'Profile') {
    newUrl = userRole.value === 'teacher' ? '/teacher/profile' : '/student/profile'
  } else if (page === 'Settings') {
    newUrl = userRole.value === 'teacher' ? '/teacher/settings' : '/student/settings'
  }
  
  newUrl = newUrl || '/'
  if (window.location.pathname !== newUrl) {
    window.history.pushState({}, '', newUrl)
  }
}

// Check for existing session on app load
onMounted(() => {
  const savedLoggedIn = localStorage.getItem('digiportal_logged_in')
  const savedUserRole = localStorage.getItem('digiportal_user_role')
  const savedCurrentPage = localStorage.getItem('digiportal_current_page')
  const currentPath = window.location.pathname
  
  console.log('App mounted - saved data:', { savedLoggedIn, savedUserRole, savedCurrentPage, currentPath });
  
  // 🔒 SECURITY: Check if user is trying to access unauthorized URL
  if (savedLoggedIn === 'true' && savedUserRole) {
    // Block students from accessing teacher URLs
    if (savedUserRole === 'student' && currentPath.startsWith('/teacher')) {
      console.warn('🚫 Access Denied: Student trying to access teacher URL:', currentPath);
      alert('Access Denied: You do not have permission to view this page.');
      window.location.href = '/student/newsfeed';
      return;
    }
    
    // Block teachers from accessing student URLs  
    if (savedUserRole === 'teacher' && currentPath.startsWith('/student')) {
      console.warn('🚫 Access Denied: Teacher trying to access student URL:', currentPath);
      alert('Access Denied: You do not have permission to view this page.');
      window.location.href = '/teacher/home';
      return;
    }
  }
  
  if (savedLoggedIn === 'true' && savedUserRole && savedCurrentPage) {
    isLoggedIn.value = true
    userRole.value = savedUserRole
    currentPage.value = savedCurrentPage
    console.log('Restored session - currentPage:', currentPage.value);
    
    // Update document title
    const titles = {
      'TeacherHome': 'Dashboard | DigiPortal Teacher',
      'TeacherRoom': 'Classroom Management | DigiPortal',
      'TeacherOutputs': 'Student Submissions | DigiPortal',
      'TeacherSprogress': 'Progress Tracking | DigiPortal',
      'TeacherProgress': 'Student Analytics | DigiPortal',
      'TeacherRemarks': 'Feedback & Remarks | DigiPortal',
      'TeacherNotice': 'Announcements | DigiPortal',
      'TeacherNotify': 'Notifications | DigiPortal',
      'TeacherArchived': 'Archive | DigiPortal',
      'Profile': 'My Profile | DigiPortal',
      'Settings': 'Account Settings | DigiPortal',
      'StudentNewsfeed': 'Home | DigiPortal Student',
      'StudentRoom': 'Classroom | DigiPortal',
      'StudentSketch': 'Creative Studio | DigiPortal',
      'StudentNotify': 'Notifications | DigiPortal',
      'StudentArchived': 'Archive | DigiPortal'
    }
    document.title = titles[savedCurrentPage] || 'DigiPortal | Digital Learning Platform'
  }
})

// Make navigation function globally available
window.navigateTo = handleNavigation
</script>

<style>
/* Global styles can be added here if needed */
</style>
