#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Starts the ircbot and runs it with supplied arguments.

"""
from optparse import OptionParser
import threading
import sys

from ircbot import bot


# Bot version number
__MODULE_VERSION__ = "1.3.0"
# Bot deployment details
__MODULE_DEPLOYMENT__ = ".py"

PARSER_DESC = """
,----------------------------------------------------------------------------,
| .            .                    .      .           .        .            |
|     ///////////////////// .////////////////   .  //////               .    |
|    /////////////////////  //////////////////    //////      .     .        |
|    .     //////   .        .         //////    //////                      |
| .       //////        .      //////////////   //////////////////       .   |
|        //////   .          ///////////////   //////////////////            |
|       //////                    .  //////   //////      //////    .        |
|   .  //////            //////////////////  //////   .  //////             .|
|     //////    .       /////////////////   //////      //////   b0t         |
| .         .       .         . Zeal Development     .     .     .     .     |
|----------------------------------------------------------------------------|
|                    T3hb0t - A Python based IRC bot                         |
|----------------------------------------------------------------------------|
|Author: Chrules at Zeal                                                     |
|Info: T3hb0t is an IRC bot client capable of connecting to multiple servers |
|and channels. Easily customized and easy to add commands.                   |
|                                                                            |
|Default operator prefix is ! . Can be set with -o option. If using -i <pass>|
|to identify, the nick must be registered beforehand (some servers require   |
|email activation !).                                                        |
|______-________-________-________-________-________-________-________-______|
"""

PARSER_USAGE = """%prog [options]"""

PARSER = OptionParser(description=PARSER_DESC, usage=PARSER_USAGE)
PARSER.add_option(
    "-r",
    "--run",
    dest="run",
    default=False,
    action="store_true",
    help="Start the bot with the saved settings (use -s to set settings)"
)
PARSER.add_option(
    "-i",
    "--ident",
    dest="identify",
    action="store",
    nargs=1,
    help="If set, the bot will try to identify with pass (must be run with\
     -r). Usage: -i <pass>"
)
PARSER.add_option("-g",
    "--get",
    dest="get",
    default=False,
    action="store_true",
    help="Print the variables set", metavar="get_variables"
)
PARSER.add_option(
    "-c",
    "--clear",
    dest="clear",
    default=False,
    action="store_true",
    help="Clear all variables", metavar="clear_variables"
)
PARSER.add_option(
    "-l",
    "--ssl",
    dest="ssl",
    default=False,
    action="store_true",
    help="Use SSL to connect", metavar="use_SSL"
)
PARSER.add_option(
    "-j",
    "--just",
    dest="just",
    action="store",
    nargs=1,
    help="Connect just to server with id. Usage: -j <id>"
)
PARSER.add_option(
    "-o",
    "--operator",
    dest="cmd_op",
    action="store",
    nargs=1,
    help="Sets operator sign to be used as prefix to commands. Usage: -o\
     <operator>"
)
PARSER.add_option(
    "-d",
    "--del",
    dest="del_id",
    action="store",
    nargs=1,
    help="Deletes setting with id. Usage: -d <id>"
)
PARSER.add_option(
    "-a",
    "--admin",
    dest="add_admin",
    action="store",
    nargs=2,
    help="Adds admin to database. Usage: -a <username> <password>"
)
PARSER.add_option(
    "-u",
    "--use",
    dest="use",
    action="store",
    nargs=4,
    help="Starts bot with specified settings. Usage: -u <nick> <host> <port>\
     <channels>"
)
PARSER.add_option(
    "-s",
    "--set",
    dest="set",
    action="store",
    nargs=5,
    help="Saves a setting. Usage: -s <id> <nick> <host> <port> <channels>"
)
PARSER.add_option(
    "-v",
    "--verbose",
    dest="verbose",
    default=False,
    action="store_true",
    help="Makes the bot more verbose"
)
(OPTIONS, ARGS) = PARSER.parse_args()


def to_unicode(text):
    """Converts bytes to unicode"""
    if type(text) != str:
        try:
            text = str(text, encoding='UTF-8')
        except UnicodeDecodeError:
            text = "\n[WARNING] : Failed to decode bytes!\n"
        except TypeError:
            text = "\n[WARNING] : Failed to decode bytes!\n"
    return text


def log_output(text, file_name="bot_log.txt"):
    """Write text to file"""
    text = to_unicode(text)
    text = "[*] %s\n" % (text,)
    log = open(file_name, "a")
    log.write(text)
    log.close()


def main():
    """Starts the script"""
    operator = '?'
    if OPTIONS.cmd_op:
        operator = OPTIONS.cmd_op
    identify = False
    if OPTIONS.identify:
        identify = OPTIONS.identify
    ssl = False
    if OPTIONS.ssl:
        ssl = OPTIONS.ssl

    if OPTIONS.run:
        ircbot = bot.IrcBot(
            host='irc.freenode.net',
            info={
                'nickname': 'Innocence',
                'realname': 'Motoko Kusanagi',
                'channels': ['##zealdev'],
                'operator': str(operator),
                'identify': identify
            },
            use_ssl=ssl
        )
        thread = threading.Thread(
            target=ircbot.run_bot,
            args=(OPTIONS.verbose,)
        )
        thread.daemon = True
        thread.start()
    elif OPTIONS.use:
        ircbot = bot.IrcBot(
            host=OPTIONS.use[1],
            port=int(OPTIONS.use[2]),
            info={
                'nickname': OPTIONS.use[0],
                'realname': 'Motoko Kusanagi',
                'channels': OPTIONS.use[3].split(),
                'operator': str(operator),
                'identify': identify
            },
            use_ssl=ssl
        )
        thread = threading.Thread(
            target=ircbot.run_bot,
            args=(OPTIONS.verbose,)
        )
        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as catched:
        log_output(catched, "bot_crashlog.txt")
