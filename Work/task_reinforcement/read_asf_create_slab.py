import re
import ezdxf
import numpy as np

# file_asf = r".\slab_v.asf"
file_asf = r".\\st4_task_fp_r01.asf"

list_of_vertex = []
with open(file_asf, "r") as f:
    for line in f:
        if 'GL' in line:
            number_vertex_of_polyline = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            vertex = [next(f).strip() for x in range(
                int(number_vertex_of_polyline[0])) if len(next(f)) > 0]
            list_of_vertex.append(vertex)

'''
def list_coordinates(list_of_vertex):
    try:
        lst_coord = []
        for v in list_of_vertex:
            num = re.findall(r"[-+]?\d*\.\d+|\d+", v)
            coordinates = np.array(num[:2], dtype='float')*1000
            lst_coord.append(coordinates)
        # return lst_coord
    except:
        lst_coord = []
        for i in range(4):
            for v in list_of_vertex[i]:
                num = re.findall(r"[-+]?\d*\.\d+|\d+", v)
                coordinates = np.array(num[:2], dtype='float')*1000
                lst_coord.append(coordinates)
    return lst_coord
'''


def list_coordinates(list_of_vertex):
    count = len(list_of_vertex)
    if count == 1:
        lst_coord = []
        for v in list_of_vertex[0]:
            num = re.findall(r"[-+]?\d*\.\d+|\d+", v)
            coordinates = np.array(num[:2], dtype='float')*1000
            lst_coord.append(coordinates)
        return count, lst_coord
    else:
        lst_coord = []
        for i in range(count):
            lst_coord1 = []
            for v in list_of_vertex[i]:
                num = re.findall(r"[-+]?\d*\.\d+|\d+", v)
                coordinates = np.array(num[:2], dtype='float')*1000
                lst_coord1.append(coordinates)
            lst_coord.append(lst_coord1)
    return count, lst_coord


# lst = list_coordinates(list_of_vertex)
'''
lst_coord = []
for v in list_of_vertex[0]:
    num = re.findall(r"[-+]?\d*\.\d+|\d+", v)
    print(num)
    # coordinates = num[:2]
    # lst_coord.append(coordinates)
# print(lst_coord)
'''
'''
# print(lst_reinf_additional_bottom_Y)
# Create a new DXF document.
doc = ezdxf.new(dxfversion='R2010', setup=True)

# Create new table entries (layers, linetypes, text styles, ...).
doc.layers.new('_Верхняя X', dxfattribs={'color': 2})
doc.layers.new('_Нижняя X', dxfattribs={'color': 3})
doc.layers.new('_Верхняя Y', dxfattribs={'color': 30})
doc.layers.new('_Нижняя Y', dxfattribs={'color': 4})
# DXF entities (LINE, TEXT, ...) reside in a layout (modelspace,
# paperspace layout or block definition).
msp = doc.modelspace()

# Add entities to a layout by factory methods: layout.add_...()
# msp.add_line((0, 0), (10, 0), dxfattribs={'color': 7})
# doc.styles.new('myStandard', dxfattribs={'font': 'ISOCPEUR.ttf'})


def create_text_add_reb(lst, layer_name):
    for i in lst:
        create = msp.add_text(
            i[2],
            dxfattribs={
                'layer': layer_name,
                'height': 50,
                'style': 'OpenSans-Italic',
            }).set_pos((i[0], i[1]), align='CENTER')
    return create


create_text_add_reb(lst_reinf_additional_bottom_Y, '_Нижняя Y')
create_text_add_reb(lst_reinf_additional_bottom_X, '_Нижняя X')
create_text_add_reb(lst_reinf_additional_top_X, '_Верхняя X')
create_text_add_reb(lst_reinf_additional_top_Y, '_Верхняя Y')

# doc.layers.remove('0')
# doc.layers.remove('Defpoints')
# print(lst_reinf_additional_bottom_Y)
# Save DXF document.
doc.saveas('test.dxf')
print(lst_reinf_additional_top_X)
'''


def create_boudary_slab(lst, layer_name):
    if lst[0] == 1:
        points = lst[1]
        msp.add_lwpolyline(points, dxfattribs={
            'layer': 'boundary_slab', 'closed': True})
    else:
        for points in lst[1]:
            msp.add_lwpolyline(points, dxfattribs={
                'layer': 'boundary_slab', 'closed': True})
# points = list_coordinates(list_of_vertex)
# print(points)


# Create boundary slab
doc = ezdxf.new(dxfversion='R2010', setup=True)
doc.layers.new('boundary_slab', dxfattribs={'color': 2})
msp = doc.modelspace()
'''
# points = [(0, 0), (300.0, 0), (6, 3), (6, 6)]
points = list_coordinates(list_of_vertex)
msp.add_lwpolyline(points[0], dxfattribs={
    'layer': 'boundary_slab', 'closed': True})
'''
create_boudary_slab(list_coordinates(list_of_vertex), 'boundary_slab')
doc.saveas('test_poly.dxf')
