import sqlite3
from lxml import html
import requests

con = sqlite3.connect('liberated_data.db')
cursor = con.cursor()
cursor.execute('DROP TABLE IF EXISTS data;')
cursor.execute('CREATE TABLE data (id integer primary key, item text, quantity integer, stock integer, price integer)')
con.commit()

i = 1
while 1:
    page = requests.get('https://s3.amazonaws.com/codecave/data%d.html' % i)
    if not page:
        break
    tree = html.fromstring(page.text)
    j = 1
    while 1:
        row = tree.xpath('//tr[%d]/td/text()' % j)
        if not row:
            break
        cursor.execute('INSERT INTO DATA (item, quantity, stock, price) VALUES (?, ?, ?, ?)', (row[0], row[1],row[2], row[3]))
        print row
        j += 1
    i += 1
con.commit()
con.close()

