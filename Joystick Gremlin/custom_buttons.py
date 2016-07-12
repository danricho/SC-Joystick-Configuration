import gremlin      # 'Coz it's a Joystick Gremlin module!
import time         # Used for delays between actions in some functions
import threading    # Threading allows the longer functions to be non-blocking
import logging      # Used for logging events and debugging

# Defining the controllers
t16000m_left = gremlin.input_devices
                .JoystickDecorator(name="T.16000M", 
                                   device_id=(1325664945, 0),
                                   mode="Default")
t16000m_right = gremlin.input_devices
                 .JoystickDecorator(name="T.16000M",
                                    device_id=(1325664945, 1),
                                    mode="Default")
control_panel = gremlin.input_devices
                 .JoystickDecorator(name="Arduino Leonardo", 
                                    device_id=(1092826752, 4), 
                                    mode="Default")

'''============================================================================

LOGGING
-------

Adding a log entry into the log window of the JG GUI:
  logging.getLogger("system").debug("System log entry.")
  logging.getLogger("user").debug("User log entry.")

Generating a popup:
  gremlin.util.display_error("Error popup")

============================================================================'''

TAP_LENGTH = 0.1   # Time (secs) between press and release of buttons

''' "Quantum Escape" function
 Purpose: Quantum travels in the direction the ship is facing in 
          order to escape from enemies.
 Notes:   Called as a threaded function to ensure that the controllers aren't
          locked during the time it is running.                             '''
def quantum_escape():
    vjoy = gremlin.input_devices.VJoyProxy()
    joy = gremlin.input_devices.JoystickProxy()

    vjoy[2].button(30).is_pressed = True     # Enable QT system
    time.sleep(TAP_LENGTH)
    vjoy[2].button(30).is_pressed = False
    time.sleep(1)                            # Wait for QT start-up
    vjoy[2].button(29).is_pressed = True     # QT engage
    time.sleep(TAP_LENGTH)
    vjoy[2].button(29).is_pressed = False
   
# Control Panel, Button 7 event (Quantum Escape)
@control_panel.button(7)
def cp_button7(event, vjoy):
    if event.is_pressed:
      # The button event was a "press", so launch 
      # the "Quantum Escape" function in a thread.
      threading.Timer(0.1, quantum_escape).start()  

''' "Fire Both CMs" function
 Purpose: Fire the selected counter-measure (CM), Cycle to the other CM, fire
          that CM, cycle back to the original CM.
 Notes:   Called as a threaded function to ensure that the controllers aren't
          locked during the time it is running.                             '''
def fire_both_cms():
    vjoy = gremlin.input_devices.VJoyProxy()
    joy = gremlin.input_devices.JoystickProxy()
    
    vjoy[1].button(38).is_pressed = True     # Fire CM
    time.sleep(TAP_LENGTH)
    vjoy[1].button(38).is_pressed = False
    time.sleep(2)                            # Wait for firing
    vjoy[1].button(40).is_pressed = True     # Cycle CM selection
    time.sleep(TAP_LENGTH)
    vjoy[1].button(40).is_pressed = False
    time.sleep(1)
    vjoy[1].button(38).is_pressed = True     # Fire CM
    time.sleep(TAP_LENGTH)
    vjoy[1].button(38).is_pressed = False
    time.sleep(2)                            # Wait for firing
    vjoy[1].button(40).is_pressed = True     # Cycle CM selection
    time.sleep(TAP_LENGTH)
    vjoy[1].button(40).is_pressed = False
    
# Control Panel, Button 8 event (Both C.M.)
@control_panel.button(8)
def cp_button8(event, vjoy):
    if event.is_pressed:
      # The button event was a "press", so launch 
      # the "Fire Both CMs" function in a thread.
      threading.Timer(0.1, fire_both_cms).start()
  
  
''' "Toggle Chat" Keyboard Macro
 Purpose: Toggles the display of the chat window by emulating keyboard 
          key-press F12.
 Notes:   For the macro to work, Joystick Gremlin must be run as an 
          administrator.
          The chat window must be hidden when this is run as the first 
          key-press toggles the chat window.                                '''
macro_toggle_chat = gremlin.input_devices.macro.Macro()
macro_toggle_chat.tap("F12")

# Control Panel, Button 54 event (Custom 1)
@control_panel.button(54)
def cp_button54(event, vjoy):
    if event.is_pressed:
      # The button event was a "press", so run 
      # the "Toggle Chat" Keyboard Macro.
      macro_toggle_chat.run()

