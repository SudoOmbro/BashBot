from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class Resources:

    """ this class contains all the text prompts and keyboards """
    # TODO add support for multiple languages

    # TEXTS
    # general
    START_TEXT = "Welcome to BashBot {}!\nUse /help to see all the commands and shortcuts"
    BASE_COMMANDS_TEXT = """
        *COMMANDS*
        /start - _shows bot welcome._
        /help - _shows commands + shortcuts_.
        /options - _lets you manage the bot_.
        /download [filename] - _lets you download a file from the machine_.
        /scripts - _shows all the saved scripts_.
        """
    ACCESS_DENIED_TEXT = "You don't have access to this Bot"
    OPTIONS_TEXT = "Here's what *you* can do"
    CONFIRM_TEXT = "Are you sure?"
    CANCEL_TEXT = "Alright, the operation was cancelled."
    END_TEXT = "Ok, back to the main menu"
    # scripts
    SCRIPTS_TEXT = "Here's a list of *all the scripts* you have saved"
    NO_SCRIPTS_TEXT = "You *don't* have any saved scripts!"
    SCRIPT_DONE_TEXT = "Finished execution of '{}' script!"
    # add to whitelist
    ADD_TO_WHITELIST_TEXT = "Write the *Telegram ID* of the user you want to *add* to the *whitelist*"
    USER_ALREADY_IN_WHITELIST_TEXT = "The specified user is *already in* the whitelist!"
    ADD_TO_WHITELIST_SUCCESS = "User {} *successfully* added to the whitelist!"
    # remove from whitelist
    NO_USERS_IN_WHITELIST_TEXT = "There *aren't* any users in the whitelist!"
    REMOVE_FROM_WHITELIST_TEXT = "Choose who you want to *remove* from the whitelist"
    REMOVE_FROM_WHITELIST_SUCCESS = "User {} *successfully* removed from the whitelist!"

    # KEYBOARDS
    OPTIONS_KEYBOARD = InlineKeyboardMarkup([
        [InlineKeyboardButton("add user ID to Whitelist", callback_data="addToWhitelist")],
        [InlineKeyboardButton("remove user ID from Whitelist", callback_data="removeFromWhitelist")],
        [InlineKeyboardButton("see all scripts", callback_data="seeAllScripts")],
        [InlineKeyboardButton("add script", callback_data="addScript"),
         InlineKeyboardButton("remove script", callback_data="removeScript")]
    ])
    CONFIRM_KEYBOARD = InlineKeyboardMarkup([
        [InlineKeyboardButton("confirm", callback_data="yes")],
        [InlineKeyboardButton("cancel", callback_data="no")]
    ])