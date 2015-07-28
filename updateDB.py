from model.DBUtilities import Model
from StackInfoRetriever import niweb
import main_config
import LogConfig
import logging
def get_stack_date(stack_name):
    return stack_name[10:18]


def newer_than_date(stack_name, date):
    return get_stack_date(stack_name) > date


if __name__ == '__main__':
    LogConfig.init_logging()
    logger = logging.getLogger(__name__)
    model = Model('myrio_roborio_2016_stack_dashboard')
    column_list = ['validated_stack',]
    exist_stacks = [stack['validated_stack'] for stack in model.select(column_list)]

    stack_urls = niweb.extract_valid_stack_urls(main_config.STACK_WEB_URL)
    stack_url_dict = niweb.convert_stackurl_list_to_dict(stack_urls)
    for stack_name in sorted(stack_url_dict.keys()):
        try:
            if newer_than_date(stack_name, '20150301') and stack_name not in exist_stacks:
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
            pass
    

    





    




