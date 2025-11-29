<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Machine>
 */
class MachineFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        static $machineNumber = 1;

        return [
            'uuid' => Str::uuid(),
            'name' => 'Machine ' . $machineNumber++,
            'small_description' => $this->faker->sentence,
            'description' => $this->faker->paragraph,
            'is_active' => true,
            'temperature' => 0,
            'is_online' => false,
            'motor_left_speed' => 0,
            'motor_right_speed' => 0,
            'lights_on' => false,
            'fog_lights_on' => false,
        ];
    }
}
