import os, sys
import struct
import sdl2
import fileinput
import re
from xml.dom import minidom

testing = 0

JGXML = os.path.abspath(os.path.join(os.getenv("userprofile"),"Joystick Gremlin","dual_t16000m_leonardo_JoystickGremlin.xml"))
JGPYCON = os.path.abspath(os.path.join(os.getenv("userprofile"),"Joystick Gremlin","configuration.py"))
SCXML = os.path.abspath(os.path.join(os.getenv("programfiles"),"Cloud Imperium Games", "StarCitizen", "Public", "USER", "Controls", "Mappings","dual_t16000m_leonardo_SCmap.xml"))
SCXML = SCXML.replace(" (x86)","")

try:
  sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
except:
  print " OOPS: Can't initialise SDL."
  raw_input("\n Press Enter to Quit.")
  sys.exit(1)
  
joysticks = []

def printJoyReport():
  for joystick in joysticksSorted:
    print "Name: " + joystick["Name"]
    print "  Resolved Name: " + str(joystick["Res Name"])
    print "  HW ID: " + str(joystick["HW ID"])
    print "  Win ID: " + str(joystick["Win ID"])
    # print "  Axes: " + str(joystick["Axes"])
    print "  Buttons: " + str(joystick["Buttons"])
    # print "  Hats: " + str(joystick["Hats"])
    print "  SCXML ID: " + str(joystick["SCXML ID"])
    print "  JGXML ID: " + str(joystick["JGXML ID"])
    print "  JGPYCON ID: " + str(joystick["JGPYCON ID"])

def ResolvedName2WinID(Name):
  for joystick in joysticksSorted:
    if joystick["Res Name"] == Name:
      return joystick["Win ID"]

def ResolvedName2Dict(Name):
  for joystick in joysticksSorted:
    if joystick["Res Name"] == Name:
      return joystick
      
def replaceInFile(filename, find, replace):
  for line in fileinput.input(filename, inplace=True):
    line = line.replace(find, replace)
    sys.stdout.write(line)
  fileinput.close()

if sdl2.SDL_NumJoysticks() < 1:
    print " OOPS: Can't find any joysticks."
    print "  - Check they are connected."
    print "  - Check they are listed in the \"USB Game Controllers\" utility."
    raw_input("\n Press Enter to Quit.")
    sys.exit(1)

  
for i in range(sdl2.SDL_NumJoysticks()):
  joy = sdl2.SDL_JoystickOpen(i)
  if joy is None:
    print("Joystick device at {} is invalid.".format(i))
  else:
    name_object = sdl2.SDL_JoystickName(joy)
    if name_object is None:
      name = "Unknown device"
      print("Encountered an invalid device name")
    else:
      name = name_object.decode("utf-8")
    hardware_id = struct.unpack(">4I", sdl2.SDL_JoystickGetGUID(joy))[0]
    windows_id = sdl2.SDL_JoystickInstanceID(joy)
    hardware_id = struct.unpack(">4I", sdl2.SDL_JoystickGetGUID(joy))[0]
    windows_id = sdl2.SDL_JoystickInstanceID(joy)
    axes = sdl2.SDL_JoystickNumAxes(joy)
    buttons = sdl2.SDL_JoystickNumButtons(joy)
    hats = sdl2.SDL_JoystickNumHats(joy)

    joystick = {
        "Name": name,
        "Res Name": None,
        "SCXML ID": None,
        "JGXML ID": None,
        "JGPYCON ID": None,
        "HW ID": hardware_id,
        "Win ID": windows_id,
        "Axes": axes,
        "Buttons": buttons,
        "Hats": hats,
        "Obj": joy,
        }
    joysticks.append(joystick)
        
joysticksSorted = sorted(joysticks, key=lambda k: k["Win ID"])

