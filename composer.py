import json
import os
import selenium
import pyautogui
import time


def main(fields):
    with open('fin.json', 'r+') as f:
        data = json.loads(f.read())
    with open('window_tracker.json', 'r') as fw:
        window_data = json.loads(fw.read())

    for d_key, d_value in data.items():
        window_name = window_data[d_key]['window']
        if 'Google Chrome' in window_name:
            os.system('start chrome "https://docs.google.com/forms/d/e/1FAIpQLSfVD_V6iGlv6jWRKzE6YePqL7CADV5WfqrfwEvFxMwB7LYiJQ/viewform?vc=0&c=0&w=1&fbzx=-7328151667264298851"')
            time.sleep(2)
        for actions in d_value['actions']:
            if actions['input'] == 'mouse_click':
                pyautogui.click(actions['pos'][0], actions['pos'][1])
            elif actions['input'] == 'mouse_scroll':
                pyautogui.scroll(actions['scroll'], actions['pos'][0], actions['pos'][1])
            elif actions['input'] == 'keyboard':
                pyautogui.typewrite(actions['key_pressed'].replace("'", ''))
            elif actions['input'] == 'field':
                field_data = fields[actions['field_name']]
                pyautogui.typewrite(str(field_data))

