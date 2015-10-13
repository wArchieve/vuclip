import json
import urllib2
import os, re
import sqlite3
import sys, getopt
import ConfReader

def main():    
  databaseFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)#'/home/pi/pythonlogger.py/data.db'

  db = sqlite3.connect(databaseFilePath)
  c = db.cursor()             
  
  c.execute("SELECT TenPointsValueInMB from generalSettings;");
  for record in c:
    TenPointsValueInMB = record[0]  
  
  c.execute("SELECT userID,DataBalance,PointsBalance,IP,DataUsed  FROM users;");

  for record in c.fetchall():
    userID = record[0]
    DataBalance = record[1]
    PointsBalance = record[2]
    IPAddress = record[3]
    DataUsed = record[4]
    
    try: 
        apiurl =ConfReader.GetAPIURL() +"GetCreditPointNew/"+str(userID)
  
        j = urllib2.urlopen(apiurl)    
        js = json.load(j)

        CreditPoint = js['ReturnObject'][0]['CreditPoint']
        CreditPointsInMB = js['ReturnObject'][0]['CreditPointsInMB']
        FreeMB = js['ReturnObject'][0]['FreeMB']
        
        DataBalance = (CreditPointsInMB + FreeMB)
        
        c.execute("update users set PointsBalance="+str(CreditPoint)+", DataBalance="+str(DataBalance)+", DataUsed=0 where userID="+str(userID))
        db.commit()    
        response = {'UserID':userID , 'CreditPoint':CreditPoint}

        print response

    except Exception, e:
        print str(e)
        
if __name__ == "__main__":
    main()           
        