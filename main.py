import telebot
from config import TOKEN
from utils import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду бота в следующем формате: \n' \
           '<Имя валюты> ' \
           '<в какую валюту перевести> ' \
           '<количество переводимой валюты>\n' \
           'Список доступных валют доступен по команде: /values'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        val = message.text.lower().split(' ')

        if len(val) != 3:
            raise ConvertionException('Некорректное количество параметров.')

        base, symbols, amount = val
        total_result = CurrencyConverter.convert(base, symbols, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {base} в {symbols} - {total_result * float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()
