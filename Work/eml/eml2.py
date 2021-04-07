# -*- coding: utf-8 -*-
"""
Скрипт для преобразования .eml файлов в pdf

Итог:
    * Рядом с .eml файлом создает папку out

    * В папке out создает папку "<Дата>_<Тема>"
    * В этой папке будет .eml, .html и .pdf а так же папки attach и img (вложения и картинки)

# TODO кстати, папку img и html можно удалить

Сторонние библиотеки:
    * pdfkit - должна быть в текущей папке, если не установлена на компьютере
    * wkhtmltopdf - должна быть в текущей папке, если не установлена на компьютере
        (ссылка на установку https://wkhtmltopdf.org/downloads.html так еже устновочник есть в папке)
"""

import datetime
import email.parser
import email.policy
import glob
import logging
import os.path
import re
import shutil
import unicodedata


# ###################### Сторонние библиотеки ###############################
import pdfkit  # сторонняя библиотека. должна быть в текущей папке

# Необходимо установить программу wkhtmltopdf (в папке установочник или ссылка в описании выше)
# TODO возможно не нужно и ссылки достаточно
PATH_WKHTMLTOPDF = r'wkhtmltopdf/bin/wkhtmltopdf.exe'  # Чтобы не добавлять программу в PATH

# ###################### Input ##############################################
PATH = 'data\\'  # Папка с .eml файлами, вложенные папки скрипт не просматривает

# ###################### Constants ##########################################
PATH_OUT = 'out'

CODE_AND_REFERENCES = {
    'NRT2': ['ратуша'],
    'SevKab': ['лср', 'севкабель'],
    'PETR3': ['setl', 'петровский'],
    'NOVOALEX': ['speech', 'новоалексеевская'],
    'LEN34': ['ленинградский', 'ленинградка'],
    'KJV26': ['кожевенная'],
    'GR9': ['графский'],
    'ChR41': ['черная речка'],
    'CHAP': ['чаплыгина'],
    'BAR4': ['барочная', 'rbi'],
    'VO20': ['20-я линия'],
}


# ###################### Folder and Files ###################################
def make_file_name_valid(file_name, repl='', empty='empty_name'):
    """

    :type file_name: str
    :param repl: На какой символ заменять
    :type repl: str
    :param empty: Значение если имя пустое
    :type empty: str
    :rtype: str
    """

    name = ''.join(ch for ch in file_name if unicodedata.category(ch)[0] != 'C')  # Remove control chars
    name = re.sub(r'[/\\?%*:|<>]', repl, name)  # remove non valid chars
    name = name.strip()  # remove space in start and end

    while name.endswith('.'):
        name = name[:-1]

    name = name[:220]  # ограничение по максимальной длине. максимум 249 для папки. взял с запасом
    name = name if name else empty

    if name != file_name:
        logging.debug('Make valid name: ["{}" --> "{}"]'.format(file_name, name))

    return name


def create_name(data_str, subject, code_building, file_type=''):
    """

    :param data_str:
    :type data_str: str
    :type subject: str
    :type code_building:
    :type file_type:
    :rtype: str
    """

    date = datetime.datetime.strptime(data_str, '%a, %d %b %Y %X %z')
    name = ' '.join(str(i) for i in [date.date(), file_type, code_building, subject] if i)
    valid_name = make_file_name_valid(name)

    logging.debug('Create name for folder: "{}"'.format(valid_name))
    return valid_name


def create_folder_or_pass_if_created(folder_path):
    try:
        os.mkdir(folder_path)
        logging.debug('Create folder "{}"'.format(folder_path))
    except FileExistsError:
        pass


def get_or_create_folder_for_save(file_path, out_folder_name, folder_name):
    folder, _ = os.path.split(file_path)

    folder_out = os.path.join(folder, out_folder_name)
    create_folder_or_pass_if_created(folder_out)

    folder_for_save = os.path.join(folder_out, folder_name)
    create_folder_or_pass_if_created(folder_for_save)

    logging.debug('Get or create folder for file: [{} --> {}]'.format(file_path, folder_for_save))
    return folder_for_save


def write_part(part, folder_for_save):
    file_name = make_file_name_valid(part.get_filename())
    file_path = os.path.join(folder_for_save, file_name)

    with open(file_path, 'wb') as fb:
        fb.write(part.get_payload(decode=True))

    logging.debug('File "{}" was recorded'.format(file_name))
    return file_name


