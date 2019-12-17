#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# autor: KeimaShikai
# version: 0.1


from requests import get
from re import findall
from time import strftime
from functools import wraps


'''Online currency analyzer (Онлайн анализатор валют)

This code is a script, the main task of which is to download certain pages
of fixed sites, and then parse data related to the rate of given currencies
in various banks of Russian cities. Additionally, banks with the cheapest
purchase and the most expensive sale of currency are determined. The parsed
data can be saved to a file for subsequent manual analysis.

Данный код является скриптом, основная задача которого заклчается в том, чтобы
выгружать определенные странницы фиксированных сайтов, а затем разбирать
данные, связанные с курсом заданных валют в различных банках ряда городов
России. Дополнительно определяются банки с самой дешевой закупкой и с самой
дорогой продажей валюты. Разобранные данные можно сохранить в файл для их
последующего ручного анализа.

'''


URL_BASE = 'https://mainfin.ru/currency/'

REGULAR = r'>([а-яА-Я ]*)<\/a><\/td><td class="[\w\s-]*"><span id="[\w_-]*" '\
           'class="[\w_-]*" data-curse-val="([\d.]*)" data-iname="[\w\s-]*" '\
           'data-curse-multi="[\d]+">[\d.]*<\/span><\/td><td class="[\w\s-]*'\
           '"><span id="[\w_-]*" class="[\w_-]*" data-curse-val="([\d.]*)" data'


currency_values = {'Доллар' : 'usd',
                   'Евро'   : 'eur',
                   'Фунт'   : 'gbp',
                   'Тенге'  : 'kzt',
                   'Юань'   : 'cny',
                   'Франк'  : 'chf',
                   'Йена'   : 'jpy'}

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


def dividers(func):
    @wraps(func)
    def wrapper(*args):
        print('\n|********************************************************|\n')
        func(*args)
        print('\n|********************************************************|\n')
    return wrapper


def get_column_from_complex_list(passed_list, column_index):
    return [row[column_index] for row in passed_list]


def main():
    """Literally the main cycle of a script"""
    print('Варианты выбора:\n'
          '1: Стандартный поиск   (Доллар, Томск)\n'
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


@dividers
def show_help_info():
    """Help info handler"""
    print('Онлайн анализатор валют')
    print()
    print('Данная софтина предоставляет возможность за несколько секунд\n'
          'получить информации о курсе определенной валюты в различныйх\n'
          'банках через вашу консоль. Быстро и удобно.\n'
          'Дополнительно выводится информация о выгодных покупке\n'
          'и продаже валюты с соответствующими банками для выбраного\n'
          'города.')
    print()
    print('Имеются возможности:\n'
          ' - вывода информации в консоль;\n'
          ' - и записи в файл.')
    print()
    print('В качестве валют Вы можете выбрать следующие варианты:')
    print(', '.join(currency_values))
    print()
    print('В качестве городов Вы можете выбрать следующие варианты:')
    city_list = list(city_values)
    for i in range(0, len(city_list), 3):
        print(', '.join(city_list[i:i + 3]))
    print()
    print('P.S.: Не во всех городах принимают все валюты!')


@dividers
def filtered_search():
    """Search filter settings function"""
    currency = input('Пожалуйста, введите наименование валюты: ')
    if (currency not in currency_values):
        print('Вы ввели неверное название валюты!')
        print('Список доступных валют можно просмотреть в выводе подсказки.')
        quit()

    city = input('И введите название города: ')
    if (city not in city_values):
        print('Вы ввели неверное название города!')
        print('Список доступных городов можно просмотреть в выводе подсказки.')
        quit()

    process_data(currency, city)


@dividers
def process_data(currency="Доллар", city="Томск"):
    """The function that parses and outputs data"""
    content = get(URL_BASE + currency_values.get(currency)
                     + '/' + city_values.get(city)).content.decode('utf-8')
    data = findall(REGULAR, content)

    if len(data) > 0:
        print('Сводка на данный момент времени:\n')
        for each in data:
            print("{0}:\nпокупка: {1} руб, продажа: {2} руб\n".format(each[0],
                                                                      each[1],
                                                                      each[2]))

        # look for min purchase price and its bank
        min_city = max_city = ''
        buy  = get_column_from_complex_list(data, 1)
        min_buy = min(buy)
        for each in data:
            if each[1] == min_buy:
                min_city = each[0]
                break

        # look for max sell price and its bank
        sell = get_column_from_complex_list(data, 2)
        max_sell = max(sell)
        for each in data:
            if each[2] == max_sell:
                max_city = each[0]
                break

        print('Итог:')
        print('Самая дешевая покупка: ' + min_buy + ' руб в ' + min_city)
        print('Самая дорогая продажа: ' + max_sell + ' руб в ' + max_city)
        print()

        # writing into the file block
        if (input('Введите \'1\' для записи в файл: ') == '1'):
            file_name = currency + '_' + city + strftime('_%d_%b_%H:%M.log')
            with open(file_name, 'w') as file:
                for each in data:
                    file.write("{0}:\nпокупка: {1} руб, "\
                               "продажа: {2} руб\n".format(each[0],
                                                           each[1],
                                                           each[2]))
                file.write('\n')
                file.write('Итог:\n')
                file.write('Самая дешевая покупка: ' + min_buy
                                                     + ' руб в ' + min_city)
                file.write('\n')
                file.write('Самая дорогая продажа: ' + max_sell
                                                     + ' руб в ' + max_city)
                file.write('\n')
            print()
            print('Успешно сохранено в файл: ' + file_name)
    else:
        print('Ничего не найдено! Вероятно, в этом городе нет банков,\n'
              'работающих с выбранной Вами валютой. :-( ')


if __name__ == '__main__':
    main()
