<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">
            {{ __('Dashboard') }}
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            @foreach ($vehicles as $vehicle)
                <div class="mb-8">
                    <h3 class="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-4">{{ $vehicle->name }} (ID: {{ $vehicle->id }})</h3>
                    <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg">
                        <div class="p-6">
                            @include('vehicles.controllers._tank_controller', ['vehicle' => $vehicle])
                        </div>
                    </div>
                </div>
            @endforeach
        </div>
    </div>
</x-app-layout>
