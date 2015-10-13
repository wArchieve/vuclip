import json
import urllib2
import sqlite3
import sys
import getopt

import ConfReader


def main():

    try:
        url = ConfReader.GetAPIURLCom() +"GetFreeWebsites"
        print url
        req = urllib2.Request(url)
        req.add_header('Content-Type','application/json')

        response = urllib2.urlopen(req)
        js = json.load(response)

        if js['StatusCode'] == 200:

            with open("/home/box/content/freeSites", "w+") as myfile:

                FreeUrls = js['ReturnObject']

                for FreeURL in FreeUrls:
                    myfile.write(str(FreeURL["WebsiteURL"]).replace("http://","")+"\n")
                    print str(FreeURL["WebsiteURL"])+"\n"

    except Exception, e:
        print str(e)

if __name__ == "__main__":
    main()
