<?php

namespace App\Http\Controllers\Api;

use App\Events\MachineStatusUpdated;
use App\Http\Controllers\Controller;
use App\Models\Machine;
use Illuminate\Http\Request;

class MachineStatusController extends Controller
{
    /**
     * Update the status of a machine.
     */
    public function update(Request $request, Machine $machine)
    {
        $validated = $request->validate([
            'temperature' => 'sometimes|numeric',
            'motor_left_speed' => 'sometimes|integer|min:0|max:100',
            'motor_right_speed' => 'sometimes|integer|min:0|max:100',
            'lights_on' => 'sometimes|boolean',
            'fog_lights_on' => 'sometimes|boolean',
        ]);

        // Fill the machine model with validated data,
        // set its status, and save it.
        $machine->fill($validated);
        $machine->is_online = true;
        $machine->save(); // This also updates the `updated_at` timestamp.

        // Dispatch the event to update the dashboard.
        MachineStatusUpdated::dispatch($machine);

        return response()->json(['status' => 'ok']);
    }
}
