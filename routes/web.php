<?php

use App\Http\Controllers\AuthController;
use App\Http\Middleware\AdminMiddleware;
use App\Http\Middleware\TeacherMiddleware;
use App\Http\Middleware\StudentMiddleware;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Auth;
use Inertia\Inertia;

// Public routes
Route::inertia('/', 'Landing')->name('landing');
Route::inertia('/login', 'Auth/Login')->name('login');
Route::post('/login', [AuthController::class, 'login']);
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

// Protected routes
Route::middleware(['auth'])->group(function () {
    // Admin routes
    Route::middleware([AdminMiddleware::class])->prefix('admin')->name('admin.')->group(function () {
        Route::get('/dashboard', function() {
            return Inertia::render('Admin/Dashboard', [
                'user' => Auth::user()
            ]);
        })->name('dashboard');

        Route::get('/classes', function() {
            return Inertia::render('Admin/Classes', [
                'user' => Auth::user()
            ]);
        })->name('classes');

        Route::get('/lessons', function() {
            return Inertia::render('Admin/Lessons', [
                'user' => Auth::user()
            ]);
        })->name('lessons');

        Route::get('/teachers', function() {
            return Inertia::render('Admin/Teachers', [
                'user' => Auth::user()
            ]);
        })->name('teachers');

        Route::get('/students', function() {
            return Inertia::render('Admin/Students', [
                'user' => Auth::user()
            ]);
        })->name('students');
    });

    // Teacher routes
    Route::middleware([TeacherMiddleware::class])->prefix('teacher')->name('teacher.')->group(function () {
        Route::get('/dashboard', function() {
            return Inertia::render('Teacher/Dashboard2', [
                'user' => Auth::user()
            ]);
        })->name('dashboard');

        Route::get('/lessons', function() {
            return Inertia::render('Teacher/Lessons2', [
                'user' => Auth::user()
            ]);
        })->name('lessons');

        Route::get('/class', function() {
            return Inertia::render('Teacher/Class2', [
                'user' => Auth::user()
            ]);
        })->name('class');

        Route::get('/calendar', function() {
            return Inertia::render('Teacher/Calendar2', [
                'user' => Auth::user()
            ]);
        })->name('calendar');
    });

    // Student routes
    Route::middleware([StudentMiddleware::class])->prefix('student')->name('student.')->group(function () {
        Route::get('/dashboard', function() {
            return Inertia::render('Student/Dashboard1', [
                'user' => Auth::user()
            ]);
        })->name('dashboard');

        Route::get('/classes', function() {
            return Inertia::render('Student/Classes', [
                'user' => Auth::user()
            ]);
        })->name('classes');

        Route::get('/assignments', function() {
            return Inertia::render('Student/Assignments', [
                'user' => Auth::user()
            ]);
        })->name('assignments');

        Route::get('/grades', function() {
            return Inertia::render('Student/Grades', [
                'user' => Auth::user()
            ]);
        })->name('grades');
    });

    // Common routes (accessible to all authenticated users)
    Route::get('/profile', function() {
        return Inertia::render('Profile', [
            'user' => Auth::user()
        ]);
    })->name('profile');
});
