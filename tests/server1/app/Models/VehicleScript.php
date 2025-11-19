<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class VehicleScript extends Model
{
    use HasFactory;

    protected $fillable = [
        'vehicle_id',
        'name',
        'code',
        'xml_code',
    ];

    public function vehicle()
    {
        return $this->belongsTo(Vehicle::class);
    }
}