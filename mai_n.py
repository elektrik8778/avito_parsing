import fun
# import sqlite3
headers_n = {"accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            "user-agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
}



BASE_URL = 'avito.ru/amurskaya_oblast_blagoveschensk/kvartiry'
prefiks_norm = 'https://www.'


data = []



total_pages_words = fun.get_page_count(fun.get_html(prefiks_norm+BASE_URL, headers_n))
print('Всего найдено %d страниц...' % total_pages_words)




con = fun.sqlite3.connect('test.db')
cur = con.cursor()
con.execute("DROP TABLE IF EXISTS kvr")
con.execute("CREATE TABLE kvr(title text, price INT, tipe text, adress text, time text, href text, tel text)")

for page in range(1,total_pages_words):

    url = str(prefiks_norm+BASE_URL + "?p=%d" % page)
    fun.parse(fun.get_html(url, headers_n),data)
    print("Жду 5 сек")
    fun.sleep(10)
cur.executemany("INSERT INTO kvr VALUES(?,?,?,?,?,?,?)",data)
fun.save_allxl("kv.xlsx", data)
con.commit()
con.close()
