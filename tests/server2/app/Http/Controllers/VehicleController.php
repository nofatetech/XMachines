<?php

namespace App\Http\Controllers;

use App\Models\Vehicle;
use Illuminate\Http\Request;
use Illuminate\View\View;

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
}
