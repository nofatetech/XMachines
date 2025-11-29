<?php

use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;
use App\Models\Machine;
use App\Events\MachineStatusUpdated;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/dashboard', function () {
    return view('dashboard');
})->middleware(['auth', 'verified'])->name('dashboard');

Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});

Route::get('/machine-update', function () {
    $machine = Machine::all()->random();
    $machine->temperature = rand(0, 100);
    $machine->is_online = (bool)rand(0, 1);
    $machine->motor_left_speed = rand(0, 100);
    $machine->motor_right_speed = rand(0, 100);
    $machine->lights_on = (bool)rand(0, 1);
    $machine->fog_lights_on = (bool)rand(0, 1);
    $machine->save();

    MachineStatusUpdated::dispatch($machine);

    return response()->json(['status' => 'Machine status updated and event dispatched!', 'machine' => $machine]);
});

require __DIR__.'/auth.php';
