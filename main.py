import telebot
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
from telebot import types
from collections import Counter

# Токен вашего бота
BOT_TOKEN = ""
bot = telebot.TeleBot(BOT_TOKEN)

JSON_FILE_NAME = "horoscopes.json"


sign_mapping = {
    'aries': 'Овен', 'taurus': 'Телец', 'gemini': 'Близнецы', 'cancer': 'Рак',
    'leo': 'Лев', 'virgo': 'Дева', 'libra': 'Весы', 'scorpio': 'Скорпион',
    'sagittarius': 'Стрелец', 'capricorn': 'Козерог', 'aquarius': 'Водолей', 'pisces': 'Рыбы'
}


def get_horoscope(sign, date=None):
    try:
        if date:
            url = f"https://horo.mail.ru/prediction/{sign}/{date}/" 
        else:
            url = f"https://horo.mail.ru/prediction/{sign}/today/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        main_element = soup.find("main", itemprop="articleBody")
        if main_element:
            paragraphs = main_element.find_all("p")
            if paragraphs:
                horoscope_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
                return horoscope_text
            else:
                return "Не удалось найти параграфы с текстом гороскопа."
        else:
            return "Не удалось найти основной элемент с гороскопом."
    except Exception as e:
        return f"Ошибка при запросе к horo.mail.ru: {e}"


def save_horoscope(chat_id, sign, horoscope_text):
    try:
        data = {}
        try:
            with open(JSON_FILE_NAME, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        key = f"{chat_id}_{date_now}"
        data[key] = {
            "chat_id": chat_id,
            "sign": sign,
            "horoscope": horoscope_text,
            "date_added": date_now
        }

        with open(JSON_FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Ошибка при записи в JSON файл: {e}")
        return False


def get_user_history(chat_id):
    try:
        with open(JSON_FILE_NAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
        history = [item for key, item in data.items() if item['chat_id'] == chat_id]
        return history
    except FileNotFoundError:
        return []


def clear_user_history(chat_id):
    try:
        with open(JSON_FILE_NAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return False

    new_data = {key: item for key, item in data.items() if item['chat_id'] != chat_id}

    with open(JSON_FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)
    return True


def get_zodiac_stats():
    try:
        with open(JSON_FILE_NAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
        signs = [item['sign'] for key, item in data.items()]
        sign_counts = Counter(signs)
        return sign_counts
    except FileNotFoundError:
        return {}


def get_user_sign(chat_id):
    history = get_user_history(chat_id)
    if history:
       
        return history[-1]['sign']
    return None


def send_horoscope_message(chat_id, sign, date=None):
    if sign is None:
        bot.send_message(chat_id, "Пожалуйста, сначала выберите свой знак зодиака. Используйте команду /set_sign")
        return

    russian_sign = sign_mapping.get(sign)
    if date:
      horoscope_text = get_horoscope(sign, date)
      date_str = datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%Y') 
      text = f"Гороскоп для {russian_sign} на {date_str}:\n\n{horoscope_text}"
    else:
      horoscope_text = get_horoscope(sign)
      text = f"Гороскоп для {russian_sign} на сегодня:\n\n{horoscope_text}"


    if horoscope_text:
        if save_horoscope(chat_id, sign, horoscope_text):
            bot.send_message(chat_id, text)
        else:
            bot.send_message(chat_id, text + "\n\nОшибка при сохранении в JSON файл.")
    else:
        bot.send_message(chat_id, "Не удалось получить гороскоп.")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот гороскопов. Чтобы узнать свой гороскоп, выберите знак зодиака с помощью команды /set_sign, а затем используйте команды /today или /tomorrow.")


@bot.message_handler(commands=['today', 'horoscope'])  
def send_today_horoscope(message):
    chat_id = message.chat.id
    sign = get_user_sign(chat_id)
    send_horoscope_message(chat_id, sign)


@bot.message_handler(commands=['tomorrow'])
def send_tomorrow_horoscope(message):
    chat_id = message.chat.id
    sign = get_user_sign(chat_id)
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d") 
    send_horoscope_message(chat_id, sign, tomorrow_str)


@bot.message_handler(commands=['history'])
def show_history(message):
    history = get_user_history(message.chat.id)
    if history:
        text = "Ваша история гороскопов:\n"
        for item in history:
            russian_sign = sign_mapping.get(item['sign'], item['sign'])
            text += f"- {russian_sign} ({item['date_added']})\n"
    else:
        text = "Ваша история гороскопов пуста."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['stats'])
def show_stats(message):
    stats = get_zodiac_stats()
    if stats:
        text = "Статистика по знакам зодиака:\n"
        for sign, count in stats.items():
            russian_sign = sign_mapping.get(sign, sign)
            text += f"- {russian_sign}: {count}\n"
    else:
        text = "Статистика пока недоступна."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['clearhistory'])
def clear_history(message):
    if clear_user_history(message.chat.id):
        text = "Ваша история гороскопов очищена."
    else:
        text = "Не удалось очистить историю гороскопов."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['set_sign'])
def set_sign(message):
    chat_id = message.chat.id
  
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)  
    buttons = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
    markup.add(*buttons)  
    bot.send_message(chat_id, "Выберите свой знак зодиака:", reply_markup=markup)


@bot.message_handler(func=lambda message: True) 
def handle_zodiac_choice(message):
    chat_id = message.chat.id
    sign_text = message.text


    if sign_text in sign_mapping.values():
        
        sign = next((k for k, v in sign_mapping.items() if v == sign_text), None)

        if sign:
            
            horoscope_text = get_horoscope(sign)
            save_horoscope(chat_id, sign, horoscope_text)

            bot.send_message(chat_id, f"Вы выбрали знак зодиака: {sign_text}.", reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(chat_id, "Теперь вы можете использовать команды /today и /tomorrow.")
        else:
            bot.send_message(chat_id, "Произошла ошибка при определении знака зодиака.")
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите знак зодиака из предложенной клавиатуры.")



bot.infinity_polling()
