from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class Resources:

    """ this class contains all the text prompts and keyboards """
    # TODO add support for multiple languages

    # TEXTS
    # general
    START_TEXT = "Welcome to BashBot {}!\nUse /help to see all the commands and shortcuts"
    BASE_COMMANDS_TEXT = """
        *COMMANDS*
        /start - _shows bot welcome_.
        /help, /h - _shows commands_.
        /options - _lets you manage the bot_. (WIP)
        /download - _lets you download a file from the current folder_.
        /upload - _lets you upload a file to the current folder_.
        /scripts - _shows all the saved scripts_.
        """
    ACCESS_DENIED_TEXT = "You don't have access to this Bot"
    OPTIONS_TEXT = "Here's what *you* can do"
    CONFIRM_TEXT = "Are you sure?"
    CANCEL_TEXT = "Alright, the operation was cancelled."
    END_TEXT = "Ok, exited to shell input"
    # download
    DOWNLOAD_TEXT = "write the name of the file you want to download to your device"
    DOWNLOAD_FAILED = "Could not find the specified file"
    DOWNLOAD_SUCCESS = "Here's the requested file"
    # upload
    UPLOAD_TEXT = "Send the file you want to upload in the current folder"
    UPLOAD_FAILED = "*Upload failed!*"
    UPLOAD_SUCCESS = "*Upload successful!*"
    # scripts
    SCRIPTS_TEXT = "Here's a list of *all the scripts* you have saved, *click* on the one you want to use."
    NO_SCRIPTS_TEXT = "You *don't* have any saved scripts!"
    SCRIPT_DONE_TEXT = "Finished execution of '{}' script!"
    REMOVE_SCRIPT_TEXT = "Select which script you want to remove"
    SCRIPT_SUCCESSFULLY_REMOVED_TEXT = "Script '{}' successfully removed!"
    SCRIPT_SUCCESSFULLY_SAVED_TEXT = "The current script was *successfully saved*!"
    SCRIPTS_SHOW_ALL_TEXT = "Here's a list of all the saved scripts"
    # add to whitelist
    ADD_TO_WHITELIST_TEXT = "Write the *Telegram ID* of the user you want to *add* to the *whitelist*"
    USER_ALREADY_IN_WHITELIST_TEXT = "The specified user is *already in* the whitelist!"
    ADD_TO_WHITELIST_SUCCESS = "User {} *successfully* added to the whitelist!"
    USER_ID_VALUE_ERROR = "The user ID *must* be an integer!"
    # remove from whitelist
    NO_USERS_IN_WHITELIST_TEXT = "There *aren't* any users in the whitelist!"
    REMOVE_FROM_WHITELIST_TEXT = "Choose who you want to *remove* from the whitelist"
    REMOVE_FROM_WHITELIST_SUCCESS = "User {} *successfully* removed from the whitelist!"

    # KEYBOARDS
    OPTIONS_KEYBOARD = InlineKeyboardMarkup([
        [InlineKeyboardButton("add user ID to Whitelist", callback_data="addToWhitelist")],
        [InlineKeyboardButton("remove user ID from Whitelist", callback_data="removeFromWhitelist")],
        [InlineKeyboardButton("see all scripts", callback_data="seeAllScripts")],
        [InlineKeyboardButton("new script", callback_data="newScript"),
         InlineKeyboardButton("edit script", callback_data="editScript"),
         InlineKeyboardButton("remove script", callback_data="removeScript")],
        [InlineKeyboardButton("Back", callback_data="back")]
    ])
    CONFIRM_KEYBOARD = InlineKeyboardMarkup([
        [InlineKeyboardButton("confirm", callback_data="yes")],
        [InlineKeyboardButton("cancel", callback_data="no")]
    ])
    EDIT_SCRIPT_KEYBOARD = InlineKeyboardMarkup([
        [InlineKeyboardButton("change title", callback_data="change_name"),
         InlineKeyboardButton("change description", callback_data="change_description")],
        [InlineKeyboardButton("change body", callback_data="change_body")],
        [InlineKeyboardButton("toggle verbose", callback_data="toggleVerbose")],
        [InlineKeyboardButton("save", callback_data="save"),
         InlineKeyboardButton("Back", callback_data="back")]
    ])
