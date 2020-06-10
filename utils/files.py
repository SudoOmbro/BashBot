import json
import os


CONFIG_FILE_NAME = "config.json"
SCRIPTS_FILE_NAME = "scripts.json"


class MissingFileException(Exception):
    pass


def load_config_json():
    if os.path.exists(CONFIG_FILE_NAME):
        return load_json_from_file(CONFIG_FILE_NAME)
    raise MissingFileException("The config.json file could not be opened")


def load_scripts_json():
    if os.path.exists(SCRIPTS_FILE_NAME):
        return load_json_from_file(SCRIPTS_FILE_NAME)
    print("no script.json file found, generating an empty one")
    scripts = {}
    save_json_to_file(scripts, SCRIPTS_FILE_NAME)
    return scripts


def load_json_from_file(filename):
    file = open(filename, mode="r")
    obj = json.load(file)
    file.close()
    return obj


def save_json_to_file(obj, filename):
    file = open(filename, "w")
    json.dump(obj, file)
    file.close()
