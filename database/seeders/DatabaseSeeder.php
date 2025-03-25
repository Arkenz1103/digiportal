<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        // Create Teacher
        User::create([
            'name' => 'Teacher',
            'email' => 'teacher@gmail.com',
            'password' => Hash::make('tpassword'),
            'role' => 'teacher',
        ]);

        // Create Student
        User::create([
            'name' => 'Student',
            'email' => 'student@gmail.com',
            'password' => Hash::make('spassword'),
            'role' => 'student',
        ]);
    }
}
