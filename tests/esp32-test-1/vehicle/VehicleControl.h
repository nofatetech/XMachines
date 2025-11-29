#ifndef VEHICLE_CONTROL_H
#define VEHICLE_CONTROL_H

#include <ArduinoJson.h>

class WebSocketsClient;

void vehicleSetup();
void vehicleLoop();
void vehicleHandleJson(JsonDocument& doc);
void vehiclePublishStatus(WebSocketsClient& client);

#endif
