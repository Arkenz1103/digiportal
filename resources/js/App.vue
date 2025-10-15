<template>
  <div id="app">
    <!-- Landing Page -->
    <Landing v-if="currentPage === 'landing'" @navigate="handleNavigation" />
    
    <!-- Login Page -->
    <AuthLogin v-if="currentPage === 'login'" @navigate="handleNavigation" />
    
    <!-- Teacher Home -->
    <TeacherHome v-if="currentPage === 'teacher-home'" @navigate="handleNavigation" />
    
    <!-- Student Newsfeed -->
    <StudentNewsfeed v-if="currentPage === 'student-newsfeed'" @navigate="handleNavigation" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Landing from './Pages/Landing.vue'
import AuthLogin from './Pages/Auth/Login.vue'
import TeacherHome from './Pages/Teacher/Home.vue'
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
