import urllib
import httplib2
import os
import urlparse
import commands
from posixpath import dirname
import shutil
import MoovahLogger


def runCommand(command,IsSudo):

    try:

        sudoPassword = 'winjit@123'
        result=""
        if IsSudo == 1:
            result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
        else:
            result = os.system(command)

        MoovahLogger.logger.info("Command Executed :"+str(command))
        return result

    except Exception,e:
        MoovahLogger.logger.error("Error :"+str(e))


def copyFile(src,dst):
    shutil.copyfile(src,dst)

def copyAllFilesToDir(src,dst):
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_nameSRC = os.path.join(src, file_name)
        full_file_nameDST = os.path.join(dst, file_name)
        if (os.path.isfile(full_file_nameSRC)):
            shutil.copyfile(full_file_nameSRC, full_file_nameDST)
        elif (os.path.isdir(full_file_nameSRC)):
            srcNew = full_file_nameSRC
            dstNew = dst + os.path.basename(os.path.normpath(full_file_nameSRC))
            MoovahLogger.logger.error("SRC : "+str(srcNew)+" ====> DST : "+str(dstNew))
            if not os.path.exists(dstNew):
                runCommand("mkdir "+dstNew,1)
                runCommand("chmod 777 -R "+dstNew,1)
            copyAllFilesToDir(srcNew,dstNew)


def CheckURLStatus(url):
    try:
        h = httplib2.Http()#res = conn.getresponse()
        resp = h.request(url, 'HEAD')
        status = resp[0]['status']
        return status
    except Exception,e:
        MoovahLogger.logger.error("Remote File Error:=> "+str(e))
        return '500'


def DownloadFileToPath(RemotePath,LocalPath):
    try:
        status = CheckURLStatus(RemotePath)
        if status == "200":
            testfile = urllib.URLopener()
            commands.getoutput("mkdir -p "+dirname(LocalPath))
            testfile.retrieve(RemotePath, LocalPath)

        if os.path.exists(LocalPath):
            return True
        else:
            return False

    except Exception,e:
        MoovahLogger.logger.error("Download File Error:=> "+str(e))
        return False


def CheckAndDownloadFile(key,RemoteURL):

    try:

        ContentTokens =[

            "AdvertPath",
            "ThumbnailPath",
            "SponsorImage",
            "ImagePath",
            "UpcomingReleaseImage",
            "SplashScreenImage",
            "Path",
            "IconImage",
            "ScreenShot1",
            "ScreenShot2",
            "ScreenShot3",
            "ScreenShot4",
            "ScreenShot5",
            "UpcomingReleaseImage",
            "SplashScreenImage",
            "Logo",
            "BannerPath",
            "TCPath",
            "ExtraContent",
            "BannerImage",
            "FullScreenImage",
            "AdditionalPath"

        ]

        LocaPath ="/media/usb0/moovah"
        #LocaPath ="/home/pi"

        if key in ContentTokens and RemoteURL is not None and RemoteURL is not '':
            parse_object = urlparse.urlparse(RemoteURL)
            LocaPath+=parse_object.path

            # if DownloadFileToPath(RemoteURL,LocaPath):
            #     print("File Downloaded to: "+LocaPath)
            #     MoovahLogger.logger.info("File Downloaded to: "+LocaPath)

    except Exception,e:
        MoovahLogger.logger.error("FileMgr.CheckAndDownloadFile: " +str(e))



#CheckAndDownloadFile("Path","http://moovahapp.net/Live/Shared/MediaFiles/Video/from_jack_to_juke__a_history_of_ghetto_house/icon.png")