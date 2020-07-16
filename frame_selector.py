import os
import json
from shutil import copy2


def pick_names(time_list, compare_list):

    picked_names = []
    for time in time_list:
        prev_frame = ''
        next_frame = ''
        for file in sorted(compare_list, reverse=True):
            if time - 0.5 < file <= time:
                prev_frame = file
                break
        for file in sorted(compare_list):
            if time <= file < 0.5:
                next_frame = file
                break
        if prev_frame:
            picked_names.append(prev_frame)
        if next_frame:
            picked_names.append(next_frame)
    for val in picked_names:
        str_value = str(val)
        if len(str_value.split('.')[1]) != 6:
            diff = 6 - len(str_value.split('.')[1])
            add = '0' * diff
            str_value += add
        name = str_value[0:2] + '_' + str_value[2:4] + '_' + str_value[4:] + '.jpg'
        file_name = 'frame_{}'.format(name)
        copy2('frames/{}'.format(file_name), 'final_frames/')
    return picked_names


frame_files = os.listdir('frames')
filename_int = []
keyboard_time = []
mouse_time = []
for filename in frame_files:
    filename_int.append(float(filename[6:-4].replace('_', '')))
with open('keyboard_tracker.json', 'r') as f:
    keyboard_data = json.loads(f.read())
with open('mouse_tracker.json', 'r') as fm:
    mouse_data = json.loads(fm.read())
for data in keyboard_data['track']:
    keyboard_time.append(float(data['time'].replace('_', '')))
for key, value in mouse_data.items():
    if key != 'moved':
        for item in value:
            # if 'mode' in item.keys():
            #     if item['mode'] == 'released':
            #         mouse_time.append(float(item['time'].replace('_', '')))
            # else:
            mouse_time.append(float(item['time'].replace('_', '')))

k_time = pick_names(keyboard_time, filename_int)
m_time = pick_names(mouse_time, filename_int)
# for value in k_time:
#     str_value = str(value)
#     if len(str_value.split('.')[1]) != 6:
#         diff = 6 - len(str_value.split('.')[1])
#         add = '0' * diff
#         str_value += add
#     name = str_value[0:2] + '_' + str_value[2:4] + '_' + str_value[4:] + '.jpg'
#     filename = 'frame_{}'.format(name)
#     copy2('frames/{}'.format(filename), 'final_frames/')

a = 23