{{-- resources/views/dashboard.blade.php --}}
<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight">
            {{ __('Dashboard') }}
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 space-y-8">

            {{-- Simple test message (kept forever) --}}
            <div class="bg-white shadow-sm rounded-lg p-6 text-center">
                <div id="msg" class="text-3xl font-bold text-green-600">
                    Waiting for test broadcast...
                </div>
            </div>

            {{-- Live vehicles list --}}
            <div class="bg-white shadow-sm rounded-lg p-6">
                <h2 class="text-2xl font-bold mb-6 text-center text-blue-600">
                    Live Vehicle Tracking – 100% Local Reverb + MQTT
                </h2>

                <div id="vehicles-list" class="space-y-4">
                    @foreach(\App\Models\Vehicle::all() as $vehicle)
                        <x-vehicle-card :vehicle="$vehicle" />
                    @endforeach
                </div>
            </div>

        </div>
    </div>

    {{-- Load Echo once --}}
    @vite(['resources/js/echo.js'])

        {{-- ONE single Echo listener for BOTH events --}}

    @push('scripts')

        <script>

            document.addEventListener('DOMContentLoaded', () => {

                Echo.channel('public')

                    .listen('TestBroadcast', (e) => {

                        document.getElementById('msg').innerText = e.message || 'Test OK';

                        console.log("OK!", e.message);

                    })

                    .listen('VehicleStatusUpdated', (e) => {   // ← THIS LINE FIXED

                        console.log('Vehicle update received!', e);

    

                                    const card = document.getElementById(`vehicle-${e.vehicle.id}`);

                                    if (card) {

                                        fetch(`/vehicle-card-partial/${e.vehicle.id}?t=${Date.now()}`)

                                            .then(r => r.text())

                                            .then(html => {

                                                card.outerHTML = html;

                                            });

                                    }                });

    

                // Function to calculate human-readable time difference

                function timeAgo(date) {

                    const seconds = Math.floor((new Date() - date) / 1000);

                    if (seconds < 2) return "just now";

                    let interval = seconds / 31536000;

                    if (interval > 1) return Math.floor(interval) + " years ago";

                    interval = seconds / 2592000;

                    if (interval > 1) return Math.floor(interval) + " months ago";

                    interval = seconds / 86400;

                    if (interval > 1) return Math.floor(interval) + " days ago";

                    interval = seconds / 3600;

                    if (interval > 1) return Math.floor(interval) + " hours ago";

                    interval = seconds / 60;

                    if (interval > 1) return Math.floor(interval) + " minutes ago";

                    return Math.floor(seconds) + " seconds ago";

                }

    

                // Periodic UI updater

                setInterval(() => {

                    const vehicleCards = document.querySelectorAll('.vehicle-card');

                    vehicleCards.forEach(card => {

                        const lastSeenStr = card.dataset.lastSeen;

                        if (!lastSeenStr) return;

    

                        const lastSeenDate = new Date(lastSeenStr);

                        const secondsAgo = Math.floor((new Date() - lastSeenDate) / 1000);

    

                        const statusEl = card.querySelector('.vehicle-status');

                        const lastSeenEl = card.querySelector('.vehicle-last-seen span');

    

                        // Update status and card color

                        if (secondsAgo < 5) {

                            statusEl.textContent = 'ONLINE';

                            statusEl.classList.remove('text-red-600');

                            statusEl.classList.add('text-green-600');

                            card.classList.remove('bg-gray-100');

                            card.classList.add('bg-green-50', 'border-green-300');

                        } else {

                            statusEl.textContent = 'OFFLINE';

                            statusEl.classList.remove('text-green-600');

                            statusEl.classList.add('text-red-600');

                            card.classList.remove('bg-green-50', 'border-green-300');

                            card.classList.add('bg-gray-100');

                        }

    

                        // Update last seen text

                        lastSeenEl.textContent = timeAgo(lastSeenDate);

                    });

                }, 1000); // Update every second

                // Delegated event listener for vehicle controls
                const vehiclesList = document.getElementById('vehicles-list');
                vehiclesList.addEventListener('click', function(event) {
                    const button = event.target.closest('.control-button');
                    if (!button) return;

                    const vehicleId = button.dataset.vehicleId;
                    const action = button.dataset.action;

                    function sendControlCommand(vehicleId, payload) {
                        const url = `/vehicle/${vehicleId}/control`;
                        fetch(url, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                            },
                            body: JSON.stringify(payload)
                        })
                        .then(response => response.json())
                        .then(data => console.log('Command sent:', data))
                        .catch(error => console.error('Error sending command:', error));
                    }

                    let payload = {};
                    switch (action) {
                        case 'update-left': {
                            const leftValue = document.getElementById(`left-${vehicleId}`).value;
                            payload = { left: parseInt(leftValue, 10) };
                            break;
                        }
                        case 'update-right': {
                            const rightValue = document.getElementById(`right-${vehicleId}`).value;
                            payload = { right: parseInt(rightValue, 10) };
                            break;
                        }
                        case 'toggle-highbeam': {
                            const newState = button.dataset.state !== 'on';
                            payload = { highbeam: newState };
                            break;
                        }
                        case 'toggle-fog': {
                            const newState = button.dataset.state !== 'on';
                            payload = { fog: newState };
                            break;
                        }
                        case 'toggle-hazard': {
                            const newState = button.dataset.state !== 'on';
                            payload = { hazard: newState };
                            break;
                        }
                    }
                    sendControlCommand(vehicleId, payload);
                });
            });

        </script>

    @endpush

    </x-app-layout>