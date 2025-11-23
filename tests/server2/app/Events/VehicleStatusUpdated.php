<?php

namespace App\Events;

use App\Models\Vehicle;
use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class VehicleStatusUpdated 
implements ShouldBroadcastNow //
{
    // use Dispatchable, InteractsWithSockets, SerializesModels;
    use Dispatchable, InteractsWithSockets;

    /**
     * Create a new event instance.
     */
    public function __construct(public Vehicle $vehicle)
    {
        //
    }

    /**
     * Get the channels the event should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel>
     */
    public function broadcastOn(): array
    {
        // return [
        //     new PrivateChannel('channel-name'),
        // ];
        return [new Channel('public')];
    }

    public function broadcastWith(): array
    {
        return [
            'vehicle' => $this->vehicle->loadMissing('id', 'name', 'status', 'batt', 'left', 'right', 'highbeam', 'fog', 'hazard', 'last_seen', 'raw_status')
        ];
    }
}
