#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import *
import threading


from ircbot import bot


# Bot version number
BOT_VERSION = "1.0.0"
# Bot deployment details
BOT_DEPLOYMENT = ".py"


parser_desc = """
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

parser_usg = """%prog [options]"""

parser = OptionParser(description = parser_desc, usage = parser_usg)
parser.add_option("-r", "--run", dest="run", default=False, action="store_true",
                  help="Start the bot with the saved settings (use -s to set settings)")
parser.add_option("-i", "--ident", dest="identify", action="store", nargs=1,
                  help="If set, the bot will try to identify with pass (must be run with -r). Usage: -i <pass>")
parser.add_option("-g", "--get", dest="get", default=False, action="store_true",
                  help="Print the variables set", metavar="get_variables")
parser.add_option("-c", "--clear", dest="clear", default=False, action="store_true",
                  help="Clear all variables", metavar="clear_variables")
parser.add_option("-l", "--ssl", dest="ssl", default=False, action="store_true",
                  help="Use SSL to connect", metavar="use_SSL")
parser.add_option("-j", "--just", dest="just", action="store", nargs=1,
                  help="Connect just to server with id. Usage: -j <id>")
parser.add_option("-o", "--operator", dest="cmd_op", action="store", nargs=1,
                  help="Sets operator sign to be used as prefix to commands. Usage: -o <operator>")
parser.add_option("-d", "--del", dest="del_id", action="store", nargs=1,
                  help="Deletes setting with id. Usage: -d <id>")
parser.add_option("-a", "--admin", dest="add_admin", action="store", nargs=2,
                  help="Adds admin to database. Usage: -a <username> <password>")
parser.add_option("-u", "--use", dest="use", action="store", nargs=4,
                  help="Starts bot with specified settings. Usage: -u <nick> <host> <port> <channels>")
parser.add_option("-s", "--set", dest="set", action="store", nargs=5,
                  help="Saves a setting. Usage: -s <id> <nick> <host> <port> <channels>")

(options, args) = parser.parse_args()



if __name__ == '__main__':
    ircbot = bot.IrcBot(host='46.38.57.109', channels={'#hq'})
    thread = threading.Thread(target=ircbot.run_bot)
    thread.start()
    pass