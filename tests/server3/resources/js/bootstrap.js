import axios from 'axios';
window.axios = axios;

window.axios.defaults.headers.common['X-Requested-with'] = 'XMLHttpRequest';

import Echo from 'laravel-echo';
import Pusher from 'pusher-js';
import Machine3D from './machine-3d.js';

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
        const machines = window.xMachines;
        const machine3dInstances = new Map();

        // Initialize a 3D scene for each machine card
        machines.forEach(machine => {
            const container = document.getElementById(`imagination-frame-${machine.id}`);
            if (container) {
                const scene = new Machine3D(container);
                machine3dInstances.set(machine.id, scene);
                scene.updateState(machine); // Set initial state
            }
        });

        // Listen for WebSocket updates
        machines.forEach(machine => {
            window.Echo.channel(`machine.${machine.id}.status`)
                .listen('.machine.status-updated', (e) => {
                    const scene = machine3dInstances.get(e.machine.id);
                    if (scene) {
                        scene.updateState(e.machine);
                    }
                    // Also update the 2D stats in the card
                    const machineId = e.machine.id;
                    document.getElementById(`status-${machineId}`).textContent = e.machine.is_online ? 'Online' : 'Offline';
                    document.getElementById(`status-${machineId}`).className = `badge ${e.machine.is_online ? 'badge-success' : 'badge-error'}`;
                    document.getElementById(`temp-${machineId}`).textContent = e.machine.temperature;
                    document.getElementById(`motor-left-${machineId}`).textContent = e.machine.motor_left_speed;
                    document.getElementById(`motor-right-${machineId}`).textContent = e.machine.motor_right_speed;
                    document.getElementById(`lights-${machineId}`).textContent = e.machine.lights_on ? 'On' : 'Off';
                    document.getElementById(`fog-lights-${machineId}`).textContent = e.machine.fog_lights_on ? 'On' : 'Off';
                    document.getElementById(`happiness-${machineId}`).textContent = e.machine.happiness;
                    document.getElementById(`hunger-${machineId}`).textContent = e.machine.hunger;
                    document.getElementById(`auto-driving-${machineId}`).textContent = e.machine.is_auto_driving ? 'On' : 'Off';
                });
        });

        // Re-attach event listeners for control buttons
        document.querySelectorAll('.control-btn').forEach(button => {
            button.addEventListener('click', function() {
                const machineId = this.dataset.machineId;
                const command = this.dataset.command;
                axios.post(`/machine/${machineId}/control`, { command: command })
                    .catch(error => console.error('Error sending control command:', error));
            });
        });

        // Re-attach event listeners for LLM query buttons
        document.querySelectorAll('.ask-llm-btn').forEach(button => {
            button.addEventListener('click', function() {
                const machineId = this.dataset.machineId;
                const modal = document.getElementById(`llm_modal_${machineId}`);
                if (modal) {
                    modal.showModal();
                }
            });
        });

        document.querySelectorAll('.send-llm-query-btn').forEach(button => {
            button.addEventListener('click', function() {
                const machineId = this.dataset.machineId;
                const questionInput = document.getElementById(`llm_question_input_${machineId}`);
                const question = questionInput.value;
                const loadingSpinner = document.querySelector(`.llm-loading-spinner_${machineId}`);
                const responseDisplay = document.querySelector(`.llm-response-display_${machineId}`);

                if (!question) {
                    alert('Please enter a question.');
                    return;
                }

                loadingSpinner.classList.remove('hidden');
                responseDisplay.classList.add('hidden');

                axios.post(`/machine/${machineId}/control`, {
                    command: 'ask_llm',
                    question: question
                }).then(response => {
                    loadingSpinner.classList.add('hidden');
                    responseDisplay.classList.remove('hidden');
                    responseDisplay.innerHTML = '<p>Response will appear in the Pi\'s terminal.</p>';
                }).catch(error => {
                    loadingSpinner.classList.add('hidden');
                    responseDisplay.classList.remove('hidden');
                    responseDisplay.innerHTML = `<p class="text-error">Error: ${error.message}</p>`;
                });
            });
        });
    });
}
