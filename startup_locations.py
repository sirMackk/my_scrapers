import requests
from lxml import html
import threading
import Queue

class Worker(threading.Thread):

    def __init__(self, queue, root):
        threading.Thread.__init__(self)
        self.queue = queue
        self.root = root

    def run(self):
        global info
        while 1:
            try:
                url = self.root + self.queue.get()
                print url + '\n'
                r = requests.get(url)
                tree = html.fromstring(r.text)

                tmp = []
                #name
                tmp.append(tree.xpath('//h1[@id="firstHeading"]/span/text()'))
                #url
                tmp.append(tree.xpath('//div[@id="mw-content-text"]/table[1]//tr[3]/td/a/text()'))
                #location
                tmp.append(tree.xpath('//div[@id="mw-content-text"]/table[1]//tr[4]/td/text()'))
                #description
                tmp.append(tree.xpath('//div[@id="mw-content-text"]/h3[3]/following::p[1]/text()'))

                tmp = ['-' if not i else i for i in[j[0].strip().encode('utf-8').replace(',', ' ') if j else '-' for j in tmp]]
                #this isnt needed since appending to lists cant invoke race conditions
                #but it's really cool
                lock.acquire()
                info.append(tmp)
                lock.release()
                self.queue.task_done()
            except Queue.Empty:
                break

root_url = 'http://startupwiki.ie'
url = 'http://startupwiki.ie/wiki/Category:Startups'

index = requests.get(url)

tree = html.fromstring(index.text)
main_index = tree.xpath('//div[@class="mw-content-ltr"]//ul/li/a/attribute::href')
print "Startups: %d" % len(main_index)
info = []
lock = threading.Lock()

queue = Queue.Queue()

for i in xrange(7):
    bee = Worker(queue, root_url)
    bee.setDaemon(True)
    bee.start()

for startup in main_index:
    queue.put(startup)

queue.join()



f = open('startups.csv', 'wb')
for i in info:
    try:
        f.write('%s,%s,%s,%s\n' % (i[0], i[1], i[2], i[3]))
    except IOError:
        print 'dat error in io'
if f:
    f.close()