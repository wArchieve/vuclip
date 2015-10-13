import mmap
import os
import re
import re #for regular expressions - to match ip's
import sys #for parsing command line opts

IPTABLES_MAIN = "/home/box/content/vcIptablesWLServers.main"
IPTABLES_DATA = "/home/box/content/vcIptablesWLServers.last"
WHITELISTFILE = "/home/box/content/vcWhiteListServerIPs.txt"

IP_LIST_PREVIOUS = []
IP_LIST_CURRENT = []
IP_ALL = []

#----------------------------------Writing current IP's in IPTABLES to file IPTABLES_MAIN----------------------------------

SAVE_IPS = "sudo iptables-save > %s" % IPTABLES_MAIN
print "Writing current IP's in IPTABLES to file IPTABLES_MAIN"
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
        #if addy is not '':
        #    print "%s" % (addy)
    #cleanup and close file
    file.close()
#catch any standard error (we can add more later)
except IOError, (errno, strerror):
    print "I/O Error(%s) : %s" % (errno, strerror)

#--------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------Allow WHITE LIST Users TO Access PORT 443----------------------------------------

for strAllow in reversed(open(WHITELISTFILE).readlines()):
    if strAllow.strip() != '' :
        try:
            if strAllow not in IP_LIST_PREVIOUS:
		#print "This -%s-" % strAllow.strip()
               	ALLOW_IP = "sudo iptables -I FORWARD -p tcp -s %s -j ACCEPT" % strAllow.strip()
               	#print "Allowing IP : %s" % ALLOW_IP.strip()
               	try:
                  	os.system(ALLOW_IP)
                except Exception,e:
                  	print "Allow WhiteList1:"+str(e)
                ALLOW_IP2 = "sudo iptables -I FORWARD -p tcp -d %s -j ACCEPT" % strAllow.strip()
                #print "Allowing IP : %s" % ALLOW_IP2.strip()
               	try:
                  	os.system(ALLOW_IP2)
                except Exception,e:
                    	print "Allow WhiteList2:"+str(e)
                #print "Allowing IP : %s" % ALLOW_IP2.strip()
        except Exception,e:
            print str(e)
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
    try:
        if strBlock.strip() != '' :
            if block not in IP_LIST_CURRENT:
		#print "This B -%s-" % strBlock.strip()
                BLOCK_IP = "sudo iptables -D FORWARD -p tcp -s %s -j ACCEPT" % strBlock
                #print "#####Blocking IP : %s" % BLOCK_IP
                try:
                    os.system(BLOCK_IP)
                except Exception,e:
                    print "Delete from iptables 1:"+str(e)
                BLOCK_IP2 = "sudo iptables -D FORWARD -p tcp -d %s -j ACCEPT" % strBlock
                try:
                    os.system(BLOCK_IP2)
                except Exception,e:
                    print "Delete from iptables 2:"+str(e)
                #print "#####Blocking IP : %s" % strBlock
    except Exception,e:
            print str(e)
#--------------------------------------------------------------------------------------------------------------------------

print "Done!"

