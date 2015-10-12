import mmap
import os
import re
import re #for regular expressions - to match ip's
import sys #for parsing command line opts
import ConfReader

IPTABLES_MAIN = "/home/box/content/iptables.main"
IPTABLES_DATA = "/home/box/content/iptables.last"
WHITELISTFILE = ConfReader.GetValue(ConfReader.strWhitelistFilePathKey)
print "Whitelist Path: "+WHITELISTFILE
WHITELIST_SERVERS_FILE = "/home/box/content/vcWhiteListServerIPs.txt"
IP_LIST_PREVIOUS = []
IP_LIST_CURRENT = []
IP_ALL = []

#----------------------------------Writing current IP's in IPTABLES to file IPTABLES_MAIN----------------------------------

SAVE_IPS = "sudo iptables-save > %s" % IPTABLES_MAIN
#print "Writing current IP's in IPTABLES to file IPTABLES_MAIN"
os.system(SAVE_IPS)

#--------------------------------------------------------------------------------------------------------------------------

#----------------------------------Extracting IP Addresses From IPTables Current Stat File---------------------------------

try:
    # open the file
    file = open(IPTABLES_MAIN, "r")
    # create an empty list
    # read through the file
    for text in file.readlines():
        #strip off the \n
        text = 'sudo iptables ' + text.strip()
        if '-m mac --mac-source' in str(text):
            text = text.replace("-I","-D")
            text = text.replace("-A","-D")
            print "Mac Rule: " + str(text)
            sudoPassword = 'winjit123'
            result = os.system('echo %s|sudo -S %s' % (sudoPassword, text))
    #cleanup and close file
    file.close()
#catch any standard error (we can add more later)
except IOError, (errno, strerror):
    print "I/O Error(%s) : %s" % (errno, strerror)

#--------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------Allow WHITE LIST Users TO Access PORT 443----------------------------------------

for strAllow in (open(WHITELISTFILE).readlines()):
    if strAllow.strip() != '' :
        strAllow = strAllow.replace("-",":")
        try:
            sudoPassword = 'winjit123'
            result=""
            command = "sudo iptables -I FORWARD -m mac --mac-source %s -j ACCEPT" % strAllow.strip()

            result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
            print "Mac Allowed : %s" % command.strip()

        except Exception,e:
            print str(e)
