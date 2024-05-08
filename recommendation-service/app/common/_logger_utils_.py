import os
import logging
from datetime import datetime as dt

class NoRequestsFilter(logging.Filter):
    def filter(self, record):
        return True #not record.name.startswith("requests")
    
def configure_logger(title:str):
    
    curr_dt = dt.now()
    log_dir = os.path.abspath(os.path.join(os.getcwd(), "../logs", title))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, mode=0o777, exist_ok=True)
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    filterer = NoRequestsFilter()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Console-Handler [LogLevel: WARNING]
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(filterer)

    # File-Handler [LogLevel: DEBUG]
    file_handler = logging.FileHandler(os.path.join(log_dir, f'{title.lower()}_log_{curr_dt.strftime("%Y%m%d_%H%M%S")}.txt'))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    console_handler.addFilter(filterer)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
