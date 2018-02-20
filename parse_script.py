'''
Пример использования сервиса http://lev.msk0.ru
'''


import requests
from json import loads


def parsing(screen_name):
    ''' Выполняет скрипт и записывает результат в файл result.txt '''
    result, step = [], 0
    while True:
        resp = requests.get('http://lev.msk0.ru/?step={}&group={}'.format(step, screen_name))
        resp = loads(resp.text)
        if 'error' in resp:
            break
        result += resp['items']
        step = step+1
        print('Step {} done.'.format(str(step)))
    result = list(set(result))
    open('result.txt', 'w', encoding='utf-8').write(','.join([str(n) for n in result]))
    return True
        
if __name__=="__main__":
    print("Введите ссылку на группу ВК")
    screen_name = input()
    parsing(screen_name)
    print("Программа завершена")
