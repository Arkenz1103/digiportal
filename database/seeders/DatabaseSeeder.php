<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        // Create Admin
        User::create([
            'name' => 'Admin',
            'email' => 'admin@admin.com',
            'password' => Hash::make('
            '),
            'role' => 'admin',
        ]);

        // Create Teacher
        User::create([
            'name' => 'Teacher',
            'email' => 'teacher@teacher.com',
            'password' => Hash::make('password123'),
            'role' => 'teacher',
        ]);

        // Create Student
        User::create([
            'name' => 'Student',
            'email' => 'student@student.com',
            'password' => Hash::make('password123'),
            'role' => 'student',
        ]);
    }
}
