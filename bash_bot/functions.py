from telegram import TelegramError, InlineKeyboardMarkup, ParseMode, InlineKeyboardButton
from telegram.error import BadRequest


def send_message(update, context, text, parse_mode=None, keyboard=None, file=None):
    """ safe and short way of sending a message to a user """
    if file is None:
        try:
            context.bot.send_message(
                chat_id=update.effective_user.id,
                text=text,
                parse_mode=parse_mode,
                reply_markup=keyboard,
            )
        except TelegramError as e:
            print("can't send the message")
            print(e)
        except BadRequest as e:
            print("bad request")
            print(e)
    else:
        try:
            context.bot.send_document(
                chat_id=update.effective_user.id,
                caption=text,
                parse_mode=parse_mode,
                document=file,
            )
        except TelegramError as e:
            print("can't send the message")
            print(e)
        except BadRequest as e:
            print("bad request")
            print(e)


def get_inline_keyboard_from_string_list(input_list):
    """ creates an inline keyboard from a list of strings, the callback data of the buttons is
    the string that is on the button itself. """
    button_list = []
    for element in input_list:
        button_list.append([InlineKeyboardButton(element, callback_data=element)])
    return InlineKeyboardMarkup(button_list)


def get_inline_keyboard_from_script_list(script_list):
    button_list = []
    for script in script_list:
        name = script.name
        button_list.append([InlineKeyboardButton(name, callback_data=name)])
    return InlineKeyboardMarkup(button_list)


def delete_callback_message(update, context):
    """ safe and short way of deleting a message from callback """
    try:
        context.bot.delete_message(chat_id=update.effective_user.id,
                                   message_id=update.callback_query.message.message_id
                                   )
    except TelegramError:
        print("The message is too old to be deleted.")
    except BadRequest as e:
        print(e)
