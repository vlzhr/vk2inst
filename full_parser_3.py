from json import loads
import requests
import vk_api
import re
from time import sleep
from codecs import open
import os

vk = vk_api.VkApi(token=u'e6ba07a7ccc1733c699f2244de37677b163c5c7b46c1816a7f5ea4f7fe8df7b4906b4c69d05a281784c47')

def get_f(name, mode='r'):
    path = os.path.join(__file__.replace(os.path.basename(__file__), ''), 'basa', name+'.txt')
    return open(path, mode, encoding='utf-8')

def load_gi(vk, link):
    screen_name = link.rsplit('/')[-1]
    li = re.findall('club([0-9]+)', screen_name) + re.findall('public([0-9]+)', screen_name)
    if len(li) > 0:
        return li[0]
    group_ids = vk.method('groups.search', {'q': screen_name, 'count': '100'})['items']
    for n in group_ids:
        if n['screen_name'] == screen_name:
            return n['id']
    raise KeyError('Group not found')   

def parse(link, full=0, step=0):
    screen_name = link.rsplit('/', 1)[-1]
    gi = u'club' + str(load_gi(vk, link))
    if step:
        n = step
        instas = ';'.split(get_f(screen_name+'-'+str(full), 'r').read())
        print(len(instas))
    else:
        n = 0
        instas = []
    while True:
        try:
            resp = requests.get('http://lev.msk0.ru', {'step': str(n), 'group': gi,
                                                'full': str(full)})
            n += 1
            try:
                try:
                    instas += loads(resp.text)['items']
                except ValueError:
                    print(resp.text)
                get_f(screen_name+'-'+str(full), 'w').write(u';'.join([str(nu) for nu in instas]))
                print(str(n) + u'\t' + str(len(instas)))
            except KeyError:
                return instas
        except requests.ConnectionError:
            print(u'Connection problems')
            sleep(2)
            
