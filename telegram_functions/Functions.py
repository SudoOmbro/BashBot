from telegram import TelegramError


def send_message(update, context, text):
    try:
        context.bot.send_message(
            chat_id=update.message.chat.id,
            text=text.decode("utf-8")
        )
    except TelegramError as e:
        print("can't send the message")
        print(e)
