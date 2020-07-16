import cv2
import math
from vision import contour_texts
import json
import os

frame_files = os.listdir('C:/Users/AshSri/PycharmProjects/recorder_master/final_frames')
filename_int = []


for filename in frame_files:
    filename_int.append(float(filename[6:-4].replace('_', '')))
filename_int.sort(reverse=True)

with open('C:/Users/AshSri/PycharmProjects/recorder_master/fin.json', 'r') as f:
    data = json.loads(f.read())

for window_no, events in data.items():
    actions = events['actions']
    for i, act in enumerate(actions):
        if act['input'] == 'field':
            time = actions[i-1]['time']
            for t_value in filename_int:
                if t_value <= time:
                    time_str = str(t_value)
                    if len(time_str.split('.')[1]) != 6:
                        diff = 6 - len(time_str.split('.')[1])
                        add = '0' * diff
                        time_str += add
                    image_loc = 'final_frames/frame_' + time_str[0:2] + '_' + time_str[2:4] + '_' + time_str[4:] + '.jpg'
                    text_list = contour_texts.main(image_loc)
                    image = cv2.imread(image_loc)
                    x = actions[i-1]['pos'][0]
                    y = actions[i-1]['pos'][1]
                    min = 99999
                    for i, item in enumerate(text_list):
                        xx = item['coords']['x']
                        yy = item['coords']['y']
                        hh = item['coords']['h']
                        ww = item['coords']['w']

                        # check for left near box

                        # if xx + ww >= x - 30 and yy - 10 < y <= yy + hh + 10:
                        #     # name of the field is on the left
                        #     pass
                        # check for top near box
                        if yy < y and xx <= x:
                            if math.sqrt((x - xx + ww) ** 2 + (y - yy + hh) ** 2) < min and 'answer' not in item['text']:
                                min = math.sqrt((x - xx + ww) ** 2 + (y - yy + hh) ** 2)
                                coords = item
                    act['field_name'] = coords['text']
                    break

with open('fin.json', 'w+') as f:
    f.write(json.dumps(data))



a = 23


'''
Put conditions to find the nearest contour
'''