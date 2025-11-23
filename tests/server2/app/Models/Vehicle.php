<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Vehicle extends Model
{
    /** @use HasFactory<\Database\Factories\VehicleFactory> */
    use HasFactory;
    
    protected $guarded = [];
    
    protected $casts = [
        'raw_status' => 'array',
        'last_seen' => 'datetime',
    ];

    protected $fillable = ['name', 'status', 'description'];

    public function isOnline(): bool
    {
        return $this->last_seen && $this->last_seen->diffInMinutes(now()) < 2;
    }

}
