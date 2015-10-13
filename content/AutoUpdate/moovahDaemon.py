
#!/usr/bin/env python

import sys
import time
import os

from daemon import Daemon
import MoovahLogger


# import sys
# sys.path.insert(0, '/home/pi')
#
# import WriteUsersToSquidWhiteList
# import CalculateDataUsageInMB
# import WriteUsersToSquidWhiteList
# import WriteUsersToSquidWhiteList
# import WriteUsersToSquidWhiteList


class MyDaemon(Daemon):
    def run(self):
        while True:

            try:

                #WriteUsersToSquidWhiteList.updateWhitelist()
                sudoPassword = 'winjit123'

                command = "python /home/box/content/AutoUpdate/Schedular.py start"
                result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

                command = "python /home/box/content/AutoUpdate/ReportDaemon.py start"
                result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

                MoovahLogger.logger.info("moovahDaemon Started")

                break

            except Exception,e:
                MoovahLogger.logger.error("moovahDaemon Error :"+str(e))

            time.sleep(10)


#if __name__ == "__main__":


try:


    LocalPath = '/var/run/MoovahDaemon/'
    PidFile = LocalPath +'MoovahDaemon.pid'
    if not os.path.exists(LocalPath):
        sudoPassword = 'winjit123'
        command ='sudo mkdir '+LocalPath
        result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
        command ='sudo chmod -R 777 '+LocalPath
        result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

    # if not os.path.exists(PidFile):
    #     pidf = open(PidFile,'w+')
    #     pidf.close()

    sudoPassword = 'winjit123'
    command ='sudo chmod -R 777 '+LocalPath
    result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))


    daemon = MyDaemon(PidFile)


    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
            print "Daemon Started"
        elif 'stop' == sys.argv[1]:
            daemon.stop()
            print "Daemon Stoped"
        elif 'restart' == sys.argv[1]:
            daemon.restart()
            print "Daemon Restarted"
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

except Exception,e:
    print(str(e))
