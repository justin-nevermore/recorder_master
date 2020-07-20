import os
import shutil
import re

ROOT = os.getcwd()

def clear_dir(path):
    file_path = os.path.join(ROOT, path)
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
        os.makedirs(file_path)
    else:
        os.makedirs(file_path)


def unicode_convert(data):
    unicode_hiffen_list = ['\u2010', '\u2011', '\u2012', '\u2013', '\u2014', '\u2015']
    hif_data = ''
    for hiffen in unicode_hiffen_list:
        if hiffen in data:
            data.replace(hiffen, '-')
            hif_data = '-'
            break
        else:
            hif_data = '-'
    return hif_data


