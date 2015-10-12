import json
import urllib2
import sqlite3
import Schedular
import ConfReader
import MoovahLogger
import datetime
import FileMgr

def main():

    try:

        IsSchedularStoped=0

        LiveAPIURL = "http://moovahapp.com/Live/LiveAPI/"


        apiurl =ConfReader.GetAPIURLCom() +"GetGeneralSettings/0001-01-01%2000:00:00.000"

        j = urllib2.urlopen(apiurl)    
        js = json.load(j)
        UpgradeTime = js['ReturnObject'][0]['UpgradeTime']
        SyncInterval = js['ReturnObject'][0]['SyncInterval']
        AndroidBuild = js['ReturnObject'][0]['AndroidBuild']
        BlackBerryBuild = js['ReturnObject'][0]['BlackBerryBuild']
        AndroidVersion = js['ReturnObject'][0]['AndroidVersion']
        BlackBerryVersion = js['ReturnObject'][0]['BlackBerryVersion']

        pt =datetime.datetime.strptime(SyncInterval,'%H:%M:%S')
        Sync_Seconds = pt.second+pt.minute*60+pt.hour*3600

        # UpgradeDate = datetime.datetime.now().date()
        # UpgradeTime = datetime.datetime.strptime(UpgradeTime,'%H:%M:%S')
        #
        # UpgradeDateTime = datetime.datetime.combine(UpgradeDate, UpgradeTime.time())
        #
        # UpgradeDateTime = datetime.datetime.strptime(str(UpgradeDateTime)+".120000","%Y-%m-%d %H:%M:%S.%f")

        pt =datetime.datetime.strptime(UpgradeTime,'%H:%M:%S')
        SyncUpgrade_Seconds = pt.second+pt.minute*60+pt.hour*3600

        MoovahLogger.logger.error("StopSchedular called from getGeneralSettingsFromcms Process: ")
        Schedular.StopSchedular()
        IsSchedularStoped=1

        db = sqlite3.connect("/home/box/content/AutoUpdate/Schedular.sqlite")
        db.isolation_level=None
        c = db.cursor()


        # update.py
        #c.execute("delete from schedule where Command like '%update.py%'")                                                                                                                     #values('python /home/pi/AutoUpdate/getGeneralSettingsFromcms.py','2015-03-18 12:38:43.852425',1,3,360,1)
        c.execute("update schedule set Interval='"+str(Sync_Seconds)+"' where Command like '%update.py%'")

        # upgrade.py
        #c.execute("delete from schedule where Command like '%upgrade.py%'")                                                                                                                     #values('python /home/pi/AutoUpdate/getGeneralSettingsFromcms.py','2015-03-18 12:38:43.852425',1,3,360,1)
        c.execute("update schedule set Interval='"+str(SyncUpgrade_Seconds)+"' where Command like '%upgrade.py%'")


        c.execute("SELECT AndroidBuild,BlackBerryBuild,AndroidVersion,BlackBerryVersion from generalSettings;");
        AndroidBuildLocal=""
        BlackBerryBuildLocal =""
        AndroidVersionLocal =""
        BlackBerryVersionLocal =""
        for record in c:
            AndroidBuildLocal=record[0]
            BlackBerryBuildLocal =record[1]
            AndroidVersionLocal =record[2]
            BlackBerryVersionLocal =record[3]

        #AndroidBuild

        if AndroidVersion != AndroidVersionLocal:

            if AndroidBuild is None or AndroidBuild is '':
                MoovahLogger.logger.error("No File is present on server on following path : "+str(AndroidBuild)+". program will now terminate")
                return
            else:
                print(AndroidBuild)

            FileMgr.DownloadFileToPath(AndroidBuild,AndroidBuildLocal+".tmp")
            Schedular.runCommand("chmod 777 -R "+AndroidBuildLocal+".tmp",1)
            Schedular.runCommand("chmod 777 -R "+AndroidBuildLocal,1)
            FileMgr.copyFile(AndroidBuildLocal+".tmp",AndroidBuildLocal)
            Schedular.runCommand("rm "+AndroidBuildLocal+".tmp",1)
            c.execute("update generalSettings set AndroidVersion='"+str(AndroidVersion)+"'")
        else:
            MoovahLogger.logger.debug("Android Version "+str(AndroidVersionLocal) +" is already present on Box.")


        #BlackBerryBuild

        if BlackBerryVersion != BlackBerryVersionLocal:

            if BlackBerryBuild is None or BlackBerryBuild is '':
                MoovahLogger.logger.error("No File is present on server on following path : "+str(BlackBerryBuild)+". program will now terminate")
                return
            else:
                print(BlackBerryBuild)

            print BlackBerryBuildLocal
            Schedular.runCommand("chmod 777 -R "+BlackBerryBuildLocal,1)
            FileMgr.DownloadFileToPath(BlackBerryBuild,BlackBerryBuildLocal+"moovah.zip")
            Schedular.runCommand("unzip -o "+BlackBerryBuildLocal+"moovah.zip"+" -d "+BlackBerryBuildLocal,1)
            Schedular.runCommand("chmod 777 -R "+BlackBerryBuildLocal,1)
            c.execute("update generalSettings set BlackBerryVersion='"+str(BlackBerryVersion)+"'")
        else:
            MoovahLogger.logger.debug("Blackberry Version "+str(BlackBerryVersionLocal) +" is already present on Box.")

        db.commit()

    except Exception,e:
        MoovahLogger.logger.error("Error in getGeneralSettingsFromcms Process: "+str(e))

    finally:
        if IsSchedularStoped==1:
            MoovahLogger.logger.error("StartSchedular called from getGeneralSettingsFromcms Process: ")
            Schedular.StartSchedular()
            IsSchedularStoped=0


if __name__ == "__main__":
    main()