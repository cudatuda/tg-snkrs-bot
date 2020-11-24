import requests
from bs4 import BeautifulSoup
import telebot
import json


def get_link(URL, SIZE_LIST=""):
    print("Generating...")
    links = []
    try:
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        productId = soup.find('meta', {"name": "branch:deeplink:productId"})['content']
        for size in SIZE_LIST:
            link = f'{URL}/?productId={productId}&size={size}'
            links.append(link)

        return links
    except:
        return "Error"


with open('./data.json') as f:
    TOKEN = json.load(f)["TOKEN"]

bot = telebot.TeleBot(TOKEN)

global url
url = ""


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Привет, я генерирую ранние ссылки на SNKRS.'
                                      '\n'
                                      '1. Отправь ссылку на желаемую пару\n'
                                      '2. Укажи нужный размер (us)\n'
                                      '--Если хочешь взять разные размеры, '
                                      'отправь их одной строкой через пробелы\n'
                                      '3. Готово!')


@bot.message_handler(content_types=['text'])
def text_handler(message):
    global url
    text = message.text.lower()
    chat_id = message.chat.id

    if str(text).startswith('https://www.nike.com/ru/launch/t/'):
        url = text
        bot.send_message(chat_id, 'Укажите размер (us)')

    if url != '':

        sizes = str(text).split()
        for size_ in sizes:
            try:
                int(size_)
            except:
                try:
                    float(size_)
                except:
                    return
        bot.send_message(chat_id, 'Генерирую...')
        for link in get_link(url, sizes):
            bot.send_message(chat_id, link)

    else:
        print(text)
        bot.send_message(chat_id, 'Неизвестная команда\nсправка - /start')


bot.polling()
