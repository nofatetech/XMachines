<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Machine;
// use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        // User::factory(10)->create();

        User::factory()->create([
            'name' => 'Admin1',
            'email' => 'admin1@test.com',
            'password' => bcrypt("123123"),
        ]);

        Machine::factory(10)->create();
    }
}
