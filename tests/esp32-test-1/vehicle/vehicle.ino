#include "config.h"
#include <WiFi.h>
#include "MqttHandler.h"
#include "VehicleControl.h"
#include "DisplayHandler.h" // Include DisplayHandler
#include "MatrixHandler.h" // Add this

DisplayHandler displayHandler; // Create DisplayHandler instance
MatrixHandler matrixHandler; // Create MatrixHandler instance

unsigned long lastStatus = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("RC Car starting...");

  displayHandler.setup(); // Setup the display
  displayHandler.showMessage("Starting..."); // Initial message

  // === Connect to WiFi FIRST ===
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi ");
  displayHandler.showMessage("Connecting\nWiFi..."); // Display WiFi connection status
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  displayHandler.showMessage("IP:\n" + WiFi.localIP().toString()); // Display IP address after connection

  matrixHandler.setup(); // Setup the matrix
  matrixHandler.drawSmile(); // Initial happy face

  vehicleSetup();
  setupMqtt();
}

void loop() {
  handleMqtt();
  vehicleLoop();

  if (millis() - lastStatus > 2000) {
    lastStatus = millis();
    if (client.connected()) {
      vehiclePublishStatus(client);
      displayHandler.showMessage("MQTT Connected\nRunning..."); // Display MQTT status
      matrixHandler.drawSmile(); // Happy face
    } else {
      displayHandler.showMessage("MQTT Disconnected\nWaiting..."); // Display MQTT disconnected status
      matrixHandler.drawFrown(); // Sad face
    }
  }
}
