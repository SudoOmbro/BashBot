from telegram import TelegramError, InlineKeyboardMarkup, ParseMode


def send_message(update, context, text, parse_mode=None):
    """ safe and short way of sending a message to a user """
    try:
        context.bot.send_message(
            chat_id=update.message.chat.id,
            text=text,
            parse_mode=parse_mode
        )
    except TelegramError as e:
        print("can't send the message")
        print(e)


def send_message_ik(update, context, text, keyboard):  # send message with inline keyboard
    """ safe and short way of sending a message with keyboard to a user """
    try:
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        print("can't send the message")
        print(e)


def delete_callback_message(update, context):
    """ safe and short way of deleting a message from callback """
    try:
        context.bot.delete_message(chat_id=update.effective_user.id,
                                   message_id=update.callback_query.message.message_id
                                   )
    except TelegramError:
        print("The message is too old to be deleted.")
