#!/usr/bin/python

import urllib2
import sqlite3
import time
import getrandom

first_hit=0
def Post_Event():
    db = sqlite3.connect('bus.sqlite')
    c = db.cursor()
    c.execute("select * from random order by id desc LIMIT 1")
    data = c.fetchall()
    if len(data)==0:#database check
        print("No token, Generating now...")
        count = 1
        return 0
    token = data[0][1]
    c.close()
    print token
    nonce = int(time.time())
    # print nonce
    postbody = 'sample data from winjit'

    posturl = "http://appbackend1.vuclip.com:8090/api/analytics/addbatch?userid=box152@vuclip.com&rnd=" + str(token) + "&iid=box152@vuclip.com&appid=vplus_android&nonce=" + str(nonce) + "&ver=1.0"

    print posturl


    req = urllib2.Request(posturl)
    req.add_header('Content-Type', 'application/xml')
    try:        #token is expired
        print(urllib2.urlopen(req, postbody))
        response = urllib2.urlopen(req, postbody)
        get_response = response.read()
        res = str(get_response)
        print(res)
        # print(get_response)
        db = sqlite3.connect('bus.sqlite')
        c = db.cursor()
        c.execute("Delete from random where token=?", (token,))
        print("Deleted:\t" + token)
        db.commit()
        c.close()
    except Exception,e:
        print e
        global first_hit
        if first_hit < 1:
            first_hit = +1
            print 'hiting again'
            print first_hit
            Post_Event()
        else:
            return 0

    #print(response.read)
   # print response

status = Post_Event()
if status == 0:
    getrandom.gen_token()
    Post_Event()