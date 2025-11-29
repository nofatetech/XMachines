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

// OLED Display (Hardware SPI)
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_MOSI   23 // HW VSPI
#define OLED_CLK    18 // HW VSPI
#define OLED_CS     5  // HW VSPI
#define OLED_DC     19 // Using PIN_MAIN_LIGHTS pin, was free
#define OLED_RST    27 // Using LEFT_IN4 pin, was free

// LED Matrix (Hardware I2C)
#define I2C_SDA 21 // HW I2C
#define I2C_SCL 22 // HW I2C

#define VREF              3.3f
#define DIVIDER_RATIO     2.0f

#endif
