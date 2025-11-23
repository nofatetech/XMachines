<?php

namespace App\Events;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class VehicleStatusUpdated implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public int $vehicleId,
        public ?int $left = null,
        public ?int $right = null,
        public ?int $batt = null,
        public ?bool $highbeam = null,
        public ?bool $fog = null,
        public ?bool $hazard = null,
        public ?string $status = null,
        public ?int $wifi = null,
        public ?int $energy = null,
        public ?int $happiness = null,
        public ?array $ai_detected_objects = null
    ) {
        //
    }

    /**
     * Get the channels the event should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel>
     */
    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('vehicle-status.' . $this->vehicleId),
        ];
    }

    /**
     * The event's broadcast name.
     */
    public function broadcastAs(): string
    {
        return 'VehicleStatusUpdated';
    }

    /**
     * Get the data to broadcast.
     *
     * @return array
     */
    public function broadcastWith(): array
    {
        return [
            'vehicleStatus' => [
                'id' => $this->vehicleId,
                'left' => $this->left,
                'right' => $this->right,
                'batt' => $this->batt,
                'highbeam' => $this->highbeam,
                'fog' => $this->fog,
                'hazard' => $this->hazard,
                'status' => $this->status,
                'wifi' => $this->wifi,
                'energy' => $this->energy,
                'happiness' => $this->happiness,
                'ai_detected_objects' => $this->ai_detected_objects,
            ]
        ];
    }
}
