<?php

use Illuminate\Support\Facades\Broadcast;

Broadcast::channel('App.Models.User.{id}', function ($user, $id) {
    return (int) $user->id === (int) $id;
});

Broadcast::channel('vehicle-status.{vehicleId}', function ($user, $vehicleId) {
    // For now, allow any authenticated user to listen.
    // In a real application, you'd verify if the user owns the vehicle.
    return $user !== null;
});
