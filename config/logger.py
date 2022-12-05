# encoding: utf-8
import json
import logging
import sys
from typing import List, Dict

colored = True
# log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)'
log_format = (
    '%(asctime)s - '
    '%(levelname)s - '
    '%(funcName)s - '
    '%(message)s'
)


class CustomFormatter(logging.Formatter):
    grey = '\x1b[38;21m'
    yellow = '\x1b[33;21m'
    red = '\x1b[31;21m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'


    FORMATS = {
        logging.DEBUG: grey + log_format + reset,
        logging.INFO: grey + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def config_logger(verbose: bool):
    """logger configuration"""
    level = logging.INFO
    if verbose:
        level = logging.DEBUG
    formatter = logging.Formatter(log_format)
    if colored:
        formatter = CustomFormatter()
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(formatter)
    logging.basicConfig(level=level, handlers=[sh])


def pprint(fw: List[Dict]):
    print(json.dumps(fw, indent=4, sort_keys=True))
