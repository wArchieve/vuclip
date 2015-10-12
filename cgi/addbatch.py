#!/usr/bin/python

import json
import sys
import os
import sqlite3

response =""

print "Content-type: application/json \n"

try:
    length=int(os.getenv('CONTENT_LENGTH', 0))

    data = sys.stdin.read(length)
    #data='this is sample'
    response = {'data':str(data)}
    postdata=str(data)    
    conn = sqlite3.connect("/home/pi/bus.sqlite")
    cursor = conn.cursor()

    s="INSERT INTO postdata (data) VALUES ('"+str(postdata)+"');"

    cursor.execute(s)
   # cursor.close()
    conn.commit()
	
	response = {'data':str(postdata),'result':'true'}

except Exception, e:
    response = {'error': str(e)}

print json.JSONEncoder().encode(response)

