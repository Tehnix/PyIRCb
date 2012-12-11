#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Wrapper for the IRC bot.

"""

import os
import argparse

import src.utilities as util
import src.settings
import src.irc.botDispatcher

__VERSION__ = '2.3.0'
PARSER_DESC = 'A python based IRC bot'

parser = argparse.ArgumentParser(description=PARSER_DESC)
parser.add_argument(
    '-c',
    '--config',
    dest='conf',
    action='store_true',
    default=False,
    help='generate a default configuration file'
)
parser.add_argument(
    '-v',
    '--verbose',
    dest='verbose', 
    action='store_true',
    default=False,
    help='print output to stdout'
)
parser.add_argument(
    '-m'
    '--module',
    dest='module',
    nargs=1, 
    default=False, 
    help='generate a module scaffold'
)

options = parser.parse_args()


class UpdateSourceCode(Exception):
    pass


def main():
    try:
        util.verbose = options.verbose
        if options.module:
            modName = options.module[0].lower()
            if ' ' in modName:
                print("Modules can't have spaces in them!")
            else:
                createScaffold(modName)
        elif options.conf:
            settingsInstance = src.settings.Settings(
                generateConf=options.conf
            )
        else:
            botDispatcherInstance = src.irc.botDispatcher.BotDispatcher()
    except UpdateSourceCode:
        print('You know, I could totally update the source code and suche here...')

def createScaffold(modName):
    basePath = os.path.join('src', 'modules')
    modPath = os.path.join(basePath, modName)
    with open(os.path.join(basePath, 'module.txt'), 'r') as moduleScaffold:
        scaffold = moduleScaffold.read().replace('{ #MODULENAME }', modName).replace('{ #CLASSNAME }', modName.title())
        if not os.path.exists(modPath):
            os.makedirs(modPath)
        with open(os.path.join(modPath, modName + '.py'), 'w') as moduleFile:
            moduleFile.write(scaffold)
        with open(os.path.join(modPath, '__init__.py'), 'w') as initFile:
            initFile.write('')

if __name__ == '__main__':
    main()
