import logging
from datetime import datetime
now=datetime.now()


class Logger():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.time=now.strftime("%Y-%m-%d %H:%M:%S")

    def info(self, message):
        self.logger.info(f"[{self.time}] {message}")

    def error(self, message):
        self.logger.error(f"[{self.time}] {message}")

    def warning(self, message):
        self.logger.warning(f"[{self.time}] {message}")

    def debug(self, message):
        self.logger.debug(f"[{self.time}] {message}")

logger=Logger()