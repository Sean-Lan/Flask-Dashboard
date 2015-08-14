"""
    If you find my code is tedious, congratulations! My code sucks because
    the demand sucks. Look, the final parsed results look like this:
    {'results': 
        {'Windows 7 (32-bit SP1 English)': 
                {'roboRIO': 1.0, 
                 'myRIO-1950': 1.0, 
                 'myRIO-1900': 0.77},
         ...
        },
      'crio_date': '20150624_1715f3'
    }
    and the raw test results are even scaring:
    {'results': 
        {'Windows 7 (32-bit SP1 English)': 
                {'roboRIO': 
                    {'Test_Install Software.vi': 'Passed', 
                     'test_upgrading_firmware target.vi': 'Passed',
                     'test_renaming target.vi': 'Passed', 
                     'test_format target.vi': 'Passed'}, 
                 'myRIO-1950': 
                    {'Test_Install Software.vi': 'Passed',
                     'test_upgrading_firmware target.vi': 'Passed', 
                     'test_renaming target.vi': 'Passed',
                     'test_format target.vi': 'Passed'}, 
                 'myRIO-1900': 
                    {'Test_Install Software.vi': 'Avoided', 
                     'test_upgrading_firmware target.vi': 'Passed', 
                     'test_renaming target.vi': 'Passed', 
                     'test_format target.vi': 'Failed'}
                }
        ...
        }, 
     'crio_date': '20150624_1715f3'
    }
    and even even awful if you dig into the csv files. (WTF...)
    I write down this to calm you down, and hope you won't maintain my code.
    OKay, here is the doc for this module! :)
"""

import csv
import os
import re
import BeautifulSoup

def get_test_result_from_csv_file(file_name):
    """
    Paser the csv file to obtain the test result in the file.
    The test results are returned as a dict, which contains:
    'target_model' : 'myRIO-1900', 'myRIO-1950', or 'roboRIO'
    test_name : test_result
    """
    test_results = {}
    test_name = ""
    reader = csv.reader(file(file_name,'rb'))
    for line in reader:
        if len(line) == 0:
            continue
        if line[0].strip() == "Test Name:":
            test_name = line[1]
            continue
        if line[0].strip() == "Test Result:":
            test_results[test_name] = line[1]
        if line[0].strip() == "Target Model:":
            test_results['target_model'] = line[1]
    return test_results


def get_csv_files_from_os_directory(os_directory):
    csv_files = []
    for root, dirs, files in os.walk(os_directory):
        for file_name in files:
            if os.path.splitext(file_name)[1] == '.csv':
                csv_files.append(os.path.join(root, file_name))
    return csv_files


def get_target_results_from_cvs_files(csv_files):
    """
    Group the test results according to the 'target_model'
    """
    target_results = {}
    for csv_file in csv_files:
        results = get_test_result_from_csv_file(csv_file)
        target_model = results.pop('target_model')
        if target_model not in target_results:
            target_results[target_model] = dict()
        target_results[target_model].update(results)
    return target_results


def get_daily_directories(test_base_directory):
    daily_directories = os.listdir(test_base_directory)
    daily_directories = map(lambda dir_name: os.path.join(test_base_directory, dir_name),
                            daily_directories)
    return daily_directories


def get_os_names_from_daily_directory(daily_directory):
    os_names = []
    for name in os.listdir(daily_directory):
        if os.path.isdir(os.path.join(daily_directory, name)):
             os_names.append(name)
    return os_names


def get_csv_files_from_daily_directory(daily_directory):
    """
    Group csv files according to the os.
    """
    os_names = get_os_names_from_daily_directory(daily_directory)
    os_csv_dict = {}
    for os_name in os_names:
        os_csv_dict[os_name] = {}
        os_directory = os.path.join(daily_directory, os_name)
        csv_files = get_csv_files_from_os_directory(os_directory)
        os_csv_dict[os_name] = csv_files
    return os_csv_dict

def get_daily_results_from_daily_directory(daily_directory):
    os_csv_dict = get_csv_files_from_daily_directory(daily_directory)
    daily_results = {}
    build_info_xml = os.path.join(daily_directory, 'BuildInfo.xml')
    daily_results['crio_date'] = get_crio_date_from_build_info_xml(build_info_xml)
    daily_results['results'] = {}
    for os_name in os_csv_dict:
        daily_results['results'][os_name] = {}
        daily_results['results'][os_name] = \
        get_target_results_from_cvs_files(os_csv_dict[os_name])
    return daily_results


def calculate_pass_rate(test_result, rating_dict, default_weight):
    numerator = 0
    denumerator = 0
    for test_vi_name, result in test_result.items():
        passed = 0
        if result == "Avoided" or result == "Disabled":
            continue
        elif result == "Passed":
            passed = 1

        if test_vi_name in rating_dict:
            if rating_dict[test_vi_name] == 5 and passed == 0:
                return 0.0
            denumerator += rating_dict[test_vi_name]
            numerator += rating_dict[test_vi_name] * passed
        else:
            denumerator += default_weight
            numerator += default_weight * passed

    if numerator == 0:
        return 0.0
    return numerator/float(denumerator)


def parse_test_result(daily_results, rating_dict, default_weight):
    parsed_results = {}
    parsed_results['crio_date'] = daily_results['crio_date']
    parsed_results['results'] = {}
    for os_name, target_results in daily_results['results'].items():
        parsed_results['results'][os_name] = {}
        for target_model, results in target_results.items():
            parsed_results['results'][os_name][target_model] = \
                    calculate_pass_rate(results, rating_dict, default_weight)
    return parsed_results


def get_crio_date_from_build_info_xml(build_info_xml):
    soup = BeautifulSoup(open(build_info_xml).read(), 'lxml')
    def is_crio_tag(tag):
        return tag.has_attr('path') and tag['path'].endswith('NICRIO')
    crio_tag = soup.find(is_crio_tag)
    # d - daily, a - alpha, b - beta, f - final
    date_pattern = re.compile(r'\d{8}_\d+[dabf]\d+')
    match = date_pattern.search(crio_tag['path'])
    return match.group()


if __name__ == '__main__':
    # file_name = r'C:\Users\xlan\Desktop\SanityTest\20160104_151351\Windows 7 (32-bit SP1 English)\2015-07-22_18-54-34_myRIO Format Target_ATS.csv'
    # results = get_test_result_from_csv_file(file_name)
    # print results

    daily_directory = r'C:\Users\xlan\Desktop\SanityTest\20160104_151351'
    daily_results = get_daily_results_from_daily_directory(daily_directory)
    print daily_results

    rating_dict = {
        'Test_Install Software.vi': 5, 
        'test_upgrading_firmware target.vi': 4, 
        'test_renaming target.vi': 3, 
        'test_format target.vi':  2
    }
    default_weight = 3

    parsed_results = parse_test_result(daily_results, rating_dict, default_weight)
    print parsed_results
