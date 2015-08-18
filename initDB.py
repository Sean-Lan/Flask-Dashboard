from model.DBUtilities import connect_db
import main_config
import LogConfig
import logging
import os

stack_dashboard_schema = 'model/DBSchmas/stack_dashboard.sql'
toolkit_installer_dashboard_schema = 'model/DBSchmas/toolkit_installer_dashboard.sql'
bundle_installer_dashboard_schema = 'model/DBSchmas/bundle_installer_dashboard.sql'
stack_test_result_schema = 'model/DBSchmas/stack_test_result.sql'

def init_db(year):
    logger = logging.getLogger(__name__)
    conn = connect_db()
    # Create stack_test_result table
    logger.info('CREATE TABLE stack_test_result_table')
    with open(stack_test_result_schema, 'rt') as f:
        schema = f.read()
        conn.executescript(schema)

    # Create stack_dashboard table
    logger.info('CREATE TABLE myrio_roborio_%s_stackdash_board', year)
    with open(stack_dashboard_schema, 'rt') as f:
        schema = f.read().format(year=year)
        conn.executescript(schema)

    # Create installer dashboard table
    logger.info('CREATE %s bundle and toolkit installer tables', year)
    schemas = [bundle_installer_dashboard_schema, toolkit_installer_dashboard_schema]
    # products = ['myrio', 'roborio']
    products = ['roborio','myrio']
    for schema_name in schemas:
        with open(schema_name, 'rt') as f:
            schema = f.read()
            for product_name in products: 
                conn.executescript(schema.format(product_name=product_name, year=year))

if __name__ == '__main__':
    LogConfig.init_logging()

    # make sure the db file in the cwd.
    cwd = os.path.dirname(__file__)
    if cwd != '':
        os.chdir(os.path.dirname(__file__))

    init_db(main_config.CURRENT_YEAR)
