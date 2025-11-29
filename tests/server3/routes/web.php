<?php

use App\Events\MachineControlSent;
use App\Http\Controllers\ProfileController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Models\Machine;
use App\Events\MachineStatusUpdated;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/dashboard', function () {
    $machines = Machine::all();
    return view('dashboard', compact('machines'));
})->middleware(['auth', 'verified'])->name('dashboard');

Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');

    Route::post('/machine/{machine}/control', function (Request $request, Machine $machine) {
        $validated = $request->validate(['command' => 'required|string']);
        
        MachineControlSent::dispatch($machine->id, $validated['command']);

        return response()->json(['status' => 'Control event dispatched for machine ' . $machine->id]);
    })->name('machine.control');
});

Route::get('/machine-update', function () {
    if (Machine::query()->count() === 0) {
        return response()->json(['status' => 'No machines found'], 404);
    }

    $machine = Machine::all()->random();
    $machine->temperature = rand(0, 100);
    $machine->is_online = true; // A machine sending an update is online
    $machine->motor_left_speed = rand(0, 100);
    $machine->motor_right_speed = rand(0, 100);
    $machine->lights_on = (bool)rand(0, 1);
    $machine->fog_lights_on = (bool)rand(0, 1);
    $machine->save();

    MachineStatusUpdated::dispatch($machine);

    return response()->json(['status' => 'Machine status updated and event dispatched!', 'machine' => $machine]);
});

use App\Http\Controllers\Api\MachineStatusController;

// API route for machine status updates (unauthenticated for now)
Route::post('/api/machine/{machine}/status', [MachineStatusController::class, 'update'])->name('api.machine.status');

require __DIR__.'/auth.php';
