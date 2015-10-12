#!/usr/bin/python

import cgi
import json
import sqlite3
import ConfReader

form = cgi.FieldStorage()

response =""

print "Content-type: application/json\n\n"

try:    
    strDBFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)
    db = sqlite3.connect(strDBFilePath)
    c = db.cursor()     
    
    c.execute("select BoxID from Box where IsActive=1;")

    BoxID = "-1"

    for record in c.fetchall():
        BoxID = record[0]

    response = {'boxid':BoxID}
    
except Exception, e:    
    with open("PythonErrors.txt", "a") as myfile:
        myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\n")        
    response = {'error': str(e)}



print json.JSONEncoder().encode(response)


