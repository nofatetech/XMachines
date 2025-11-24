<div id="vehicle-{{ $vehicle->id }}"
     data-last-seen="{{ $vehicle->last_seen?->toIso8601String() }}"
     class="vehicle-card p-4 mb-4 border rounded-lg {{ $vehicle->isOnline() ? 'bg-green-50 border-green-300' : 'bg-gray-100' }}">
    <div class="flex justify-between items-center">
        <div>
            <h3 classs="font-bold text-lg">{{ $vehicle->name }} (ID:{{ $vehicle->id }})</h3>
            <span class="vehicle-status text-sm {{ $vehicle->isOnline() ? 'text-green-600' : 'text-red-600' }}">
                {{ $vehicle->isOnline() ? 'ONLINE' : 'OFFLINE' }}
            </span>
            • Battery: {{ $vehicle->batt ?? '—' }}V
            • Highbeam: {{ $vehicle->highbeam ? 'On' : 'Off' }}
            • Fog: {{ $vehicle->fog ? 'On' : 'Off' }}
            • Hazard: {{ $vehicle->hazard ? 'On' : 'Off' }}
        </div>
        <div class="text-right text-sm">
            Left: {{ $vehicle->left }} | Right: {{ $vehicle->right }}
        </div>
    </div>
    <div class="mt-4 p-4 border rounded-lg bg-gray-50">
        <h4 class="font-semibold mb-2">Vehicle Controls</h4>
        <div class="grid grid-cols-2 gap-4">
            <div>
                <label for="left-{{ $vehicle->id }}" class="block text-sm font-medium text-gray-700">Left (-100 to 100)</label>
                <input type="number" id="left-{{ $vehicle->id }}" min="-100" max="100" value="{{ $vehicle->left }}"
                       class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                <button class="control-button mt-2 inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        data-action="update-left" data-vehicle-id="{{ $vehicle->id }}">Set Left</button>
            </div>
            <div>
                <label for="right-{{ $vehicle->id }}" class="block text-sm font-medium text-gray-700">Right (-100 to 100)</label>
                <input type="number" id="right-{{ $vehicle->id }}" min="-100" max="100" value="{{ $vehicle->right }}"
                       class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                <button class="control-button mt-2 inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        data-action="update-right" data-vehicle-id="{{ $vehicle->id }}">Set Right</button>
            </div>
            <div class="col-span-2 flex justify-around mt-2">
                <button class="control-button inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white {{ $vehicle->highbeam ? 'bg-indigo-600' : 'bg-gray-400' }} hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        data-action="toggle-highbeam" data-vehicle-id="{{ $vehicle->id }}" data-state="{{ $vehicle->highbeam ? 'on' : 'off' }}">
                    Highbeam: {{ $vehicle->highbeam ? 'On' : 'Off' }}
                </button>
                <button class="control-button inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white {{ $vehicle->fog ? 'bg-indigo-600' : 'bg-gray-400' }} hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        data-action="toggle-fog" data-vehicle-id="{{ $vehicle->id }}" data-state="{{ $vehicle->fog ? 'on' : 'off' }}">
                    Fog: {{ $vehicle->fog ? 'On' : 'Off' }}
                </button>
                <button class="control-button inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white {{ $vehicle->hazard ? 'bg-indigo-600' : 'bg-gray-400' }} hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        data-action="toggle-hazard" data-vehicle-id="{{ $vehicle->id }}" data-state="{{ $vehicle->hazard ? 'on' : 'off' }}">
                    Hazard: {{ $vehicle->hazard ? 'On' : 'Off' }}
                </button>
            </div>
        </div>
    </div>
    <div class="vehicle-last-seen text-xs text-gray-500 mt-2">
        Last seen: <span class="font-semibold">{{ $vehicle->last_seen?->diffForHumans() ?? 'never' }}</span>
    </div>
</div>
