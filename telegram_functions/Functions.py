from telegram import TelegramError


def send_message_safe(update, context, text):
    try:
        context.bot.send_message(
            chat_id=update.message.chat.id,
            text=text
        )
    except TelegramError as e:
        print("can't send the message")
        print(e)


def send_message(update, context, text):
    context.bot.send_message(
        chat_id=update.message.chat.id,
        text=text
    )