# Resolve the Sticks (Press Left Trigger)
print "\n-- RESOLVING THE STICKS --"
testRunning = True
print " > Press the LEFT Trigger"
while testRunning:
  for joystick in joysticksSorted:
    if joystick["Name"] == "T.16000M":
      sdl2.SDL_JoystickUpdate()
      if sdl2.SDL_JoystickGetButton(joystick["Obj"], 0):
        print " Left Stick has Win ID: " + str(joystick["Win ID"])
        joystick["Res Name"] = "Left Stick"
        for otherJoystick in joysticksSorted:
          if otherJoystick["Name"] == "T.16000M" and otherJoystick["Res Name"] == None:
            otherJoystick["Res Name"] = "Right Stick"
            print " Right Stick has Win ID: " + str(otherJoystick["Win ID"])
        testRunning = False

# Label the Control Panel
print "\n-- RESOLVING CONTROL PANEL --"
for joystick in joysticksSorted:
  if joystick["Name"] == "Arduino Leonardo":
    print " Control Panel has Win ID: " + str(joystick["Win ID"])
    joystick["Res Name"] = "Control Panel"
        
# Resolve the vJoy devices (vJoy2 has 49 buttons rather than 50)
print "\n-- RESOLVING VJOYS --"
for joystick in joysticksSorted:
  if joystick["Name"] == "vJoy Device" and joystick["Buttons"] == 50:
    joystick["Res Name"] = "vJoy 1"
    print " vJoy 1 has Win ID: " + str(joystick["Win ID"])
  elif joystick["Name"] == "vJoy Device" and joystick["Buttons"] == 49:
    print " vJoy 2 has Win ID: " + str(joystick["Win ID"])
    joystick["Res Name"] = "vJoy 2"
        
# Done with the joysticks - close them.    
for joystick in joysticksSorted:
    sdl2.SDL_JoystickClose(joystick["Obj"]);

# printJoyReport()

# Lets check the JG XML
print "\n-- PARSING THE JOYSTICK GREMLIN MAPPING XML --"
try:
  xmldoc = minidom.parse(JGXML)
except:
  print " OOPS: Can't open the Joystick Gremlin XML."
  sys.exit(1)
devices = xmldoc.getElementsByTagName('device')
for device in devices:
  if device.getAttribute("name") == "T.16000M":
    axes = device.getElementsByTagName('axis')
    for axis in axes:
      if axis.getAttribute('id') == "1":
        remaps = axis.getElementsByTagName('remap')
        for remap in remaps:
          if remap.getAttribute("vjoy") == "1":
            ResolvedName2Dict("Left Stick")["JGXML ID"] = int(device.getAttribute('windows_id'))
          elif remap.getAttribute("vjoy") == "2":
            ResolvedName2Dict("Right Stick")["JGXML ID"] = int(device.getAttribute('windows_id'))
  elif device.getAttribute("name") == "Arduino Leonardo":
    ResolvedName2Dict("Control Panel")["JGXML ID"] = int(device.getAttribute('windows_id'))

# Lets check the JG configuration.py
print "-- PARSING THE JOYSTICK GREMLIN CUSTOM MODULE CONFIGURATION --"
try:
  textfile = open(JGPYCON, 'r')
  filetext = textfile.read()
  textfile.close()
except:
  print " OOPS: Can't open the Joystick Gremlin configuration module."
  sys.exit(1)
ResolvedName2Dict("Left Stick")["JGPYCON ID"] = int(re.findall("LFT_STK_WID = ([0-9]+)", filetext)[0])
ResolvedName2Dict("Right Stick")["JGPYCON ID"] = int(re.findall("RGT_STK_WID = ([0-9]+)", filetext)[0])
ResolvedName2Dict("Control Panel")["JGPYCON ID"] = int(re.findall("CP_WID = ([0-9]+)", filetext)[0])

# Lets check the SC XML
print "-- PARSING THE STAR CITIZEN KEYBINDING XML --"
try:
  xmldoc = minidom.parse(SCXML)
except:
  print " OOPS: Can't open the Star Citizen XML."
  sys.exit(1)
