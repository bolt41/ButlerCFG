from django.http import response
from datetime import datetime
from django.shortcuts import render, HttpResponse
from django.template.response import TemplateResponse
from .models import *
from collections import Counter
import xlsxwriter
from math import ceil


def make_pivot_table(workbook, name, data_cost, sys, lev):  # функция заполнения листа сводной

    # запрос на значение констант с ценой на проектирование
    proekt_min = Constant.objects.get(name='proekt_min')
    proekt_max = Constant.objects.get(name='proekt_standart_max')

    # денежный формат
    format_money = workbook.add_format({'font_size': '10', 'num_format': '#,##0"₽"'})

    # формат для заголовка
    format_title = workbook.add_format({'font_color': 'white', 'font_size': '12', 'bg_color': '#4679fa'})

    format_info = workbook.add_format({'font_color': 'white', 'font_size': '8', 'bg_color': '#4679fa'})

    # формат для шапки таблицы
    format_header = workbook.add_format(
        {'font_color': 'white', 'font_size': '10', 'bg_color': '#4679fa', 'align': 'center'})

    # формат для первой строки таблицы
    format_one_string = workbook.add_format({'font_size': '10', 'bg_color': '#f5f0f0'})

    # формат для основного текста
    format_main_font = workbook.add_format({'font_size': '10'})

    # формат с границей
    format_with_border = workbook.add_format({'top': 6, 'bold': 'True', 'font_size': '10'})

    # формат с границей и денежным форматом
    format_with_border_money = workbook.add_format(
        {'top': 6, 'bold': 'True', 'font_size': '10', 'num_format': '#,##0"₽"'})

    # Создаем лист для сводной таблицы
    worksheet = workbook.add_worksheet('Свод')
    worksheet.set_tab_color('green')

    # Формируем заголовок листа и ширину ячеек
    worksheet.set_row(0, 20)
    worksheet.set_column('A:A', 3)
    worksheet.set_column('B:B', 6)
    worksheet.set_column('C:C', 45)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 15)
    worksheet.set_column('F:F', 15)
    worksheet.write('A1', '', format_title)
    worksheet.write('A2', '', format_title)
    worksheet.merge_range('B1:D1', 'СВОДНАЯ ТАБЛИЦА', format_title)
    worksheet.merge_range('B2:D2', 'стоимости оборудования и работ по подсистемам автоматизации', format_title)
    worksheet.merge_range('E1:F1', 'Объект:' + ' ' + name, format_info)
    worksheet.merge_range('E2:F2', 'Дата:' + ' ' + str(datetime.now().date()), format_info)

    # Формируем шапку таблицы
    worksheet.write('B5', '№', format_header)
    worksheet.write('C5', 'наименование раздела', format_header)
    worksheet.write('D5', 'Минимальный', format_header)
    worksheet.write('E5', 'Стандартный', format_header)
    worksheet.write('F5', 'Максимальный', format_header)

    # первая строка таблицы
    worksheet.merge_range('B6:F6', 'Базовые подсистемы автоматизации', format_one_string)

    # заполняем тело таблицы
    worksheet.write('C7', 'Управление освещением', format_main_font)
    worksheet.write('C8', 'Управление механизмами', format_main_font)
    worksheet.write('C9', 'Управление климатом', format_main_font)
    worksheet.write('C10', 'Органы управления', format_main_font)
    worksheet.write('C11', 'Мониторинг протечек/ресурсов', format_main_font)
    worksheet.write('C12', 'Аудио мультирум', format_main_font)
    worksheet.write('C13', 'Сеть и WiFi', format_main_font)
    worksheet.write('C14', 'Видеонаблюдение', format_main_font)
    worksheet.write('C15', 'Домофония', format_main_font)

    worksheet.merge_range('B16:F16', 'Системные разделы', format_one_string)
    worksheet.write('C17', 'Системное оборудование', format_main_font)
    worksheet.write('C18', 'Проектирование, исполнительная документация', format_main_font)
    worksheet.write('C19', 'Сборка щита автоматизации', format_main_font)

    worksheet.merge_range('B20:F20', 'Ключевые функции', format_one_string)
    worksheet.write('C21', 'Управление с мобильных устройств', format_main_font)
    worksheet.write('C22', 'Голосовое управление (Алиса, Siri)', format_main_font)

    # словарь с координатами ячеек по подсистемам и уровням
    system_in_page = {
        'Минимум': {'Освещение': 'D7', 'LAN': 'D13', 'Аудио': 'D12', 'Видеонаблюдение': 'D14', 'Домофония': 'D15',
                    'Климат': 'D9', 'Механизмы': 'D8', 'Мониторинг': 'D11', 'Устройства управления': 'D10',
                    'Системное оборудование': 'D17'},
        'Стандарт': {'Освещение': 'E7', 'LAN': 'E13', 'Аудио': 'E12', 'Видеонаблюдение': 'E14', 'Домофония': 'E15',
                     'Климат': 'E9', 'Механизмы': 'E8', 'Мониторинг': 'E11', 'Устройства управления': 'E10',
                     'Системное оборудование': 'E17'},
        'Максимум': {'Освещение': 'F7', 'LAN': 'F13', 'Аудио': 'F12', 'Видеонаблюдение': 'F14', 'Домофония': 'F15',
                     'Климат': 'F9', 'Механизмы': 'F8', 'Мониторинг': 'F11', 'Устройства управления': 'F10',
                     'Системное оборудование': 'F17'}}

    # цикл заполнения таблицы данными о стоимости работ/оборудования
    for element in sys:
        for level in lev:
            if element in data_cost[level]:
                worksheet.write(system_in_page[level][element], data_cost[level][element], format_money)

    worksheet.write('B25', 'Не включено в спецификации (после проектирования при необходимости)', format_main_font)
    worksheet.write('B26', '-', format_main_font)
    worksheet.write('C26', 'Кабель (электрический, слаботочный) и работы по прокладке', format_main_font)
    worksheet.write('B27', '-', format_main_font)
    worksheet.write('C27', 'Электрощит и базовые устройства защиты', format_main_font)
    worksheet.write('B28', '-', format_main_font)
    worksheet.write('C28', 'Электрофурнитура (обычные розетки, выключатели, вставки,рамки)', format_main_font)
    worksheet.write('B29', '-', format_main_font)
    worksheet.write('C29', 'Слаботочный шкаф)', format_main_font)

    # добавление подсчета итогов
    worksheet.write('B23', '', format_with_border)
    worksheet.write('C23', 'ИТОГО (оборудование и работы)', format_with_border)
    worksheet.write_formula('D23', '=SUM(D7:D19)', format_with_border_money)
    worksheet.write_formula('E23', '=SUM(E7:E19)', format_with_border_money)
    worksheet.write_formula('F23', '=SUM(F7:F19)', format_with_border_money)

    worksheet.write('D18', proekt_min.value, format_money)
    worksheet.write('E18', proekt_max.value, format_money)
    worksheet.write('F18', proekt_max.value, format_money)
    worksheet.write('E21', 'Да', format_main_font)
    worksheet.write('F21', 'Да', format_main_font)
    worksheet.write('E22', 'Да', format_main_font)
    worksheet.write('F22', 'Да', format_main_font)


