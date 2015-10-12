import json

strConfigPath = "/home/box/content/moovah.config"

strLogFilePathKey = "AccessLogFilePath"
strDBFilePathKey = "DatabaseFilePath"

strBoxIP = "168.63.241.212"
strCMSIP = "192.168.5.1"

def GetValue(Key):
    try:
        with open(strConfigPath) as file:
            result = json.load(file)

            return result[Key]
    except Exception, e:
        return ''

def UpdateValue(Key,Value):
    try:
        result=''
        with open(strConfigPath) as file:
            result = json.load(file)
            result[Key]=Value

        with open(strConfigPath, 'w+') as outfile:
            json.dump(result, outfile)

        return 'true'
    except Exception, e:
        return 'false'

def AddKeyValue(Key,Value):
    try:
        with open(strConfigPath, 'w+') as outfile:
            result = json.load(outfile)
            result[Key]=Value
            json.dump(result, outfile)
        return 'true'
    except Exception, e:
        return 'false'

def GetAPIURL():
    try:

        Mode = GetValue('Mode')

        if Mode=='1':
            # This mode is for Staging API URL
            return GetValue('APIURL_Live')
        if Mode=='2':
            # This mode is for Live Staging API URL
            return GetValue('APIURL_Testing')
        if Mode=='3':
            return GetValue('APIURL_LiveOld')

        return Mode
    except Exception, e:
        return 'error'

def GetSyncDBPath():
    try:

        Mode = GetValue('Mode')

        if Mode=='1':
            # This mode is for Staging API URL
            return GetValue('SyncDBFilePath_Live')
        if Mode=='2':
            # This mode is for Live Staging API URL
            return GetValue('SyncDBFilePath_Testing')

        return GetValue('SyncDBFilePath_Live')
    except Exception, e:
        return 'error'


def GetAPIURLCom():

    try:
        Mode = GetValue('Mode')

        if Mode=='1':
            # This mode is for Staging API URL
            return GetValue('APIURL_LiveCom')
        if Mode=='2':
            # This mode is for Live Staging API URL
            return GetValue('APIURL_TestingCom')
        if Mode=='3':
            return GetValue('APIURL_LiveOld')

    except Exception, e:
        return 'Config Error : '+str(e)
