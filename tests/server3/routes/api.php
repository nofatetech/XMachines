<?php

use App\Http\Controllers\Api\MachineStatusController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

// API route for machine status updates.
// This route is stateless and does not require CSRF protection.
Route::post('/machine/{machine}/status', [MachineStatusController::class, 'update'])->name('api.machine.status');
