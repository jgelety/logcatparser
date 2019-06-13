#!/usr/bin/env python
# coding: utf-8

"""This script parse logfile to look up for certain patterns in test result."""

__author__ = 'Jan Gelety'


import argparse
import datetime
import os
import sys


TEST_START = 'TEST STARTED'
TEST_END = 'TEST FINISHED'


def test_exec_time(log):
    """Prints out the time difference between lines containing TEST_START and
    TEST_END strings.

    :param Binary I/O log: Logfile to be parsed.
    """

    def get_datetime(ln_str):
        """Extract date and time data from line

        :param str ln_str: Line string.
        :returns: Dictionary of year, month, day, hour, minute, second and
            microsecond data.
        :rtype: dict
        """

        words = ln_str.split()
        date = words[0].split('-')
        time = words[1].split(':')
        time[2] = time[2].split('.')
        if len(date) == 3:
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
        else:
            year = datetime.date.today().year
            month = int(date[0])
            day = int(date[1])
        hour = int(time[0])
        minute = int(time[1])
        second = int(time[2][0])
        microsecond = int(time[2][1]) * 10 ** (6 - len(time[2][1]))

        return dict(year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    second=second,
                    microsecond=microsecond)

    test_started = False
    test_finished = False
    for line in log:
        if TEST_START in line:
            test_started = datetime.datetime(**get_datetime(line))
        elif TEST_END in line:
            test_finished = datetime.datetime(**get_datetime(line))
            break
    if test_started and test_finished:
        print('{sep}Test execution time: {delta}'.format(
            sep=os.linesep, delta=str(test_finished - test_started)))
    else:
        print('{sep}"{start}" and/or "{end}" string(s) not found.'.format(
            sep=os.linesep, start=TEST_START, end=TEST_END))


def print_include(log, words):
    """Print lines containing all required words.

    :param Binary I/O log: Logfile to be parsed.
    :param list words: List of words to look for.
    """

    print('{sep}Line(s) containing words {w}:'.format(sep=os.linesep, w=words))
    cmd = ' and '.join('"{w}" in line'.format(w=word) for word in words)
    found = 0
    for line in log:
        if eval(cmd):
            found += 1
            print(line.rstrip(os.linesep))
    if not found:
        msg = 'No line containing all required words.'
        print('=' * len(msg))
        print(msg)
    elif found == 1:
        msg = '1 line contains all required words.'
        print('=' * len(msg))
        print(msg)
    else:
        msg = '{nr} lines contain all required words.'.format(nr=found)
        print('=' * len(msg))
        print(msg)


def print_exclude(log, words):
    """Print lines not containing any of provided words.

    :param Binary I/O log: Logfile to be parsed.
    :param list words: List of words to look for.
    """

    print('{sep}Line(s) not containing any of words {w}:'.format(
        sep=os.linesep, w=words))
    cmd = ' or '.join('"{w}" not in line'.format(w=word) for word in words)
    found = 0
    for line in log:
        if eval(cmd):
            found += 1
            print(line.rstrip(os.linesep))
    if not found:
        msg = 'No line missing any of required words.'
        print('=' * len(msg))
        print(msg)
    elif found == 1:
        msg = '1 line missing any of  required words.'
        print('=' * len(msg))
        print(msg)
    else:
        msg = '{nr} lines missing any of required words.'.format(nr=found)
        print('=' * len(msg))
        print(msg)


def main():
    """Main function for the LogCat parser.
    """

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('logfile',
                        help='Logfile to be parsed.')
    parser.add_argument('-i',
                        nargs=1,
                        default=False,
                        metavar='args,...>',
                        help='Prints out lines containing all arguments.')
    parser.add_argument('-e',
                        nargs=1,
                        default=False,
                        metavar='<args,...>',
                        help='Prints out lines not containing any of provided '
                             'arguments.')
    parser.add_argument('-s',
                        action='store_true',
                        help='Prints out the time difference between lines '
                             'containing "{start}" and "{end}" strings.'.format(
                                start=TEST_START, end=TEST_END))

    args = parser.parse_args()

    if args.s:
        with open(args.logfile, 'r') as logfile:
            test_exec_time(logfile)
    if args.i is not False:
        with open(args.logfile, 'r') as logfile:
            print_include(logfile, args.i[0].split(','))
    if args.e is not False:
        with open(args.logfile, 'r') as logfile:
            print_exclude(logfile, args.e[0].split(','))


if __name__ == '__main__':
    sys.exit(main())