def make_table_system(workbook, house, sys, choice_temp, all_param):  # функция заполнения ведомости

    # Создаем лист для ведомости
    worksheet = workbook.add_worksheet('Ведомость')
    worksheet.set_tab_color('green')

    # формат для заголовка
    format_title = workbook.add_format({'font_color': 'white', 'font_size': '12', 'bg_color': '#4679fa'})
    format_title_table = workbook.add_format({'font_size': '6', 'align': 'center', 'valign': 'vcenter', 'bold': True})
    format_title_table2 = workbook.add_format({'font_size': '6', 'align': 'center', 'rotation': '90'})
    format_table_text = workbook.add_format({'font_size': '6', 'align': 'center', 'valign': 'vcenter'})

    # Формируем заголовок листа и ширину ячеек
    worksheet.set_row(0, 20)
    worksheet.write('A1', '', format_title)
    worksheet.write('A2', '', format_title)
    worksheet.merge_range('B1:Y1', 'ВЕДОМОСТЬ', format_title)
    worksheet.merge_range('B2:Y2', 'элементов подсистем автоматизации', format_title)

    worksheet.set_column('A:A', 3)
    worksheet.set_column('B:C', 6)
    worksheet.set_column('D:D', 25)
    worksheet.set_column('E:AK', 3)

    # формат строки итогов
    format_with_border = workbook.add_format({'top': 6, 'bold': 'True', 'font_size': '10'})

    ###### Шапка таблицы
    rows = 3
    cols = 4

    worksheet.merge_range('B4:B7', '№ п/п', format_title_table)
    worksheet.merge_range('C4:C7', 'Область', format_title_table)
    worksheet.merge_range('D4:D7', 'Помещение', format_title_table)

    list_param = []
    itog = {}
    for system in sys:  # заполняем шапку таблицы и формируем словарь itog с данными из шаблонов
        if rows == 3:
            zapros = Params.objects.filter(system__name=system)
            count_zapros = zapros.count()
            if count_zapros != 0:
                worksheet.merge_range(rows, cols, rows, cols + count_zapros - 1, system, format_title_table)
                count_pod = cols
                for element in zapros:
                    list_param.append(element.name)
                    worksheet.merge_range(rows + 1, count_pod, rows + 3, count_pod, element.name, format_title_table2)

                    for key in house.keys():

                        for item in house[key]:
                            try:
                                dan = choice_temp.get(room__name=item, param__name=element.name)
                            except Templates.DoesNotExist:
                                if key in itog:
                                    itog[key].append([item, ''])
                                else:
                                    itog[key] = []
                                    itog[key].append([item, ''])
                            else:
                                if key in itog:
                                    itog[key].append([item, dan.count])
                                else:
                                    itog[key] = []
                                    itog[key].append([item, dan.count])
                    count_pod += 1

                cols = cols + count_zapros
    count_param = count_pod - 4  # ввычисляем количество параметров в таблице
    rows = 7
    cols = 1
    count = 1
    print(itog)
    for key in itog.keys():
        count_room = (int(len(itog[key]) / count_param))  # получаем количество комнат
        for i in range(count_room):
            worksheet.write(rows, cols, count, format_table_text)
            cols += 1
            worksheet.write(rows, cols, key, format_table_text)
            cols += 1
            worksheet.write(rows, cols, itog[key][i][0], format_table_text)
            cols += 1
            count += 1

            for j in range(i, len(itog[key]), count_room):
                print(itog[key][j])
                worksheet.write(rows, cols, itog[key][j][1], format_table_text)
                cols += 1
            rows += 1
            cols = 1

        print(len(itog[key]))

    # строка итогового подсчета

    cols = 4
    worksheet.write(rows, cols - 1, 'Итого:', format_with_border)
    for el in list_param:
        if el in all_param:
            worksheet.write(rows, cols, all_param[el], format_with_border)
            cols += 1
        else:
            worksheet.write(rows, cols, '', format_with_border)
            cols += 1

    print(rows, count_pod)
    print(all_param)
    print(list_param)

    # worksheet.write(rows, cols, count, format_title_table)
    # worksheet.write(rows, cols+1, key, format_title_table)
    # worksheet.write(rows, cols+2, itog[key])
    # count += 1
    # rows += 1


