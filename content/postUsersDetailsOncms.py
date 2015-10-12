import urllib2,json
import sqlite3
import sys, getopt
import os
import commands
import platform
import imp
import ConfReader


try:

    strDBFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)
    db = sqlite3.connect(strDBFilePath)
    c = db.cursor()

    MacID = ""
    MSISDN = ""
    UserID = ""
    IP = ""
    BoxID =None

    data={}
    i=0

    c.execute("SELECT BoxID FROM Box;");
    for record in c.fetchall():
        BoxID = record[0]

    c.execute("SELECT DISTINCT userID,MacID,MSISDN,IP FROM Users;");
    for record in c.fetchall():
        MacID = record[1]
        MSISDN = record[2]
        UserID = record[0]
        IP = record[3]
        data[i] = [{'MacID':str(MacID),'MSISDN':str(MSISDN),'UserID':str(UserID),
                'IPAddress':str(IP),'BoxID':BoxID}]
        i+=1

    url=''

    url = ConfReader.GetAPIURLCom() +'UsersDetails'
    print url

    postdata = data.values()

    req = urllib2.Request(url)
    req.add_header('Content-Type','application/json')
    data = json.dumps(postdata)
    print data
    response = urllib2.urlopen(req,data)

    result = json.loads(response.read())
    print result
    if result["StatusCode"] is 200:
        print "Users inserted to live CMS"
    else:
        print "Error while pushing records :" + str(result)

except Exception,e:
    with open("PythonErrors.txt", "a") as myfile:
        myfile.write("boxdetails.py"+"######"+str(e)+"\r\n")
    print str(e)
