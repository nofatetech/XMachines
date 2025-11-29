#include "MatrixHandler.h"

MatrixHandler::MatrixHandler() : matrix() {
}

void MatrixHandler::setup() {
    Wire.begin(); // Initialize with default I2C pins (21, 22)
    matrix.begin(0x70); // Default I2C address for HT16K33
    matrix.setRotation(1); // Adjust rotation if needed
    matrix.clear();
    matrix.writeDisplay();
}

void MatrixHandler::loop() {
    // Placeholder for potential future animations or updates
}

void MatrixHandler::clear() {
    matrix.clear();
    matrix.writeDisplay();
}

void MatrixHandler::drawSmile() {
    static const uint8_t PROGMEM
      smile_bmp[] =
      { 0b00111100,
        0b01000010,
        0b10100101,
        0b10000001,
        0b10100101,
        0b10011001,
        0b01000010,
        0b00111100 };
    matrix.clear();
    matrix.drawBitmap(0, 0, smile_bmp, 8, 8, LED_GREEN); // Green smile
    matrix.writeDisplay();
}

void MatrixHandler::drawFrown() {
    static const uint8_t PROGMEM
      frown_bmp[] =
      { 0b00111100,
        0b01000010,
        0b10100101,
        0b10000001,
        0b10011001,
        0b10100101,
        0b01000010,
        0b00111100 };
    matrix.clear();
    matrix.drawBitmap(0, 0, frown_bmp, 8, 8, LED_RED); // Red frown
    matrix.writeDisplay();
}

