# -*- coding: utf-8 -*-
import traceback
import logging
from logging.handlers import TimedRotatingFileHandler


def loggerInFile(func):
    def inner(*args, **kwargs):
        logFilePath = "./log.txt"
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        handler = TimedRotatingFileHandler(logFilePath, when="d", interval=1, backupCount=5)
        formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        try:
            func(*args, **kwargs)
        except:
            logger.info("funcName: {0}, args: {1}, kwargs: {2}".format(func.__name__, args, kwargs))
            logger.error(traceback.format_exc())

    return inner


@loggerInFile
def a():
    t = 1 / 0


if __name__ == "__main__":
    a()
