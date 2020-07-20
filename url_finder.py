import browserhistory as bh
import json
from common import unicode_convert

def history():
    return bh.get_browserhistory()  # brings chrom & firbox  browser history


def get_url():
    chrome_dict = {}
    with open("window_tracker.json", 'r') as F:
        d = json.loads(F.read())
    for key1, value1 in d.items():  # from recorded window removing non chrome windows
        json_window_name = value1['window']
        if 'chrome' in json_window_name.lower():
            chrome_dict[key1] = value1
        else:
            pass
    pop_key = []
    history_data = history()
    for key2, value2 in history_data.items():  # from history tracker getting all history from chrome only
        if key2.lower() == 'chrome':
            for items in value2:
                url = items[0]
                url_page_name = items[1]
                url_time = items[2]
                for key3, value3 in chrome_dict.items():
                    hif_data = unicode_convert(value3['window'])
                    json_page_name = value3['window'].split(hif_data)[0]
                    if url_page_name.lower() in json_page_name.lower():
                        pop_key.append(key3)
                        chrome_dict[key3]['url'] = str(url)
                        break
                    else:
                        pass
        else:
            pass

    for item in pop_key:
        d.pop(item)
    d.update(chrome_dict)
    with open("url_updated.json",'w+') as f:
        f.write(json.dumps(d))
    return d


get_url()