def make_content_systems(workbook, data_dict, data_cost, sys):  # функция заполнения листов по подсистемам
    format_title = workbook.add_format()
    format_title.set_font_color('#003366')
    format_title.set_font_size(16)

    format_level = workbook.add_format()
    format_level.set_font_size(14)
    format_level.set_font_color('#003366')

    format_bold = workbook.add_format({'bold': True})

    cols = 2
    rows = 1

    for i in sys:  # заполнение вкладок по подсистемам
        row = 3
        cols = 0
        a = Systems.objects.filter(name=i).get()
        worksheet = workbook.add_worksheet(i)
        worksheet.set_tab_color('red')
        worksheet.set_row(1, 20)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 50)
        worksheet.set_column('F:F', 10)
        worksheet.write(1, 1, a.public_text, format_title)  # добавление заголовка листа

        for key in data_dict.keys():

            cols += 3
            count_element = 1
            if i in data_dict[key]:
                worksheet.write(cols, rows, key, format_level)  # добавление уровня
                cols += 2
                for el in data_dict[key][i]:
                    worksheet.write(cols, rows, count_element)
                    rows += 1
                    for item in el:  # цикл заполнения данными оборудования
                        worksheet.write(cols, rows, item)
                        rows += 1
                    cols += 1
                    rows = 1
                    count_element += 1
                worksheet.write(cols, rows + 5, 'Итого:', format_bold)
                worksheet.write(cols, rows + 6, data_cost[key][i], format_bold)


def xlsxcreate(name, data_dict, data_cost, sys, lev, house, choice_temp,
               all_param):  # функция формирования и заполнения excel  документа
    path = './media/'
    workbook = xlsxwriter.Workbook(path + name + '.xlsx')

    make_table_system(workbook, house, sys, choice_temp, all_param)
    make_pivot_table(workbook, name, data_cost, sys, lev)
    make_content_systems(workbook, data_dict, data_cost,
                         sys)  # вызов функции создания и заполнения по выбранным подсистемам

    workbook.close()
    return name + '.xlsx'


