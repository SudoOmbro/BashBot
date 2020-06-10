from bash_bot.bot import BashBot
from utils.files import load_config_json, load_scripts_json


def main():
    config = load_config_json()
    scripts = load_scripts_json()
    bot = BashBot(config, scripts)
    bot.start()


if __name__ == '__main__':
    main()
