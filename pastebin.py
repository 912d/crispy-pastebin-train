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
        #TODO XXX: 
        # Download, and save (to database or file?) every paste
        #   before they are removed ;)
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
        conn.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
       
        for d in range(250):
            #print data[d]
            cursor.execute("""INSERT INTO archive (scrape_url, full_url, date, key_something, size, expire, title, syntax, user) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (data[d]["scrape_url"], data[d]["full_url"], data[d]["date"], data[d]["key"], data[d]["size"], data[d]["expire"], data[d]["title"], data[d]["syntax"], data[d]["user"]))
        conn.commit()
        #print data[0]["key"], data[0]["title"], data[0]["date"], data[0]["user"], data[0]["size"], data[0]["syntax"], data[0]["full_url"],

try:
    paste = pastebinScraper()
    paste.scraper()
    #db = mysqlConnect()
    #print db.r()
except Exception as e:
    print "[!] API Error:",e