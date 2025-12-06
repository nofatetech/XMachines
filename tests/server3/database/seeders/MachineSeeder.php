<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Machine;
use App\Models\MachineType;
use App\Models\Node;

class MachineSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $vehicleType = MachineType::where('name', 'vehicle')->first();
        $robotArmType = MachineType::where('name', 'robot arm')->first();

        // Create 5 vehicles
        Machine::factory(5)->create([
            'machine_type_id' => $vehicleType->id,
        ])->each(function ($machine) {
            Node::create([
                'machine_id' => $machine->id,
                'name' => 'gps',
                'node_type' => 'sensor',
                'status' => 'running',
            ]);
            Node::create([
                'machine_id' => $machine->id,
                'name' => 'motor_controller_left',
                'node_type' => 'actuator',
                'status' => 'running',
            ]);
            Node::create([
                'machine_id' => $machine->id,
                'name' => 'motor_controller_right',
                'node_type' => 'actuator',
                'status' => 'running',
            ]);
        });

        // Create 5 robot arms
        Machine::factory(5)->create([
            'machine_type_id' => $robotArmType->id,
        ])->each(function ($machine) {
            Node::create([
                'machine_id' => $machine->id,
                'name' => 'gripper_actuator',
                'node_type' => 'actuator',
                'status' => 'running',
            ]);
            Node::create([
                'machine_id' => $machine->id,
                'name' => 'joint_position_sensor',
                'node_type' => 'sensor',
                'status' => 'running',
            ]);
        });
    }
}
