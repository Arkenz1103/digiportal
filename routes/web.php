<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\ClassroomController;
use App\Http\Controllers\LessonPlanController;
use App\Http\Middleware\AdminMiddleware;
use App\Http\Middleware\TeacherMiddleware;
use App\Http\Middleware\StudentMiddleware;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Auth;
use Inertia\Inertia;
use Illuminate\Http\Request;

// Public routes
Route::inertia('/', 'Landing')->name('landing');
Route::inertia('/login', 'Auth/Login')->name('login');
Route::post('/login', [AuthController::class, 'login']);
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

// Protected routes
Route::middleware(['auth'])->group(function () {
    // Admin routes
    Route::middleware([AdminMiddleware::class])->prefix('admin')->name('admin.')->group(function () {

        Route::get('/lessons', function(Request $request) {
            return Inertia::render('Admin/Lessons', [
                'user' => Auth::user(),
                'view' => $request->query('view', 'urgent_and_upcoming') // Default to 'urgent_and_upcoming' view
            ]);
        })->name('lessons');
    });

    // Teacher routes
    Route::middleware([TeacherMiddleware::class])->prefix('teacher')->name('teacher.')->group(function () {

        Route::get('/class', function() {
            return Inertia::render('Teacher/Class2', [
                'user' => Auth::user()
            ]);
        })->name('class');

        Route::get('/lessons', function(Request $request) {
            return Inertia::render('Teacher/Lessons', [
                'user' => Auth::user(),
                'view' => $request->query('view', 'urgent_and_upcoming') // Default to 'urgent_and_upcoming' view
            ]);
        })->name('lessons');

        Route::get('/class/{className}', function($className) {
            return Inertia::render('Teacher/ClassDetail2', [
                'className' => ucfirst($className)
            ]);
        })->name('class.show');

        Route::get('/calendar', function() {
            return Inertia::render('Teacher/Calendar2', [
                'user' => Auth::user()
            ]);
        })->name('calendar');

        Route::post('/lesson-plans/upload', [LessonPlanController::class, 'upload'])->name('lesson-plans.upload');
        Route::get('/lesson-plans', [LessonPlanController::class, 'index'])->name('lesson-plans.index');

    });

    // Student routes
    Route::middleware([StudentMiddleware::class])->prefix('student')->name('student.')->group(function () {
        Route::get('/dashboard', function() {
            return Inertia::render('Student/Dashboard1');
        })->name('dashboard');

        // Class routes
        Route::get('/class', function() {
            return Inertia::render('Student/ClassOverview');
        })->name('class');

        Route::get('/class/{className}', function($className) {
            return Inertia::render('Student/ClassDetail1', [
                'className' => ucfirst($className)
            ]);
        })->name('class.show');

        // Calendar route
        Route::get('/calendar', function() {
            return Inertia::render('Student/Calendar');
        })->name('calendar');
    });

    // Common routes (accessible to all authenticated users)
    Route::get('/profile', function() {
        return Inertia::render('Profile', [
            'user' => Auth::user()
        ]);
    })->name('profile');
});
