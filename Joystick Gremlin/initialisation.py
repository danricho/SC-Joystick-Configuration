import gremlin      # 'Coz it's a Joystick Gremlin module!
import logging      # Used for logging events and debugging
from configuration import *   # Holds the Joysticks IDs and other constants

''' "Initialise Axes" function
 Purpose: This function sets all axes of both virtual joysticks to zero when
          Joystick Gremlin starts. This is to ensure that no inputs are set 
          prior to the physical joysticks generating an event.              '''
def initialise_axes():
  vjoy = gremlin.input_devices.VJoyProxy()
  vjoy[1].axis(1).value = 0
  vjoy[1].axis(2).value = 0
  vjoy[1].axis(3).value = 0
  vjoy[2].axis(1).value = 0
  vjoy[2].axis(2).value = 0
  vjoy[2].axis(3).value = 0


initialise_axes()

'''============================================================================
LOGGING
-------
Adding a log entry into the log window of the JG GUI:
  logging.getLogger("system").debug("System log entry.")
  logging.getLogger("user").debug("User log entry.")
Generating a popup:
  gremlin.util.display_error("Error popup")
============================================================================'''