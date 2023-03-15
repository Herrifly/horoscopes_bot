import telebot
from config import BOT_TOKEN
import sqlite3
from telebot import types

bot = telebot.TeleBot(BOT_TOKEN)
conn = sqlite3.connect('db/database_zodiak.db', check_same_thread=False)
cursor = conn.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.send_message(message.chat.id, "Чтобы узнать гороскоп, для начала напишите /help и выберите свой знак зодиака",
                     parse_mode='html')

    us_id = message.from_user.id
    us_name = message.from_user.first_name

    db_table_val(user_id=us_id, user_name=us_name)


def db_table_val(user_id: int, user_name: str):
    cursor.execute('INSERT INTO zodiaks (user_id, user_name) VALUES (?, ?)',
                   (user_id, user_name))
    conn.commit()


def db_table_zodiak(user_id: int, user_zodiak: str):
    cursor.execute('UPDATE "zodiaks"  SET "user_zodiak" = ? WHERE "user_id" = ? ',
                   (user_zodiak, user_id))
    conn.commit()


@bot.message_handler(commands=['help'])
def choice_zodiac(message):
    markup = types.InlineKeyboardMarkup(row_width=3)

    aries = types.InlineKeyboardButton(text='Овен', callback_data="aries")
    taurus = types.InlineKeyboardButton(text='Телец', callback_data="taurus")
    gemini = types.InlineKeyboardButton(text='Близнецы', callback_data="gemini")
    cancer = types.InlineKeyboardButton(text='Рак', callback_data="cancer")
    leo = types.InlineKeyboardButton(text='Лев', callback_data="leo")
    virgo = types.InlineKeyboardButton(text='Дева', callback_data="virgo")
    libra = types.InlineKeyboardButton(text='Весы', callback_data="libra")
    scorpio = types.InlineKeyboardButton(text='Скорпион', callback_data="scorpio")
    sagittarius = types.InlineKeyboardButton(text='Стрелец', callback_data="sagittarius")
    capricorn = types.InlineKeyboardButton(text='Козерог', callback_data="capricorn")
    aquarius = types.InlineKeyboardButton(text='Водолей', callback_data="aquarius")
    pisces = types.InlineKeyboardButton(text='Рыбы', callback_data="pisces")

    markup.add(aries,
               taurus,
               gemini,
               cancer,
               leo,
               virgo,
               libra,
               scorpio,
               sagittarius,
               capricorn,
               aquarius,
               pisces)

    bot.send_message(message.chat.id, 'Выберите знак зодиака', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.message:
        if call.data == 'today' or call.data == 'yesterday' or call.data == 'tomorrow' or call.data == 'week' or call.data == 'month' or call.data == 'year':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,

                                  text="Отлично, секунду, делаю запрос во вселенную")
            for value in cursor.execute(f'SELECT user_zodiak FROM zodiaks WHERE user_id == {call.from_user.id}'):
                user_zodiak = value[0]

            for value2 in cursor.execute(f"SELECT {call.data} FROM horoscopes WHERE zodiak == '{user_zodiak}' "):
                text = value2

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text)
        elif call.data:
            us_id = call.from_user.id
            us_zodiak = call.data
            db_table_zodiak(us_id, us_zodiak)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Отлично, теперь я знаю твой знак зодиака")
            bot.send_message(chat_id=call.message.chat.id, text="Чтобы выбрать день для прогноза нажми /prognoz",
                             parse_mode='html')


@bot.message_handler(commands=['prognoz'])
def prognoz(message):
    markup = types.InlineKeyboardMarkup(row_width=3)

    yesterday = types.InlineKeyboardButton(text='Вчера', callback_data='yesterday')
    day = types.InlineKeyboardButton(text='Сегодня', callback_data='today')
    tomorrow = types.InlineKeyboardButton(text='Завтра', callback_data='tomorrow')
    week = types.InlineKeyboardButton(text='На неделю', callback_data='week')
    month = types.InlineKeyboardButton(text='Месяц', callback_data='month')
    year = types.InlineKeyboardButton(text='Год', callback_data='year')

    markup.add(yesterday,
               day,
               tomorrow,
               week,
               month,
               year)

    bot.send_message(message.chat.id, 'Выберите временной промежуток', reply_markup=markup)


bot.infinity_polling()