import re
from abc import ABC, abstractmethod


class System:
    def __init__(self, text):
        tmp = re.sub(r"\W", ' ', text.lower())
        tmp = re.sub(r' +', ' ', tmp).strip()
        self.text = tmp

    def get_processed_text(self, processor):
        result = processor.process_text(self.text)
        print(*result, sep='\n')


class TextProcessor(ABC):
    @abstractmethod
    def process_text(self, text):
        pass


class WordCounter:
    def count_words(self, text):
        self.__words = dict()
        for word in text.split():
            self.__words[word] = self.__words.get(word, 0) + 1

    def get_count(self, word):
        return self.__words.get(word, 0)

    def get_all_words(self):
        return self.__words.copy()


class WordCounterAdapter(TextProcessor):
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def process_text(self, text):
        self.adaptee.count_words(text)

        return sorted(self.adaptee.get_all_words(),
                      key=lambda x: self.adaptee.get_count(x),
                      reverse=True)


if __name__ == '__main__':
    with open('text.txt') as f:
        text = f.read()

    system = System(text)

    counter = WordCounter()
    counter = WordCounterAdapter(counter)
    system.get_processed_text(counter)

