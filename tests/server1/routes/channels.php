<?php

use Illuminate\Support\Facades\Broadcast;
use Illuminate\Support\Facades\Log; // Added for logging

Broadcast::channel('App.Models.User.{id}', function ($user, $id) {
    return (int) $user->id === (int) $id;
});

Broadcast::channel('vehicle-status.{vehicleId}', function ($user, $vehicleId) {
    Log::info('Channel authorization for vehicle-status.' . $vehicleId, ['user' => $user ? $user->id : 'Guest']);
    // For now, allow any authenticated user to listen.
    // In a real application, you'd verify if the user owns the vehicle.
    return $user !== null;
});
