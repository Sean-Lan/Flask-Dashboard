import re
import os
from record import get_lv_info, get_versions_from_msi
import installer
from BeautifulSoup import BeautifulSoup
import msilib

def get_bundle_record(bundle_path, product_names, DVD_names):
    msb_xml = os.path.join(bundle_path, 'MSB_Summary.xml')
    soup = BeautifulSoup(open(msb_xml).read())

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
        total_size = getdirsize(abs_path)
        deduped_size = get_deduped_size(abs_path)
        actual_size.append(str(total_size))
        idea_size.append(str(total_size-deduped_size))
    record['actual_size'] = '/'.join(actual_size)
    record['idea_size'] = '/'.join(idea_size)
    return record


def getdirsize(dir):  
    size = 0L  
    for root, dirs, files in os.walk(dir):  
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])  
    return size 


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


def get_deduped_size(dirname):
    """
    Find the duplicate products, return the size of the duplicate products.
    A *duplicate* product is the product with the same UpgradeCode and 
    older ProductVersion.
    """
    product_dict = {}
    deduped_size = 0L
    for root, dirs, files in os.walk(dirname):  
        if len(dirs) != 0:
            continue
        files = filter( lambda filename: os.path.splitext(filename)[1] == '.msi',
                    files
                    )
        if len(files) == 0:
            continue
        # Get the first msi as a representative
        msi = sorted(files)[0]
        fullpath = os.path.join(root, msi)
        UpgradeCode, ProductVersion = get_installer_info_from_msi(fullpath)

        size = reduce(lambda size, name: size + os.path.getsize(
                                            os.path.join(root, name)),
                      files, 0)
        if UpgradeCode in product_dict:
            if product_dict[UpgradeCode]['version'] > ProductVersion:
                deduped_size += size
            else:
                deduped_size += product_dict[UpgradeCode]['size']
                product_dict[UpgradeCode] = {'version': ProductVersion,
                                             'size': size}
        else:
            product_dict[UpgradeCode] = {'version': ProductVersion,
                                         'size': size}

    return deduped_size


def get_installer_info_from_msi(msiPath):
    """
    Get the UpgradeCode, ProductVersion from Property table of product msi.
    """
    viewSql = "SELECT Value FROM Property WHERE Property = '{field_name}'"
    db = msilib.OpenDatabase(msiPath,msilib.MSIDBOPEN_READONLY)

    # Get `UpgradeCode`
    view = db.OpenView(viewSql.format(field_name='UpgradeCode'))
    view.Execute(None)
    result = view.Fetch()
    UpgradeCode = result.GetString(1)

    # Get `ProductVersion`
    view = db.OpenView(viewSql.format(field_name='ProductVersion'))
    view.Execute(None)
    result = view.Fetch()
    ProductVersion = result.GetString(1)

    return UpgradeCode, ProductVersion

if __name__ == '__main__':
    bundle_path = r'C:\Users\xlan\Desktop\bundle\2015_06_19_2143'
    product_names = ['myRIO']
    DVD_names = ['myRIO_DVD1', 'myRIO_DVD2']
    record = get_bundle_record(bundle_path, product_names, DVD_names)
    print record

