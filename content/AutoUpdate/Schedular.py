import datetime
import time
import os
import sqlite3
import sys

import MoovahLogger
from daemon import Daemon

def addSecs(dtCurrent,secs):
    fulldate = dtCurrent
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate

def ReOpenDBConn():
    try:
        db = sqlite3.connect("/home/box/content/AutoUpdate/Schedular.sqlite")
        db.isolation_level=None
        c = db.cursor()
    except Exception,e:
        db.close()

def runCommand(command,IsSudo):

    try:

        sudoPassword = 'winjit123'
        result=""
        if IsSudo == 1:
            result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
        else:
            result = os.system(command)

        MoovahLogger.logger.debug("Command Executed :"+str(command))
        return result

    except Exception,e:
        MoovahLogger.logger.error("Error in Run Command: "+str(e))


def RunOnceAt(DateNTime,Command,IsSudo,ID):

    try:
        db = sqlite3.connect("/home/box/content/AutoUpdate/Schedular.sqlite")
        db.isolation_level=None
        c = db.cursor()

        margin = datetime.datetime.timedelta(seconds = 5)
        DateNTime = datetime.datetime.strptime(DateNTime, "%Y-%m-%d %H:%M:%S.%f")

        if (datetime.datetime.now() - margin <= DateNTime <= datetime.datetime.now() + margin):

            c.execute("update schedule SET IsActive=0 where ID ='"+str(ID)+"';");
            db.commit()

            MoovahLogger.logger.debug("Command '"+str(Command)+"' is Deactivated")

            Result = runCommand(Command,IsSudo)

            MoovahLogger.logger.debug("RunOnceAt Executed For Schedule ID="+str(ID))

        db.close()
    except Exception,e:
        MoovahLogger.logger.error("RunOnce: "+str(e))
        ReOpenDBConn()

def RunEvery(dtCurrent,Command,IsSudo,ID,Interval):

    try:
        db = sqlite3.connect("/home/box/content/AutoUpdate/Schedular.sqlite")
        db.isolation_level=None
        c = db.cursor()

        dtCurrent = datetime.datetime.strptime(dtCurrent, "%Y-%m-%d %H:%M:%S.%f")

        if (dtCurrent <= datetime.datetime.now()):

            dtNew = addSecs(datetime.datetime.now(),Interval)
            c.execute("update schedule SET DateTime='"+str(dtNew)+"' where ID ='"+str(ID)+"';");
            db.commit()

            MoovahLogger.logger.debug("Command '"+str(Command)+"' will next execute at"+str(dtNew))


            Result = runCommand(Command,IsSudo)
            MoovahLogger.logger.debug("RunEvery Executed For Schedule ID="+str(ID))

        db.close()
        #time.sleep(SleepInterval)
    except Exception,e:
        MoovahLogger.logger.error("RunEvery: "+str(e))
        ReOpenDBConn()


def RunSchedular():
    try:
        db = sqlite3.connect("/home/box/content/AutoUpdate/Schedular.sqlite")
        db.isolation_level=None
        c = db.cursor()

        c.execute("SELECT * from schedule where IsActive=1;");
        for record in c.fetchall():

            ID = record[0]
            Command = record[1]
            DateNTime = record[2]
            IsSudo = record[3]
            RepeateType = record[4]
            Interval = record[5]

            if DateNTime is None or DateNTime is '':
                DateNTime = datetime.datetime.now()

            # This means the Command should be executed only once
            if RepeateType == 1:
                runCommand(Command,IsSudo)
            elif RepeateType == 2:
                RunOnceAt(DateNTime,Command,IsSudo,ID)
            elif RepeateType == 3:
                RunEvery(DateNTime,Command,IsSudo,ID,Interval)

        db.close()
    except Exception,e:
        MoovahLogger.logger.error("RunSchedular :"+str(e))
        ReOpenDBConn()

def StartSchedular():
    try:
        ReOpenDBConn()
        LocalPath = '/var/run/SchedularDaemon/'
        PidFile = LocalPath +'SchedularDaemon.pid'
        ObjDaemon = MyDaemon(PidFile)
        ObjDaemon.start()
    except Exception,e:
        MoovahLogger.logger.error("StartSchedular :"+str(e))

def StopSchedular():
    try:
        LocalPath = '/var/run/SchedularDaemon/'
        PidFile = LocalPath +'SchedularDaemon.pid'
        ObjDaemon = MyDaemon(PidFile)
        ObjDaemon.stop()

    except Exception,e:
        MoovahLogger.logger.error("StopSchedular :"+str(e))


class MyDaemon(Daemon):
    def run(self):
        while True:
            RunSchedular()
            time.sleep(10)
             # delays for 5 seconds


try:

    if len(sys.argv) == 2:

        MoovahLogger.logger.debug("Argument 0 : "+str(sys.argv[0]) +" Argument 1 : "+str(sys.argv[1]))

        LocalPath = '/var/run/SchedularDaemon/'
        PidFile = LocalPath +'SchedularDaemon.pid'

        if not os.path.exists(LocalPath):
            sudoPassword = 'winjit123'
            command ='sudo mkdir '+LocalPath
            result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
            command ='sudo chmod -R 777 '+LocalPath
            result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

        sudoPassword = 'winjit123'
        command ='sudo chmod -R 777 '+LocalPath
        result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

        ObjDaemon = MyDaemon(PidFile)

        if 'start' == sys.argv[1]:
            ObjDaemon.start()
            MoovahLogger.logger.debug( "SchedularDaemon Started")
        elif 'stop' == sys.argv[1]:
            ObjDaemon.stop()
            MoovahLogger.logger.debug("SchedularDaemon Stoped")
        elif 'restart' == sys.argv[1]:
            ObjDaemon.restart()
            MoovahLogger.logger.debug("SchedularDaemon Restarted")
        else:
            MoovahLogger.logger.debug("Unknown command")
            sys.exit(2)
        sys.exit(0)

except Exception,e:
    MoovahLogger.logger.debug(str(e))




