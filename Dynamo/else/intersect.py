
type_Surf = 'Autodesk.DesignScript.Geometry.Surface'
type_PolySurf = 'Autodesk.DesignScript.Geometry.PolySurface'


def find_iter(surf1, surf2):
    """
        Находит пересечение двух плоскостей
        И возвращает эту плоскость
    """


    # if inter and DSCore.Object.Type(inter[0]) == type_PolySurf:
    # return inter[0]

    return surf2 - surf1


def dublicate(surf1, surf2):
    """
        Проверяет дублирование
    """

    return surf1 == surf2


def explode(all_surf, number_iter=10):
    i = n = 0
    exp_surf = []
    exp_surf.append(all_surf.pop(0))

    while all_surf and n <= number_iter:
        new_surf = all_surf.pop(0)
        add_surf = []

        for i, old_surf in enumerate(exp_surf):

            if dublicate(new_surf, old_surf):
                break

            inter = find_iter(new_surf, old_surf)
            if not inter: continue

            if dublicate(new_surf, inter):
                exp_surf[i] = Surface.Difference(old_surf, [inter])
                add_surf.append(inter)
                new_surf = []
                break

            if dublicate(old_surf, inter):
                new_surf = Surface.Difference(new_surf, [inter])
                continue

            exp_surf[i] = Surface.Difference(old_surf, [inter])
            new_surf = Surface.Difference(new_surf, [inter])
            add_surf.append(inter)

        if new_surf: exp_surf.append(new_surf)
        if add_surf: exp_surf.append(add_surf)
        n += 1

    global messenge_status
    messenge_status = 'ok' if n < number_iter else 'no ok(('

    return exp_surf, n


def main():
    all_surf = [1, 2, 3, 4, 5, 6]
    number_iter = 10

    global messenge_status
    messenge_status = []

    explode_surf = explode(all_surf, number_iter)

    return explode_surf, messenge_status


OUT = main()

# Ошибки:
#	- удаление дублирующих элементов (не проработан)
# 	- случай, когда одна плоскость полностью находится во второй
#	- ошибка в расчете общей площади при объединении входных плоскостей, если все не пересекаются
