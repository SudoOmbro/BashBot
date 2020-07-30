from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class Resources:

    """ this class contains all the text prompts and keyboards """
    # TODO add support for multiple languages

    # text
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
    SCRIPTS_TEXT = "Here's a list of *all the scripts* you have saved"
    NO_SCRIPTS_TEXT = "You *don't* have any saved scripts!"

    # keyboards
    OPTIONS_KEYBOARD = InlineKeyboardMarkup([
        [InlineKeyboardButton("add user ID to Whitelist", callback_data="addToWhitelist")],
        [InlineKeyboardButton("remove user ID from Whitelist", callback_data="removeFromWhitelist")],
        [InlineKeyboardButton("add script", callback_data="addScript")],
        [InlineKeyboardButton("remove script", callback_data="removeScript")]
    ])
    CONFIRM_KEYBOARD = InlineKeyboardMarkup([
        [InlineKeyboardButton("confirm", callback_data="yes")],
        [InlineKeyboardButton("cancel", callback_data="no")]
    ])