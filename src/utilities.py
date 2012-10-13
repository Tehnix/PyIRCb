#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various utitity methods...

"""

import inspect


def write(text, outputType="*"):
    """Write out the given text."""
    print("[%s] %s" % (outputType, text,))

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
    if targetClass is None:
        return inspect.cleandoc(inspect.getdoc(targetFunc))
    return inspect.cleandoc(inspect.getdoc(getattr(targetClass, targetFunc)))
