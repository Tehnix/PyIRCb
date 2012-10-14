"""
Testing src/utilities.py

"""

import unittest
import ast

import src.utilities as util


class UtilitiesTest(unittest.TestCase):
    
    def test_that_toBytes_converts_unicode_to_bytes(self):
        testString = u'This is a string'
        newString = util.toBytes(testString)
        self.assertNotEqual(testString, newString)
        self.assertEqual(type(newString), bytes)
    
    def test_that_toUnicode_converts_bytes_to_unicode(self):
        testString = bytes('This is a string')
        newString = util.toUnicode(testString)
        self.assertEqual(type(newString), str)
    
    def test_that_getDocstring_can_get_the_docstring(self):
        def some_random_method():
            """This is my docstring...."""
            pass
        testDocstring = """This is my docstring...."""
        docstring = util.getDocstring(some_random_method)
        self.assertEqual(testDocstring, docstring)


if __name__ == '__main__':
    unittest.main()