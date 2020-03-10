#файл, содержащий функции, которые используются в основной программе
import requests
from bs4 import BeautifulSoup
from time import sleep
from openpyxl import Workbook
import datetime
import sqlite3
import random
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
def parse_date(item: str):
    params = item.strip().split(' ')
    # print(params)
    if len(params) == 2:
        day, time = params
        if day == 'Сегодня':
            date = datetime.date.today()
            # print(date)
        elif day == 'Вчера':
            date = datetime.date.today() - datetime.timedelta(days=1)
        else:
            print('Не смогли разобрать день:', item)
            return

        time = datetime.datetime.strptime(time, '%H:%M').time()
        # print(time)
        t = str(date)+' '+str(time)
        return t
        # return datetime.datetime.combine(date=date, time=time)

    elif len(params) == 3:
        day, month_hru, time = params
        day = int(day)
        months_map = {
            'января': 1,
            'февраля': 2,
            'марта': 3,
            'апреля': 4,
            'мая': 5,
            'июня': 6,
            'июля': 7,
            'августа': 8,
            'сентября': 9,
            'октября': 10,
            'ноября': 11,
            'декабря': 12,
        }
        month = months_map.get(month_hru)
        if not month:
            print('Не смогли разобрать месяц:', item)
            return

        today = datetime.datetime.today()
        time = datetime.datetime.strptime(time, '%H:%M')
        return datetime.datetime(day=day, month=month, year=today.year, hour=time.hour, minute=time.minute)

    else:
        print('Не смогли разобрать формат:', item)
        return

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
    soup = BeautifulSoup(html, "lxml")
    work_item = soup.find_all('div', attrs = {'class':'item_table-wrapper'})
    lenght_page.append(len(work_item))
    count = 1

    for div in work_item:
        annaouncement +=1
        print('Обработано '+str(len(data)+1)+' объявлениий')
        try:
            title = div.find('a', attrs={"class": "snippet-link"})['title']
            # title_block = div.select_one('a.snippet-link')
            # title = title_block.get('title')



        except:
            title = '-'
        try:
            price_block = div.find('span', attrs={"class": "snippet-price"})#.text.strip()#['content']

            # price_block = div.select_one('span.snippet-price snippet-price-vas')
            price_block = price_block.get_text('\n')
            price_block = list(filter(None, map(lambda i: i.strip(), price_block.split('\n'))))
            if len(price_block) == 2:
                price, currency = price_block
            elif len(price_block) == 1:
                # Бесплатно
                price, currency = 0, None
            else:
                price, currency = price_block[0], str(price_block[1]) + ' ' + str(price_block[2])
                # print(f'Что-то пошло не так при поиске цены: {price_block}, {href}')

        except:
            price = '-'
        try:
            tipe = div.find('div', attrs={"class": "data"}).text.strip()
            tipe.replace("\n", "")

        except:
            tipe = '-'
        try:
            adress = div.find('span', attrs={"class":"item-address__string"}).text.strip()

        except:
            adress = '-'
        try:
            # date = None
            # date_block = div.select_one('div.snippet-date-info')
            # absolute_date = date_block.get('data-absolute-date')
            # if absolute_date:
            #     date = parse_date(item=absolute_date)


            date = parse_date(div.find('div', attrs={"class": "snippet-date-info"}).text.strip())
        except:
            date = '-'
        try:
            href = div.find('a', attrs={"class":"snippet-link"})['href']
        except:
            href = '-'
        try:
            t=href[-10:]
            response = requests.get(
                f'https://m.avito.ru/api/1/items/{t}/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir')
            # print(t, '+7' + str(response.text)[-14:-4])
            fon = '+7' + str(response.text)[-14:-4]
        except:
            fon = '-'
        # fon = '-'
        # dikt = {
        #     'title':title,
        #     'price':price,
        #     'tipe':tipe,
        #     'adress':adress,
        #     'time':date,
        #     'href':href,
        #     'tel':'8'+str(fon),
        # }
        temp = (
            title,
            price,
            tipe,
            adress,
            date,
            'https://www.avito.ru'+str(href),
            fon,
        )
        data.append(temp)
        # print(temp)
        sleep(random.randint(1,3))
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
#


