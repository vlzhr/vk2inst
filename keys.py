from json import load, dump
import os
from codecs import open
import random
import time

dic = {}

flink = os.path.join(__file__.replace(os.path.basename(__file__), ''),
                     'keys', 'keys.txt')

def open_file(mode='rb', link=flink):
    return open(link, mode, encoding='utf-8')

def get_keydic():
    return load(open_file())

def get_keys():
    return get_keydic().keys()

def add_key(key=None):
    keys = get_keydic()
    if key is None:
        while True:
            key = random.randint(1000000, 9999999)
            if not key in keys:
                break
    keys[key] = time.time()
    dump(keys, open_file('wb'))
    return key
