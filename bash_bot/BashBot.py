
from telegram.ext import Updater, MessageHandler, Filters

from bash.Bash import execute_command
from telegram_functions.Functions import send_message


class BashBot:

    def __init__(self, bot_token, whitelist):
        self._updater = Updater(bot_token, use_context=True)
        self._updater.dispatcher.add_handler(MessageHandler(Filters.text, self.handle_command))
        if len(whitelist) != 0:
            self._whiteList = whitelist
        else:
            self._whiteList = None

    def start(self):
        print("starting updater...")
        self._updater.start_polling()
        print("updater started")
        self._updater.idle()
        print("updater stopped")

    def check_permission(self, update):
        if self._whiteList is not None:
            return update.effective_user.id in self._whiteList
        return True

    def handle_command(self, update, context):
        if self.check_permission(update):
            command = update.message.text
            out = execute_command(command)
            send_message(update, context, out.decode("utf-8"))
        else:
            send_message(update, context, "You don't have access to this Bot")
