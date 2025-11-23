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

class VehicleStatusUpdated implements ShouldBroadcastNow
{
    // use Dispatchable, InteractsWithSockets, SerializesModels;
    // use Dispatchable, InteractsWithSockets;
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public Vehicle $vehicle;


    /**
     * Create a new event instance.
     */
    public function __construct(Vehicle $vehicle)
    {
        //
        $this->vehicle = $vehicle;
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
            'vehicle' => $this->vehicle->toArray()
        ];
    }
}
