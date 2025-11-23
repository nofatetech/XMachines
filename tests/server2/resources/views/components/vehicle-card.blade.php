<div id="vehicle-{{ $vehicle->id }}"
     class="p-4 mb-4 border rounded-lg {{ $vehicle->isOnline() ? 'bg-green-50 border-green-300' : 'bg-gray-100' }}">
    <div class="flex justify-between items-center">
        <div>
            <h3 class="font-bold text-lg">{{ $vehicle->name }} (ID:{{ $vehicle->id }})</h3>
            <span class="text-sm {{ $vehicle->isOnline() ? 'text-green-600' : 'text-red-600' }}">
                {{ $vehicle->isOnline() ? 'ONLINE' : 'OFFLINE' }}
            </span>
            • Battery: {{ $vehicle->batt ?? '—' }}V
        </div>
        <div class="text-right text-sm">
            Left: {{ $vehicle->left }} | Right: {{ $vehicle->right }}<br>
            @if($vehicle->highbeam) Highbeam @endif
            @if($vehicle->fog) Fog @endif
            @if($vehicle->hazard) Hazard @endif
        </div>
    </div>
    <div class="text-xs text-gray-500 mt-2">
        Last seen: {{ $vehicle->last_seen?->diffForHumans() ?? 'never' }}
    </div>
</div>
