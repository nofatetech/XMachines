import axios from 'axios';
window.axios = axios;

window.axios.defaults.headers.common['X-Requested-with'] = 'XMLHttpRequest';

/**
 * Echo exposes an expressive API for subscribing to channels and listening
 * for events that are broadcast by Laravel. Echo and event broadcasting
 * allow your team to quickly build robust real-time web applications.
 */

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

// --- Dashboard Specific Logic ---
// This will only run on pages that have defined `window.xMachines`
if (typeof window.xMachines !== 'undefined') {
    document.addEventListener('DOMContentLoaded', function() {
        const wsStatus = document.getElementById('websocket-status');
        console.log('DOM Content Loaded. Echo instance:', window.Echo);

        console.log('Binding to state_change event...');
        window.Echo.connector.pusher.connection.bind('state_change', function(states) {
            console.log('WebSocket state changed:', states);
            if (wsStatus) {
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
            }
        });

        const machines = window.xMachines;
        const lastMachineUpdate = {};

        machines.forEach(machine => {
            // Initialize last update time for each machine
            lastMachineUpdate[machine.id] = Date.now();

            window.Echo.channel(`machine.${machine.id}.status`)
                .listen('.machine.status-updated', (e) => {
                    console.log(`Received machine.status-updated event for machine ${machine.id}:`, e);
                    const machineId = e.machine.id;
                    const machineCard = document.getElementById(`machine-${machineId}`);
                    if (machineCard) {
                        // Update last update time
                        lastMachineUpdate[machineId] = Date.now();

                        const statusBadge = document.getElementById(`status-${machineId}`);
                        statusBadge.textContent = e.machine.is_online ? 'Online' : 'Offline';
                        statusBadge.className = `badge ${e.machine.is_online ? 'badge-success' : 'badge-error'}`;

                        document.getElementById(`temp-${machineId}`).textContent = e.machine.temperature;
                        document.getElementById(`motor-left-${machineId}`).textContent = e.machine.motor_left_speed;
                        document.getElementById(`motor-right-${machineId}`).textContent = e.machine.motor_right_speed;
                        document.getElementById(`lights-${machineId}`).textContent = e.machine.lights_on ? 'On' : 'Off';
                        document.getElementById(`fog-lights-${machineId}`).textContent = e.machine.fog_lights_on ? 'On' : 'Off';
                        
                        // Update new Tamagotchi fields
                        document.getElementById(`happiness-${machineId}`).textContent = e.machine.happiness;
                        document.getElementById(`hunger-${machineId}`).textContent = e.machine.hunger;
                        document.getElementById(`auto-driving-${machineId}`).textContent = e.machine.is_auto_driving ? 'On' : 'Off';
                    }
                });
        });

        // Client-side timeout check
        setInterval(() => {
            const fiveSecondsAgo = Date.now() - 5000;
            machines.forEach(machine => {
                const machineId = machine.id;
                const statusBadge = document.getElementById(`status-${machineId}`);
                if (statusBadge && lastMachineUpdate[machineId] < fiveSecondsAgo) {
                    if (statusBadge.textContent !== 'Offline') {
                        console.log(`Machine ${machineId} timed out. Setting to Offline.`);
                        statusBadge.textContent = 'Offline';
                        statusBadge.className = 'badge badge-error';
                    }
                }
            });
        }, 1000); // Check every second

        // Add event listeners for control buttons
        document.querySelectorAll('.control-btn').forEach(button => {
            button.addEventListener('click', function() {
                const machineId = this.dataset.machineId;
                const command = this.dataset.command;

                console.log(`Sending command '${command}' to machine ${machineId}`);

                axios.post(`/machine/${machineId}/control`, {
                    command: command
                }).then(response => {
                    console.log('Control command sent successfully:', response.data);
                }).catch(error => {
                    console.error('Error sending control command:', error);
                });
            });
        });
    });
}
