<?php

namespace App\Vehicle;

use App\Models\Vehicle;
use PhpMqtt\Client\MqttClient;
use PhpMqtt\Client\ConnectionSettings;

class Engine
{
    private MqttClient $mqtt;
    private Vehicle $vehicle;
    private string $vehicle_topic;

    /**
     * Engine constructor.
     *
     * @param Vehicle $vehicle The vehicle model this engine controls.
     */
    public function __construct(Vehicle $vehicle)
    {
        $this->vehicle = $vehicle;
        $this->vehicle_topic = "vehicles/{$this->vehicle->id}/command";

        $server   = config('mqtt.host');
        $port     = config('mqtt.port');
        $clientId = config('mqtt.client_id') . '_engine_' . uniqid();
        $username = config('mqtt.username');
        $password = config('mqtt.password');

        $this->mqtt = new MqttClient($server, $port, $clientId);
        
        $connectionSettings = (new ConnectionSettings)
            ->setUsername($username)
            ->setPassword($password);

        $this->mqtt->connect($connectionSettings, true);
    }

    /**
     * Publishes a command to the vehicle's MQTT topic.
     *
     * @param array $payload
     */
    private function publishCommand(array $payload): void
    {
        $this->mqtt->publish($this->vehicle_topic, json_encode($payload), 0);
    }

    /**
     * Moves the vehicle in a given direction for a duration.
     *
     * @param string $direction 'forward' or 'backward'
     * @param int $duration    In seconds
     */
    public function move(string $direction = 'forward', int $duration = 1): void
    {
        $this->publishCommand(['action' => 'move', 'direction' => $direction]);
        sleep($duration);
        $this->publishCommand(['action' => 'stop']);
    }

    /**
     * Turns the vehicle.
     *
     * @param string $direction 'left' or 'right'
     */
    public function turn(string $direction = 'left'): void
    {
        $this->publishCommand(['action' => 'turn', 'direction' => $direction]);
    }

    /**
     * Controls the vehicle's lights.
     *
     * @param string $light  e.g., 'headlights', 'left_blinker'
     * @param string $status 'on' or 'off'
     */
    public function setLights(string $light, string $status = 'on'): void
    {
        $this->publishCommand(['action' => 'lights', 'light' => $light, 'status' => $status]);
    }

    /**
     * Pauses execution for a number of seconds.
     *
     * @param int $seconds
     */
    public function wait(int $seconds = 1): void
    {
        sleep($seconds);
    }

    /**
     * Gets data from a vehicle's sensor.
     * Note: This is a placeholder. A real implementation would require a
     * request/response pattern over MQTT, which is more complex.
     *
     * @param string $sensorName
     * @return mixed
     */
    public function getSensorData(string $sensorName)
    {
        // Placeholder: In a real system, you would publish a request to a sensor topic
        // and wait for a response on a reply topic.
        switch ($sensorName) {
            case 'temperature':
                return 25; // Dummy value
            case 'battery':
                return $this->vehicle->energy ?? 100; // Return real value if available
            default:
                return null;
        }
    }

    /**
     * Disconnects the MQTT client.
     */
    public function __destruct()
    {
        $this->mqtt->disconnect();
    }
}
