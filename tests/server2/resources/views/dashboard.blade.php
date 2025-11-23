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
                })
                .listen('VehicleStatusUpdated', (e) => {   // ← THIS LINE FIXED
                    console.log('Vehicle update received!', e);

                    const card = document.getElementById(`vehicle-${e.vehicle.id}`);
                    if (card) {
                        fetch(`/vehicle-partial/${e.vehicle.id}?t=${Date.now()}`)
                            .then(r => r.text())
                            .then(html => {
                                card.outerHTML = html;
                            });
                    }
                });
        });
    </script>
@endpush
</x-app-layout>