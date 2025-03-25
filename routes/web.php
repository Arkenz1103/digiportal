<?php

use App\Http\Controllers\AuthController;
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
Route::post('/logout', [AuthController::class, 'logout'])->name('logout'); // Logout route added

// Protected routes
Route::middleware(['auth'])->group(function () {

    // Teacher routes
    Route::middleware([TeacherMiddleware::class])->prefix('teacher')->name('teacher.')->group(function () {
        // Add home route
        Route::get('/home', function() {
            return Inertia::render('Teacher/Home');
        })->name('home');

        Route::get('/class/{gradeSection}', function($gradeSection) {
            // Convert 'grade1-a' to 'Grade 1 - A'
            $parts = explode('-', $gradeSection);
            
            if (count($parts) < 2) {
                abort(404, 'Invalid class format');
            }
            
            $grade = ucfirst(preg_replace('/grade(\d+)/', 'Grade $1', $parts[0]));
            $section = strtoupper($parts[1] ?? '');
            $displayName = "$grade - $section";
            
            // Get the theme from the session or database
            // For now, we'll use a simple array to simulate stored data
            $classes = [
                'Grade 1 - A' => 'emerald',
                'Grade 2 - A' => 'blue',
                'Grade 3 - A' => 'purple',
                // Add more classes as they're created
            ];
            
            return Inertia::render('Teacher/Room', [
                'className' => $displayName,
                'theme' => $classes[$displayName] ?? 'emerald' // Default to emerald if not found
            ]);
        })->name('class.show');

        Route::get('/notify', function() {
            return Inertia::render('Teacher/Notify', [
                'user' => Auth::user()
            ]);
        })->name('notify');

        Route::get('/progress', function(Request $request) {
            return Inertia::render('Teacher/Progress', [
                'selectedStudent' => $request->student ?? null
            ]);
        })->name('progress');

        Route::get('/remarks', function() {
            return Inertia::render('Teacher/Remarks', [
                'user' => Auth::user()
            ]);
        })->name('remarks');

        Route::get('/archived', function() {
            return Inertia::render('Teacher/Archived');
        })->name('archived');
    });

    // Student routes
    Route::middleware([StudentMiddleware::class])->prefix('student')->name('student.')->group(function () {
        Route::get('/dashboard', function() {
            return redirect()->route('student.newsfeed');
        })->name('dashboard');

        // Add newsfeed route
        Route::get('/newsfeed', function() {
            return Inertia::render('Student/Newsfeed');
        })->name('newsfeed');

        // Change Calendar route to Sketch route
        Route::get('/sketch', function() {
            return Inertia::render('Student/Sketch');
        })->name('sketch');

        // Add archived route
        Route::get('/archived', function() {
            return Inertia::render('Student/Archived');
        })->name('archived');

        Route::get('/class/{gradeSection}', function($gradeSection) {
            $parts = explode('-', $gradeSection);
            
            if (count($parts) < 2) {
                abort(404, 'Invalid class format');
            }
            
            $grade = ucfirst(preg_replace('/grade(\d+)/', 'Grade $1', $parts[0]));
            $section = strtoupper($parts[1] ?? '');
            $displayName = "$grade - $section";
            
            $classes = [
                'Grade 1 - A' => 'emerald',
                'Grade 2 - A' => 'blue',
                'Grade 3 - A' => 'purple',
            ];
            
            return Inertia::render('Student/Sroom', [
                'className' => $displayName,
                'theme' => $classes[$displayName] ?? 'emerald'
            ]);
        })->name('class.show');
    });

});
