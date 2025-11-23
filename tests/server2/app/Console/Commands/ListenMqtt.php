<?php

namespace App\Console\Commands;

use App\Events\VehicleStatusUpdated;
use App\Models\Vehicle;
use Illuminate\Console\Command;
use PhpMqtt\Client\MqttClient;
use PhpMqtt\Client\ConnectionSettings;

class ListenMqtt extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mqtt:listen';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Listen for MQTT messages from vehicles';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $server   = config('mqtt.host');
        $port     = config('mqtt.port');
        $clientId = config('mqtt.client_id') . '_server_' . uniqid();
        $username = config('mqtt.username');
        $password = config('mqtt.password');

        $mqtt = new MqttClient($server, $port, $clientId);

        $connectionSettings = (new ConnectionSettings)
            ->setUsername($username)
            ->setPassword($password);

        $mqtt->connect($connectionSettings, true);
        $this->info("MQTT client connected and listening for messages...");

        // Subscribe to the topic where all vehicles publish their status
        $mqtt->subscribe('vehicle/+/status', function ($topic, $message) {
            $this->info("Received message on topic [{$topic}]: {$message}");

            $data = json_decode($message, true);
            $topicParts = explode('/', $topic);
            $vehicleId = $topicParts[1];

            $this->info("DEBUG: Extracted vehicleId: {$vehicleId}");

            // Use the vehicle's ID from the payload to update its record
            // in the server's database.
            if ($vehicleId) {
                $this->info("DEBUG: Inside if(\$vehicleId) block for vehicle #{$vehicleId}");


                $vehicle = \App\Models\Vehicle::findOrFail($vehicleId);

                $vehicle->update([
                    'raw_status' => $payload,
                    'batt'       => $payload['batt'] ?? null,
                    'left'       => $payload['left'] ?? 0,
                    'right'      => $payload['right'] ?? 0,
                    'highbeam'   => $payload['highbeam'] ?? false,
                    'fog'        => $payload['fog'] ?? false,
                    'hazard'     => $payload['hazard'] ?? false,
                    'last_seen'  => now(),
                ]);

                broadcast(new \App\Events\VehicleStatusUpdated($vehicle));

                $this->info("Vehicle {$vehicleId} updated → batt: {$payload['batt']}V");





                // $fillableData = [];
                // $vehicleFillable = (new Vehicle())->getFillable();

                // foreach ($data as $key => $value) {
                //     if (in_array($key, $vehicleFillable)) {
                //         $fillableData[$key] = $value;
                //     }
                // }

                // Vehicle::updateOrCreate(
                //     ['id' => $vehicleId], // Find vehicle by its unique ID
                //     $fillableData          // Update with only fillable data from the payload
                // );
                // $this->info("Updated vehicle #{$vehicleId}");

                // $this->info("DEBUG: Attempting to dispatch VehicleStatusUpdated event for vehicle #{$vehicleId}");
                // try {
                //     // Fire the event to broadcast the telemetry data to the frontend
                //     VehicleStatusUpdated::dispatch(
                //         $vehicleId,
                //         $data['left'] ?? null,
                //         $data['right'] ?? null,
                //         $data['batt'] ?? null,
                //         $data['highbeam'] ?? null,
                //         $data['fog'] ?? null,
                //         $data['hazard'] ?? null,
                //         $data['status'] ?? null,
                //         $data['wifi'] ?? null,
                //         $data['energy'] ?? null,
                //         $data['happiness'] ?? null,
                //         $data['ai_detected_objects'] ?? null
                //     );
                //     $this->info("Dispatched VehicleStatusUpdated event for vehicle #{$vehicleId}");
                // } catch (\Throwable $e) { // Catch Throwable instead of just Exception
                //     $this->error("ERROR: Failed to dispatch VehicleStatusUpdated event for vehicle #{$vehicleId}. Throwable: " . $e->getMessage());
                //     $this->error($e->getTraceAsString()); // Log full trace for more details
                // }
            }
        }, 0);

        // // Subscribe to the topic where control commands are published
        // $mqtt->subscribe('vehicle/+/control', function ($topic, $message) {
        //     $this->info("Received control command on topic [{$topic}]: {$message}");
        //     // At this point, the command has been published.
        //     // The actual vehicle is expected to subscribe to this topic directly.
        //     // We are just logging it here for visibility within the Laravel app.
        //     $data = json_decode($message, true);
        //     $vehicleId = explode('/', $topic)[1]; // Extract vehicle ID from topic
        //     if (isset($data['action'])) {
        //         // $this->info("Vehicle #{$vehicleId} - Action: {$data['action']}, Speed: {$data['speed'] ?? 'N/A'}");

        //         $speed = isset($data['speed']) ? $speed = $data['speed'] : 'N/A';
        //         $this->info("Vehicle #{$vehicleId} - Action: {$data['action']}, Speed: {$speed}");

        //         // Further actions can be added here, e.g., logging to a database,
        //         // updating UI in real-time if a WebSocket server is running.
        //     }
        // }, 0);

        
        $this->info("MQTT bridge listening on vehicle/+/status");
        // $mqtt->loopForever();
        
        $mqtt->loop(true);


    }
}
