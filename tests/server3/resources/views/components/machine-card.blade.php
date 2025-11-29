<div id="machine-{{ $machine->id }}" class="card bg-base-100 shadow-xl">
    <div class="card-body">
        <h2 class="card-title">{{ $machine->name }}</h2>
        <p class="text-sm text-gray-500">UUID: {{ $machine->uuid }}</p>
        @isset($localIp)
            <p class="text-sm text-gray-500">Local IP: {{ $localIp }}</p>
        @endisset
        <p>Status: <span id="status-{{ $machine->id }}" class="badge {{ $machine->is_online ? 'badge-success' : 'badge-error' }}">{{ $machine->is_online ? 'Online' : 'Offline' }}</span></p>
        <div class="grid grid-cols-2 gap-2 text-sm">
            <p>Temp: <span id="temp-{{ $machine->id }}">{{ $machine->temperature }}</span>°C</p>
            <p>Lights: <span id="lights-{{ $machine->id }}">{{ $machine->lights_on ? 'On' : 'Off' }}</span></p>
            <p>L Motor: <span id="motor-left-{{ $machine->id }}">{{ $machine->motor_left_speed }}</span>%</p>
            <p>R Motor: <span id="motor-right-{{ $machine->id }}">{{ $machine->motor_right_speed }}</span>%</p>
            <p>Fog: <span id="fog-lights-{{ $machine->id }}">{{ $machine->fog_lights_on ? 'On' : 'Off' }}</span></p>
            <p>Happiness: <span id="happiness-{{ $machine->id }}">{{ $machine->happiness }}</span></p>
            <p>Hunger: <span id="hunger-{{ $machine->id }}">{{ $machine->hunger }}</span></p>
            <p>Auto-Driving: <span id="auto-driving-{{ $machine->id }}">{{ $machine->is_auto_driving ? 'On' : 'Off' }}</span></p>
        </div>

        <!-- NEW: Mind State Panel -->
        <div class="mt-4 pt-4 border-t border-base-300">
            <h3 class="text-xs uppercase font-bold text-gray-400 mb-2">Mind State</h3>
            <div class="flex items-center gap-4">
                <!-- Mood Orb -->
                <div class="flex-shrink-0">
                    <div id="mood-orb-{{ $machine->id }}"
                         class="w-16 h-16 rounded-full transition-all duration-500
                                {{ $machine->is_online ? 'bg-green-500' : 'bg-red-500' }}
                                {{ $machine->is_auto_driving ? 'animate-pulse-fast' : 'animate-pulse-normal' }}">
                    </div>
                </div>
                <div class="flex-grow">
                    <!-- Last Thoughts Ticker -->
                    <div class="text-xs text-gray-500">Last Thoughts:</div>
                    <p id="last-thought-1-{{ $machine->id }}" class="text-sm italic">"Awaiting input..."</p>
                    <p id="last-thought-2-{{ $machine->id }}" class="text-sm italic text-gray-400">"..."</p>
                    <p id="last-thought-3-{{ $machine->id }}" class="text-sm italic text-gray-400">"..."</p>
                    <!-- Imagination Frame (Placeholder) -->
                    <div id="imagination-frame-{{ $machine->id }}" class="w-full h-24 bg-base-200 mt-2 rounded flex items-center justify-center hidden">
                         <span class="text-xs text-gray-500">Imagination will appear here.</span>
                    </div>
                </div>
            </div>
        </div>

        @isset($showControls)
            <div class="card-actions justify-end mt-4">
                <button class="btn btn-primary btn-sm control-btn" data-machine-id="{{ $machine->id }}" data-command="toggle_lights">Toggle Lights</button>
                <button class="btn btn-secondary btn-sm control-btn" data-machine-id="{{ $machine->id }}" data-command="toggle_fog_lights">Toggle Fog</button>
                <button class="btn btn-info btn-sm control-btn" data-machine-id="{{ $machine->id }}" data-command="toggle_auto_driving">Toggle Auto Drive</button>
                <button class="btn btn-success btn-sm control-btn" data-machine-id="{{ $machine->id }}" data-command="feed">Feed</button>
                <button class="btn btn-warning btn-sm control-btn" data-machine-id="{{ $machine->id }}" data-command="play">Play</button>
                <button class="btn btn-ghost btn-sm ask-llm-btn" data-machine-id="{{ $machine->id }}" onclick="document.getElementById('llm_modal_{{ $machine->id }}').showModal()">Ask LLM</button>
            </div>

            <!-- LLM Modal -->
            <dialog id="llm_modal_{{ $machine->id }}" class="modal">
                <div class="modal-box">
                    <h3 class="font-bold text-lg">Ask Machine {{ $machine->name }} (ID: {{ $machine->id }})</h3>
                    <p class="py-4">Enter your question for the machine's local LLM:</p>
                    <input type="text" placeholder="e.g., What is my current temperature?" class="input input-bordered w-full mb-4" id="llm_question_input_{{ $machine->id }}" />
                    <div class="llm-loading-spinner_{{ $machine->id }} hidden text-center mb-4">
                        <span class="loading loading-spinner loading-lg"></span>
                        <p>Machine {{ $machine->name }} is thinking...</p>
                    </div>
                    <div class="llm-response-display_{{ $machine->id }} hidden border rounded-md p-2 bg-base-200 text-sm overflow-auto max-h-40">
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

<style>
    @keyframes pulse-normal {
        0%, 100% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(1.05);
            opacity: 0.8;
        }
    }

    @keyframes pulse-fast {
        0%, 100% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(1.07);
            opacity: 0.7;
        }
    }

    .animate-pulse-normal {
        animation: pulse-normal 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    .animate-pulse-fast {
        animation: pulse-fast 1s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
</style>
