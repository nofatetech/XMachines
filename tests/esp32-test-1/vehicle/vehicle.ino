#include "config.h"
#include <WiFi.h>
#include "MqttHandler.h"
#include "VehicleControl.h"
#include "DisplayHandler.h" // Include DisplayHandler

DisplayHandler displayHandler; // Create DisplayHandler instance

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

  vehicleSetup();
  setupMqtt();
}

void loop() {
  handleMqtt();          // now safe – WiFi is up
  vehicleLoop();

  if (millis() - lastStatus > 2000) {
    lastStatus = millis();
    if (client.connected()) {
      vehiclePublishStatus(client);
      displayHandler.showMessage("MQTT Connected\nRunning..."); // Display MQTT status
    } else {
      displayHandler.showMessage("MQTT Disconnected\nWaiting..."); // Display MQTT disconnected status
    }
  }
}
