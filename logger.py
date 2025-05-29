import logging

from main.infrastructure.interfaces import ILogger


class Logger(ILogger):

    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def info(self, message):
        self.__logger.info(message)

    def error(self, message, exc_info=True):
        self.__logger.error(message, exc_info=exc_info)

    def warning(self, message):
        self.__logger.warning(message)

    def debug(self, message):
        self.__logger.debug(message)
