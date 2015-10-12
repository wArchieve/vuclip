#!/usr/bin/python

import cgi, cgitb
import json
import sqlite3
import ConfReader
import os
import getenv
form = cgi.FieldStorage()

#macid = str(form.getvalue('macid'))
#ip = str(form.getvalue('ip'))
#userid = str(form.getvalue('userid'))


#print "Content-type: application/json\n\n"
page = 'Content-type: text/html\n\n'
page +='<html><head><title>Test Form</title></head>\n'

try:

    from socket import gethostname, gethostbyname, getaddrinfo
    ip = gethostbyname(gethostname())

    page+= 'IP : '+ip
    ip2 = os.environ["REMOTE_ADDR"]
    ip3 = os.getenv("HTTP_CLIENT_IP")
    page+= '\r\nIP2 : ' + ip2
    page+= '\r\nIP3 : ' + ip3
    #response = {'success':'true','macID':macid,'IP':ip,'UserID':userid}
    
except Exception,e:
    with open("PythonErrors.txt", "a") as myfile:
        myfile.write("postBoxDetailsOncms.py "+"###### "+str(e) +"\r\n")
    response = {'result': str(e)}
    page+='page contains Error :'+str(e)

print page

#print json.JSONEncoder().encode(response)


