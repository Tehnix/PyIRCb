#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Wrapper for the IRC bot.

"""

import src.irc.dispatcher


def main():
    botDispatcherInstance = src.irc.dispatcher.BotDispatcher()

if __name__ == '__main__':
    main()
