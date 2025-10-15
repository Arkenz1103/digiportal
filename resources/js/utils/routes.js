/**
 * Vue Router Routes Configuration
 * Frontend routing for DigiPortal Creative Learning Platform
 */

// Import components directly
import Landing from '../Pages/Landing.vue'
import AuthLogin from '../Pages/Auth/Login.vue'

// Teacher pages
import TeacherHome from '../Pages/Teacher/Home.vue'
import TeacherOutputs from '../Pages/Teacher/Outputs.vue'
import TeacherRoom from '../Pages/Teacher/Room.vue'
import TeacherNotify from '../Pages/Teacher/Notify.vue'
import TeacherProgress from '../Pages/Teacher/Progress.vue'
import TeacherSprogress from '../Pages/Teacher/Sprogress.vue'
import TeacherRemarks from '../Pages/Teacher/Remarks.vue'
import TeacherNotice from '../Pages/Teacher/Notice.vue'
import TeacherArchived from '../Pages/Teacher/Archived.vue'

// Student pages
import StudentNewsfeed from '../Pages/Student/Newsfeed.vue'
import StudentSketch from '../Pages/Student/Sketch.vue'
import StudentRoom from '../Pages/Student/Sroom.vue'
import StudentNotify from '../Pages/Student/Snotify.vue'
import StudentArchived from '../Pages/Student/Sarchived.vue'

// Route definitions for Vue Router
export const routes = [
    {
        path: '/',
        name: 'Landing',
        component: Landing,
        meta: { title: 'Creative Learning Platform' }
    },
    {
        path: '/login',
        name: 'Login',
        component: AuthLogin,
        meta: { title: 'Authentication - DigiPortal' }
    },
    // Teacher Routes
    {
        path: '/teacher/home',
        name: 'TeacherHome',
        component: TeacherHome,
        meta: { title: 'Teacher Home', requiresAuth: true, role: 'teacher' }
    },
    {
        path: '/teacher/outputs/:id?',
        name: 'TeacherOutputs',
        component: TeacherOutputs,
        meta: { title: 'Student Outputs', requiresAuth: true, role: 'teacher' }
    },
    {
        path: '/teacher/room/:gradeSection?',
        name: 'TeacherRoom',
        component: TeacherRoom,
        meta: { title: 'Class Room', requiresAuth: true, role: 'teacher' }
    },
    {
        path: '/teacher/notify',
        name: 'TeacherNotify',
        component: TeacherNotify,
        meta: { title: 'Notifications', requiresAuth: true, role: 'teacher' }
    },
    {
        path: '/teacher/progress',
        name: 'TeacherProgress',
        component: TeacherProgress,
        meta: { title: 'Student Progress', requiresAuth: true, role: 'teacher' }
    },
    {
        path: '/teacher/sprogress',
        name: 'TeacherSProgress',
        component: TeacherSprogress,
        meta: { title: 'Special Progress', requiresAuth: true, role: 'teacher' }
    },
    {
        path: '/teacher/remarks',
        name: 'TeacherRemarks',
        component: TeacherRemarks,
        meta: { title: 'Remarks', requiresAuth: true, role: 'teacher' }
    },
    {
        path: '/teacher/notice',
        name: 'TeacherNotice',
        component: TeacherNotice,
        meta: { title: 'Notices', requiresAuth: true, role: 'teacher' }
    },
    {
        path: '/teacher/archived',
        name: 'TeacherArchived',
        component: TeacherArchived,
        meta: { title: 'Archived', requiresAuth: true, role: 'teacher' }
    },
    // Student Routes
    {
        path: '/student/newsfeed',
        name: 'StudentNewsfeed',
        component: StudentNewsfeed,
        meta: { title: 'Newsfeed', requiresAuth: true, role: 'student' }
    },
    {
        path: '/student/sketch',
        name: 'StudentSketch',
        component: StudentSketch,
        meta: { title: 'Creative Sketch', requiresAuth: true, role: 'student' }
    },
    {
        path: '/student/room/:gradeSection?',
        name: 'StudentRoom',
        component: StudentRoom,
        meta: { title: 'My Class', requiresAuth: true, role: 'student' }
    },
    {
        path: '/student/notify',
        name: 'StudentNotify',
        component: StudentNotify,
        meta: { title: 'Notifications', requiresAuth: true, role: 'student' }
    },
    {
        path: '/student/archived',
        name: 'StudentArchived',
        component: StudentArchived,
        meta: { title: 'Archived', requiresAuth: true, role: 'student' }
    },
    // Catch-all route for 404
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('../Pages/Landing.vue'), // Redirect to landing for now
        meta: { title: '404 - Page Not Found' }
    }
];

/**
 * Route helper function for generating URLs
 * @param {string} name - Route name
 * @param {object} params - Route parameters
 * @returns {string} - Route path
 */
export function route(name, params = {}) {
    const routeConfig = routes.find(r => r.name === name);
    
    if (!routeConfig) {
        console.warn(`Route "${name}" not found`);
        return '/';
    }
    
    let path = routeConfig.path;
    
    // Replace route parameters
    Object.keys(params).forEach(key => {
        path = path.replace(`:${key}`, params[key]);
    });
    
    // Remove optional parameters that weren't provided
    path = path.replace(/\/:[^/]*\?/g, '');
    
    return path;
}

// Make route function available globally
if (typeof window !== 'undefined') {
    window.route = route;
}

export default routes;
