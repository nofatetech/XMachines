<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use PHP\MQTT\Client;

class MqttToReverbBridge extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'app:mqtt-to-reverb-bridge';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        //
        $mqtt = new Client('127.0.0.1', 1883, 'laravel-bridge');
        $mqtt->connect();

        $mqtt->subscribe('sensors/#', function ($topic, $message) {
            // Forward every MQTT message to the browser via Reverb
            broadcast(new \App\Events\TestBroadcast("MQTT → $topic: $message"));
            $this->info("MQTT → $topic: $message");
        });

        $this->info("MQTT → Reverb bridge running. Listening on sensors/#");
        $mqtt->loop(true); // runs forever
    }
}
