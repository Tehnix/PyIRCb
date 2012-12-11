#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CloudFlare command...

"""

import urllib.request
import urllib.parse
import urllib.error
import json

import src.moduleBase
import src.utilities as util

class Cf(src.moduleBase.ModuleBase):
    """
    Interact with the CloudFlare API.
    """    

    def __init__(self, cmdInstance, cmdName=None, cmdArgs=None):
        super(Cf, self).__init__(cmdInstance, cmdArgs=cmdArgs)
        if cmdName is not None:
            self._execute(cmdName)
    
    
    def stats(self):
        """Pull out CloudFlare statistics."""
        cfSettings = self.settingsInstance.settings['commands']['cf']
        site = cfSettings['z']
        if self.args:
            site = self.args
        parameters = {
            'a': 'stats',
            'tkn': cfSettings['tkn'],
            'email': cfSettings['email'],
            'z': site,
            'd': '20'
        }
        req = urllib.request.Request(
            "https://www.cloudflare.com/api_json.html", 
            data=urllib.parse.urlencode(parameters).encode('UTF-8')
        )
        stats = urllib.request.urlopen(req)
        req = json.loads(stats.read().decode('utf8'))
        traffic = req['response']['result']['objs'][0]['trafficBreakdown']
        uniq = traffic['uniques']
        views = traffic['pageviews']
        parsed = "Unique visitors: Regular = %s, Threat = %s, Crawler = %s. \nPageviews: Regular = %s, Threat = %s, Crawler = %s." % (
            uniq['regular'],
            uniq['threat'],
            uniq['crawler'],
            views['regular'],
            views['threat'],
            views['crawler']
        )
        self.reply(parsed)

    def purge(self):
        """Purge the CloudFlare caches."""
        cfSettings = self.settingsInstance.settings['commands']['cf']
        site = cfSettings['z']
        if self.args:
            site = self.args
        parameters = {
            'a': 'fpurge_ts',
            'tkn': cfSettings['tkn'],
            'email': cfSettings['email'],
            'z': site,
            'v': '1'
        }
        req = urllib.request.Request(
            "https://www.cloudflare.com/api_json.html",
            data=urllib.parse.urlencode(parameters).encode('UTF-8')
        )
        response = urllib.request.urlopen(req)
        req = json.loads(response.read().decode('utf8'))
        if req['result'] == 'success':
            self.reply('Succesfully purged cache for %s' % (cfSettings['z'],))
        else:
            self.reply(
                'Clearing cache for %s returned: %s' % (
                    cfSettings['z'],
                    req['result']
                )
            )



