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
</x-app-layout>