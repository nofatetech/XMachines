#ifndef MATRIXHANDLER_H
#define MATRIXHANDLER_H

#include "config.h"
#include <Wire.h>
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"

class MatrixHandler {
public:
    MatrixHandler();
    void setup();
    void loop(); // Added for potential future animations
    void drawSmile();
    void drawFrown();
    void clear();

private:
    Adafruit_BicolorMatrix matrix; // Correct class for bi-color
};

#endif // MATRIXHANDLER_H
