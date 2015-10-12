import mmap
import os
import re
import re  # for regular expressions - to match ip's
import sys  # for parsing command line opts
import time, sys

IPTABLES_MAIN = "/home/pi/iptables.main"
IPTABLES_DATA = "/home/pi/iptables.last"
WHITELISTFILE = "/etc/squid3/whitelist"
IP_LIST_PREVIOUS = []
IP_LIST_CURRENT = []
IP_ALL = []


def getDataByIPs(IP_LIST):
    try:

        # ----------------------------------Writing current IP's in IPTABLES to file IPTABLES_MAIN----------------------------------

        SAVE_IPS = "sudo iptables -v -n -L -x > %s" % IPTABLES_DATA
        print "Writing current IP's in IPTABLES to file IPTABLES_DATA"
        os.system(SAVE_IPS)

        #--------------------------------------------------------------------------------------------------------------------------

        COUNTER = 0
        DICT_RESULT = {}

        # open the file
        file = open(IPTABLES_DATA, "r")
        # create an empty list
        ips = []
        # read through the file
        for text in file.readlines():
            #strip off the \n
            LINE_CONTENT = []
            LINE_SPLITED = []
            text = text.rstrip()
            #this is probably not the best way, but it works for now
            #regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})$', text)
            regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', text)
            # if the regex is not empty and is not already in ips list append
            if regex is not None:

                ips.append(regex)
                strCurrentIP = ''.join(regex)
                strCurrentIP = strCurrentIP.replace("[", "")
                strCurrentIP = strCurrentIP.replace("]", "")
                DATA_BYTES = 0
                if strCurrentIP != "":
                    LINE_CONTENT = text.split(" ")
                    for content in LINE_CONTENT:
                        if content != "":
                            LINE_SPLITED.append(content)
                    if len(LINE_SPLITED) != 0 and len(LINE_SPLITED) != 8:
                        BYTES_USED = LINE_SPLITED[1]
                        if len(LINE_SPLITED) == 8:
                            IP_SOURCE = LINE_SPLITED[6]
                            IP_DEST = LINE_SPLITED[7]
                        else:
                            IP_SOURCE = LINE_SPLITED[7]
                            IP_DEST = LINE_SPLITED[8]

                        if (IP_SOURCE in IP_LIST):

                            DATA_BYTES = int(BYTES_USED)
                            if IP_SOURCE in DICT_RESULT.keys():
                                DICT_RESULT[IP_SOURCE] += DATA_BYTES
                                print str([IP_SOURCE])+"+=Bytes"+ str(DICT_RESULT[IP_SOURCE])
                            else:
                                DICT_RESULT[IP_SOURCE] = DATA_BYTES
                                print str([IP_SOURCE])+"=Bytes"+ str(DICT_RESULT[IP_SOURCE])

                        if (IP_DEST in IP_LIST):

                            DATA_BYTES = int(BYTES_USED)
                            if IP_DEST in DICT_RESULT.keys():
                                DICT_RESULT[IP_DEST] += DATA_BYTES
                                print str([IP_DEST])+"+=Bytes"+ str(DICT_RESULT[IP_DEST])
                            else:
                                DICT_RESULT[IP_DEST] = DATA_BYTES
                                print str([IP_DEST])+"=Bytes"+ str(DICT_RESULT[IP_DEST])
        print("MyDict:")
        print DICT_RESULT
        print("----------")
        return DICT_RESULT
        # print "Done"
        #loop through the list
        #for ip in ips:
        #I know there is argument as to whether the string join method is pythonic
        #addy = "".join(ip)
        #if addy is not '':
        #print "%s" % (addy)
        #cleanup and close file
        file.close()

# catch any standard error (we can add more later)
    except IOError, (errno, strerror):
        print "I/O Error(%s) : %s" % (errno, strerror)


def resetDataUsageOfIPs(IP_LIST):
    try:
        for content in IP_LIST:
            DELETE_IP = "sudo iptables -D FORWARD -s %s -j ACCEPT" % content
            os.system(DELETE_IP)
            DELETE_IP = "sudo iptables -D FORWARD -d %s -j ACCEPT" % content
            os.system(DELETE_IP)
            DELETE_IP = "sudo iptables -D OUTPUT -d %s" % content
            os.system(DELETE_IP)
            print "Blocking IP : %s" % DELETE_IP
            ADD_IP = "sudo iptables -I FORWARD 1 -s %s -j ACCEPT" % content
            os.system(ADD_IP)
            ADD_IP = "sudo iptables -I FORWARD 1 -d %s -j ACCEPT" % content
            os.system(ADD_IP)
            ADD_IP = "sudo iptables -I OUTPUT -d %s" % content
            os.system(ADD_IP)
            print "Allowing IP : %s" % ADD_IP

    #catch any standard error (we can add more later)
    except IOError, (errno, strerror):
        print "I/O Error(%s) : %s" % (errno, strerror)


