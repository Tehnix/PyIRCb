#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Wrapper for the IRC bot.

"""

import settings


def main():
    # Testing the settings
    settingsInstance = settings.Settings()
    for i, j in settingsInstance.servers.items():
        print i
        for k, z in j.channels.items():
            print k
            print z.name


if __name__ == '__main__':
    main()
