<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Machine extends Model
{
    /** @use HasFactory<\Database\Factories\MachineFactory> */
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'uuid',
        'name',
        'small_description',
        'description',
        'happiness',
        'hunger',
        'is_active',
        'temperature',
        'is_online',
        'motor_left_speed',
        'motor_right_speed',
        'lights_on',
        'fog_lights_on',
        'is_auto_driving',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'is_active' => 'boolean',
        'is_online' => 'boolean',
        'lights_on' => 'boolean',
        'fog_lights_on' => 'boolean',
        'motor_left_speed' => 'integer',
        'motor_right_speed' => 'integer',
        'temperature' => 'decimal:2',
        'happiness' => 'integer',
        'hunger' => 'integer',
        'is_auto_driving' => 'boolean',
    ];

    /**
     * Get the nodes for the machine.
     */
    public function nodes()
    {
        return $this->hasMany(Node::class);
    }
}
