<div id="machine-{{ $machine->id }}" class="card bg-gray-800 shadow-xl border border-gray-700 text-gray-200 h-full flex flex-col">
    <div class="card-body flex flex-col">
        <!-- 3D Visualization Area -->
        <div id="imagination-frame-{{ $machine->id }}" class="imagination-frame w-full h-48 bg-gray-900 rounded-lg mb-4 flex items-center justify-center">
        </div>

        <h2 class="card-title text-xl font-bold text-primary-focus mb-2">{{ $machine->name }}</h2>
        <p class="text-sm text-gray-400 mb-4">UUID: {{ $machine->uuid }}</p>

        <!-- Main Stats Grid -->
        <div class="grid grid-cols-2 gap-y-2 gap-x-4 text-sm mb-4">
            <div class="stat-item">
                <span class="text-gray-500">Status:</span>
                <span id="status-{{ $machine->id }}" class="badge {{ $machine->is_online ? 'badge-success' : 'badge-error' }}">{{ $machine->is_online ? 'Online' : 'Offline' }}</span>
            </div>
            <div class="stat-item">
                <span class="text-gray-500">Temp:</span>
                <span id="temp-{{ $machine->id }}" class="font-bold text-blue-400">{{ $machine->temperature }}</span>°C
            </div>
            <div class="stat-item">
                <span class="text-gray-500">L Motor:</span>
                <span id="motor-left-{{ $machine->id }}" class="font-bold">{{ $machine->motor_left_speed }}</span>%
            </div>
            <div class="stat-item">
                <span class="text-gray-500">R Motor:</span>
                <span id="motor-right-{{ $machine->id }}" class="font-bold">{{ $machine->motor_right_speed }}</span>%
            </div>
            <div class="stat-item">
                <span class="text-gray-500">Lights:</span>
                <span id="lights-{{ $machine->id }}" class="font-bold {{ $machine->lights_on ? 'text-yellow-400' : 'text-gray-500' }}">{{ $machine->lights_on ? 'On' : 'Off' }}</span>
            </div>
            <div class="stat-item">
                <span class="text-gray-500">Fog:</span>
                <span id="fog-lights-{{ $machine->id }}" class="font-bold {{ $machine->fog_lights_on ? 'text-yellow-400' : 'text-gray-500' }}">{{ $machine->fog_lights_on ? 'On' : 'Off' }}</span>
            </div>
        </div>

        <!-- Tamagotchi & Auto-Driving Section -->
        <div class="mt-auto pt-4 border-t border-gray-700 flex items-center justify-between">
            <div class="flex items-center gap-4">
                <!-- Mood Orb - Larger and more prominent -->
                <div class="flex-shrink-0">
                    <div id="mood-orb-{{ $machine->id }}"
                         class="w-20 h-20 rounded-full transition-all duration-500 flex items-center justify-center text-xs font-bold
                                {{ $machine->is_online ? 'bg-green-600' : 'bg-red-600' }}
                                {{ $machine->is_auto_driving ? 'animate-pulse-fast' : 'animate-pulse-normal' }}">
                        <span>{{ $machine->is_online ? 'AWARE' : 'SLEEP' }}</span>
                    </div>
                </div>
                <div class="flex-grow">
                    <p class="text-sm text-gray-400">Happiness: <span id="happiness-{{ $machine->id }}" class="font-bold text-green-400">{{ $machine->happiness }}</span></p>
                    <p class="text-sm text-gray-400">Hunger: <span id="hunger-{{ $machine->id }}" class="font-bold text-red-400">{{ $machine->hunger }}</span></p>
                    <p class="text-sm text-gray-400">Auto-Driving: <span id="auto-driving-{{ $machine->id }}" class="font-bold {{ $machine->is_auto_driving ? 'text-green-400' : 'text-gray-500' }}">{{ $machine->is_auto_driving ? 'On' : 'Off' }}</span></p>
                </div>
            </div>
        </div>

        @isset($showControls)
            <div class="card-actions justify-end mt-4 pt-4 border-t border-gray-700">
                <!-- Grouped Controls -->
                <div class="flex flex-wrap gap-2">
                    <button class="btn btn-sm btn-outline btn-info control-btn" data-machine-id="{{ $machine->id }}" data-command="toggle_lights">Lights</button>
                    <button class="btn btn-sm btn-outline btn-info control-btn" data-machine-id="{{ $machine->id }}" data-command="toggle_fog_lights">Fog</button>
                    <button class="btn btn-sm btn-outline btn-success control-btn" data-machine-id="{{ $machine->id }}" data-command="feed">Feed</button>
                    <button class="btn btn-sm btn-outline btn-warning control-btn" data-machine-id="{{ $machine->id }}" data-command="play">Play</button>
                    <button class="btn btn-sm btn-outline btn-ghost ask-llm-btn" data-machine-id="{{ $machine->id }}" onclick="document.getElementById('llm_modal_{{ $machine->id }}').showModal()">Ask LLM</button>
                </div>
                <!-- Separate Auto-Driving "Gear Shift" -->
                <div class="mt-3 w-full">
                    <button class="btn btn-sm w-full {{ $machine->is_auto_driving ? 'btn-error' : 'btn-accent' }} control-btn" data-machine-id="{{ $machine->id }}" data-command="toggle_auto_driving">
                        {{ $machine->is_auto_driving ? 'Engaged (Click to Disengage)' : 'Engage Auto-Drive' }}
                    </button>
                </div>
            </div>

            <!-- LLM Modal - kept for functionality -->
            <dialog id="llm_modal_{{ $machine->id }}" class="modal">
                <div class="modal-box bg-gray-800 text-gray-200">
                    <h3 class="font-bold text-lg">Ask Machine {{ $machine->name }} (ID: {{ $machine->id }})</h3>
                    <p class="py-4">Enter your question for the machine's local LLM:</p>
                    <input type="text" placeholder="e.g., What is my current temperature?" class="input input-bordered w-full mb-4 bg-gray-700 text-gray-200 border-gray-600" id="llm_question_input_{{ $machine->id }}" />
                    <div class="llm-loading-spinner_{{ $machine->id }} hidden text-center mb-4">
                        <span class="loading loading-spinner loading-lg"></span>
                        <p>Machine {{ $machine->name }} is thinking...</p>
                    </div>
                    <div class="llm-response-display_{{ $machine->id }} hidden border rounded-md p-2 bg-gray-700 text-sm overflow-auto max-h-40">
                        <p>Response will appear in the Pi's terminal.</p>
                    </div>
                    <div class="modal-action">
                        <button class="btn btn-primary send-llm-query-btn" data-machine-id="{{ $machine->id }}">Ask</button>
                        <form method="dialog">
                            <button class="btn">Close</button>
                        </form>
                    </div>
                </div>
            </dialog>
        @endisset
    </div>
</div>
