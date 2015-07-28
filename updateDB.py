from model.DBUtilities import Model
from utilities import niweb, installer
import main_config
import LogConfig
import logging
def get_stack_date(stack_name):
    return stack_name[10:18]


def newer_than_date(stack_name, date):
    return get_stack_date(stack_name) > date


def update_stack_dashboard(table_name, stack_web_url, date):
    logger = logging.getLogger(__name__)
    model = Model(table_name)
    column_list = ['validated_stack',]
    exist_stacks = [stack['validated_stack'] for stack in model.select(column_list)]

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
    column_list = ['myrio_daily_build_folder_path',]
    exist_installers = [stack['myrio_daily_build_folder_path'] for stack in model.select(column_list)]
    installer_folders = installer.retrieve_installer_folders(toolkit_folder, name, date)
    for installer_folder in installer_folders:
        if installer_folder in exist_installers:
            continue
        logger.info('Handle install: %s', installer_folder)
        try:
            record = installer.get_installer_record(installer_folder, products)
            table_record = {
                    'myrio_daily_build_folder_path': record['installer_path'],
                    'lv_version': record['lvVersion'],
                    'lv_api_version': record['lvAPIVersion'],
                    'safemode': record['safemode']
                    }
            logger.info('The record is: %s', record)
            model.insert(table_record)
        except Exception as e:
            logger.warning('Exception happened: %s', e)


if __name__ == '__main__':
    LogConfig.init_logging()

    # update_stack_dashboard('myrio_roborio_2016_stack_dashboard', main_config.STACK_WEB_URL, main_config.NEWER_THAN_DATE)

    update_toolkit_installer('myrio_2016_toolkit_installer_dashboard', 
            main_config.MYRIO_TOOLKIT_INSTALLER_DAILY_FOLDER, 
            'myRIO', 
            ['myRIO-1900','myRIO-1950'], 
            main_config.NEWER_THAN_DATE)
    