def runWhiteList():
    try:
        #----------------------------------Writing current IP's in IPTABLES to file IPTABLES_MAIN----------------------------------

        SAVE_IPS = "sudo iptables-save > %s" % IPTABLES_MAIN
        print "Writing current IP's in IPTABLES to file IPTABLES_MAIN"
        os.system(SAVE_IPS)

        #--------------------------------------------------------------------------------------------------------------------------

        #----------------------------------Extracting IP Addresses From IPTables Current Stat File---------------------------------

        # open the file
        file = open(IPTABLES_MAIN, "r")
        # create an empty list
        # read through the file
        for text in file.readlines():
           #strip off the \n
            text = text.rstrip()
           #this is probably not the best way, but it works for now
            #regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})$', text)
            regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', text)
            # if the regex is not empty and is not already in ips list append
            #print "IP: %s" % (regex)
            if regex is not None and regex not in IP_LIST_PREVIOUS:
                IP_LIST_PREVIOUS.append(regex)

        #print "Done"
        #loop through the list
        for ip in IP_LIST_PREVIOUS:
            #I know there is argument as to whether the string join method is pythonic
            addy = "".join(ip)
            if addy is not '':
                print "%s" % (addy)
        #cleanup and close file
        file.close()
        #catch any standard error (we can add more later)
        #--------------------------------------------------------------------------------------------------------------------------

        #-----------------------------------------Allow WHITE LIST Users TO Access PORT 443----------------------------------------

        for strAllow in reversed(open(WHITELISTFILE).readlines()):
            if strAllow.strip() != '' :
                if strAllow not in IP_LIST_PREVIOUS:
                #print "This -%s-" % strAllow.strip()
                    ALLOW_IP = "sudo iptables -I FORWARD -s %s -j ACCEPT" % strAllow.strip()
                    print "Allowing IP : %s" % ALLOW_IP.strip()
                    os.system(ALLOW_IP)
                    ALLOW_IP2 = "sudo iptables -I FORWARD -d %s -j ACCEPT" % strAllow.strip()
                    os.system(ALLOW_IP2)
                    ALLOW_IP3 = "sudo iptables -I OUTPUT -d %s" % strAllow.strip()
                    os.system(ALLOW_IP3)
                    print "Allowing IP : %s" % ALLOW_IP2.strip()
        #--------------------------------------------------------------------------------------------------------------------------

        #-----------------------------------------Removing IPs Which Are Not In White List-----------------------------------------
        IP_ALL = IP_LIST_PREVIOUS + IP_LIST_CURRENT

        #for LIST1 in IP_LIST_PREVIOUS:
        #	IP_ALL.append(LIST1)

        #for LIST2 in IP_LIST_CURRENT:
        #	IP_ALL.append(LIST2)

        for block in IP_ALL:
            strBlock = ''.join(block)
            strBlock = strBlock.replace("[","")
            strBlock = strBlock.replace("]","")
            if strBlock.strip() != '' :
                if block not in IP_LIST_CURRENT:
                    print "This B -%s-" % strBlock.strip()
                    BLOCK_IP = "sudo iptables -D FORWARD -s %s -j ACCEPT" % strBlock
                    os.system(BLOCK_IP)
                    BLOCK_IP2 = "sudo iptables -D FORWARD -d %s -j ACCEPT" % strBlock
                    os.system(BLOCK_IP2)
                    BLOCK_IP3 = "sudo iptables -D OUTPUT -d %s" % strBlock
                    os.system(BLOCK_IP3)
                    print "#####Blocking IP : %s" % strBlock
        #---------------------------------------------------
        # -----------------------------------------------------------------------
        print("Done")
    except IOError, (errno, strerror):
        print "I/O Error(%s) : %s" % (errno, strerror)




#resetDataUsageOfIPs(IP_LIST)

#getDataByIPs(IP_LIST)