actionMaps = xmldoc.getElementsByTagName('actionmap')
for actionMap in actionMaps:
  if actionMap.getAttribute('name') == "spaceship_movement":
    for action in actionMap.getElementsByTagName('action'):
      # vJoy 2 is the right stick + some Panel. 
      # Test for "v_strafe_vertical".
      if action.getAttribute('name') == "v_strafe_vertical":
        for rebind in action.getElementsByTagName('rebind'):
          ResolvedName2Dict("vJoy 2")["SCXML ID"] = int(rebind.getAttribute("input")[2]) - 1
      # vJoy 1 is the left stick + some Panel.
      # Test for "v_roll".    
      elif action.getAttribute('name') == "v_roll":
        for rebind in action.getElementsByTagName('rebind'):
          ResolvedName2Dict("vJoy 1")["SCXML ID"] = int(rebind.getAttribute("input")[2]) - 1

          
# Force some changes for testing.
if testing:
  ResolvedName2Dict("Left Stick")["Win ID"] = 8
  ResolvedName2Dict("Right Stick")["Win ID"] = 7
  ResolvedName2Dict("Control Panel")["Win ID"] = 6
  ResolvedName2Dict("vJoy 1")["Win ID"] = 5
  ResolvedName2Dict("vJoy 2")["Win ID"] = 4
          
print "\n-- CORRECTIONS --"

corrections_count = 0

  #####################################

if not ResolvedName2Dict("Left Stick")["JGXML ID"] == ResolvedName2WinID("Left Stick"):
  itIS = str(ResolvedName2Dict("Left Stick")["JGXML ID"])
  itSHALL = str(ResolvedName2WinID("Left Stick"))
  try:
    replaceInFile(JGXML, 'windows_id="' + itIS + '"', 'windows_id="' + itSHALL + '"')
  except:
    print " OOPS: Can't change the Joystick Gremlin XML."
    print "  - Check the path."
    raw_input("\n Press Enter to Quit.")
    sys.exit(1)
  print " JG MAPPING XML Left Stick WID was incorrect; Changed from " + itIS + " to " + itSHALL + "."
  corrections_count += 1
  
if not ResolvedName2Dict("Right Stick")["JGXML ID"] == ResolvedName2WinID("Right Stick"):
  itIS = str(ResolvedName2Dict("Right Stick")["JGXML ID"])
  itSHALL = str(ResolvedName2WinID("Right Stick"))
  try:
    replaceInFile(JGXML, 'windows_id="' + itIS + '"', 'windows_id="' + itSHALL + '"')
  except:
    print " OOPS: Can't change the Joystick Gremlin XML."
    print "  - Check the path."
    raw_input("\n Press Enter to Quit.")
    sys.exit(1)
  print " JG MAPPING XML Right Stick WID was incorrect; Changed from " + itIS + " to " + itSHALL + "."
  corrections_count += 1
  
if not ResolvedName2Dict("Control Panel")["JGXML ID"] == ResolvedName2WinID("Control Panel"):
  itIS = str(ResolvedName2Dict("Control Panel")["JGXML ID"])
  itSHALL = str(ResolvedName2WinID("Control Panel"))
  try:
    replaceInFile(JGXML, 'eonardo" windows_id="' + itIS + '"', 'eonardo" windows_id="' + itSHALL + '"')
  except:
    print " OOPS: Can't change the Joystick Gremlin XML."
    print "  - Check the path."
    raw_input("\n Press Enter to Quit.")
    sys.exit(1)
  print " JG MAPPING XML Control Panel WID was incorrect; Changed from " + itIS + " to " + itSHALL + "."
  corrections_count += 1

  #####################################
  
