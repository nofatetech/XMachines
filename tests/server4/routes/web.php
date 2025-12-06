<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('index');
});

Route::get('/dashboard', function () {
    $data=[
        'machines' => \App\Models\Machine::all(),
    ];
    return view('dashboard', $data);
});

Route::get('/machine_display', function () {
    return view('machine_display');
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
