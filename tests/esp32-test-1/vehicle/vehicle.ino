#include "config.h"
#include <WiFi.h>
#include <WebSocketsClient.h>
#include "VehicleControl.h"
#include "DisplayHandler.h"
#include "MatrixHandler.h"

DisplayHandler displayHandler;
MatrixHandler matrixHandler;
WebSocketsClient webSocket;

unsigned long lastStatus = 0;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED:
      Serial.printf("[WSc] Disconnected!\n");
      displayHandler.showMessage("WebSocket\nDisconnected");
      matrixHandler.drawFrown();
      break;
    case WStype_CONNECTED:
      Serial.printf("[WSc] Connected to url: %s\n", payload);
      displayHandler.showMessage("WebSocket\nConnected");
      matrixHandler.drawSmile();
      webSocket.sendTXT("{\"action\":\"subscribe\",\"topic\":\"vehicle/1/cmd\"}");
      break;
    case WStype_TEXT:
      Serial.printf("[WSc] get text: %s\n", payload);
      JsonDocument doc;
      if (deserializeJson(doc, payload) == DeserializationError::Ok) {
        vehicleHandleJson(doc);
      } else {
        Serial.println("Warning: [JSON parse failed]");
      }
      break;
    case WStype_BIN:
    case WStype_ERROR:
    case WStype_FRAGMENT_TEXT_START:
    case WS_type_FRAGMENT_BIN_START:
    case WStype_FRAGMENT:
    case WStype_FRAGMENT_FIN:
      break;
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("RC Car starting...");

  displayHandler.setup();
  displayHandler.showMessage("Starting...");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi ");
  displayHandler.showMessage("Connecting\nWiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  displayHandler.showMessage("IP:\n" + WiFi.localIP().toString());

  matrixHandler.setup();
  matrixHandler.drawSmile();

  vehicleSetup();

  webSocket.begin(WEBSOCKET_URL);
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
}

void loop() {
  webSocket.loop();
  vehicleLoop();

  if (millis() - lastStatus > 2000) {
    lastStatus = millis();
    if (webSocket.isConnected()) {
        vehiclePublishStatus(webSocket);
    }
  }
}
