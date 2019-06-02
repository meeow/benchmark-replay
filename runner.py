import pyautogui, time, random
from keyboard import *

while 1:
    #print(pyautogui.position())
    x_res, y_res = 1920, 1080
    duration = 2
    x_target = random.randint(0, x_res)
    y_target = random.randint(0, y_res)
    print(x_target, y_target)
    #pyautogui.moveTo(x_target, y_target, duration=duration)
    press_key_time('a', duration)
    #move_mouse(500,500)
    time.sleep(5)