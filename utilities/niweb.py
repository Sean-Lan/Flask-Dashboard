import urllib2
import BeautifulSoup
from record import get_lv_info, get_versions_from_msi
import os
NIWEB_URL =  r'http://niweb.natinst.com'


def extract_valid_stack_urls(url):
    urls = []
    try:
        htmlsource = urllib2.urlopen(url).read()
        soup = BeautifulSoup(htmlsource, 'lxml')
        sw = soup.findAll('h4', text='Software Stacks')[-1]
        swtable = sw.findNext('table', { 'class': 'confluenceTable' })
        for tr in swtable.findAll('tr'):
            tds = tr.findAll('td')
            if len(tds) >= 3 and ('dat validated' in tds[2].text.lower() 
                    or 'passed' in tds[2].text.lower()):
                urls.append(NIWEB_URL + tds[1].find('a')['href'])
    except:
        pass
    return urls


def extract_installer_locations(stackUrl):
    installerLocationDict = {}
    try:
        htmlsource = urllib2.urlopen(stackUrl).read()
        soup = BeautifulSoup(htmlsource, 'lxml')
        installerHeader = soup.findAll('h1', text='Installers')[0]
        installerInfoTable = installerHeader.findNext('table',  { 'class': 'confluenceTable' })
        for tr in installerInfoTable.findAll('tr'):
            tds = tr.findAll('td')
            if len(tds) == 0:                    # skip the table header
                continue
            softwareName = tds[0].find('strong').string
            installerLocation = tds[1]
            if installerLocation.find('p'):      # means the field in the table is empty
                installerLocation = ''
            else:
                installerLocation = installerLocation.string
            installerLocationDict[softwareName] = installerLocation.\
                                replace('\setup.exe','')
                                # replace('us-aus','cn-sha').\
    except:
        pass
    return installerLocationDict


def convert_stackurl_list_to_dict(stackUrlList):
    stackUrlDict = {}
    for url in stackUrlList:
        stackName = url.split('/')[-1].replace('+',' ')
        stackUrlDict[stackName] = url
    return stackUrlDict


def construct_record_dict(stackUrl):
    stackRecord = {}
    stackRecord['stackUrl'] = stackUrl
    stackName = stackUrl.split('/')[-1].replace('+',' ')
    stackRecord['Validated Stack'] = stackName
    installerLocationDict = extract_installer_locations(stackUrl)

    # Get the LabVIEW infomation(i.e. lvVersion and lvAPIVersion)
    configFilePath = os.path.join(installerLocationDict['LV_Core'], 'buildInfo.txt')
    lvInfoDict = get_lv_info(configFilePath)
    stackRecord.update(lvInfoDict)

    # Get the myRIO/roboRIO safemode version from NIRIO msi file
    rioPath = installerLocationDict['cRIO']                                                         
    msiPath = os.path.join(rioPath,r'Products\NI-RIO_cRIO_Firmware_RT\cRIO_Firmware.msi')
    productNames = ('myRIO-1900','myRIO-1950','roboRIO')                                           
    safemodeVersionDict = get_versions_from_msi(msiPath,productNames)
    stackRecord['Safemode'] = safemodeVersionDict['myRIO-1900']+'/'+safemodeVersionDict['roboRIO']
    return stackRecord


if __name__ == '__main__':
    url = 'http://niweb.natinst.com/confluence/display/RIOSW/NI-RIO+15.0.0+Install+Instructions'
    urls = extract_valid_stack_urls(url)
    print urls[-1]
    # stackUrlDict = convert_stackurl_list_to_dict(urls)
    # print stackUrlDict
    stackUrl = r'http://niweb.natinst.com/confluence/display/RIOSW/RIO+Build+20150624_1715f3+with+06-18+LV+Stack'
    rec = construct_record_dict(stackUrl)
    print rec
