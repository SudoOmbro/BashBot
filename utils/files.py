import json
import os

from bash_bot.scripts import Script

CONFIG_FILE_NAME = "config.json"
SCRIPTS_FILE_NAME = "scripts.json"


class MissingFileException(Exception):
    pass


def load_config_json():
    if os.path.exists(CONFIG_FILE_NAME):
        return load_json_from_file(CONFIG_FILE_NAME)
    raise MissingFileException("The config.json file could not be opened")


def save_config_json(bot_token, whitelist):
    save_json_to_file(
        {
            "telegram_bot_token": bot_token,
            "whitelist": whitelist
        },
        "config.json"
    )


def save_scripts_json(script_list):
    save_json_to_file(
        Script.get_script_list_json(script_list),
        "scripts.json"
    )


def load_scripts_json():
    if os.path.exists(SCRIPTS_FILE_NAME):
        return load_json_from_file(SCRIPTS_FILE_NAME)
    print("no script.json file found, generating an empty one")
    scripts = {"scripts": []}
    save_json_to_file(scripts, SCRIPTS_FILE_NAME)
    return scripts


def load_json_from_file(filename: str):
    file = open(filename, mode="r")
    obj = json.load(file)
    file.close()
    return obj


def save_json_to_file(obj: json, filename: str):
    file = open(filename, "w")
    file.write(json.dumps(obj))
    file.close()
