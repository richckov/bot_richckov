from telebot import TeleBot
from telebot import types

token = '6906833006:AAEdQxcs7U6DUhxYkHFpWjWx4CHBt3aSWQs'
bot = TeleBot(token=token)
channel_username = -1002154053875  # Укажите имя вашего канала


@bot.message_handler(commands=['start'])
def start_message(message):
    welcome_message = (
        "Здесь Вы можете оставить отзыв о работе Евгения.\n"
        "Напишите отзыв и он опубликуется на канале!\n"
        "С примерами отзывов вы можете ознакомиться @karmanniy_repetitor"
    )
    hello = bot.send_message(
        message.chat.id,
        text=welcome_message
    )
    # После отправки стартового сообщения следующий шаг будет check_msg
    bot.register_next_step_handler(hello, check_msg)


def check_msg(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_button = types.KeyboardButton('Опубликовать отзыв')
    rewrite_button = types.KeyboardButton('Переписать')

    markup.add(yes_button, rewrite_button)

    check = bot.send_message(
        message.chat.id,
        text=f"Ваш отзыв:\n{message.text}\n\nВы хотите опубликовать его или переписать?",
        reply_markup=markup
    )

    bot.register_next_step_handler(check, handle_confirmation, message.text)


def handle_confirmation(message, review_text):
    if message.text == 'Опубликовать отзыв':
        # Сперва проверяем подписку на канал
        if is_user_subscribed(message.chat.id):
            send_msg_to_channel(message, review_text)
        else:
            bot.send_message(
                message.chat.id,
                "Вы должны быть подписчиком закрытого канала, чтобы оставить отзыв. Обратитесь к Евгению."
            )
    elif message.text == 'Переписать':
        bot.send_message(
            message.chat.id,
            "Пожалуйста, напишите ваш новый отзыв."
        )
        bot.register_next_step_handler(message, check_msg)
    else:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, выберите опцию 'Опубликовать отзыв' или 'Переписать'."
        )
        bot.register_next_step_handler(message, handle_confirmation, review_text)


def send_msg_to_channel(message, review_text):
    bot.send_message(-1001960128084, review_text)
    bot.send_message(message.chat.id, "Ваш отзыв успешно опубликован на канале @karmanniy_repetitor!")


def is_user_subscribed(user_id):
    # Проверка статуса пользователя на наличие подписки на канал
    try:
        chat_member = bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        # Cтатусы 'member', 'administrator' и 'creator' обозначают, что пользователь подписан на канал
        if chat_member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}\nОбпатитесь к Евгению @richckov")
    return False


if __name__ == '__main__':
    bot.polling()