''' "Salute Emote" Keyboard Macro
 Purpose: Triggers the /salute emote by emulating keyboard 
          key-presses F12, ENTER, /, S, A, L, U, T, E, ENTER, F12.
 Notes:   For the macro to work, Joystick Gremlin must be run as an 
          administrator.
          The chat window must be hidden when this is run as the first 
          key-press toggles the chat window.                                '''
macro_salute_emote = gremlin.input_devices.macro.Macro()
macro_salute_emote.tap(macro.Keys.F12)
macro_salute_emote.tap(macro.Keys.Enter)
macro_salute_emote.tap(macro.Keys.Slash)
macro_salute_emote.tap(macro.Keys.S)
macro_salute_emote.tap(macro.Keys.A)
macro_salute_emote.tap(macro.Keys.L)
macro_salute_emote.tap(macro.Keys.U)
macro_salute_emote.tap(macro.Keys.T)
macro_salute_emote.tap(macro.Keys.E)
macro_salute_emote.tap(macro.Keys.Enter)
macro_salute_emote.tap(macro.Keys.F12)

# Control Panel, Button 55 event (Custom 2)
@control_panel.button(55)
def cp_button55(event, vjoy):
    if event.is_pressed:
      # The button event was a "press", so run 
      # the "Salute Emote" Keyboard Macro.
      macro_salute_emote.run()

''' "Rude Emote" Keyboard Macro
 Purpose: Triggers the /rude emote by emulating keyboard 
          key-presses F12, ENTER, /, R, U, D, E, ENTER, F12.
 Notes:   For the macro to work, Joystick Gremlin must be run as an 
          administrator.
          The chat window must be hidden when this is run as the first 
          key-press toggles the chat window.                                '''
macro_rude_emote = gremlin.input_devices.macro.Macro()
macro_rude_emote.tap(macro.Keys.F12)
macro_rude_emote.tap(macro.Keys.Enter)
macro_rude_emote.tap(macro.Keys.Slash)
macro_rude_emote.tap(macro.Keys.R)
macro_rude_emote.tap(macro.Keys.U)
macro_rude_emote.tap(macro.Keys.D)
macro_rude_emote.tap(macro.Keys.E)
macro_rude_emote.tap(macro.Keys.Enter)
macro_rude_emote.tap(macro.Keys.F12)

# Control Panel, Button 56 event (Custom 3)
@control_panel.button(56)
def cp_button56(event, vjoy):
    if event.is_pressed:
      # The button event was a "press", so run 
      # the "Rude Emote" Keyboard Macro.
      macro_rude_emote.run()

''' "Toggle ShadowPlay - Recording" Keyboard Macro
 Purpose: Toggles ShadowPlay Video Recording (which I have mapped to Alt-F7).
 Notes:   For the macro to work, Joystick Gremlin must be run as an 
          administrator.                                                    '''
macro_toggle_sp_rec = gremlin.input_devices.macro.Macro()
macro_toggle_sp_rec.press("RAlt")
macro_toggle_sp_rec.tap("F7")
macro_toggle_sp_rec.release("RAlt")

# Control Panel, Button 57 event (Custom 4)
@control_panel.button(57)
def cp_button57(event, vjoy):
    if event.is_pressed:
      # The button event was a "press", so run 
      # the "Toggle ShadowPlay - Recording" Keyboard Macro
      macro_toggle_sp_rec.run()

''' "ShadowPlay - Save Buffer" Keyboard Macro
 Purpose: Saves the ShadowPlay Rolling Buffer (which I have mapped to Alt-F8).
 Notes:   For the macro to work, Joystick Gremlin must be run as an 
          administrator.                                                    '''
macro_toggle_sp_save_buffer = gremlin.input_devices.macro.Macro()
macro_toggle_sp_save_buffer.press("RAlt")
macro_toggle_sp_save_buffer.tap("F8")
macro_toggle_sp_save_buffer.release("RAlt")
   
# Control Panel, Button 58 event (Custom 5)
@control_panel.button(58)
def cp_button58(event, vjoy):
    if event.is_pressed:
      # The button event was a "press", so run 
      # the ''' "ShadowPlay - Save Buffer" Keyboard Macro
      macro_toggle_sp_save_buffer.run()