def write_html(html, html_path):
    with open(html_path, 'wb') as f:
        f.write(html)

    return html_path


def create_pdf(file_path):
    config = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF)  # чтобы не добавлять программу wkhtmltopdf в PATH
    wkhtmltopdf_options = {'enable-local-file-access': None,  # Для доступа к локальным файлам
                           'quiet': '',   # Подавление логирования
                           }

    pdf_path = os.path.splitext(file_path)[0] + '.pdf'
    pdfkit.from_file(file_path, pdf_path, configuration=config, options=wkhtmltopdf_options)
    logging.debug('Create pdf: "{}"'.format(pdf_path))


def rename_folder(folder_path, attachments):
    def remove_folder(_path):
        for i in os.listdir(_path):
            _i_path = os.path.join(_path, i)
            if os.path.isfile(_i_path):
                os.remove(_i_path)
            elif os.path.isdir(_i_path):
                remove_folder(_i_path)
        os.rmdir(_path)  # Now the directory is empty of files

    root, folder_name = os.path.split(folder_path)

    new_name = make_file_name_valid(folder_name + ' -- ' + ', '.join(attachments))
    new_path = os.path.join(root, new_name)

    if os.path.exists(new_path):
        remove_folder(new_path)  # удалить рекурсивно

    os.rename(folder_path, new_path)
    logging.debug('Add attachments to name folder: "{}"'.format(new_path))


# ###################### Parsing ############################################
def get_email_message_by_path(eml_path):
    """

    :type eml_path: str
    :rtype: email.Message
    """

    with open(eml_path, 'rb') as eml_file:
        msg = email.message_from_binary_file(eml_file, policy=email.policy.default)
        return msg


def parse_images_and_save(message, folder_for_save):
    img_id_and_path = {}

    for part in message.walk():
        if part.get_content_type() == 'image/png' and part["Content-ID"]:  # игнорируем изображения-вложения
            name = write_part(part, folder_for_save)
            img_id_and_path[part["Content-ID"][1:-1]] = name  # Для замены в html

    logging.debug('Parse and save {} images'.format(len(img_id_and_path)))
    return img_id_and_path


def parse_attachment_and_save(message, folder_for_save):
    attach_name_and_path = []

    for part in message.iter_attachments():
        if part.get_content_type() == 'application/octet-stream':  # Вложения
            name = write_part(part, folder_for_save)

            if name.endswith('.eml'):
                eml_path = os.path.join(folder_for_save, name)
                convert_eml_to_html(eml_path)

            attach_name_and_path.append(name)

        elif part.get_content_type() == 'image/png' and part["Content-ID"] is None:  # Вложенное изображение
            name = write_part(part, folder_for_save)
            attach_name_and_path.append(name)

    logging.debug('Parse and save {} attachments'.format(len(attach_name_and_path)))
    return attach_name_and_path


def get_html(message):
    for part in message.walk():
        if part.get_content_type() == 'text/html':
            html = part.get_payload(decode=True)

            logging.debug('Get html')
            return html

    raise Exception('Html not found')


# ###################### Main logic #########################################
def find_building_code_in_message(html, title, default='UNKNOWN'):
    """
    Пытается найти код здания по максимальному вхождения похожих слов (references) в html и заголовок

    :param title: заголовок
    :type title: str
    :param html: тело письма
    :type html: bytearray
    :param default: значение по умолчанию
    :type default: str
    :return: Найденное значение или значение по умолчанию
    :rtype: str
    """

    text = html.decode('koi8-r').lower() + title.lower()  # декодируем для работы поиска

    code_in_and_counts = {}
    for code, references in CODE_AND_REFERENCES.items():
        count_entry = sum(text.count(reference) for reference in references)
        if count_entry:
            code_in_and_counts[code] = sum(text.count(reference) for reference in references)

    code_building = max(code_in_and_counts, key=lambda x: code_in_and_counts[x], default=default)
    logging.debug('Find code building as "{}"'.format(code_building) if code_building != default else
                  'Error with find code building')

    return code_building


