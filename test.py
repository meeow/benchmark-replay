import win32gui, win32api, win32con, ctypes, mousefunc, mouse

import win32api
import win32con
import time, mousefunc, keyboard
from win32api import GetSystemMetrics
from key_reference import vk_keys, keys

M = mousefunc.Mouse()

WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
BUTTON_DOWN, BUTTON_UP = 1, 0
move = 0
x_sensitivity = 0.0315
#ref_states = {key: win32api.GetKeyState(vk_keys[key]) for key in list(vk_keys.keys())}


def record(ST=0.01):
    f=open('record.txt','w')
    f.close()
    f=open('record.txt','a')

    # leftMouse = 0x01
    # rightMouse = 0x02
    # state_left = win32api.GetKeyState(leftMouse)  # Left button down = 0 or 1. Button up = -127 or -128
    # state_right = win32api.GetKeyState(rightMouse)  # Right button down = 0 or 1. Button up = -127 or -128

    record_button = win32api.GetKeyState(vk_keys['VK_KEY_1']) # 1
    prev_states = {key: win32api.GetKeyState(vk_keys[key]) for key in list(vk_keys.keys())}
    current_time = time.time()
    x_edge, y_edge = 0,0
    prev_x, prev_y = win32api.GetCursorPos()
    switch = False

    while True:
        # a = win32api.GetKeyState(vk_keys['VK_LBUTTON'])
        # b = win32api.GetKeyState(vk_keys['VK_RBUTTON'])
        recording = win32api.GetKeyState(vk_keys['VK_KEY_1'])

        if recording != record_button:
            time.sleep(0.4)
            f.close()
            return
        
        if time.time() - current_time > ST:
            current_x, current_y = win32api.GetCursorPos()
            current_states = {key: win32api.GetKeyState(vk_keys[key]) for key in vk_keys}

            # move mouse back to center if it gets to the edge
            if current_x <= 0 or current_x >= WIDTH-1:
                switch = not switch
                M.move_mouse((WIDTH//2, current_y))
            if current_y >= HEIGHT-1 or current_y <= 0:
                switch = not switch
                M.move_mouse((current_x, HEIGHT//2))

            delta_x, delta_y = x_sensitivity * (current_x + (switch * x_edge) - prev_x), x_sensitivity * (current_y + (switch * y_edge) - prev_y)
            prev_x, prev_y = current_x, current_y

            # remove offset caused by moving mouse back to center 
            if delta_x >= x_sensitivity * WIDTH // 2.5: delta_x -= x_sensitivity * WIDTH // 2
            if delta_y >= x_sensitivity * HEIGHT // 2.5: delta_y -= x_sensitivity * HEIGHT // 2
            if delta_x <= x_sensitivity * -WIDTH // 2.5: delta_x += x_sensitivity * WIDTH // 2
            if delta_y <= x_sensitivity * -HEIGHT // 2.5: delta_y += x_sensitivity * HEIGHT // 2

            f.write("%.3f " % (time.time() - current_time))
            f.write(' 0'  + ' ' + str(0) + ' ' + str(delta_x) + ' ' + str(delta_y) + '\n') 
            current_time = time.time()    

            if prev_states != current_states: # Button state changed
                for key in current_states:
                    if current_states[key] != prev_states[key]:
                        print("record: {} toggled".format(key))
                        f.write("%.3f " % (time.time()-current_time))
                        button_action = BUTTON_UP
                        if current_states[key] < 0: button_action = BUTTON_DOWN
                        f.write(' ' + str(vk_keys[key]) + ' ' + str(button_action) + ' ' + str(delta_x) + ' ' + str(delta_y) + '\n') 
                        
                # if a != state_left:  
                #     print('- record: Left toggled')
                #     state_left = a
                #     mouseStateA = str(BUTTON_UP)
                #     if a < 0: mouseStateA = str(BUTTON_DOWN)
                #     f.write(' ' + str(leftMouse) + ' ' + str(mouseStateA) + ' ' + str(delta_x) + ' ' + str(delta_y) + '\n') 
                # if b != state_right: 
                #     print('- record: Right toggled')
                #     state_right = b
                #     mouseStateB = str(BUTTON_UP)
                #     if b < 0: mouseStateB = str(BUTTON_DOWN)
                #     f.write(' ' + str(rightMouse) + ' ' + str(mouseStateB) + ' ' + str(delta_x) + ' ' + str(delta_y) + '\n')

            prev_states = current_states
            
        time.sleep(0.001)
        
def play(loopTime = 1, sleepTime = 0.1):
    f = open('record.txt','r')
    lineStr = f.readlines()
    play_button = win32api.GetKeyState(0x32)
    # leftMouse=0x01
    # rightMouse=0x02
    while loopTime:
        loopTime = loopTime - 1
        for str in lineStr:
            currentEvent = str.split()
            c = win32api.GetKeyState(0x32)
            if c != play_button:
                time.sleep(0.5)
                f.close()
                return
                
            time.sleep(float(currentEvent[0]))
            movX, movY = float(currentEvent[3]), float(currentEvent[4])
            M.move_relative((movX, movY))

            if int(currentEvent[1]) == 1:
                if int(currentEvent[2]) == BUTTON_DOWN:
                    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,
                    #0,0,0,0)
                    keyboard.press_key('N')
                    #M.click(button_name='left')
                if int(currentEvent[2]) == BUTTON_UP:
                    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,
                    #0,0,0,0)
                    keyboard.release_key('N')
            elif int(currentEvent[1]) == 2:
                if int(currentEvent[2]) == BUTTON_DOWN:
                    #win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,
                    #0,0,0,0)
                    #keyboard.PressKey(0x101)
                    #keyboard.PressKey(rightMouse)
                    keyboard.press_key('M')
                    #M.click(button_name='right')
                if int(currentEvent[2]) == BUTTON_UP:
                    #win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,
                    #0,0,0,0)    
                    keyboard.release_key('M')
       
        time.sleep(sleepTime)

def _main():
    while True:
        toggled = False
        isPlay = False

        while win32api.GetKeyState(0x31) not in [0,1]:
            toggled = True
            time.sleep(0.01)
        if toggled:
            toggled = False
            record()
            
        while win32api.GetKeyState(0x32) not in [0,1]:
            isPlay = True
            time.sleep(0.01)
        if isPlay:
            isPlay = False
            play()
        time.sleep(0.001)               

_main()



