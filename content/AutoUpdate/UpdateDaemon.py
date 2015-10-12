import datetime
import time
import os
import sqlite3
import sys
import MoovahLogger
from daemon import Daemon


def runCommand(command,IsSudo):

    try:

        sudoPassword = 'winjit@123'
        result=""
        if IsSudo == 1:
            result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
        else:
            result = os.system(command)

        MoovahLogger.logger.debug("Command Executed :"+str(command))
        return result

    except Exception,e:
        MoovahLogger.logger.error("Error in Run Command: "+str(e))



def StartSyncProcess():
    try:
        #MoovahLogger.logger.error("UpdateSchedular :")
        runCommand("python /home/box/content/SyncDB/SyncBox.py",1)

    except Exception,e:
        MoovahLogger.logger.error("UpdateSchedular :"+str(e))


class MyDaemon(Daemon):
    def run(self):
        MoovahLogger.logger.info("Update Process Started ...")
        StartSyncProcess()

try:

    if len(sys.argv) == 2:

        MoovahLogger.logger.debug("Argument 0 : "+str(sys.argv[0]) +" Argument 1 : "+str(sys.argv[1]))

        LocalPath = '/var/run/UpdateSchedular/'
        PidFile = LocalPath +'UpdateSchedular.pid'
        if not os.path.exists(LocalPath):
            sudoPassword = 'winjit@123'
            command ='sudo mkdir '+LocalPath
            result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
            command ='sudo chmod -R 777 '+LocalPath
            result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))


        sudoPassword = 'winjit@123'
        command ='sudo chmod -R 777 '+LocalPath
        result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

        ObjDaemon = MyDaemon(PidFile)

        if 'start' == sys.argv[1]:
            ObjDaemon.start()
            print "UpdateSchedular Started"
        elif 'stop' == sys.argv[1]:
            ObjDaemon.stop()
            print "UpdateSchedular Stoped"
        elif 'restart' == sys.argv[1]:
            ObjDaemon.restart()
            print "UpdateSchedular Restarted"
        else:
            print "UpdateSchedular Unknown command"
            sys.exit(2)
        sys.exit(0)

except Exception,e:
    print(str(e))




