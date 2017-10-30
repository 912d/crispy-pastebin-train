#!/user/bin/python2.7
import urllib2
import urllib
import MySQLdb
from lxml import etree
import json
from pprint import pprint

class pastebinScraper():
    #Class Variables

    def list_trending(self):
        #list Trending Pastes, max of 18 results allowed:
        # api_option = 'trends'
        # data = {'api_dev_key':self.api_dev_key,
        #         'api_option':api_option}
        req = urllib2.urlopen('https://pastebin.com/api/scraping.php',0,timeout=7)
        return req.read()

    def show_paste(self, paste_key):
        #Print Raw paste
        req = urllib2.urlopen('https://pastebin.com/raw/'+paste_key, timeout=7)
        return req.read()

    def scraper(self):
        #Fetch most recent pastes
        #Add ?limit=# to limit responses, max=250, default=50
        req = urllib2.urlopen('https://pastebin.com/api_scraping.php?limit=250',timeout=7)
        #document = etree.fromstring(req.read())
        x = req.read()
        data = json.loads(x)
        #print json.dumps(x)
        conn = MySQLdb.connect(
            host="host",
            user="user",
            passwd="password",
            db="db")
        cursor = conn.cursor()
   
        print "scrape url " + data[0]["scrape_url"]
        print "fullurl " + data[0]["full_url"]
        print "date " + data[0]["date"]
        print "key " + data[0]["key"]
        print "size " + data[0]["size"]
        print "expire " + data[0]["expire"]
        print "title " + data[0]["title"]
        print "syntax " + data[0]["syntax"]
        print "user " + data[0]["user"]
        #print data[0]["key"], data[0]["title"], data[0]["date"], data[0]["user"], data[0]["size"], data[0]["syntax"], data[0]["full_url"],
        cursor.execute("""INSERT INTO archive (scrape_url, full_url, date, key_something, size, expire, title, syntax, user) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
(data[0]["scrape_url"], data[0]["full_url"], data[0]["date"], data[0]["key"], data[0]["size"], data[0]["expire"], data[0]["title"], data[0]["syntax"], data[0]["user"]))
        conn.commit()

try:
    paste = pastebinScraper()
    paste.scraper()
    #db = mysqlConnect()
    #print db.r()
except Exception as e:
    print "[!] API Error:",e