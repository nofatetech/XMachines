#include "DisplayHandler.h"

DisplayHandler::DisplayHandler() : 
  display(SCREEN_WIDTH, SCREEN_HEIGHT, OLED_MOSI, OLED_CLK, OLED_DC, OLED_RST, OLED_CS) {
}

void DisplayHandler::setup() {
    // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
    if(!display.begin(SSD1306_SWITCHCAPVCC)) { 
        Serial.println(F("SSD1306 allocation failed"));
        for(;;); // Don't proceed, loop forever
    }
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0,0);
    display.println(F("Display ready."));
    display.display();
}

void DisplayHandler::showMessage(const String& message) {
    display.clearDisplay();
    display.setCursor(0,0);
    display.println(message);
    display.display();
}

void DisplayHandler::clear() {
    display.clearDisplay();
    display.display();
}
