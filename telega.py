import datetime  # Importing the datetime library
import telepot   # Importing the telepot library
from telepot.loop import MessageLoop    # Library function to communicate with telegram bot

from time import sleep      # Importing the time library to provide the delays in program
import sqlite3




now = datetime.datetime.now() # Getting date and time


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
        bot.sendMessage(chat_id, str(results))
        for i in results:
            bot.sendMessage(chat_id, str("Адрес: ")+str(i)[2:-3])
            for n in i:
                bot.sendMessage(chat_id, str(n))
                
            bot.sendMessage(chat_id, str("--------------------"))
    else:
        while True:
            bot.sendMessage(chat_id, str("Не знаю такой команды"))
            sleep(5)
    con.close()
# Insert your telegram token below

# telepot.api.set_proxy('http://154.0.15.166:46547')
#telepot.api.set_proxy('http://192.162.62.197:59246')
# telepot.api.set_proxy('http://173.242.95.77:36179')

# bot = telepot.Bot('961615492:AAFJFbnW8MwjKyexl47qxiOabUGUJLOcvuo')#MakerPol
bot = telepot.Bot('1058012960:AAGSTw7XQlPzPUell83cjQXBXZt2kuDzw6Q')#KvantoBot
print (bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print ('Listening....')

while 1:
    sleep(10)

