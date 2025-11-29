

Phase 1: One-Time Project Installation

  You only need to do this once after you've cloned the project.

   1. Clone the Repository (if you haven't already):

   1     git clone <your-repository-url>
   2     cd <project-folder>

   2. Install PHP Dependencies:
      This command reads the composer.json file and installs all the necessary PHP libraries
  for Laravel.

   1     composer install

   3. Install JavaScript Dependencies:
      This command reads the package.json file and installs all the JavaScript libraries
  needed for the frontend, including Laravel Echo and DaisyUI.

   1     npm install

   4. Create and Configure Environment File:
      This creates your local configuration file and then generates a unique, secure
  application key.

   1     cp .env.example .env
   2     php artisan key:generate

   5. Set Up the Database:
      The project is configured to use SQLite, which is a simple file-based database. This
  command creates the empty database file, then builds the table structure and populates it
  with the default user and machines.

   1     touch database/database.sqlite
   2     php artisan migrate:fresh --seed

   6. Build Frontend Assets:
      This command compiles all the JavaScript and CSS using Vite, creating the final asset
  files that will be served to the browser.

   1     npm run build

   7. Install Python Dependencies:
      This installs the Python libraries needed for the Raspberry Pi client script.
   1     pip install requests websocket-client python-dotenv

  Phase 2: Running the Application

  To run the full system for development, you will need 3 separate terminal windows running
  these processes concurrently.

   1. Terminal 1: Start the Laravel Web Server
      This is the main web application.

   1     php artisan serve
      (This will serve your application, typically at `http://127.0.0.1:8000`)

   2. Terminal 2: Start the Reverb WebSocket Server
      This process handles all the real-time connections.
   1     php artisan reverb:start
      (Leave this running. You can watch connections and messages here.)

   3. Terminal 3: Start the Python Client (Simulated Machine)
      This simulates a Raspberry Pi connecting to your Laravel application. It will read its
  configuration from your .env file.

   1     python clients/python/pi_client.py
      (Leave this running. You will see it send status heartbeats and receive commands in
  this window.)

  How to Use and Test:

   1. With all three processes running, open your web browser and go to the URL from the php
      artisan serve command (e.g., http://127.0.0.1:8000/dashboard).
   2. Log in with the default user: test@example.com / password.
   3. You should see the dashboard with your machines. Within a couple of seconds, you will
      see "Machine 1" switch to "Online" as the Python client sends its first heartbeat.
   4. Click the control buttons on the "Machine 1" card and watch the output in Terminal 3
      to see the commands being received in real-time.


