import axios from 'axios';
window.axios = axios;

window.axios.defaults.headers.common['X-Requested-with'] = 'XMLHttpRequest';

import Echo from 'laravel-echo';
import Pusher from 'pusher-js';
import Machine3D from './machine-3d.js';
import $ from 'jquery';
window.$ = window.jQuery = $;

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
    $(function() {
        const machines = window.xMachines;
        const machine3dInstances = new Map();

        // Initialize a 3D scene for each machine card
        machines.forEach(machine => {
            const container = $(`#imagination-frame-${machine.id}`);
            if (container.length) {
                const scene = new Machine3D(container[0]);
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
                    $(`#status-${machineId}`).text(e.machine.is_online ? 'Online' : 'Offline');
                    $(`#status-${machineId}`).attr('class', `badge ${e.machine.is_online ? 'badge-success' : 'badge-error'}`);
                    $(`#temp-${machineId}`).text(e.machine.temperature);
                    $(`#motor-left-${machineId}`).text(e.machine.motor_left_speed);
                    $(`#motor-right-${machineId}`).text(e.machine.motor_right_speed);
                    $(`#lights-${machineId}`).text(e.machine.lights_on ? 'On' : 'Off');
                    $(`#fog-lights-${machineId}`).text(e.machine.fog_lights_on ? 'On' : 'Off');
                    $(`#happiness-${machineId}`).text(e.machine.happiness);
                    $(`#hunger-${machineId}`).text(e.machine.hunger);
                    $(`#auto-driving-${machineId}`).text(e.machine.is_auto_driving ? 'On' : 'Off');
                });
        });

        // Use event delegation for control buttons
        $(document).on('click', '.control-btn', function() {
            const machineId = $(this).data('machine-id');
            const command = $(this).data('command');
            axios.post(`/machine/${machineId}/control`, { command: command })
                .catch(error => console.error('Error sending control command:', error));
        });

        // Use event delegation for LLM query buttons
        $(document).on('click', '.ask-llm-btn', function() {
            const machineId = $(this).data('machine-id');
            const modal = $(`#llm_modal_${machineId}`);
            if (modal.length) {
                modal[0].showModal();
            }
        });

        $(document).on('click', '.send-llm-query-btn', function() {
            const machineId = $(this).data('machine-id');
            const questionInput = $(`#llm_question_input_${machineId}`);
            const question = questionInput.val();
            const loadingSpinner = $(`.llm-loading-spinner_${machineId}`);
            const responseDisplay = $(`.llm-response-display_${machineId}`);

            if (!question) {
                alert('Please enter a question.');
                return;
            }

            loadingSpinner.removeClass('hidden');
            responseDisplay.addClass('hidden');

            axios.post(`/machine/${machineId}/control`, {
                command: 'ask_llm',
                question: question
            }).then(response => {
                loadingSpinner.addClass('hidden');
                responseDisplay.removeClass('hidden');
                responseDisplay.html('<p>Response will appear in the Pi\'s terminal.</p>');
            }).catch(error => {
                loadingSpinner.addClass('hidden');
                responseDisplay.removeClass('hidden');
                responseDisplay.html(`<p class="text-error">Error: ${error.message}</p>`);
            });
        });
    });
}
