<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Storage;
use App\Models\LessonPlan;

class LessonPlanController extends Controller
{
    public function upload(Request $request)
    {
        // Validate the uploaded file
        $request->validate([
            'lesson_plan' => 'required|file|mimes:pdf,doc,docx|max:10240' // 10MB max
        ]);

        // Get the uploaded file
        $file = $request->file('lesson_plan');

        // Generate a unique filename
        $filename = 'lesson_plan_' . time() . '.' . $file->getClientOriginalExtension();

        // Store the file in the lesson plans directory
        $path = $file->storeAs('lesson_plans', $filename, 'public');

        // Create a lesson plan record
        $lessonPlan = LessonPlan::create([
            'user_id' => Auth::id(),
            'title' => $file->getClientOriginalName(),
            'filename' => $filename,
            'path' => $path,
            'status' => 'Pending',
            'uploaded_at' => now()
        ]);

        // Return lesson plans for the user
        return response()->json([
            'message' => 'Lesson plan uploaded successfully',
            'lesson_plans' => LessonPlan::where('user_id', Auth::id())->get()
        ]);
    }

    public function index()
    {
        return response()->json([
            'lesson_plans' => LessonPlan::where('user_id', Auth::id())->get()
        ]);
    }
}