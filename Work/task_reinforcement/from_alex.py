# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 11:14:23 2020

@author: alsmirnov
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename_import = r".\st3_r02.asf"

with open(filename_import, "r") as file:
    text = file.readlines()
    text_array = list()
    list1_temp = list()
    list2_temp = list()
    for i in range(len(text)):
        # убираем последний символ из строки
        text[i] = text[i].replace(text[i][-1], '')
        text_array.append(text[i].split(" "))
        for j in range(len(text_array[i])):
            if text_array[i][j] != '':
                list1_temp.append(text_array[i][j])
        if len(list1_temp) != 0:
            list2_temp.append(list1_temp)
        list1_temp = list()

km = 0
for i in range(len(list2_temp)):
    for j in range(len(list2_temp[i])):
        if list2_temp[i][j] == 'ELEM':
            km = i
            break

# список элементов с номерами по возрастанию - начальный полный список
list1 = list()

# массив узлов элементов
list2 = np.zeros((int(list2_temp[km][2]), 4))

# преобразуем массив numpy в list
for i in range(int(list2_temp[km][2])):
    list1.append(int(list2_temp[i+km+1][0]))
    list2[i] = np.array(list2_temp[i+km+1][1:])

list2 = np.array(list2, dtype=int)
list1_temp = list()

for i in range(int(list2_temp[km][2])):
    list3_temp = list()
    for j in range(np.size(list2[i])):
        list3_temp.append(list2[i][j])
    list1_temp.append(list3_temp)

list2 = list1_temp

# координаты узлов
point_x = list()
point_y = list()

# список значений армирования в узлах
list3 = list()

for i in range(len(list2_temp)):
    if list2_temp[i][0] == 'QB':
        list3.append(float(list2_temp[i][4]))  # для одного напрадения арматуры
        point_x.append(float(list2_temp[i][1]))
        point_y.append(float(list2_temp[i][2]))

# преобразовываем в массив numpy для упрощения работы
list3 = np.array(list3)

# вычитаем основное армирование
list3 = list3 - 10
list3 = np.where(list3 > 0, list3, 0)

list1_temp = list()
list3_temp = list()

"""
Так как в asf файле в списке элементов и их узлов число символов в строке не меняется
в случае с треугольным элементом в списке узлов появляется "0"
поэтому требуется вносить дополнительные условия для обработки

"""

for i in range(len(list1)):
    k = 0
    for j in range(len(list2[i])):
        if list2[i][j] == 0:  # дополнительное условие для треугольных элементов
            continue
        else:
            if list3[list2[i][j]-1] != 0:
                k = 0
                break
            else:
                k = k + 1
    if k == 0:
        list1_temp.append(list1[i])
        list3_temp.append(list2[i])

list1 = list1_temp
list2 = list3_temp


# список элементов входящих в одну группу дополнительного армирования (предварительная группа)
list4_el = list()

# массив узлов элементов в list4_el
list4_point = list()

# список оставшихся элементов среди которых идет поиск смежных, после переноса части элементов в list4_el
list5_el = list()

# список узлов элементов в list5_el
list5_point = list()

# массив групп элементов дополнительного армирования
group_add_reinf_el = list()

# массив номеров элементов по группам дополнительного армирования
group_add_reinf_point = list()

# счетчик для первого цикла while
count = 0

# общее количество элементов
general_count = len(list1)

while count < general_count:
    # исключаем первый элемент из списка с которого начинаем всю процедуру
    if len(list1) != 1:
        x = list1[0]
        y = list2[0]
        list4_el.append(x)
        list4_point.append(y)
        list1.remove(list1[0])
        list2.remove(list2[0])
    else:
        x = list1[0]
        y = list2[0]

    # количество элементов в list1 за исключением первого
    element_count = len(list1)

    i = 0
    # цикл для формирования групп дополнительного армирования
    while count < general_count:
        if len(list5_el) != 0:
            x = list4_el[i]
            y = list4_point[i]
            i = i + 1

        for item in list1:
            t = len(list4_el)
            p = len(list1)
            for j in range(len(y)):
                if t == len(list4_el):
                    temp = 0
                    for k in range(len(list2[list1.index(item)])):
                        # y[j]!=0 дополнительное условие для треугольных элементов
                        if y[j] != 0 and y[j] == list2[list1.index(item)][k]:
                            list4_el.append(item)
                            list4_point.append(list2[list1.index(item)])
                            count = count + 1
                            temp = temp + 1
                        else:
                            continue
                    if temp != 0 and i != 0:
                        list5_point.remove(list5_point[list5_el.index(item)])
                        list5_el.remove(item)

                else:
                    continue
            if t != len(list4_el):
                continue
            else:
                if i == 0:
                    list5_el.append(item)
                    list5_point.append(list2[list1.index(item)])

        list1 = list5_el
        list2 = list5_point
        if len(list1) == 0:
            group_add_reinf_el.append(list4_el)
            group_add_reinf_point.append(list4_point)
            break

        if (len(list4_el) == 0 or x == list4_el[len(list4_el)-1]) and item == list5_el[len(list5_el)-1] and temp == 0:
            group_add_reinf_el.append(list4_el)
            group_add_reinf_point.append(list4_point)
            list4_el = list()
            list4_point = list()
            list5_el = list()
            list5_point = list()
            break
    if len(list1) == 1:
        group_add_reinf_el.append(list1)
        group_add_reinf_point.append(list2)
        break
    elif len(list1) == 0:
        break
    else:
        continue


