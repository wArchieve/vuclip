import socket
import re

WHITE_LIST_SERVERS = "/home/box/content/vcFreeWebsites.txt"
IP_ALL = []


def get_ips_for_host(host):
    try:
        ips = socket.gethostbyname_ex(host)
    except socket.gaierror:
        ips = []
    return ips


def getServerIPfromWhiteListDomains():
    try:
        # open the file
        file = open(WHITE_LIST_SERVERS, "r")
        # create an empty list
        # read through the file
        for text in file.readlines():
            # strip off the \n
            text = text.rstrip()

            ips = get_ips_for_host(text)
            # print "text:%s ips:%s" %(text, ips)
            for currentIP in ips:
                regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', str(currentIP))
                if regex is not None and regex not in IP_ALL:
                    IP_ALL.append(regex)

        # cleanup and close file
        file.close()

        IP_CURRENT = []
        fileCurrent = open("/home/box/content/vcWhiteListServerIPs.txt", "r")
        # create an empty list
        # read through the file
        for text in fileCurrent.readlines():
            # strip off the \n
            text = text.rstrip()
            IP_CURRENT.append(text)

        result = list(IP_CURRENT)
        for ipNew in IP_ALL:
            result.extend(x for x in ipNew if x not in result)

        print (IP_ALL)
        print(IP_CURRENT)
        with open("/home/box/content/vcWhiteListServerIPs.txt", "w") as myfile:
            for ipNew in result:
                myfile.write(ipNew+"\n")
    # catch any standard error (we can add more later)
    except IOError, (errno, strerror):
        print "I/O Error(%s) : %s" % (errno, strerror)


getServerIPfromWhiteListDomains()
