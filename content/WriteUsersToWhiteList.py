import sqlite3
import time
import ConfReader

def updateWhitelist():

    try:
        strDBFilePath = ConfReader.GetValue(ConfReader.strDBFilePathKey)
        db = sqlite3.connect(strDBFilePath)
        c = db.cursor()

        strWhiteListFilePath =ConfReader.GetValue(ConfReader.strWhitelistFilePathKey)
        with open(strWhiteListFilePath, "w") as myfile:
            MacID = open('/sys/class/net/eth0/address').read()
            myfile.write(str(MacID))
            print str(MacID)+" : added to whitelist"
            c.execute("SELECT DISTINCT MacID,Timestamp FROM Users ;");
            for record in c.fetchall():
                MacID = record[0]
                Timestamp = record[1]
                MacID =str(MacID).replace("'","")
                MacID =str(MacID).replace("-",":")
                if (int(Timestamp) > int(time.time())) and MacID is not None:
                    myfile.write(str(MacID)+"\n")
                    print  str(MacID)+": added to whitelist."



    except Exception,e:
        print str(e)
    
updateWhitelist()
