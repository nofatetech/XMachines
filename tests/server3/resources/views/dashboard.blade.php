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
                    <div class="flex" style="height: 60vh;">
                        <!-- Main 3D Scene -->
                        <div id="scene-container" class="flex-grow bg-gray-900 rounded-lg mr-4">
                            <!-- Three.js canvas will be injected here -->
                        </div>

                        <!-- Sidebar for Machine Details -->
                        <div id="machine-details-sidebar" class="w-1/3 bg-gray-700 p-4 rounded-lg hidden">
                            <h3 id="sidebar-title" class="text-lg font-bold text-white mb-4">Select a Machine</h3>
                            <div id="sidebar-content" class="text-white">
                                <!-- Machine details will be populated here -->
                            </div>
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
