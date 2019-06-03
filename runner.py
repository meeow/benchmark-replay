import pyautogui, time, random, threading, math
from keyboard import *
from mousefunc import *

M = Mouse()

def mousetest():
    for i in range(50000):
        x = int(500+math.sin(math.pi*i/100)*500)
        y = int(500+math.cos(i)*100)
        M.move_relative((0.1,0))
        time.sleep(0.01)

def keytest():
    for i in range(5):
        duration = 2
        press_key_time('a', duration)
        time.sleep(3)

# k = threading.Thread(target = keytest)
# m = threading.Thread(target = mousetest)

# k.start()
# m.start()

mousetest()
