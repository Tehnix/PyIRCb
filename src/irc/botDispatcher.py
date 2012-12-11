#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IRC bot...

"""

import threading

import src.utilities as util
import src.settings
import src.irc.botObject


class BotDispatcher(threading.Thread):
    """
    The BotDispatcher object handles the delegation of the various bots on
    the various specified servers.
    
    One Bot object for each server (call name), meaning several bots can be
    connected to the same address.
    
    All bots are stored in the botObjects class variable.
    
    """
    
    botObjects = {}
    
    def __init__(self):
        """Prepare the object and fire off the dispatch method."""
        super(BotDispatcher, self).__init__()
        self.settingsInstance = src.settings.Settings()
        self.dispatch()
        
    def dispatch(self):
        """Create one Bot object for each server and start it in threads."""
        servers = self.settingsInstance.settings['servers']
        for name, info in servers.items():
            self.botObjects[name] = src.irc.botObject.BotObject(
                self.settingsInstance.settings,
                info
            )
            thread = threading.Thread(
                target=self.botObjects[name].connectToServer
            )
            thread.start()
    
    def destroyBot(self, botObjName):
        """Gracefully shut down the bot and remove it from self.botObjects."""
        try:
            self.botObjects[botObjName].destroy()
            del self.botObjects[botObjName]
            util.write("Bot %s has been detroyed." % botObjName)
        except KeyError:
            util.write(
                "Bot %s does not exist." % botObjName, 
                outputType="Warning"
            )
    
    def reloadBot(self, botObjName):
        """First destroy the Bot object and then reinstantiate it."""
        try:
            info = self.botObjects[botObjName].info
        except KeyError:
            info = None
        if info is not None:
            self.destroyBot(botObjName)
            self.botObjects[botObjName] = src.irc.botObject.BotObject(info)
            util.write("Bot %s has been reloaded." % botObjName)
        else:
            util.write(
                "Bot %s does not exist." % botObjName, 
                outputType="Warning"
            )

            