#!/usr/bin/env python
# encoding: utf-8
import argparse
import logging
import os.path
import sys

from config import config_logger
from metadata import process_images


def get_args() -> argparse.Namespace:
    """create scripts arguments and parse console arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--verbosity',
        help='increase output verbosity',
        nargs='?', const=1, type=bool, default=False)
    parser.add_argument(
        '-i', '--input',
        dest='input',
        help='path to files "--directory=~/input"',
        required=True, nargs='?', type=str)
    parser.add_argument(
        '-o', '--output',
        dest='output',
        help='path to output directory "--directory=~/output"',
        required=True, nargs='?', type=str)
    parser.add_argument(
        '-m', '--max-date',
        dest='max_date',
        help='max allowed date',
        nargs='?', const=1, type=str, default='')
    return parser.parse_args()


def main():
    args = get_args()
    config_logger(args.verbosity)
    logger = logging.getLogger('epub-updater')
    if not os.path.isdir(args.input):
        logger.error(f'not found directory {args.input}')
        sys.exit(1)
    if not os.path.isdir(args.output):
        logger.error(f'not found directory {args.output}')
        sys.exit(1)
    logger.info('****************** Starting Application *****************')
    process_images(args.input, args.output, args.max_date)
    logger.info('****************** Terminating Application *****************')


if __name__ == '__main__':
    main()
