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
    data='this is sample'
    response = {'data':str(data)}
    postdata=str(data)
    response = {'data':str(postdata)}
    conn = sqlite3.connect("bus.sqlite")
    cursor = conn.cursor()

    s="INSERT INTO postdata (data) VALUES ('"+str(postdata)+"');"

    cursor.execute(s)
   # cursor.close()
    conn.commit()

except Exception, e:
    response = {'error': str(e)}

print json.JSONEncoder().encode(response)

