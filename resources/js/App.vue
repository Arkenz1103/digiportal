<template>
  <div id="app">
    <!-- Debug info -->
    <div v-if="false" class="fixed top-0 right-0 bg-red-500 text-white p-2 z-50">
      Current Page: {{ currentPage }}
    </div>
    <!-- Landing Page -->
    <Landing v-if="currentPage === 'Landing'" @navigate="handleNavigation" />
    
    <!-- Login Page -->
    <AuthLogin v-if="currentPage === 'Login'" @navigate="handleNavigation" />
    
    <!-- Teacher Pages with MainLayout -->
    <MainLayout v-if="currentPage.startsWith('Teacher')" @navigate="handleNavigation">
      <TeacherHome v-if="currentPage === 'TeacherHome'" @navigate="handleNavigation" />
      <TeacherRoom v-if="currentPage === 'TeacherRoom'" @navigate="handleNavigation" />
      <TeacherOutputs v-if="currentPage === 'TeacherOutputs'" @navigate="handleNavigation" />
      <TeacherSprogress v-if="currentPage === 'TeacherSprogress'" @navigate="handleNavigation" />
      <TeacherProgress v-if="currentPage === 'TeacherProgress'" @navigate="handleNavigation" />
      <TeacherRemarks v-if="currentPage === 'TeacherRemarks'" @navigate="handleNavigation" />
      <TeacherNotice v-if="currentPage === 'TeacherNotice'" @navigate="handleNavigation" />
      <TeacherNotify v-if="currentPage === 'TeacherNotify'" @navigate="handleNavigation" />
      <TeacherArchived v-if="currentPage === 'TeacherArchived'" @navigate="handleNavigation" />
    </MainLayout>
    
    <!-- Student Pages with MainLayout -->
    <MainLayout v-if="currentPage.startsWith('Student')" @navigate="handleNavigation">
      <StudentNewsfeed v-if="currentPage === 'StudentNewsfeed'" @navigate="handleNavigation" />
      <StudentRoom v-if="currentPage === 'StudentRoom'" @navigate="handleNavigation" />
      <StudentSketch v-if="currentPage === 'StudentSketch'" @navigate="handleNavigation" />
      <StudentNotify v-if="currentPage === 'StudentNotify'" @navigate="handleNavigation" />
      <StudentArchived v-if="currentPage === 'StudentArchived'" @navigate="handleNavigation" />
    </MainLayout>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Landing from './Pages/Landing.vue'
import AuthLogin from './Pages/Auth/Login.vue'
import MainLayout from './Layouts/MainLayout.vue'

// Teacher components
import TeacherHome from './Pages/Teacher/Home.vue'
import TeacherRoom from './Pages/Teacher/Room.vue'
import TeacherOutputs from './Pages/Teacher/Outputs.vue'
import TeacherSprogress from './Pages/Teacher/Sprogress.vue'
import TeacherProgress from './Pages/Teacher/Progress.vue'
import TeacherRemarks from './Pages/Teacher/Remarks.vue'
import TeacherNotice from './Pages/Teacher/Notice.vue'
import TeacherNotify from './Pages/Teacher/Notify.vue'
import TeacherArchived from './Pages/Teacher/Archived.vue'

// Student components
import StudentNewsfeed from './Pages/Student/Newsfeed.vue'
import StudentRoom from './Pages/Student/Sroom.vue'
import StudentSketch from './Pages/Student/Sketch.vue'
import StudentNotify from './Pages/Student/Snotify.vue'
import StudentArchived from './Pages/Student/Sarchived.vue'

// Current page state - using route names from routes.js
const currentPage = ref('Landing')
const isLoggedIn = ref(false)
const userRole = ref(null)

// Handle navigation between pages
const handleNavigation = (page) => {
  console.log('Navigating to:', page);
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
    'Landing': 'DigiPortal - Creative Learning Platform',
    'Login': 'Login - DigiPortal',
    'TeacherHome': 'Teacher Home - DigiPortal',
    'TeacherRoom': 'Class Room - DigiPortal',
    'TeacherOutputs': 'Student Outputs - DigiPortal',
    'TeacherSprogress': 'Special Progress - DigiPortal',
    'TeacherProgress': 'Student Progress - DigiPortal',
    'TeacherRemarks': 'Remarks - DigiPortal',
    'TeacherNotice': 'Notices - DigiPortal',
    'TeacherNotify': 'Notifications - DigiPortal',
    'TeacherArchived': 'Archived - DigiPortal',
    'StudentNewsfeed': 'Student Home - DigiPortal',
    'StudentRoom': 'Class Room - DigiPortal',
    'StudentSketch': 'Sketch - DigiPortal',
    'StudentNotify': 'Notifications - DigiPortal',
    'StudentArchived': 'Archived - DigiPortal'
  }
  
  document.title = titles[page] || 'DigiPortal'
}

// Check for existing session on app load
onMounted(() => {
  const savedLoggedIn = localStorage.getItem('digiportal_logged_in')
  const savedUserRole = localStorage.getItem('digiportal_user_role')
  const savedCurrentPage = localStorage.getItem('digiportal_current_page')
  
  console.log('App mounted - saved data:', { savedLoggedIn, savedUserRole, savedCurrentPage });
  
  if (savedLoggedIn === 'true' && savedUserRole && savedCurrentPage) {
    isLoggedIn.value = true
    userRole.value = savedUserRole
    currentPage.value = savedCurrentPage
    console.log('Restored session - currentPage:', currentPage.value);
    
    // Update document title
    const titles = {
      'TeacherHome': 'Teacher Home - DigiPortal',
      'TeacherRoom': 'Class Room - DigiPortal',
      'TeacherOutputs': 'Student Outputs - DigiPortal',
      'TeacherSprogress': 'Special Progress - DigiPortal',
      'TeacherProgress': 'Student Progress - DigiPortal',
      'TeacherRemarks': 'Remarks - DigiPortal',
      'TeacherNotice': 'Notices - DigiPortal',
      'TeacherNotify': 'Notifications - DigiPortal',
      'TeacherArchived': 'Archived - DigiPortal',
      'StudentNewsfeed': 'Student Home - DigiPortal',
      'StudentRoom': 'Class Room - DigiPortal',
      'StudentSketch': 'Sketch - DigiPortal',
      'StudentNotify': 'Notifications - DigiPortal',
      'StudentArchived': 'Archived - DigiPortal'
    }
    document.title = titles[savedCurrentPage] || 'DigiPortal'
  }
})

// Make navigation function globally available
window.navigateTo = handleNavigation
</script>

<style>
/* Global styles can be added here if needed */
</style>
