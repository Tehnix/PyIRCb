#!/usr/bin/python
"""
Run all starting with test

"""

import sys
import os
import nose
import time

def main():
    sys.path.insert(0, os.path.dirname(__file__))
    nose.core.TestProgram(exit=False)

if __name__ == '__main__':
    main()