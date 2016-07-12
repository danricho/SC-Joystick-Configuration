import gremlin      # 'Coz it's a Joystick Gremlin module!
import logging      # Used for logging events and debugging

# Defining the controllers
t16000m_left = gremlin.input_devices\
                 .JoystickDecorator(name = "T.16000M", 
                                    device_id = (1325664945, 
                                                 0
                                                ), 
                                    mode = "Default"
                                   )
t16000m_right = gremlin.input_devices\
                  .JoystickDecorator(name = "T.16000M", 
                                     device_id = (1325664945, 
                                                  1
                                                  ), 
                                     mode = "Default"
                                    )
''' "Hats to Buttons" function
 Purpose: Converts hat directions into button presses.                      '''
def hats_to_buttons(evnt, joystick):
  
  x_value, y_value = evnt.value
  
  if x_value == 0:
    # The hat event was horizontally centred
    # virtual buttons 7 and 8 aren't pressed.
    joystick.button(7).is_pressed = False
    joystick.button(8).is_pressed = False
  elif x_value == -1:
    # The hat event was horizontally left
    # virtual buttons 7 is pressed.
    joystick.button(7).is_pressed = True
    joystick.button(8).is_pressed = False
  elif x_value == 1:
    # The hat event was horizontally right
    # virtual buttons 8 is pressed.
    joystick.button(7).is_pressed = False
    joystick.button(8).is_pressed = True
  
  if y_value == 0:
    # The hat event was vertically centred
    # virtual buttons 5 and 6 aren't pressed.
    joystick.button(5).is_pressed = False
    joystick.button(6).is_pressed = False
  elif y_value == -1:
    # The hat event was vertically up
    # virtual button 5 is pressed.
    joystick.button(5).is_pressed = False
    joystick.button(6).is_pressed = True
  elif y_value == 1:
    # The hat event was vertically up
    # virtual button 6 is pressed.
    joystick.button(5).is_pressed = True
    joystick.button(6).is_pressed = False

                                    
# Left stick, hat event
@t16000m_left.hat(1)
def left_hat_management(event, vjoy):
  hats_to_buttons(event, vjoy[1])

        
# Right stick, hat event
@t16000m_right.hat(1)
def right_hat_management(event, vjoy):
  hats_to_buttons(event, vjoy[2])


'''============================================================================
LOGGING
-------
Adding a log entry into the log window of the JG GUI:
  logging.getLogger("system").debug("System log entry.")
  logging.getLogger("user").debug("User log entry.")
Generating a popup:
  gremlin.util.display_error("Error popup")
============================================================================'''