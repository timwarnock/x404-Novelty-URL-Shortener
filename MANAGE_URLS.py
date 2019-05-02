#!/usr/bin/env python
# vim: set fileencoding=utf-8 tabstop=4 shiftwidth=4 autoindent smartindent:
''' Usage: MANAGE_URLS.py command [options]

    Where command includes:
    add [url]        * e.g., add http://www.anattatechnologies.com/
    get [key]        * e.g., get esza (returns the matching url)
    edit [key] [url] * update the entry matching to key
    list [type]      * list all entries by type in csv

'''
import os
import sys
import argparse
import traceback

import x404
#TODO import ConfigParser


##
## GLOBALS
DBFILE = 'x404.db'
SURL = x404.ShortURLDB.ShortURLDB(DBFILE)
NN = x404.NovelNum.NovelNum()


def add(url):
    return SURL.add(url)

def get(key):
    return SURL.resolve(key)

def edit(key, url):
    rowid = NN.decode(key)
    return SURL._edit(rowid, url)

def print_list(type):
    rows = SURL.list(type)
    for row in rows:
        print u",".join(map(unicode, row))

def load(filename):
    SURL._loadURLs(filename)
    return ""

def drop():
    SURL._newdb()
    return ""


def requireArgs(n,testn):
    if testn < n:
        raise ValueError('not enough arguments')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='''MANAGE_URLS.py <command> [<args>]

    add [url]        * e.g., add http://www.anattatechnologies.com/
    get [key]        * e.g., get esza (returns the matching url)
    edit [key] [url] * update the entry matching to key
    list [type]      * list all entries by type in csv
    load [filename]  * load a file of URLs into the database
    drop             * delete all URLs from the database

''')
    parser.add_argument('command', help='command to run: add, get, edit, list')
    parser.add_argument('-d', '--debug', help='debug', action='store_true')
    parser.add_argument('vars', nargs="*", help='arguments needed by command, like the URL or key')
    args = parser.parse_args()
    try:
        if args.command == "add":
            requireArgs(1,len(args.vars))
            print add(args.vars[0])
        elif args.command == "get":
            requireArgs(1,len(args.vars))
            print get(args.vars[0])
        elif args.command == "edit":
            requireArgs(2,len(args.vars))
            print edit(args.vars[0], args.vars[1])
        elif args.command == "list":
            requireArgs(1,len(args.vars))
            print_list(args.vars[0])
        elif args.command == "load":
            requireArgs(1,len(args.vars))
            print load(args.vars[0])
        elif args.command == "drop":
            print drop()
    except:
        parser.print_help()
        if args.debug:
            print traceback.format_exc()
        exit(1)


