<?php

namespace Database\Seeders;

use App\Models\Vehicle;
use Illuminate\Database\Seeder;

class VehicleSeeder extends Seeder
{
    public function run(): void
    {
        Vehicle::create([
            'name' => 'Truck Alpha',
            'status' => 'online',
            'description' => 'Main delivery truck – GPS active',
        ]);

        Vehicle::create([
            'name' => 'Van Beta',
            'status' => 'offline',
            'description' => 'In maintenance until Friday',
        ]);

        Vehicle::create([
            'name' => 'Car Gamma',
            'status' => 'online',
            'description' => 'Manager vehicle – live tracking',
        ]);
    }
}