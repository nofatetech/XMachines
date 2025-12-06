<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('index');
});


// use App\Http\Controllers\AuthController;

// Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
// Route::post('/login', [AuthController::class, 'login']);

// Route::get('/register', [AuthController::class, 'showRegister']);
// Route::post('/register', [AuthController::class, 'register']);

// Route::post('/logout', [AuthController::class, 'logout'])->middleware('auth');

// Route::get('/dashboard', function () {
//     return view('dashboard');
// })->middleware('auth');
