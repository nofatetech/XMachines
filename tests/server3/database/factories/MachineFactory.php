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
            'is_active' => $this->faker->boolean,
            'temperature' => $this->faker->randomFloat(2, 0, 100),
            'is_online' => $this->faker->boolean,
            'motor_left_speed' => $this->faker->numberBetween(0, 100),
            'motor_right_speed' => $this->faker->numberBetween(0, 100),
            'lights_on' => $this->faker->boolean,
            'fog_lights_on' => $this->faker->boolean,
        ];
    }
}
