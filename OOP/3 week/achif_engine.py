from abc import ABC, abstractmethod


class ObservableEngine:
    def __init__(self):
        self.__group = set()

    def subscribe(self, person):
        self.__group.add(person)

    def unsubscribe(self, person):
        self.__group.remove(person)

    def notify(self, message):
        title = message['title']
        text = message['text']

        for person in self.__group:
            person.update(title, text)


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, title, text):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, title, text):
        self.achievements.add(title)


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = []

    def update(self, title, text):
        if title not in self.achievements:
            self.achievements.append(title)


if __name__ == '__main__':
    pr1 = FullNotificationPrinter()
    pr2 = FullNotificationPrinter()
    pr3 = ShortNotificationPrinter()
    pr4 = ShortNotificationPrinter()

    prs = [pr1, pr2, pr3, pr4]

    eng = ObservableEngine()
    for pr in prs:
        eng.subscribe(pr)

    eng.notify({"title": "Покоритель2", "text": "Дается при выполнении всех заданий в игре"})
    eng.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})
    eng.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})
    eng.notify({"title": "Покоритель2", "text": "Дается при выполнении всех заданий в игре"})

    for pr in prs:
        print(pr.achievements)