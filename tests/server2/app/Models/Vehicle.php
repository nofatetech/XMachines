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

    protected $fillable = [
        'name',
        'status',
        'description',
        'raw_status',
        'batt',
        'left',
        'right',
        'highbeam',
        'fog',
        'hazard',
        'last_seen',
    ];

    public function isOnline(): bool
    {
        return $this->last_seen && $this->last_seen->diffInSeconds(now()) < 5;
    }

}
