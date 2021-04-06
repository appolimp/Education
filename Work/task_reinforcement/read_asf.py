import re
import ezdxf

file_asf = r".\slab_v.asf"
# file_asf = r".\\st4_task_fp_r01.asf"
# 2.51
top_reinforcement = 2.0
bottom_reinforcement = 2.0


def add_pnts(X, Y, top):
    pass


lst_reinf_additional_top_X = []
lst_reinf_additional_top_Y = []
lst_reinf_additional_bottom_X = []
lst_reinf_additional_bottom_Y = []


with open(file_asf, "r") as f:
    for line in f:
        if 'QB' in line:
            # print(line.index(line))
            # first_row = f.__next__()
            number = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            X_coordinates = float(number[0]) * 1000.0
            Y_coordinates = float(number[1]) * 1000.0
            reinf_additional_top_X = round(
                float(number[3])-top_reinforcement, 2)
            reinf_additional_top_Y = round(
                float(number[4])-top_reinforcement, 2)
            reinf_additional_bottom_X = round(
                float(number[6])-top_reinforcement, 2)
            reinf_additional_bottom_Y = round(
                float(number[7])-top_reinforcement, 2)
            if reinf_additional_top_X > 0:
                lst_reinf_additional_top_X.append(
                    [X_coordinates, Y_coordinates, reinf_additional_top_X])
            if reinf_additional_top_Y > 0:
                lst_reinf_additional_top_Y.append(
                    [X_coordinates, Y_coordinates, reinf_additional_top_Y])
            if reinf_additional_bottom_X > 0:
                lst_reinf_additional_bottom_X.append(
                    [X_coordinates, Y_coordinates, reinf_additional_bottom_X])
            if reinf_additional_bottom_Y > 0:
                lst_reinf_additional_bottom_Y.append(
                    [X_coordinates, Y_coordinates, reinf_additional_bottom_Y])


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
#msp.add_line((0, 0), (10, 0), dxfattribs={'color': 7})
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
