import datetime  # Importing the datetime library
import funP
import telepot   # Importing the telepot library
from telepot.loop import MessageLoop    # Library function to communicate with telegram bot

from time import sleep      # Importing the time library to provide the delays in program
import sqlite3

headers_n = {"accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            "user-agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

BASE_URL = 'https://www.avito.ru/amurskaya_oblast_blagoveschensk/kvartiry'
data = []
total_pages_words = funP.get_page_count(funP.get_html(BASE_URL, headers_n))
print('Всего найдено %d страниц...' % total_pages_words)
now = datetime.datetime.now() # Getting date and time
for page in range(total_pages_words-80):
    url = str(BASE_URL + "?p=%d" % page)
    funP.parse(funP.get_html(url, headers_n), data)
print(data)
def handle(msg):
    chat_id = msg['chat']['id'] # Receiving the message from telegram
    command = msg['text']   # Getting text from the message
    con = sqlite3.connect('test.db')
    cur = con.cursor()

    cur.execute("SELECT * FROM kvr")

    # Получаем результат сделанного запроса
    results = cur.fetchall()


    print(results)  # [('A Cor Do Som',), ('Aaron Copland & London Symphony Orchestra',), ('Aaron Goldberg',)]


    print ('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/привет':
        bot.sendMessage (chat_id, str("Привет! Алексей"))
    elif command == '/time':
        bot.sendMessage(chat_id, str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/date':
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    elif command == '/red_1':
        bot.sendMessage(chat_id, str("Red led is ON"))
        # GPIO.output(red_led_pin, True)

    elif command == '/red_0':
        bot.sendMessage(chat_id, str("Red led is OFF"))

        # GPIO.output(red_led_pin, False)
    elif command == '/green_1':
        bot.sendMessage(chat_id, str("Green led is ON"))
        # GPIO.output(green_led_pin, True)
    elif command == '/green_0':
        bot.sendMessage(chat_id, str("Green led is OFF"))
        # GPIO.output(green_led_pin, False)
    elif command == '/?':
        bot.sendMessage(chat_id, str("--------------------"))
        # bot.sendMessage(chat_id, str(results))
        for i in results:
            bot.sendMessage(chat_id, str("Адрес: ")+str(i)[2:-3])
            # for n in i:
            #     bot.sendMessage(chat_id, str(n))
                
            bot.sendMessage(chat_id, str("--------------------"))
    else:
        for i in data:
            bot.sendMessage(chat_id, str(i[0]))
            sleep(5)
    con.close()

bot = telepot.Bot('961615492:AAFJFbnW8MwjKyexl47qxiOabUGUJLOcvuo')#MakerPol
# bot = telepot.Bot('1058012960:AAGSTw7XQlPzPUell83cjQXBXZt2kuDzw6Q')#KvantoBot
print (bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print ('Listening....')

while 1:
    sleep(10)

