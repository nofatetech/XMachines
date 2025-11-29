<?php

use App\Events\MachineControlSent;
use App\Http\Controllers\ProfileController;
use App\Models\Machine;
use App\Events\MachineStatusUpdated;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('xm-home');
});

// Conditional routing based on APP_MODE
if (env('APP_MODE') === 'SERVER') {
    Route::get('/dashboard', function () {
        $machines = Machine::all();
        return view('dashboard', compact('machines'));
    })->middleware(['auth', 'verified'])->name('dashboard');
} elseif (env('APP_MODE') === 'MACHINE') {
    Route::get('/display', function () {
        $machineId = env('MACHINE_ID');
        $machine = Machine::find($machineId);
        if (!$machine) {
            abort(404, "Machine with ID {$machineId} not found for display mode.");
        }

        // You might fetch the local IP here if needed for display
        $localIp = '127.0.0.1'; // Placeholder, actual IP detection might be complex in Laravel

        return view('machine.display', compact('machine', 'localIp'));
    })->name('machine.display');
}

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

// This route should always be available for machines reporting status
Route::get('/machine-update', function () {
    if (Machine::query()->count() === 0) {
        return response()->json(['status' => 'No machines found'], 404);
    }

    $machine = Machine::all()->random(); // This is the test route, still uses random machine
    $machine->temperature = rand(0, 100);
    $machine->is_online = true;
    $machine->motor_left_speed = rand(0, 100);
    $machine->motor_right_speed = rand(0, 100);
    $machine->lights_on = (bool)rand(0, 1);
    $machine->fog_lights_on = (bool)rand(0, 1);
    $machine->save();

    MachineStatusUpdated::dispatch($machine);

    return response()->json(['status' => 'Machine status updated and event dispatched!', 'machine' => $machine]);
});


require __DIR__.'/auth.php';
