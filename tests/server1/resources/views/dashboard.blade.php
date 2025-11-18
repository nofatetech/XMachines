@extends('layout1')

@section('content')

<div>
    Server IP: 
    <div>{{ $localIp }}</div>
</div>

<ul>
    @foreach($vehicles as $vehicle)
        <li data-vehicle-id="{{ $vehicle->id }}">
            {{ $vehicle->name }}: {{ $vehicle->status }}
            <div>
                <div style="background-color: #333333; border-radius: 15px; padding: 20px; width: 400px; margin: auto; box-shadow: 5px 5px 15px rgba(0,0,0,0.5);">
                    <table style="border-collapse: collapse; width: 100%;">
                        <tr>
                            <td colspan="3" style="width: 33%;"></td>
                            <td style="text-align: center; width: 33%;">
                                <button class="control-button" data-action="forward" style="background-color: #666666; color: white; border: none; padding: 10px 15px; border-radius: 5px; font-weight: bold; width: 50px; height: 40px;">Forward</button>
                            </td>
                            <td colspan="4" style="width: 33%;"></td>
                        </tr>
                        <tr>
                            <td colspan="2" style="width: 22%;"></td>
                            <td style="text-align: center; width: 11%;">
                                <button class="control-button" data-action="turn_left" style="background-color: #666666; color: white; border: none; padding: 10px 15px; border-radius: 5px; font-weight: bold; width: 50px; height: 40px;">Left</button>
                            </td>
                            <td style="width: 11%;"></td>
                            <td style="text-align: center; width: 11%;">
                                <button class="control-button" data-action="turn_right" style="background-color: #666666; color: white; border: none; padding: 10px 15px; border-radius: 5px; font-weight: bold; width: 50px; height: 40px;">Right</button>
                            </td>
                            <td colspan="3" style="width: 45%;"></td>
                        </tr>
                        <tr>
                            <td colspan="3" style="width: 33%;"></td>
                            <td style="text-align: center; width: 33%;">
                                <button class="control-button" data-action="back" style="background-color: #666666; color: white; border: none; padding: 10px 15px; border-radius: 5px; font-weight: bold; width: 50px; height: 40px;">Back</button>
                            </td>
                            <td colspan="4" style="width: 33%;"></td>
                        </tr>
                        <tr>
                            <td colspan="8" style="height: 30px;"></td>
                        </tr>
                        <tr>
                            <td colspan="2"></td>
                            <td colspan="4" style="text-align: center;">
                                <button style="background-color: #666666; color: white; border: none; padding: 5px 10px; border-radius: 3px; font-size: 0.8em;">Select</button>
                                <button style="background-color: #666666; color: white; border: none; padding: 5px 10px; border-radius: 3px; font-size: 0.8em;">Start</button>
                            </td>
                            <td colspan="2"></td>
                        </tr>
                        <tr>
                            <td colspan="8" style="height: 30px;"></td>
                        </tr>
                        <tr>
                            <td colspan="6"></td>
                            <td style="text-align: center;">
                                <button style="background-color: #CC0000; color: white; border: none; width: 50px; height: 50px; border-radius: 50%; font-weight: bold; font-size: 1.2em;">A</button>
                            </td>
                            <td style="text-align: center;">
                                <button style="background-color: #CC0000; color: white; border: none; width: 50px; height: 50px; border-radius: 50%; font-weight: bold; font-size: 1.2em;">B</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
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
                        console.log('Command sent:', response);
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
    });
</script>
@endsection