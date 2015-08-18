from model.DBUtilities import Model
from utilities import niweb, installer, bundle, remove_path_prefix, testing
import main_config
import LogConfig
import logging
import os
def get_stack_date(stack_name):
    return stack_name[10:18]


def newer_than_date(stack_name, date):
    return get_stack_date(stack_name) > date


def update_stack_dashboard(table_name, stack_web_url, date):
    logger = logging.getLogger(__name__)
    model = Model(table_name)
    column_list = ['validated_stack',]
    exist_stacks = [record['validated_stack'] for record in model.select(column_list)]

    stack_urls = niweb.extract_valid_stack_urls(stack_web_url)
    stack_url_dict = niweb.convert_stackurl_list_to_dict(stack_urls)
    for stack_name in sorted(stack_url_dict.keys()):
        try:
            if newer_than_date(stack_name, date) and stack_name not in exist_stacks:
                logger.info('Construct record for %s', stack_name)
                record = niweb.construct_record_dict(stack_url_dict[stack_name])
                table_record = {
                        'validated_stack': record['Validated Stack'],
                        'validated_stack_url': record['stackUrl'],
                        'lv_version': record['lvVersion'],
                        'lv_api_version': record['lvAPIVersion'],
                        'safemode': record['Safemode']
                        }
                logger.info('The record is: %s', record)
                model.insert(table_record)
        except Exception as e:
            logger.warning('Exception happened: %s', e)


def update_toolkit_installer(table_name, toolkit_folder, name, products, date):
    logger = logging.getLogger(__name__)
    model = Model(table_name)
    column_list = ['installer_path',]
    exist_installers = [record['installer_path'] for record in model.select(column_list)]
    installer_folders = installer.retrieve_installer_folders(toolkit_folder, name, date)
    for installer_folder in installer_folders:
        if remove_path_prefix(installer_folder) in exist_installers:
            continue
        logger.info('Handle toolkit installer: %s', installer_folder)
        try:
            record = installer.get_installer_record(installer_folder, products)
            logger.info('The record is: %s', record)
            table_record = {
                    'installer_path': remove_path_prefix(record['installer_path']),
                    'lv_version': record['lvVersion'],
                    'lv_api_version': record['lvAPIVersion'],
                    'safemode': record['safemode']
                    }
            model.insert(table_record)
        except Exception as e:
            logger.warning('Exception happened: %s', e)


def update_bundle_installer(table_name, bundle_root, products, DVD_names, date):
    logger = logging.getLogger(__name__)
    model = Model(table_name)
    column_list = ['bundle_path',]
    exist_bundles = [record['bundle_path'] for record in model.select(column_list)]
    bundle_folders = bundle.retrieve_bundle_folders(bundle_root, date)
    for bundle_folder in bundle_folders:
        if remove_path_prefix(bundle_folder) in exist_bundles:
            continue
        logger.info('Handle bundle installer: %s', bundle_folder)
        try:
            record = bundle.get_bundle_record(bundle_folder, products, DVD_names)
            logger.info('The record is: %s', record)
            table_record = {
                    'bundle_path': remove_path_prefix(record['bundle_path']),
                    'toolkit_path': remove_path_prefix(record['installer_path']),
                    'lv_version': record['lvVersion'],
                    'lv_api_version': record['lvAPIVersion'],
                    'safemode': record['safemode'],
                    'actual_size': record['actual_size'],
                    'dedupe_size': record['idea_size']
                    }
            model.insert(table_record)
        except Exception as e:
            logger.warning('Exception happened: %s', e)


def update_stack_test_results(root_folder, rating_dict, default_weight):
    LogConfig.init_logging()
    logger = logging.getLogger(__name__)
    daily_folders = testing.get_daily_directories(root_folder)
    model = Model('stack_test_result')
    column_list = ['daily_folder',]
    parsed_folders = [record['daily_folder'] for record in model.select(column_list)]
    
    for daily_folder in daily_folders:
        if daily_folder in parsed_folders:
            continue
        try:
            daily_results = testing.get_daily_results_from_daily_directory(daily_folder)
            parsed_results = testing.parse_test_result(daily_results, 
                    rating_dict, default_weight)
            crio_date = parsed_results['crio_date']
            results = parsed_results['results']
            for os_name, pass_rates in results.items():
                for target_model, pass_rate in pass_rates.items():
                    table_record = {
                            'daily_folder': daily_folder,
                            'validated_stack': crio_date,
                            'os_name': os_name,
                            'target_name': target_model,
                            'pass_rate': pass_rate
                    }
                    model.insert(table_record)
        except Exception as e:
            logger.warning('Exception happened: %s', e)

        
def update_db(year):
    year = str(year)
    logger = logging.getLogger(__name__)

    logger.info('UPDATE TABLE myrio_roborio_%s_stack_dashboard', year)
    update_stack_dashboard('myrio_roborio_'+year+'_stack_dashboard', 
            main_config.STACK_WEB_URL, 
            main_config.NEWER_THAN_DATE)

    logger.info('UPDATE TABLE myrio_%s_toolkit_installer_dashboard', year)
    update_toolkit_installer('myrio_'+year+'_toolkit_installer_dashboard', 
            main_config.MYRIO_TOOLKIT_INSTALLER_DAILY_FOLDER, 
            'myRIO', 
            ['myRIO-1900'], 
            main_config.NEWER_THAN_DATE)

    logger.info('UPDATE TABLE roborio_%s_toolkit_installer_dashboard', year)
    update_toolkit_installer('roborio_'+year+'_toolkit_installer_dashboard', 
            main_config.ROBORIO_TOOLKIT_INSTALLER_DAILY_FOLDER, 
            'roboRIO', 
            ['roboRIO'], 
            main_config.NEWER_THAN_DATE)

    logger.info('UPDATE TABLE myrio_%s_bundle_installer_dashboard', year)
    update_bundle_installer('myrio_'+year+'_bundle_installer_dashboard', 
            main_config.MYRIO_BUNDLE_INSTALLER_DAILY_FOLDER, 
            ['myRIO-1900'], 
            ['myRIO_DVD1', 'myRIO_DVD2'],
            main_config.NEWER_THAN_DATE)

    logger.info('UPDATE TABLE roborio_%s_bundle_installer_dashboard', year)
    update_bundle_installer('roborio_'+year+'_bundle_installer_dashboard', 
            main_config.ROBORIO_BUNDLE_INSTALLER_DAILY_FOLDER, 
            ['roboRIO'], 
            ['roboRIO_DVD1', 'roboRIO_DVD2'], 
            main_config.NEWER_THAN_DATE)

    logger.info('UPDATE TABLE stack_test_result')
    update_stack_test_results(main_config.SANITY_TEST_ROOT_FOLDER,
            main_config.SANITY_TEST_RATING_DICT,
            main_config.SANITY_TEST_DEFAULT_WEIGHT)

if __name__ == '__main__':
    LogConfig.init_logging()

    # make sure the db file in the cwd.
    cwd = os.path.dirname(__file__)
    if cwd != '':
        os.chdir(os.path.dirname(__file__))

    update_db(main_config.CURRENT_YEAR)
