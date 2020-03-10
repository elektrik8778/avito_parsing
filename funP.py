#файл, содержащий функции, которые используются в основной программе
import requests
from bs4 import BeautifulSoup
from time import sleep
from openpyxl import Workbook
import sqlite3
import time
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
# import telepot   # Importing the telepot library
# from telepot.loop import MessageLoop    # Library function to communicate with telegram bot
# import datetime  # Importing the datetime library




# data = ()
#
# con = sqlite3.connect('test.db')
# cur = con.cursor()
# cur.execute("DROP TABLE IF EXISTS kvr")
# cur.execute("CREATE TABLE kvr(title text, price INT, tipe text, adress text, time text, href text, tel text)")
# cur.executemany("INSERT INTO kvr VALUES(?,?,?,?,?,?,?)",data)
#
# con.commit()


# # Вставляем множество данных в таблицу используя безопасный метод "?"
# albums = [('Exodus', 'Andy Hunter', '7/9/2002', 'Sparrow Records', 'CD'),
#           ('Until We Have Faces', 'Red', '2/1/2011', 'Essential Records', 'CD'),
#           ('The End is Where We Begin', 'Thousand Foot Krutch', '4/17/2012', 'TFKmusic', 'CD'),
#           ('The Good Life', 'Trip Lee', '4/10/2012', 'Reach Records', 'CD')]
#
# cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?)", albums)
# conn.commit()





headers_m = {
    "User-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36"
}
# BASE_URL = 'https://www.avito.ru/amurskaya_oblast_blagoveschensk/kvartiry'

BASE_URL = 'avito.ru/amurskaya_oblast_blagoveschensk/kvartiry'
prefiks_norm = 'https://www.'
prefiks_mob = 'https://m.avito.ru'
kvartiry = []
fons = []
lenght_page=[]
global annaouncement
annaouncement = 0
#-------------------------------------------------------------------
#   функция получения ответа на запрос
def get_html(url, headers):
    session = requests.Session()
    request = session.get(url, headers=headers)
    return request.content
#-------------------------------------------------------------------
#   функция получения количества страниц с объявлениями
def get_page_count(html):
    soup = BeautifulSoup(html, "html.parser")
    paggination = soup.find('div', attrs={"class":'pagination-pages clearfix'})
    h = paggination.find_all('a', href=True)[-1]['href'][-2:]             # основаная строка для парсинга количества страниц
    return int(h)

#-------------------------------------------------------------------
# парсинг мобильной версии сайта
def get_fon(url, headers, fons):
    h = requests.get(url, headers=headers)
    soup = BeautifulSoup(h.text, "html.parser")
    fon = soup.find('div', class_='_3vWKQ').find('a')['href'][6:]
    fons.append((fon))
    # sleep(0)
    return fon
#-------------------------------------------------------------------
# основной парсинг
def parse(html, data):
    global annaouncement
    annaouncement = 0
    soup = BeautifulSoup(html, "html.parser")
    work_item = soup.find_all('div', attrs = {'class':'item item_table clearfix js-catalog-item-enum item-with-contact js-item-extended'})
    lenght_page.append(len(work_item))
    count = 1

    for div in work_item:
        annaouncement +=1
        print('Обработано '+str(len(data)+1)+' объявлениий')
        try:
            id = div['id']
        except:
            id = '-'

        # dikt = {
        #     'title':title,
        #     'price':price,
        #     'tipe':tipe,
        #     'adress':adress,
        #     'time':time_,
        #     'href':href,
        #     'tel':'8'+str(fon),
        # }
        temp = (
            id,

        )
        data.append(temp)
        # print(data)
        # sleep(1)
        # if annaouncement == 5:
        #     break
        # except:
        #     print('error1')
    # count += 1
    # print('парсинг',count)

    return data
#-------------------------------------------------------------------
def save_allxl(path, data):

    wb = Workbook()
    ws = wb.active
    for row in data:
        ws.append(row)

    wb.save(path)
#-------------------------------------------------------------------


#-------------------------------------------------------------------


#-------------------------------------------------------------------
#


