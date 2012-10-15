#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CloudFlare command...

"""

import urllib.request
import urllib.parse
import urllib.error
import json

import src.utilities as util

class Cf(object):
    
    def __init__(self, settingsInstance, commandInstance, cmdName, *args):
        super(Cf, self).__init__()
        self.settingsInstance = settingsInstance
        self.commandInstance = commandInstance
        if cmdName is not None:
            if args[0] is not None:
                getattr(self, cmdName)(*args)
            else:
                getattr(self, cmdName)()
    
    def stats(self, *args):
        """Pull out CloudFlare statistics."""
        cfSettings = self.settingsInstance.settings['commands']['cf']
        print(args)
        if args:
            site = ''.join(args)
        else:
            site = cfSettings['z']
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
        parsed = "Unique visitors: Regular = %s, Threat = %s, Crawler = %s. Pageviews: Regular = %s, Threat = %s, Crawler = %s." % (
            uniq['regular'],
            uniq['threat'],
            uniq['crawler'],
            views['regular'],
            views['threat'],
            views['crawler']
        )
        self.commandInstance.replyWithMessage(parsed)

    def purge(self, *args):
        """Purge the CloudFlare caches."""
        cfSettings = self.settingsInstance.settings['commands']['cf']
        if args:
            site = ''.join(args)
        else:
            site = cfSettings['z']
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
            self.commandInstance.replyWithMessage(
                'Succesfully purged cache for %s' % (cfSettings['z'],)
            )
        else:
            self.commandInstance.replyWithMessage(
                'Clearing cache for %s returned: %s' % (cfSettings['z'], req['result'],)
            )