def system_count(sys, all_room, count_room):  # подсчет показателей систем
    if 'Освещение' in sys:  # если
        sys.append('Устройства управления')
    a = Templates.objects.filter(room__name__in=all_room, param__system__name__in=sys)
    # создаем словарь итоговых параметров вида Система: счетчик
    param = dict()
    for el in a:
        if el.param.name in param:
            param[el.param.name] += el.count * count_room[el.room.name]  # умножаем на количество повторений комнат
        else:
            param[el.param.name] = el.count * count_room[el.room.name]  # умножаем на количество повторений комнат
    return param, a


def find_light(level, param1, sys):  # формируем список оборудования с необходимым количеством (уровень, подсистема)
    sys.append('Системное оборудование')
    all_system_query = Devices.objects.filter(system__name__in=sys)  # выбор всех устройств по выбранным системам
    dict_level = {}
    dict_cost = {}

    for i in level:
        param = param1.copy()  # создаем копию словаря, чтобы не изменялся родительский

        if 'Механизмы' in sys:
            if ('Шторы' in param) and ('Ворота' in param):
                param['Шторы'] = param['Шторы'] + param['Ворота']
            elif 'Ворота' in param:
                param['Шторы'] = param['Ворота']

        if 'Климат' in sys:
            if ('Теплый пол' in param) and ('Радиатор' in param):
                param['Радиатор'] = param['Радиатор'] + param['Теплый пол']
            elif 'Теплый пол' in param:
                param['Радиатор'] = param['Теплый пол']

        dict_cost[i] = {}
        dict_level[i] = {}
        a = all_system_query.filter(level__name=i, param__name__in=param, is_main=False)  # выбираем из всех устройств
        # только те, что с параметрами
        b = all_system_query.filter(level__name=i, param__name__in=param, is_main=True)  # выбираем базовые устройства
        # с параметрами
        c = all_system_query.filter(level__name=i, count=0, is_main=True)  # выбираем те, которые с main и
        # количеством входов 0
        e = c.filter(price__gt=1)  # выбираем базовые с count=0 и ценой больше 1
        f = c.filter(price__lte=1)
        g = c.filter(price=None)

        print(param)
        if 'Видеонаблюдение' in sys:  # если подсистема Видеонаблюдение выбрана
            count_cam = 0  # счетчик камер объявляем равный 0
            if ('Камера внутренняя' in param) and (
                    'Камера внешняя' in param):  # если в списке параметров есть и внутренние и внешние камеры, получаем их сумму
                count_cam = param['Камера внутренняя'] + param['Камера внешняя']  # либо только внешние или внутренние
            elif 'Камера внутренняя' in param:
                count_cam = param['Камера внутренняя']
            elif 'Камера внешняя' in param:
                count_cam = param['Камера внешняя']

            if count_cam > 0:  # проверяем, есть ли вообще камеры в
                # соответствии с выбранными шаблонами, если есть то
                # обрабатываем данную подсистему
                d = all_system_query.filter(level__name=i, system__name='Видеонаблюдение', is_main=True,
                                            count__gte=count_cam)

                for el in d:
                    if el.count - count_cam < count_cam:
                        if el.system.name in dict_level[i]:
                            dict_level[i][el.system.name].append(
                                [el.vendor.name, el.model, el.caption, 1, el.price, el.price])
                            dict_cost[i][el.system.name] = dict_cost[i][el.system.name] + el.price
                        else:
                            dict_level[i][el.system.name] = []
                            dict_cost[i][el.system.name] = 0
                            dict_cost[i][el.system.name] = dict_cost[i][el.system.name] + el.price
                            dict_level[i][el.system.name].append(
                                [el.vendor.name, el.model, el.caption, 1, el.price, el.price])
            elif count_cam == 0:  # если камер нет, то удаляем подсистему из списка выбранных
                sys.remove('Видеонаблюдение')

        for el1 in b:  # формируем список из базовых устройств с параметрами
            if el1.system.name in dict_level[i]:
                dict_level[i][el1.system.name].append(
                    [el1.vendor.name, el1.model, el1.caption, 1, el1.price, el1.price])
                dict_cost[i][el1.system.name] = dict_cost[i][el1.system.name] + el1.price
            else:
                dict_level[i][el1.system.name] = []
                dict_cost[i][el1.system.name] = 0
                dict_cost[i][el1.system.name] = dict_cost[i][el1.system.name] + el1.price
                dict_level[i][el1.system.name].append(
                    [el1.vendor.name, el1.model, el1.caption, 1, el1.price, el1.price])
            if el1.count > param[el1.param.name]:
                param[el1.param.name] = 0
            else:
                param[el1.param.name] -= el1.count

        for el in a:  # формируем список из оборудования с параметрами но не базового
            kol = ceil(param[el.param.name] / el.count)
            if kol > 0:
                if el.system.name in dict_level[i]:
                    dict_level[i][el.system.name].append(
                        [el.vendor.name, el.model, el.caption, kol, el.price, el.price * kol])
                    dict_cost[i][el.system.name] = el.price * kol + dict_cost[i][el.system.name]
                else:
                    dict_level[i][el.system.name] = []
                    dict_cost[i][el.system.name] = 0
                    dict_cost[i][el.system.name] = el.price * kol + dict_cost[i][el.system.name]
                    dict_level[i][el.system.name].append(
                        [el.vendor.name, el.model, el.caption, kol, el.price, el.price * kol])

        # оборудование с отметкой базовое, без параметров с count=0 и ценой выше 1
        for el in e:
            if el.system.name in dict_level[i]:
                dict_level[i][el.system.name].append(
                    [el.vendor.name, el.model, el.caption, 1, el.price, el.price])
                dict_cost[i][el.system.name] = dict_cost[i][el.system.name] + el.price
            else:
                dict_level[i][el.system.name] = []
                dict_cost[i][el.system.name] = 0
                dict_cost[i][el.system.name] = dict_cost[i][el.system.name] + el.price
                dict_level[i][el.system.name].append(
                    [el.vendor.name, el.model, el.caption, 1, el.price, el.price])

        # оборудование с отметкой базовое, без параметров с count=0 и ценой ниже 1 но не равной 0
        for el in f:
            if el.system.name in dict_level[i]:
                cost = dict_cost[i][el.system.name] * el.price
                dict_level[i][el.system.name].append([el.vendor.name, el.model, el.caption, '', '', cost])
                dict_cost[i][el.system.name] = dict_cost[i][el.system.name] + cost

        for el in g:  # рудование с отметкой базовое, без параметров, count = 0 и не определенной ценой (т.е. цена неизвестна)
            if el.system.name in dict_level[i]:
                dict_level[i][el.system.name].append([el.vendor.name, el.model, el.caption, '', '', ''])

    # for key in dict_cost.keys(): # добавляем информацию с итоговыми подсчетами в словарь оборудования
    #     for i in dict_cost[key]:
    #         dict_level[key][i].append(['','','','','Итого',dict_cost[key][i]])

    return dict_level, dict_cost


