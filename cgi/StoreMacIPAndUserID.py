#!/usr/bin/python
import cgi, cgitb
import json
import sqlite3
import ConfReader
import time
import os

def updateWhitelist(MacID):

    try:
        strWhiteListFilePath =ConfReader.GetValue(ConfReader.strWhitelistFilePathKey)

        f = open(strWhiteListFilePath, 'r')
        lines = f.read()
        MacID = MacID.replace("-",":")
        if MacID not in lines:
            with open(strWhiteListFilePath, "w+") as myfile:
                myfile.write(str(MacID)+"\n")

        sudoPassword = 'winjit123'
        result=""
        command = "sudo iptables -D FORWARD -m mac --mac-source %s -j ACCEPT" % MacID
        os.system('echo %s|sudo -S %s' % (sudoPassword, command))

        command = "sudo iptables -I FORWARD -m mac --mac-source %s -j ACCEPT" % MacID
        os.system('echo %s|sudo -S %s' % (sudoPassword, command))

        #command = "sudo squid3 -k reconfigure"
        #result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
        #response = {'result':result,'updateSquid':1}
        #print json.JSONEncoder().encode(response)

    except Exception,e:
        print str(e)

form = cgi.FieldStorage()

macid=""
ip=""
userid=""
duration=1
msisdn=""

macid = str(form.getvalue('macid')).replace("'","")
ip = str(form.getvalue('ip')).replace("'","")
userid = str(form.getvalue('userid')).replace("'","")
duration = (form.getvalue('duration'))
msisdn = str(form.getvalue('msisdn')).replace("'","")

if ip is None:
    ip='10.42.0.1'
if userid is None:
    userid ='0'
if macid is None:
    macid ='1'
if duration is None:
    duration=10
if msisdn is None:
    msisdn=''

response =""

print "Content-type: application/json\n\n"
strQuery=""
cTimestamp=int(time.time())
Timestamp=0
try:    
    strDBFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)
    db = sqlite3.connect(strDBFilePath)
    c = db.cursor()     

    if userid is None:
        response = {'result':False,'error':'userid is null','IP':ip,'UserID':userid,'recordCount':0,'IsCreated':0,'TimeUpdated':0,'duration':duration,
                'MSISDN':msisdn}
        exit()
    c.execute("select MacID,Timestamp from Users where MacID = '" + str(macid) + "';")

    Timestamp=int(time.time())+int(duration)*60

    IsUserPresent=False
    for record in c.fetchall():
        MacID = record[0]
        #Timestamp = record[1]
        IsUserPresent=True
        break

    if IsUserPresent:

        # if int(Timestamp) <= cTimestamp:
        #     Timestamp = cTimestamp+int(ConfReader.GetValue(ConfReader.strFreeLimitSeconds))

        if userid is None:
            strQuery = "UPDATE Users SET MacID='"+str(macid)+"',  IP='"+str(ip)+"', userID='"+str(userid)+"', Timestamp="+str(Timestamp)+", MSISDN='"+str(msisdn)+"' WHERE MacID ='"+str(MacID)+"';"

            c.execute(strQuery)
        else:
            strQuery = "UPDATE Users SET MacID='"+str(macid)+"',  IP='"+str(ip)+"', userID='"+str(userid)+"', Timestamp="+str(Timestamp)+", MSISDN='"+str(msisdn)+"' WHERE MacID ='"+str(MacID)+"';"
            c.execute(strQuery)
    else:

        # Timestamp = cTimestamp+int(ConfReader.GetValue(ConfReader.strFreeLimitSeconds))

        if userid is None:
            strQuery ="insert into Users(IP,MacID,userID,Timestamp,MSISDN) values('"+str(ip)+"','"+str(macid)+"','"+str(userid)+"',"+str(Timestamp)+",'"+str(msisdn)+"');"
            c.execute(strQuery)
        else:
            strQuery ="insert into Users(IP,MacID,userID,Timestamp,MSISDN) values('"+str(ip)+"','"+str(macid)+"','"+str(userid)+"',"+str(Timestamp)+",'"+str(msisdn)+"');"
            c.execute(strQuery)

    db.commit()
    db.close()

    updateWhitelist(macid)

    response = {'result':True,'error':None,'macID':macid,'IP':ip,'UserID':userid,'IsCreated':not IsUserPresent,
            'TimeUpdated':Timestamp,
            'cTimeUpdated':cTimestamp,'duration':duration,
                'MSISDN':msisdn}


    #updateIPTableRules()
    #updateSquid()

except Exception,e:
        response = {'result':False,'error':str(e),'IP':ip,'UserID':userid,'recordCount':0,'IsCreated':0,'TimeUpdated':Timestamp,
                'cTimeUpdated':cTimestamp,'duration':duration,
                'MSISDN':msisdn}




print json.JSONEncoder().encode(response)
