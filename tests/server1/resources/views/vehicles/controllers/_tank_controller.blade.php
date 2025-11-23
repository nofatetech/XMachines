<div id="vehicle-controller-{{ $vehicle->id }}" style="background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 10px; padding: 20px; width: 600px; margin: auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    <table style="width: 100%;">
        <tr>
            <td colspan="2">
                <div style="border: 1px solid #ccc; background-color: #fff; min-height: 240px; text-align: center; padding: 10px;">
                    Camera Feed
                </div>
            </td>
        </tr>
        <tr>
            <td style="width: 50%; vertical-align: top;">
                <table style="width: 100%;">
                    <caption>Motor Controls</caption>
                    <tr>
                        <td>Left Motor</td>
                        <td>
                            <input type="range" min="-100" max="100" value="0" class="motor-slider" data-motor="left">
                            <span id="left-motor-value-{{ $vehicle->id }}">0</span>
                        </td>
                    </tr>
                    <tr>
                        <td>Right Motor</td>
                        <td>
                            <input type="range" min="-100" max="100" value="0" class="motor-slider" data-motor="right">
                            <span id="right-motor-value-{{ $vehicle->id }}">0</span>
                        </td>
                    </tr>
                </table>
                <table style="width: 100%; margin-top: 10px;">
                    <caption>Light Controls</caption>
                    <tr>
                        <td><button class="light-button" data-light="headlights">Headlights</button> <span id="headlights-status-{{ $vehicle->id }}">(Off)</span></td>
                        <td><button class="light-button" data-light="high_beams">High Beams</button> <span id="high_beams-status-{{ $vehicle->id }}">(Off)</span></td>
                    </tr>
                    <tr>
                        <td><button class="light-button" data-light="fog_lights">Fog Lights</button> <span id="fog_lights-status-{{ $vehicle->id }}">(Off)</span></td>
                        <td><button class="light-button" data-light="hazard">Hazard Lights</button> <span id="hazard-status-{{ $vehicle->id }}">(Off)</span></td>
                    </tr>
                    <tr>
                        <td><button class="light-button" data-light="left_blinker">Left Blinker</button> <span id="left_blinker-status-{{ $vehicle->id }}">(Off)</span></td>
                        <td><button class="light-button" data-light="right_blinker">Right Blinker</button> <span id="right_blinker-status-{{ $vehicle->id }}">(Off)</span></td>
                    </tr>
                </table>
            </td>
            <td style="width: 50%; vertical-align: top; padding-left: 20px;">
                <div style="border: 1px solid #ccc; background-color: #fff; padding: 10px; border-radius: 5px;">
                    <h4>Status</h4>
                    <ul style="list-style-type: none; padding: 0;">
                        <li><strong>Battery:</strong> <span id="battery-level-{{ $vehicle->id }}">N/A</span></li>
                        <li><strong>Status:</strong> <span id="status-{{ $vehicle->id }}">{{ $vehicle->status }}</span></li>
                        <li><strong>Wi-Fi:</strong> <span id="wifi-level-{{ $vehicle->id }}">N/A</span></li>
                        <!-- Add other vehicle data here -->
                    </ul>
                    <button class="settings-button" data-vehicle-id="{{ $vehicle->id }}">Settings</button>
                </div>
            </td>
        </tr>
        <tr>
            <td style="vertical-align: top; padding-top: 10px;">
                <div style="border: 1px solid #ccc; background-color: #fff; padding: 10px; border-radius: 5px;">
                    <h4>AI Camera</h4>
                    <ul id="ai-detected-objects-{{ $vehicle->id }}" style="list-style-type: none; padding: 0;">
                        <li>-</li>
                    </ul>
                </div>
            </td>
            <td style="vertical-align: top; padding-left: 20px; padding-top: 10px;">
                <div style="border: 1px solid #ccc; background-color: #fff; padding: 10px; border-radius: 5px;">
                    <h4>Personality</h4>
                    <ul style="list-style-type: none; padding: 0;">
                        <li><strong>Energy:</strong> <span id="energy-{{ $vehicle->id }}">{{ $vehicle->energy ?? 'N/A' }}</span></li>
                        <li><strong>Happiness:</strong> <span id="happiness-{{ $vehicle->id }}">{{ $vehicle->happiness ?? 'N/A' }}</span></li>
                    </ul>
                </div>
            </td>
        </tr>
    </table>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Using a self-executing anonymous function to encapsulate our code
        (function() {
            const vehicleId = {{ $vehicle->id }};
            const controllerRoot = document.getElementById(`vehicle-controller-${vehicleId}`);
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            // --- Sending Control Commands ---

            const sendControlCommand = (command) => {
                fetch(`/vehicle/${vehicleId}/control`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': csrfToken
                    },
                    body: JSON.stringify(command)
                }).catch(error => console.error('Error sending control command:', error));
            };

            // Add listeners to motor sliders within this specific controller
            controllerRoot.querySelectorAll('.motor-slider[data-motor]').forEach(slider => {
                slider.addEventListener('input', (e) => {
                    const motor = e.target.getAttribute('data-motor');
                    const value = e.target.value;
                    controllerRoot.querySelector(`#${motor}-motor-value-${vehicleId}`).innerText = value;
                    sendControlCommand({ [motor]: parseInt(value, 10) });
                });
            });

            // Add listeners to light buttons within this specific controller
            controllerRoot.querySelectorAll('.light-button[data-light]').forEach(button => {
                button.addEventListener('click', (e) => {
                    const light = e.target.getAttribute('data-light');
                    // The backend should handle the toggle logic.
                    sendControlCommand({ [light]: 'toggle' });
                });
            });


            // --- Listening for Status Updates ---
            console.log(`DEBUG JS: Frontend vehicleId is: ${vehicleId}`);
            const channelName = `vehicle-status.${vehicleId}`;
            const eventName = 'VehicleStatusUpdated'; // The event name we *expect*
            console.log(`DEBUG JS: Echo subscribing to channel: ${channelName}`);
            console.log(`DEBUG JS: Echo listening for event: ${eventName}`);

            Echo.private(channelName)
                .subscribed(() => {
                    console.log(`DEBUG JS: Successfully subscribed to private channel: ${channelName}`);
                })
                .error((error) => {
                    console.error(`DEBUG JS: Error subscribing to private channel ${channelName}:`, error);
                })
                .listen('.', (e) => { // Changed eventName to '.' to catch all events
                    console.log(`DEBUG JS: ALL Event received - full payload:`, e);
                    // The actual event name is usually within e.event or similar for Pusher/Reverb.
                    // We will inspect 'e' to find the actual event name.

                    // Check if e.event exists (common for broadcasted events)
                    const receivedEventName = e.event || 'UNKNOWN_EVENT_NAME';
                    console.log(`DEBUG JS: Received Event Name: ${receivedEventName}`);

                    if (receivedEventName === 'VehicleStatusUpdated') { // Only process if it's our event
                        console.log(`DEBUG JS: Processing VehicleStatusUpdated event for vehicle ${vehicleId}.`);
                        const status = e.vehicleStatus;

                        // Update motor value displays
                        if (status.hasOwnProperty('left')) {
                            controllerRoot.querySelector(`input[data-motor='left']`).value = status.left;
                            controllerRoot.querySelector(`#left-motor-value-${vehicleId}`).innerText = status.left;
                        }
                        if (status.hasOwnProperty('right')) {
                            controllerRoot.querySelector(`input[data-motor='right']`).value = status.right;
                            controllerRoot.querySelector(`#right-motor-value-${vehicleId}`).innerText = status.right;
                        }

                        // Update battery level
                        if (status.hasOwnProperty('batt')) {
                            console.log("!!!!!");
                            controllerRoot.querySelector(`#battery-level-${vehicleId}`).innerText = status.batt + '%';
                        }

                        // Update light statuses
                        if (status.hasOwnProperty('headlights')) {
                            controllerRoot.querySelector(`#headlights-status-${vehicleId}`).innerText = status.headlights ? '(On)' : '(Off)';
                        } else {
                             controllerRoot.querySelector(`#headlights-status-${vehicleId}`).innerText = '(Off)';
                        }
                        if (status.hasOwnProperty('highbeam')) {
                            controllerRoot.querySelector(`#high_beams-status-${vehicleId}`).innerText = status.highbeam ? '(On)' : '(Off)';
                        } else {
                             controllerRoot.querySelector(`#high_beams-status-${vehicleId}`).innerText = '(Off)';
                        }

                        if (status.hasOwnProperty('fog')) {
                             controllerRoot.querySelector(`#fog_lights-status-${vehicleId}`).innerText = status.fog ? '(On)' : '(Off)';
                        } else {
                             controllerRoot.querySelector(`#fog_lights-status-${vehicleId}`).innerText = '(Off)';
                        }

                        if (status.hasOwnProperty('hazard')) {
                             controllerRoot.querySelector(`#hazard-status-${vehicleId}`).innerText = status.hazard ? '(On)' : '(Off)';
                        } else {
                             controllerRoot.querySelector(`#hazard-status-${vehicleId}`).innerText = '(Off)';
                        }
                        if (status.hasOwnProperty('left_blinker')) {
                             controllerRoot.querySelector(`#left_blinker-status-${vehicleId}`).innerText = status.left_blinker ? '(On)' : '(Off)';
                        } else {
                             controllerRoot.querySelector(`#left_blinker-status-${vehicleId}`).innerText = '(Off)';
                        }
                        if (status.hasOwnProperty('right_blinker')) {
                             controllerRoot.querySelector(`#right_blinker-status-${vehicleId}`).innerText = status.right_blinker ? '(On)' : '(Off)';
                        } else {
                             controllerRoot.querySelector(`#right_blinker-status-${vehicleId}`).innerText = '(Off)';
                        }
                    } else {
                         console.log(`DEBUG JS: Received non-VehicleStatusUpdated event: ${receivedEventName}`);
                    }
                });

        })();
    });
</script>