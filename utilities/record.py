"""
This module mainly deals with the process of retrieving
infomation (e.g., lvVersion, lvAPIversion, safemode) of the toolkit or bundle.
"""
import msilib
import ConfigParser
import os


def get_lv_info(config_file_path):
    lvInfo = {}
    lvCfgParser = ConfigParser.ConfigParser()
    lvCfgParser.read(config_file_path)
    if lvCfgParser.has_section('Build Information'):
        section_name = 'Build Information'
    else:
        section_name = 'LabVIEW Build Information'

    lvInfo['lvVersion'] = lvCfgParser.get(section_name, 'lvVersion')
    lvInfo['lvAPIVersion'] = lvCfgParser.get(section_name, 'lvAPIVersion')
    return lvInfo


def get_versions_from_msi(msiPath,productNames):
    """
    Get product versions from the File of designated msi file.
    The FileName field in the File table must end with '.cfg'
    (e.g. kcsbvqgs.cfg|myRIO-1900_3.0.0a10.cfg)
    """
    db = msilib.OpenDatabase(msiPath,msilib.MSIDBOPEN_READONLY)
    viewSql = "SELECT FileName FROM File "       # Note that msi SQL doesn't support LIKE keyword
    fileView = db.OpenView(viewSql)
    fileView.Execute(None)
    fileNameList = []
    try:
        while True:
            result = fileView.Fetch()
            fileNameList.append(result.GetString(1))
    except:
        pass
    versionDict = {}
    for fileName in fileNameList:
        for productName in productNames:
            index = fileName.find(productName)
            if index != -1:
                version = fileName[index+len(productName)+1:-4]
                versionDict[productName] = version
    return versionDict