"""
 Определение последовательности узлов элементов
 
 """


point = [0, 5, 6, 1]
point_x_arr = [0, 1, 1, 0]
point_y_arr = [0, -1, 1, 0]


# Функция выстраивает узлы элемента по часовой стрелке и формирует массив с номерами узлов каждой грани
def edge_sort(point, point_x_arr, point_y_arr):
    """
    point - список узлов элементов. пример - [0, 5, 6, 1]
    point_x_arr - список координат Х узлов элементов. пример - [0, 1, 1, 0]
    point_y_arr - список координат Y узлов элементов. пример - [0, -1, 1, 0]

    """
    # координаты точек одного элемента
    point_coordinat = np.array([point, point_x_arr, point_y_arr])

    zero_index = -10
    # дополнительная обработка для треугольных элементов
    for i in range(4):
        if point_coordinat[0][i] == 0:
            zero_index = i

    # создаем словарь для перевода его в DataFrame

    data = {'point_number': point_coordinat[0],
            'x': point_coordinat[1], 'y': point_coordinat[2]}

    # дополнительная обработка для треугольных элементов
    if zero_index != -10:
        frame = pd.DataFrame(data)
        frame = frame.drop([zero_index])
    else:
        frame = pd.DataFrame(data)

    # сортируем DataFrame по X

    data = frame.sort_values(by=['x', 'y']).reset_index()

    # записываем координаты из DataFrame в массивы для вычисления угла между вертикалью и
    # отрезком, который соединяет первый узел и рассматриваемый
    x = np.array(data['x'])
    y = np.array(data['y'])
    point_number = np.array(data['point_number'])

    # вычисляем координаты первого узла из координат всех узлов
    x_new = x - x[0]
    y_new = y - y[0]

    alfa = np.zeros(x_new.size)

    for i in range(x_new.size):
        tan = x_new[i] / y_new[i]
        if tan >= 0:
            alfa[i] = np.arctan(tan)*180/np.pi
        else:
            alfa[i] = 180 + np.arctan(tan)*180/np.pi

    data = {'point_number': point_number, 'x': x_new, 'y': y_new, 'alfa': alfa}

    # заменяем NaN на '0'
    frame = pd.DataFrame(data).fillna(0)

    # сортируем по углу
    frame = frame.sort_values('alfa').reset_index()

    # записываем порядок узлов по часовой стрелке
    point_order = np.array(frame['point_number'])

    # создаем пустой массив для номеров узлов граней элемента
    edge_point_number = np.zeros((x_new.size, 2))

    # заполняем массив
    for i in range(x_new.size):
        if i == x_new.size - 1:
            edge_point_number[i][0] = point_order[i]
            edge_point_number[i][1] = point_order[i-i]
        else:
            edge_point_number[i][0] = point_order[i]
            edge_point_number[i][1] = point_order[i+1]

    return (edge_point_number)

# Цикл для формирования массива граней элементов по часовой стрелке


# массив с номерами узлов граней элементов одной группы доп. арм.
edge_point_number = list()

for i in range(len(group_add_reinf_el[0])):
    point = list()
    point_x_arr = list()
    point_y_arr = list()

    point = group_add_reinf_point[0][i]

    for j in range(4):
        # условие для треугольних элементов
        if group_add_reinf_point[0][i][j] != 0:
            point_x_arr.append(point_x[group_add_reinf_point[0][i][j]-1])
            point_y_arr.append(point_y[group_add_reinf_point[0][i][j]-1])
        else:
            point_x_arr.append(0)
            point_y_arr.append(0)

    edge_point_number.append(
        np.array(edge_sort(point, point_x_arr, point_y_arr), dtype=int))

# массив граней внешнего полигона одной группы доп армирования
polygon_edge_point = list()

# выбираем грани, формирующие внещний полигон
for i in range(len(edge_point_number)):
    for j in range(len(edge_point_number[i])):
        t = 0
        for k in range(len(edge_point_number)):
            if t == 0:
                for m in range(len(edge_point_number[k])):
                    if i != k:
                        #                        print(edge_point_number[i][j][0], edge_point_number[i][j][1],edge_point_number[k][m][0],edge_point_number[k][m][1])
                        if (edge_point_number[i][j][0] == edge_point_number[k][m][0] and edge_point_number[i][j][1] == edge_point_number[k][m][1])\
                                or (edge_point_number[i][j][1] == edge_point_number[k][m][0] and edge_point_number[i][j][0] == edge_point_number[k][m][1]):
                            t = t + 1
                            break
                        else:
                            continue
            else:
                break
        if t == 0:
            polygon_edge_point.append(edge_point_number[i][j])

# выстраиваем грани в нужном порядке следования друг за другом

polygon_edge = list()

polygon_edge.append(polygon_edge_point[0])

for i in range(len(polygon_edge_point)-1):
    for j in range(len(polygon_edge_point)):
        #        print(polygon_edge[i][1], polygon_edge_point[j][0])
        if polygon_edge[i][1] == polygon_edge_point[j][0]:
            polygon_edge.append(polygon_edge_point[j])


polygon_x = list()
polygon_y = list()

for i in range(len(polygon_edge)):
    for j in range(2):
        polygon_x.append(point_x[polygon_edge[i][j]-1])
        polygon_y.append(point_y[polygon_edge[i][j]-1])

plt.plot(polygon_x, polygon_y)
plt.show()
