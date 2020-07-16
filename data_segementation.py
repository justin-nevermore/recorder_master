import json
from collections import OrderedDict
with open('mouse_tracker.json', 'r') as fm:
    mouse_data = json.loads(fm.read())
with open('keyboard_tracker.json', 'r') as fk:
    key_data = json.loads(fk.read())

time_dict = {}

for key, data in mouse_data.items():
    if key != 'moved':
        for datum in data:
            if datum['mode'] != 'released':
                dict_key = float(datum.pop('time').replace('_', ''))
                time_dict[dict_key] = datum
                if datum['mode'] == 'pressed':
                    time_dict[dict_key]['input'] = 'mouse_click'
                elif datum['mode'] == 'scroll':
                    time_dict[dict_key]['input'] = 'mouse_scroll'


for key, value in key_data.items():
    for values in value:
        key = float(values.pop("time").replace('_', ''))
        time_dict[key] = values
        time_dict[key]['input'] = 'keyboard'

a = OrderedDict(sorted(time_dict.items()))

with open('window_tracker.json', 'r') as fw:
    window_data = json.loads(fw.read())
window_timed_data = {}
for index, value in window_data.items():
    start = float(value['start_time'].replace('_', ''))
    end = float(value['end_time'].replace('_', ''))
    for key in a.keys():
        if start <= key < end:
            a[key]['time'] = key
            if index in window_timed_data.keys():
                window_timed_data[index].append({key: a[key]})
            else:
                window_timed_data[index] = [{key: a[key]}]
final = {}
for window_index, data in window_timed_data.items():
    for dic in data:
        if window_index not in final.keys():
            final[window_index] = {"actions": [list(dic.values())[0]]}
        else:
            final[window_index]['actions'].append(list(dic.values())[0])

with open('final.json', 'w+') as ff:
    ff.write(json.dumps(final))
