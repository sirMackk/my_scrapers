# scraper for startups wiki in ireland

import requests
from lxml import html
root_url = 'http://startupwiki.ie'
url = 'http://startupwiki.ie/wiki/Category:Startups'

index = requests.get(url)

tree = html.fromstring(index.text)
main_index = tree.xpath('//div[@class="mw-content-ltr"]//ul/li/a/attribute::href')
print len(main_index)
print main_index[0]
info = []

for i in main_index:
    r = requests.get(root_url + i)
    tree = html.fromstring(r.text)
    print i

    name = tree.xpath('//h1[@id="firstHeading"]/span/text()')
    url = tree.xpath('//div[@id="mw-content-text"]/table[1]//tr[3]/td/a/text()')
    location = tree.xpath('//div[@id="mw-content-text"]/table[1]//tr[4]/td/text()')
    desc = tree.xpath('//div[@id="mw-content-text"]/h3[3]/following::p[1]/text()')

    info.append([name, url, location, desc])

f = open('startups.csv', 'wb')
for i in info:
    try:
        f.write('%s,%s,%s,%s\n', i[0], i[1], i[2], [3])
    except IOError:
        print 'dat error in io'
if f:
    f.close()