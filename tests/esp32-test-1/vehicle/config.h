#ifndef CONFIG_H
#define CONFIG_H

extern const char* WIFI_SSID;
extern const char* WIFI_PASSWORD;

extern const char* MQTT_SERVER;
extern uint16_t    MQTT_PORT;
extern const char* MQTT_CLIENT_ID;
extern const char* MQTT_CONTROL_TOPIC;
extern const char* MQTT_STATUS_TOPIC;

// --- Pinout Configuration ---

// Vehicle Motors (No changes)
#define LEFT_IN1    13
#define LEFT_IN2    12
#define LEFT_IN3    14
#define LEFT_IN4    27
#define RIGHT_IN1   26
#define RIGHT_IN2   25
#define RIGHT_IN3   33
#define RIGHT_IN4   32

// Vehicle Lights & Horn (Relocated to free up hardware peripherals)
#define PIN_HORN          15 // Was 23
#define PIN_HIGH_BEAMS    2  // Was 22
#define PIN_FOG_LIGHTS    4  // Was 21
#define PIN_MAIN_LIGHTS   19 // No change
#define PIN_LEFT_BLINKER  12 // Was 18
#define PIN_RIGHT_BLINKER 13 // Was 5

// Vehicle Battery
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

#define VREF           3.3f
#define DIVIDER_RATIO  2.0f

#endif
