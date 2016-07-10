#include <Wire.h>
#include "Adafruit_MCP23017.h"
#include "Joystick.h"

// Set the information about the Joystick being implemented
uint8_t hidReportId = 0x03;  // Joystick type HID
uint8_t buttonCount = 64;
uint8_t hatSwitchCount = 0;
bool includeXAxis = false;
bool includeYAxis = false;
bool includeZAxis = false;
bool includeRxAxis = false;
bool includeRyAxis = false;
bool includeRzAxis = false;
bool includeRudder = false;
bool includeThrottle = false;
bool includeAccelerator = false;
bool includeBrake = false;
bool includeSteering = false;

// Create an array of four MCP23017 objects
Adafruit_MCP23017 MCP[4];
// Create the joystick object, providing info above
Joystick_ myJoystick(hidReportId, buttonCount, hatSwitchCount, includeXAxis, includeYAxis, includeZAxis, includeRxAxis, includeRyAxis, includeRzAxis, includeRudder, includeThrottle, includeAccelerator, includeBrake, includeSteering);

void setup() {  
  // Initialise the joystick
  myJoystick.begin();
  for (int mcpIndex = 0; mcpIndex < 4; mcpIndex++){
    // Initialise the MCP ICs, setting their hardwired addresses
    MCP[mcpIndex].begin(mcpIndex);
    for (int inputIndex = 0; inputIndex < 16; inputIndex++){
      // Set all the pins to be inputs with internal pullup resistors
      MCP[mcpIndex].pinMode(inputIndex, INPUT); 
      MCP[mcpIndex].pullUp(inputIndex, HIGH);
    }
  }
}

// Array to keep track of the MCP pins' states
bool lastInputState[4][16] = {{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
                              {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
                              {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
                              {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}};

// Array which tells us if a specific pin need to be inverted
// when read (momentary-on vs. momentary-off)
bool invertInput[4][16]    = {{0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0},
                              {1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0},
                              {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
                              {0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1}};

void loop() {
  for (int mcpIndex = 0; mcpIndex < 4; mcpIndex++){
    for (int inputIndex = 0; inputIndex < 16; inputIndex++){
      // Read each pin state
      bool currentInputState = MCP[mcpIndex].digitalRead(inputIndex);
      // Invert the pin's state if necessary
      if (invertInput[mcpIndex][inputIndex]){
        currentInputState = !currentInputState;
      }
      if (lastInputState[mcpIndex][inputIndex] != currentInputState) {
        // If the state has changed, report that the joystick button state 
        // which represents that pin has changed
        myJoystick.setButton(((mcpIndex * 16) + inputIndex), currentInputState);
        // Set the state for the next read to compare against
        lastInputState[mcpIndex][inputIndex] = currentInputState;
      }
    }
  }
  // Slow it down to 50Hz
  delay(20);
}
