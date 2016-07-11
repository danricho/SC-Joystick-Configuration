import gremlin

right_t16000m = gremlin.input_devices.JoystickDecorator(name="T.16000M", device_id=(1325664945, 1), mode="Default")
arduino_leonardo_1 = gremlin.input_devices.JoystickDecorator(name="Arduino Leonardo", device_id=(1092826752, 4), mode="Default")
left_t16000m = gremlin.input_devices.JoystickDecorator(name="T.16000M", device_id=(1325664945, 0), mode="Default")

# Logging Methods:
# import logging
# logging.getLogger("system").debug("System debug info.")
# logging.getLogger("user").debug("User debug info.")
# or
# gremlin.util.display_error("Error popup")

# This module creates button presses from hat movements from each joystick.
# It allows hat movements to be mapped to virtual button presses which are also triggered by button presses on the control panel.

# # LEFT HAT MOVEMENT

@left_t16000m.hat(1)
def left_hat_management(event, vjoy):
  if event.value == (0, 1): # IF MOVED TO "UP", VIRTUAL BUTTON 5 "PRESSED"
      vjoy[1].button(5).is_pressed = True
      vjoy[1].button(6).is_pressed = False
      vjoy[1].button(7).is_pressed = False
      vjoy[1].button(8).is_pressed = False
  elif event.value == (0, -1): # IF MOVED TO "DOWN", VIRTUAL BUTTON 6 "PRESSED"
      vjoy[1].button(5).is_pressed = False
      vjoy[1].button(6).is_pressed = True
      vjoy[1].button(7).is_pressed = False
      vjoy[1].button(8).is_pressed = False
  elif event.value == (-1, 0): # IF MOVED TO "LEFT", VIRTUAL BUTTON 7 "PRESSED"
      vjoy[1].button(5).is_pressed = False
      vjoy[1].button(6).is_pressed = False
      vjoy[1].button(7).is_pressed = True
      vjoy[1].button(8).is_pressed = False
  elif event.value == (1, 0): # IF MOVED TO "RIGHT", VIRTUAL BUTTON 8 "PRESSED"
      vjoy[1].button(5).is_pressed = False
      vjoy[1].button(6).is_pressed = False
      vjoy[1].button(7).is_pressed = False
      vjoy[1].button(8).is_pressed = True
  elif event.value == (0, 0): # IF CENTRED, NO BUTTONS "PRESSED"
      vjoy[1].button(5).is_pressed = False
      vjoy[1].button(6).is_pressed = False
      vjoy[1].button(7).is_pressed = False
      vjoy[1].button(8).is_pressed = False
        
# # RIGHT HAT MOVEMENT
@right_t16000m.hat(1)
def right_hat_management(event, vjoy):
  if event.value == (0, 1): # IF MOVED TO "UP", VIRTUAL BUTTON 5 "PRESSED"
      vjoy[2].button(5).is_pressed = True
      vjoy[2].button(6).is_pressed = False
      vjoy[2].button(7).is_pressed = False
      vjoy[2].button(8).is_pressed = False
  elif event.value == (0, -1): # IF MOVED TO "DOWN", VIRTUAL BUTTON 6 "PRESSED"
      vjoy[2].button(5).is_pressed = False
      vjoy[2].button(6).is_pressed = True
      vjoy[2].button(7).is_pressed = False
      vjoy[2].button(8).is_pressed = False
  elif event.value == (-1, 0): # IF MOVED TO "LEFT", VIRTUAL BUTTON 7 "PRESSED"
      vjoy[2].button(5).is_pressed = False
      vjoy[2].button(6).is_pressed = False
      vjoy[2].button(7).is_pressed = True
      vjoy[2].button(8).is_pressed = False
  elif event.value == (1, 0): # IF MOVED TO "RIGHT", VIRTUAL BUTTON 8 "PRESSED"
      vjoy[2].button(5).is_pressed = False
      vjoy[2].button(6).is_pressed = False
      vjoy[2].button(7).is_pressed = False
      vjoy[2].button(8).is_pressed = True
  elif event.value == (0, 0): # IF CENTRED, NO BUTTONS "PRESSED"
      vjoy[2].button(5).is_pressed = False
      vjoy[2].button(6).is_pressed = False
      vjoy[2].button(7).is_pressed = False
      vjoy[2].button(8).is_pressed = False
