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
        <script type="module">
            import Echo from 'laravel-echo';
            import Pusher from 'pusher-js';

            window.Pusher = Pusher;

            window.Echo = new Echo({
                broadcaster: 'reverb',
                key: import.meta.env.VITE_REVERB_APP_KEY,
                wsHost: import.meta.env.VITE_REVERB_HOST,
                wsPort: import.meta.env.VITE_REVERB_PORT ?? 80,
                wssPort: import.meta.env.VITE_REVERB_PORT ?? 443,
                forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
                enabledTransports: ['ws', 'wss'],
            });

            document.addEventListener('DOMContentLoaded', function() {
                const wsStatus = document.getElementById('websocket-status');
                console.log('DOM Content Loaded. Echo instance:', window.Echo);

                console.log('Binding to state_change event...');
                window.Echo.connector.pusher.connection.bind('state_change', function(states) {
                    console.log('WebSocket state changed:', states);
                    wsStatus.textContent = states.current;
                    if (states.current === 'connected') {
                        wsStatus.classList.remove('text-red-500', 'text-yellow-500');
                        wsStatus.classList.add('text-green-500');
                    } else if (states.current === 'connecting') {
                        wsStatus.classList.remove('text-green-500', 'text-red-500');
                        wsStatus.classList.add('text-yellow-500');
                    } else {
                        wsStatus.classList.remove('text-green-500', 'text-yellow-500');
                        wsStatus.classList.add('text-red-500');
                    }
                });

                const machines = @json($machines);
                machines.forEach(machine => {
                    window.Echo.channel(`machine.${machine.id}.status`)
                        .listen('.machine.status-updated', (e) => {
                            console.log(`Received machine.status-updated event for machine ${machine.id}:`, e);
                            const machineId = e.machine.id;
                            const machineCard = document.getElementById(`machine-${machineId}`);
                            if (machineCard) {
                                const statusBadge = document.getElementById(`status-${machineId}`);
                                statusBadge.textContent = e.machine.is_online ? 'Online' : 'Offline';
                                statusBadge.className = `badge ${e.machine.is_online ? 'badge-success' : 'badge-error'}`;
                                
                                document.getElementById(`temp-${machineId}`).textContent = e.machine.temperature;
                                document.getElementById(`motor-left-${machineId}`).textContent = e.machine.motor_left_speed;
                                document.getElementById(`motor-right-${machineId}`).textContent = e.machine.motor_right_speed;
                                document.getElementById(`lights-${machineId}`).textContent = e.machine.lights_on ? 'On' : 'Off';
                                document.getElementById(`fog-lights-${machineId}`).textContent = e.machine.fog_lights_on ? 'On' : 'Off';
                            }
                        });
                });
            });
        </script>
    @endpush
</x-app-layout>
