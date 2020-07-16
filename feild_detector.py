import json

with open('final.json', 'r') as f:
    data = json.loads(f.read())
mouse = False
fields = {}
final_fields = {}
counter = 0
for key, value in data.items():
    mouse = False
    for i, action in enumerate(value['actions']):
        # check mouse click
        # followed by keyboard action
        # until another click
        if action['input'] == 'mouse_click':
            if not mouse:
                mouse = True
                continue
            else:
                counter += 1
        if action['input'] == 'keyboard' and mouse:
            if counter in fields.keys():
                fields[counter].append(i)
            else:
                fields[counter] = [i]
    if fields:
        final_fields[key] = fields
incrementer = 0
fin_action = []
for key, value in data.items():
    if key in final_fields.keys():
        popkeys = []
        lastkey = list(final_fields[key].keys())[-1]
        for k, val in final_fields[key].items():
            start = False
            for i, action in enumerate(value['actions']):
                if i in val:
                    start = True
                    popkeys.append(i)
                    continue
                elif not start and i not in popkeys:
                    fin_action.append(action)
                    popkeys.append(i)
                elif not start:
                    continue
                else:
                    fin_action.append({"field_name": "field_{}".format(incrementer+1),
                                       "input": "field"})
                    incrementer += 1
                    if k == lastkey:
                        fin_action.append(action)
                        start = False
                    break
        value['actions'] = fin_action

with open('fin.json', 'w') as f:
    f.write(json.dumps(data))
#         pass
#     value['actions'].insert(val[0] + incrementer, {
#         "field_{}".format(k+1): "field name"
#     })
#     incrementer += 1
#     for v in val:
#         popkeys.append(v + 1)
# actions = value['actions']
# value['actions'] = []
# for i, v in enumerate(actions):
#     if i not in popkeys:
#         value['actions'].append(v)
a = 23
