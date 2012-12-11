#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various utitity methods...

"""

import inspect
import traceback


verbose = False

def stripUsername(username):
    if username[0:1] in ['@', '%', '!']:
        username = username[1:]
    return username

def write(text, outputType="*", priority=1):
    """Write out the given text."""
    if verbose and text != "" or priority > 3 and text != "":
        print("[%s] %s" % (outputType, text,))

def writeException(sysExec):
    """Write out an exception"""
    exc_type, exc_value, exc_traceback = sysExec
    write(
        "\r".join(
            traceback.format_exception(
                exc_type, exc_value, exc_traceback
            )
        )
    )

def toBytes(text):
    """Convert string (unicode) to bytes."""
    try:
        if type(text) != bytes:
            text = bytes(text, 'UTF-8')
    except TypeError:
        text = "\n[WARNING] : Failed to encode unicode!\n"
    return text

def toUnicode(text):
    """Converts bytes to unicode."""
    if type(text) != str:
        try:
            text = str(text, encoding='UTF-8')
        except UnicodeDecodeError:
            text = "\n[WARNING] : Failed to decode bytes!\n"
        except TypeError:
            text = "\n[WARNING] : Failed to decode bytes!\n"
    return text

def getDocstring(targetFunc, targetClass=None):
    """Fetches the docstring of the given function/method."""
    try:
        if targetClass is None:
            return inspect.cleandoc(inspect.getdoc(targetFunc))
        return inspect.cleandoc(inspect.getdoc(getattr(targetClass, targetFunc)))
    except AttributeError:
        return "A docstring couldn't be found!"

def publicMethods(targetClass):
    """Construct a list of all the commands"""
    cmdList = []
    # These are common to the class, but we do not need them
    cmdListIgnores = [
        "daemon", "getName",
        "ident", "is_alive",
        "isAlive", "isDaemon",
        "join", "name",
        "run", "setDaemon",
        "setName", "start"
    ]
    classMembers = inspect.getmembers(targetClass)
    for i in range(len(classMembers)):
        method = classMembers[i][0]
        if not method.startswith("_") and method not in cmdListIgnores:
            cmdList.append(method)
    # Sort the command list alphabetically
    cmdList.sort(key=lambda x: x.lower())
    return ', '.join(cmdList)
