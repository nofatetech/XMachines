<?php

use Illuminate\Support\Facades\Route;
use App\Models\Vehicle;
use Illuminate\Http\Request;
use PhpMqtt\Client\MqttClient;

Route::get('/', function () {
    // return view('welcome');

    // $serverIp = $_SERVER;
    // dd($serverIp); // For debugging

    $localIp = getHostByName(getHostName());
    // $localIp = "192.168.0.33";
    // dd($localIp);


    return view('dashboard', ['vehicles' => \App\Models\Vehicle::all(), 'localIp' => $localIp]);
});

Route::post('/vehicle/{id}/command', function (Request $request, $id) {
    // dd("xxx");
    $vehicle = Vehicle::findOrFail($id);
    $action = $request->input('action');
    $speed = $request->input('speed', 0.5); // Default speed: 0.5

    // Validate inputs
    if (!in_array($action, ['forward', 'stop', 'turn_left', 'turn_right'])) {
        return response()->json(['error' => 'Invalid action'], 400);
    }

    // Publish MQTT command
    $client = new MqttClient('localhost', 1883, 'laravel-command-' . uniqid());
    $client->connect();
    $payload = json_encode(['action' => $action, 'speed' => (float)$speed]);
    $client->publish("vehicle/$id/control", $payload, 0);
    $client->disconnect();

    return response()->json(['message' => "Command sent to vehicle $id: $payload"]);
})
// ->withoutMiddleware([\App\Http\Middleware\VerifyCsrfToken::class])
->withoutMiddleware([Illuminate\Foundation\Http\Middleware\VerifyCsrfToken::class])
;