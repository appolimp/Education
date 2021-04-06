import glob
import os.path
import logging
import email.parser
import email.policy
from email.iterators import _structure
import datetime

from htmldocx import HtmlToDocx
from docx import Document

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
    name = f'{date.date()}_{subject}'

    logging.debug(f'Create name for folder: "{name}"')
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

    logging.debug(f'Parse and save {len(img_id_and_path)} images')
    return img_id_and_path


def write_part(part, work_directory, folder_to_save):
    file_name = part.get_filename()

    absolute_path = os.path.join(folder_to_save, file_name)
    relative_path = os.path.relpath(absolute_path, work_directory)  # Для связи c html

    with open(absolute_path, 'wb') as fb:
        fb.write(part.get_payload(decode=True))

    logging.debug(f'File "{file_name}" was recorded')
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

    logging.debug(f'Parse and save {len(attach_name_and_path)} attachments')
    return attach_name_and_path


def create_folder_or_pass_if_created(folder_path):
    try:
        os.mkdir(folder_path)
        logging.debug(f'Create folder "{folder_path}"')
    except FileExistsError:
        pass


def parse_html(message):
    for part in message.walk():
        if part.get_content_type() == 'text/html':
            my_html = part.get_payload(decode=True)

            logging.debug(f'Get html')
            return my_html


def replace_link_to_image(html, images_id_and_path):
    for img_id, img_path in images_id_and_path.items():
        html = html.replace(bytes('cid:' + img_id, 'utf-8'), bytes(img_path, 'utf-8'))

    logging.debug('Replace link to image')
    return html


def convert_eml_to_html(eml_file, out_folder):
    msg = parsing_file(eml_file)

    folder_name = create_name_for_folder(msg['Date'], msg['Subject'])
    folder_path = os.path.join(out_folder, folder_name)
    create_folder_or_pass_if_created(folder_path)

    images_id_and_path = parse_images_and_save(msg, folder_path, PATH_IMAGE)
    attachments = parse_attachment_and_save(msg, folder_path, PATH_ATTACH)

    html = parse_html(msg)
    html_with_img = replace_link_to_image(html, images_id_and_path)

    html_name = msg['Subject']
    html_path = os.path.join(folder_path, html_name + '.html')
    with open(html_path, 'wb') as f:
        f.write(html_with_img)

    logging.debug(f'OK. Convert eml to html [{eml_file} --> {html_path}]')


def main():
    eml_files = glob.glob(PATH + '*.eml')  # get all .eml files in a list
    out_folder = os.path.join(PATH, PATH_OUT)
    create_folder_or_pass_if_created(out_folder)

    for eml_file in eml_files:
        convert_eml_to_html(eml_file, out_folder)

    logging.info(f'Convert {len(eml_files)} eml files to html')


if __name__ == '__main__':
    logging.basicConfig(
        filename=None, level=logging.DEBUG,
        format='[%(asctime)s] %(levelname).1s: %(message)s',
        datefmt='%H:%M:%S')
    main()
