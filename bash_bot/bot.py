from telegram import ParseMode, InlineKeyboardButton
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from utils.bash import execute_command
from bash_bot.functions import send_message, send_message_ik


class BashBot:

    _START_TEXT = "Welcome to BashBot {}!\nUse /help to see all the commands and shortcuts"
    _BASE_COMMANDS_TEXT = """
    *COMMANDS*
    /start - _shows bot welcome._
    /help - _shows commands + shortcuts_.
    /options - _lets you manage the bot_.
    /download [filename] - _lets you download a file from the machine_.
    /scripts - _shows all the saved scripts_.
    """
    _ACCESS_DENIED_TEXT = "You don't have access to this Bot"
    _OPTIONS_TEXT = "Here's what *you* can do"
    _OPTIONS_KEYBOARD = [
        [InlineKeyboardButton("add user ID to Whitelist", callback_data="addToWhitelist")],
        [InlineKeyboardButton("remove user ID from Whitelist", callback_data="removeFromWhitelist")],
        [InlineKeyboardButton("add shortcut", callback_data="addShortcut")],
        [InlineKeyboardButton("remove shortcut", callback_data="removeShortcut")]
    ]

    def __init__(self, config, scripts):
        """ initialize all of the bot's variables """
        bot_token = config["telegram_bot_token"]
        whitelist = config["whitelist"]
        self._scripts = scripts
        self._updater = Updater(bot_token, use_context=True)
        self._updater.dispatcher.add_handler(CommandHandler('start', self._start_command_handler))
        self._updater.dispatcher.add_handler(CommandHandler('help', self._help_command_handler))
        self._updater.dispatcher.add_handler(CommandHandler('options', self._options_command_handler))
        self._updater.dispatcher.add_handler(CommandHandler('download', self._download_command_handler))
        self._updater.dispatcher.add_handler(CommandHandler('scripts', self._scripts_command_handler))
        self._updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self._handle_command))
        if len(whitelist) != 0:
            self._whiteList = whitelist
        else:
            self._whiteList = None

    def start(self):
        """ start the bot """
        print("starting updater...")
        self._updater.start_polling()
        print("updater started")
        self._updater.idle()
        print("updater stopped")

    # utility ----------------------------------------------------------------------------------------------------------

    def _check_permission(self, update):
        """ checks if the update comes from a whitelisted user """
        if self._whiteList is not None:
            return update.effective_user.id in self._whiteList
        return True

    def _handle_shell_input(self, update, context, command):
        """ handles an input to the shell, used to handle both single commands and scripts """
        if self._check_permission(update):
            out = execute_command(command)
            send_message(update, context, out.decode("utf-8"))
        else:
            send_message(update, context, self._ACCESS_DENIED_TEXT)

    # telegram command handlers ----------------------------------------------------------------------------------------

    def _start_command_handler(self, update, context):
        """ greets the user """
        username = update.effective_user.first_name
        send_message(update, context, self._START_TEXT.format(username))

    def _help_command_handler(self, update, context):
        """ sends the user the commands + scripts list """
        text = self._BASE_COMMANDS_TEXT
        if len(self._scripts) != 0:
            # FIXME
            text += "\n\n*SCRIPTS*\n"
            for line in self._scripts:
                text += line
        send_message(update, context, text, parse_mode=ParseMode.MARKDOWN)

    def _options_command_handler(self, update, context):
        """ shows the user the options keyboard """
        if self._check_permission(update):
            send_message_ik(update, context, self._OPTIONS_TEXT, self._OPTIONS_KEYBOARD)

    def _download_command_handler(self, update, context):
        """ lets the user download a file from the machine """
        if self._check_permission(update):
            send_message(update, context, "This feature has yet to be implemented")
            # TODO
        else:
            send_message(update, context, self._ACCESS_DENIED_TEXT)

    def _scripts_command_handler(self, update, context):
        """ shows the user all the available scripts """
        if self._check_permission(update):
            send_message(update, context, "This feature has yet to be implemented")
            # TODO
        else:
            send_message(update, context, self._ACCESS_DENIED_TEXT)

    # basic shell command handlers -------------------------------------------------------------------------------------

    def _handle_command(self, update, context):
        """ handle a single commands sent by the user """
        command = update.message.text
        self._handle_shell_input(update, context, command)

    def _handle_script(self, update, context):
        """ handle the execution of a script """
        # TODO
        pass

    # options callback / conversation handlers -------------------------------------------------------------------------

    # TODO
