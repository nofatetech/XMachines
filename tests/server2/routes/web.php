<?php

use App\Http\Controllers\ProfileController;
use App\Http\Controllers\VehicleController;
use Illuminate\Support\Facades\Route;

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

Route::get('/vehicle-card-partial/{vehicle}', [VehicleController::class, 'getVehicleCardPartial'])->name('vehicle.card.partial');
Route::post('/vehicle/{vehicle}/control', [VehicleController::class, 'control'])->name('vehicle.control');


// Route::get('/vehicle-partial/{id}', function ($id) {
//     $vehicle = \App\Models\Vehicle::findOrFail($id);
//     return view('components.vehicle-card', compact('vehicle'));
// });

require __DIR__.'/auth.php';
