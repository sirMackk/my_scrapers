
from lxml import html
import requests

page = requests.get('http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm')

tree = html.fromstring(page.text)

country = tree.xpath('//table[2]//table[2]//table/tr[position()>4]/td[1]/child::text()')
year = tree.xpath('//table[2]//table[2]//table/tr[position()>4]/td[2]/child::text()')
total = tree.xpath('//table[2]//table[2]//table/tr[position()>4]/td[5]/child::text()')
men = tree.xpath('//table[2]//table[2]//table/tr[position()>4]/td[8]/child::text()')
women = tree.xpath('//table[2]//table[2]//table/tr[position()>4]/td[11]/child::text()')

sum = []
for i in xrange(len(total)):
    sum.append({'country':country[i], 'year':year[i], 'total':total[i], 'men':men[i], 'women':women[i]})



