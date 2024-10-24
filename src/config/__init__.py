import configparser
#this is shared between all

_config = None

def getConfig():
    global _config
    if not _config:
        _config = configparser.ConfigParser()
        _config.read('assets/configs/config.ini')
    return _config
