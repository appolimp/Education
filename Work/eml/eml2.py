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

Документация:
https://docs.google.com/document/d/1_HbTB98g7Wt0plE8mKnO8IBN7iNb8gBSzRABiS8ZKdE/edit?usp=sharing
"""

import datetime
import email.parser
import email.policy
import glob
import logging
import os.path
import re
import shutil
import tempfile
import unicodedata
import uuid

# ###################### Сторонние библиотеки ###############################
import pdfkit  # сторонняя библиотека. должна быть в текущей папке

# Необходимо установить программу wkhtmltopdf (в папке установочник или ссылка в описании выше)
# TODO возможно не нужно и ссылки достаточно
PATH_WKHTMLTOPDF = r'wkhtmltopdf/bin/wkhtmltopdf.exe'  # Чтобы не добавлять программу в PATH

# ###################### Input ##############################################
PATH = r'data\final_project\marina\Sent Items'  # Папка с .eml файлами, вложенные папки скрипт не просматривает

# ###################### Constants ##########################################
PATH_OUT = 'out'
PATH_ERROR = 'error'
PATH_TEMP = 'temp'

CODE_AND_REFERENCES = {
    'NRT2': ['ратуш', 'нрт2', 'нр2', 'нр.', 'журко', '@gals'],
    'SevKab': ['лср', 'севкабел'],
    'PETR2': ['ппр2'],
    'PETR3': ['setl', 'петровск', 'ппр3'],
    'NOVOALEX': ['speech', 'новоалексеевск'],
    'LEN34': ['ленинградск', 'ленинградк'],
    'KJV26': ['кожевенн'],
    'GR9': ['графск'],
    'ChR': ['черная речка', 'чр55', 'чр41', 'chr41', 'chr55', ' чр '],
    'CHAP': ['чаплыги'],
    'BAR4': ['барочн', 'rbi'],
    'VO20': ['20-я лин', 'легенда во', 'васьк', 'легенда_во', 'васильевс'],
}

# ###################### TEMP ##########################################
CREATED_NAME = set()


# ###################### Folder and Files ###################################
def make_file_name_valid(file_name, rep='', empty='empty_name'):
    """

    :type file_name: str
    :param rep: На какой символ заменять
    :type rep str
    :param empty: Значение если имя пустое
    :type empty: str
    :rtype: str
    """

    name = ''.join(ch for ch in file_name if unicodedata.category(ch)[0] != 'C')  # Remove control chars
    name = re.sub(r'[/\\?%*:|<>"]', rep, name)  # remove non valid chars
    name = name.strip()  # remove space in start and end

    while name.endswith('.'):
        name = name[:-1]

    name = name[:99]  # ограничение по максимальной длине. максимум 249 для папки. взял с запасом
    name = name if name else empty

    if name != file_name:
        logging.debug('Make valid name: [{}] --> [{}]'.format(file_name, name))

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
    name = ' '.join(str(i) for i in [date.date(), file_type, code_building, (subject or 'Без темы>')] if i)
    name = make_file_name_valid(name)
    name = name.replace(' Re ', ' ').replace(' RE ', ' ').replace(' Fwd', '').replace(' Fw', '').replace(' FW', '')

    if name in CREATED_NAME:
        name = name + ' ' + str(uuid.uuid4().hex)[:3]
        if name in CREATED_NAME:
            raise NotImplementedError('Имя не уникально')

    CREATED_NAME.add(name)
    logging.debug('Create name: "{}"'.format(name))
    return name


def write_part(part, folder_for_save, ext=''):
    file_name = make_file_name_valid(part.get_filename() or f'Unnamed{ext}')
    uniq_file_name = str(uuid.uuid4().hex)[:5] + '_' + file_name
    file_path = os.path.join(folder_for_save, uniq_file_name)

    with open(file_path, 'wb') as fb:
        fb.write(part.get_payload(decode=True))

    logging.debug('File "{}" was recorded'.format(uniq_file_name))
    return uniq_file_name


def write_html(html, html_path, charset):
    with open(html_path, 'wb') as file_html:
        file_html.write(html.encode(charset))

    return html_path


def create_pdf(file_path, folder_for_log=''):
    try:
        config = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF)  # чтобы не добавлять программу wkhtmltopdf в PATH
        wkhtmltopdf_options = {'enable-local-file-access': None,  # Для доступа к локальным файлам
                               'quiet': '',  # Подавление логирования
                               }

        pdf_path = os.path.splitext(file_path)[0] + '.pdf'
        pdfkit.from_file(file_path, pdf_path, configuration=config, options=wkhtmltopdf_options,)
        logging.debug('Create pdf: "{}"'.format(pdf_path))
    except OSError:
        logging.debug(f'ER. Error with create PDF [{folder_for_log}]')
        error_with_pdf.append(folder_for_log)


def copy_folder(folder, new_path):
    folder_path_long = "\\\\?\\" + os.path.abspath(new_path)  # в win 7 нужно обрабатывать длинные пути (>260)
    if os.path.exists(folder_path_long):
        shutil.rmtree(folder_path_long)

    shutil.copytree(folder, folder_path_long)


# ###################### Parsing ############################################
def get_email_message_by_path(eml_path):
    """

    :type eml_path: str
    :rtype: email.Message
    """
    long_path = "\\\\?\\" + os.path.abspath(eml_path)  # в win 7 нужно обрабатывать длинные пути (>260)
    with open(long_path, 'rb') as eml_file:
        msg = email.message_from_binary_file(eml_file, policy=email.policy.default)
        return msg


def parse_images_and_save(message, folder_for_save):
    img_id_and_path = {}

    for part in message.walk():
        if 'image' in part.get_content_type() and part["Content-ID"]:  # игнорируем изображения-вложения
            if 'png' in part.get_content_type():
                ext = '.png'
            elif 'jpeg' in part.get_content_type():
                ext = '.jpeg'
            elif 'gif' in part.get_content_type():
                ext = '.gif'
            else:
                logging.error('Extension image is not png or jpeg')
                ext = ''
            name = write_part(part, folder_for_save, ext=ext)
            img_id_and_path[part["Content-ID"][1:-1]] = name  # Для замены в html

    logging.debug('Parse and save {} images'.format(len(img_id_and_path)))
    return img_id_and_path


def parse_attachment_and_save(message, folder_for_save):
    attach_name_and_path = []

    for part in message.iter_attachments():
        if 'application/' in part.get_content_type():  # Вложения
            name = write_part(part, folder_for_save)

            if name.endswith('.eml'):
                eml_path = os.path.join(folder_for_save, name)
                convert_eml_to_html(eml_path)

            attach_name_and_path.append(name)

        elif 'image' in part.get_content_type() and part["Content-ID"] is None:  # Вложенное изображение
            name = write_part(part, folder_for_save)
            attach_name_and_path.append(name)

    logging.debug('Parse and save {} attachments'.format(len(attach_name_and_path)))
    return attach_name_and_path


def get_html(message):
    def get_charset(content_type: str):
        prefix = 'charset='
        values = [val.strip() for val in content_type.split(';')]

        for val in values:
            if val.startswith(prefix):
                charset = val.lstrip(prefix).replace('"', '')
                logging.debug(f'Get charset document [{charset}]')
                return charset

        raise NotImplementedError

    for part in message.walk():
        if part.get_content_type() == 'text/html':
            charset = get_charset(part['Content-Type'])
            html = part.get_payload(decode=True).decode(charset)

            logging.debug('Get html')
            return html, charset

    for part in message.walk():
        if part.get_content_type() == 'text/plain':
            charset = get_charset(part['Content-Type'])
            text = part.get_payload(decode=True).decode(charset)
            fake_html = create_fake_html(text, charset=charset)

            logging.debug('Get as fake html')
            return fake_html, charset

    raise Exception('Html not found')


def create_fake_html(text: str, charset: str):
    body = '\n'.join("<p>" + val + "</p>" for val in text.split('\n'))
    fake_html = f"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
     <head>
        <meta http-equiv="Content-Type" content="text/html; charset={charset}">
    </head>
     <body>
        {body}
    </body>
</html>
"""
    logging.debug('Create fake html')
    return fake_html


