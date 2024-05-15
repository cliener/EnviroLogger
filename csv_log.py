#!/usr/bin/python3

import logging
from logging.handlers import RotatingFileHandler

LOG_FILE_NAME = 'log.csv'
LOG_MAX_SIZE = 4096 # Max size of each log file in bytes
LOG_MAX_FILES = 4 # Max of files count
LOG_HEADER = ['date', 'value_1', 'value_2'] # Pass None for no csv header
LOG_FORMAT = '%(message)s' # Log record format can use: asctime, levelname
LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

class CsvFormatter(logging.Formatter):

    def format_msg(self, msg):
        '''Format the msg to csv string'''
        if isinstance(msg, list):
            msg = ','.join(map(str, msg))
        return msg

    def format(self, record):
        record.msg = self.format_msg(record.msg)
        return logging.Formatter.format(self, record)


class CsvRotatingFileHandler(RotatingFileHandler):

    def __init__(self, fmt, datefmt, filename, max_size, max_files, header=None):
        handler = RotatingFileHandler.__init__(self, filename, maxBytes=max_size, backupCount=max_files)
        self.formatter = CsvFormatter(fmt, datefmt)
        # Format header string if needed
        self._header = header and self.formatter.format_msg(header)

    def rotation_filename(self, default_name):
        '''Make log files counter before the .csv extension'''
        s = default_name.rsplit('.', 2)
        return '{}_{:0{}d}.csv'.format(s[0], int(s[-1]), self.backupCount // 10 + 1)

    def doRollover(self):
        '''Apped header string to each log file'''
        RotatingFileHandler.doRollover(self)
        if self._header is None:
            return
        f = self.formatter.format
        self.formatter.format = lambda x: x
        self.handle(self._header)
        self.formatter.format = f


class RotatingCsvLogger(logging.Logger):
    def __init__(self, level, fmt, datefmt, filename, max_size, max_files, header=None):
        logging.Logger.__init__(self, filename.rsplit('.', 1)[0], level)
        handler = CsvRotatingFileHandler(fmt, datefmt, filename, max_size, max_files, header)
        self.addHandler(handler)
