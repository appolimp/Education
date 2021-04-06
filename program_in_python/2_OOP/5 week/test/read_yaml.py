import yaml

yaml_file = """
---
objects:
    - some_text: ...
game: 
    name: !!str 'Cool Game'
    persons:
     -mage:
      name: !!str mage
      weight: !!float 5
     warrior:
      name: !!str warrior
      weight: !!float 10
        
"""


ol = yaml.load(yaml_file, Loader=yaml.FullLoader)

print(ol)

