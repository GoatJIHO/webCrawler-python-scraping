import logging
from datetime import datetime

class CrawlerLogger:
    """
    DEBUG : 디버그 정보 (10)
    INFO : 작업의 정상 작동 로그 (20)
    WARNING : 작업은 진행 되나, 문제 발생점 명시 (30)
    ERROR : 함수의 실행 문제 (40)
    CRITICAL : 프로그램 동작 실패 (50)

    site_name 에 해당하는 logger 생성
    """
    def __init__(self, site_name: str):
        self.logger = logging.getLogger(site_name)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(messages)s")

    def console_log(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)
        logger.addHandler(stream_handler)

    def file_log(self):
        file_handler = logging.FileHandler(f'./logs/{site_name}.log')
        file_handler.setFormatter(self.formatter)
        logger.addHandler(file_handler)

    def log_info(self, message: str):
        self.logger.info(message)

    def log_error(self, message: str):
        self.logger.error(message)

    def log_warning(self, message: str):
        self.logger.warning(message)

    def log_critical(self, message: str):
        self.logger.critical("Error: ", message)
