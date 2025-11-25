



Run

composer run dev
npm run build && php artisan serve
php artisan mqtt:listen
php artisan reverb:start --host=127.0.0.1 --port=8080


Reset

npm install && npm run build

php artisan config:clear
php artisan cache:clear
composer dump-autoload

│ php artisan clear-compiled && php artisan cache:clear && php artisan view:clear && php artisan route:clear && php        │
│ artisan config:clear && composer dump-autoload  


Install

composer isntall, update


php artisan vendor:publish --provider="PhpMqtt\Client\MqttClientServiceProvider" --tag="config"



User::create(['name'=>'admin','email'=>'admin@test.com','password'=>bcrypt('123123')]);


php artisan tinker

event(new App\Events\TestBroadcast("It works 100% locally!"));

$vehicle = \App\Models\Vehicle::find(1);
$vehicle->batt = 4.50;
$vehicle->left = 1;
$vehicle->right = 0;
$vehicle->highbeam = true;
$vehicle->last_seen = now();
$vehicle->save();
event(new \App\Events\VehicleStatusUpdated($vehicle));
broadcast(new \App\Events\VehicleStatusUpdated($vehicle));







ESP32 / Arduino


# Auto-detect the port (works 99 % of the time)
arduino-cli upload --fqbn esp32:esp32:esp32 --port $(ls /dev/ttyUSB* /dev/ttyACM* | head -1) ~/your_sketch

# Compile + upload + open serial monitor immediately
arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 ~/your_sketch && \
minicom -D /dev/ttyUSB0 -b 115200
# or use screen:
# screen /dev/ttyUSB0 115200


echo "alias espup='arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32'" >> ~/.bashrc
source ~/.bashrc



# Find your ESP32 port (usually /dev/ttyUSB0 or /dev/ttyACM0)
ls /dev/ttyUSB* /dev/ttyACM*

# Compile only (optional, to check errors)
arduino-cli compile --fqbn esp32:esp32:esp32 /home/user1/Documents/dev/XMachines/gitrepo_XMachines/tests/esp32-test-1/vehicle

# Compile + upload in one command (most common)
arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 /home/user1/Documents/dev/XMachines/gitrepo_XMachines/tests/esp32-test-1/vehicle










✦ To migrate this project's functionality to a fresh Laravel install:

   1. Setup:
       * Perform a laravel new project-name.
       * Install laravel/reverb and any other Composer packages (e.g., php-mqtt/client).
       * Install frontend dependencies: npm install.

   2. Backend Core:
       * Database: Copy database/migrations/* and database/seeders/*. Run php artisan migrate
         --seed.
       * Models: Copy app/Models/Vehicle.php (and User.php if modified).
       * Controllers: Copy custom controllers from app/Http/Controllers/.
       * Routes: Merge custom entries from routes/web.php, routes/channels.php.
       * Console Commands: Copy app/Console/Commands/ListenMqtt.php,
         app/Console/Commands/VehicleLive.php.
       * Events: Copy app/Events/VehicleStatusUpdated.php.
       * Config: Copy config/mqtt.php. Merge relevant Reverb settings into config/broadcasting.php
         and config/reverb.php.

   3. Frontend:
       * Views: Copy resources/views/vehicles/*, resources/views/dashboard.blade.php, and any
         customized layouts or components.
       * JavaScript: Copy resources/js/app.js, resources/js/echo.js, resources/js/bootstrap.js.
       * CSS: Copy resources/css/app.css.
       * Build: Copy tailwind.config.js, postcss.config.js, vite.config.js. Run npm run dev (or npm
         run build).

   4. Environment (`.env`):
       * Update APP_URL, database credentials.
       * Set BROADCAST_CONNECTION=reverb.
       * Configure REVERB_APP_KEY, REVERB_APP_SECRET, REVERB_APP_ID, REVERB_HOST, REVERB_PORT,
         REVERB_SCHEME.
       * Add dummy PUSHER_APP_KEY=ANY_KEY, PUSHER_APP_SECRET=ANY_SECRET, PUSHER_APP_ID=ANY_ID
         (required by Reverb).
       * Configure VITE_ prefixed variables (e.g., VITE_REVERB_APP_KEY, VITE_REVERB_HOST,
         VITE_REVERB_PORT, VITE_REVERB_SCHEME).
       * Configure MQTT_HOST, MQTT_PORT.

   5. Finalize:
       * Run php artisan optimize:clear.
       * Run php artisan reverb:install.
       * Copy gamepad_mqtt_publisher.py to the new project root.
       * Ensure your Mosquitto (MQTT broker) is installed and running.
       * Start Laravel app (php artisan serve), Reverb server (php artisan reverb:start), and Vite
         (npm run dev).

