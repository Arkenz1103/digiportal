<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class AuthController extends Controller
{
    public function login(Request $request){
       $fields = $request->validate([
        'email' => ['required', 'email'],
        'password' => ['required']
       ]);

       if(Auth::attempt($fields, $request->remember)){
            $request->session()->regenerate();

            $user = Auth::user();
            switch($user->role) {
                case 'admin':
                    return redirect()->route('admin.class');
                case 'teacher':
                    return redirect()->route('teacher.class');
                case 'student':
                    return redirect()->route('student.class');
                default:
                    return redirect()->route('class');
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
