<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;

class AuthController extends Controller
{
    public function login(Request $request){
       $fields = $request->validate([
        'email' => ['required', 'email'],
        'password' => ['required']
       ]);

       Log::info('Login attempt', [
           'email' => $fields['email'],
           'attempt' => Auth::attempt([
               'email' => $fields['email'],
               'password' => $fields['password']
           ], $request->boolean('remember'))
       ]);

       if(Auth::attempt([
           'email' => $fields['email'],
           'password' => $fields['password']
       ], $request->boolean('remember'))){
            $request->session()->regenerate();

            $user = Auth::user();

            Log::info('User authenticated', [
                'user_id' => $user->id,
                'user_role' => $user->role
            ]);

            switch($user->role) {
                case 'teacher':
                    return redirect()->route('teacher.meetings');
                case 'student':
                    return redirect()->route('student.class');
                default:
                    return redirect()->route('meetings');
            }
       }

       return back()->withErrors([
        'email' => 'The provided credentials do not match our records.'
       ])->onlyInput('email');
    }

    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        return redirect()->route('landing');
    }
}
