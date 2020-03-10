import requests

import  fun

con = fun.sqlite3.connect('test.db')
cur = con.cursor()
sql = "SELECT * FROM kvr"
cur.execute(sql)
rows = cur.fetchall()
c=0
for i in rows:
    c+=1
    if c==5:
        break
    t=i[5][-10:]
    response = requests.get(
        f'https://m.avito.ru/api/1/items/{t}/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir')
    print(t,'+7'+str(response.text)[-14:-4])

# print(sql)
con.commit()
con.close()

