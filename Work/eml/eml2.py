import glob
import os.path
import logging
import email.parser
import email.policy
import datetime
import shutil

PATH = 'data\\'
PATH_OUT = 'out'
PATH_IMAGE = 'img'
PATH_ATTACH = 'attach'


def create_name_for_folder(data_str, subject):
    """

    :param data_str:
    :type data_str: str
    :type subject: str
    :rtype: str
    """

    date = datetime.datetime.strptime(data_str, '%a, %d %b %Y %X %z')
    name = '{}_{}'.format(date.date(), subject)

    logging.debug('Create name for folder: "{}"'.format(name))
    return name


def parsing_file(eml_path):
    """

    :type eml_path: str
    :rtype: email.Message
    """

    with open(eml_path, 'rb') as eml_file:
        msg = email.message_from_binary_file(eml_file, policy=email.policy.default)
        return msg


def parse_images_and_save(message, folder_path, relative_image_path):
    img_id_and_path = {}

    folder_to_image = os.path.join(folder_path, relative_image_path)
    create_folder_or_pass_if_created(folder_to_image)

    for part in message.walk():
        if part.get_content_type() == 'image/png' and part["Content-ID"]:  # игнорируем изображения-вложения
            _, relative_path = write_part(part, folder_path, folder_to_image)
            img_id_and_path[part["Content-ID"][1:-1]] = relative_path  # Для замены в html

    logging.debug('Parse and save {} images'.format(len(img_id_and_path)))
    return img_id_and_path


def write_part(part, work_directory, folder_to_save):
    file_name = part.get_filename()

    absolute_path = os.path.join(folder_to_save, file_name)
    relative_path = os.path.relpath(absolute_path, work_directory)  # Для связи c html

    with open(absolute_path, 'wb') as fb:
        fb.write(part.get_payload(decode=True))

    logging.debug('File "{}" was recorded'.format(file_name))
    return file_name, relative_path


def parse_attachment_and_save(message, folder_path, relative_attachment_path):
    attach_name_and_path = {}

    folder_to_attachment = os.path.join(folder_path, relative_attachment_path)
    create_folder_or_pass_if_created(folder_to_attachment)
    for part in message.iter_attachments():
        if part.get_content_type() == 'application/octet-stream':  # вложение
            name, relative_path = write_part(part, folder_path, folder_to_attachment)
            attach_name_and_path[name] = relative_path

        elif part.get_content_type() == 'image/png' and part["Content-ID"] is None:  # Вложенное изображение
            name, relative_path = write_part(part, folder_path, folder_to_attachment)
            attach_name_and_path[name] = relative_path

    logging.debug('Parse and save {} attachments'.format(len(attach_name_and_path)))
    return attach_name_and_path


def create_folder_or_pass_if_created(folder_path):
    try:
        os.mkdir(folder_path)
        logging.debug('Create folder "{}"'.format(folder_path))
    except FileExistsError:
        pass


def parse_html(message):
    for part in message.walk():
        if part.get_content_type() == 'text/html':
            my_html = part.get_payload(decode=True)

            logging.debug('Get html')
            return my_html


def replace_link_to_image(html, images_id_and_path):
    for img_id, img_path in images_id_and_path.items():
        html = html.replace(bytes('cid:' + img_id, 'utf-8'), bytes(img_path, 'utf-8'))

    logging.debug('Replace link to image')
    return html


def create_list(title, lines, sign='numbers'):
    added_lines = [b'<DIV><FONT size=4 face=Arial>' + title.encode() + b'</FONT></DIV>',
                   b'<ol>' if sign == 'numbers' else b'<ul>']

    for line in lines:
        added_lines.append(b'	<li>' + line.replace('<', '&lt;').encode('koi8-r') + b'</li>')  # &lt; - Обертка '<'

    added_lines.extend([b'</ol>' if sign == 'numbers' else b'</ul>',
                        b'<HR>'])  # горизонтальная линия

    return added_lines


def add_to_top(html, added_lines):
    lines = html.split(b'\n')
    number_line_start_with = next(i for i, line in enumerate(lines) if line.startswith(b'<BODY'))
    result = lines[:number_line_start_with + 1] + added_lines + lines[number_line_start_with + 1:]
    logging.debug('Add {} lines to top'.format(len(added_lines)))
    return b'\n'.join(result)


def change_html(html, images_id_and_path, attachments, info_about_letters):
    """

    :param html:
    :type html:
    :param images_id_and_path:
    :type images_id_and_path:
    :param attachments:
    :type attachments:
    :param info_about_letters:
    :type info_about_letters:
    :return:
    :rtype:
    """

    if images_id_and_path:
        html = replace_link_to_image(html, images_id_and_path)

    if attachments:
        info_about_attachments = create_list('Attachments:', attachments)
        html = add_to_top(html, info_about_attachments)

    if info_about_letters:
        info_about_letters = create_list('Information about letter:', info_about_letters, sign='points')
        html = add_to_top(html, info_about_letters)

    return html


def write_html(html, folder_path, name):
    html_path = os.path.join(folder_path, name)
    with open(html_path, 'wb') as f:
        f.write(html)

    return html_path


def convert_eml_to_html(eml_file, out_folder):
    msg = parsing_file(eml_file)
    info_about_letters = ['Subject: ' + msg.get("Subject", ""),
                          'Date: ' + msg.get("Date", ""),
                          'From: ' + msg.get("From", ""),
                          'To: ' + msg.get("To", ""),
                          'Cc: ' + msg.get("Cc", ""),
                          'Priority: ' + msg.get("X-MSMail-Priority", ""),
                          ]

    folder_name = create_name_for_folder(msg['Date'], msg['Subject'])
    folder_path = os.path.join(out_folder, folder_name)
    create_folder_or_pass_if_created(folder_path)

    images_id_and_path = parse_images_and_save(msg, folder_path, PATH_IMAGE)
    attachments = parse_attachment_and_save(msg, folder_path, PATH_ATTACH)

    html = parse_html(msg)
    html = change_html(html, images_id_and_path, attachments, info_about_letters)
    html_path = write_html(html, folder_path, name=msg['Subject'] + '.html')

    logging.debug('OK. Convert eml to html [{} --> {}]'.format(eml_file, html_path))
    return folder_path, html_path


def main():
    eml_files = glob.glob(PATH + '*.eml')  # get all .eml files in a list
    out_folder = os.path.join(PATH, PATH_OUT)
    create_folder_or_pass_if_created(out_folder)

    for eml_file in eml_files:
        file_folder, html_path = convert_eml_to_html(eml_file, out_folder)
        shutil.copy2(eml_file, file_folder)

    logging.info('Convert {} eml files to html'.format(len(eml_files)))


if __name__ == '__main__':
    logging.basicConfig(
        filename=None, level=logging.DEBUG,
        format='[%(asctime)s] %(levelname).1s: %(message)s',
        datefmt='%H:%M:%S')
    main()
