import csv
import requests
from lxml import html 
from time import clock

#This script gets querries the CORDIS database and scrapes the name (acronym), title, research area
#and start date of all 18000k+ projects from the databse and writes them to a CSV file. I decided
#to seperate the first iteration as this makes it easier for the scraper to browse through the pages
#due to how the navigation is structured. Also note that some minor pieces of information are missing
#from the research area column because CORDIS breaks it into different lines. There is also one project 
#missing because it did not have an acronym. It also omits the project start date as this data was
#inconcistent throughout the records - these functions are commented out in the code below.
#NOTE: This scraper stores all the data in ram until it is to be writtens, it's easy to make
#this scraper write the file as it scrapes to reduce the ram footprint, but this probably will
#increase disk IO times.

url = 'http://cordis.europa.eu/fetch?CALLER=FP7_PROJ_EN&USR_SORT=EN_QVD+CHAR+DESC&DOC=1&QUERY=013bdef6678b:ebcb:2328b071'
start = clock()
page = requests.get(url)
tree = html.fromstring(page.text)

name = tree.xpath('//div[@id="PResults"]/dl/dt/a/text()')
title = tree.xpath('//div[@id="PResults"]/dl/dd[1]/text()')
r_area = tree.xpath('//div[@id="PResults"]/dl/dd[2]/text()')
#p_date = tree.xpath('//div[@id="PResults"]/dl/dd[3]/span/child::text()')


next = tree.xpath('//p[@class="PNav"]/a/attribute::href')[0].replace('../', url[:24])

while 1:
    print '.',
    page = requests.get(next)
    tree = html.fromstring(page.text)

    name += tree.xpath('//div[@id="PResults"]/dl/dt/a/text()')
    title += tree.xpath('//div[@id="PResults"]/dl/dd[1]/text()[1]')
    r_area += tree.xpath('//div[@id="PResults"]/dl/dd[2]/text()')
  #  p_date += tree.xpath('//div[@id="PResults"]/dl/dd[3]/span/child::text()')

    try:
        next = tree.xpath('//p[@class="PNav"]/a/attribute::href')[1].replace('../', url[:24])
    except IndexError:
        print 'Scraping Completed'
        break

writer = csv.writer(open('CORDIS.csv', 'wb'))

writer.writerow(['ACRONYM', 'TITLE', 'RESEARCH AREA'])
print 'writing csv'

size = len(name)
for i in xrange(size):
    #writer.writerow([name[i].encode("utf8"), title[i].encode("utf8"), r_area[i].encode("utf8"), p_date[i]])
    writer.writerow([name[i].encode("utf8"), title[i].encode("utf8"), r_area[i].encode("utf8")])
print clock() - start

