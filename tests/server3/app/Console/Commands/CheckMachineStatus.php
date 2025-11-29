<?php

namespace App\Console\Commands;

use App\Events\MachineStatusUpdated;
use App\Models\Machine;
use Illuminate\Console\Command;
use Illuminate\Support\Carbon;

class CheckMachineStatus extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'machines:check-status';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Check for machines that have not reported in recently and mark them as offline.';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $timeout = 5; // seconds
        $this->info("Checking for machines that have not been updated in the last {$timeout} seconds...");

        $timedOutMachines = Machine::where('is_online', true)
            ->where('updated_at', '<', Carbon::now()->subSeconds($timeout))
            ->get();

        if ($timedOutMachines->isEmpty()) {
            $this->info('No timed-out machines found.');
            return;
        }

        $this->info("Found {$timedOutMachines->count()} timed-out machines. Updating their status.");

        foreach ($timedOutMachines as $machine) {
            $machine->is_online = false;
            $machine->save();

            // Broadcast the status update
            MachineStatusUpdated::dispatch($machine);

            $this->warn("Machine {$machine->name} (ID: {$machine->id}) marked as offline.");
        }

        $this->info('Finished checking machine statuses.');
    }
}
