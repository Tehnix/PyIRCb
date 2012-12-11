#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Wrapper for the IRC bot.

"""

from optparse import OptionParser

import src.utilities as util
import src.settings
import src.irc.botDispatcher

__VERSION__ = "2.2.0"
PARSER_DESC = "A python based IRC bot"
PARSER_USAGE = """%prog [options]"""

parser = OptionParser(description=PARSER_DESC, usage=PARSER_USAGE)
parser.add_option(
    "-c",
    "--conf",
    dest="conf",
    default=False,
    action="store_true",
    help="generate a default configuration file"
)
parser.add_option(
    "-v",
    "--verbose",
    dest="verbose",
    default=False,
    action="store_true",
    help="makes the bot verbose"
)

(options, args) = parser.parse_args()

def main():
    util.verbose = options.verbose
    if options.conf:
        settingsInstance = src.settings.Settings(
            generateConf=options.conf
        )
    else:
        botDispatcherInstance = src.irc.botDispatcher.BotDispatcher()

if __name__ == '__main__':
    main()
