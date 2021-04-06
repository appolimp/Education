import win32com.client
from pythoncom import VT_R8, VT_ARRAY, VT_DISPATCH

app = win32com.client.Dispatch("AutoCAD.Application")
app.visible = True  # Сделать видимым акад, т.к запускает невидимым окно
aDoc = app.ActiveDocument
msp = aDoc.ModelSpace

# немного модифицировал функцию ptA(), теперь она преобразует в variant array of doubles
# все аргументы, в т.ч. и представленные в виде списка или кортежа


def convert_coordinates(*args):
    """
    Функция преобразования координат в формат AutoCAD
    :param args: координаты для преобразования, допустима передача списка или кортежа
    :return: Координаты в формате AutoCAD
    """
    if isinstance(args[0], (list, tuple)):
        coords = [item for item in args[0]]
    else:
        coords = args
    return win32com.client.VARIANT(VT_ARRAY | VT_R8, coords)


def vtpt(x, y, z=0):
    return win32com.client.VARIANT(VT_ARRAY | VT_R8, (x, y, z))


def vtobj(obj):
    return win32com.client.VARIANT(VT_ARRAY | VT_DISPATCH, obj)


def VtVertex(*args):
    """
    Converts 2D coordinates of a serial points into the required float array
    """
    return win32com.client.VARIANT(VT_ARRAY | VT_R8, args)


pt1 = vtpt(0, 0)
pt2 = vtpt(0, 100)
coor = 210.0, 0.0, 0
coord_plyne = [[0, 0, 0], [0, 100, 0], [100, 200, 0], [300, 400, 0]]
lst = [convert_coordinates(i) for i in coord_plyne]
# print(lst)
pt = convert_coordinates(coor)
# msp.AddCircle(pt, 200)
# msp.AddPolyline(1, 1, 0)
# msp.Addline(pt1, pt2)


def AddLwpline(*vertexCoord):
    """
    LightWeight Poly line, this method requires the group of 2D vertex coordinates(that is x,y),
    This method is recommended to draw line
    """
    lwpline = msp.AddLightWeightPolyline(VtVertex(*vertexCoord))
    return lwpline


ar = 0, 0, 100, 100, 500, 300, 700, 900
pline = AddLwpline(*ar)
pline.Closed = True