# ###################### Main logic #########################################
def find_building_code_in_message(html, title, attachments, default='$$$$'):
    """
    Пытается найти код здания по максимальному вхождения похожих слов (references) в html и заголовок

    :param title: заголовок
    :type title: str
    :param html: тело письма
    :type html: str
    :parameter attachments: имена вложенией
    :type attachments: list[str]
    :param default: значение по умолчанию
    :type default: str
    :return: Найденное значение или значение по умолчанию
    :rtype: str
    """

    html = html or ''
    title = title or ''

    text = html.lower() + title.lower() + ''.join(attachments or []).lower()  # декодируем для работы поиска

    code_in_and_counts = {}
    for code, references in CODE_AND_REFERENCES.items():
        code_in_text = 10 * bool(code.lower() in text)
        count_entry_title = 20 * sum(title.lower().count(reference) for reference in references)
        count_entry = sum(text.count(reference) for reference in references)
        all_count = code_in_text + count_entry_title + count_entry

        if all_count:
            code_in_and_counts[code] = all_count

    code_building = max(code_in_and_counts, key=lambda x: code_in_and_counts[x], default=default)
    if 'петухов' in text:
        code_building = code_building + '_BIM'

    logging.debug('Find code building as "{}"'.format(code_building) if code_building != default else
                  'Error with find code building')

    return code_building


