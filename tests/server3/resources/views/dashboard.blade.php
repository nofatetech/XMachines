<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">
            {{ __('Dashboard') }}
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6 text-gray-900 dark:text-gray-100">
                    {{ __("You're logged in!") }}

                    <div class="mt-4">
                        <p>WebSocket Server: <span id="websocket-server">localhost:8080</span></p>
                        <p>WebSocket Status: <span id="websocket-status" class="font-bold">Connecting...</span></p>
                    </div>

                    <div class="mt-6">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Connected Machines:</h3>
                        <div id="machines-grid" class="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            @foreach($machines as $machine)
                                <div id="machine-{{ $machine->id }}" class="card bg-base-100 shadow-xl">
                                    <div class="card-body">
                                        <h2 class="card-title">{{ $machine->name }}</h2>
                                        <p class="text-sm text-gray-500">{{ $machine->uuid }}</p>
                                        <p>Status: <span id="status-{{ $machine->id }}" class="badge {{ $machine->is_online ? 'badge-success' : 'badge-error' }}">{{ $machine->is_online ? 'Online' : 'Offline' }}</span></p>
                                        <div class="grid grid-cols-2 gap-2 text-sm">
                                            <p>Temp: <span id="temp-{{ $machine->id }}">{{ $machine->temperature }}</span>°C</p>
                                            <p>Lights: <span id="lights-{{ $machine->id }}">{{ $machine->lights_on ? 'On' : 'Off' }}</span></p>
                                            <p>L Motor: <span id="motor-left-{{ $machine->id }}">{{ $machine->motor_left_speed }}</span>%</p>
                                            <p>R Motor: <span id="motor-right-{{ $machine->id }}">{{ $machine->motor_right_speed }}</span>%</p>
                                            <p>Fog: <span id="fog-lights-{{ $machine->id }}">{{ $machine->fog_lights_on ? 'On' : 'Off' }}</span></p>
                                        </div>
                                        <div class="card-actions justify-end mt-4">
                                            <button class="btn btn-primary btn-sm control-btn" data-machine-id="{{ $machine->id }}" data-command="toggle_lights">Toggle Lights</button>
                                            <button class="btn btn-secondary btn-sm control-btn" data-machine-id="{{ $machine->id }}" data-command="toggle_fog_lights">Toggle Fog</button>
                                        </div>
                                    </div>
                                </div>
                            @endforeach
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    @push('scripts')
        <script>
            // Expose machine data to the global window object
            window.xMachines = @json($machines);
        </script>
    @endpush
</x-app-layout>
