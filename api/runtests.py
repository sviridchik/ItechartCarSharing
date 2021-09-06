#!/usr/bin/env python
import os
from argparse import ArgumentParser

from django.conf import settings
from django_nose import NoseTestSuiteRunner

os.environ['DJANGO_SETTINGS_MODULE'] = 'cars.settings'

settings.NOSE_ARGS = (
    '--nologcapture',
    '-s',
)

import sys


def runtests(**kwargs):
    test_args = kwargs.pop('test', None) or ['tests']
    kwargs.setdefault('interactive', False)

    test_runner = NoseTestSuiteRunner(**kwargs)

    failures = test_runner.run_tests(test_args)

    sys.exit(failures)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('test', nargs='*')
    NoseTestSuiteRunner.add_arguments(parser)
    test_arguments = parser.parse_args()

    runtests(**vars(test_arguments))