def change_html(html, images_id_and_path, attachments, info_about_letters, charset=None):
    """
    Заменяем ссылки на изображения, добавляем информацию о вложениях и письме
    :type html: str
    :param images_id_and_path: словарь из cid сообщений и относительных путей к нему, для замены в html
    :type images_id_and_path: dict[str, str]
    :type attachments: dict or list or set
    :type info_about_letters: list
    :parameter charset: кодировка документа
    :type charset: str
    :rtype: str
    """

    def replace_link_to_image(html_, images_id_and_path_):
        for img_id, img_path in images_id_and_path_.items():
            html_ = html_.replace('cid:' + img_id, img_path)

        logging.debug('Replace link to image')
        return html_

    def create_list(title, lines, sign='numbers'):
        added_lines = ['<DIV><FONT size=4 face=Arial>' + title + '</FONT></DIV>',
                       '<ol>' if sign == 'numbers' else '<ul>']

        for line in lines:
            added_lines.append(
                '	<li>' + line.replace('<', '&lt;') + '</li>')  # &lt; - Обертка '<'

        added_lines.extend(['</ol>' if sign == 'numbers' else '</ul>',
                            '<HR>'])  # горизонтальная линия

        return added_lines

    def add_to_top(html_, added_lines):
        lines = html_.split('\n')
        number_line_start_with = next((i for i, line in enumerate(lines) if '<body' in line.lower()), 0)  # 0 чтобы записать в первую строчку

        result = lines[:number_line_start_with] + added_lines + lines[number_line_start_with:]
        logging.debug('Add {} lines to top'.format(len(added_lines)))
        return '\n'.join(result)

    def add_charset_to_top(html_, charset_):
        head = f'<META content="text/html; charset={charset_}" http-equiv=Content-Type>\n'
        logging.debug('Add charset to html')
        return head + html_

    def change_charset(html_, charset_):
        """

        :type html_: str
        :param charset_: необходимая кодировка
        :type charset_: str
        :rtype: str
        """
        # Поиск кодировки в строке вида: "charset=utf-8" и "charset="koi8-r""
        pattern = re.compile(r'charset=[\"\']?([\w-]*)[\"\';]?')
        result = re.search(pattern, html_)

        if result is None:  # charset не задан в html
            html_ = add_charset_to_top(html_, charset_)
        else:
            html_charset = result.group(1)
            if html_charset != charset_:
                html_ = html_.replace(html_charset, charset_, 1)
                logging.debug(f'Change charset in html [{html_charset}] --> [{charset_}]')

        return html_

    if images_id_and_path:
        html = replace_link_to_image(html, images_id_and_path)

    if attachments:
        info_about_attachments = create_list('Attachments:', attachments)
        html = add_to_top(html, info_about_attachments)

    if info_about_letters:
        info_about_letters = create_list('Information about letter:', info_about_letters, sign='points')
        html = add_to_top(html, info_about_letters)

    if charset:
        html = change_charset(html, charset)

    logging.debug('Change html')
    return html


