import re
import os
from record import get_lv_info, get_versions_from_msi
import installer
from bs4 import BeautifulSoup

def get_bundle_record(bundle_path, product_names, DVD_names):
    msb_xml = os.path.join(bundle_path, 'MSB_Summary.xml')
    soup = BeautifulSoup(open(msb_xml).read(), 'lxml')
    # obtain lvVersion and lvAPIVersion from buildInfo.txt of
    # LabVIEW distribution
    lv_tag = soup.find(attrs={'name':re.compile('^LabVIEW')})
    lv_path = lv_tag.find('volume')['path']
    lv_build_info_path = os.path.join(lv_path, 'buildInfo.txt')
    lv_info = get_lv_info(lv_build_info_path)

    # obtain toolkit installer location and
    # safemode from toolkit installer
    toolkit_tag = soup.find(attrs={'name':re.compile('Toolkit$')})
    toolkit_path = toolkit_tag.find('volume')['path']
    record = installer.get_installer_record(toolkit_path, product_names)
    record.update(lv_info)

    record['bundle_path'] = bundle_path

    # obtain actual size and dedupe size
    actual_size = []
    idea_size = []
    for name in DVD_names:
        abs_path = os.path.join(bundle_path, name)
        actual_size.append(str(getdirsize(abs_path)))
        idea_size.append(str(redupesize(abs_path)))
    record['actual_size'] = '/'.join(actual_size)
    record['idea_size'] = '/'.join(idea_size)
    return record


def getdirsize(dir):  
    size = 0L  
    for root, dirs, files in os.walk(dir):  
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])  
    return size 


def redupesize(dir, deduped_dict = {}, used_dict = {}):
    """
    Dedupe:
    With regard to files with the same name,
    only the last visit file's size counts.
    If `depuded_dict` is passed in, all depuded file, 
    and its size is stored in the dict.
    If `used_dict` is passed in, all final used file, 
    and its size is stored in the dict.
    """
    file_dict = {}
    fullpath_dict = {}
    for root, dirs, files in os.walk(dir):
        for name in files:
            full_path = os.path.join(root, name)
            file_size = os.path.getsize(full_path)
            if name in file_dict: # duplicate file found
                deduped_path = fullpath_dict[name]
                deduped_dict[deduped_path] = file_dict[name]
            fullpath_dict[name] = full_path
            file_dict[name] = file_size
    for name in file_dict:
        used_dict[fullpath_dict[name]] = file_dict[name]
    return reduce(lambda size, name: size + file_dict[name],
            file_dict,
            0)


def get_date(date):
    """convert date from '2015_01_09_1234' to '20150109'"""
    parts = date.split('_')
    return parts[0]+parts[1]+parts[2]


def retrieve_bundle_folders(bundle_root, newer_than_date):
    """
    Get the bundle folers from the `bundle_root` whose 
    date is newer than `newer_than_date`
    """
    date_folders = os.listdir(bundle_root)
    date_folders = filter(lambda folder_name: get_date(folder_name) > newer_than_date, 
                        date_folders)
    bundle_folders = map(lambda date_folder: os.path.join(bundle_root, date_folder), 
                        date_folders)
    return bundle_folders




if __name__ == '__main__':
    # bundle_root = r'\\cn-sha-argo\NISoftwarePrerelease\myRIO\Bundle\3.1\Daily' 
    # newer_than_date = 20150301
    # bundle_folders = retrieve_bundle_folders(bundle_root, newer_than_date)
    # print bundle_folders
    # bundle_path = r'\\cn-sha-argo\NISoftwarePrerelease\roboRIO\Bundle\3.1\Daily\2015_06_15_1523'
    # product_names = ['roboRIO']
    # DVD_names = ['roboRIO_DVD1', 'roboRIO_DVD2']
    # record = get_bundle_record(bundle_path, product_names, DVD_names)
    # bundle_path = r'\\cn-sha-argo\NISoftwarePrerelease\roboRIO\Bundle\3.1\Daily\2015_06_15_1523'
    bundle_path = r'\\cn-sha-argo\NISoftwareReleased\Windows\Suites\LabVIEW Add-ons\myRIO\2015\3.1.0\myRIO_DVD1'
    deduped_dict = {}
    used_dict = {}
    deduped_size = redupesize(bundle_path, deduped_dict, used_dict)
    print deduped_size
    f = open('dedupe.log', 'w')
    f.write('%s files remained, %s files deduped\n\n' % (len(used_dict), len(deduped_dict)))
    f.write('-'*80)
    f.write('\n\n')
    f.write('Remained files(full path, size):\n')
    for name in sorted(used_dict):
        f.write(name + ': ' + str(used_dict[name]) + '\n')
    f.write('\n\nDeduped files(full path, size):\n')
    for name in sorted(deduped_dict):
        f.write(name + ': ' + str(deduped_dict[name]) + '\n')
