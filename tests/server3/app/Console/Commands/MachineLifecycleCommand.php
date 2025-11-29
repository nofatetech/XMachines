<?php

namespace App\Console\Commands;

use App\Events\MachineStatusUpdated;
use App\Models\Machine;
use Illuminate\Console\Command;

class MachineLifecycleCommand extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'machine:life-cycle {machineId}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Simulates the daily life-cycle of a machine (Tamagotchi-like features).';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $machineId = $this->argument('machineId');
        $machine = Machine::find($machineId);

        if (!$machine) {
            $this->error("Machine with ID {$machineId} not found.");
            return;
        }

        $this->info("Running life cycle for Machine: {$machine->name}");

        // Simulate hunger increase
        $machine->hunger = min(100, $machine->hunger + 5); // Hunger increases by 5, max 100

        // Simulate happiness change based on hunger
        if ($machine->hunger >= 80) {
            $machine->happiness = max(0, $machine->happiness - 10); // Very hungry, happiness drops fast
        } elseif ($machine->hunger >= 50) {
            $machine->happiness = max(0, $machine->happiness - 2); // Hungry, happiness drops slowly
        } else {
            $machine->happiness = min(100, $machine->happiness + 1); // Not hungry, happiness slowly recovers
        }

        $machine->save();

        // Dispatch event to update local dashboard/display
        MachineStatusUpdated::dispatch($machine);

        $this->info("Machine {$machine->name} - Hunger: {$machine->hunger}, Happiness: {$machine->happiness}");
    }
}
