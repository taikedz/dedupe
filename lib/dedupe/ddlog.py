import logging

__dedupe_logger = None
__dedupe_logger_handler = None

def getLogger(name="dedupe", level=logging.INFO):
    if __dedupe_logger == None:
        __createLogger(name, level)

    return __dedupe_logger

def setLevel(level, name="dedupe"):
    getLogger(name, level)

    __dedupe_logger.setLevel(level)
    __dedupe_logger_handler.setLevel(level)

def __createLogger(name, level):
    global __dedupe_logger
    global __dedupe_logger_handler

    __dedupe_logger = logging.getLogger(name)
    __dedupe_logger.setLevel(level)

    __dedupe_logger_handler = logging.StreamHandler()
    __dedupe_logger_handler.setLevel(level)

    __dedupe_logger.addHandler(__dedupe_logger_handler)
