from telegram import TelegramError, InlineKeyboardMarkup, ParseMode, InlineKeyboardButton


def send_message(update, context, text, parse_mode=None, keyboard=None):
    """ safe and short way of sending a message to a user """
    try:
        context.bot.send_message(
            chat_id=update.message.chat.id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=keyboard
        )
    except TelegramError as e:
        print("can't send the message")
        print(e)


def get_inline_keyboard_from_string_list(input_list, columns=1):
    """ creates an inline keyboard from a list of strings, the callback data of the buttons is
    the string that is on the button itself. Optionally the number of columns can be set, by default it's 1"""
    button_list = []
    for element in input_list:
        row = []
        for i in range(columns):
            row.append(InlineKeyboardButton(element, callback_data="element"))
        button_list.append(row)
    return InlineKeyboardMarkup(button_list)


def delete_callback_message(update, context):
    """ safe and short way of deleting a message from callback """
    try:
        context.bot.delete_message(chat_id=update.effective_user.id,
                                   message_id=update.callback_query.message.message_id
                                   )
    except TelegramError:
        print("The message is too old to be deleted.")
