<?php

namespace App\Http\Controllers;

use App\Models\Vehicle;
use Illuminate\Http\Request;
use Illuminate\View\View;
// use PhpMqtt\Client\Facades\Mqtt;
use PhpMqtt\Client\Facades\MQTT;

class VehicleController extends Controller
{
    /**
     * Get a rendered vehicle card partial view.
     */
    public function getVehicleCardPartial(string $id): View
    {
        $vehicle = Vehicle::findOrFail($id);
        return view('components.vehicle-card', compact('vehicle'));
    }

    /**
     * Send a control command to a vehicle via MQTT.
     */
    public function control(Request $request, Vehicle $vehicle)
    {
        $validated = $request->validate([
            'left' => 'sometimes|integer|min:-100|max:100',
            'right' => 'sometimes|integer|min:-100|max:100',
            'highbeam' => 'sometimes|boolean',
            'fog' => 'sometimes|boolean',
            'hazard' => 'sometimes|boolean',
        ]);

        $topic = "vehicle/{$vehicle->id}/control";
        $payload = json_encode($validated);

        Mqtt::publish($topic, $payload);

        return response()->json(['status' => 'Command sent', 'topic' => $topic, 'payload' => $validated]);
    }
}
