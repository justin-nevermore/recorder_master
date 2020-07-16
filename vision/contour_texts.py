import pytesseract
import cv2
import collections

def tess_data_parser(tess_data):
    try:
        left = []
        width = []
        top = []
        height = []
        text = []
        level = ''
        full_list = tess_data.split('\t')
        data_dict = []
        a = 17
        counter = 0
        while a + 5 < len(full_list) - 1:
            if int(full_list[a + 4]) != -1:
                if not level:
                    level = int(full_list[a - 5])
                split_data = full_list[a + 5].split('\n')
                if level == 5:
                    if split_data[0] != '' and split_data[0] != ' ':
                        left.append(int(full_list[a]))
                        top.append(int(full_list[a + 1]))
                        width.append(int(full_list[a + 2]))
                        height.append(int(full_list[a + 3]))
                        text.append(split_data[0])
                        data_dict.append({
                            "coords": {'x': left[-1], 'y': top[-1], 'h': height[-1], 'w': width[-1]},
                            "text": text[-1],

                        })
                if len(split_data) > 1:
                    level = int(split_data[-1])
                else:
                    break
                counter += 1
            else:
                split_data = full_list[a + 5].split('\n')
                level = int(split_data[-1])
            a += 11

        return data_dict
    except Exception as e:
        print("Error in tess data parser: ", e)
        return None


def sort_by_y(rows):
    n = len(rows)
    for _ in range(n):
        for j in range(0, n - _ - 1):
            if rows[j]['coords']['y'] > rows[j + 1]['coords']['y']:
                rows[j], rows[j + 1] = rows[j + 1], rows[j]
    return rows


def sort_by_row(data_dict):
    try:
        y_axis_dict = {}
        for dict_values in data_dict:
            y = dict_values['coords']['y']
            if y_axis_dict:
                for key, values in y_axis_dict.items():
                    if y - 9 <= key <= y + 9:
                        append_key = key
                        values.append(dict_values)
                        append_data = values
                        break
                    else:
                        append_key = y
                        append_data = [dict_values]
            else:
                append_key = y
                append_data = [dict_values]
            y_axis_dict[append_key] = append_data
        return y_axis_dict
    except Exception as e:
        print("Error in sorting rowise: ", e)
        return None


def sort_by_x(rows):
    n = len(rows)
    for _ in range(n):
        for j in range(0, n - _ - 1):
            if rows[j]['coords']['x'] > rows[j + 1]['coords']['x']:
                rows[j], rows[j + 1] = rows[j + 1], rows[j]
    return rows


def group_nearby_texts(row_d, ima, limit):
    new_row_d = {}
    row_d = collections.OrderedDict(sorted(row_d.items()))
    try:
        for key, row in row_d.items():
            row = sort_by_x(row)
            for i, item in enumerate(row):
                # ima1 = ima.copy()
                # ima2 = ima1.copy()
                # ima3 = ima2.copy()
                modified = False
                if i != len(row) - 1:
                    f_x = item['coords']['x']
                    f_y = item['coords']['y']
                    f_w = item['coords']['w']
                    f_h = item['coords']['h']
                    f_text = item['text']
                    # cv2.rectangle(ima1, (f_x, f_y), (f_x + f_w, f_y + f_h), (0, 0, 255), 1)
                    # cv2.imwrite('fool.jpg', ima1)
                    s_x = row[i + 1]['coords']['x']
                    s_w = row[i + 1]['coords']['w']
                    s_y = row[i + 1]['coords']['y']
                    s_h = row[i + 1]['coords']['h']
                    # cv2.rectangle(ima2, (s_x, s_y), (s_x + s_w, s_y + s_h), (0, 0, 255), 1)
                    # cv2.imwrite('fool2.jpg', ima2)
                    s_text = row[i + 1]['text']
                    if s_x <= f_x + f_w + limit:
                        row[i + 1]['coords']['x'] = f_x
                        row[i + 1]['coords']['w'] = s_x + s_w - f_x
                        row[i + 1]['coords']['y'] = min([s_y, f_y])
                        row[i + 1]['coords']['h'] = max(f_h, s_h)
                        # cv2.rectangle(ima3, (row[i + 1]['coords']['x'], row[i + 1]['coords']['y']), (row[i + 1]['coords']['x'] + row[i + 1]['coords']['w'], row[i + 1]['coords']['y'] + row[i + 1]['coords']['h']), (0, 0, 255), 1)
                        # cv2.imwrite('fool3.jpg', ima3)
                        row[i + 1]['text'] = f_text + ' ' + s_text
                        row[i + 1]['contour'] = True
                        item['contour'] = False
                        modified = True
                    else:
                        f_x = item['coords']['x']
                        f_y = item['coords']['y']
                        f_w = item['coords']['w']
                        f_h = item['coords']['h']
                        f_text = item['text']
                        # cv2.rectangle(ima1, (f_x, f_y), (f_x + f_w, f_y + f_h), (0, 0, 255), 1)
                        # cv2.imwrite('fool3.jpg', ima1)
                        item['contour'] = True

                else:
                    f_x = item['coords']['x']
                    f_y = item['coords']['y']
                    f_w = item['coords']['w']
                    f_h = item['coords']['h']
                    # cv2.rectangle(ima1, (f_x, f_y), (f_x + f_w, f_y + f_h), (0, 0, 255), 1)
                    item['contour'] = True
        for key, value in row_d.items():
            row = sort_by_x(value)
            for item in row:
                if item['contour']:
                    if key in new_row_d.keys():
                        new_row_d[key].append(item)
                    else:
                        new_row_d[key] = [item]
        newnew_row = []
        counter = 0
        for key, value in new_row_d.items():
            for val in value:
                val.pop('contour')
                newnew_row.append(val)
                x = val['coords']['x']
                w = val['coords']['w']
                y = val['coords']['y']
                h = val['coords']['h']
                cv2.rectangle(ima, (x, y), (x + w, y + h), (0, 0, 255), 1)
                cv2.imwrite('joined.jpg', ima)
                counter += 1
        return newnew_row

    except Exception as e:
        print("Error in grouping nearby texts: ", e)
        return None


def main(image_loc):
    image = cv2.imread(image_loc)
    data = pytesseract.pytesseract.image_to_data(image)
    words_dictionary = tess_data_parser(data)
    words_dictionary = sort_by_y(words_dictionary)
    row_data = sort_by_row(words_dictionary)
    limit = 15
    final_dict_list = group_nearby_texts(row_data, image, limit)
    final_dict_list = sort_by_y(final_dict_list)
    return final_dict_list
