import urllib2
import sqlite3
import time
import getrandom

first_hit = 0

dbPath ="/home/box/content/bus.sqlite"
dataDBPath='/home/box/content/pythonlogger.py/data.db'

def Post_Event():

    db = sqlite3.connect(dataDBPath)
    c = db.cursor()
    BoxID = None
    c.execute("SELECT BoxID FROM Box LIMIT 1;");
    for record in c.fetchall():
        BoxID = record[0]
    print BoxID

    db = sqlite3.connect(dbPath)
    c = db.cursor()
    c.execute("select * from random order by id desc LIMIT 1")
    data = c.fetchall()
    if len(data)==0:#database check
        print("No token, Generating now...")
        count = 1
        return 0
    token = data[0][1]
    c.close()
    db.commit()
    print token
    nonce = int(time.time())

    posturl = "http://appbackend1.vuclip.com:8090/api/analytics/addbatch?userid=box"+str(BoxID)+"@vuclip.com&rnd=" + str(token) + "&iid=box"+str(BoxID)+"@vuclip.com&appid=vplus_android&nonce=" + str(nonce) + "&ver=1.0"
    print posturl
    
    db = sqlite3.connect(dbPath)
    c = db.cursor()
    c.execute("update postdata set IsUploading=1")
    c.execute("select * from postdata where Isuploading=1")
    data = c.fetchall()
    postbody = ''
    for each in data:
        postbody = postbody+each[1]+"\n"
    c.close()
    db.commit()

    if postbody=='' or postbody==None:
        print("No data to upload..")
        return 1

    req = urllib2.Request(posturl)
    req.add_header('Content-Type', 'text/plain')

    try:        #token is expired
        print "PostBody: "+postbody
        response = urllib2.urlopen(req, postbody)
        get_response = response.read()
        res = str(get_response)
        print("status: "+ res)
        if res.find("success") >= 0:
            db = sqlite3.connect(dbPath)
            c = db.cursor()
            c.execute("Delete from postdata where IsUploading=1")
            db.commit()
            c.close()
            print "records uploaded."
            return 1
        else:
            return 0

    except Exception,e:
        print "Error in uploading :"+str(e)
        global first_hit
        if first_hit < 1:
            first_hit = +1
            print 'hiting again'
            print first_hit
            Post_Event()
        else:
            return 0


status = Post_Event()
if status == 0:
    getrandom.gen_token()
    Post_Event()