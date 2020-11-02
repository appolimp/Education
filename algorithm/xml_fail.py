from xml.etree import ElementTree

tree = ElementTree.parse('student.xml')
root = tree.getroot()
child = root.find('studenq')
child.text = 'Moana'
child.set('id', '2')
desc = ElementTree.Element('desc')
desc.text = 'Amazing'
root.append(desc)
tree.write('student.xml')



tree = ElementTree.parse('example.xml')
print(type(tree))
root = tree.getroot()
print(root, root.tag, root.attrib, type(root))
student1 = next(root.iter('student'))
print(333, student1, student1.attrib, student1.text)

for child in root:
    print(child.tag, child.attrib)

# print(root[0][0].text)
for element in root.iter('scores'):
    score_sum = 0
    for child in element:
        # print(child.tag, child.text)
        score_sum += float(child.text)
    print(score_sum)

# tree.write('example_xml.xml')

greg = root[0]
module1 = next(greg.iter('module1'))
print(module1, module1.text)
module1.text = str(int(module1.text)+30)




certificate = greg[2]
certificate.set("type", 'with distinction')  # добавить аттрибут

description = ElementTree.Element('description')
description.text = 'Show amazing skills during course'
greg.append(description)

description = greg.find('description')
greg.remove(description)

tree.write('example_xml.xml')

root = ElementTree.Element('student')
first_name = ElementTree.SubElement(root, 'firstName')
first_name.text = 'Greg'
second_name = ElementTree.SubElement(root, 'secondName')
second_name.text = 'Dean'
scores = ElementTree.SubElement(root, 'scores')

module1 = ElementTree.SubElement(scores, 'module1')
module1.text = '70'
module2 = ElementTree.SubElement(scores, 'module2')
module2.text = '60'
module3 = ElementTree.SubElement(scores, 'module3')
module3.text = '90'

tree = ElementTree.ElementTree(root)
tree.write('st.xml')

