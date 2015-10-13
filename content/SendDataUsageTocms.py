import json
import urllib2
import sqlite3
import ConfReader
import getDataUsageByIPs
import re
import os
import time

def readFileToMatrix(fd):
  dataMatrix,i={},0
  while 1:
    l=[]
    data=fd.readline()
    if data =="":
      break
    dd = data.split(" ")
    for item in dd:
      if item != "":
          l.append(item)
    if len(l)==10:
      c,s=l[3].split('/')[0],l[3].split('/')[1]
      ps,ph=l[8].split('/')[0],l[8].split('/')[1]
      l[9]=l[9].strip("\n")
      dataMatrix[i]=[l[0],l[1],l[2],c,s,l[4],l[5],l[6],l[7],ps,ph,l[9]]
      i = i + 1
  return dataMatrix

def main():    

    logFilePath = ConfReader.GetValue(ConfReader.strLogFilePathKey) #'/var/log/squid3/access.log'
    databaseFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)#'/home/pi/pythonlogger.py/data.db'

    print logFilePath
    print databaseFilePath

    fd = open(logFilePath,'r')
    dataMatrix = readFileToMatrix(fd)

    print dataMatrix

    db = sqlite3.connect(databaseFilePath)
    c = db.cursor()

    BoxID = None
    c.execute("SELECT BoxID FROM Box LIMIT 1;");
    for record in c.fetchall():
      BoxID = record[0]

    print "BoxID: "+str(BoxID)
    LogData ={}
    UserIDs=''
    i=0
    for key, value in dataMatrix.items():

        BytesUsed = value[5]
        IpAddress = value[2]
        URLVisited = value[7]

        userID=None
        strQuery ="SELECT userID,MacID FROM Users where IP='"+str(IpAddress)+"';"

        c.execute(strQuery);
        for record in c.fetchall():
            userID = record[0]
            macID = record[1]

        print(str(userID)+"::::"+str(macID))

        if (str(userID) == None) or (str(userID) == 'None') or (str(userID) == ''):
            userID=macID

        LogData[i]={ "UserID":userID ,"Bytes":BytesUsed, "URL":URLVisited,"IpAddress":IpAddress,"BoxID":BoxID }
        i+=1

    try:
        url = ConfReader.GetAPIURLCom() +"BrowsingTransactionNew"

        print url

        postdata = LogData.values()

        print postdata

        req = urllib2.Request(url)
        req.add_header('Content-Type','application/json')
        data = json.dumps(postdata)

        #if DataUsed > 0:
        response = urllib2.urlopen(req,data)
        js = json.load(response)
        print("MyResponse:%s:"+str(js))
        lFile = open(logFilePath, "w")
        lFile.close()
        print "done"

    except Exception, e:
        print str(e)
        
if __name__ == "__main__":
    main()           
        