def is_correct_file(path):
    with open(path, 'rb') as file:
        if any(file):
            return True


def convert_eml_to_html(eml_path):
    """

    :param eml_path:
    :type eml_path:
    :return:
    :rtype:
    """

    logging.debug('=== Start with file: "{}"'.format(eml_path))
    if not is_correct_file(eml_path):
        logging.info(f'OK. File empty [{eml_path}]')
        return

    # Шаг 1. Получение Message и html
    msg = get_email_message_by_path(eml_path)
    html, charset = get_html(msg)
    info_about_letters = ['Subject: ' + msg.get("Subject", ""),
                          'Date: ' + msg.get("Date", ""),
                          'From: ' + msg.get("From", ""),
                          'To: ' + msg.get("To", ""),
                          'Cc: ' + msg.get("Cc", ""),
                          'Priority: ' + msg.get("X-MSMail-Priority", ""),
                          ]

    with tempfile.TemporaryDirectory() as temp_dir:
        logging.debug(temp_dir)

        # Шаг 3. Parse и сохраняем картинки и вложения
        images_id_and_path = parse_images_and_save(msg, temp_dir)
        attachments = parse_attachment_and_save(msg, temp_dir)

        # Шаг 4. Заменяем ссылки на изображения, добавляем информацию о вложениях и письме
        html_correct = change_html(html, images_id_and_path, attachments, info_about_letters, charset)

        # Шаг 5. Формируем имя для .html и сохраняем
        # Шаг 1. Пытаемся найти код здания
        code_building = find_building_code_in_message(html, msg['Subject'], list(attachments))
        html_name = create_name(msg['Date'], msg['Subject'], code_building, file_type='Почта') + '.html'
        html_path = os.path.join(temp_dir, html_name)
        write_html(html_correct, html_path, charset)

        folder_name = create_name(msg['Date'], msg['Subject'], code_building)
        folder_path = os.path.join(os.path.split(eml_path)[0], PATH_OUT, folder_name)
        logging.debug(f'Get folder path [{folder_path}]')

        # Шаг 6.
        shutil.copy2(eml_path, temp_dir)  # копирует исходный eml в папку. Мб переместить?
        create_pdf(html_path, folder_for_log=folder_path)
        copy_folder(temp_dir, folder_path)

        logging.info('OK. Convert eml to html ["{}" --> "{}"]'.format(eml_path, folder_path))


def main(folder):
    path_test = r'D:\share\Revit_Script\Education\Work\eml\data\final_project\Inbox\5D537AEE-00000138.eml'
    if os.path.exists(path_test):
        logging.info('Start test')
        convert_eml_to_html(path_test)
        return

    folder = folder if folder.endswith('\\') else folder + '\\'  # для корректной работы glob
    eml_files = glob.glob(folder + '*.eml')  # get all .eml files in a list
    logging.info(f'Find {len(eml_files)} .eml files')

    for eml_file in eml_files:
        try:
            convert_eml_to_html(eml_file)

        except PermissionError:
            logging.error(f'Отказано в доступе: {eml_file}')
            count_error.append(eml_file)

        except Exception as err_convert:
            logging.exception(err_convert)
            count_error.append(eml_file)

    logging.info('Convert {} eml files to html'.format(len(eml_files)))


error_with_pdf = []
count_error = []
# ###################### Start ##############################################
if __name__ == '__main__':
    logging.basicConfig(
        filename=None, level=logging.INFO,
        format='[%(asctime)s] %(levelname).1s: %(message)s',
        datefmt='%H:%M:%S')
    try:
        main(folder=PATH)
    except Exception as global_err:
        logging.exception(global_err)
        raise

    finally:
        logging.info(f'Error: {len(count_error)}')
        logging.info(f'Error with pdf: {len(error_with_pdf)}')

        if count_error:
            with open('errors_files.txt', 'a', encoding='utf-8') as f:
                f.write(f'\n\n{datetime.datetime.now()}: [{PATH}]\n')
                f.write('\n'.join(count_error))

    # input()
