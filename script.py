# -*- coding: utf-8 -*-
import vk_api
import re
import requests
from vk_acc import vk

def load_users(vk, group_id, count, offset, sort='id_asc'): # sort = id_desc
    users = []
    for n in range((count/1000) + 1):
        user_ids = vk.method('groups.getMembers', {'count': str(count-n*1000),
                                                'group_id': group_id,
                                                'offset': offset+n*1000,
                                                'sort': sort})['items']
        if len(user_ids) == 0:
            return users
        user_ids = [str(ui) for ui in user_ids]
        users_str = ','.join(user_ids)
        users += vk.method('users.get', {'user_ids': users_str,
                                        'fields': 'connections,status,sex,city'})
    return users

def get_instas(vk, users):
    instas = []
    for user in users:
        if 'instagram' in user:
            instas.append(user['instagram'])
        elif 'status' in user and 'instagram' in user['status'].lower():
            i = get_insta_from_status(user['status'])
            if i:
                instas.append(i)
            else:
                print user['status']
        #else:
        #    posts = load_user_posts(vk, user['id'])
        #    print get_instas_from_posts(posts)
    return instas

def load_user_posts(vk, ui):
    try:
        posts = vk.method('wall.get', {'owner_id': ui, 'count': '20', 'filter':'owner'})['items']
    except vk_api.ApiError:
        posts = []
    return posts

def get_insta_from_posts(posts):
    for post in posts:
        if 'platform' in post['post_source'] and post['post_source']['platform'] == 'instagram':
            try:
                return post['post_source']['url']
            except KeyError:
                return False

def load_group_id(vk, link):
    screen_name = link.rsplit('/')[-1]
    return vk.method("groups.getById", {"group_ids": screen_name})[0]['id']

def load_vk():
    return vk
    token = u'e828591d01bbe1351b1689de34d58cf7221583647eb59da7df4a652423f296420a98a1d903640d7c8a4641142f372'
    vk = vk_api.VkApi(token=token)
    #vk = vk_api.VkApi('79031109652', '111222')
    #vk.authorization()
    return vk

def run_script(screen_name):
    #vk = load_vk()
    group_id = load_group_id(vk, screen_name)
    users = load_users(vk, group_id, 1000)
    instas = get_instas(vk, users)
    return instas

def work_with_status(users):
    instas = []
    for user in users:
        if 'status' in user and 'instagram' in user['status'].lower():
            print user['status']
            instas.append(user['status'])
    return instas

def get_insta_from_status(status):
    li = re.findall('instagram.com/([a-zA-Z0-9\._]+)', status)
    if len(li) > 0:
        return li[0]
    s = re.sub('[\:\-\,]', ' ', status)
    li = s.split()
    for n in range(len(li)):
            try:
                if u'insta' in li[n].lower() or u'инста' in li[n].lower():
                    insta = re.findall('([a-zA-Z0-9_\.]+)', li[n+1])[0]
                    return insta
            except IndexError:
                pass
    return False
    
def load_insta_from_link(link):
    post = requests.get(link)
    text = post.text
    #print text.split('\n')[171]
    try:
        try:
            inst = re.findall('See this Instagram [^ ]+ by @([^ ]+)', text)[0]
        except IndexError:
            inst = re.findall('это [^ ]+ от @([^ ]+) на Instagram', text)[0]
    except IndexError:
        return False
    return inst

def first_wave(vk, group_id, count=3000, offset=0):
    if count > 120000:
        count = 120000
    users = load_users(vk, group_id, count, offset)
    if len(users) == 0:
        raise IndexError
    instas = []
    needed_users = []
    for user in users:
        if 'instagram' in user:
            instas.append(user)
        elif 'status' in user and ('insta' in user['status'].lower() or u'инста' in user['status'].lower()):
            i = get_insta_from_status(user['status'])
            if i:
                user['instagram'] = i
                instas.append(user)
        else:
            needed_users.append(user)
    return instas, needed_users

def second_wave(vk, ulist):
    print len(ulist)
    instas = []
    for user in ulist:
        posts = load_user_posts(vk, user['id'])
        link = get_insta_from_posts(posts)
        print link
        if link:
            #try: 3054352
            insta = load_insta_from_link(link)
            #except Exception as e:
            #    raise KeyError, str(e) + str(user['id'])
            if insta:
                instas.append(insta)
    return instas

def get_cities(cities):
    cities = list(set(cities))
    resp = load_vk().method('database.getCitiesById', {'city_ids': ','.join(cities)})
    cities = {}
    for n in resp:
        cities[n['id']] = n['title']
    return cities

def run(part, screen_name, full=False, extra_data=False):
    if full:
        part_size = 25
    else:
        part_size = 1000
    #vk = load_vk()
    group_id = load_group_id(vk, screen_name)
    try:
        instas, needed = first_wave(vk, group_id, count=part_size, offset=part*part_size)
    except IndexError:
        return 'Out of range' 
    if extra_data:
        instas = [{'instagram': n['instagram'], 'city': n.get('city', {'title': ''})['title'], 'sex': n['sex']} for n in instas]
        ins, new = [], []
        for n in instas:
            if not n['instagram'] in ins:
                ins.append(n['instagram'])
                new.append(n)
    else:
        new = [n['instagram'] for n in instas]
        new = list(set(new))

    if full:
        new += second_wave(vk, needed)
    return new






