<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight">
            {{ __('Dashboard') }}
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6 text-gray-900">
                    {{ __("You're logged in!") }}
                </div>
            </div>
        </div>
    </div>

    <div class="p-6">
        <div id="msg" class="text-2xl font-bold text-green-600">Waiting for message...</div>
    </div>

    {{-- Load Echo + Reverb connection --}}
    @vite(['resources/js/echo.js'])

    {{-- Listen for the broadcast --}}
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            Echo.channel('public')
                .listen('TestBroadcast', (e) => {
                    document.getElementById('msg').innerText = e.message || 'Received!';
                });

            console.log('Echo connected to local Reverb');
        });
    </script>













<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-6 text-gray-900">
                <h2 class="text-2xl font-bold mb-6">Live Vehicle Status</h2>

                <div id="vehicles-list">
                    @foreach(\App\Models\Vehicle::all() as $vehicle)
                        <x-vehicle-card :vehicle="$vehicle" />
                    @endforeach
                </div>
            </div>
        </div>
    </div>
</div>

<!-- @ vite(['resources/js/echo.js']) -->
@push('scripts')

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            Echo.channel('public')
                .listen('VehicleStatusUpdated', (e) => {
                    const vehicle = e.vehicle;
                    const card = document.getElementById(`vehicle-${vehicle.id}`);
                    if (card) {
                        fetch(`/vehicle-card-partial/${vehicle.id}`)
                            .then(response => response.text())
                            .then(html => {
                                card.outerHTML = html;
                            })
                            .catch(error => {
                                console.error('Error fetching vehicle card partial:', error);
                            });
                    }
                });
        });
    </script>
@endpush








</x-app-layout>