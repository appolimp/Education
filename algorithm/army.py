class Warrior:
    def __init__(self, health=50, attack=5):
        self.health = health
        self.attack = attack

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def hit(self, unit):
        unit.loss(self.attack * self.is_alive)

    def loss(self, attack):
        self.health -= attack


class Knight(Warrior):
    def __init__(self):
        super().__init__(attack=7)


class Defender(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=3)
        self.defense = 2

    def loss(self, attack):
        self.health -= max(0, attack - self.defense)


class Vampire(Warrior):
    def __init__(self):
        super().__init__(health=40, attack=4)
        self.vampirism = 50

    def hit(self, unit):
        start = unit.health * unit.is_alive
        unit.loss(self.attack * self.is_alive)
        self.health += (start - unit.health * unit.is_alive)*self.vampirism//100


class Lancer(Warrior):
    def hit(self, unit):
        start = unit.health * unit.is_alive
        unit.loss(self.attack * self.is_alive)
        self.health += (start - unit.health * unit.is_alive) * 50 // 100


def fight(unit_1, unit_2):
    print(type(unit_1), type(unit_1) == list)
    if type(unit_1) == list:
        unit_1, unit_12 = unit_1
    if type(unit_2) == list:
        unit_2, unit_22 = unit_2
        print(unit_2, unit_12, unit_2, unit_22)
    while unit_1.is_alive and unit_2.is_alive:
        unit_1.hit(unit_2)
        unit_2.hit(unit_1)
    return unit_1.is_alive

class Army(list):
    def add_units(self, unit, count):
        for _ in range(count):
            self.append(unit())

    @property
    def is_alive(self) -> bool:
        return self != []


class Battle:
    def fight(self, arm_1, arm_2) -> bool:
        while arm_1.is_alive and arm_2.is_alive:
            if fight(arm_1[0:2], arm_2[0:2]):
                del arm_2[0]
            else:
                del arm_1[0]

        return arm_1.is_alive



if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    # fight tests
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()
    bob = Defender()
    mike = Knight()
    rog = Warrior()
    lancelot = Defender()
    eric = Vampire()
    adam = Vampire()
    richard = Defender()
    ogre = Warrior()
    freelancer = Lancer()
    vampire = Vampire()

    assert fight(chuck, bruce) == True
    assert fight(dave, carl) == False
    assert chuck.is_alive == True
    assert bruce.is_alive == False
    assert carl.is_alive == True
    assert dave.is_alive == False
    assert fight(carl, mark) == False
    assert carl.is_alive == False
    assert fight(bob, mike) == False
    assert fight(lancelot, rog) == True
    assert fight(eric, richard) == False
    assert fight(ogre, adam) == True
    assert fight(freelancer, vampire) == True
    assert freelancer.is_alive == True

    # battle tests
    my_army = Army()
    my_army.add_units(Defender, 2)
    my_army.add_units(Vampire, 2)
    my_army.add_units(Lancer, 4)
    my_army.add_units(Warrior, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)
    enemy_army.add_units(Lancer, 2)
    enemy_army.add_units(Defender, 2)
    enemy_army.add_units(Vampire, 3)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Lancer, 1)
    army_3.add_units(Defender, 2)

    army_4 = Army()
    army_4.add_units(Vampire, 3)
    army_4.add_units(Warrior, 1)
    army_4.add_units(Lancer, 2)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == True
    assert battle.fight(army_3, army_4) == False
    print("Coding complete? Let's try tests!")
