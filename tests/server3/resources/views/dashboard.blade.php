<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">
            {{ __('Dashboard') }}
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6 text-gray-900 dark:text-gray-100">
                    {{ __("You're logged in!") }}

                    <div class="mt-4">
                        <p>WebSocket Server: <span id="websocket-server">localhost:8080</span></p>
                        <p>WebSocket Status: <span id="websocket-status" class="font-bold">Connecting...</span></p>
                    </div>

                    <div class="mt-6">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Connected Machines:</h3>
                        <div id="machines-grid" class="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            @foreach($machines as $machine)
                                <x-machine-card :machine="$machine" :showControls="true" />
                            @endforeach
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    @push('scripts')
        <script>
            // Expose machine data to the global window object
            window.xMachines = @json($machines);
        </script>
    @endpush
</x-app-layout>
