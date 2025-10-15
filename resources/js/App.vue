<template>
  <div id="app">
    <!-- Landing Page -->
    <Landing v-if="currentPage === 'landing'" @navigate="handleNavigation" />
    
    <!-- Login Page -->
    <AuthLogin v-if="currentPage === 'login'" @navigate="handleNavigation" />
    
    <!-- Teacher Pages with MainLayout -->
    <MainLayout v-if="currentPage.startsWith('teacher-')" @navigate="handleNavigation">
      <TeacherHome v-if="currentPage === 'teacher-home'" @navigate="handleNavigation" />
      <TeacherOutputs v-if="currentPage === 'teacher-outputs'" @navigate="handleNavigation" />
      <TeacherRoom v-if="currentPage === 'teacher-room'" @navigate="handleNavigation" />
      <TeacherNotify v-if="currentPage === 'teacher-notify'" @navigate="handleNavigation" />
      <TeacherProgress v-if="currentPage === 'teacher-progress'" @navigate="handleNavigation" />
      <TeacherSprogress v-if="currentPage === 'teacher-sprogress'" @navigate="handleNavigation" />
      <TeacherRemarks v-if="currentPage === 'teacher-remarks'" @navigate="handleNavigation" />
      <TeacherNotice v-if="currentPage === 'teacher-notice'" @navigate="handleNavigation" />
      <TeacherArchived v-if="currentPage === 'teacher-archived'" @navigate="handleNavigation" />
    </MainLayout>
    
    <!-- Student Newsfeed -->
    <StudentNewsfeed v-if="currentPage === 'student-newsfeed'" @navigate="handleNavigation" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Landing from './Pages/Landing.vue'
import AuthLogin from './Pages/Auth/Login.vue'
import MainLayout from './Layouts/MainLayout.vue'

// Teacher components
import TeacherHome from './Pages/Teacher/Home.vue'
import TeacherOutputs from './Pages/Teacher/Outputs.vue'
import TeacherRoom from './Pages/Teacher/Room.vue'
import TeacherNotify from './Pages/Teacher/Notify.vue'
import TeacherProgress from './Pages/Teacher/Progress.vue'
import TeacherSprogress from './Pages/Teacher/Sprogress.vue'
import TeacherRemarks from './Pages/Teacher/Remarks.vue'
import TeacherNotice from './Pages/Teacher/Notice.vue'
import TeacherArchived from './Pages/Teacher/Archived.vue'

// Student components
import StudentNewsfeed from './Pages/Student/Newsfeed.vue'

// Current page state
const currentPage = ref('landing')

// Handle navigation between pages
const handleNavigation = (page) => {
  currentPage.value = page
  
  // Update document title based on page
  const titles = {
    'landing': 'DigiPortal - Creative Learning Platform',
    'login': 'Login - DigiPortal',
    'teacher-home': 'Teacher Home - DigiPortal',
    'teacher-outputs': 'Student Outputs - DigiPortal',
    'teacher-room': 'Class Room - DigiPortal',
    'teacher-notify': 'Notifications - DigiPortal',
    'teacher-progress': 'Student Progress - DigiPortal',
    'teacher-sprogress': 'Special Progress - DigiPortal',
    'teacher-remarks': 'Remarks - DigiPortal',
    'teacher-notice': 'Notices - DigiPortal',
    'teacher-archived': 'Archived - DigiPortal',
    'student-newsfeed': 'Student Newsfeed - DigiPortal'
  }
  
  document.title = titles[page] || 'DigiPortal'
}

// Make navigation function globally available
window.navigateTo = handleNavigation
</script>

<style>
/* Global styles can be added here if needed */
</style>
