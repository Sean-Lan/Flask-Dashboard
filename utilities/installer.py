import os
from record import get_lv_info, get_versions_from_msi

def get_installer_record(installer_path, product_names):
    record = {}
    lv_info = get_lv_info(os.path.join(installer_path, 'buildInfo.txt'))
    record.update(lv_info)
    msi_path = os.path.join(installer_path, r'Products\NI-RIO_cRIO_Firmware_RT\cRIO_Firmware.msi')
    safemodes = get_versions_from_msi(msi_path, product_names)
    safemode_str = reduce(lambda ret_str, product_name: ret_str + r'/' + safemodes[product_name],
                    product_names[1:], safemodes[product_names[0]])
    record['safemode'] = safemode_str
    record['installer_path'] = installer_path
    return record

    
def retrieve_installer_folders(toolkit_folder, product_name, newer_than_date):
    """
    Get the installer folers from the `toolkit_folder` whose product name 
    is `product_name` (myRIO or roboRIO) and whose date is newer than 
    `newer_than_date`
    """
    date_folders = os.listdir(toolkit_folder)
    date_folders = filter(lambda folder_name: folder_name.split('_')[0] > newer_than_date, 
                        date_folders)
    installer_folders = map(lambda date_folder: os.path.join(toolkit_folder, date_folder, product_name), 
                        date_folders)
    return installer_folders



if __name__ == '__main__':
    product_name = 'myRIO'
    toolkit_folder = r'\\us-aus-argo\NISoftwarePrerelease\myRIO\Toolkit\3.1\Daily'
    NEWER_THAN_DATE = '20150301'
    product_names = ['myRIO-1900', 'myRIO-1950']
    installer_folders = retrieve_installer_folders(toolkit_folder, product_name, NEWER_THAN_DATE)
    for installer_folder in installer_folders:
        print installer_folder
        try:
            print get_installer_record(installer_folder, product_names)
        except Exception as e:
            print 'Exception happend!'
            print e
