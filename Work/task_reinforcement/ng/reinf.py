import logging
import scipy.spatial
import scipy.interpolate

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PATH = r'st3_r02.asf'
NAME_COLUMNS = ['x', 'y', 'z', 'top_x', 'top_y', 'top_z', 'bot_x', 'bot_y', 'bot_z']
DROP_COLUMNS = ['z', 'top_z', 'bot_z']


def read_asf(path: str) -> list:
    """Чтение файла, поиск графы арматура и преобразование в список чисел"""

    data = []
    with open(path) as f:
        for line in f:
            if line.startswith('QB'):
                numbers = [float(i) for i in line.split()[1:]]
                data.append(numbers[:-1])

    logging.info(f'Read .asf complete. Count = {len(data)} row')
    return data


def get_data_from_asf(path: str) -> pd.DataFrame:
    asf_data = read_asf(path)
    df = pd.DataFrame(asf_data, columns=NAME_COLUMNS)
    df = df.drop(columns=DROP_COLUMNS)

    logging.info('DataFrame was created')
    return df


def remove_background_reinforcement(data: pd.DataFrame, top_x=10, top_y=10, bot_x=10, bot_y=10) -> pd.DataFrame:
    def remove_or_zero(column, val):
        data[[column]] = data[[column]] - val
        data[data[[column]] < 0] = 0

    remove_or_zero('top_x', top_x)
    remove_or_zero('top_y', top_y)
    remove_or_zero('bot_x', bot_x)
    remove_or_zero('bot_y', bot_y)

    logging.info(f'Background reinforcement {[top_x, top_y, bot_x, bot_y]} was removed: ')
    return data


def find_nearest_point(coord: pd.DataFrame, radius=0.5 * 2 ** 0.5 + 0.2) -> np.ndarray:
    """
    Находит ближайшие точки, используя k-d деревья.

    Минусы:

    - Содержит в результате свой номер

    :param coord: Координаты точек: X, Y
    :param radius: Максимальное расстояние до соседней точки
    :return: Массив с индексами соседних точек и своим индексом
    """

    tree = scipy.spatial.KDTree(coord)
    near_point = tree.query_ball_point(coord, radius)

    logging.info(f'Find nearest point with radius: {radius:.3f}')
    return near_point


def convert_to_iso_line(data: pd.DataFrame, step=2) -> pd.DataFrame:
    """
    Создает список список точек с кратным шагу значением армирования

    Пропускает пары, по которым уже проходил

    Пути оптимизации:

    - При использовании словаря из set() отрабатывает за секунду
    - Сделать красивые массивы. Сейчас на коленке. Пока не силен в numpy

    """

    iso_line_value = np.arange(0, max(data.iloc[:, 2]) + step, step=step)
    iso_line = pd.DataFrame()
    passed_pair = set()

    for i, (x, y, value, near_points) in enumerate(data.to_numpy()):
        if value:
            for near_point_i in near_points:
                key = frozenset([i, near_point_i])
                if key not in passed_pair:
                    passed_pair.add(key)

                    near_x, near_y, near_value, *_ = data.loc[near_point_i].to_numpy()

                    new_value = get_new_z(iso_line_value, value, near_value)
                    if len(new_value):
                        new_x_int = scipy.interpolate.interp1d([value, near_value], [x, near_x])
                        new_y_int = scipy.interpolate.interp1d([value, near_value], [y, near_y])

                        new_x = np.around(new_x_int(new_value), 5)
                        new_y = np.around(new_y_int(new_value), 5)
                        new_points = np.array([new_x, new_y, new_value])

                        iso_line = iso_line.append(pd.DataFrame(new_points.T))

    iso_line.columns = ['x', 'y', 'val']
    iso_line.drop_duplicates(inplace=True)

    logging.info(f'Create iso line [step={step}] with {len(iso_line)} points')
    return iso_line


def get_new_z(grid, first, second):
    start, stop = sorted([first, second])
    more_grid = grid[grid >= start]
    return more_grid[more_grid <= stop]


def print_reinforce(data: pd.DataFrame):
    """Печать общего вида арматуры"""

    fig, ax = plt.subplots(2, 2, sharex='all', sharey='all')

    for ax_i, color, name in zip([ax[0, 0], ax[0, 1], ax[1, 0], ax[1, 1]],
                                 ['top_x', 'top_y', 'bot_x', 'bot_y'],
                                 ['Top X', 'Top Y', 'Bottom X', 'Bottom Y']):
        data.plot(x='x', y='y', c=color, ax=ax_i,
                  kind='scatter', colormap='inferno', colorbar=True,
                  title=name, sharey='all')

    fig.set_facecolor('#d8dcd6')
    fig.suptitle('Общий вид армирования', fontsize=15)

    plt.show()


def print_distribution(data: pd.DataFrame):
    """Печать общего распределения арматуры"""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5, 4))

    for ax, col, name in zip([ax1, ax2],
                             ['top', 'bot'],
                             ['Top reinforce', 'Bottom reinforce']):
        sns.kdeplot(data=data, x=col + "_x", fill=True, ax=ax)
        sns.kdeplot(data=data, x=col + "_y", fill=True, ax=ax)

        ax.yaxis.set_visible(False)
        ax.set_xlabel(name)

    fig.set_facecolor('#d8dcd6')
    fig.suptitle('Распределение армирования', fontsize=15)
    plt.show()


def main():
    data = get_data_from_asf(PATH)
    data = remove_background_reinforcement(data)

    print_reinforce(data)  # Оценить положение арматуры
    # print_distribution(data)  # Оценить распределение значений площади

    # Найдем ближайшие точки
    near_point = find_nearest_point(data[['x', 'y']])
    data = data.assign(near_point=near_point)

    # Формируем поля
    top_x = convert_to_iso_line(data[['x', 'y', 'top_x', 'near_point']], step=5)
    top_x_s = top_x[top_x.iloc[:, 2] > 0]
    top_x_s.plot(x='x', y='y', c='val', s=0.5,
                 kind='scatter', colormap='inferno', colorbar=True)

    plt.show()


if __name__ == '__main__':

    logging.basicConfig(
        filename=None, level=logging.INFO,
        format='[%(asctime)s] %(levelname).1s: %(message)s',
        datefmt='%H:%M:%S')

    try:
        main()
    except Exception as err:
        logging.exception('Critical error: ' + err.args[0])
