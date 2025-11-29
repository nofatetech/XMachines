import axios from 'axios';
window.axios = axios;

window.axios.defaults.headers.common['X-Requested-with'] = 'XMLHttpRequest';

import Echo from 'laravel-echo';
import Pusher from 'pusher-js';
import SharedScene from './machine-3d.js'; // Updated import

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

if (typeof window.xMachines !== 'undefined') {
    document.addEventListener('DOMContentLoaded', function() {
        const sceneContainer = document.getElementById('scene-container');
        if (!sceneContainer) return;

        const sharedScene = new SharedScene(sceneContainer);
        sharedScene.populateScene(window.xMachines);

        const machines = window.xMachines;

        machines.forEach(machine => {
            window.Echo.channel(`machine.${machine.id}.status`)
                .listen('.machine.status-updated', (e) => {
                    console.log(`Received status update for machine ${e.machine.id}`, e.machine);
                    sharedScene.updateMachineState(e.machine);
                    // Also update sidebar if this machine is selected
                    const sidebar = document.getElementById('machine-details-sidebar');
                    if (!sidebar.classList.contains('hidden') && sidebar.dataset.machineId == e.machine.id) {
                        updateSidebar(e.machine);
                    }
                });
        });

        // Handle machine selection from 3D scene
        window.addEventListener('machine-selected', (event) => {
            const machineId = event.detail.id;
            const machineData = machines.find(m => m.id == machineId);
            if (machineData) {
                updateSidebar(machineData);
            }
        });

        // Function to update the sidebar
        function updateSidebar(machine) {
            const sidebar = document.getElementById('machine-details-sidebar');
            const title = document.getElementById('sidebar-title');
            const content = document.getElementById('sidebar-content');

            sidebar.dataset.machineId = machine.id;
            title.textContent = machine.name;

            // Build the sidebar content
            content.innerHTML = `
                <p><strong>Status:</strong> <span class="badge ${machine.is_online ? 'badge-success' : 'badge-error'}">${machine.is_online ? 'Online' : 'Offline'}</span></p>
                <p><strong>Temperature:</strong> ${machine.temperature}°C</p>
                <p><strong>Happiness:</strong> ${machine.happiness}</p>
                <p><strong>Hunger:</strong> ${machine.hunger}</p>
                <p><strong>L Motor:</strong> ${machine.motor_left_speed}%</p>
                <p><strong>R Motor:</strong> ${machine.motor_right_speed}%</p>
                <div class="card-actions justify-end mt-4">
                    <button class="btn btn-primary btn-sm control-btn" data-machine-id="${machine.id}" data-command="toggle_lights">Toggle Lights</button>
                    <button class="btn btn-secondary btn-sm control-btn" data-machine-id="${machine.id}" data-command="toggle_fog_lights">Toggle Fog</button>
                    <button class="btn btn-info btn-sm control-btn" data-machine-id="${machine.id}" data-command="toggle_auto_driving">Toggle Auto Drive</button>
                </div>
            `;

            // Re-attach event listeners to new buttons
            content.querySelectorAll('.control-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const machineId = this.dataset.machineId;
                    const command = this.dataset.command;
                    axios.post(`/machine/${machineId}/control`, { command: command })
                        .catch(error => console.error('Error sending control command:', error));
                });
            });


            sidebar.classList.remove('hidden');
        }
    });
}
