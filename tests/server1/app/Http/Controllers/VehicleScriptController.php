<?php

namespace App\Http\Controllers;

use App\Models\Vehicle;
use App\Models\VehicleScript;
use App\Vehicle\Engine;
use Illuminate\Http\Request;

class VehicleScriptController extends Controller
{
    public function index($vehicle_id)
    {
        $scripts = VehicleScript::where('vehicle_id', $vehicle_id)->get();
        return response()->json($scripts);
    }

    public function store(Request $request)
    {
        $request->validate([
            'vehicle_id' => 'required|exists:vehicles,id',
            'name' => 'required|string|max:255',
            'code' => 'required|string',
            'xml_code' => 'required|string',
        ]);

        $script = VehicleScript::create([
            'vehicle_id' => $request->vehicle_id,
            'name' => $request->name,
            'code' => $request->code,
            'xml_code' => $request->xml_code,
        ]);

        return response()->json(['message' => 'Script saved successfully!', 'script' => $script]);
    }

    public function execute(VehicleScript $script)
    {
        try {
            $vehicle = $script->vehicle;
            $engine = new Engine($vehicle);
            
            // This is where the user-generated code is executed.
            eval($script->code);

            return response()->json(['message' => 'Script executed successfully.']);
        } catch (\Throwable $e) {
            // Catch any error from the eval'd code
            return response()->json(['error' => 'Error during script execution: ' . $e->getMessage()], 500);
        }
    }

    public function destroy(VehicleScript $script)
    {
        $script->delete();
        return response()->json(['message' => 'Script deleted successfully.']);
    }
}