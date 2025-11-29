<div id="machine-{{ $machine->id }}" class="card bg-base-100 shadow-xl">
    <div class="card-body">
        <h2 class="card-title">{{ $machine->name }}</h2>
        <p class="text-sm text-gray-500">UUID: {{ $machine->uuid }}</p>
        @isset($localIp)
            <p class="text-sm text-gray-500">Local IP: {{ $localIp }}</p>
        @endisset
        <p>Status: <span id="status-{{ $machine->id }}" class="badge {{ $machine->is_online ? 'badge-success' : 'badge-error' }}">{{ $machine->is_online ? 'Online' : 'Offline' }}</span></p>
        <div class="grid grid-cols-2 gap-2 text-sm">
            <p>Temp: <span id="temp-{{ $machine->id }}">{{ $machine->temperature }}</span>°C</p>
            <p>Lights: <span id="lights-{{ $machine->id }}">{{ $machine->lights_on ? 'On' : 'Off' }}</span></p>
            <p>L Motor: <span id="motor-left-{{ $machine->id }}">{{ $machine->motor_left_speed }}</span>%</p>
            <p>R Motor: <span id="motor-right-{{ $machine->id }}">{{ $machine->motor_right_speed }}</span>%</p>
            <p>Fog: <span id="fog-lights-{{ $machine->id }}">{{ $machine->fog_lights_on ? 'On' : 'Off' }}</span></p>
            <p>Happiness: <span id="happiness-{{ $machine->id }}">{{ $machine->happiness }}</span></p>
            <p>Hunger: <span id="hunger-{{ $machine->id }}">{{ $machine->hunger }}</span></p>
            <p>Auto-Driving: <span id="auto-driving-{{ $machine->id }}">{{ $machine->is_auto_driving ? 'On' : 'Off' }}</span></p>
        </div>
        @isset($showControls)
            <div class="card-actions justify-end mt-4">
                <button class="btn btn-primary btn-sm control-btn" data-machine-id="{{ $machine->id }}" data-command="toggle_lights">Toggle Lights</button>
                <button class="btn btn-secondary btn-sm control-btn" data-machine-id="{{ $machine->id }}" data-command="toggle_fog_lights">Toggle Fog</button>
                <button class="btn btn-info btn-sm control-btn" data-machine-id="{{ $machine->id }}" data-command="toggle_auto_driving">Toggle Auto Drive</button>
                <button class="btn btn-success btn-sm control-btn" data-machine-id="{{ $machine->id }}" data-command="feed">Feed</button>
                <button class="btn btn-warning btn-sm control-btn" data-machine-id="{{ $machine->id }}" data-command="play">Play</button>
            </div>
        @endisset
    </div>
</div>
