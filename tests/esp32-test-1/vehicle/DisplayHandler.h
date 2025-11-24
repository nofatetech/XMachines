#ifndef DISPLAYHANDLER_H
#define DISPLAYHANDLER_H

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "config.h"

class DisplayHandler {
public:
    DisplayHandler();
    void setup();
    void showMessage(const String& message);
    void clear();

private:
    Adafruit_SSD1306 display;
};

#endif // DISPLAYHANDLER_H
