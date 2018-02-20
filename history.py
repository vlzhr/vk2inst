import os
from json import load, dump
from codecs import open as old_open
import time

def vlink():
    day = time.strftime('%d')
    month = time.strftime('%m')
    if len(day) < 2:
        day = '0'+day
    if len(month) < 2:
        month = '0'+month
    day_month = day+month
    return os.path.join(__file__.replace(os.path.basename(__file__), ''), 'history', '{}.txt'.format(day_month))

def open(mode='rb'):
    try:
        return old_open(vlink(), mode, encoding='utf-8')
    except IOError:
        dump([], old_open(vlink(), 'wb', encoding='utf-8'))
        return old_open(vlink(), mode, encoding='utf-8')

def key():
    return int(time.time())

def tf(t):
    return time.strftime('%Y.%m.%d %H-%M-%S', time.gmtime(t))

def add_history(string):
    li = load(open())
    li.append([key(), string])
    dump(li, open('wb'))

def get_history():
    li = load(open())
    history = []
    for n in li:
        history.append({'time': tf(n[0]), 'text': n[1]})
    history.reverse()
    return history
