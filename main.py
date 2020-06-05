from bash_bot.bot import BashBot
import json


def main():

    # load options from Json file
    file = open("config.json", mode="r")
    config = json.load(file)
    token = config["telegram_bot_token"]
    whitelist = config["whitelist"]
    file.close()

    # create and start bot
    bot = BashBot(token, whitelist)
    bot.start()


if __name__ == '__main__':
    main()