def index(request):
    if request.method == 'POST':
        sys = request.POST.getlist('system')  # получаем список подсистем
        lev = request.POST.getlist('level')  # получаем список уровней
        uname = request.POST['uname']  # получаем название объекта (используется для именования файла)
        floor = request.POST.getlist('floor')  # получаем список локаций (этажей)
        rooms = []
        for item in request.POST:  # получаем список выбраных помещений
            if item not in ['uname', 'level', 'system', 'floor', 'csrfmiddlewaretoken']:
                a = request.POST[item].replace(' ', '')
                rooms.append(a.split(','))  # добавляем в список помещения
        house = dict(zip(floor, rooms))  # из 2 списков (локации, помещения) формируем словарь

        all_room = []  # собираем все комнаты в один список
        for list_room in rooms:
            all_room.extend(list_room)

        count_room = Counter(all_room)  # считаем кол-во повторений комнат
        # print(count_room)
        # для работы: count_room: словарь всех комнат посчитанный
        # house - словарь где ключ - этаж, значение - список комнат
        all_param, choice_temp = system_count(sys, all_room,
                                              count_room)  # получаем количественные показатели всех выбранных подсистем

        all_calc, all_cost = find_light(lev, all_param, sys)

        file = xlsxcreate(uname, all_calc, all_cost, sys, lev, house, choice_temp, all_param)

        return render(request, 'download.html', {'file': file})

    rooms = Rooms.objects.all()
    levels = Levels.objects.all().order_by('id')
    systems = Systems.objects.filter(is_visible=True).order_by('id')  # Выбираем все поля с пометкой "Видимые"
    floors = Floor.objects.all()

    return render(request, 'index.html', {'floors': floors, 'rooms': rooms, 'levels': levels, 'systems': systems})
