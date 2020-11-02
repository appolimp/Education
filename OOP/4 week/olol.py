import yaml  # для работы с PyYAML

yml_MD = '''
--- !MDreport                # указывает, что хранящаяся ниже структура относиться к типу MDreport   
objects:                     # для хранения якорей
  - &img !img                # якорь img хранит объект типа img
      alt_text: coursera     # описание изображения
      src: "https://blog.coursera.org/wp-content/uploads/2017/07/coursera-fb.png"   # адрес изображения
report: !report              # содержит непосредственно отчёт
  filename: report_yaml.md   # имя файла отчёта
  title: !!str Report        # название отчёта - строковый параметр (!!str) "Report"
  parts:                     # содержание отчёта - список частей (каждая часть начинаеться с "-")
    - !chapter                   # первая часть отчёта - объект типа "chapter"
      caption: "chapter one"         # заглавие первой части
      parts:                         # содержание первой части - список ниже

 # первая часть - текст.
 # символ '>' вконце показывает, что весь блок ниже являеться содержанием. Перенос строк не учитываеться
 # Для учёта переноса строк - символ '|'

        - |                            
          chapter
          1
          text               
        - !link                          # далее ссылка
            obj: coursera                    # текст ссылки
            href: "https://ru.coursera.org"  # куда ссылаеться
    - !chapter                   # вторая часть отчёта - объект типа "chapter"
      caption: "chapter two"         # заглавие второй части
      parts:                         # содержание второй части - список ниже
        - "Chapter 2 header"             # сначала текст
        - !link                          # далее ссылка
            obj: *img                        # объект, хранящийся по якорю img (изображение) будет являться ссылкой
            href: "https://ru.coursera.org"  # куда ссылаеться
        - "Chapter 2 footer"             # в конце - текст'''


# теперь ReportFactory - потомок yaml.YAMLObject.
# Сделано для того, чтобы yaml оработчик знал новый тип данных, указанный в yaml_tag
# он будет определён в фабриках - потомках
class ReportFactory(yaml.YAMLObject):

    # данные yaml фала - структура отчёта одинакова для всех потомков.
    # В связи с этим - получение отчёта из yaml файла - классовый метод со специальным именем from_yaml
    @classmethod
    def from_yaml(cls, loader, node):
        # сначала опишем функции для обработки каждого нового типа
        # метод loader.construct_mapping() формирует из содержания node словарь

        # обработчик создания отчёта !report
        def get_report(loader, node):
            data = loader.construct_mapping(node)
            rep = cls.make_report(data["title"])
            rep.filename = data["filename"]
            # на данный момент data["parts"] пуст. Он будет заполнен позже, соответствующим обработчиком,
            # сохраняем на него ссылку, дополнив сразу частями из rep.parts
            data["parts"].extend(rep.parts)
            rep.parts = data["parts"]
            return rep

        # обработчик создания части !chapter
        def get_chapter(loader, node):
            data = loader.construct_mapping(node)
            ch = cls.make_chapter(data["caption"])
            # аналогично предыдущему обработчику
            data["parts"].extend(ch.objects)
            ch.objects = data["parts"]
            return ch

        # обработчик создания ссылки !link
        def get_link(loader, node):
            data = loader.construct_mapping(node)
            lnk = cls.make_link(data["obj"], data["href"])
            return lnk

        # обработчик создания изображения !img
        def get_img(loader, node):
            data = loader.construct_mapping(node)
            img = cls.make_img(data["alt_text"], data["src"])
            return img

        # добавляем обработчики
        loader.add_constructor(u"!report", get_report)
        loader.add_constructor(u"!chapter", get_chapter)
        loader.add_constructor(u"!link", get_link)
        loader.add_constructor(u"!img", get_img)

        # возвращаем результат yaml обработчика - отчёт
        return loader.construct_mapping(node)['report']

    # ниже - без изменений

    @classmethod
    def make_report(cls, title):
        return cls.Report(title)

    @classmethod
    def make_chapter(cls, caption):
        return cls.Chapter(caption)

    @classmethod
    def make_link(cls, obj, href):
        return cls.Link(obj, href)

    @classmethod
    def make_img(cls, alt_text, src):
        return cls.Img(alt_text, src)


class MDreportFactory(ReportFactory):
    yaml_tag = u'!MDreport'  # указываем соответствие

    class Report:
        def __init__(self, title):
            self.parts = []
            self.parts.append(f"# {title}\n\n")

        """
        def add(self, part):
            self.parts.append(part)
        """

        def save(self):  # вносим изменения - имя файла отчёта указываеться в yaml файле
            try:
                file = open(self.filename, "w", encoding="utf-8")
                print('\n'.join(map(str, self.parts)), file=file)
            finally:
                if isinstance(self.filename, str) and file is not None:
                    file.close()

    class Chapter:
        def __init__(self, caption):
            self.caption = caption
            self.objects = []

        """
        def add(self, obj):
            print(obj)
            self.objects.append(obj)
        """

        def __str__(self):
            return f'## {self.caption}\n\n' + ''.join(map(str, self.objects))

    class Link:
        def __init__(self, obj, href):
            self.obj = obj
            self.href = href

        def __str__(self):
            return f'[{self.obj}]({self.href})'

    class Img:
        def __init__(self, alt_text, src):
            self.alt_text = alt_text
            self.src = src

        def __str__(self):
            return f'![{self.alt_text}]({self.src})'


txtreport = yaml.load(yml_MD, Loader=yaml.FullLoader)  # загружаем yaml файл markdown отчёта
txtreport.save()  # сохраняем
print(txtreport)
print("Сохранено:", txtreport)  # вывод
