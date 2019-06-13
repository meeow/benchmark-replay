import win32gui, win32api, win32con
import ctypes
import time
import mousefuncs, keyboard

from key_reference import vk_keys, keys, codes, vk_codes
from logger import logger

M = mousefuncs.Mouse()

WIDTH, HEIGHT = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
BUTTON_DOWN, BUTTON_UP = 1, 0
RECORD_BTN, PLAY_BTN = vk_keys['VK_1'], vk_keys['VK_2']
# X_SENS = 0.03
# Y_SENS = X_SENS / 2
X_SENS = 1
Y_SENS = 1

def record(ST=0.005):
    buffer = []

    record_button = win32api.GetKeyState(RECORD_BTN) 
    prev_states = {key: win32api.GetKeyState(vk_keys[key]) for key in list(vk_keys.keys())}
    current_time = time.time()
    x_edge, y_edge = 0,0
    prev_x, prev_y = win32api.GetCursorPos()

    while True:
        recording = win32api.GetKeyState(RECORD_BTN)

        if recording != record_button:
            logger.debug('Saving buffers...')
            f = open('record.txt', 'w')
            for item in buffer:
                f.write(item)
            time.sleep(0.5)
            logger.debug('Buffer save complete.')
            f.close()
            return
        
        if time.time() - current_time > ST:
            switch = 0
            current_x, current_y = win32api.GetCursorPos()
            current_states = {key: win32api.GetKeyState(vk_keys[key]) for key in vk_keys}

            # move mouse back to center if it gets to the edge
            if current_x <= 0 or current_x >= WIDTH-1:
                switch = 1
                M.move_mouse((WIDTH//2, current_y))
            if current_y >= HEIGHT-1 or current_y <= 0:
                switch = 1
                M.move_mouse((current_x, HEIGHT//2))

            delta_x, delta_y = X_SENS * (current_x + (switch * x_edge) - prev_x), Y_SENS * (current_y + (switch * y_edge) - prev_y)
            prev_x, prev_y = current_x, current_y

            # remove offset caused by moving mouse back to center 
            if delta_x >= X_SENS * WIDTH // 3: 
                delta_x -= X_SENS * WIDTH // 2
                logger.debug('Triggered')
            if delta_y >= Y_SENS * HEIGHT // 3: 
                delta_y -= Y_SENS * HEIGHT // 2
                logger.debug('Triggered')
            if delta_x <= X_SENS * -WIDTH // 3: 
                delta_x += X_SENS * WIDTH // 2
                logger.debug('Triggered')
            if delta_y <= Y_SENS * -HEIGHT // 3: 
                delta_y += Y_SENS * HEIGHT // 2
                logger.debug('Triggered')

            buffer += ['{} 0 0 {} {} \n'.format(time.time() - current_time, delta_x, delta_y)]

            current_time = time.time()    

            if prev_states != current_states: # Button state changed
                for key in current_states:
                    if current_states[key] != prev_states[key]:
                        button_action = BUTTON_UP
                        if current_states[key] < 0: 
                            button_action = BUTTON_DOWN
                        buffer += ['0 {} {} 0 0 \n'.format(str(vk_keys[key]), str(button_action))]
                        logger.debug("[ Record ] {} [{}] toggled {}".format(key, vk_keys[key], button_action))

            prev_states = current_states
            
        time.sleep(0.001)
        
def play(loopTime = 1, sleepTime = 0.1):
    f = open('record.txt','r')
    lines = f.readlines()
    play_button = win32api.GetKeyState(PLAY_BTN)

    while loopTime:
        loopTime -= 1

        for line in lines:
            currentEvent = line.split()
            playing = win32api.GetKeyState(PLAY_BTN)
            if playing != play_button:
                time.sleep(0.5)
                f.close()
                return
                
            time.sleep(float(currentEvent[0]))
            movX, movY = int(currentEvent[3]), int(currentEvent[4])
            #M.move_relative((movX, movY))
            keyboard.move_mouse_to(movX, movY)

            if int(currentEvent[1]): # key pressed/released
                vk_key = vk_codes[int(currentEvent[1])]
                scan_key = vk_key[3:]

                # Temp workaround: M1/M2 map to N/M
                if scan_key == "M1": scan_key = "N"
                elif scan_key == "M2": scan_key = "M"

                if int(currentEvent[2]) == BUTTON_DOWN:
                    keyboard.press_key(scan_key)
                if int(currentEvent[2]) == BUTTON_UP:
                    keyboard.release_key(scan_key)

        time.sleep(sleepTime)

def _main():
    print ("Press [1] to start/stop recording and [2] to replay")
    while True:
        toggled = False
        isPlay = False

        while win32api.GetKeyState(RECORD_BTN) not in [0,1]:
            toggled = True
            time.sleep(0.01)
        if toggled:
            toggled = False
            record()
            
        while win32api.GetKeyState(PLAY_BTN) not in [0,1]:
            isPlay = True
            time.sleep(0.01)
        if isPlay:
            isPlay = False
            play()

        time.sleep(0.001)               

_main()



