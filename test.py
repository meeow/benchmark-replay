import win32api
import time
import math
import pynput

import win32gui, win32api, win32con, ctypes, mousefunc, mouse

import win32api
import win32con
import time, mousefunc
from win32api import GetSystemMetrics

M = mousefunc.Mouse()

wide = GetSystemMetrics(0)
height = GetSystemMetrics(1)
mouseDown=2
mouseUp=1
move=0
sensitivity = 0.0315

def record(ST=0.01):
    f=open('record.txt','w')
    f.close()
    f=open('record.txt','a')

    leftMouse = 0x01
    rightMouse = 0x02
    state_left = win32api.GetKeyState(leftMouse)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(rightMouse)  # Right button down = 0 or 1. Button up = -127 or -128

    record_button = win32api.GetKeyState(0x31) # 111222
    
    currentTime=time.time()
    xedge,yedge = 0,0
    switch = False

    prvX, prvY = win32api.GetCursorPos()
    while True:
        a = win32api.GetKeyState(leftMouse)
        b = win32api.GetKeyState(rightMouse)
        c = win32api.GetKeyState(0x31)

        if c != record_button:
            time.sleep(0.5)
            f.close()
            return
        
        if time.time() - currentTime > ST:
            h_x, h_y = win32api.GetCursorPos()
            # move mouse back to center
            if h_x <= 0 or h_x >= wide-1:
                switch = not switch
                M.move_mouse((wide//2, h_y))
            if h_y >= height-1 or h_y <= 0:
                switch = not switch
                M.move_mouse((h_x, height//2))

            dX, dY = sensitivity*(h_x + (switch * xedge) - prvX), sensitivity*(h_y + (switch * yedge)- prvY)
            prvX, prvY = h_x, h_y

            if dX >= sensitivity*wide//2.5: dX -= sensitivity*wide//2
            if dY >= sensitivity*height//2.5: dY -= sensitivity*height//2
            if dX <= sensitivity*-wide//2.5: dX += sensitivity*wide//2
            if dY <= sensitivity*-height//2.5: dY += sensitivity*height//2

            print('rec:', dX, dY)    
            f.write("%.3f " % (time.time()-currentTime))
            f.write(' 0'  + ' ' + str(move) + ' ' + str(dX) + ' ' + str(dY) + '\n') 
            currentTime=time.time()    


            if a != state_left or b != state_right: # Button state changed
                f.write("%.3f " % (time.time()-currentTime))
                if a != state_left:  
                    state_left = a
                    mouseStateA = str(mouseUp)
                    if a < 0: mouseStateA = str(mouseDown)
                    f.write(' ' + str(leftMouse) + ' ' + str(mouseDown) + ' ' + str(dX) + ' ' + str(dY) + '\n') 

                if b != state_right: 
                    state_right = b
                    mouseStateB = str(mouseUp)
                    if a < 0: mouseStateB = str(mouseDown)
                    f.write(' ' + str(rightMouse) + ' ' + str(mouseDown) + ' ' + str(dX) + ' ' + str(dY) + '\n')

        time.sleep(0.001)
        
def play(loopTime = 1, sleepTime = 0.1):
    f = open('record.txt','r')
    lineStr = f.readlines()
    play_button = win32api.GetKeyState(0x32)
    leftMouse=0x01
    rightMouse=0x02
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

            if int(currentEvent[1]) == 1 :
                if int(currentEvent[2]) == mouseDown:
                    M.click(button_name='left')
                if int(currentEvent[2]) == mouseUp:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,
                    0,0,0,0)
            elif int(currentEvent[1]) == 2 :
                if int(currentEvent[2]) == mouseDown:
                    M.click(button_name='right')
                if int(currentEvent[2]) == mouseUp:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,
                    0,0,0,0)           
        time.sleep(sleepTime)

def _main():
    while True:
        toggled = False
        isPlay = False
        
        # while win32api.GetKeyState(0x33) not in [0,1]:
        #     return
        
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

# M = mousefunc.Mouse()
# l = mouse.record()
# print(l)
# mouse.play(l)

# while 1:
#     time.sleep(1)
#     print ( win32gui.GetCursorInfo() )
#     print ( M.get_position() )



