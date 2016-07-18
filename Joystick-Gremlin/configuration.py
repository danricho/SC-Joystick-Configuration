LFT_STK_WID = 3
RGT_STK_WID = 4
STK_HWID = 1325664945
STK_NAME = "T.16000M"

CP_WID = 0
CP_HWID = 1092826752
CP_NAME = "Arduino Leonardo"

MODE_ALL = 'Default"

# DECLARE THE JOYSTICKS:
t16000m_left = gremlin.input_devices.JoystickDecorator(name = STK_NAME, device_id = (STK_HWID, LFT_STK_WID), mode = MODE_ALL)
t16000m_right = gremlin.input_devices.JoystickDecorator(name = STK_NAME, device_id = (STK_HWID, RGT_STK_WID), mode = MODE_ALL)
control_panel = gremlin.input_devices.JoystickDecorator(name = CP_NAME, device_id = (CP_HWID, CP_WID), mode = MODE_ALL)
