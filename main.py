#!/bin/python

from subprocess import check_output
import re
import sys
from os import path, makedirs

INPUT_FOLDER = ""
OUTPUT_FOLDER = ""


class TranslatedStringInfo:
    def __init__(self, folder, key, string):
        self.folder = folder
        self.key = key
        self.string = string

    def __str__(self):
        return self.key + "\n" + self.folder + "\n" + self.string + "\n"

    def get_string_with_new_key(self, key):
        return self.string.replace(self.key, key)


def find_matched_strings(string_key):
    output_lines = check_output(["grep", "-r", string_key, INPUT_FOLDER]).splitlines()
    info_list = []
    for line in output_lines:
        colon_index = line.find(":")
        file_path = line[:colon_index]
        # check if folder name contains values
        if file_path.find("values") == -1:
            continue
        path_last_segment = path.basename(path.dirname(file_path))

        translated_string = line[colon_index + 1:]
        key = re.findall(r'\"(.+?)\"', line)
        if key is None or len(key) == 0:
            continue

        info_list.append(TranslatedStringInfo(path_last_segment, key[0], translated_string))

    return info_list


def append_string_to_file(file_path, string):
    # create folder if necessary
    if not path.exists(path.dirname(file_path)):
        try:
            makedirs(path.dirname(file_path))
        except OSError as exc:
            raise

    # create strings.xml if necessary
    file_exists = path.isfile(file_path)
    if not file_exists:
        print("not exist: " + file_path)
        print("creating...")
        create_strings_xml(file_path)

    with open(file_path) as f:
        file_str = f.read()

    new_file_string = file_str.replace("</resources>", string + "\n</resources>")
    with open(file_path, 'w') as f:
        f.write(new_file_string)


def create_strings_xml(file_path):
    with open(file_path, 'w+') as f:
        f.write("""<xml version="1.0" encoding="utf-8"?>\n"""
                "<resources>\n"
                "</resources>\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("wrong parameters\n"
              "Usage:\n"
              "python main.py search_key output_key")
        sys.exit(1)

    search_key = output_key = sys.argv[1]
    if len(sys.argv) > 2:
        output_key = sys.argv[2]
    print("search key: " + search_key)
    print("output key: " + output_key)

    string_info_list = find_matched_strings(search_key)
    for s in string_info_list:
        new_file_path = OUTPUT_FOLDER + s.folder + "/strings.xml"
        append_string_to_file(new_file_path, s.get_string_with_new_key(output_key))
