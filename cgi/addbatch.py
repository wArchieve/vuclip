#!/usr/bin/python

import json
import sys
import os
import sqlite3

response =""
s=''
strPath=''
print "Content-type: application/json \n"

try:
    length=int(os.getenv('CONTENT_LENGTH', 0))

    data = sys.stdin.read(length)
    #data='this is sample'
    response = {'data':str(data)}
    postdata=str(data)
    strPath = "/home/pi/content/bus.sqlite"
    conn = sqlite3.connect(strPath)
    cursor = conn.cursor()

    s="INSERT INTO postdata (data) VALUES('"+str(postdata)+"');"
    cursor.execute(s)
    response = {'data':str(data)}

except Exception, e:
    response = {'error': str(e)+' Path: '+str(strPath)+" Cmd: "+str(s)}

print json.JSONEncoder().encode(response)

