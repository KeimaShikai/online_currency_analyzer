#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# autor: KeimaShikai
# version: 0.1


from requests import get
from re import findall


'''FUTURE DOCS INFO

I will add some extra info in here to make it look like
I'm da professional.

'''


URL_BASE = 'https://mainfin.ru/currency/'

REGULAR = r'>([а-яА-Я ]*)<\/a><\/td><td class="[\w\s-]*"><span id="[\w_-]*" '\
           'class="[\w_-]*" data-curse-val="([\d.]*)" data-iname="[\w\s-]*" '\
           'data-curse-multi="[\d]+">[\d.]*<\/span><\/td><td class="[\w\s-]*'\
           '"><span id="[\w_-]*" class="[\w_-]*" data-curse-val="([\d.]*)" data'


currency_values = ('usd', 'eur', 'gbp', 'kzt', 'cny', 'chf', 'jpy')

city_values = ('moskva', 'sankt-peterburg', 'ekaterinburg', 'kazan',
               'nizhniy-novgorod', 'novosibirsk', 'omsk', 'samara',
               'chelyabinsk', 'rostov-na-donu', 'ufa', 'krasnoyarsk',
               'perm', 'voronezh', 'volgograd', 'krasnodar',
               'saratov', 'tumen', 'tolyatti', 'izhevsk',
               'barnaul', 'irkutsk', 'ulyanovsk', 'habarovsk',
               'yaroslavl', 'vladivostok', 'mahachkala', 'tomsk',
               'orenburg', 'kemerovo', 'novokuzneck')


def main():
    """some info"""
    print('Варианты выбора:\n'
          '1: Стандартный поиск   (доллары, Томск)\n'
          '2: Настраиваемый поиск (выбор валюты и города)\n'
          '3: Вывод подсказки\n'
          '0: Выход из программы')
    while (True):
        switch = input('Введите номер действия: ')
        if   (switch == "1"):
            process_data(URL_BASE + 'usd/tomsk')
            quit()
        elif (switch == "2"):
            filtered_search()
            quit()
        elif (switch == "3"):
            show_help_info()
        elif (switch == "0"):
            print('На подскоке!')
            quit()
        else:
            print('Неверный ввод!')

def show_help_info():
    """some info"""
    print('Тут будут данные')
    # TODO add nice output

def filtered_search():
    """some info"""
    currency = input('Пожалуйста, введиете наименование валюты: ')
    if (currency not in currency_values):
        print('Вы ввели неверное название валюты!')
        quit()

    city = input('И введите название города: ')
    if (city not in city_values):
        print('Вы ввели неверное название города!')
        quit()

    process_data(URL_BASE + currency + '/' + city)

def process_data(url):
    """some info"""
    content = get(url).content.decode('utf-8')
    data = findall(REGULAR, content)
    for each in data:
        print("{0}: \nпокупка: {1}, продажа: {2}\n".format(each[0],
                                                           each[1],
                                                           each[2]))

# TODO remove this function
def test():
    with open('tomsk.html', 'r') as test:
        t = test.read()
        data = findall(REGULAR, t)
        for i in data:
            print("{0}: \nпокупка: {1}, продажа: {2}\n".format(i[0], i[1], i[2]))


# TODO add writing into the file
# TODO add output dividers through the decorators
# TODO test all parts
# TODO comment the code
# TODO fix README
# TODO add GUI?

if __name__ == '__main__':
    main()
    #test()
