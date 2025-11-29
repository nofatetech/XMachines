#include <cstdint>
#ifndef CONFIG_H
#define CONFIG_H

extern const char* WIFI_SSID;
extern const char* WIFI_PASSWORD;

extern const char* WEBSOCKET_URL;

// --- Pinout Configuration ---

// Vehicle Motors (28BYJ-48 + ULN2003)
#define LEFT_IN1  17
#define LEFT_IN2  18
#define LEFT_IN3  27
#define LEFT_IN4  22

#define RIGHT_IN1 23
#define RIGHT_IN2 24
#define RIGHT_IN3 25
#define RIGHT_IN4 8

// Lights & accessories
#define PIN_MAIN_LIGHTS   5   // Headlights + taillights together
#define PIN_FOG_LIGHTS    6
#define PIN_HIGH_BEAMS    13
#define PIN_LEFT_BLINKER  26
#define PIN_RIGHT_BLINKER 16
#define PIN_HORN          20

// Optional sensor
#define PIN_BATTERY       34
#define VREF              3.3f
#define DIVIDER_RATIO     2.0f

#endif
