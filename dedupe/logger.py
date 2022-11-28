'''
General logging utility

When using get_logger(log_name, log_level) , a log folder is created either in
 the path defined by env var LOG_DIRECTORY or the current working directory the current working directory,
 at ./logs

A log file of the specified name is produced, logging at the specified level; along with a full log file,
 logging at debug level always.

The stderr will always print at INFO level and more-serious.

    import mylib.logger as logger
    LOG = logger.get_logger("my_log", log_level=logger.DEBUG)
    LOG.info("message") # available: debug(), info(), warning(), error()

Log level is optional and generally can be left at its default level (INFO).
'''

import os
import re
import shutil
import sys
import logging
import logging.handlers

# Make all these names directly available from this module
from logging import DEBUG, INFO, WARNING, ERROR

# Don't risk over-configuring an existing log
# Track those we've already seen requests for
__ALL_LOGGERS = {}
__FULL_FORMAT_STRING = '%(asctime)s | %(name)s | %(levelname)s %LE% %(message)s'
__LIVE_FORMAT_STRING = '%(asctime)s | %(name)s %LE% %(message)s'
__ALL_FORMATTERS = {}


def get_logger(log_name, log_level=INFO, file_location=None, inline=True):
    line_end = ":: "
    if not inline:
        line_end = "---::\n"

    if file_location is None:
        file_location = "{}.debug.log".format(log_name)

    full_format_string = __FULL_FORMAT_STRING.replace("%LE% ", line_end)
    live_format_string = __LIVE_FORMAT_STRING.replace("%LE% ", line_end)

    _validate_name(log_name)

    _logger, pre_existing = __get_existing_logger(log_name)

    if not pre_existing:
        # Some frameworks do their own logging and might
        #  duplicate our logs. Prevent this.
        _logger.propagate = False

        # Base level of detail
        # Any lesser messages than this level will be discarded
        #  before being passed to handlers
        # (Set debug to pass everything to handlers)
        _logger.setLevel(DEBUG)

        # Log to info level only in the console
        # We write messages to stderror, instead of the default stdout for console
        _add_stream_handler(_logger, live_format_string, INFO, sys.stderr)

        # Unified logging location retains logs at user-specfied level
        # Debug data can always be seen in the name-specific log
        _add_file_handler(_logger, full_format_string, log_level, "main_log.log".format(log_name), rotate=False)

        # Name-specific log. This will contain ALL the messages, including debug dumps
        _add_file_handler(_logger, full_format_string, DEBUG, file_location)

    return _logger


def __get_existing_logger(log_name):
    """ Get a logger, indicate whether it pre-existed
    @return (logger, pre_existed) : a logger, and whether it already existed
    """
    global __ALL_LOGGERS

    _logger = None

    if log_name in __ALL_LOGGERS:
        _logger = __ALL_LOGGERS[log_name]
        pre_existing = True

    else:
        _logger = logging.getLogger(log_name)
        __ALL_LOGGERS[log_name] = _logger
        pre_existing = False
    
    return _logger, pre_existing


# Handler utilities


def _formatter(fmt_string):
    global __ALL_FORMATTERS

    if fmt_string in __ALL_FORMATTERS:
        return __ALL_FORMATTERS[fmt_string]

    formatter = logging.Formatter(fmt_string)
    __ALL_FORMATTERS[fmt_string] = formatter

    return formatter


def _configure_handler(logger:logging.Logger, io_stream:logging.StreamHandler, fmt_string:str, log_level:str):
    io_stream.setLevel(log_level)
    io_stream.setFormatter(_formatter(fmt_string))
    logger.addHandler(io_stream)


def _add_stream_handler(logger, fmt_string, log_level, stream):
    stream_handler = logging.StreamHandler(stream=stream)
    _configure_handler(logger, stream_handler, fmt_string, log_level)


def _add_file_handler(logger, fmt_string, log_level, file_path, rotate=True):
    file_path = _get_log_path(file_path)

    if rotate:
        # Avoid creating monstruous single log files by creating a rotation
        # the logs are numbered and the latest log is always the lowest, or no number
        file_handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=2097152,
            backupCount=5,
            delay=1
        )
    else:
        file_handler = logging.FileHandler(file_path)

    _configure_handler(logger, file_handler, fmt_string, log_level)




def _get_log_path(file_name):
    # Note - if run on Linux, can be absolute
    # If run on Windows, may or may not work as an absolute path
    #  depending on whether run via MinGW or Powershell/Cmd.exe
    base_location = __get_log_dir()

    if not os.path.isdir(base_location):
        os.makedirs(base_location)

    full_path = os.path.join(base_location, file_name)

    return full_path


def __get_log_dir():
    base_location = os.getenv("LOG_DIRECTORY", ".")
    base_location = os.path.join(base_location, "logs")
    return base_location


def remove_log_dir():
    log_dir = __get_log_dir()
    shutil.rmtree(log_dir)


def _validate_name(file_name):
    if re.match("^[a-zA-Z0-9_.-]+$", file_name) == None or re.findall("[.-][.-]+", file_name):
        raise ValueError("Log name {} is invalid - can only contain letters, numbers, dashes and underscores; "
                         "dots and dashes may not be juxtaposed.".format(file_name))