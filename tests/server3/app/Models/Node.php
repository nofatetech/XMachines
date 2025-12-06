<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Node extends Model
{
    /** @use HasFactory<\Database\Factories\NodeFactory> */
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'machine_id',
        'name',
        'node_type',
        'status',
        'configuration',
    ];

    /**
     * Get the machine that owns the node.
     */
    public function machine()
    {
        return $this->belongsTo(Machine::class);
    }
}
