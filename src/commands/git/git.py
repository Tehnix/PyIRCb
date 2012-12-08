#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Git commands!

"""

import os
import disutils
import urllib
import shutil


def unpackfile(filepath, path):
    zfile = zipfile.ZipFile(filepath)
    zfile.extractall(path)
    zfile.close()
    
class TempFolder(object):
    def __enter__(self):
        self.path = tempfile.mkdtemp()
        return self.path

    def __exit__(self, type, value, traceback):
        shutil.rmtree(self.path)
        


class Git(object):

    def __init__(self, settingsInstance, commandInstance, cmdName, *args):
        super(Git, self).__init__()
        self.settingsInstance = settingsInstance
        self.commandInstance = commandInstance
        if cmdName is not None:
            if args[0] is not None:
                getattr(self, cmdName)(*args)
            else:
                getattr(self, cmdName)()
    
    def clone(self, *args):
        self.def_dir = "/home/%s/www/" % args[0]
        self.commandInstance.replyWithMessage('Cloning %s to %s...' % (args[1], def_dir))
        self._download(args[1])
            
    def _download(self, url):
        if url[4] != "s":
            self.commandInstance.replyWithMessage("faggot, use HTTPS!")
            return
        s = url[17:]
        utl = "https://nodeload.github.com%s/zip/master" % s
    with TempFolder() as tmp_path:
        packedname = tmp_path + "/tmp.zip"
        urllib.urlretrieve(url, packedname)
        unpackfile(packedname, tmp_path)
        newdir = os.listdir(tmp_path)
        distutils.file_util.copy_file(newdir, self.def_dir)