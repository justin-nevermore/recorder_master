
import browserhistory as bh
import json

history_data = bh.get_browserhistory()  # brings chrom & firbox  browser history

chrome_dict = {}
with open("window_tracker.json", 'r') as F:
    d = json.loads(F.read())
for key1, value1 in d.items():  # from recorded window removing non chrome windows
    json_window_name = value1['window']
    if 'chrome' in json_window_name.lower():
        chrome_dict[key1] = value1
    else:
        pass


def get_url():
    final_url = []
    for key2, value2 in history_data.items():  # from history tracker getting all history from chrome only
        if key2.lower() == 'chrome':  # to get only from chrome
            for key3, value3 in chrome_dict.items():  # checking in sorted chrome dict
                json_page_name = value3['window'].replace(" - Google Chrome", "")
                for items in value2:
                    url = items[0]
                    url_page_name = items[1]
                    url_time = items[2]
                    if json_page_name.lower() == url_page_name.lower():
                        if final_url:
                            for it in final_url:
                                if it != url:
                                    final_url.append(url)
                                else:
                                    pass
                        else:
                            final_url.append(url)
                    else:
                        pass
        else:
            pass
    return final_url

