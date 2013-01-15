# coding: utf-8
import requests
from lxml import html

kaczor = 0.0
tusk = 0.0
words = 0.0
def get_art(link):
    strona = requests.get(link)
    drzewko = html.fromstring(strona.text)
    art = drzewko.xpath('//div[@id="artykul"]/text()')

    return art

def searchk(s):
    global kaczor
    global tusk
    for i in s:
        if i == u'kaczyński':
            kaczor += 1
    for i in s:
        if i == u'tusk':
            tusk += 1
    for i in s:
        if i == u'kaczyńskiego':
            kaczor += 1
    for i in s:
        if i == u'tuska':
            tusk += 1
#xrange defines number and range of pages to scrape
for i in xrange(1, 6):
    print 'page %d' % i

    page = requests.get('http://wiadomosci.gazeta.pl/wiadomosci/0,114884.html?str=%d_10103403' % i)
    print 'request succeeded'
    tree = html.fromstring(page.text)
    links = tree.xpath('//div[@class="wrap wrap_0"]/h3/a/attribute::href')
    print 'links obtained %d' % len(links)


    for i in links:
        a = get_art(i)
        a = u''.join(a).strip().lower()
        a = a.split(' ')
        print 'Number of words in article: ', len(a)
        words += len(a)
        searchk(a)

print 'Kaczyński: %d' % kaczor
print 'Tusk: %d' % tusk
print 'Total # of words: %d' % words



