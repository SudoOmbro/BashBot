from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from bash.bash import execute_command
from telegram_functions.Functions import send_message


class BashBot:

    _START_TEXT = "Welcome to BashBot {}! Write /help to see all the commands and shortcuts"
    _BASE_COMMANDS_TEXT = """
    *COMMANDS*
    /start - _shows bot welcome._
    /help - _shows commands + shortcuts_.
    /options - _lets you manage the bot (WIP)_.
    /download [filename] - _lets you download a file from the machine (WIP)_.
    """

    def __init__(self, bot_token, whitelist):
        self._updater = Updater(bot_token, use_context=True)
        self._updater.dispatcher.add_handler(CommandHandler('start', self._start_command_handler))
        self._updater.dispatcher.add_handler(CommandHandler('help', self._help_command_handler))
        self._updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self._handle_command))
        self._shortcuts = []
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

    # basic command / shortcut handlers -----------------------------------------------------

    def _start_command_handler(self, update, context):
        username = update.effective_user.first_name
        send_message(update, context, self._START_TEXT.format(username), parse_mode=ParseMode.MARKDOWN)

    def _help_command_handler(self, update, context):
        text = self._BASE_COMMANDS_TEXT
        if len(self._shortcuts) != 0:
            text += "\n\n*SHORTCUTS*\n"
            for line in self._shortcuts:
                text += line
        send_message(update, context, text, parse_mode=ParseMode.MARKDOWN)

    def _check_permission(self, update):
        if self._whiteList is not None:
            return update.effective_user.id in self._whiteList
        return True

    def _handle_input(self, update, context, command):
        if self._check_permission(update):
            out = execute_command(command)
            send_message(update, context, out.decode("utf-8"))
        else:
            send_message(update, context, "You don't have access to this Bot")

    def _handle_command(self, update, context):
        command = update.message.text
        self._handle_input(update, context, command)

    def _handle_shortcut(self, update, context):
        # TODO
        pass
