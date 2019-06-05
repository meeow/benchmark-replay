# References
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
# https://github.com/Sentdex/pygta5/blob/master/directkeys.py
# https://wiki.nexusmods.com/index.php/DirectX_Scancodes_And_How_To_Use_Them

import ctypes
import time
import logging
import os
from key_reference import keys

SendInput = ctypes.windll.user32.SendInput

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger('')
logging.root.setLevel(logging.DEBUG)


# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actual Functions
def move_mouse(x,y):
    ctypes.windll.user32.SetCursorPos(x, y)

def press_key(key):
    def press_key_helper(hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
    hex_code = keys[key.upper()]
    press_key_helper(hex_code)
    logger.debug('Pressed {}'.format(key))

def release_key(key):
    def release_key_helper(hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
    hex_code = keys[key.upper()]
    release_key_helper(hex_code)
    logger.debug('Released {}'.format(key))


def press_key_time(key, t):
    print ('Pressing {} for {}s'.format(key, t))
    try:
        key = key.upper()
        press_key(key)
        time.sleep(t)
        release_key_helper(keys[key])
        time.sleep(1)
    except:
        print("Error: requested key {} undefined".format(key))    
        
if __name__ == '__main__':
    time.sleep(3)
    press_key('W')
    time.sleep(1)
    release_key('W')
    time.sleep(1)