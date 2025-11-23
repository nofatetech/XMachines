@extends('layout1')

@section('content')

<div>
    Server IP:
    <div>{{ $localIp }}</div>
</div>

<ul class="vehicle-list">
    @foreach($vehicles as $vehicle)
        <li data-vehicle-id="{{ $vehicle->id }}">
            {{ $vehicle->name }}: {{ $vehicle->status }}
            {{-- @include('vehicles.controllers._nes_controller', ['vehicle' => $vehicle]) --}}
            @include('vehicles.controllers._tank_controller', ['vehicle' => $vehicle])

        </li>
    @endforeach
</ul>
<script>
    $(document).ready(function() {
        $('.control-button').on('click', function() {
            const vehicleId = $(this).closest('li').data('vehicle-id');
            const action = $(this).data('action');
            const speed = 0.5; // Default speed, can be made dynamic later

            if (vehicleId && action) {
                $.ajax({
                    url: `/vehicle/${vehicleId}/command`,
                    type: 'POST',
                    data: {
                        action: action,
                        speed: speed,
                        _token: '{{ csrf_token() }}' // Laravel CSRF token
                    },
                    success: function(response) {
                        console.log('Com3i jmand sent:', response);
                        alert('Command sent: ' + response.message);
                    },
                    error: function(xhr, status, error) {
                        console.error('Error sending command:', error);
                        alert('Error sending command: ' + (xhr.responseJSON ? xhr.responseJSON.error : error));
                    }
                });
            } else {
                console.error('Missing vehicle ID or action.');
            }
        });

        // Listen for real-time updates
        $('.vehicle-list li[data-vehicle-id]').each(function() {
            const vehicleId = $(this).data('vehicle-id');

            window.Echo.private(`vehicle-status.${vehicleId}`)
                .listen('.VehicleStatusUpdated', (e) => {
                    console.log('VehicleStatusUpdated event received:', e);

                    // Update status fields
                    if (e.status !== null) {
                        $(`#status-${vehicleId}`).text(e.status);
                    }
                    if (e.battery !== null) {
                        $(`#battery-level-${vehicleId}`).text(e.battery + '%');
                    }
                    if (e.wifi !== null) {
                        $(`#wifi-level-${vehicleId}`).text(e.wifi + '%');
                    }

                    // Update personality fields
                    if (e.energy !== null) {
                        $(`#energy-${vehicleId}`).text(e.energy);
                    }
                    if (e.happiness !== null) {
                        $(`#happiness-${vehicleId}`).text(e.happiness);
                    }

                    // Update AI detected objects
                    if (e.ai_detected_objects !== null && e.ai_detected_objects.length > 0) {
                        const objectsList = $(`#ai-detected-objects-${vehicleId}`);
                        objectsList.empty();
                        e.ai_detected_objects.forEach(obj => {
                            objectsList.append(`<li>${obj.name} (${(obj.confidence * 100).toFixed(1)}%)</li>`);
                        });
                    } else if (e.ai_detected_objects !== null) {
                        $(`#ai-detected-objects-${vehicleId}`).html('<li>-</li>');
                    }
                });
        });
    });
</script>
@endsection