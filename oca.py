#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# autor: KeimaShikai
# version: 0.1


from requests import get
from re import findall
from time import strftime


'''FUTURE DOCS INFO

I will add some extra info in here to make it look like
I'm da professional.

'''


URL_BASE = 'https://mainfin.ru/currency/'

REGULAR = r'>([а-яА-Я ]*)<\/a><\/td><td class="[\w\s-]*"><span id="[\w_-]*" '\
           'class="[\w_-]*" data-curse-val="([\d.]*)" data-iname="[\w\s-]*" '\
           'data-curse-multi="[\d]+">[\d.]*<\/span><\/td><td class="[\w\s-]*'\
           '"><span id="[\w_-]*" class="[\w_-]*" data-curse-val="([\d.]*)" data'


currency_values = {'Доллар' : 'usd',
                   'Евро'   : 'eur',
                   'Фунт'   : 'gpb',
                   'Тенге'  : 'kzt',
                   'Юань'   : 'cny',
                   'Франк'  : 'chf',
                   'Йена'   : 'jpy'}

# city_values = ('moskva', 'sankt-peterburg', 'ekaterinburg', 'kazan',
               # 'nizhniy-novgorod', 'novosibirsk', 'omsk', 'samara',
               # 'chelyabinsk', 'rostov-na-donu', 'ufa', 'krasnoyarsk',
               # 'perm', 'voronezh', 'volgograd', 'krasnodar',
               # 'saratov', 'tumen', 'tolyatti', 'izhevsk',
               # 'barnaul', 'irkutsk', 'ulyanovsk', 'habarovsk',
               # 'yaroslavl', 'vladivostok', 'mahachkala', 'tomsk',
               # 'orenburg', 'kemerovo', 'novokuzneck')

city_values = {'Москва'          : 'moskva',
               'Санкт-Петербург' : 'sankt-peterburg',
               'Екатеринбург'    : 'ekaterinburg',
               'Kазань'          : 'kazan',
               'Нижний Новгород' : 'nizhniy-novgorod',
               'Новосибирск'     : 'novosibirsk',
               'Омск'            : 'omsk',
               'Самара'          : 'samara',
               'Челябинск'       : 'chelyabinsk',
               'Ростов-на-Дону'  : 'rostov-na-donu',
               'Уфа'             : 'ufa',
               'Красноярск'      : 'krasnoyarsk',
               'Пермь'           : 'perm',
               'Воронеж'         : 'voronezh',
               'Волгоград'       : 'volgograd',
               'Краснодар'       : 'krasnodar',
               'Саратов'         : 'saratov',
               'Тюмень'          : 'tumen',
               'Тольятти'        : 'tolyatti',
               'Ижевск'          : 'izhevsk',
               'Барнаул'         : 'barnaul',
               'Иркутск'         : 'irkutsk',
               'Ульяновск'       : 'ulyanovsk',
               'Хабаровск'       : 'habarovsk',
               'Ярославль'       : 'yaroslavl',
               'Владивосток'     : 'vladivostok',
               'Махачкала'       : 'mahachkala',
               'Томск'           : 'tomsk',
               'Оренбург'        : 'orenburg',
               'Кемерово'        : 'kemerovo',
               'Новокузнецк'     : 'novokuzneck'}


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
            process_data()
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
    print()
    print('Данная софтина предоставляет возможность за несколько секунд\n'
          'получить информации о курсе определенной валюты в различныйх\n'
          'банках через вашу консоль. Быстро и удобно.\n')
    print('Имеется возможность вывода информации в консоль\n'
          'или записи в файл.')
    print()
    print('В качестве валют Вы можете выбрать следующие варианты:')
    print(', '.join(currency_values))
    print()
    print('В качестве городов Вы можете выбрать следующие варианты:')
    city_list = list(city_values)
    for i in range(0, len(city_list), 3):
        print(', '.join(city_list[i:i + 3]))

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

    process_data(currency, city)

def process_data(currency="Доллар", city="Томск"):
    """some info"""
    content = get(URL_BASE + currency_values.get(currency)
                     + '/' + city_values.get(city)).content.decode('utf-8')
    data = findall(REGULAR, content)
    print()
    print('Сводка на данный момент времени:\n')
    for each in data:
        print("{0}:\nпокупка: {1} руб, продажа: {2} руб\n".format(each[0],
                                                                  each[1],
                                                                  each[2]))
    print()
    if (input('Введите \'1\' для записи в файл: ') == '1'):
        file_name = currency + '_' + city + strftime('_%d_%b_%H:%M.log')
        with open(file_name, 'w') as file:
            for each in data:
                file.write("{0}:\nпокупка: {1} руб, "\
                           "продажа: {2} руб\n".format(each[0],
                                                       each[1],
                                                       each[2]))


# TODO remove this function
def test():
    with open('tomsk.html', 'r') as test:
        t = test.read()
        data = findall(REGULAR, t)
        print('Сводка на данный момент времени:\n')
        for i in data:
            print("{0}: \nпокупка: {1} руб, продажа: {2} руб\n".format(i[0], i[1], i[2]))


# TODO add output dividers through the decorators
# TODO test all parts (and check names
# TODO comment the code
# TODO fix README
# TODO add GUI?


if __name__ == '__main__':
    main()
    #test()
