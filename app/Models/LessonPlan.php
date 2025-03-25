<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class LessonPlan extends Model
{
    protected $fillable = [
        'edulib.user_id', 
        'title', 
        'filename', 
        'path', 
        'status', 
        'uploaded_at'
    ];

    protected $dates = ['uploaded_at'];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
