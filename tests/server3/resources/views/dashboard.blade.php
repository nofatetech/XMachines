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
                        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Machine Updates:</h3>
                        <ul id="machine-updates" class="mt-2 space-y-2"></ul>
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
                const machineUpdates = document.getElementById('machine-updates');

                window.Echo.connector.pusher.connection.bind('state_change', function(states) {
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

                window.Echo.channel('machines')
                    .listen('.machine.status-updated', (e) => {
                        const listItem = document.createElement('li');
                        listItem.textContent = `Machine ${e.machine.name} (UUID: ${e.machine.uuid}) updated: Temperature=${e.machine.temperature}, Online=${e.machine.is_online ? 'Yes' : 'No'}, Left Motor=${e.machine.motor_left_speed}, Right Motor=${e.machine.motor_right_speed}, Lights=${e.machine.lights_on ? 'On' : 'Off'}, Fog Lights=${e.machine.fog_lights_on ? 'On' : 'Off'}`;
                        machineUpdates.prepend(listItem);
                    });
            });
        </script>
    @endpush
</x-app-layout>
