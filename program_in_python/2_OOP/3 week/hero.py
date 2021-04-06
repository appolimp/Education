from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base
        self.main_char = ['Strength', 'Perception', 'Endurance', 'Charisma', 'Intelligence', 'Agility', 'Luck']

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass


class AbstractPositive(AbstractEffect):
    @abstractmethod
    def get_stats(self):
        pass

    def get_positive_effects(self):
        self.get_stats()
        return self.positive_effects

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect):
    @abstractmethod
    def get_stats(self):
        pass

    def get_positive_effects(self):
        return self.base.get_positive_effects()

    def get_negative_effects(self):
        self.get_stats()
        return self.negative_effects.copy()


class Berserk(AbstractPositive):
    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Strength"] += 7
        self.stats["Endurance"] += 7
        self.stats["Agility"] += 7
        self.stats["Luck"] += 7

        self.stats["Perception"] -= 3
        self.stats["Charisma"] -= 3
        self.stats["Intelligence"] -= 3

        self.stats["HP"] += 50

        self.positive_effects = self.base.get_positive_effects() + ['Berserk']

        return self.stats.copy()


class Blessing(AbstractPositive):
    def get_stats(self):
        self.stats = self.base.get_stats()

        for key in self.main_char:
            self.stats[key] += 2

        self.positive_effects = self.base.get_positive_effects() + ['Blessing']

        return self.stats.copy()


class Weakness(AbstractNegative):
    def get_stats(self):
        self.stats = self.base.get_stats()

        self.stats["Strength"] -= 4
        self.stats["Endurance"] -= 4
        self.stats["Agility"] -= 4

        self.negative_effects = self.base.get_negative_effects() + ['Weakness']

        return self.stats.copy()


class EvilEye(AbstractNegative):
    def get_stats(self):
        self.stats = self.base.get_stats()

        self.stats["Luck"] -= 10

        self.negative_effects = self.base.get_negative_effects() + ['EvilEye']

        return self.stats.copy()


class Curse(AbstractNegative):
    def get_stats(self):
        self.stats = self.base.get_stats()

        for key in self.main_char:
            self.stats[key] -= 2
        self.negative_effects = self.base.get_negative_effects() + ['Curse']

        return self.stats.copy()


if __name__ == '__main__':
    hero = Hero()
    print(hero.get_stats(), hero.get_positive_effects())

    brs1 = Berserk(hero)
    print(brs1.get_stats(), brs1.get_positive_effects())

    brs2 = Berserk(brs1)
    print(brs2.get_stats(), brs2.get_positive_effects())

    brs2.base = hero
    print(brs2.get_stats(), brs2.get_positive_effects())

    ber1 = Berserk(hero); print(ber1.get_positive_effects(), ber1.get_negative_effects())
    cur1 = Curse(ber1); print(cur1.get_positive_effects(), cur1.get_negative_effects())
    cur2 = Curse(cur1); print(cur2.get_positive_effects(), cur2.get_negative_effects())
    cur3 = Curse(cur2); print(cur3.get_positive_effects(), cur3.get_negative_effects())

    out = Curse(Weakness(EvilEye(Curse(Blessing(Berserk(Hero()))))))
    print(out.get_positive_effects(), out.get_negative_effects())