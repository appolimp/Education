class Character:
    def __init__(self):
        self.name = "Cool_Boy"
        self.xp = 0
        self.passed_quests = set()
        self.taken_quests = set()


QUEST_SPEAK, QUEST_HUNT, QUEST_CARRY = 'QSPEAK', 'QHUNT', 'QCARRY'


class Event:
    def __init__(self, kind):
        self.kind = kind


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, char, event):
        if self.__successor is not None:
            self.__successor.handle(char, event)



