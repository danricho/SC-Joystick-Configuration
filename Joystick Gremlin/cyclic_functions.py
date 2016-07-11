import time
import gremlin
import logging
from vjoy.vjoy import AxisName

# Logging Methods:
# import logging
# logging.getLogger("system").debug("System debug info.")
# logging.getLogger("user").debug("User debug info.")
# or
# gremlin.util.display_error("Error popup")

# This module contains a time triggered (periodic) function which is designed to read the state of the sliders on the joysticks and report them irrespective if they have moved and caused an event.
# Currently this function is disabled as I have a throttle +/- button press event mapped against my hats and don't want the setting overwritten by the slider position.

# Periodic function (every second)
@gremlin.input_devices.periodic(0.5)
def slider_update(vjoy, joy):
  
  left_updating = False
  right_updating = False
  
  if left_updating:
    left_value = joy[0].axis(4).value # READ THE LEFT STICK SLIDER VALUE
    if (left_value < 0.998): # SET THE VIRTUAL SLIDER VALUES WITH JITTER
      vjoy[1].axis(7).value = (left_value + 0.002) 
    else:
      vjoy[1].axis(7).value = (left_value - 0.002) 
    vjoy[1].axis(7).value = left_value # SET THE VIRTUAL SLIDER VALUES CORRECTLY
  
  if right_updating:
    right_value = joy[1].axis(4).value  # READ THE RIGHT STICK SLIDER VALUE
    if (right_value < 0.998): # SET THE VIRTUAL SLIDER VALUES WITH JITTER
      vjoy[2].axis(7).value = (right_value + 0.002) 
    else:
      vjoy[2].axis(7).value = (right_value - 0.002) 
    vjoy[2].axis(7).value = right_value # SET THE VIRTUAL SLIDER VALUES CORRECTLY
    
  time.sleep(0.05)
