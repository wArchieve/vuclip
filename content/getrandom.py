#!/usr/bin/python

import sqlite3
import urllib2
from xml.dom import minidom


print "Content-type: text/xml\n\n"

def gen_token():

	db = sqlite3.connect('/home/pi/pythonlogger.py/data.db')
    c = db.cursor()
	BoxID = None
    c.execute("SELECT BoxID FROM Box LIMIT 1;");
    for record in c.fetchall():
      BoxID = record[0]

	print BoxID

    document = ("http://appbackend1.blueapple.mobi:8090/api/apps/getrandom?userid=box123@vuclip.com&password=Vuclip@123&ver=1.0&iid=12344")
    web = urllib2.urlopen(document)
    get_web = web.read()
    xmldoc = minidom.parseString(get_web)

    response=xmldoc.getElementsByTagName('X-VPRIME-RANDOM')

    for r in response:
        print(r.childNodes[0].nodeValue)
        val = r.childNodes[0].nodeValue

    conn = sqlite3.connect("/home/pi/bus.sqlite")
    cursor = conn.cursor()

    s="INSERT INTO random (token) VALUES ('"+str(val)+"');"
    cursor.execute(s)

    conn.commit()

if __name__ == "__gen_token__":
    gen_token()