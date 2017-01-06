#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2017 by Reiner Rottmann <reiner@rottmann.it>.
Released under GPLv3 or later: https://www.gnu.org/licenses/gpl-3.0.txt
"""

import os
import re
import sys
import time
import logging
import argparse
import datetime

__version__ = "0.1"


def _get_ctime(path):
    '''Get the creation time of the given file.'''
    fmt = "%y%m%d"
    ctime = datetime.datetime.strptime(time.ctime(os.path.getctime(path)), "%c").strftime(fmt)
    return ctime


def _manage_tags(path, addtags=None, removetags=None, tagctime=True, sorttags=True, preservetags=True):
    '''
    Add/Remove given tags to the file described by path.
    Decide whether to append a tag with the file's ctime.
    Decide whether to sort the tags alphabetically.
    Decide whether to preserve original tags.
    '''
    if removetags is None:
        logging.debug('No tags to remove.')
        removetags = []
    if addtags is None:
        addtags = []
    if tagctime:
        addtags = addtags + [_get_ctime(path)]
    for tag in addtags:
        if tag in removetags:
            if tag in addtags:
                addtags.remove(tag)
    if len(addtags) == 0 and not removetags:
        logging.debug('No tags to add or remove.')
        return path
    regex = '(?P<name>^.*)\[(?P<tags>[^\[]+)\](?P<ext>.*$)'
    fname = os.path.basename(path)
    dir = os.path.dirname(path)
    m = re.search(regex, fname)
    if m:
        logging.debug('File has been tagged before.')
        oldtags = m.group('tags').split()
        if preservetags:
            logging.debug('Using old tags: ' + ','.join(oldtags))
        else:
            logging.debug('Ignoring old tags: ' + ','.join(oldtags))
            oldtags = []
        newtags = oldtags
        for tag in addtags:
            if tag not in oldtags:
                if tag not in removetags:
                    logging.debug('Adding tag: ' + tag)
                    newtags.append(tag)
        if removetags == ['*']:
            newtags=[]
        else:
            for tag in removetags:
                if tag in newtags:
                    logging.debug('Removing tag: ' + tag)
                    newtags.remove(tag)
        tags = newtags
        if sorttags:
            logging.debug('Sorting tags.')
            tags.sort()
        if len(tags) == 0:
            if m.group('ext').strip():
                newfname = m.group('name').strip() + m.group('ext').strip()
            else:
                newfname = m.group('name').strip()
        else:
            newfname = m.group('name').strip() + ' [' + ' '.join(newtags)+']'+m.group('ext').strip()
    else:
        logging.debug('The file is tagged for the first time.')
        ext = '.' + fname.split('.')[-1]
        name = fname[0:-len(ext)]
        if sorttags:
            logging.debug('Sorting tags.')
            addtags.sort()
        newfname = name + ' [' + ' '.join(addtags).strip() + ']' + ext
        logging.debug('Old filename: ' + fname)
        logging.debug('New filename: ' + newfname)
    cmd = 'mv "%s" "%s"' % (os.path.join(dir, fname), os.path.join(dir, newfname))
    return cmd


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', help='Enable debug output.', action='store_true')
    parser.add_argument('--nopreserve', help='Do not preserve original tags.', action='store_false')
    parser.add_argument('--nosorttags', help='Do not sort tags.', action='store_false')
    parser.add_argument('--notagctime', help='Do not add tag for ctime.', action='store_false')
    parser.add_argument('--path',
                        help='Path to file/dir to tag.',
                        default='.',
                        required=True)
    parser.add_argument('--quiet', help='Quiet mode.', action='store_true')
    parser.add_argument('--addtags',
                        help='Comma seperated list of tags to add.',
                        default=None)
    parser.add_argument('--removetags',
                        help='Comma seperated list of tags to remove. * to remove all.',
                        default=None)
    args = parser.parse_args()
    if args.quiet:
        logging.basicConfig(level=logging.CRITICAL, format='#%(levelname)s: %(message)s')
    else:
        if args.debug:
            logging.basicConfig(level=logging.DEBUG, format='#%(levelname)s: %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='#%(levelname)s: %(message)s')
    if not os.path.exists(args.path):
        logging.error('No such file or directory: ' + args.path)
        sys.exit(1)
    if args.addtags is not None:
        addtags = args.addtags.split(',')
    else:
        addtags = []
    if args.removetags is not None:
        removetags = args.removetags.split(',')
    else:
        removetags = []
    print _manage_tags(args.path, addtags, removetags, args.notagctime, args.nosorttags, args.nopreserve)
