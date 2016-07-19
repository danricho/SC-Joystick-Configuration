import gremlin      # 'Coz it's a Joystick Gremlin module!
import time         # Used for delays between actions in some functions
import threading    # Threading allows the longer functions to be non-blocking
import logging      # Used for logging events and debugging
from configuration import *   # Holds the Joysticks IDs and other constants

''' "Slider Update" function
 Purpose: Forces a read of the current Slider positions of the joysticks then
          sets the positions to the corresponding vJoy sliders
 Notes:   The constants LEFT_SLIDER_UPDATE and RIGHT_SLIDER_UPDATE control
          control whether these functions are performed.
          This functionalilty is not desirable if a manual increment and 
          decrement throttle is mapped to a button press as the value will be 
          overwritten every time this is run.                               '''
def slider_update(vjoy, joy):
  if LEFT_SLIDER_UPDATE:
    # Read physical left Slider
    left_value = joy[2].axis(4).value      
    # Add some jitter and set virtual left slider
    if (left_value < 0.998):      
      vjoy[1].axis(7).value = (left_value + 0.002) 
    else:
      vjoy[1].axis(7).value = (left_value - 0.002) 
    time.sleep(0.1)
    # Set the the virtual slider to the clean value
    vjoy[1].axis(7).value = left_value      
  if RIGHT_SLIDER_UPDATE:
    # Read physical right Slider
    right_value = joy[0].axis(4).value
    # Add some jitter and set virtual right slider
    if (right_value < 0.998):
      vjoy[2].axis(7).value = (right_value + 0.002) 
    else:
      vjoy[2].axis(7).value = (right_value - 0.002) 
    time.sleep(0.1)
    # Set the the virtual slider to the clean value
    vjoy[2].axis(7).value = right_value

# Periodic Function, every 0.5 seconds
@gremlin.input_devices.periodic(0.5)
def periodic_half_second(vjoy, joy):
  slider_update(vjoy, joy)


'''============================================================================
LOGGING
-------
Adding a log entry into the log window of the JG GUI:
  logging.getLogger("system").debug("System log entry.")
  logging.getLogger("user").debug("User log entry.")
Generating a popup:
  gremlin.util.display_error("Error popup")
============================================================================'''