if not ResolvedName2Dict("Left Stick")["JGPYCON ID"] == ResolvedName2WinID("Left Stick"):
  itIS = str(ResolvedName2Dict("Left Stick")["JGPYCON ID"])
  itSHALL = str(ResolvedName2WinID("Left Stick"))
  try:
    replaceInFile(JGPYCON, 'LFT_STK_WID = ' + itIS, 'LFT_STK_WID = ' + itSHALL)
  except:
    print " OOPS: Can't change the Joystick Gremlin configuration module."
    print "  - Check the path."
    raw_input("\n Press Enter to Quit.")
    sys.exit(1)
  print " JG MAPPING XML Left Stick WID was incorrect; Changed from " + itIS + " to " + itSHALL + "."
  corrections_count += 1
  
if not ResolvedName2Dict("Right Stick")["JGPYCON ID"] == ResolvedName2WinID("Right Stick"):
  itIS = str(ResolvedName2Dict("Right Stick")["JGPYCON ID"])
  itSHALL = str(ResolvedName2WinID("Right Stick"))
  try:
    replaceInFile(JGPYCON, 'RGT_STK_WID = ' + itIS, 'RGT_STK_WID = ' + itSHALL)
  except:
    print " OOPS: Can't change the Joystick Gremlin configuration module."
    print "  - Check the path."
    raw_input("\n Press Enter to Quit.")
    sys.exit(1)
  print " JG MAPPING XML Right Stick WID was incorrect; Changed from " + itIS + " to " + itSHALL + "."
  corrections_count += 1
  
if not ResolvedName2Dict("Control Panel")["JGPYCON ID"] == ResolvedName2WinID("Control Panel"):
  itIS = str(ResolvedName2Dict("Control Panel")["JGPYCON ID"])
  itSHALL = str(ResolvedName2WinID("Control Panel"))
  try:
    replaceInFile(JGPYCON, 'CP_WID = ' + itIS, 'CP_WID = ' + itSHALL)
  except:
    print " OOPS: Can't change the Joystick Gremlin configuration module."
    print "  - Check the path."
    raw_input("\n Press Enter to Quit.")
    sys.exit(1)
  print " JG MAPPING XML Control Panel WID was incorrect; Changed from " + itIS + " to " + itSHALL + "."
  corrections_count += 1
  
  #####################################

if not ResolvedName2Dict("vJoy 1")["SCXML ID"] == ResolvedName2WinID("vJoy 1"):
  itIS = str(ResolvedName2Dict("vJoy 1")["SCXML ID"] + 1)
  itSHALL = str(ResolvedName2WinID("vJoy 1") + 1)
  try:
    replaceInFile(SCXML, 'input="js' + itIS + '_', 'input="js' + itSHALL + '_')
    replaceInFile(SCXML, 'instance="' + itIS + '"', 'instance="' + itSHALL + '"')
  except:
    print " OOPS: Can't change the Star Citizen XML."
    print "  - Try running from elevated command prompt (as administrator)."
    print "  - Check the path."
    raw_input("\n Press Enter to Quit.")
    sys.exit(1)
  print " SC KEYBINDING XML VJoy 1 WID was incorrect; Changed from " + itIS + " to " + itSHALL + "."
  corrections_count += 1
  
if not ResolvedName2Dict("vJoy 2")["SCXML ID"] == ResolvedName2WinID("vJoy 2"):
  itIS = str(ResolvedName2Dict("vJoy 2")["SCXML ID"] + 1)
  itSHALL = str(ResolvedName2WinID("vJoy 2") + 1)
  try:
    replaceInFile(SCXML, 'input="js' + itIS + '_', 'input="js' + itSHALL + '_')
    replaceInFile(SCXML, 'instance="' + itIS + '"', 'instance="' + itSHALL + '"')
  except:
    print " OOPS: Can't change the Star Citizen XML."
    print "  - Try running from elevated command prompt (as administrator)."
    print "  - Check the path."
    raw_input("\n Press Enter to Quit.")
    sys.exit(1)
  print " SC KEYBINDING XML VJoy 2 WID was incorrect; Changed from " + itIS + " to " + itSHALL + "."
  corrections_count += 1
 
if corrections_count == 0:
  print " None required."
  
raw_input("\n Press Enter to Quit.")
  
