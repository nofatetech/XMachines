<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\User;
use App\Models\Vehicle;

class VehicleSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Find the first user or create one if none exist
        $user = User::first();
        if (!$user) {
            $user = User::factory()->create([
                'name' => 'Test User 1',
                'email' => 'test1@example.com',
            ]);
        }

        Vehicle::create([
            'user_id' => $user->id,
            'name' => 'Tank Bot 1',
            'type' => 'tank',
            'status' => 'offline',
            'energy' => 100,
            'happiness' => 100,
        ]);

        Vehicle::create([
            'user_id' => $user->id,
            'name' => 'Rover Alpha',
            'type' => 'rover',
            'status' => 'online',
            'energy' => 85,
            'happiness' => 90,
        ]);

        Vehicle::create([
            'user_id' => $user->id,
            'name' => 'NES Controller Car',
            'type' => 'nes_controller',
            'status' => 'offline',
            'energy' => 50,
            'happiness' => 60,
        ]);
    }
}