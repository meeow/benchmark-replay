import win32gui, win32api, win32con, ctypes, mousefunc, mouse

import win32api
import win32con
import time, mousefunc, keyboard
from win32api import GetSystemMetrics
from key_reference import vk_keys, keys

M = mousefunc.Mouse()

width, height = GetSystemMetrics(0), GetSystemMetrics(1)
button_down, button_up = 1, 0
move = 0
sensitivity = 0.0315
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
    currentTime=time.time()
    xedge, yedge = 0,0
    switch = False

    prvX, prvY = win32api.GetCursorPos()
    while True:
        # a = win32api.GetKeyState(vk_keys['VK_LBUTTON'])
        # b = win32api.GetKeyState(vk_keys['VK_RBUTTON'])
        recording = win32api.GetKeyState(vk_keys['VK_KEY_1'])

        if recording != record_button:
            time.sleep(0.4)
            f.close()
            return
        
        if time.time() - currentTime > ST:
            h_x, h_y = win32api.GetCursorPos()
            current_states = {key: win32api.GetKeyState(vk_keys[key]) for key in vk_keys}

            # move mouse back to center if it gets to the edge
            if h_x <= 0 or h_x >= width-1:
                switch = not switch
                M.move_mouse((width//2, h_y))
            if h_y >= height-1 or h_y <= 0:
                switch = not switch
                M.move_mouse((h_x, height//2))

            dX, dY = sensitivity*(h_x + (switch * xedge) - prvX), sensitivity*(h_y + (switch * yedge)- prvY)
            prvX, prvY = h_x, h_y

            # remove offset caused by moving mouse back to center 
            if dX >= sensitivity*width//2.5: dX -= sensitivity*width//2
            if dY >= sensitivity*height//2.5: dY -= sensitivity*height//2
            if dX <= sensitivity*-width//2.5: dX += sensitivity*width//2
            if dY <= sensitivity*-height//2.5: dY += sensitivity*height//2

            f.write("%.3f " % (time.time() - currentTime))
            f.write(' 0'  + ' ' + str(move) + ' ' + str(dX) + ' ' + str(dY) + '\n') 
            currentTime = time.time()    

            if prev_states != current_states: # Button state changed
                for key in current_states:
                    if current_states[key] != prev_states[key]:
                        print("record: {} toggled".format(key))
                        f.write("%.3f " % (time.time()-currentTime))
                        button_action = 0
                        if current_states[key] < 0: button_action = 1
                        f.write(' ' + str(vk_keys[key]) + ' ' + str(button_action) + ' ' + str(dX) + ' ' + str(dY) + '\n') 
                        
                # if a != state_left:  
                #     print('- record: Left toggled')
                #     state_left = a
                #     mouseStateA = str(button_up)
                #     if a < 0: mouseStateA = str(button_down)
                #     f.write(' ' + str(leftMouse) + ' ' + str(mouseStateA) + ' ' + str(dX) + ' ' + str(dY) + '\n') 
                # if b != state_right: 
                #     print('- record: Right toggled')
                #     state_right = b
                #     mouseStateB = str(button_up)
                #     if b < 0: mouseStateB = str(button_down)
                #     f.write(' ' + str(rightMouse) + ' ' + str(mouseStateB) + ' ' + str(dX) + ' ' + str(dY) + '\n')

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
                if int(currentEvent[2]) == button_down:
                    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,
                    #0,0,0,0)
                    keyboard.press_key('N')
                    #M.click(button_name='left')
                if int(currentEvent[2]) == button_up:
                    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,
                    #0,0,0,0)
                    keyboard.release_key('N')
            elif int(currentEvent[1]) == 2:
                if int(currentEvent[2]) == button_down:
                    #win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,
                    #0,0,0,0)
                    #keyboard.PressKey(0x101)
                    #keyboard.PressKey(rightMouse)
                    keyboard.press_key('M')
                    #M.click(button_name='right')
                if int(currentEvent[2]) == button_up:
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



