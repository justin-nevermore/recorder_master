from multiprocessing import Process
import cv2
import numpy as np
import pyautogui
from win32gui import GetWindowText, GetForegroundWindow
# from PIL import ImageGrab

from win32api import GetSystemMetrics
import keyboard
from pynput.mouse import Listener
from pynput.keyboard import Listener as k_Listener
from datetime import datetime
import json
import time
global mouse_tracker, keyboard_tracker
mouse_tracker = {
    "moved": [],
    "clicked": [],
    "scrolled": []
}
keyboard_tracker = {
    "track": []
}


def on_move(x, y):
    # print('Pointer moved to {0} at {1}'.format(
    #     (x, y), datetime.now().strftime("%H:%M:%S")))
    mouse_tracker['moved'].append({
        "time": datetime.now().time().strftime("%H_%M_%S.%f"),
        "pos": (x, y)
    })


def on_click(x, y, button, pressed):
    # print('{0} at {1} at {2}'.format(
    #     'Pressed' if pressed else 'Released',
    #     (x, y), datetime.now().strftime("%H:%M:%S")))
    if pressed:
        mouse_tracker['clicked'].append({
            "time": datetime.now().time().strftime("%H_%M_%S.%f"),
            "pos": (x, y),
            "mode": 'pressed',
            "button": str(button)[7:]
        })
    else:
        mouse_tracker['clicked'].append({
            "time": datetime.now().time().strftime("%H_%M_%S.%f"),
            "pos": (x, y),
            "mode": 'released',
            "button": str(button)[7:]
        })


def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        (x, y), str(datetime.now().time())))
    mouse_tracker['scrolled'].append({
        "time":  datetime.now().time().strftime("%H_%M_%S.%f"),
        "pos": (x, y),
        "mode": 'scroll',
        "scroll": dy
    })


def on_press(key):
    keyboard_tracker['track'].append({
        "key_pressed": str(key),
        "time": datetime.now().time().strftime("%H_%M_%S.%f")
    })


def func1():
    # width = GetSystemMetrics(0)
    # height = GetSystemMetrics(1)
    # screen_size = (width, height)
    # fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # out = cv2.VideoWriter("output.avi", fourcc, 9.0, (screen_size))
    start = False
    printer = False
    while True:
        # make a screenshot
        if keyboard.is_pressed('1') and not start:
            if not printer:
                print('frame recorder started')
                printer = True
            start = True
            start_time = datetime.now().time().strftime("%H_%M_%S.%f")
            print(start_time)
        if start:

            img = pyautogui.screenshot()
            c_time = datetime.now().time().strftime("%H_%M_%S.%f")
            img.save('frames/frame_{}.jpg'.format(c_time))
            # convert these pixels to a proper numpy array to work with OpenCV
            # frame = np.array(img)
            # convert colors from BGR to RGB
            # frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # write the frame
            # time.sleep(1)
            # out.write(frame)
            # show the frame
            # cv2.imshow("screenshot", frame)
            # if the user clicks q, it exits
        if keyboard.is_pressed('0'):
            end_time = datetime.now().time().strftime("%H_%M_%S.%f")
            print(end_time)
            break

    # make sure everything is closed when exited
    # cv2.destroyAllWindows()
    # out.release()


def func2():
    listener = Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    start = '00:00:00'
    printer = False
    while True:
        if keyboard.is_pressed('1'):
            if not printer:
                print('mouse recorder started')
                printer = True
            if not listener.is_alive():
                listener.start()
        if keyboard.is_pressed('0') and listener.is_alive():
            listener.stop()
            with open('mouse_tracker.json', 'w+') as f:
                f.write(json.dumps(mouse_tracker))
            break


def func3():
    printer = False
    k_listener = k_Listener(on_press=on_press)
    while True:
        if keyboard.is_pressed('1'):
            if not printer:
                print('keyboard traker started')
                printer = True
            if not k_listener.is_alive():
                k_listener.start()
        if keyboard.is_pressed('0') and k_listener.is_alive():
            k_listener.stop()
            with open('keyboard_tracker.json', 'w+') as file:
                file.write(json.dumps(keyboard_tracker))
            break


def func4():
    window_dict = {}
    start_time = ''
    end_time = ''
    prev_window = ''
    count = 0
    start = False
    while True:
        if keyboard.is_pressed('1') or start:
            if not start:
                print('window tracker started')
            cur_window = GetWindowText(GetForegroundWindow())
            if not start_time:
                start_time = datetime.now().time().strftime("%H_%M_%S.%f")
            start = True
            if not prev_window:
                prev_window = cur_window
            else:
                if prev_window != cur_window and cur_window != '':
                    end_time = datetime.now().time().strftime("%H_%M_%S.%f")
                    window_dict[count] = {
                        "start_time": start_time,
                        "end_time": end_time,
                        "window": prev_window
                    }
                    start_time = ''
                    count += 1
                    prev_window = cur_window
        if keyboard.is_pressed('0'):
            if prev_window:
                end_time = datetime.now().time().strftime("%H_%M_%S.%f")
                window_dict[count] = {
                    "start_time": start_time,
                    "end_time": end_time,
                    "window": prev_window
                }
            with open('window_tracker.json', 'w+') as fw:
                fw.write(json.dumps(window_dict))
            break


if __name__ == '__main__':
    p1 = Process(target=func1)
    p2 = Process(target=func2)
    p3 = Process(target=func3)
    p4 = Process(target=func4)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    print('Bye')
