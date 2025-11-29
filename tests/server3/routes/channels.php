<?php

use Illuminate\Support\Facades\Broadcast;

/*
|--------------------------------------------------------------------------
| Broadcast Channels
|--------------------------------------------------------------------------
|
| Here you may register all of the event broadcasting channels that your
| application supports. The given channel authorization callbacks are
| used to check if an authenticated user can listen to the channel.
|
*/

// For now, we allow any client to subscribe to these channels without authentication.
// In the future, you could add authentication here to verify the machine's identity.

Broadcast::channel('machine.{machineId}.status', function ($user, $machineId) {
    return true; // Allow anyone to listen
});

Broadcast::channel('machine.{machineId}.control', function ($user, $machineId) {
    return true; // Allow anyone to listen
});