<?php

use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Auth;


Route::get('/', function () {
    return view('welcome');
});



Route::get('/xtmp1', function () {
    $user = App\Models\User::where('email', 'test1@example.com')->first();
    $user->password = Hash::make('123123');
    $user->save();
    return "x";
});

Route::get('/dashboard', function () {
    $vehicles = Auth::user()->vehicles;
    return view('dashboard', ['vehicles' => $vehicles]);
})->middleware(['auth', 'verified'])->name('dashboard');

Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});

require __DIR__.'/auth.php';