def change_html(html, images_id_and_path, attachments, info_about_letters):
    """
    Заменяем ссылки на изображения, добавляем информацию о вложениях и письме

    :type html: bytes
    :param images_id_and_path: словарь из cid сообщений и относительных путей к нему, для замены в html
    :type images_id_and_path: dict[str, str]
    :type attachments: dict or list or set
    :type info_about_letters: list
    :rtype: bytes
    """

    def replace_link_to_image(html_, images_id_and_path_):
        for img_id, img_path in images_id_and_path_.items():
            html_ = html_.replace(bytes('cid:' + img_id, 'utf-8'), bytes(img_path, 'utf-8'))

        logging.debug('Replace link to image')
        return html_

    def create_list(title, lines, sign='numbers'):
        added_lines = [b'<DIV><FONT size=4 face=Arial>' + title.encode() + b'</FONT></DIV>',
                       b'<ol>' if sign == 'numbers' else b'<ul>']

        for line in lines:
            added_lines.append(
                b'	<li>' + line.replace('<', '&lt;').encode('koi8-r') + b'</li>')  # &lt; - Обертка '<'

        added_lines.extend([b'</ol>' if sign == 'numbers' else b'</ul>',
                            b'<HR>'])  # горизонтальная линия

        return added_lines

    def add_to_top(html_, added_lines):
        lines = html_.split(b'\n')
        number_line_start_with = next(i for i, line in enumerate(lines) if line.lower().startswith(b'<body'))
        # FIXME упадет если не найдет. но странно если в html нет body

        result = lines[:number_line_start_with + 1] + added_lines + lines[number_line_start_with + 1:]
        logging.debug('Add {} lines to top'.format(len(added_lines)))
        return b'\n'.join(result)

    if images_id_and_path:
        html = replace_link_to_image(html, images_id_and_path)

    if attachments:
        info_about_attachments = create_list('Attachments:', attachments)
        html = add_to_top(html, info_about_attachments)

    if info_about_letters:
        info_about_letters = create_list('Information about letter:', info_about_letters, sign='points')
        html = add_to_top(html, info_about_letters)

    return html


def convert_eml_to_html(eml_path):
    """

    :param eml_path:
    :type eml_path:
    :return:
    :rtype:
    """

    logging.debug('=== Start with file: "{}"'.format(eml_path))

    # Шаг 1. Получение Message и html
    msg = get_email_message_by_path(eml_path)
    html = get_html(msg)
    info_about_letters = ['Subject: ' + msg.get("Subject", ""),
                          'Date: ' + msg.get("Date", ""),
                          'From: ' + msg.get("From", ""),
                          'To: ' + msg.get("To", ""),
                          'Cc: ' + msg.get("Cc", ""),
                          'Priority: ' + msg.get("X-MSMail-Priority", ""),
                          ]

    # Шаг 1. Пытаемся найти код здания
    code_building = find_building_code_in_message(html, msg['Subject'])

    # Шаг 2. Формируем имя и создаем папку для сохранения всей информации
    folder_name = create_name(msg['Date'], msg['Subject'], code_building)
    folder_for_save = get_or_create_folder_for_save(eml_path, PATH_OUT, folder_name)

    # Шаг 3. Parse и сохраняем картинки и вложения
    images_id_and_path = parse_images_and_save(msg, folder_for_save)
    attachments = parse_attachment_and_save(msg, folder_for_save)

    # Шаг 4. Заменяем ссылки на изображения, добавляем информацию о вложениях и письме
    html_correct = change_html(html, images_id_and_path, attachments, info_about_letters)

    # Шаг 5. Формируем имя для .html и сохраняем
    html_name = create_name(msg['Date'], msg['Subject'], code_building, file_type='Почта') + '.html'
    html_path = os.path.join(folder_for_save, html_name)
    write_html(html_correct, html_path)

    # Шаг 6. Копируем исходный eml в папку, И создаем pdf из html
    shutil.copy2(eml_path, folder_for_save)  # копирует исходный eml в папку. Мб переместить?
    create_pdf(html_path)

    logging.info('OK. Convert eml to html ["{}" --> "{}"]'.format(eml_path, html_path))

    # Шаг 7. Костыль. Добавляем в имя папки имена вложений
    if attachments:
        # костыль, так как у меня сначала создается папка, а потом в нее все записывается
        rename_folder(folder_for_save, attachments)


def main():
    eml_files = glob.glob(PATH + '*.eml')  # get all .eml files in a list
    for eml_file in eml_files:
        convert_eml_to_html(eml_file)

    logging.info('Convert {} eml files to html'.format(len(eml_files)))


# ###################### Start ##############################################
if __name__ == '__main__':
    logging.basicConfig(
        filename=None, level=logging.INFO,
        format='[%(asctime)s] %(levelname).1s: %(message)s',
        datefmt='%H:%M:%S')
    try:
        main()
    except Exception as err:
        logging.error(err)
        raise

    input()
