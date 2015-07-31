"""
This module mainly deals with the process of retrieving
infomation (e.g., lvVersion, lvAPIversion, safemode) of the toolkit or bundle.
"""
import msilib
import ConfigParser
import os
import re


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


def remove_path_prefix(path):
    """
    Remove '\\cn-sha-argo\' or '\\us-aus-argo\'
    from path
    """
    return path[14:]


def add_path_prefix(path, prefix):
    """
    Add '\\cn-sha-argo' or '\\us-aus-argo'
    to the begin of the path
    """
    return os.path.join(prefix, path)


def get_date(folder_name):
    date_pattern = re.compile(r'\d{4}_?\d{2}_?\d{2}_\d{4}')
    match = date_pattern.search(folder_name)
    return match.group()



if __name__ == '__main__':
    path = r'\\us-aus-argo\NISoftwarePrerelease\myRIO\Bundle\3.1\Daily\2015_06_23_0247'
    print remove_path_prefix(path)
