#!/usr/bin/python

import cgi, cgitb
import json
import sqlite3
import ConfReader
import time

form = cgi.FieldStorage()

macid=""
ip=""
userid=""

macid = str(form.getvalue('macid')).replace("'","")
ip = str(form.getvalue('ip')).replace("'","")
userid = str(form.getvalue('userid')).replace("'","")

if ip is None:
    ip='192.168.5.1'
if userid is None:
    userid ='0'
if macid is None:
    macid ='1'

response =""

print "Content-type: application/json\n\n"

try:


    strDBFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)
    db = sqlite3.connect(strDBFilePath)
    c = db.cursor()
    strQuery ="select IP,Timestamp from Users where MacID = '" + str(macid) + "';"
    strQueries = strQuery
    c.execute(strQuery)

    Timestamp=0
    IsUserPresent=False
    for record in c.fetchall():
        IP = record[0]
        Timestamp = record[1]
        IsUserPresent=True
        break

    if IsUserPresent:

        if Timestamp<int(time.time()):
            Timestamp = int(time.time())+30*60

        if userid is None:
            strQuery ="UPDATE Users SET MacID='"+str(macid)+"',  IP='"+str(ip)+"', Timestamp="+str(Timestamp)+"  WHERE MacID = '"+str(macid)+"';"
            strQueries += strQuery
            c.execute(strQuery)
        else:
            strQuery ="UPDATE Users SET MacID='"+str(macid)+"',  IP='"+str(ip)+"', Timestamp="+str(Timestamp)+", userID='"+str(userid)+"' WHERE MacID='"+str(macid)+"';"
            strQueries += strQuery
            c.execute(strQuery)
    else:

        Timestamp = int(time.time())+30*60

        if userid is None:
            strQuery ="insert into Users(IP,MacID,DataUsed,DataBalance,IsRegistered,PointsBalance,userID,IsConnected,Timestamp) values('"+str(ip)+"','"+str(macid)+"',0,0,0,0,'"+str(userid)+"',0,"+str(Timestamp)+");"
            strQueries += strQuery
            c.execute(strQuery)
        else:
            strQuery ="insert into Users(IP,MacID,DataUsed,DataBalance,IsRegistered,PointsBalance,userID,IsConnected,Timestamp) values('"+str(ip)+"','"+str(macid)+"',0,0,0,0,'"+str(userid)+"',0,"+str(Timestamp)+");"
            strQueries += str(strQuery)
            c.execute(str(strQuery))

    db.commit()    
    response = {'success':'true','macID':str(macid),'IP':str(ip),'UserID':str(userid),'input':str(strQueries)}
    
except Exception,e:
        response = {'success':'true','ErrorDetails': str(e)}


print json.JSONEncoder().encode(response)


