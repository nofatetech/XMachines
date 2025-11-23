<?php

use Illuminate\Support\Facades\Route;
use App\Models\Vehicle;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use PhpMqtt\Client\MqttClient;

// The web routes are only available if the application is in server mode.
if (config('app.server_mode_enabled')) {
    Route::get('/', function () {
        $localIp = getHostByName(getHostName());
        return view('dashboard', [
            'vehicles' => \App\Models\Vehicle::all(),
            'localIp' => $localIp
        ]);
    })->middleware('auth');

    Route::post('/vehicle/{id}/control', function (Request $request, $id) {
        // For now, we'll assume the frontend sends valid data for direct passthrough.
        // If more strict validation is needed for specific keys (e.g., 'left', 'right'),
        // it can be added here.

        $server   = config('mqtt.host');
        $port     = config('mqtt.port');
        $clientId = config('mqtt.client_id') . '_control_' . uniqid();
        $client = new MqttClient($server, $port, $clientId);

        $client->connect();
        $payload = json_encode($request->all()); // Directly encode the entire request payload
        $client->publish("vehicle/$id/control", $payload, 0);
        $client->disconnect();

        return response()->json(['message' => "control sent to vehicle $id: $payload"]);
    })
    ->withoutMiddleware([Illuminate\Foundation\Http\Middleware\VerifyCsrfToken::class]);

    // Temporary developer login route
    Route::get('/dev-login/{userId}', function ($userId) {
        $user = User::findOrFail($userId);
        Auth::login($user);
        return redirect('/');
    });
}