import logging
import os
import traceback

from telegram import ParseMode, TelegramError
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler, ConversationHandler

from bash_bot.scripts import Script
from utils.bash import Shell
from bash_bot.functions import send_message, get_inline_keyboard_from_string_list, delete_callback_message, \
    get_inline_keyboard_from_script_list
from utils.files import save_scripts_json, save_config_json
from utils.resources import Resources


logging.basicConfig(
    format='%(asctime)s - {%(pathname)s} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


class BashBot:

    [

        DOWNLOAD,
        UPLOAD,
        SCRIPT_SELECT,
        # options
        OPTIONS,
        ADD_USER,
        REMOVE_USER,
        REMOVE_SCRIPT,
        LOAD_SCRIPT,
        EDIT_SCRIPT,
        EDIT_SCRIPT_TEXTFIELD

    ] = range(10)

    WORKING_DIRECTORY = os.getcwd()

    def __init__(self, config, scripts_json):
        """ initialize all of the bot's variables """
        # init resources
        self._res = Resources()
        # init telegram stuff
        self._bot_token = config["telegram_bot_token"]
        whitelist = config["whitelist"]
        self._updater = Updater(self._bot_token, use_context=True)
        # conversation handlers
        yes_handler = CallbackQueryHandler(self._action_confirm_handler, pattern="yes")
        no_handler = CallbackQueryHandler(self._action_cancelled_handler, pattern="no")
        # options
        self._updater.dispatcher.add_handler(ConversationHandler(
            entry_points=[
                CommandHandler('options', self._options_command_handler)
            ],
            states={
                self.OPTIONS: [
                    CallbackQueryHandler(
                        self._add_to_whitelist_callback_handler,
                        pattern="addToWhitelist"
                    ),
                    CallbackQueryHandler(
                        self._remove_from_whitelist_callback_handler,
                        pattern="removeFromWhitelist"
                    ),
                    CallbackQueryHandler(
                        self._show_scripts_callback_handler,
                        pattern="seeAllScripts"
                    ),
                    CallbackQueryHandler(
                        self._remove_script_callback_handler,
                        pattern="removeScript"
                    ),
                    CallbackQueryHandler(
                        self._edit_script_menu_new_script,
                        pattern="newScript"
                    ),
                    CallbackQueryHandler(
                      self._edit_script_menu_load_script_handler,
                      pattern="editScript"
                    ),
                    CallbackQueryHandler(
                        self._end_conversation_handler,
                        pattern="back"
                    )
                ],
                self.ADD_USER: [
                    yes_handler,
                    no_handler,
                    MessageHandler(Filters.text & (~Filters.command), self._add_to_whitelist_handler)
                ],
                self.REMOVE_USER: [
                    yes_handler,
                    no_handler,
                    CallbackQueryHandler(self._remove_from_whitelist_handler),
                ],
                self.REMOVE_SCRIPT: [
                    yes_handler,
                    no_handler,
                    CallbackQueryHandler(self._remove_script_handler),
                ],
                self.LOAD_SCRIPT: [
                    CallbackQueryHandler(self._edit_script_menu_load_script)
                ],
                self.EDIT_SCRIPT: [
                    CallbackQueryHandler(self._toggle_script_verbose_handler, pattern="toggleVerbose"),
                    CallbackQueryHandler(self._edit_script_save, pattern="save"),
                    CallbackQueryHandler(self._edit_script_back, pattern="back"),
                    CallbackQueryHandler(self._edit_script_text_field_handler)
                ],
                self.EDIT_SCRIPT_TEXTFIELD: [
                    MessageHandler(Filters.text & (~Filters.command), self._edit_script_text_field)
                ]
            },
            fallbacks=[
                CommandHandler("end", self._end_conversation_handler)
            ]
        ))
        # download
        self._updater.dispatcher.add_handler(ConversationHandler(
            entry_points=[
                CommandHandler('download', self._download_command_handler)
            ],
            states={
                self.DOWNLOAD: [
                    MessageHandler(Filters.text & (~Filters.command), self._download_handler)
                ]
            },
            fallbacks=[
                CommandHandler("end", self._end_conversation_handler)
            ]
        ))
        # upload
        self._updater.dispatcher.add_handler(ConversationHandler(
            entry_points=[
                CommandHandler('upload', self._upload_command_handler)
            ],
            states={
                self.UPLOAD: [
                    MessageHandler(Filters.all & (~Filters.command) & (~Filters.text), self._upload_handler)
                ]
            },
            fallbacks=[
                CommandHandler("end", self._end_conversation_handler)
            ]
        ))
        # scripts
        self._updater.dispatcher.add_handler(ConversationHandler(
            entry_points=[
                CommandHandler('scripts', self._scripts_command_handler)
            ],
            states={
                self.SCRIPT_SELECT: [
                    CallbackQueryHandler(self._handle_script)
                ]
            },
            fallbacks=[
                CommandHandler("end", self._end_conversation_handler)
            ]
        ))
        # command handlers
        self._updater.dispatcher.add_handler(CommandHandler('start', self._start_command_handler))
        self._updater.dispatcher.add_handler(CommandHandler('help', self._help_command_handler))
        self._updater.dispatcher.add_handler(CommandHandler('h', self._help_command_handler))
        # text message handler
        self._updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self._handle_command))
        # callback query handlers
        self._updater.dispatcher.add_error_handler(self._error)
        # check if there is a whitelist
        if len(whitelist) != 0:
            self._whiteList = whitelist
        else:
            self._whiteList = None
        self._scripts_json = scripts_json
        self._scripts = Script.get_scripts_from_json(self._scripts_json)
        # init shell
        self.shell = Shell(self.WORKING_DIRECTORY)
        print("working directory: " + self.WORKING_DIRECTORY)

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
            out = self.shell.execute_command(command)
            if out is not None:
                send_message(update, context, out)
        else:
            send_message(update, context, self._res.ACCESS_DENIED_TEXT)

    def _send_confirmation(self, update, context, function, argument=None, current_menu=None):
        context.chat_data["function"] = function
        context.chat_data["argument"] = argument
        context.chat_data["menu"] = current_menu
        send_message(
            update,
            context,
            text=self._res.CONFIRM_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            keyboard=self._res.CONFIRM_KEYBOARD
        )

    def _action_confirm_handler(self, update, context):
        delete_callback_message(update, context)
        if self._check_permission(update):
            context.chat_data["function"](update, context)
            if context.chat_data["menu"] is not None:
                return context.chat_data["menu"](update, context)
        else:
            send_message(update, context, self._res.ACCESS_DENIED_TEXT)
        return ConversationHandler.END

    def _action_cancelled_handler(self, update, context):
        delete_callback_message(update, context)
        if self._check_permission(update):
            send_message(update, context, self._res.CANCEL_TEXT)
            if context.chat_data["menu"] is not None:
                return context.chat_data["menu"](update, context)
        else:
            send_message(update, context, self._res.ACCESS_DENIED_TEXT)
        return ConversationHandler.END

    def _end_conversation_handler(self, update, context):
        delete_callback_message(update, context)
        send_message(update, context, self._res.END_TEXT)
        return ConversationHandler.END

    @staticmethod
    def _error(update, context):
        """Log Errors caused by Updates."""
        logger.error(
            'with user: "%s (%s)"\nmessage: "%s\ntraceback %s"',
            update.effective_user,
            update.effective_user.id,
            context.error,
            traceback.format_exc()
        )

    # telegram command handlers ----------------------------------------------------------------------------------------

    def _start_command_handler(self, update, context):
        """ greets the user """
        username = update.effective_user.first_name
        send_message(update, context, self._res.START_TEXT.format(username))

    def _help_command_handler(self, update, context):
        """ sends the user the commands + scripts list """
        send_message(update, context, self._res.BASE_COMMANDS_TEXT, parse_mode=ParseMode.MARKDOWN)

    def _options_command_handler(self, update, context):
        """ shows the user the options keyboard """
        if self._check_permission(update):
            send_message(
                update,
                context,
                self._res.OPTIONS_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                keyboard=self._res.OPTIONS_KEYBOARD
            )
            return self.OPTIONS
        else:
            send_message(update, context, self._res.ACCESS_DENIED_TEXT)
            return ConversationHandler.END

    def _download_command_handler(self, update, context):
        """ lets the user download a file from the machine """
        if self._check_permission(update):
            send_message(update, context, self._res.DOWNLOAD_TEXT)
            return self.DOWNLOAD
        else:
            send_message(update, context, self._res.ACCESS_DENIED_TEXT)
            return ConversationHandler.END

    def _upload_command_handler(self, update, context):
        """ lets the user download a file from the machine """
        if self._check_permission(update):
            send_message(update, context, self._res.UPLOAD_TEXT)
            return self.UPLOAD
        else:
            send_message(update, context, self._res.ACCESS_DENIED_TEXT)
            return ConversationHandler.END

    def _scripts_command_handler(self, update, context):
        """ shows the user all the available scripts """
        if self._check_permission(update):
            if len(self._scripts) == 0:
                send_message(update, context, self._res.NO_SCRIPTS_TEXT, parse_mode=ParseMode.MARKDOWN)
                return ConversationHandler.END
            keyboard = get_inline_keyboard_from_script_list(self._scripts)
            send_message(
                update,
                context,
                self._res.SCRIPTS_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                keyboard=keyboard
            )
            return self.SCRIPT_SELECT
        else:
            send_message(update, context, self._res.ACCESS_DENIED_TEXT)
            return ConversationHandler.END

    # basic shell command handlers -------------------------------------------------------------------------------------

    def _handle_command(self, update, context):
        """ handle a single commands sent by the user """
        command = update.message.text
        self._handle_shell_input(update, context, command)

    def _handle_script(self, update, context):
        """ handle the execution of a script """
        if self._check_permission(update):
            script = Script.get_script_from_name(self._scripts, update.callback_query.data)
            if script.verbose:
                for command in script.body.split("\n"):
                    self._handle_shell_input(update, context, command)
            else:
                for command in script.body.split("\n"):
                    self.shell.execute_command(command)
            send_message(update, context, self._res.SCRIPT_DONE_TEXT.format(script.name))
        else:
            send_message(update, context, self._res.ACCESS_DENIED_TEXT)
        delete_callback_message(update, context)
        return ConversationHandler.END

    # options callback / conversation handlers -------------------------------------------------------------------------

    def _download_handler(self, update, context):
        filename = update.message.text
        file = self.shell.download_file(filename)
        if file is not None:
            send_message(update, context, text=self._res.DOWNLOAD_SUCCESS, file=file)
            file.close()
        else:
            send_message(update, context, text=self._res.DOWNLOAD_FAILED)
        return ConversationHandler.END

    def _upload_handler(self, update, context):
        try:
            file_id = update.message.document["file_id"]
            file_name = update.message.document["file_name"]
            file = context.bot.getFile(file_id).download_as_bytearray()
            self.shell.upload_file(file, file_name)
            send_message(update, context, text=self._res.UPLOAD_SUCCESS, parse_mode=ParseMode.MARKDOWN)
        except TelegramError:
            send_message(update, context, text=self._res.UPLOAD_FAILED, parse_mode=ParseMode.MARKDOWN)
        return ConversationHandler.END

    def _show_scripts_callback_handler(self, update, context):
        delete_callback_message(update, context)
        if len(self._scripts) == 0:
            send_message(update, context, self._res.NO_SCRIPTS_TEXT, parse_mode=ParseMode.MARKDOWN)
        else:
            for script in self._scripts:
                send_message(update, context, str(script), parse_mode=ParseMode.MARKDOWN)
        self._options_command_handler(update, context)

    # add to whitelist --->

    def _add_to_whitelist_callback_handler(self, update, context):
        delete_callback_message(update, context)
        send_message(update, context, self._res.ADD_TO_WHITELIST_TEXT, parse_mode=ParseMode.MARKDOWN)
        return self.ADD_USER

    def _add_to_whitelist_handler(self, update, context):
        if self._check_permission(update):
            user_id = update.message.text
            self._send_confirmation(
                update,
                context,
                self._add_to_whitelist,
                argument=user_id,
                current_menu=self._options_command_handler,
            )
        else:
            send_message(update, context, self._res.ACCESS_DENIED_TEXT)

    def _add_to_whitelist(self, update, context):
        try:
            user_id = int(context.chat_data["argument"])
            if self._whiteList is None:
                self._whiteList = [update.effective_user.id, user_id]
                save_config_json(self._bot_token, self._whiteList)
            elif user_id not in self._whiteList:
                self._whiteList.append(user_id)
                send_message(update, context, self._res.ADD_TO_WHITELIST_SUCCESS)
                save_config_json(self._bot_token, self._whiteList)
            else:
                send_message(update, context, self._res.USER_ALREADY_IN_WHITELIST_TEXT)
        except ValueError:
            send_message(update, context, text=self._res.USER_ID_VALUE_ERROR, parse_mode=ParseMode.MARKDOWN)

    # remove from whitelist --->

    def _remove_from_whitelist_callback_handler(self, update, context):
        delete_callback_message(update, context)
        if self._whiteList is None:
            send_message(update, context, self._res.NO_USERS_IN_WHITELIST_TEXT, parse_mode=ParseMode.MARKDOWN)
            return self._options_command_handler(update, context)
        send_message(
            update,
            context,
            self._res.REMOVE_FROM_WHITELIST_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            keyboard=get_inline_keyboard_from_string_list(self._whiteList),
        )
        return self.REMOVE_USER

    def _remove_from_whitelist_handler(self, update, context):
        delete_callback_message(update, context)
        if self._check_permission(update):
            user_id = update.callback_query.data
            self._send_confirmation(
                update,
                context,
                self._remove_from_whitelist,
                argument=user_id,
                current_menu=self._options_command_handler,
            )
        else:
            send_message(update, context, self._res.ACCESS_DENIED_TEXT)
            return ConversationHandler.END

    def _remove_from_whitelist(self, update, context):
        user_id = int(context.chat_data["argument"])
        if user_id in self._whiteList:
            self._whiteList.remove(user_id)
            save_config_json(self._bot_token, self._whiteList)
        send_message(
            update,
            context,
            self._res.REMOVE_FROM_WHITELIST_SUCCESS.format(user_id),
            parse_mode=ParseMode.MARKDOWN
        )

    # remove script --->

    def _remove_script_callback_handler(self, update, context):
        delete_callback_message(update, context)
        if len(self._scripts) == 0:
            send_message(update, context, text=self._res.NO_SCRIPTS_TEXT, parse_mode=ParseMode.MARKDOWN)
            return self._options_command_handler(update, context)
        send_message(
            update,
            context,
            text=self._res.REMOVE_SCRIPT_TEXT,
            keyboard=get_inline_keyboard_from_script_list(self._scripts)
        )
        return self.REMOVE_SCRIPT

    def _remove_script_handler(self, update, context):
        delete_callback_message(update, context)
        if self._check_permission(update):
            send_message(
                update,
                context,
                text=str(Script.get_script_from_name(self._scripts, update.callback_query.data)),
                parse_mode=ParseMode.MARKDOWN
            )
            self._send_confirmation(
                update,
                context,
                self._remove_script,
                argument=update.callback_query.data,
                current_menu=self._options_command_handler
            )
        else:
            send_message(update, context, self._res.ACCESS_DENIED_TEXT)
            return ConversationHandler.END

    def _remove_script(self, update, context):
        delete_callback_message(update, context)
        script_name = context.chat_data["argument"]
        script = Script.get_script_from_name(self._scripts, script_name)
        self._scripts.remove(script)
        send_message(
            update,
            context,
            text=self._res.SCRIPT_SUCCESSFULLY_REMOVED_TEXT.format(script_name)
        )
        save_scripts_json(self._scripts)

    # edit script menu --->

    def _edit_script_menu_show_script(self, update, context):
        send_message(
            update,
            context,
            text=str(context.chat_data["current_script"]),
            parse_mode=ParseMode.MARKDOWN,
            keyboard=self._res.EDIT_SCRIPT_KEYBOARD
        )
        return self.EDIT_SCRIPT

    def _edit_script_menu_new_script(self, update, context):
        delete_callback_message(update, context)
        if self._check_permission(update):
            context.chat_data["current_script"] = Script("script name", "cd", "script description", True)
            self._edit_script_menu_show_script(update, context)
            return self.EDIT_SCRIPT
        send_message(update, context, self._res.ACCESS_DENIED_TEXT)
        return ConversationHandler.END

    def _edit_script_menu_load_script_handler(self, update, context):
        delete_callback_message(update, context)
        if self._check_permission(update):
            if len(self._scripts) != 0:
                delete_callback_message(update, context)
                send_message(
                    update,
                    context,
                    text=self._res.SCRIPTS_SHOW_ALL_TEXT,
                    keyboard=get_inline_keyboard_from_script_list(self._scripts)
                )
                return self.LOAD_SCRIPT
            else:
                send_message(update, context, text=self._res.NO_SCRIPTS_TEXT, parse_mode=ParseMode.MARKDOWN)
                return self._options_command_handler(update, context)
        send_message(update, context, self._res.ACCESS_DENIED_TEXT)
        return ConversationHandler.END

    def _edit_script_menu_load_script(self, update, context):
        context.chat_data["current_script"] = Script.get_script_from_name(self._scripts, update.callback_query.data)
        return self._edit_script_menu_show_script(update, context)

    def _edit_script_text_field_handler(self, update, context):
        delete_callback_message(update, context)
        field = update.callback_query.data.replace("change_", "")
        context.chat_data["argument"] = field
        send_message(
            update,
            context,
            text="`{}`".format(context.chat_data["current_script"].__dict__[field]),
            parse_mode=ParseMode.MARKDOWN
        )
        return self.EDIT_SCRIPT_TEXTFIELD

    def _edit_script_text_field(self, update, context):
        field = context.chat_data["argument"]
        text = update.message.text
        context.chat_data["current_script"].__dict__[field] = text
        return self._edit_script_menu_show_script(update, context)

    def _toggle_script_verbose_handler(self, update, context):
        delete_callback_message(update, context)
        context.chat_data["current_script"].verbose = not context.chat_data["current_script"].verbose
        self._edit_script_menu_show_script(update, context)

    def _edit_script_save(self, update, context):
        delete_callback_message(update, context)
        if self._check_permission(update):
            context.chat_data["current_script"].save(self._scripts)
            save_scripts_json(self._scripts)
            send_message(
                update,
                context,
                text=self._res.SCRIPT_SUCCESSFULLY_SAVED_TEXT,
                parse_mode=ParseMode.MARKDOWN
            )
            self._edit_script_menu_show_script(update, context)
        else:
            send_message(update, context, self._res.ACCESS_DENIED_TEXT)
            return ConversationHandler.END

    def _edit_script_back(self, update, context):
        delete_callback_message(update, context)
        return self._options_command_handler(update, context)
