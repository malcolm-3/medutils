#!/usr/bin/python

import click
import os
from datetime import datetime
from pathlib import Path

# be sure to update docstring if you change DEFAULT_IGNORE_GLOBS
DEFAULT_IGNORE_GLOBS = [
    '*~',
    '*.pyc',
    '#*',
    '.*',
    '*.OLD',
    'OLD'
    ]


@click.command()
@click.option('-i', '--ignore','ignore_patterns', multiple=True, type=str,
              help='glob patterns to ignore (likely needs to be quoted, and can be repeated)')
@click.option('-f', '--ignore-file', 'ignore_pattern_files', multiple=True, type=click.Path(exists=True),
              help='file with glob patterns (one per line) to ignore (can be repeated)')
@click.option('-n', '--no-default-ignore', is_flag=True,
              help='do not use default ignore globs')
@click.argument('touch_file', type=str)
@click.argument('paths_to_check', nargs=-1, type=click.Path(exists=True), required=True)
def touch_latest(touch_file, paths_to_check, ignore_patterns=(), ignore_pattern_files=(), no_default_ignore=False):
    """
    Find the latest changed date of file under the specified PATHS_TO_CHECK 
    and touch the TOUCH_FILE with that date (creating it if necessary).

    Files that match ignore patterns will be ignored when locating searching
    for the file with the latest change date.
    Patterns that contain slashes either need to be absolute (i.e. start
    with a slash) or they need to start with an asterisk in order
    to match anything. So any such pattern that doesn't have either
    will have an asterisk prepended.

    Directories which match an ignore pattern will not be traversed.
    Paths can be specified to ignore only from specific directories,
    e.g. '*/test/*.out'.

    Default ignore globs: '*~', '*.pyc', '#*', '.*' '*.OLD' 'OLD'

    \b
    touch_file: file to be touchead with the latest date
    paths_to_check: paths to search for the latest change date
    \f
    
    :param touch_file: file to be touchead with the latest date
    :param paths_to_check: paths to search for the latest change date
    :param ignore_patterns: glob patterns to ignore
    :param ignore_pattern_files: files of glob patterns to ignore
    :param no_default_ignore: if True do not include default glob patterns

    """
    ignore_patterns = IgnorePatterns()

    if not no_default_ignore:
        ignore_patterns.add_patterns(DEFAULT_IGNORE_GLOBS)
    for fn in ignore_pattern_files:
        with open(fn, 'r') as fh:
            ignore_patterns.add_patterns(fn)
    ignore_patterns.add_patterns(ignore_patterns)

    latest_timestamp = 0

    for path in paths_to_check:
        apath = os.path.abspath(path)
        for root, dirs, files in os.walk(apath):
            dirs[:] = [dn for dn in dirs if not ignore_patterns.ignore(root, dn)]
            for fn in files:
                if not ignore_patterns.ignore(root, fn):
                    statinfo = os.stat(os.path.join(root, fn))
                    if statinfo.st_mtime > latest_timestamp:
                        latest_timestamp = statinfo.st_mtime


class IgnorePatterns:

    def __init__(self, patterns=()):
        self.names = []
        self.paths = []
        self.add_patterns(patterns)

    def add_patterns(patterns):
        for pattern in patterns:
            pattern = pattern.strip()
            if '/' in pattern:
                if pattern[0] in '/*':
                    pattern = '*' + pattern
                self.paths.append(pattern)
            else:
                self.names.append(pattern)

    def ignore(self, dn, fn):
        for ignore_name in self.names:
            if fnmatch(fn, ignore_name):
                return True
        path = os.join(dn, fn)
        for ignore_path in self.paths:
            if fnmatch(path, ignore_path):
                return True
        return False


if __name__ == "__main__":
    touch_latest()
