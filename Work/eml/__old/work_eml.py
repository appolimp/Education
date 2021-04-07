import datetime
import json
import eml_parser
import glob
import os.path


def json_serial(obj):
  if isinstance(obj, datetime.datetime):
      serial = obj.isoformat()
      return serial


path = 'data/'  # set this to "./" if in current directory
eml_files = glob.glob(path + '*.eml')  # get all .eml files in a list
for eml_file in eml_files:
    print(eml_file)
    with open(eml_file, 'rb') as fp:  # select a specific email file from the list
        raw_email = fp.read()
        ep = eml_parser.EmlParser(include_attachment_data=True, include_raw_body=True, parse_attachments=True)
        parsed_eml = ep.decode_email_bytes(raw_email)

    with open('data/2/' + os.path.split(eml_file)[-1] + '.json', 'w') as file:
        json.dump(parsed_eml, file, default=json_serial, indent=4, sort_keys=False)

# print(json.dumps(parsed_eml, default=json_serial, indent=4))

