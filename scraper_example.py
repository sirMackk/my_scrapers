import requests
import lxml.html
import csv

#TODO:
#- figure out using xpath instead of cssselect - tested out, both xpath and cssselect seem good
#- figure out using something else instead of requests - not really, seems the best option for now
#- work on better csv output &&|| on sqlite output - first work on first two problems

#url of file
url = 'http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm'
#gets html
page = requests.get(url)
#lxml uses html to create something, figure this out more
root = lxml.html.fromstring(page.content)
main_data = []
#lxml uses cssselect to get all table rows marked by tr
main_table = root.cssselect('tr')
#then iterate through that list and use cssselect to get td columns
for tr in main_table:
    tds = tr.cssselect('td')
#only append rows with 12 columns
    if len(tds) == 12:
#append a dictionary with data from columns to list
        main_data.append({'country':tds[0].text_content(), 
    'year':tds[1].text_content(), 
    'total':tds[4].text_content(), 
'men':tds[7].text_content(), 
'women':tds[10].text_content()})


print len(main_data)
#creates csv writer object called countries.csv
writer = csv.writer(open('countries.csv', 'wb'))
#writes the first row of the csv with the headers
writer.writerow(['Country', 'Year', 'Total', 'Men', 'Women'])
#iterates through data
for i in main_data:
#j becomes a list of all items for each dict object in the list
    j = i.items()
#csv writer writes rows based on previously created list
    writer.writerow([j[0][1].encode("utf8"), j[4][1], j[2][1], j[3][1], j[1][1]])
    


