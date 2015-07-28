import logging
import logging.handlers

LOG_FILENAME = 'runtime.log'
LOG_LEVEL = logging.DEBUG
MAX_BYTES = 5*1024*1024                 # 5M for each log file
BACKUP_COUNT = 5                        # 5 separate log files

def init_logging():
    """
    Config the logging module.
    Set the log level, add handler for file output and console output.
    """
    root_logger = logging.getLogger('')
    root_logger.setLevel(LOG_LEVEL)

    # add rotating file handler to the root logger
    file_handler = logging.handlers.RotatingFileHandler(
                    LOG_FILENAME, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    formatter = logging.Formatter(fmt='%(asctime)s %(name)s %(levelname)s \n\t%(message)s',
                                  datefmt='%m-%d %H:%M')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # add stream handler to the root logger
    console_handler = logging.StreamHandler()
    # set a format which is simpler for console log
    formatter = logging.Formatter(fmt='%(name)s %(levelname)s \n\t%(message)s')
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

if __name__ == '__main__':
    init_logging()
